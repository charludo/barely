"""
push to git remote rep automatically
"""
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

from git import Repo
from datetime import datetime
from barely.plugins import PluginBase


class Git(PluginBase):
    # add changes / commit them / push them to origin

    def __init__(self):
        super().__init__()
        try:
            standard_config = {
                "PRIORITY": 40,
                "MESSAGE": "barely auto commit",
                "REMOTE_NAME": "origin"
            }
            self.plugin_config = standard_config | self.config["GIT"]
        except KeyError:
            self.plugin_config = {"PRIORITY": -1}

    def register(self):
        return "git", self.plugin_config["PRIORITY"]

    def action(self, *args, **kwargs):
        try:
            repo = Repo(os.path.join(self.config["ROOT"]["DEV"], ".git"))
            repo.git.add(all=True)
            repo.index.commit(datetime.now().strftime("%Y-%m-%d--%H-%M-%S") + " " + self.plugin_config["MESSAGE"])
            origin = repo.remote(name=self.plugin_config["REMOTE_NAME"])
            origin.push()
            self.logger.info(f"successfully pushed to {self.plugin_config['REMOTE_NAME']}")
        except Exception:
            self.logger.error(f"an error occurred while pushing to {self.plugin_config['REMOTE_NAME']}")
