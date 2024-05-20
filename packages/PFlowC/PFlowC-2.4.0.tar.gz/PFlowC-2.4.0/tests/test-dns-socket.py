# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/30
@Software: PyCharm
@disc:
======================================="""
import socket

import geoip2.database

GEOIP_DB_PATH = '/Users/shadikesadamu/数据/geoip/Country.mmdb'
geoip_db = geoip2.database.Reader(GEOIP_DB_PATH)
if __name__ == '__main__':
    # 查询域名对应的IP地址
    hostname = 'github.com'
    ip_addresses = socket.getaddrinfo(hostname, None)

    for record in ip_addresses:
        # 每个record是一个元组，包含(family, type, proto, canonname, sockaddr)
        address_info = record[4]
        ip = address_info[0]
        response = geoip_db.country(ip)
        print(f"{hostname} <===> {address_info}  <===>  {response.country.iso_code}  <===>  {response}")
