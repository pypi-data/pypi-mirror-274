"""GLiCID spawner module."""

import asyncio
import re
import sys
from pathlib import Path

from batchspawner import JobStatus, SlurmSpawner
from traitlets import Bool, Integer, Unicode, default

from .form import options_form, options_from_form
from .micromamba import MAMBA_EXE, MAMBA_ROOT_PREFIX, MAMBA_USER_BASE
from .progress import ElapseTime, get_progress
from .templates import get_template_src

SPAWNER_BIN = Path(sys.exec_prefix) / 'bin'


class GlicidSpawner(SlurmSpawner):
    """Glicid SLURM Spawner."""

    batchspawner_singleuser_cmd = Unicode(
        'glicid-spawner-singleuser',
        help='Spawner singleuser command.',
    ).tag(config=True)

    req_mamba_exe = Unicode(
        MAMBA_EXE,
        help='Micromamba global exe',
    ).tag(config=True)

    req_mamba_root_prefix = Unicode(
        MAMBA_ROOT_PREFIX,
        help='Micromamba global root prefix',
    ).tag(config=True)

    req_mamba_user_base = Unicode(
        MAMBA_USER_BASE,
        help='Micromamba user base prefix',
    ).tag(config=True)

    req_job_name = Unicode(
        'jupyterhub_glicid',
        help='SLURM job name',
    ).tag(config=True)

    req_qos = Unicode(
        'short',
        help='QoS name to submit job to resource manager',
    ).tag(config=True)

    batch_script = Unicode(
        get_template_src('slurm_script.jinja'),
        help='Template for SLURM job submission batch script.',
    ).tag(config=True)

    disable_user_config = Bool(
        True,
        help='Disable per-user configuration of single-user servers.',
    ).tag(config=True)

    notebook_dir = Unicode(
        '/',
        help='Path to the notebook directory for the single-user server.',
    ).tag(config=True)

    @default('default_url')
    def _default_url_default(self) -> str:
        """The URL the single-user server should start in."""
        return '/lab/tree' + self.user_options.get('workdir', '/home/{username}') + '?reset'

    def cmd_formatted_for_batch(self):
        """The command which is substituted inside of the batch script.

        Here we need the absolute path to the spawner and singleuser commands.

        """
        return ' '.join(
            [
                str(SPAWNER_BIN / self.batchspawner_singleuser_cmd),
                str(SPAWNER_BIN / self.cmd[0]),
                *self.get_args(),
            ]
        )

    slurm_job_id_re = Unicode(r'(\d+)(?:;(\w+))?').tag(config=True)

    def parse_job_id(self, output) -> str:
        """Parse job id with cluster name support.

        If cluster name is present, `job_id` will be a string
        and suffix with `-M job_cluster` name.

        """
        for job_id, job_cluster in re.findall(self.slurm_job_id_re, output):
            return f'{job_id} -M {job_cluster}' if job_cluster else job_id

        self.log.error(f'GlicidSpawner unable to parse job ID from text: {output}')
        return ''

    @default('options_form')
    def _options_form_default(self) -> str:
        """JupyterHub rendered form template."""
        return options_form(self.user.name)

    def options_from_form(self, formdata) -> dict:
        """Export options from form."""
        return options_from_form(formdata)

    progress_rate = Integer(
        5, help='Interval in seconds at which progress is polled for messages'
    ).tag(config=True)

    async def progress(self):
        """Progress bar feedback."""
        elapse_time = 0

        while True:
            if self.state_isrunning():
                job_status = JobStatus.RUNNING
                elapse_time += self.progress_rate
            elif self.state_ispending():
                job_status = JobStatus.PENDING
            else:
                job_status = JobStatus.NOTFOUND

            yield get_progress(job_status, elapse_time)

            if elapse_time >= ElapseTime.CONNECT:
                break

            await asyncio.sleep(self.progress_rate)
