"""Header widget for the game."""

##############################################################################
# Textual imports.
from textual.app        import ComposeResult
from textual.widget     import Widget
from textual.reactive   import reactive
from textual.widgets    import Static
from textual.containers import Horizontal

##############################################################################
class GameHeader( Widget ):
    """Header for the game.

    Comprises of the title (``#app-title``), the number of moves ``#moves``
    and the count of how many cells are turned on (``#progress``).
    """

    moves = reactive( 0 )
    """Keep track of how many moves the player has made."""

    filled = reactive( 0 )
    """Keep track of how many cells are filled."""

    def compose( self ) -> ComposeResult:
        """Compose the game header.

        Returns:
            The result of composing the game header.
        """
        self.move_count = Static( id="moves" )
        self.progress   = Static( id="progress" )
        yield Horizontal(
            Static( self.app.title, id="app-title" ), self.move_count, self.progress
        )

    def watch_moves( self, moves: int ) -> None:
        """Watch the moves reactive and update when it changes.

        Args:
            moves: The number of moves made.
        """
        self.move_count.update( f"Moves: {moves}" )

    def watch_filled( self, filled: int ) -> None:
        """Watch the on-count reactive and update when it changes.

        Args:
            filled: The number of cells that are currently on.
        """
        self.progress.update( f"Filled: {filled}" )

### game_header.py ends here
