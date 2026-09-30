import os
from pathlib import Path

BASE_URL = os.getenv("ZEPTO_BASE_URL", "https://www.zepto.com/")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"
VIDEOS_DIR = PROJECT_ROOT / "videos"
TRACES_DIR = PROJECT_ROOT / "traces"
DEFAULT_TIMEOUT_MS = int(os.getenv("ZEPTO_TIMEOUT_MS", "15000"))
