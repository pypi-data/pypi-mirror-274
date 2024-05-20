#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/5/20 16:34
# Author:Zhang HongTao
# @File:time_zone.py

import logging
import pytz
from datetime import datetime


class BeijingFormatter(logging.Formatter):
    converter = datetime.fromtimestamp
    timezone = pytz.timezone('Asia/Shanghai')  # 北京所在时区

    def formatTime(self, record, date_fmt=None):
        dt = self.converter(record.created, self.timezone)
        if date_fmt:
            s = dt.strftime(date_fmt)
        else:
            t = dt.strftime(self.default_time_format)
            s = self.default_msec_format % (t, record.msecs)
        return s
