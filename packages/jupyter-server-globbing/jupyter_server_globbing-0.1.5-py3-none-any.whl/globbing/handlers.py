import json
from pathlib import Path

from jupyter_server.base.handlers import APIHandler
import tornado


class GlobbingExtensionHandler(APIHandler):

    @tornado.web.authenticated
    def get(self, pattern):
        """
        /api/globbing/{pattern}
        return a list of files or directories that match the provided pattern
        trying to be kind-of compliant with the results of
        /api/contents/{path} from jupyter-server
        https://jupyter-server.readthedocs.io/en/latest/developers/rest-api.html
        """
        matches = Path('.').glob(pattern)
        result = []
        for match in matches:
            if match.is_dir():
                result.append(dict(path=str(match), type='directory'))
            else:
                result.append(dict(path=str(match), type='file'))
        self.finish(json.dumps(result))
