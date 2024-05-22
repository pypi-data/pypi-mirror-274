import asyncio


async def run_shell_cmd(cmd: str) -> (int, str, str):
    """Execute shell command

    Returns:
      Tuple (returned code, stdout, stderr)
    """
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout.decode().strip(), stderr.decode().strip()
