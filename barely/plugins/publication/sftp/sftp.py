"""
transfer only the changed files
(save bandwidth) to an sftp server
"""
import os
import pysftp
from barely.plugins import PluginBase


class SFTP(PluginBase):
    """ copy to remote server; only new/changed though """

    def __init__(self):
        super().__init__()
        try:
            standard_config = {
                "PRIORITY": 90,
                "HOSTNAME": "",
                "USER": "",
                "PASSWORD": "",
                "KEY": "",
                "ROOT": ""
            }
            self.plugin_config = standard_config | self.config["SFTP"]
        except KeyError:
            self.plugin_config = {"PRIORITY": -1}

    def register(self):
        return "sftp", self.plugin_config["PRIORITY"]

    def action(self, *args, **kwargs):
        try:
            if self.plugin_config["KEY"] != "":
                conn = pysftp.Connection(self.plugin_config["HOSTNAME"],
                                         username=self.plugin_config["USER"],
                                         private_key=self.plugin_config["KEY"],
                                         private_key_pass=True)
            else:
                conn = pysftp.Connection(self.plugin_config["HOSTNAME"],
                                         username=self.plugin_config["USER"],
                                         password=self.plugin_config["PASSWORD"])

            conn.put_r(os.path.join(self.config["ROOT"]["WEB"], ""), self.plugin_config["ROOT"], preserve_mtime=True)
            conn.close()
            self.logger.info(f"published via SFTP to {self.plugin_config['HOSTNAME']}")
        except KeyError:
            self.logger.error("SFTP configuration is incomplete or invalid.")
