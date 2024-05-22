"""Micromamba environments module."""

from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path

MICROMAMBA_ROOT = Path('/micromamba')  # default micromamba root location
GLOBAL_USER = 'operator'

MAMBA_ROOT_PREFIX = f'{MICROMAMBA_ROOT}/{GLOBAL_USER}'
MAMBA_EXE = f'{MAMBA_ROOT_PREFIX}/bin/micromamba'
MAMBA_USER_BASE = f'{MICROMAMBA_ROOT}/$USER'


@dataclass
class MicromambaEnv:
    """Generic micromamba environment."""

    scope: str
    name: str
    path: str


def _envs(folder) -> list:
    """List micromamba environments with jupyter kernel(s)."""
    # Get micromamba environments as pathlib.Path folders
    envs = MICROMAMBA_ROOT / folder / 'envs'

    if not envs.exists():
        return []

    return sorted(
        [
            (env.name, str(env))
            for env in envs.iterdir()
            if env.is_dir() and any(env.glob('share/jupyter/kernels/*/kernel.json'))
        ],
        key=itemgetter(0),
    )


def _envs_user(username: str) -> list:
    """Micromamba environment(s) available to the user."""
    return [MicromambaEnv('USER', name, path) for name, path in _envs(username)]


def _envs_team(username: str) -> list:
    """Micromamba environment(s) available to the user's team.

    Warning
    -------
    At the moment micromamba team environments is not available on GLiCID.

    """
    teams = []  # FIXME: pull user teams list from groups
    return [
        MicromambaEnv('TEAM', name, path) for team in teams for name, path in _envs(f'teams/{team}')
    ]


def _envs_global() -> list:
    """Micromamba environment(s) available globally."""
    return [MicromambaEnv('GLOBAL', name, path) for name, path in _envs(GLOBAL_USER)]


def get_envs(username: str) -> list:
    """List of all the micromamba environment available to a user."""
    return _envs_user(username) + _envs_team(username) + _envs_global()
