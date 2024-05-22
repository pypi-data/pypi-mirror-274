"""GLiCID template form module."""

from .micromamba import get_envs
from .resources import CPU, GPU_DEFAULTS, MEMORY, get_folders, gpu_max_duration
from .slurm import gres, sinfo
from .templates import render_template

GRES_CLUSTERS_LOWERCASE = [
    'waves',
]


def options_attrs(username: str) -> dict:
    """Form options attributes."""
    slurm_sinfo = sinfo(username)

    # Allocated 1h to any SLURM GPU resources not listed in GPUS
    gpus = gpu_max_duration(gres(slurm_sinfo), unknown_default=1)

    return {
        'username': username,
        'folders': get_folders(username),
        'envs': get_envs(username),
        'cpus': CPU,
        'mems': MEMORY,
        'gpus': gpus,
        'sinfo': slurm_sinfo,
    }


def options_form(username: str) -> str:
    """Render default spawner form."""
    return render_template('spawner_form.jinja', **options_attrs(username))


def options_from_form(formdata) -> dict:
    """Export options from default form."""
    # Parse form data response
    workdir = formdata['workdir'][0]
    env = formdata['python-env'][0]
    cpu = int(formdata['cpu'][0])
    mem = int(formdata['mem'][0])
    gpu = formdata['gpu'][0]
    cluster = formdata.get('cluster', [None])[0]
    partition = formdata.get('partition', [None])[0]
    node = formdata.get('node', [None])[0]

    # Compute max duration
    # If the value provided is not in the original list, runtime = 0 (except unknown GPU = 1h)
    runtime = min(CPU.get(cpu, 0), MEMORY.get(mem, 0), GPU_DEFAULTS.get(gpu, 1))

    # Export options
    options = {
        'workdir': workdir,
        'pyenv': env,
        'nprocs': cpu,
        'memory': f'{mem}GB',
        'runtime': f'{runtime:02d}:00:00',
    }

    if gpu != 'None':
        if cluster in GRES_CLUSTERS_LOWERCASE:
            gpu = gpu.lower()

        options['gres'] = f'gpu:{gpu}'

    if cluster:
        options['cluster'] = cluster

    if partition:
        options['partition'] = partition

    if node:
        options['node'] = node

    return options
