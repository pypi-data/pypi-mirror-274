#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/3/27 17:44
# Author:Zhang HongTao
# @File:read_conf_from_ini.py


import configparser
import os


class GetConfInfo:
    """获取配置文件中的信息
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式

        :param args:
        :param kwargs:
        """
        if not cls.__instance:
            cls.__instance = super(GetConfInfo, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, conf_path="config/conf.ini"):
        self.conf = configparser.RawConfigParser()
        self.conf_path = os.path.join(os.getcwd(), conf_path)
        self.conf.read(self.conf_path)
        self.env_value = os.getenv("ENV")  # 获取环境变量
        self.field = self.get_field()

    def get_field(self):
        """根据环境变量ENV记录的值，获取不同环境的配置参数

        :return:
        """
        field = "ENV-DEV"
        if not self.env_value:
            return field
        content_split = str(self.env_value).lower()
        if 'test' in content_split:
            field = "ENV-TEST"
        elif 'uat' in content_split:
            field = "ENV-UAT"
        elif 'prod' in content_split:
            field = "ENV-PROD"
        return field

    def get_conf_info(self, key):
        """获取key对应的配置信息

        :param key:
        :return:
        """
        conf_info = self.conf.get(self.field, key)
        return conf_info
