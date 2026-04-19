import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from queryquest import state


class StateTests(unittest.TestCase):
    def test_load_state_missing_file_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_state = Path(tmpdir) / ".provider.json"
            with patch.object(state, "STATE_FILE", fake_state):
                self.assertIsNone(state.load_state())

    def test_save_and_load_state_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_state = Path(tmpdir) / ".provider.json"
            with patch.object(state, "STATE_FILE", fake_state):
                state.save_state("groq", "key123", "llama-3.3-70b-versatile", excel_dir="/tmp/excel")
                loaded = state.load_state()

        self.assertIsNotNone(loaded)
        assert loaded is not None
        self.assertEqual(loaded["provider"], "groq")
        self.assertEqual(loaded["api_key"], "key123")
        self.assertEqual(loaded["model"], "llama-3.3-70b-versatile")
        self.assertEqual(loaded["excel_dir"], "/tmp/excel")

    def test_load_state_invalid_provider_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_state = Path(tmpdir) / ".provider.json"
            fake_state.write_text(
                json.dumps({"provider": "invalid", "api_key": "key", "model": "m"}),
                encoding="utf-8",
            )
            with patch.object(state, "STATE_FILE", fake_state):
                self.assertIsNone(state.load_state())


if __name__ == "__main__":
    unittest.main()
