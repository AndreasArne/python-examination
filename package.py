#! /usr/bin/env python3
import shutil
import os
import examiner
from importlib.util import find_spec



def read_requirements(filename):
    with open(filename) as f:
        return f.readlines()



def find_modules_paths(modules):
    modules_paths = []
    for module in modules:
        module_path = find_spec(module).origin
        modules_paths.append((os.path.dirname(module_path), module))
    return modules_paths



def build(modules):
    try:
        shutil.rmtree("build")
    except FileNotFoundError:
        pass
    try:
        os.mkdir("build")
    except FileExistsError:
        pass
    shutil.copytree('examiner', 'build/examiner', ignore=shutil.ignore_patterns("*pycache*"))
    for module in modules:
        shutil.copytree(
            module[0],
            "build/examiner/"+module[1],
            ignore=shutil.ignore_patterns("*pycache*")
        )


    shutil.make_archive("build/examiner-"+examiner.__version__, 'zip', "build/examiner")



if __name__ == "__main__":
    modules = find_modules_paths(read_requirements("requirements.txt"))
    build(modules)
