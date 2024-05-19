#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# # # # # # # # # # # # 
"""
 ╭───────────────────────────────────────╮  
 │ __init__.py.py   2024/5/17-21:57
 ╰───────────────────────────────────────╯ 
 │ Description:
    Handler cfgc's envs
"""  # [By: HuYw]

# region |- Import -|
import os
from pathlib import Path
# endregion

PATH = Path(os.path.split(os.path.realpath(__file__))[0])
FORMAT = "pkl"

# Func

def view():
    envs = os.listdir(PATH)
    for i, e in enumerate(envs):
        print(f"{i} -\t{e.split('.', maxsplit=1)[0]}")


def delete(name: str):
    envs = os.listdir(PATH)
    for e in envs:
        fname, ftype = e.split('.', maxsplit=1)
        if ftype == "pkl" and name == fname:
            os.remove(PATH / e)
            print(f"Env File [{e}] has been removed")
            return
    print(f"Failed! Env [{name}] not found, use 'view()' to list all envs.")