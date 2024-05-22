"""Patched JupyterHub singleuser command script.

Fix based on batchspawner#250:
    https://github.com/jupyterhub/batchspawner/pull/250

The Hub API should use an async call.

"""

import asyncio
import json
import sys
from runpy import run_path
from shutil import which

from jupyterhub.services.auth import HubAuth
from jupyterhub.utils import random_port, url_path_join


def main(argv=None):
    port = random_port()
    hub_auth = HubAuth()

    asyncio.run(
        hub_auth._api_request(
            method='POST',
            url=url_path_join(hub_auth.api_url, 'batchspawner'),
            body=json.dumps({'port': port}),
        )
    )

    cmd_path = which(sys.argv[1])
    sys.argv = sys.argv[1:] + [f'--port={port}']
    run_path(cmd_path, run_name='__main__')


if __name__ == '__main__':  # pragma: no cover
    main()
