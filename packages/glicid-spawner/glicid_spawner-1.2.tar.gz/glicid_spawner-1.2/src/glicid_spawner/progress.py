"""Progress messages module."""

from batchspawner import JobStatus


def jhp(progress, message):
    """Jupyterhub progress message dictionary."""
    return {'progress': progress, 'message': message}


class Process:
    """Progress value."""

    ERROR = jhp(0, '💀 Oops something when wrong')
    SUBMIT = jhp(10, '📝 Job submitted')
    PENDING = jhp(20, '⏱️ Your job is pending in queue')
    INIT = jhp(40, '📦 The resources were allocated')
    SETUP = jhp(60, '🏗️ Setting up your environment (it should take a minute or two)')
    CONNECT = jhp(80, '📡 Be ready you should be connected at any moment')
    TOO_LONG = jhp(95, '🧐 Your instance takes longer than usual but it should be ready soon')


class ElapseTime:
    """Elapse time steps when the job is running."""

    SUBMIT = 0
    PENDING = 0
    INIT = 10
    SETUP = 30
    CONNECT = 60


def get_progress(job_status: JobStatus, elapse_time: int) -> dict:  # noqa: PLR0911 (too-many-return-statements)
    """Progress and message based on job status and elapse time."""
    match job_status:
        case JobStatus.NOTFOUND:
            return Process.SUBMIT

        case JobStatus.PENDING:
            return Process.PENDING

        case JobStatus.RUNNING:
            if elapse_time < ElapseTime.INIT:
                return Process.INIT

            if elapse_time < ElapseTime.SETUP:
                return Process.SETUP

            if elapse_time < ElapseTime.CONNECT:
                return Process.CONNECT

            return Process.TOO_LONG

    return Process.ERROR
