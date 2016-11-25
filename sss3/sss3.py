import sys
import json
import os

import boto3
import ctypes

class SSS3:
    aws_access_key_id = None
    aws_secret_access_key = None
    config = None
    arguments = None

    COMMANDS = ['init', 'i', 'status', 's', 'clone', 'pull', 'push', 'commit', 'c', 'help', 'h', 'config', 'connect']
    FOLDER_NAME = '.sss3'
    CONFIG_FILE = './{0}/config.json'.format(FOLDER_NAME)

    # Reading config and return it
    def __read_config(self):
        with open(self.CONFIG_FILE) as json_data:
            self.config = json.load(json_data)

    # Check if connection to bucket is succesfull
    def __check_connection_to_bucket(accesid, secretkey, bucketname):
        connection_to_bucket = True
        session = boto3.Session(aws_access_key_id=accesid, aws_secret_access_key=secretkey)
        s3 = session.resource('s3')
        bucket = s3.Bucket(bucketname)

        try:
            s3.meta.client.head_bucket(Bucket=bucketname)
        except:
            connection_to_bucket = False
        return connection_to_bucket

    def __check_hidden_folder_exists(self):
        # If directory sss3 doesnt exist
        if not os.path.isdir(self.FOLDER_NAME):
            if os.name == 'nt':
                os.makedirs(self.FOLDER_NAME)
                ctypes.windll.kernel32.SetFileAttributesW(ur"" + self.FOLDER_NAME, 0x02)
            else:
                os.makedirs("." + self.FOLDER_NAME)
            open("./" + self.FOLDER_NAME + "/config.json", 'w').close()

        else:
            if not os.path.isfile(self.FOLDER_NAME):
                open(self.FOLDER_NAME, 'w').close()

    def __init__(self, arguments):
        self.arguments = arguments

        if len(self.arguments) < 2:
            self.__help()
            return

        cmd = self.arguments[1]
        if cmd not in self.COMMANDS:
            self.__help()
            return

        print("Command: %s" % cmd)

        if cmd == 'init' or cmd == 'i':
            self.__init()

        if cmd == 'config':
            self.__config()

    def __help(self):
        print('Help...')
        return

    def __init(self):
        self.__check_hidden_folder_exists()

        if len(self.arguments) == 5:
            #Insert data into json
            data={"GUID":self.arguments[2],"Secret_Access_Key": self.arguments[3], "Access_Key_ID": self.arguments[4]}
            with open(self.FOLDER_NAME, 'w') as outfile:
                json.dump(data, outfile)

        elif len(self.arguments) == 3:
            print("ahhdwq")

    def __status(self):
        return

    def __clone(self):
        return

    def __pull(self):
        return

    def __push(self):
        return

    def __commit(self):
        return

    def __config(self):
        if not os.path.isfile(self.FOLDER_NAME):
            print "Configuration file does not exists, please run command init first"
            return

        if self.arguments[2] == "GUID":
            if len(self.arguments) < 4:
                print "GUID of directory is", self.config["GUID"]
            else:
                print "GUID is read only!!!"
            return

        if self.arguments[2] == "AWS":
            if len(self.arguments) == 5:
                dec=raw_input("Configuration already exists are you sure to overwrite it? Type y for yes and n for no")
                if dec.startswith('y'):
                    if self.__check_connection_to_bucket(self.arguments[3],self.arguments[4], self.config['GUID']):
                        data = {"GUID": self.config['GUID'], "Secret_Access_Key": self.arguments[3], "Access_Key_ID": self.arguments[4]}
                        with open(self.FOLDER_NAME, 'w') as outfile:
                            json.dump(data, outfile)
                        print "Configuration saved!"
                    else:
                        print "User doesn't have access to resource in AWS, exiting without saving..."
                else:
                    print "Exiting without saving new configuration"
            else:
                print "Invalid number of arguments!"


if __name__ == '__main__':
    SSS3(sys.argv)

