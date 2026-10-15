import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class PackageVersionTests(unittest.TestCase):
    def test_python_and_both_npm_manifests_match(self):
        python_version = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"]
        root_npm_version = json.loads((ROOT / "package.json").read_text())["version"]
        frontend_npm_version = json.loads((ROOT / "frontend" / "package.json").read_text())["version"]
        self.assertEqual(python_version, root_npm_version)
        self.assertEqual(frontend_npm_version, root_npm_version)


if __name__ == "__main__":
    unittest.main()
