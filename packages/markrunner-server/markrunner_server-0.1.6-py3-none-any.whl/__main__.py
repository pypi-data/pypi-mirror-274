"""
JupyterLab Server Application for Markrunner

=============================================

Sample code using `LabServerApp`:
https://github.com/jupyterlab/jupyterlab/blob/main/packages/services/examples/browser/main.py
Config options for `ServerApp`:
https://github.com/jupyter-server/jupyter_server/blob/main/jupyter_server/serverapp.py
"""

# NOTE:
# Markrunner publishes this package to PyPI
# so that the rest of dependencies can be installed easily via pip.
# Importing this file as a script and directly running from the Node process
# is also possible but since they will need to install the Jupyter dependencies anyway,
# it is better to publish this as an independent package.

import os

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
from jupyterlab_server import LabServerApp

__version__ = "0.1.6"


def _jupyter_server_extension_points():
    return [{"module": __name__, "app": MarkrunnerApp}]


class InfoHandler(ExtensionHandlerMixin, JupyterHandler):
    def get(self):
        return self.write({"name": "markrunner-server"})


class StopHandler(ExtensionHandlerMixin, JupyterHandler):
    # NOTE:
    # This intentionally uses the `GET`` method to circumvent the CSRF protection.
    # This makes sense because the Markrunner plugin should be able to terminate any Markrunner server instance
    # launched by anyone, regardless of the token.
    def get(self):
        self.finish("Stopping server...")
        self.serverapp.stop()


class MarkrunnerApp(LabServerApp):
    serverapp_config = {
        "token": os.environ.get("MARKRUNNER_SERVER_TOKEN", ""),
        "port": int(os.environ.get("MARKRUNNER_SERVER_PORT", "8888")),
        "allow_origin": "app://obsidian.md",
        "open_browser": False,
    }

    def initialize_handlers(self):
        self.handlers.append(("/info", InfoHandler))
        self.handlers.append(("/stop", StopHandler))


def main():
    if os.environ.get("MARKRUNNER_SERVER_VERSION") != __version__:
        raise ValueError("Version mismatch")

    MarkrunnerApp.launch_instance()


if __name__ == "__main__":
    main()
