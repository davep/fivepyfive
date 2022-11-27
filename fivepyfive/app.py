"""The main app class for the application."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app     import App
from textual.binding import Binding

##############################################################################
# Local imports.
from .game_screen import Game
from .help_screen import Help

##############################################################################
class FiveByFive( App[ None ] ):
    """Main 5x5 application class."""

    CSS_PATH = Path( "fivepyfive.css" )
    """Path: The path to the style sheet for the application."""

    SCREENS = {
        "game": Game,
        "help": Help
    }
    """Screen collection for the application."""

    BINDINGS = [
        Binding( "t", "toggle_dark", "Toggle Dark Mode" )
    ]
    """list[ Binding ]: App-level bindings."""

    TITLE = "5x5 -- A little annoying puzzle"
    """str: The title of the app."""

    def on_mount( self ) -> None:
        """Set up the application on startup."""
        self.push_screen( "game" )

##############################################################################
def run() -> None:
    """Run the application."""
    FiveByFive().run()

### app.py ends here
