"""Start the target process and keep it for later approvals."""

import subprocess
import sys
import time
import urllib.request

from pager.config import settings
from pager.target.client import HttpTarget

HOST = "127.0.0.1"
PORT = 8010


def target_url() -> str:
    return settings.target_url or f"http://{HOST}:{PORT}"


def _up(url: str) -> bool:
    try:
        with urllib.request.urlopen(f"{url}/health", timeout=0.5) as response:
            return response.status == 200
    except Exception:
        return False


def ensure_running() -> str:
    url = target_url()
    if _up(url):
        return url
    subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "pager.target.app:app", "--host", HOST, "--port", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(50):
        if _up(url):
            return url
        time.sleep(0.1)
    raise RuntimeError("The target did not start.")


def inject(scenario_id: str, url: str | None = None) -> None:
    HttpTarget(url or ensure_running()).inject(scenario_id)


def revert(url: str | None = None) -> None:
    HttpTarget(url or ensure_running()).revert()
