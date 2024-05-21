from jupyter_server.serverapp import ServerApp

from .handlers import GlobbingExtensionHandler

from .version import __version__

def _load_jupyter_server_extension(serverapp: ServerApp):
    """
    This function is called when the extension is loaded.
    """
    handlers = [("/api/globbing/(.*)", GlobbingExtensionHandler)]
    serverapp.web_app.add_handlers(".*$", handlers)
