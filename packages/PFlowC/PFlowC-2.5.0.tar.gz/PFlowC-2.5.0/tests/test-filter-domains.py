# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/5/10
@Software: PyCharm
@disc:
======================================="""
LOCAL_REGION_CODE = 'CN'
AGENT_DOMAINS = {
    "CN": [
        "github.com",
        "api.github.com"
    ]
}
if __name__ == '__main__':
    x = AGENT_DOMAINS[LOCAL_REGION_CODE]
    y = ["github.com", "api.github.com"]
    for z in [x, y]:
        print(type(z), z)
        for domain in ["github.com", "api.github.com"]:
            res = domain in z
            print(domain, ":", res)
