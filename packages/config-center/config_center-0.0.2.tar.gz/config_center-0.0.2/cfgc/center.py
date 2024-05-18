#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# # # # # # # # # # # # 
"""
 ╭───────────────────────────────────────╮  
 │ center.py   2024/5/17-22:02
 ╰───────────────────────────────────────╯ 
 │ Description:
    
"""  # [By: HuYw]

# region |- Import -|
from importlib import import_module
from pathlib import Path
import pickle
import shutil
import sys
import os
# endregion

# Absolute Path of cfgc package
PATH_X = Path(os.path.split(os.path.realpath(__file__))[0])
PATH_CUSTOM = PATH_X / 'custom'
PATH_ENV = PATH_CUSTOM / 'envs'

# Class Domain
class Domain:
    def __init__(self, data: dict={}):
        assert isinstance(data, dict)
        self.data = data
    def __setitem__(self, key, val):
        self.data[key] = val
    def __getitem__(self, key):
        return self.data.get(key)

# Class Env
class Environment:
    def __init__(self, name='base', domain: dict={}, engine: Path='.', load: str=None):
        if load is None:
            self.define(name, domain, engine)
        else:   # 如果是加载环境则 直接构建 并 启动engine包
            self.load(load)
            self.drive()
    def define(self, name, domain: dict={}, engine: Path='.'):
        """
        创建配置环境

        :param name: 环境名称
        :param data: 环境全局变量 [对于大型数据, 也可以存储数据仓库路径, 挂载访问]
        :param engine: 加载的驱动包目录 [不需要在site-packages里, 会自动加载管理]
        """
        self.name = name
        self.domain = domain if isinstance(domain, Domain) else Domain(domain)
        self.__engine = str(engine)
        self.engine = Path(engine)
    def drive(self):
        """
        驱动, 加载驱动目录作为 包, 通过engine 调用内部函数

        :return:
        """
        sys.path.insert(0, os.path.dirname(self.engine))
        self.engine = import_module(os.path.basename(self.engine))
        sys.path.pop(0)  # 剔除
    def save(self, safe=True):
        """
        储存该环境文件, 之后可以随时加载

        :param safe: 安全模式, 默认开启 ——当存在env时提示是否覆盖, 否则将直接覆盖
        :return:
        """
        assert self.engine.is_absolute(), "engine must be a Absolute Path"    # 仅支持绝对定位 & 目录
        assert self.engine.is_dir(), "engine only can be a Dir"
        save_path = PATH_ENV / f'{self.name}.pkl'
        if os.path.exists(save_path):
            status = True and safe
            while status:
                replace = input(f"There has been an env called: {self.name}, overwrite ?(yes/no)\n")
                if replace == 'yes':
                    break
                elif replace == 'no':
                    return
                else:
                    continue
        # store as name.pkl
        with open(save_path, "wb") as cfg:
            pickle.dump({
                "name": self.name,
                "domain": self.domain,
                "engine": self.__engine,
            }, cfg)
        print(f"CFGC-Env [{self.name}] has been saved to: {save_path}")
    def load(self, name):
        """
        由环境名称 加载

        :param name: 环境名称
        :return:
        """
        with open(PATH_ENV / f'{name}.pkl', "rb") as cfg:
            cfg = pickle.load(cfg)
        self.define(**cfg)
    def rename(self, name):
        self.name = name