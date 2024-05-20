# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/5/10
@Software: PyCharm
@disc:
======================================="""
import importlib.resources as pkg_resources

if __name__ == '__main__':
    GEOIP_DB_PATH = str(pkg_resources.path('PFlowC.utils', 'Country.mmdb'))
    print(GEOIP_DB_PATH)
