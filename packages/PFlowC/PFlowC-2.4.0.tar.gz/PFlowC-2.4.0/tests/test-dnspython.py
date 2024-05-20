# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/30
@Software: PyCharm
@disc:
======================================="""
from PFlowC.utils.net import is_domestic

if __name__ == '__main__':
    # 查询A记录（IPv4地址）
    domains = ["baidu.com", "github.com", "api.github.com", "microsoft.com"]
    for domain_name in domains:
        # domain_name = input('请输入一个域名：')
        print(domain_name, ":", is_domestic(domain_name))
        # print("=" * 20, "%0.2f" % , "=" * 20)

        # 若要查询其他类型的记录，只需更改查询类型，如MX记录：
        # mx_answers = resolver.query(domain_name, 'MX')
        # for rdata in mx_answers:
        #     print(f"{domain_name} 的MX记录：{rdata.exchange}，优先级：{rdata.preference}")
