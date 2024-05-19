from typing import Optional

from flask_projects.default.middle.NameFactory import name_extend
from flask_projects.interface.container import ContainerAbs
from flask_projects.interface.scanner import ScannerAbs


class Plan0MiddleContainer(ContainerAbs):
    name = name_extend

    def __init__(self, pro):
        self.middles: Optional[tuple] = tuple()

        super().__init__(pro)

    def insert(self, path_dir: str, scanner: ScannerAbs):
        self.middles = scanner.scan(path_dir)

    def query(self):

        return self.middles
