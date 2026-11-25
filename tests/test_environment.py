from pathlib import Path

from dotenv import dotenv_values

test_env = dotenv_values(Path(__file__).parent / "test.env")
