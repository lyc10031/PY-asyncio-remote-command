import asyncio
import paramiko
import os

def split_host_info(host_info):
    host,port,username,password = host_info.split(';')
    return host,port,username,password

def record_host_status(name,info):
    """ 获取记录结果 写入文件中 """
    try:
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
    except:
        pass
    # 获取mac地址 与正常mac地址进行匹配
    normal_info = ['00:1f:c1:1d:bc:5d','00:1f:c1:1d:bc:51','00:1f:c1:1d:bc:53','00:1f:c1:1d:bc:63']
    if info in normal_info:
        mac_status = "OK"
    else:
        mac_status = 'ERROR'
    with open(f'tmp/{name}_status.txt','a+') as s:
        tt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        s.write(f'{tt} <--* {name} {info} {mac_status}*--> times\n')


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

