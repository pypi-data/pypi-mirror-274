import importlib
import os
import traceback

from flask_projects.default.middle.NameFactory import name_extend
from flask_projects.default.middle.convention import OutContextBeforeMiddle, OutContextBackMiddle, \
    InContextBeforeMiddle, InContextBackMiddle
from flask_projects.interface.scanner import ScannerAbs


class Plan0MiddleScanner(ScannerAbs):
    name = name_extend

    def scan(self, path_dir: str):

        middles_before_out_context = []
        middles_before_in_context = []
        middles_back_in_context = []
        middles_back_out_context = []
        for r, d, filenames in os.walk(path_dir):
            if 'business' not in r or 'middle' not in r:
                continue
            for filename in filenames:
                if filename == '__init__.py' or not filename.endswith('.py'):
                    continue

                try:
                    module = importlib.machinery.SourceFileLoader(
                        filename.replace(',py', ''), os.path.join(r, filename)
                    ).load_module()
                    class_imported = getattr(module, filename.replace('.py', ''))
                    if issubclass(class_imported, OutContextBeforeMiddle):
                        middles_before_out_context.append(class_imported())
                    elif issubclass(class_imported, OutContextBackMiddle):
                        middles_back_out_context.append(class_imported())
                    elif issubclass(class_imported, InContextBeforeMiddle):
                        middles_before_in_context.append(class_imported())
                    elif issubclass(class_imported, InContextBackMiddle):
                        middles_back_in_context.append(class_imported())

                except Exception:
                    print(traceback.format_exc())
        middles_before_out_context.sort(key=lambda x: x.sort)
        middles_before_in_context.sort(key=lambda x: x.sort)
        middles_back_in_context.sort(key=lambda x: x.sort)
        middles_back_out_context.sort(key=lambda x: x.sort)

        return (
            middles_before_out_context,
            middles_before_in_context,
            middles_back_in_context,
            middles_back_out_context
        )
