import asyncio
import paramiko
import time,itertools,sys
import queue
from configparser import ConfigParser
from itertools import chain

q1 = queue.Queue()


async def send_command(host_info):
    host,port,username,password = split_host_info(host_info)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host,port=int(port),username=username,password=password)
        # 获取命令结果
        # command_mac = "/usr/sbin/ifconfig | grep ether | awk 'NR==1 {print $2}'"
        # stdin,stdout,stderr = ssh.exec_command(command_mac)
        # await asyncio.sleep(0.1)
        # status = stdout.read().decode('UTF-8').strip()
        # record_host_status(host_mark,status)
        # print(host,'<-->','[',status,']')

        command_date = f'date'
        stdin,stdout,stderr = ssh.exec_command(command_date)
        await asyncio.sleep(0.1)
        status = stdout.read().decode('UTF-8').strip()
        # record_host_status(host_mark,status)
        print(host,'<-->','[',status,']','times')

        # 执行reboot命令
        # command_reboot = f'/sbin/reboot'
        #ssh.exec_command(command_reboot)
        # await asyncio.sleep(0.1)
        #status = stdout.read().decode('UTF-8').strip()

    except Exception as e:
        print(f' * {host} cannot be connected !!!')
        print(e)
        time.sleep(0.2)
    finally:
        ssh.close()





def split_host_info(host_info):
    host,port,username,password = host_info.split(';')
    return host,port,username,password

def get_host_info(online_host=None):
    file = 'host.conf'   # 配置文件
    cfg = ConfigParser()
    with open(file,'r') as fp:
        cfg.read_file(chain(['[global]'], fp), source=file)
        hosts_list = cfg.get('test_hosts', 'hosts_nums').split(';')
        host_info = [cfg.get('test_hosts', i) for i in hosts_list]
   
    if online_host != None:
        [q1.put(i) for i in host_info if i.split(";")[0] in online_host]
    else:     
        [q1.put(i) for i in host_info]
    # print(host_info)

def main(online_host=None):
    start_time = time.time()
    get_host_info(online_host)
    host_info_list = []
    while not q1.empty():
        host_info_list.append(q1.get())
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(send_command(i)) for i in host_info_list]
    loop.run_until_complete(asyncio.wait(tasks))
    #loop.stop()
    #print('程序运行耗时：%s' % (time.time() - start_time))

if __name__ == '__main__':
    main()

