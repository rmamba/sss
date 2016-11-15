import sys,json
import os
import boto3
import ctypes


commands = ['init', 'i', 'status', 's', 'clone', 'pull', 'push', 'commit', 'c', 'help', 'h', 'config']
fname="sss3"
jsonpath="./"+fname+"/config.json"



def help():
    print('Help...')
    return

def init():
    # If directory sss3 doesnt exist
    if not os.path.isdir(fname):
        if os.name == 'nt':
            os.makedirs(fname)
            ctypes.windll.kernel32.SetFileAttributesW(ur""+fname,0x02)
        else:
            os.makedirs("."+fname)
        open("./"+fname+"/config.json", 'w').close()

    else:
        if not os.path.isfile(jsonpath):
            open(jsonpath, 'w').close()


    if len(sys.argv) == 5:
        #Insert new user into json file if doesnt exists - overwrite if exists
        with open(jsonpath, 'r') as outfile:
            try:
                data=json.load(outfile)
            except:
                data={}

        data[sys.argv[2]]={"Secret_Access_Key": sys.argv[3], "Access_Key_ID": sys.argv[4]}
        with open(jsonpath, 'w') as outfile:
            json.dump(data, outfile)


    elif len(sys.argv) == 3:
        print("ahhdwq")





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
