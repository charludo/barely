"""
Utils that help with testing.
Nothing complex, just makes the
rest of the tests more readable
"""
import os
import shutil


def read(filename):
    with open(os.path.join("test", "ref", filename), "r") as file:
        contents = file.read()
        file.close()
        return contents


def write(filename, content):
    with open(os.path.join("test", "ref", filename), "w") as file:
        file.write(content)
        file.close()


def concat_yaml(str, n):
    if n == 0:
        return ""
    sep = "---\n"
    c = n * (sep + str) + sep
    return c


def prepare_tempfiles(yaml=0, markdown=0, dict=False, html=False, out=""):
    if dict:
        in_c = read("dict")
    elif html:
        in_c = read("html")
    else:
        in_yaml = read("yaml")
        in_md = read("markdown")
        in_c = concat_yaml(in_yaml, yaml) + markdown * in_md

    if not len(out):
        out_c = read("empty")
    else:
        out_c = read(out)
    write("in", in_c)
    write("out", out_c)


def cleanup():
    for path in ["in", "out", "temp"]:
        if os.path.exists(os.path.join("test", "ref", path)):
            os.remove(os.path.join("test", "ref", path))


def remove(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
