"""Simple version of 5x5, developed for/with Textual.

5x5 is one of my little go-to problems to help test new development
environments and tools, especially those that are very visual. See
http://5x5.surge.sh/ as an example of the game. Versions I've written
include:

https://github.com/davep/5x5.xml
https://github.com/davep/Chrome-5x5
https://github.com/davep/5x5-Palm
https://github.com/davep/5x5.el
https://github.com/davep/5x5-react

amongst others (they're just the ones that I still have code for and which
are on GitHub).

NOTE: For the moment docstrings and type annotations will be lacking or
possibly wrong. In part this is because, as of the time of writing, I've got
no docs to go on yet as to the full extent of the API or the types involved.

ALSO NOTE: The choices of widget, colour, styling, etc, are likely to not be
my ideal or final choice. Again, guesswork and example-reading are the guide
here; a lot of this will change when documentation is available.
"""

from pathlib import Path

from textual.containers import Horizontal
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Footer, Button, Static
from textual.css.query import DOMQuery


class GameHeader(Widget):
    """Header for the game.

    Comprises of the title (``#app-title``), the number of moves ``#moves``
    and the count of how many cells are turned on (``#progress``).
    """

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Static(self.app.title, id="app-title"),
            Static(id="moves"),
            Static(id="progress"),
        )


class FiveByFive(App[None]):
    """Main 5x5 application class."""

    #: The name of the stylesheet for the app. The cast to a str is
    # temporary while CSS_PATH doesn't support PurePath.
    CSS_PATH = str(Path(__file__).with_suffix(".css"))

    #: The size of the game grid. Clue's in the name really.
    SIZE = 5

    BINDINGS = [("r", "reset()", "Reset"), ("q", "quit()", "Quit")]

    def __init__(self) -> None:
        super().__init__(title="5x5 -- A little annoying puzzle")

    @property
    def on_cells(self) -> DOMQuery[Button]:
        """The collection of cells that are currently turned on.

        :type: DOMQuery[Button]
        """
        return self.query("Button.on")

    @property
    def on_count(self) -> int:
        """The number of cells that are turned on.

        :type: int
        """
        return len(self.on_cells)

    def new_game(self) -> None:
        """Start a new game."""
        self.moves = 0
        self.on_cells.remove_class("on")
        self.toggle_cells(
            self.query_one(f"#cell-{ self.SIZE // 2 }-{ self.SIZE // 2}", Button)
        )

    def compose(self) -> ComposeResult:
        """Compose the application screen."""
        yield GameHeader()
        for row in range(self.SIZE):
            yield Horizontal(
                *[Button("", id=f"cell-{row}-{col}") for col in range(self.SIZE)]
            )
        yield Footer()

        # TODO: I suspect there's a problem here in that I should not be
        # trying to tinker with the DOM inside compose. The setting up of a
        # new game (and so flipping classes on the buttons) seems to work,
        # but updating the game header doesn't because Textual claims it
        # can't find the #moves Static yet. Presumably there's a hook/event
        # that is "the DOM is ready, go have fun" but I've not found it yet.
        self.new_game()
        # ...hence this is commented out for now, and the above is suspect.
        # self.refresh_state_of_play()

    def refresh_state_of_play(self) -> None:
        """Refresh the details of the current state of play."""
        self.query_one("#moves", Static).update(f"Moves: {self.moves}")
        self.query_one("#progress", Static).update(
            "Winner!" if self.on_count == (self.SIZE**2) else f"On: {self.on_count}"
        )

    def toggle_cell(self, row: int, col: int) -> None:
        """Toggle an individual cell, but only if it's on bounds.

        :param int row: The row of the cell to toggle.
        :param int col: The column of the cell to toggle.

        If the row and column would place the cell out of bounds for the
        game grid, this function call is a no-op. That is, it's safe to call
        it with an invalid cell coordinate.
        """
        if 0 <= row <= (self.SIZE - 1) and 0 <= col <= (self.SIZE - 1):
            self.query_one(f"Button#cell-{row}-{col}", Button).toggle_class("on")

    def toggle_cells(self, cell: Button) -> None:
        """Toggle a 5x5 pattern around the given cell.

        :param Button cell: The cell to toggle the buttons around.
        """
        # Abusing the ID as a data- attribute too (or a cargo instance
        # variable if you're old enough to have worked with Clipper).
        # Textual doesn't have anything like it at the moment:
        #
        # https://twitter.com/davepdotorg/status/1555822341170597888
        #
        # but given the reply it may do at some point.
        if cell.id:
            row, col = map(int, cell.id.split("-")[1:])
            self.toggle_cell(row - 1, col)
            self.toggle_cell(row + 1, col)
            self.toggle_cell(row, col)
            self.toggle_cell(row, col - 1)
            self.toggle_cell(row, col + 1)

    def make_move_on(self, cell: Button) -> None:
        """Make a move on the given cell.

        All relevant cells around the given cell are toggled as per the
        game's rules.
        """
        self.toggle_cells(cell)
        self.moves += 1
        self.refresh_state_of_play()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """React to a press of a button on the game grid."""
        self.make_move_on(event.button)

    def action_reset(self) -> None:
        """Reset the game."""
        self.new_game()
        self.refresh_state_of_play()


if __name__ == "__main__":
    FiveByFive().run()

### fivepyfive.py ends here
