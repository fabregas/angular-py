import os
import ast

from .py2js_parser import Py2JsParser

STDLIB_DIR = os.path.join(os.path.dirname(__file__), "../stdlib")


def translate(pycode):
    node = ast.parse(source=pycode)
    p = Py2JsParser()
    p.visit(node)
    return p.result()


def get_stdlib():
    stdlib = ""
    for fname in os.listdir(STDLIB_DIR):
        fpath = os.path.join(STDLIB_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        stdlib += "\n// -------- {} -------\n".format(fname)
        if fname.endswith('.js'):
            with open(fpath) as fd:
                stdlib += fd.read()
        elif fname.endswith('.py'):
            with open(fpath) as fd:
                stdlib += translate(fd.read())
        else:
            raise RuntimeError('unknown file {}'.format(fpath))
    return stdlib


