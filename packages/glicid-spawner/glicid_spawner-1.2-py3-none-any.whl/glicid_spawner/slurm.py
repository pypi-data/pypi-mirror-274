"""SLURM module."""

import re
import shlex
import subprocess
from dataclasses import dataclass, field
from itertools import groupby
from operator import attrgetter
from pathlib import Path

STATES_AVAILABLE = (
    'idle',
    'mixed',
    'completing',
)


@dataclass
class SlurmCpu:
    """SLURM CPU."""

    allocated: int
    idle: int
    total: int

    def __post_init__(self):
        self.allocated = int(self.allocated)
        self.idle = int(self.idle)
        self.total = int(self.total)


@dataclass
class SlurmGpu:
    """SLURM GPU."""

    name: str = field(default='None')
    nb: int = field(default=0)

    def __post_init__(self):
        self.name = str(self.name).capitalize()
        self.nb = int(self.nb)

    def __bool__(self):
        return self.nb > 0

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return str(self) == str(other)


@dataclass
class SlurmNode:
    """SLURM node."""

    cluster: str
    partition: str
    hostname: str
    state: str
    cpu: SlurmCpu
    mem: int
    gpu: SlurmGpu

    def __init__(self, cluster, partition, hostname, state, cpus_state, memory_mb, gres):  # noqa: PLR0913
        self.cluster = cluster.strip()
        self.partition = partition.strip()
        self.hostname = hostname.strip()
        self.state = state.strip().lower()
        self.cpu = SlurmCpu(*re.findall(r'(\d+)/(\d+)/\d+/(\d+)', cpus_state)[0])
        self.mem = int(memory_mb) // 1000  # in GB
        self.gpu = SlurmGpu(*re.findall(r'gpu:([\w\.]+):(\d+)', gres)[0] if 'gpu:' in gres else [])

    def __str__(self):
        return self.hostname

    def __eq__(self, other):
        return str(self) == str(other)


@dataclass
class SlurmPartition:
    """SLURM partition."""

    name: str
    nodes: list

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return str(self) == str(other)

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, other):
        return self.nodes[self.nodes.index(other)]

    @property
    def gpus(self) -> str:
        """List of GPUs available."""
        return ':'.join({node.gpu.name for node in self.nodes})

    @property
    def max_idle_cpu(self) -> int:
        """Maximum of idle CPU available."""
        return max(node.cpu.idle for node in self.nodes)

    @property
    def max_mem(self) -> int:
        """Maximum of memory available."""
        return max(node.mem for node in self.nodes)


@dataclass
class SlurmCluster:
    """SLURM cluster."""

    name: str
    partitions: list

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return str(self) == str(other)

    def __iter__(self):
        return iter(self.partitions)

    def __len__(self):
        return len(self.partitions)

    def __getitem__(self, other):
        return self.partitions[self.partitions.index(other)]


def sinfo_run(username: str = None) -> str:
    """SLURM SINFO run command."""
    flags = '--federation --noheader --responding --cluster=all'
    fmt = 'Cluster,PartitionName,NodeHost,StateLong,CPUsState,Memory,Gres'
    cmd = f'sinfo {flags} --Format={fmt}'

    if username:
        cmd = f"su - {username} -c '{cmd}'"

    return subprocess.check_output(shlex.split(cmd)).decode('utf-8')


def sinfo_reader(result: str) -> list:
    """SLURM SINFO reader."""
    return [SlurmNode(*re.findall('.{20}', node)) for node in result.splitlines()]


def sinfo_filter(resources: list, with_states=STATES_AVAILABLE) -> dict:
    """SLURM SINFO filtered resources available with a given state(s).

    Grouped by cluster and partition names.

    """
    clusters = [
        SlurmCluster(
            cluster,
            [
                SlurmPartition(partition, nodes_with_states)
                for partition, nodes in groupby(partitions, key=attrgetter('partition'))
                if (nodes_with_states := [node for node in nodes if node.state in with_states])
            ],
        )
        for cluster, partitions in groupby(resources, key=attrgetter('cluster'))
    ]

    # Remove empty cluster
    return {cluster.name: cluster for cluster in clusters if cluster}


def sinfo_from_file(fname, with_states=STATES_AVAILABLE) -> dict:
    """SLURM SINFO resources available from a given file."""
    content = Path(fname).read_text()
    return sinfo_filter(sinfo_reader(content), with_states=with_states)


def sinfo(username: str = None, with_states=STATES_AVAILABLE) -> dict:
    """SLURM SINFO resources available for a given user."""
    return sinfo_filter(sinfo_reader(sinfo_run(username=username)), with_states=with_states)


def gres(resources: dict) -> list:
    """List SLURM GPU resources."""
    return sorted(
        {
            node.gpu.name
            for cluster in resources.values()
            for partition in cluster
            for node in partition
        }
    )
