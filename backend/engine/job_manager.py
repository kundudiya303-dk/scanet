"""
scanet — Process Job Manager
Async subprocess execution with process-group isolation and SSE streaming.
Zero orphaned processes. Zero blocking calls.
"""
import asyncio
import os
import signal
import typing
import logging

logger = logging.getLogger("scanet.job_manager")


class ProcessJobManager:
    """
    Manages the full lifecycle of external tool processes:
    - Spawn with isolated process group (os.setsid)
    - Stream stdout/stderr line-by-line to output callback
    - Cancel entire process group on request
    - Enforce execution timeouts
    """

    def __init__(self):
        self.active_processes: dict[str, asyncio.subprocess.Process] = {}

    async def execute_job(
        self,
        job_id: str,
        cmd_args: list[str],
        output_callback: typing.Callable[[str], typing.Awaitable[None]],
        timeout_seconds: int = 600,
    ) -> tuple[int, str]:
        """
        Executes a command in an isolated process group.
        Streams each output line through output_callback.
        Returns (exit_code, full_output_string).
        """
        logger.info("Starting job %s: %s", job_id, " ".join(cmd_args))

        proc = await asyncio.create_subprocess_exec(
            *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            preexec_fn=os.setsid,  # New session = independent process group
        )
        self.active_processes[job_id] = proc
        output_lines: list[str] = []

        try:
            async with asyncio.timeout(timeout_seconds):
                while True:
                    line = await proc.stdout.readline()
                    if not line:
                        break
                    decoded = line.decode("utf-8", errors="replace")
                    output_lines.append(decoded)
                    await output_callback(decoded)
                await proc.wait()

        except asyncio.TimeoutError:
            logger.warning("Job %s timed out after %ds", job_id, timeout_seconds)
            await self.cancel_job(job_id)
            return (-1, "".join(output_lines) + "\n[TIMEOUT] Job exceeded maximum execution time.\n")

        except Exception as exc:
            logger.exception("Unexpected error in job %s: %s", job_id, exc)
            await self.cancel_job(job_id)
            return (-2, "".join(output_lines) + f"\n[ERROR] {exc}\n")

        finally:
            self.active_processes.pop(job_id, None)

        exit_code = proc.returncode or 0
        logger.info("Job %s finished with exit code %d", job_id, exit_code)
        return (exit_code, "".join(output_lines))

    async def cancel_job(self, job_id: str) -> bool:
        """
        Terminates the entire process group of a running job.
        Sends SIGTERM, then SIGKILL after 1 second if still alive.
        """
        proc = self.active_processes.get(job_id)
        if not proc or proc.returncode is not None:
            return False

        try:
            pgid = os.getpgid(proc.pid)
            logger.info("Sending SIGTERM to process group %d for job %s", pgid, job_id)
            os.killpg(pgid, signal.SIGTERM)
            await asyncio.sleep(1.0)
            if proc.returncode is None:
                logger.warning("Escalating to SIGKILL for job %s", job_id)
                os.killpg(pgid, signal.SIGKILL)
            return True
        except ProcessLookupError:
            return True
        except Exception as exc:
            logger.error("Error cancelling job %s: %s", job_id, exc)
            return False

    def list_active_jobs(self) -> list[str]:
        """Returns job IDs of currently running processes."""
        return list(self.active_processes.keys())


# Singleton instance shared across the application
job_manager = ProcessJobManager()
