import unittest

from rich.console import Console

from queryquest.cli import is_quit_command, normalize_prompt_input, parse_args


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.console = Console(record=True)

    def test_is_quit_command_variants(self) -> None:
        self.assertTrue(is_quit_command("-q"))
        self.assertTrue(is_quit_command("qq --quit"))
        self.assertFalse(is_quit_command("show listings"))

    def test_normalize_prompt_input(self) -> None:
        self.assertEqual(normalize_prompt_input("-p hello"), ("hello", False))
        self.assertEqual(normalize_prompt_input("--prompt world"), ("world", False))
        self.assertEqual(normalize_prompt_input("-p"), ("", True))

    def test_parse_args_prompt(self) -> None:
        options = parse_args(["-p", "top 5 cities"], self.console)
        self.assertFalse(options.setup)
        self.assertEqual(options.prompt, "top 5 cities")

    def test_parse_args_setup(self) -> None:
        options = parse_args(["--setup"], self.console)
        self.assertTrue(options.setup)
        self.assertIsNone(options.prompt)

    def test_parse_args_help_exits(self) -> None:
        with self.assertRaises(SystemExit):
            parse_args(["-h"], self.console)


if __name__ == "__main__":
    unittest.main()
