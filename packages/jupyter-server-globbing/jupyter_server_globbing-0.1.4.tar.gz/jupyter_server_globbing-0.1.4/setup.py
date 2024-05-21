#!/usr/bin/env python

from setuptools import setup

from globbing import __version__

setup(
    name="jupyter-server-globbing",
    version=__version__,
    description = "a minimal extension for jupyter-server that supports file globbing",
    include_package_data=True,
    data_files=[
        (
            "etc/jupyter/jupyter_server_config.d",
            ["jupyter-config/jupyter_server_config.d/globbing.json"],
        ),
    ],
)
