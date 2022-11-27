"""The help screen for the application."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Textual imports.
from textual.app     import ComposeResult
from textual.screen  import Screen
from textual.binding import Binding
from textual.widgets import Static

##############################################################################
# Rich imports.
from rich.markdown import Markdown

##############################################################################
class Help( Screen ):
    """The help screen for the application."""

    BINDINGS = [
        Binding( "escape,space,q,question_mark", "pop_screen", "Close" )
    ]
    """Bindings for the help screen."""

    def compose( self ) -> ComposeResult:
        """Compose the game's help.

        Returns:
            ComposeResult: The result of composing the help screen.
        """
        yield Static( Markdown( ( Path( __file__  ).parent / "help.md" ).read_text() ) )

### help_screen.py ends here
