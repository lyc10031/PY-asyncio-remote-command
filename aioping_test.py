import asyncio
import aioping
import queue
import time
from configparser import ConfigParser
from itertools import chain


start = time.time()

q1 = queue.Queue()
q2 = queue.Queue()

async def do_ping(host):
    try:
        delay = await aioping.ping(host,2) * 1000
        info = host + ' OK'
        q2.put(info)
        #print("Ping response in %s ms" % delay)
    except TimeoutError:
        info = host + ' ERROR'
        q2.put(info)
        #print("Timed out")

def get_host_info():
    file = 'host.conf'   # 配置文件
    cfg = ConfigParser()
    with open(file,'r') as fp:
        cfg.read_file(chain(['[global]'], fp), source=file)
        hosts_list = cfg.get('test_hosts', 'hosts_nums').split(';')
        host_info = [cfg.get('test_hosts', i) for i in hosts_list]
    [q1.put(i) for i in host_info]
    # print(host_info)

def split_host_info(host_info):
#    host,port,username,password = host_info.split(';')
    info = host_info.split(';')
#    return host,port,username,password
    return info 

def tic():
    print('at %1.5f seconds' % (time.time() - start))
    return 'at %1.1f seconds' % (time.time() - start)

def main():
    get_host_info()
    h_list = ['172.16.80.49','172.16.80.50','172.16.80.34','172.16.80.48','172.16.80.36','172.16.80.41']
    host_info_list = []
    while not q1.empty():
        host = split_host_info(q1.get())
        host_info_list.append(host)
#    ks = [asyncio.ensure_future(do_ping(i)) for i in h_list]
    ks = [asyncio.ensure_future(do_ping(i[0])) for i in host_info_list]
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(do_ping("google.com"))
    loop.run_until_complete(asyncio.gather(*ks))
#    with open("online_host.txt",'w') as f:
#        while not q2.empty():
#            print(q2.get(),file=f)
    online = []
    while not q2.empty():
        ping_result = q2.get()
        host,status = ping_result.split(' ')
        if status == "OK":
            online.append(host)
            print(ping_result)
        else:
            print(ping_result)

#    tic()
    return online
        
#    tic()

if __name__ == "__main__":
    main()
    tic()
