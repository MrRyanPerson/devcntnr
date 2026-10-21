from .util import DockerRunner
from dotenv import dotenv_values
from loguru import logger
import docker

config = dict(dotenv_values())
client = docker.from_env()
runner = DockerRunner(client=client)

def main() -> None:
    runner.startDevContainer(config)