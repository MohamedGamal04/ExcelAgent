"""Lightweight append-only JSON logging for CLI/session events."""

import json
from collections.abc import Mapping
from datetime import datetime, timezone

from .config import LOG_FILE


def append_log(entry: Mapping[str, object]) -> None:
	"""Append a timestamped JSON log entry.

	Logging failures are intentionally swallowed to avoid interrupting user flow.
	"""
	payload = {
		"timestamp": datetime.now(timezone.utc).isoformat(),
		**entry,
	}
	try:
		with LOG_FILE.open("a", encoding="utf-8") as f:
			f.write(json.dumps(payload, ensure_ascii=True, indent=2) + "\n")
	except OSError:
		# Logging should never interrupt chat flow.
		pass
