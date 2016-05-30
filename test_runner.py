import os
from py2js.utils import translate, get_stdlib

TESTS_DIR = os.path.join(os.path.dirname(__file__), "tests")
CACHE_DIR = os.path.join(TESTS_DIR, '.cache')
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)

STDLIB_JS = get_stdlib()


def translate_file(pypath):
    translated = translate(open(pypath).read())
    js_path = os.path.join(CACHE_DIR, os.path.basename(pypath))
    with open(js_path, 'w') as fd:
        fd.write(STDLIB_JS)
        fd.write("\n// ========== END OF STDLIB ===========\n")
        fd.write(translated)
    return js_path


for fname in os.listdir(TESTS_DIR):
    fpath = os.path.join(TESTS_DIR, fname)
    if not os.path.isfile(fpath):
        continue
    print("* processing {}".format(fname))

    ret = os.system("python3 {}".format(fpath))
    if ret:
        raise RuntimeError("PY FAILED")
    print("PY - ok ;)")
    js_path = translate_file(fpath)

    ret = os.system("node {}".format(js_path))
    if ret:
        raise RuntimeError("JS FAILED")
    print("JS - ok ;)")


