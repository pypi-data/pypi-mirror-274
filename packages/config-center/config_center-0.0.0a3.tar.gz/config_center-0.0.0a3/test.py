#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# # # # # # # # # # # # 
"""
 ╭───────────────────────────────────────╮  
 │ tmp.py   2024/5/17-22:27
 ╰───────────────────────────────────────╯ 
 │ Description:
    Pls Test under the path of cfgc
"""  # [By: HuYw]

# region |- Import -|
from cfgc import center as cc
import datetime
import os
# endregion

# region |- Create an Env -|
env = cc.Environment()
env.define(
    "cfgc-base",  # env name: test
    {"date": datetime.datetime.now().strftime('%Y-%m-%d')},  # env domain(data): test
    os.path.join(cc.PATH.center)  # env engine(site-package): cfgc self
    )
env.save(safe=True)
# Input: yes
# endregion

del env

# region |- Reload the Env -|
from cfgc import center as cc
from pprint import pprint
load_env = cc.Environment(load="cfgc-base")     # env name: test
pprint(dir(load_env.engine))
# endregion

# region |- Export the Env -|
load_env.export("../export")
del load_env
# reload
load_env = cc.Environment()
load_env.load_path("../export")     # env name: export
pprint(dir(load_env.engine.center))
print(load_env.domain)
# endregion