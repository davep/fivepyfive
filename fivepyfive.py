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
"""

from pathlib import Path
from typing import Final, cast

from textual.containers import Horizontal
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Footer, Button, Static
from textual.css.query import DOMQuery
from textual.reactive import reactive


class WinnerMessage(Static):
    """Widget to tell the user they have won."""

    #: The minimum number of moves you can solve the puzzle in.
    MIN_MOVES: Final = 14

    @staticmethod
    def _plural(value: int) -> str:
        return "" if value == 1 else "s"

    def show(self, moves: int):
        """Show the winner message."""
        self.update(
            "W I N N E R !\n\n\n"
            f"You solved the puzzle in {moves} move{self._plural(moves)}." + (
                (
                    f" It is possible to solve the puzzle in {self.MIN_MOVES}, "
                    f"you were {moves - self.MIN_MOVES} move{self._plural(moves - self.MIN_MOVES)} over."
                ) if moves > self.MIN_MOVES else
                " Well done! That's the minimum number of moves to solve the puzzle!"
            )
        )
        self.add_class("visible")

    def hide(self):
        """Hide the winner message."""
        self.remove_class("visible")


class GameHeader(Widget):
    """Header for the game.

    Comprises of the title (``#app-title``), the number of moves ``#moves``
    and the count of how many cells are turned on (``#progress``).
    """

    #: Keep track of how many moves the player has made.
    moves = reactive(0)

    #: Keep track of how many cells are turned on.
    on = reactive(0)

    def compose(self) -> ComposeResult:
        """Compose the game header."""
        yield Horizontal(
            Static(self.app.title, id="app-title"),
            Static(id="moves"),
            Static(id="progress"),
        )

    def watch_moves(self, moves: int):
        """Watch the moves reactive and update when it changes."""
        self.query_one("#moves", Static).update(f"Moves: {moves}")

    def watch_on(self, on: int):
        """Watch the on-count reactive and update when it changes."""
        self.query_one("#progress", Static).update(f"On: {on}")


class GameCell(Button):
    """Individual playable cell in the game."""

    @staticmethod
    def at(row: int, col: int) -> str:
        return f"cell-{row}-{col}"

    def __init__(self, row: int, col: int) -> None:
        """Initialise the game cell."""
        super().__init__("", id=self.at(row, col))


class GameGrid(Widget):
    """The main playable grid of game cells."""

    def compose(self) -> ComposeResult:
        """Compose the game grid."""
        for row in range(Game.SIZE):
            for col in range(Game.SIZE):
                yield GameCell(row, col)


class Game(Screen):
    """Main 5x5 game grid screen."""

    #: The size of the game grid. Clue's in the name really.
    SIZE = 5

    #: The bindings for the main game grid.
    BINDINGS = [("n", "reset", "New Game"), ("q", "quit", "Quit")]

    @property
    def on_cells(self) -> DOMQuery[GameCell]:
        """The collection of cells that are currently turned on.

        :type: DOMQuery[GameCell]
        """
        return cast(DOMQuery[GameCell], self.query("GameCell.on"))

    @property
    def on_count(self) -> int:
        """The number of cells that are turned on.

        :type: int
        """
        return len(self.on_cells)

    @property
    def all_on(self) -> bool:
        """Are all the cells turned on?

        :type: bool
        """
        return self.on_count == self.SIZE * self.SIZE

    def game_playable(self, playable: bool) -> None:
        """Mark the game as playable, or not.

        :param bool playable: Should the game currently be playable?
        """
        for cell in self.query(GameCell):
            cell.disabled = not playable

    def new_game(self) -> None:
        """Start a new game."""
        self.query_one(GameHeader).moves = 0
        self.on_cells.remove_class("on")
        self.query_one(WinnerMessage).hide()
        self.game_playable(True)
        self.toggle_cells(
            self.query_one(f"#{GameCell.at(self.SIZE // 2,self.SIZE // 2 )}", GameCell)
        )

    def compose(self) -> ComposeResult:
        """Compose the application screen."""
        yield GameHeader()
        yield GameGrid()
        yield Footer()
        yield WinnerMessage()

    def toggle_cell(self, row: int, col: int) -> None:
        """Toggle an individual cell, but only if it's on bounds.

        :param int row: The row of the cell to toggle.
        :param int col: The column of the cell to toggle.

        If the row and column would place the cell out of bounds for the
        game grid, this function call is a no-op. That is, it's safe to call
        it with an invalid cell coordinate.
        """
        if 0 <= row <= (self.SIZE - 1) and 0 <= col <= (self.SIZE - 1):
            self.query_one(f"#{GameCell.at(row, col)}", GameCell).toggle_class("on")

    def toggle_cells(self, cell: GameCell) -> None:
        """Toggle a 5x5 pattern around the given cell.

        :param GameCell cell: The cell to toggle the cells around.
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
            self.query_one(GameHeader).on = self.on_count

    def make_move_on(self, cell: GameCell) -> None:
        """Make a move on the given cell.

        All relevant cells around the given cell are toggled as per the
        game's rules.
        """
        self.toggle_cells(cell)
        self.query_one(GameHeader).moves += 1
        if self.all_on:
            self.query_one(WinnerMessage).show(self.query_one(GameHeader).moves)
            self.game_playable(False)

    def on_button_pressed(self, event: GameCell.Pressed) -> None:
        """React to a press of a button on the game grid."""
        self.make_move_on(cast(GameCell, event.button))

    def action_reset(self) -> None:
        """Reset the game."""
        self.new_game()

    def on_mount(self) -> None:
        """Get the game started when we first mount."""
        self.new_game()


class FiveByFive(App[None]):
    """Main 5x5 application class."""

    #: The name of the stylesheet for the app.
    CSS_PATH = Path(__file__).with_suffix(".css")

    def __init__(self) -> None:
        """Constructor."""
        super().__init__(title="5x5 -- A little annoying puzzle")

    def on_mount(self) -> None:
        """Set up the application on startup."""
        self.push_screen(Game())


if __name__ == "__main__":
    FiveByFive().run()

### fivepyfive.py ends here
