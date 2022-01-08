from pathlib import Path

import daemon
from plumbum import cmd, local


class DockerDaemon(daemon.Daemon):
    def __init__(self):
        super().__init__(
            "/home/kapi/CLionProjects/noisepage-pilot/build/explorer/noisepage/"
        )
        self.docker = local["docker"]
        self.docker_compose = local["docker-compose"]

    def _docker_build(self):
        # Build the Docker image.
        build_command = cmd.sudo[
            self.docker[
                "build",
                "--tag",
                "pgnp",
                "--file",
                f"{Path(self.noisepage_path) / 'cmudb/env/Dockerfile'}",
            ]
        ]
        print(build_command)

    def _docker_up(self):
        # build_command = cmd.sudo[
        #     self.docker_compose[
        #         "--project-name",
        #         "",
        #         "--file",
        #         f"{Path(self.noisepage_path) / 'cmudb/env/'}",
        #         "down",
        #         "--volumes",  # Remove all the associated volumes.
        #     ]
        # ]
        pass

    def container_up(self):
        super().container_up()
        print("Docker up.")

        # Create a Docker volume.
        # print(build_command)
        # print(cmd.sudo(self.docker['--help']))
        pass

    def container_down(self):
        super().container_down()
        print("Docker down.")
        pass


if __name__ == "__main__":
    d = DockerDaemon()
    # d.noisepage_clone()
    d.container_up()
    d.container_down()
