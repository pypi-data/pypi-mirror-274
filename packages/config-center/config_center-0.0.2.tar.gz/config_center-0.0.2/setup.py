#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# # # # # # # # # # # # 
"""
 ╭───────────────────────────────────────╮  
 │ setup.py   2024/5/17-21:57
 ╰───────────────────────────────────────╯ 
 │ Description:
    SetUp for config-center [site-package]
"""  # [By: HuYw]

# region |- Import -|
import setuptools
# endregion

VERSION = '0.0.2'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="config-center",
    version=VERSION,
    author="VaterFus",
    author_email="1107818699@qq.com",
    description="A site-package to create your local pypi-sitepackage, manage your own scripts pack as an env!",#包的简述
    long_description=long_description,    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://github.com/WhatMelonGua/config-center",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',    #对python的最低版本要求
)