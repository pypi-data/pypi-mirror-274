# -*- coding: utf-8 -*-

import os
from py_mini_racer import py_mini_racer


class Ths:
    """ 同花顺 """
    __js_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ths.js")

    @staticmethod
    def ths_headers():
        """ 生成同花顺的cookie并添加到headers中 """
        with open(Ths.__js_file) as f:
            js_content = f.read()
        js_code = py_mini_racer.MiniRacer()
        js_code.eval(js_content)
        v_code = js_code.call("v")
        headers = {
            "host": "q.10jqka.com.cn",
            "Referer": "https://q.10jqka.com.cn/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "Cookie": f"v={v_code}",
            "X-Requested-With": "XMLHttpRequest"
        }
        return headers
