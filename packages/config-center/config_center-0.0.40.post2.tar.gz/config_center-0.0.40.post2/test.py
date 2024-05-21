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
import cfgc
import datetime
import os
# endregion

cfgc.envs.view()

# region |- Create an Env -|
env = cfgc.center.Environment()
env.define(
    "cfgc-base",  # env name: test
    {"date": datetime.datetime.now().strftime('%Y-%m-%d')},  # env domain(data): test
    os.path.join(cfgc.center.PATH.center)  # env engine(site-package): cfgc self
    )
env.save(safe=True)
# Input: yes
# endregion

del env

# region |- Reload the Env -|
from pprint import pprint
load_env = cfgc.center.Environment(load="cfgc-base")     # env name: test
pprint(dir(load_env.engine))
# endregion

# region |- Export the Env -|
load_env.export("../export")
del load_env
# reload
load_env = cfgc.center.Environment()
load_env.load_path("../export")     # env name: export
pprint(dir(load_env.engine.center))
print(load_env.domain)
# endregion