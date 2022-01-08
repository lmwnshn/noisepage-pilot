from abc import ABC, abstractmethod

from plumbum import local


class Daemon(ABC):
    def __init__(self, noisepage_path):
        self.noisepage_path = noisepage_path
        self.git = local["git"]

    def noisepage_clone(self):
        self.git("clone", "https://github.com/cmu-db/postgres.git", self.noisepage_path)

    @abstractmethod
    def container_up(self):
        print("Daemon up.")
        pass

    @abstractmethod
    def container_down(self):
        print("Daemon down.")
        pass
