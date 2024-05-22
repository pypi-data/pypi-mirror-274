JupyterHub Batch Spawner for GLiCID
===================================

[![Gitlab CI](https://gitlab.univ-nantes.fr/glicid/jupyter/spawner/badges/main/pipeline.svg)](https://gitlab.univ-nantes.fr/glicid/jupyter/spawner/pipelines/main/latest)
[![Test coverage](https://gitlab.univ-nantes.fr/glicid/jupyter/spawner/badges/main/coverage.svg)](https://gitlab.univ-nantes.fr/glicid/jupyter/spawner/pipelines/main/latest)

![Spawner form](img/spawner_form.png)


JupyterHub config
-----------------

In `jupyterhub_config.py`, add:
```txt
c.JupyterHub.spawner_class = 'glicid-spawner'
```

At the moment, you also need to change the `c.GlicidSpawner.batch_script`.
This will be be included in the future.


Contribution
------------
This package is managed by [Poetry](https://python-poetry.org/):
```bash
git clone https://gitlab.univ-nantes.fr/glicid/jupyter/spawner glicid-spawner
cd glicid-spawner
poetry install
poetry run pre-commit install
```

To test the spawner:
```bash
poetry run pytest
```

To lint and format the source code:
```bash
poetry run ruff check . --fix
poetry run ruff format
```

To render the form template (with live reload):
```bash
poetry run python -m render [--single-cluster]
```

To activate the virtual environement globally:
```bash
source .venv/bin/activate
```

Bump to a new version:
```bash
poetry run tbump Major.Patch
```

External resources
------------------
- https://jupyterhub.readthedocs.io/en/stable/reference/spawners.html
- https://github.com/jupyterhub/batchspawner
- https://gitlab.com/idris-cnrs/jupyter/jupyter-jeanzay-spawner/
- https://gitlab.com/ifb-elixirfr/cluster/utils/slurmspawner/
- https://getbootstrap.com/docs/3.4/
