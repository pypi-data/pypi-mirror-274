import importlib
import os
import traceback

from flask_projects.default.router.NameFactory import name_extend
from flask_projects.default.router.convention import RouterBasic
from flask_projects.interface.scanner import ScannerAbs


class Plan0RouterScanner(ScannerAbs):
    name = name_extend

    def scan(self, path_dir: str):
        cls_route = []

        for r, d, filenames in os.walk(path_dir):
            if 'business' not in r or 'router' not in r:
                continue

            for filename in filenames:
                if filename == '__init__.py' or not filename.endswith('.py'):
                    continue

                try:
                    module = importlib.machinery.SourceFileLoader(
                        filename.replace(',py', ''), os.path.join(r, filename)
                    ).load_module()

                    class_imported = getattr(module, filename.replace('.py', ''))
                    if issubclass(class_imported, RouterBasic):
                        cls_route.append(class_imported)

                except Exception:
                    print(traceback.format_exc())

        return cls_route
