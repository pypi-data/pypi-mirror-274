# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/29
@Software: PyCharm
@disc:
======================================="""
import json

bypass_domains = [
    "127.0.0.1",
    "192.168.0.0/16",
    "172.16.0.0/16",
    "10.0.0.0/8"
]
bypass_domains_fp = "test.json"
if __name__ == '__main__':
    with open(bypass_domains_fp, "w") as bypass_domains_file:
        json.dump(bypass_domains, bypass_domains_file)
    bypass_domains = json.load(open(bypass_domains_fp))
    print(bypass_domains)
