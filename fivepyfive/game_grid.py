"""Provides the main grid of the game."""

##############################################################################
# Textual imports.
from textual.app    import ComposeResult
from textual.widget import Widget

##############################################################################
# Local imports.
from .game_cell import GameCell

##############################################################################
class GameGrid( Widget ):
    """The main playable grid of game cells."""

    def __init__( self, size: int ) -> None:
        """Initialise the game grid.

        Args:
            size: The size of the grid.
        """
        super().__init__()
        self._game_size = size

    def compose( self ) -> ComposeResult:
        """Compose the game grid.

        Returns:
            The result of composing the game grid.
        """
        for row in range( self._game_size ):
            for col in range( self._game_size ):
                yield GameCell( row, col )

### game_grid.py ends here
