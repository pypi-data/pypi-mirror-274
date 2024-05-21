from rich.console import RenderableType
from textual import screen
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Label


class ModalScreen(screen.ModalScreen[screen.ScreenResultType]):
    DEFAULT_CSS = """
    ModalScreen {
        align: center middle;
    }
    .modal_container {
        max-width: 80;
        height: auto;
        border: round gray;
    }
    """

    BINDINGS = [
        Binding("q,escape", "quit", "Close"),
    ]

    def __init__(self, *, id: str | None = None):
        super().__init__(id=id)

    def compose_modal(self) -> ComposeResult:
        raise NotImplementedError()

    def compose(self) -> ComposeResult:
        self.vertical = Vertical(*self.compose_modal(), classes="modal_container")
        yield self.vertical

    def action_quit(self):
        self.app.pop_screen()


class ModalTitle(Label):
    DEFAULT_CSS = """
    ModalTitle {
        width: 100%;
        text-align: center;
        background: $accent;

        &.error {
            background: $error;
        }
    }
    """

    def __init__(self, renderable: RenderableType, error: bool = False):
        super().__init__(
            renderable,
            markup=False,
            classes="error" if error else ""
        )
