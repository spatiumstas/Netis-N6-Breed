import os
import sys
import shutil
import time
import socket
import paramiko
import gateway
import filecmp
from scp import SCPClient
from getpass import getpass

GREEN = "\033[92m"
RESET = "\033[0m"

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data')

def get_hex_offset(filename, offset, length):
    with open(filename, 'rb') as f:
        f.seek(offset)
        return f.read(length).hex()

def get_mtd_partitions(client):
    stdin, stdout, stderr = client.exec_command('cat /proc/mtd')
    data = stdout.read().decode()
    lines = data.split('\n')
    partitions = {}
    for line in lines:
        if 'u-boot' in line:
            partitions['u-boot'] = line.split(':')[0]
        elif 'factory' in line:
            partitions['factory'] = line.split(':')[0]
    return partitions

def backup(client, partitions):
    commands = [
        (f'dd if=/dev/{partitions["u-boot"]} of=/tmp/u-boot_stock.bin count=1024', 'u-boot_stock.bin'),
        (f'dd if=/dev/{partitions["factory"]} of=/tmp/OpenWrt.mtd2.bin count=1024', 'OpenWrt.mtd2.bin')
    ]
    for command, filename in commands:
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        time.sleep(2)
        data = stdout.read() + stderr.read()
        scp = SCPClient(client.get_transport())
        scp.get(f'/tmp/{filename}', os.path.join(DATA_DIR, filename))
        if filename == 'OpenWrt.mtd2.bin':
            new_filename = 'EEPROM_'+ get_hex_offset(os.path.join(DATA_DIR, filename), 0x7EF20, 6).upper() + '.bin'
            shutil.copy(os.path.join(DATA_DIR, filename), os.path.join(DATA_DIR, new_filename))
            if filecmp.cmp(os.path.join(DATA_DIR, filename), os.path.join(DATA_DIR, new_filename)):
                os.remove(os.path.join(DATA_DIR, filename))
            filename = new_filename
        if os.path.exists(os.path.join(DATA_DIR, filename)):
            if filename == 'u-boot_stock.bin':
                print(f'Стоковый загрузчик {filename} успешно сохранен в папку Data')
            else:
                print(f'{filename} успешно сохранен в папку Data, отправьте его в Telegram @spatiumstas/@yeezio для установки KeeneticOS')
        else:
            print(f'Ошибка при сохранении {filename}')


def write_loader(client):
    stdin, stdout, stderr = client.exec_command('insmod mtd-rw i_want_a_brick=1')
    scp = SCPClient(client.get_transport())
    scp.put(os.path.join(DATA_DIR, 'breed_netis_n6.bin'), '/tmp/breed_netis_n6.bin')
    stdin, stdout, stderr = client.exec_command('mtd write /tmp/breed_netis_n6.bin u-boot', get_pty=True)
    time.sleep(2)
    data = stdout.read() + stderr.read()

def main():
    print (f"{GREEN}+--------------------------------------------------------------+")
    print ("|          Breed installer for Netis N6 by shallador           |")
    print (f"+--------------------------------------------------------------+{RESET}")

    router_ip = gateway.get_ip_address()
    username = 'root'
    password = 'root'
    ssh_port = '22'

    try:
        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=router_ip, username=username, password=password, port=ssh_port)
            time.sleep(2)
            partitions = get_mtd_partitions(client)
            backup(client, partitions)
            write_loader(client)
            print ("")
            print(f"{GREEN}+--------------------------------------------------------------+")
            print("|              Загрузчик Breed успешно установлен              |")
            print(f"+--------------------------------------------------------------+{RESET}")
            print ("")
            print ('Перезагрузка в Breed...')
            client.exec_command('reboot')
            time.sleep(2)
            client.close()
            sys.exit()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
