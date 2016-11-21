import sys,json
import os
from StringIO import StringIO

import boto3
import ctypes
import ConfigParser


commands = ['init', 'i', 'status', 's', 'clone', 'pull', 'push', 'commit', 'c', 'help', 'h', 'config']
fname="sss3"
jsonpath="./"+fname+"/config.json"
awspath=os.path.expanduser('~')+"\\aws"
os.environ["AWS_SHARED_CREDENTIALS_FILE"]=awspath+"\\credentials"


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
        #Insert data into json
        data={"GUID":sys.argv[2],"Secret_Access_Key": sys.argv[3], "Access_Key_ID": sys.argv[4]}
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
    write=False;
    if len(sys.argv)>5:
        print "Error:Too many arguments"

    else:
        #check if global config location exists if not create it
        if not os.path.isdir(awspath):
            if os.name == 'nt':
                os.makedirs(awspath)
                ctypes.windll.kernel32.SetFileAttributesW(ur""+awspath,0x02)
            else:
                os.makedirs("."+awspath)

        parser = ConfigParser.ConfigParser()
        parser.readfp(StringIO('[default]'))
        parser.set('default', 'aws_access_key_id', sys.argv[3])
        parser.set('default', 'aws_secret_access_key', sys.argv[4])

        if os.path.isfile(awspath+ "\\credentials"):
            if os.stat(awspath+ "\\credentials").st_size != 0:
                dec=raw_input("Are you sure to overwrite credentials? Type y for yes and n  for no")
                if dec.startswith('y'):
                    write=True;
                elif dec.startswith('n'):
                    print "Exiting without saving credentials..."
                    exit(0)
            else:
                write=True
        else:
            write=True

        if write:
            print "Saving configuration to global config file"
            with open(awspath + "\\credentials", 'w') as configfile:
                parser.write(configfile)


    #s3 = boto3.resource('s3')
    #bucket = s3.Bucket('sss3-test')
    #for obj in bucket.objects.all():
    #    print(obj)


    return ""


def read_config(section,path):
    config = ConfigParser.RawConfigParser()
    config.read(path)
    return config.items(section)





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
