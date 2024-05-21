from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import TabPane, TabbedContent

from tooi.api.timeline import HomeTimeline, Timeline
from tooi.data.instance import InstanceInfo
from tooi.messages import ShowStatusMessage
from tooi.screens.compose import ComposeScreen
from tooi.screens.goto import GotoScreen
from tooi.screens.instance import InstanceScreen
from tooi.tabs.search import SearchTab
from tooi.tabs.timeline import TimelineTab
from tooi.widgets.header import Header
from tooi.widgets.status_bar import StatusBar


class MainScreen(Screen[None]):
    """
    The primary app screen, which contains tabs for content.
    """

    DEFAULT_CSS = """
    Tabs {
        height: 1;

        #tabs-list {
           min-height: 1;
        }

        Tab {
            height: 1;
            padding: 0 2 0 2;
        }
    }

    TabPane {
        padding: 0;
    }

    Underline {
        display: none
    }

    StatusBar {
        dock: bottom;
    }
    """

    BINDINGS = [
        Binding("c", "compose", "Compose"),
        Binding("g", "goto", "Goto"),
        Binding("i", "show_instance", "Instance"),
        Binding("ctrl+d,ctrl+w", "close_current_tab"),
        Binding("ctrl+pageup", "previous_tab"),
        Binding("ctrl+pagedown", "next_tab"),
        Binding(".", "refresh_timeline", "Refresh"),
        Binding("/", "open_search_tab", "Search"),
        Binding("1", "select_tab(1)", show=False),
        Binding("2", "select_tab(2)", show=False),
        Binding("3", "select_tab(3)", show=False),
        Binding("4", "select_tab(4)", show=False),
        Binding("5", "select_tab(5)", show=False),
        Binding("6", "select_tab(6)", show=False),
        Binding("7", "select_tab(7)", show=False),
        Binding("8", "select_tab(8)", show=False),
        Binding("9", "select_tab(9)", show=False),
        Binding("0", "select_tab(10)", show=False),
    ]

    def __init__(self, instance: InstanceInfo):
        super().__init__()
        self.instance = instance

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header("toot")
            # Start with the home timeline
            with TabbedContent():
                yield TimelineTab(self.instance, HomeTimeline(self.instance))
            yield StatusBar()

    async def open_timeline_tab(self, timeline: Timeline, initial_focus: str | None = None):
        tab = TimelineTab(self.instance, timeline, initial_focus=initial_focus)
        tc = self.query_one(TabbedContent)

        with self.app.batch_update():
            await tc.add_pane(tab)
            tc.active = tab.id
            self.on_tab_pane_activated(tab)

    def on_show_status_message(self, message: ShowStatusMessage):
        status_bar = self.query_one(StatusBar)

        if message.text is None:
            status_bar.clear()
        else:
            status_bar.set_message(message.text, message.timeout)

    # This is triggered when a tab is clicked, but not when the tab is activated
    # programatically, see: https://github.com/Textualize/textual/issues/4150
    @on(TabbedContent.TabActivated)
    def on_tab_activated(self, message: TabbedContent.TabActivated):
        tc = self.query_one(TabbedContent)
        tab_pane = tc.get_pane(message.tab)
        self.on_tab_pane_activated(tab_pane)

    def on_tab_pane_activated(self, tab_pane: TabPane):
        if isinstance(tab_pane, TimelineTab):
            tab_pane.batch_show_update()

    @on(TimelineTab.EventUpdated)
    def on_event_updated(self, message: TimelineTab.EventUpdated):
        for tab in self.query(TimelineTab):
            tab.update_event(message.event)

    @on(TimelineTab.EventDeleted)
    def on_event_deleted(self, message: TimelineTab.EventDeleted):
        for tab in self.query(TimelineTab):
            tab.remove_event(message.event)

    def action_compose(self):
        self.app.push_screen(ComposeScreen(self.instance))

    @work
    async def action_goto(self):
        if message := await self.app.push_screen_wait(GotoScreen()):
            self.post_message(message)

    async def action_show_instance(self):
        self.app.push_screen(InstanceScreen(self.instance))

    def action_select_tab(self, tabnr: int):
        tc = self.query_one(TabbedContent)
        tabs = tc.query(TabPane)
        if tabnr <= len(tabs):
            with self.app.batch_update():
                tab = tabs[tabnr - 1]
                tc.active = tab.id
                self.on_tab_pane_activated(tab)

    def action_previous_tab(self):
        self._change_active_index(-1)

    def action_next_tab(self):
        self._change_active_index(1)

    def _change_active_index(self, delta: int):
        tc = self.query_one(TabbedContent)
        panes = tc.query(TabPane).nodes
        if len(panes) < 2:
            return

        active_index = self._get_active_pane_index(tc, panes)
        if active_index is None:
            return

        index = (active_index + delta) % len(panes)
        pane = panes[index]
        if pane.id is None:
            return

        tc.active = pane.id
        self.on_tab_pane_activated(pane)

    def _get_active_pane_index(self, tc: TabbedContent, panes: list[TabPane]) -> int | None:
        for index, pane in enumerate(panes):
            if pane.id == tc.active:
                return index

    async def action_close_current_tab(self):
        tc = self.query_one(TabbedContent)
        # Don't close last tab
        if tc.tab_count > 1:
            with self.app.batch_update():
                await tc.remove_pane(tc.active)
                if tc.active:
                    tab = tc.get_pane(tc.active)
                    self.on_tab_pane_activated(tab)

    async def action_refresh_timeline(self):
        tc = self.query_one(TabbedContent)
        await tc.get_pane(tc.active).refresh_timeline()

    async def action_open_search_tab(self):
        tc = self.query_one(TabbedContent)
        tab = SearchTab("Search")
        await tc.add_pane(tab)
        tc.active = tab.id
        self.on_tab_pane_activated(tab)
