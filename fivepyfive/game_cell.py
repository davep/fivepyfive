"""Provides an individual cell in the game."""

##############################################################################
# Textual imports.
from textual.widgets import Button

##############################################################################
class GameCell( Button ):
    """Individual playable cell in the game."""

    @staticmethod
    def at( row: int, col: int ) -> str:
        """Get the ID of the cell at the given location.

        Args:
            row: The row of the cell.
            col: The column of the cell.

        Returns:
            A string ID for the cell.
        """
        return f"cell-{row}-{col}"

    def __init__( self, row: int, col: int ) -> None:
        """Initialise the game cell.

        Args:
            row: The row of the cell.
            col: The column of the cell.
        """
        super().__init__( "", id=self.at( row, col ) )
        self.row = row
        self.col = col

### game_cell.py ends here
