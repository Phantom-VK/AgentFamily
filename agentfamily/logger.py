from __future__ import annotations

from datetime import datetime
from pathlib import Path
import traceback


class AgentFamilyLogger:
    def __init__(self, log_dir: Path | None = None, echo: bool = True):
        base_dir = Path(__file__).resolve().parents[1]
        self.log_dir = log_dir or (base_dir / "logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = self.log_dir / f"agentfamily_{timestamp}.log"
        self.echo = echo
        self.info(f"Logger initialized. Writing logs to {self.log_file}")

    def _write(self, level: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{level}] {message}"
        with self.log_file.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        if self.echo:
            print(line)

    def info(self, message: str) -> None:
        self._write("INFO", message)

    def warning(self, message: str) -> None:
        self._write("WARNING", message)

    def error(self, message: str) -> None:
        self._write("ERROR", message)

    def exception(self, message: str) -> None:
        details = traceback.format_exc()
        self._write("ERROR", f"{message}\n{details}")


app_logger = AgentFamilyLogger()
