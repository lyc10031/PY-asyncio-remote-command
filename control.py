import asyncio
import aioping
import queue
import time
from configparser import ConfigParser
from itertools import chain
import aioping_test
import send_command
import os


start_time = time.time()

def tic():
    return 'at %1.4f seconds' % (time.time() - start_time)

def get_host_info():
    file = 'conf/host.conf'   # 配置文件
    cfg = ConfigParser()
    with open(file,'r') as fp:
        cfg.read_file(chain(['[global]'], fp), source=file)
        hosts_list = cfg.get('test_hosts', 'hosts_nums').split(';')
        host_info = [cfg.get('test_hosts', i) for i in hosts_list]
#    [q1.put(i) for i in host_info]
    return host_info

def record_host_status(name,info,report=None):
    name = name.split(".")[-1]
    """ 获取记录结果 写入文件中 """
    try:
        if not os.path.exists('result'):
            os.mkdir('result')
    except:
        pass

    # 获取mac地址 与正常mac地址进行匹配
#    normal_info = ['00:1f:c1:1d:bc:5d','00:1f:c1:1d:bc:51','00:1f:c1:1d:bc:53','00:1f:c1:1d:bc:63']
##    if info in normal_info:
#        mac_status = "OK"
#    else:
#        mac_status = 'ERROR'
    with open(f'result/{name}_status.txt','a+') as s:
        tt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        s.write(f'{tt} <--* {name} {info} {report} *--> \n')

if __name__ == "__main__":
    #online = aioping_test.main()
    #time.sleep(0.5)
    #send_command.main(online)
#    print(tic())
    for t in range(1,3):
        all_host = get_host_info()
        host_mark = [i.split(";")[0] for i in all_host]
        online = aioping_test.main()
    #    for i in online:
    #        print(i)
    
        [record_host_status(i,t,"OK") for i in host_mark if i in online]
        [record_host_status(i,t,"ERROR") for i in host_mark if i not in online]
        send_command.main(online)
        print(tic())
        time.sleep(5)


