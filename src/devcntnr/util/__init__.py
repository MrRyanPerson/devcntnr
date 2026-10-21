from argon2 import PasswordHasher
from docker import DockerClient
from loguru import logger
import docker
import os

hasher = PasswordHasher()

class DockerRunner:
    def __init__(self, client: DockerClient) -> None:
        self.client = client
        self.container = None;
        logger.info("Docker Runner initialized")

    def startDevContainer(self, config) -> None:
        if (config["GIT_SSH_TOKEN"] != ""):
            with open(rf"{os.getcwd()}/config/.ssh", "w", encoding="utf-8") as file:
                file.write(config["GIT_SSH_TOKEN"])
            logger.info("Wrote Github SSH token to .ssh")

        self.container = self.client.containers.run(
            image="lscr.io/linuxserver/code-server:latest",
            name="code-server",
            detach=True,
            environment={
                "PUID": "1000",
                "PGID": "1000",
                "TZ": config["TZ"],
                "HASHED_PASSWORD": hasher.hash(password=config["PASSWORD"]),
                "SUDO_PASSWORD_HASH": hasher.hash(password=config["SUDO_PASSWORD"]),
            },
            ports={
                "8443/tcp": 8443,
            },
            volumes={
                rf"{os.getcwd()}/config": {
                    "bind": "/config",
                    "mode": "rw",
                },
            },
            restart_policy={
                "Name": "unless-stopped",
            },
        )

        logger.info(f"Started Container: {self.container.name}")

    def stopDevContainer(self):
        if (self.container != None):
            self.container.stop()

    def runComposeFile(file) -> None:
        pass

