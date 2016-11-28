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
        return self.config

    # Check if connection to bucket is succesfull
    def __check_connection_to_bucket(self, accesid, secretkey, bucketname):
        connection_to_bucket = True
        session = boto3.Session(aws_access_key_id=accesid, aws_secret_access_key=secretkey)
        s3 = session.resource('s3')
        bucket = s3.Bucket(bucketname)
        try:
            s3.meta.client.head_bucket(Bucket=bucketname)
        except:
            connection_to_bucket = False
        return connection_to_bucket

    # If directory sss3 doesnt exist
    def __check_hidden_folder_exists(self):
        if not os.path.isdir(self.FOLDER_NAME):
            if os.name == 'nt':
                os.makedirs(self.FOLDER_NAME)
                ctypes.windll.kernel32.SetFileAttributesW(ur"" + self.FOLDER_NAME, 0x02)
            else:
                os.makedirs("." + self.FOLDER_NAME)
            open("./" + self.FOLDER_NAME + "/config.json", 'w').close()

        else:
            if not os.path.isfile(self.CONFIG_FILE):
                open(self.CONFIG_FILE, 'w').close()


    def __init__(self, arguments):
        self.arguments = arguments

        if len(self.arguments) < 2:
            self.__help()
            return

        cmd = self.arguments[1]
        if cmd not in self.COMMANDS:
            self.__help()
            return


        if cmd == 'init' or cmd == 'i':
            self.__init()

        if cmd == 'config':
            self.__config()


    def __help(self):
        print('usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration')
        return


    def __init(self):
        self.__check_hidden_folder_exists()
        if len(self.arguments) == 5:
            #Insert data into json
            data={"GUID":self.arguments[2],"Secret_Access_Key": self.arguments[4], "Access_Key_ID": self.arguments[3]}
            with open(self.CONFIG_FILE, 'w') as outfile:
                json.dump(data, outfile)


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
        if (not os.path.isfile(self.CONFIG_FILE)):
            print "This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command."
            return

        if len(self.arguments)<3:
            print 'usage: sss3 config <argument> <argument> <argument>\n\nArguments:\n\tAWS\tPrints AWS credentials. Or sets credentials if new are provided.\n\tGUID\tPrint name of this repository.'
            return

        if self.arguments[2] == "GUID":
            if len(self.arguments) < 4:
                print "GUID:", self.__read_config()["GUID"]
            else:
                print "GUID is read only!!!"
            return


        if self.arguments[2] == "AWS":
            if len(self.arguments)==3:
                print 'AccessKeyID: \t{0}\nSecretAccessKey: \t{1}'.format(self.__read_config()["Access_Key_ID"], self.__read_config()["Secret_Access_Key"])
                return

            if len(self.arguments) == 5:
                dec=raw_input("Configuration already exists are you sure to overwrite it? Type y for yes and n for no")
                if dec.startswith('y'):
                    if self.__check_connection_to_bucket(self.arguments[3],self.arguments[4], self.__read_config()['GUID']):
                        data = {"GUID": self.__read_config()["GUID"], "Secret_Access_Key": self.arguments[3], "Access_Key_ID": self.arguments[4]}
                        with open(self.CONFIG_FILE, 'w') as outfile:
                            json.dump(data, outfile)
                        print "Configuration saved!"
                        return
                    else:
                        print "User doesn't have access to resource in AWS, exiting without saving..."
                else:
                    print "Exiting without saving new configuration"
            else:
                print "You need to specify both AccessKeyID and SecretAccessKey to change them!!!"


if __name__ == '__main__':
    SSS3(sys.argv)


