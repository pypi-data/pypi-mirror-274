"""Default resources module."""

CPU = {
    # description: max-duration [h]
    1: 24,
    2: 12,
    4: 6,
    8: 3,
    12: 2,
    24: 1,
}

MEMORY = {  # [GB]
    4: 24,
    8: 12,
    16: 6,
    32: 3,
    48: 2,
    96: 1,
}

GPU_DEFAULTS = {
    'None': 24,
    'A40': 2,
    'A100': 1,
}


def gpu_max_duration(gpus: list, unknown_default=1) -> dict:
    """GPU max-duration allocation.

    By default 1h is allocated to any unknown GPU resource
    not listed in the GPU_DEFAULTS.

    """
    # Filter defaults value in the same order as GPUS_DEFAULTS
    defaults = {gpu: duration for gpu, duration in GPU_DEFAULTS.items() if gpu in gpus}
    unknowns = {gpu: unknown_default for gpu in gpus if gpu not in GPU_DEFAULTS}
    return defaults | unknowns


def get_folders(username: str) -> list:
    """List of folders accessible to the users as a working directory."""
    return [
        f'/home/{username}',
        f'/scratch/nautilus/users/{username}',
        f'/scratch/waves/users/{username}',
        '/scratch/nautilus/projects',
        '/scratch/waves/projects',
        '/LAB-DATA/',
    ]
