import unittest
from mock import patch
from unittest.mock import MagicMock
from barely.plugins.backup.git.git import Git


class TestGit(unittest.TestCase):

    def test___init__(self):
        git = Git()

        golden = {
            "PRIORITY": 40,
            "MESSAGE": "barely auto commit",
            "REMOTE_NAME": "origin"
        }

        self.assertDictEqual(golden, git.plugin_config)

    def test_register(self):
        git = Git()
        name, prio = git.register()

        self.assertEqual(name, "git")
        self.assertEqual(prio, 40)

    @patch("barely.plugins.backup.git.git.Repo")
    def test_action(self, r):
        repo = MagicMock()

        repo.git.add = MagicMock()
        repo.index.commit = MagicMock()

        repo.remote = MagicMock()

        r.return_value = repo

        git = Git()
        git.plugin_config = {
            "PRIORITY": 2,
            "MESSAGE": "barely auto commit",
            "REMOTE_NAME": "origin"
        }
        git.action()

        repo.git.add.assert_called()
        repo.index.commit.assert_called()

        repo.remote.assert_called()

        def error():
            raise Exception

        repo.git.add = MagicMock(side_effect=error)

        with self.assertRaises(Exception) as context:
            git.action()
            self.assertTrue('barely :: an error occurred while pushing to origin' in str(context.exception))
