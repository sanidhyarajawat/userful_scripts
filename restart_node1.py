#!/usr/bin/python3.5 -u

from pexpect import pxssh
import getpass
import time
import os

def connect_to_node1():
    print("Restarting service in Node 1.")
    try:
        s = pxssh.pxssh()
        ip = "10.31.91.197"
        hostname = "S0I1I2SHRSCS001"
        username = "plzz017t"
        password = "PolandWroclawIBM@98"
        #hostname = input('hostname: ')
        #username = input('username: ')
        #password = getpass.getpass('password: ')
        #hostname = sys.argv[1]
        #username = sys.argv[2]
        #if len(sys.argv) < 3:
        #    print("Please run the script as: ./script_name <hostname> <username> <password>")
       # elif len(sys.argv) == 3:
       #     print("Password not provided in command. Please provide the password now.")
        #    password = getpass.getpass('password: ')
        #elif len(sys.argv) == 4:
        #    password = sys.argv[3]
        s.login (hostname, username, password)
        s.sendline ('service shib stop')   # run a command
        s.prompt()             # match the prompt
        print(s.before)          # print everything before the prompt.
        s.sendline ('service shib start')
        s.prompt()
        print(s.before)
        s.logout()
        print("Service restarted in Node 1.")
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(str(e))

def connect_to_node2():
    print("Restarting service in Node 2.")
    try:
        s = pxssh.pxssh()
        ip = "10.31.91.196"
        hostname = "S0I2I2SHRSCS001"
        username = "plzz017t"
        password = "PolandWroclawIBM@98"
        #hostname = input('hostname: ')
        #username = input('username: ')
        #password = getpass.getpass('password: ')
        #hostname = sys.argv[1]
        #username = sys.argv[2]
        #if len(sys.argv) < 3:
        #    print("Please run the script as: ./script_name <hostname> <username> <password>")
        #elif len(sys.argv) == 3:
        #    print("Password not provided in command. Please provide the password now.")
        #    password = getpass.getpass('password: ')
        #elif len(sys.argv) == 4:
        #    password = sys.argv[3]
        s.login (hostname, username, password)
        s.sendline ('service shib stop')   # run a command
        s.prompt()             # match the prompt
        print(s.before)          # print everything before the prompt.
        s.sendline ('service shib start')
        s.prompt()
        print(s.before)
        s.logout()
        print("Service restarted in Node 2.")
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(str(e))


def enter_into_root():
    try:
        os.system("sudo su")
        os.system(password)
    except Exception as ex:
        print("Exception in enter_into_root")
        print(str(ex))


if __name__ == "__main__":
    connect_to_node2()
    time.sleep(240)
    connect_to_node1()
    print("Restart completed in both nodes!")

