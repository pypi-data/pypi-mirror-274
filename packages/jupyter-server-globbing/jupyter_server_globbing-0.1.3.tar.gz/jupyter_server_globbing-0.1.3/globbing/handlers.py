import json
from pathlib import Path

from jupyter_server.base.handlers import APIHandler
import tornado


class GlobbingExtensionHandler(APIHandler):

    @tornado.web.authenticated
    def get(self, slug):
        matches = Path('.').glob(slug)
        result = []
        for match in matches:
            if match.is_dir():
                result.append(dict(path=str(match), type='directory'))
            else:
                result.append(dict(path=str(match), type='file'))
        self.finish(json.dumps(result))
