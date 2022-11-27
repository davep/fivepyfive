"""Provides the winner message."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# Textual imports.
from textual.widgets import Static

##############################################################################
class WinnerMessage( Static ):
    """Widget to tell the user they have won."""

    MIN_MOVES: Final = 14
    """int: The minimum number of moves you can solve the puzzle in."""

    @staticmethod
    def _plural( value: int ) -> str:
        return "" if value == 1 else "s"

    def show( self, moves: int ) -> None:
        """Show the winner message.

        Args:
            moves (int): The number of moves required to win.
        """
        self.update(
            "W I N N E R !\n\n\n"
            f"You solved the puzzle in {moves} move{self._plural( moves )}."
            + (
                (
                    f" It is possible to solve the puzzle in {self.MIN_MOVES}, "
                    f"you were {moves - self.MIN_MOVES} move{self._plural( moves - self.MIN_MOVES )} over."
                )
                if moves > self.MIN_MOVES
                else " Well done! That's the minimum number of moves to solve the puzzle!"
            )
        )
        self.add_class( "visible" )

    def hide( self ) -> None:
        """Hide the winner message."""
        self.remove_class( "visible" )

### winner.py ends here
