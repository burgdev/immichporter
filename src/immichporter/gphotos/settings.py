from platformdirs import user_config_dir
from pathlib import Path

config_dir = Path(user_config_dir("immichporter", "burgdev"))

playwright_session_dir = config_dir / "playwright_session"
