"""The game screen."""

##############################################################################
# Python imports.
from typing import Final, cast

##############################################################################
# Textual imports.
from textual.app       import ComposeResult
from textual.screen    import Screen
from textual.binding   import Binding
from textual.css.query import DOMQuery
from textual.widgets   import Footer

##############################################################################
# Local imports.
from .game_header import GameHeader
from .game_cell   import GameCell
from .game_grid   import GameGrid
from .winner      import WinnerMessage

##############################################################################
class Game( Screen ):
    """Main 5x5 game grid screen."""

    SIZE: Final = 5
    """int: The size of the game grid. Clue's in the name really."""

    BINDINGS = [
        Binding( "n",             "new_game",            "New Game" ),
        Binding( "question_mark", "push_screen('help')", "Help", key_display="?" ),
        Binding( "q",             "quit",                "Quit" ),
        Binding( "up,w,k",        "navigate(-1,0)",      "Move Up",    False ),
        Binding( "down,s,j",      "navigate(1,0)",       "Move Down",  False ),
        Binding( "left,a,h",      "navigate(0,-1)",      "Move Left",  False ),
        Binding( "right,d,l",     "navigate(0,1)",       "Move Right", False ),
        Binding( "space",         "move",                "Toggle",     False )
    ]
    """list[ Binding ]: The bindings for the main game grid."""

    @property
    def filled_cells( self ) -> DOMQuery[ GameCell ]:
        """DOMQuery[ GameCell ]: The collection of cells that are currently turned on."""
        return cast( DOMQuery[ GameCell ], self.query( "GameCell.filled" ) )

    @property
    def filled_count( self ) -> int:
        """int: The number of cells that are currently filled."""
        return len( self.filled_cells )

    @property
    def all_filled( self ) -> bool:
        """bool: Are all the cells filled?"""
        return self.filled_count == self.SIZE * self.SIZE

    def game_playable( self, playable: bool ) -> None:
        """Mark the game as playable, or not.

        Args:
            playable (bool): Should the game currently be playable?
        """
        for cell in self.query( GameCell ):
            cell.disabled = not playable

    def cell( self, row: int, col: int ) -> GameCell:
        """Get the cell at a given location.

        Args:
            row (int): The row of the cell to get.
            col (int): The column of the cell to get.

        Returns:
            GameCell: The cell at that location.
        """
        return self.query_one( f"#{GameCell.at( row, col )}", GameCell )

    def compose( self ) -> ComposeResult:
        """Compose the game screen.

        Returns:
            ComposeResult: The result of composing the game screen.
        """
        self.header = GameHeader()
        self.grid   = GameGrid( self.SIZE )
        self.winner = WinnerMessage()
        yield self.header
        yield self.grid
        yield self.winner
        yield Footer()

    def toggle_cell( self, row: int, col: int ) -> None:
        """Toggle an individual cell, but only if it's in bounds.

        If the row and column would place the cell out of bounds for the
        game grid, this function call is a no-op. That is, it's safe to call
        it with an invalid cell coordinate.

        Args:
            row (int): The row of the cell to toggle.
            col (int): The column of the cell to toggle.
        """
        if 0 <= row <= ( self.SIZE - 1 ) and 0 <= col <= ( self.SIZE - 1 ):
            self.cell( row, col ).toggle_class( "filled" )

    _PATTERN: Final = ( -1, 1, 0, 0, 0 )

    def toggle_cells( self, cell: GameCell ) -> None:
        """Toggle a 5x5 pattern around the given cell.

        Args:
            cell (GameCell): The cell to toggle the cells around.
        """
        for row, col in zip( self._PATTERN, reversed( self._PATTERN ) ):
            self.toggle_cell( cell.row + row, cell.col + col )
        self.header.filled = self.filled_count

    def make_move_on( self, cell: GameCell ) -> None:
        """Make a move on the given cell.

        All relevant cells around the given cell are toggled as per the
        game's rules.

        Args:
            cell (GameCell): The cell to make a move on
        """
        self.toggle_cells( cell )
        self.header.moves += 1
        if self.all_filled:
            self.winner.show( self.header.moves )
            self.game_playable( False )

    def on_button_pressed( self, event: GameCell.Pressed ) -> None:
        """React to a press of a button on the game grid.

        Args:
            event (GameCell.Pressed): The event to react to.
        """
        self.make_move_on( cast( GameCell, event.button ) )

    def action_new_game( self ) -> None:
        """Start a new game."""
        self.header.moves = 0
        self.filled_cells.remove_class( "filled" )
        self.winner.hide()
        middle = self.cell( self.SIZE // 2, self.SIZE // 2 )
        self.toggle_cells( middle )
        self.set_focus( middle )
        self.game_playable( True )

    def action_navigate( self, row: int, col: int ) -> None:
        """Navigate to a new cell by the given offsets.

        Args:
            row (int): The row of the cell to navigate to.
            col (int): The column of the cell to navigate to.
        """
        if isinstance( self.focused, GameCell ):
            self.set_focus(
                self.cell(
                    ( self.focused.row + row ) % self.SIZE,
                    ( self.focused.col + col ) % self.SIZE,
                )
            )

    def action_move( self ) -> None:
        """Make a move on the current cell."""
        if isinstance( self.focused, GameCell ):
            self.focused.press()

    def on_mount( self ) -> None:
        """Get the game started when we first mount."""
        self.action_new_game()

### game_screen.py ends here
