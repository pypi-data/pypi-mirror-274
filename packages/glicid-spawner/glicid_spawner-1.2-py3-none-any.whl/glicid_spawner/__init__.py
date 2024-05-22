"""GLiCID spawner module."""

from importlib.metadata import version

from .spawner import GlicidSpawner

__all__ = ['GlicidSpawner']

__version__ = version('glicid-spawner')
