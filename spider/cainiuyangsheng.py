# -*- coding: utf-8 -*-
import json

import requests
import time

if __name__ == '__main__':
    for i in range(1,1000):
        response = requests.get("https://www.cnys.com/shicai/33451.html")
        print(response)