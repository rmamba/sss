import sys,json
import os
from StringIO import StringIO

import boto3
import ctypes
import ConfigParser

import botocore

commands = ['init', 'i', 'status', 's', 'clone', 'pull', 'push', 'commit', 'c', 'help', 'h', 'config', 'connect']
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

    if not len(sys.argv) in [3,5]:
        print "Error: Wrong number of arguments"
        exit(1)

    elif sys.argv[2] == "GUID":
        print "GUID of directory is",read_config()["GUID"]

    else:
        if not os.path.isfile(jsonpath):
            print "Configuration file does not exists, please run command init first"
            exit(0)

        else:
            dec=raw_input("Configuration already exists are you sure to overwrite it? Type y for yes and n for no")
            if dec.startswith('y'):
                guid=read_config()["GUID"]
                if checkconnectiontobucket(sys.argv[3],sys.argv[4],guid):
                    data = {"GUID": guid, "Secret_Access_Key": sys.argv[3], "Access_Key_ID": sys.argv[4]}
                    with open(jsonpath, 'w') as outfile:
                        json.dump(data, outfile)
                    print "Configuration saved!"
                    exit(0)
                else:
                    print "User doesn't have access to resource in AWS, exiting without saving..."

            elif dec.startswith('n'):
                print "Exiting without saving new configuration"
                exit(0)




#-----------------------------------Helper functions-------------------------------------------------

#Reading config and return it
def read_config():
    with open(jsonpath) as json_data:
        data = json.load(json_data)
        return data


#Check if connection to bucket is succesfull
def checkconnectiontobucket(accesid,secretkey,bucketname):
            contobucket=True
            session = boto3.Session(aws_access_key_id=accesid,
            aws_secret_access_key=secretkey)
            s3 = session.resource('s3')
            bucket = s3.Bucket(bucketname)

            try:
                s3.meta.client.head_bucket(Bucket=bucketname)
            except:
                contobucket = False
            return contobucket





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

