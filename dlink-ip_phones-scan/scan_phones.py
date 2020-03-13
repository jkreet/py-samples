#!/usr/bin/python
    # -*- coding: utf-8 -*-
# Сканирование диапазона IP в несколько потоков
# Получение параметров IP телефона через telnet 
# 
#
import sys
import re
import telnetlib
import threading
import socket
import ipaddress
from pprint import pprint

from Auth import auth
from HTMLRequests import GetNumber

login = b'admin'
passw = b'admin'
start_ip = '10.0.0.50'
end_ip = '10.0.0.250'
timeout = 5

phones = []

class Phone(object):
    def __init__(self, ip, status, username):
        self.ip = ip
        self.status = status
        self.username = username

    def auth(self, login, passw):
        if 'auth' in session.cookies:
            auth = session.cookies['auth']

            hashed = hashlib.md5(str.encode(username) + b":" + str.encode(password) + b":" + str.encode(auth))

            encoded = username + ':' + hashed.hexdigest()

            # print(encoded)

            post_data = {
                'encoded': encoded,
                'nonce': auth
            }

            return post_data

        return False


class GetInfoThread(threading.Thread):
    def __init__(self, ip, name):
        """Инициализация потока"""

        threading.Thread.__init__(self)
        self.name = name
        self.ip = ip

    def run(self):
        """Запуск потока"""
        try:
            tn = telnetlib.Telnet(self.ip, 23, timeout)
        except Exception as excp:
            # print(excp)
            pass
        else:
            tn.read_until(b"Login:")
            tn.write(login + b'\r\n')
            tn.read_until(b"Password:")
            tn.write(passw + b"\r")
            tn.read_until(b"#")
            tn.write(b"show sip\r")
            sip_info = tn.read_until(b"#").decode('utf-8')
            tn.close()

            if sip_info:
                result = re.search(r'Status\.+\:(?P<status>\w+)', sip_info)
                if result:
                    status = result.group('status')
                result = re.search(r'Name\.+\:(?P<username>[a-zA-Z.]+)', sip_info)
                if result:
                    username = result.group('username')
                    # pprint(username)

                if 'status' in locals():
                    phones.append(Phone(self.ip, status, username))
        finally:
            pass



def main(iplist):
    """ Run the program """

    print('Searching...')

    for item, ip in enumerate(iplist):
        name = "thread %s" % (item + 1)
        thread = GetInfoThread(ip, name)
        thread.start()

    while threading.activeCount() > 1:
        pass

    phones.sort(key=lambda item: socket.inet_aton(item.ip), reverse=False)

    print ('№\tIP address\tStatus\tUsername')
    for item, phone in enumerate(phones):
        print(str(item + 1) + '\t' + phone.ip + '\t' + phone.status + '\t' + phone.username)


def ips(start_ip, end_ip):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    ips_array = []

    for ip_int in range(int(start), int(end)):
        ips_array.append(str(ipaddress.IPv4Address(ip_int)))

    return(ips_array)



    # import socket, struct
    # start = struct.unpack('>I', socket.inet_aton(start))[0]
    # end = struct.unpack('>I', socket.inet_aton(end))[0]
    # return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end)]


if __name__ == "__main__":
    iplist = ips(start_ip, end_ip)

    main(iplist)
