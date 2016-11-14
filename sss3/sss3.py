import sys
import os
import boto3
import ctypes


commands = ['init', 'i', 'status', 's', 'clone', 'pull', 'push', 'commit', 'c', 'help', 'h', 'config']
fname="sss3"



def help():
    print('Help...')
    return

def init():
    if not os.path.isdir(fname):
        if os.name == 'nt':
            os.makedirs(fname)
            ctypes.windll.kernel32.SetFileAttributesW(ur""+fname,0x02)
        else:
            os.makedirs("."+fname)




    return

def status():
    return

def clone():
    return

def pull():
    return

def push():
    return

def commit():
    return

def config():
    print("to je config")



if __name__ == '__main__':
    if len(sys.argv) < 2:
        help()
        quit()

    cmd = sys.argv[1]
    if cmd not in commands:
        help()
        quit()

    print("Command: %s" % cmd)

    if cmd == 'init' or cmd == 'i':
        init()

    if cmd == 'config':
        config()
