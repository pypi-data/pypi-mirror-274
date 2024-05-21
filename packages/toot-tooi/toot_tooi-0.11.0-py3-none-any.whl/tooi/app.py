import asyncio
import re
import shlex
import webbrowser

from os import path
from pathlib import Path
from textual import work
from textual.app import App
from textual.screen import ModalScreen
from urllib.parse import urlparse

from tooi import messages
from tooi.api.streaming import InstanceStreamer
from tooi.api.timeline import FederatedTimeline, ContextTimeline, NotificationTimeline
from tooi.api.timeline import Timeline, HomeTimeline, LocalTimeline, TagTimeline, AccountTimeline
from tooi.asyncio import create_async_context, set_async_context
from tooi.context import get_context, is_mine
from tooi.data.instance import get_instance_info
from tooi.screens.account import AccountScreen
from tooi.screens.compose import ComposeScreen
from tooi.screens.goto import GotoHashtagScreen
from tooi.screens.help import HelpScreen
from tooi.screens.loading import LoadingScreen
from tooi.screens.main import MainScreen
from tooi.screens.messagebox import MessageBox
from tooi.screens.source import SourceScreen
from tooi.screens.status_context import StatusMenuScreen
from tooi.settings import get_stylesheet_path
from tooi.utils.file import FilePickerError, pick_file
from tooi.utils.temp import download_temporary
from tooi.widgets.dialog import ConfirmationDialog
from tooi.widgets.link import Link


class TooiApp(App[None]):
    TITLE = "tooi"
    SUB_TITLE = "1.0.0"
    SCREENS = {"loading": LoadingScreen()}
    CSS_PATH = "app.css"

    BINDINGS = [
        ("?", "help", "Help"),
        ("q", "pop_or_quit", "Quit"),
    ]

    def __init__(self):
        super().__init__(css_path=self._get_css_paths())
        set_async_context(create_async_context(self))

    def _get_css_paths(self):
        base_css = "app.css"
        user_css = get_stylesheet_path()
        return [base_css, user_css] if path.exists(user_css) else [base_css]

    async def on_mount(self):
        self.push_screen("loading")
        self.context = get_context()
        self.instance = await get_instance_info()
        self.instance.streamer = InstanceStreamer(self.instance)
        self.tabs = MainScreen(self.instance)
        self.switch_screen(self.tabs)

    def on_status_edit(self, message: messages.StatusEdit):
        if is_mine(message.status):
            self.push_screen(ComposeScreen(
                self.instance,
                edit=message.status,
                edit_source=message.status_source))

    async def confirm(
        self,
        title: str,
        *,
        text: str | None = None,
        confirm_label: str = "Confirm",
        cancel_label: str = "Cancel"
    ) -> bool:
        dialog = ConfirmationDialog(
            modal_title=title,
            modal_text=text,
            confirm_label=confirm_label,
            cancel_label=cancel_label,
        )
        return await self.push_screen_wait(dialog)

    @work
    async def action_pop_or_quit(self):
        if len(self.screen_stack) > 2:
            self.pop_screen()
        else:
            if await self.confirm("Quit tooi?", confirm_label="Quit"):
                self.exit()

    def action_help(self):
        self.push_screen(HelpScreen())

    def close_modals(self):
        while isinstance(self.screen, ModalScreen):
            self.pop_screen()

    @work
    async def on_show_account(self, message: messages.ShowAccount):
        self.close_modals()
        if to_post := await self.push_screen_wait(AccountScreen(message.account)):
            self.post_message(to_post)

    def on_show_source(self, message: messages.ShowSource):
        self.push_screen(SourceScreen(message.status))

    def on_show_status_menu(self, message: messages.ShowStatusMenu):
        self.push_screen(StatusMenuScreen(message.status))

    def on_status_reply(self, message: messages.StatusReply):
        self.push_screen(ComposeScreen(self.instance, message.status))

    @work
    async def on_show_hashtag_picker(self):
        if hashtag := await self.push_screen_wait(GotoHashtagScreen()):
            self.post_message(messages.GotoHashtagTimeline(hashtag))

    async def on_show_thread(self, message: messages.ShowThread):
        # TODO: add footer message while loading statuses
        timeline = ContextTimeline(self.instance, message.status.original)
        # TODO: composing a status: event id by hand is probably not ideal.
        await self.tabs.open_timeline_tab(
                timeline,
                initial_focus=f"status:{message.status.original.id}")

    async def on_goto_home_timeline(self):
        # TODO: add footer message while loading statuses
        await self._open_timeline(HomeTimeline(self.instance))

    async def on_goto_personal_timeline(self):
        timeline = await AccountTimeline.from_name(self.instance, self.context.auth.acct)
        await self._open_timeline(timeline)

    async def on_goto_account_timeline(self, message: messages.GotoAccountTimeline):
        timeline = AccountTimeline(self.instance, message.account.acct, message.account.id)
        await self._open_timeline(timeline)

    async def on_goto_local_timeline(self):
        await self._open_timeline(LocalTimeline(self.instance))

    async def on_goto_federated_timeline(self):
        await self._open_timeline(FederatedTimeline(self.instance))

    async def on_goto_hashtag_timeline(self, message: messages.GotoHashtagTimeline):
        await self._open_timeline(TagTimeline(self.instance, hashtag=message.hashtag))

    async def on_show_notifications(self):
        await self.tabs.open_timeline_tab(NotificationTimeline(self.instance))

    async def on_show_images(self, message: messages.ShowImages):
        self.show_images(message.urls)

    async def on_show_error(self, message: messages.ShowError):
        self.push_screen(MessageBox(message.title, message.message, error=True))

    async def _open_timeline(self, timeline: Timeline):
        await self.tabs.open_timeline_tab(timeline)

    async def on_link_clicked(self, message: Link.Clicked):
        parsed = urlparse(message.url)

        # Hashtag
        if m := re.match(r"/tags/(\w+)", parsed.path):
            hashtag = m.group(1)
            await self._open_timeline(TagTimeline(self.instance, hashtag))
        else:
            # TODO: improve link handling
            webbrowser.open(message.url)

    @work(group="show_images")
    async def show_images(self, urls: list[str]):
        """
        Open a local image viewer to display the given images, which should be a list of URLs.
        This returns immediately and starts the work in a background thread.
        """
        if not (viewer := self.context.config.media.image_viewer):
            self.post_message(messages.ShowError("Error", "No image viewer has been configured"))
            return

        async with download_temporary(urls) as (tempdir, tempfiles):
            args = " ".join(map(shlex.quote, tempfiles))
            cmd = f"{viewer} {args}"

            # Spawn the image viewer.
            process = await asyncio.create_subprocess_shell(cmd)
            # ... and wait for it to exit.
            await process.communicate()

    async def pick_file(self) -> Path | None:
        # TODO: this is not ideal because it needs to stop the app
        # Consider alternatives:
        # - a textual file picker
        # - using a builtin terminal like this one:
        #   https://github.com/mitosch/textual-terminal
        with self.suspend():
            try:
                return await pick_file()
            except FilePickerError as ex:
                self.post_message(messages.ShowError("File picker failed", str(ex)))
