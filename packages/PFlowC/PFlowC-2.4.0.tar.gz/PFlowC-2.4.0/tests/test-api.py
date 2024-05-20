# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/29
@Software: PyCharm
@disc:
======================================="""
import requests

proxies = {
    'http': 'socks5://10.2.1.0:7890',
    'https': 'socks5://10.2.1.0:7890',
}
if __name__ == '__main__':
    resp = requests.get("https://ip.useragentinfo.com/json")
    print(resp.json())
