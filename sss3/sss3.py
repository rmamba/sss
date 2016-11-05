import sys
import boto3

commands = ['init', 'i', 'status', 's', 'clone', 'pull', 'push', 'commit', 'c', 'help', 'h']

def help():
    print('Help...')
    return

def init():
    return

def status():
    return

def clone():
    return

def pull():
    return\

def push():
    return

def commit():
    return

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
