import sys
import json
import os
import boto3
import ctypes
import re
import uuid
from os.path import expanduser

class SSS3:
    aws_access_key_id = None
    aws_secret_access_key = None
    config = None
    arguments = None

    COMMANDS = ['init', 'i', 'status', 's', 'clone', 'pull', 'push', 'commit', 'c', 'help', 'h', 'config', 'connect']
    FOLDER_NAME = '.sss3'
    CONFIG_FILE = './{0}/config.json'.format(FOLDER_NAME)
    home_directory = '{0}/aws/credentials'.format(expanduser("~"))
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = home_directory


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


    #Check bucket creation
    def __check_creation_of_bucket(self, session, bucketname, create):
        s3 = session.resource('s3')
        try:
            s3.create_bucket(Bucket=bucketname)
            bucket = s3.Bucket(bucketname)
            if not create:
                bucket.delete()
            return None
        except Exception as e:
            print e
            sys.exit(1)


    #Check if valid domain name
    def __check_valid_domain(self,domain):
        if not re.search(u'^[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*$', domain) is not None:
            print('Domain name is not safe!!')
            sys.exit(1)
        else:
            return True

    # If directory sss3 doesnt exist
    def __check_hidden_folder_exists(self):
        if not os.path.isdir(self.FOLDER_NAME):
            if os.name == 'nt':
                os.makedirs(self.FOLDER_NAME)
                ctypes.windll.kernel32.SetFileAttributesW((u'{0}'.format(self.FOLDER_NAME)), 0x02)
            else:
                os.makedirs("." + self.FOLDER_NAME)
            open("./" + self.FOLDER_NAME + "/config.json", 'w').close()

        else:
            if not os.path.isfile(self.CONFIG_FILE):
                open(self.CONFIG_FILE, 'w').close()
            else:
                return True


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
        if len(self.arguments) > 5 or len(self.arguments)<2:
            self.__help()
            return

        if os.path.isfile(self.CONFIG_FILE):
            print "Directory already inicialized"
            return

            #if directory is not inicialized
        if len(self.arguments)==5:
            if self.__check_valid_domain(self.arguments[2]):
                #check if creation of bucket is possible
                session = boto3.Session(aws_access_key_id=self.arguments[3],aws_secret_access_key=self.arguments[4])
                if self.__check_creation_of_bucket(session,self.arguments[2],True) is None:
                    self.__check_hidden_folder_exists()
                    data = {"GUID": self.arguments[2].lower(), "Secret_Access_Key": self.arguments[4], "Access_Key_ID": self.arguments[3]}
                    with open(self.CONFIG_FILE, 'w') as outfile:
                        json.dump(data, outfile)
                    print "Configuration saved!"
                    return

        if len(self.arguments)==3:
            if self.__check_valid_domain(self.arguments[2]):
                session = boto3.Session()
                if self.__check_creation_of_bucket(session, self.arguments[2],True) is None:
                    self.__check_hidden_folder_exists()
                    data={"GUID": self.arguments[2].lower()}
                    with open(self.CONFIG_FILE, 'w') as outfile:
                        json.dump(data, outfile)
                    print "Configuration saved!"
                    return

        if len(self.arguments)==2:
            creation=None
            session = boto3.Session()
            while(creation is None):
                guid = uuid.uuid4()
                creation=self.__check_creation_of_bucket(session, str(guid),True)
                if creation is None:
                    self.__check_hidden_folder_exists()
                    data = {"GUID": guid}
                    with open(self.CONFIG_FILE, 'w') as outfile:
                        json.dump(data, outfile)
                    print "Configuration saved!"
                    return
        self.__help()


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
            print('This directory is not a SSS3 archive!!!\nIf you would like to make it one run init command.')
            return

        if len(self.arguments)<3:
            print('usage: sss3 config <argument> <argument> <argument>\n\nArguments:\n\tAWS\tPrints AWS credentials. Or sets credentials if new are provided.\n\tGUID\tPrint name of this repository.')
            return

        if self.arguments[2] == "GUID":
            if len(self.arguments) < 4:
                print('GUID: {0}'.format(self.__read_config()["GUID"]))
            else:
                print('GUID is read only!!!')
            return


        if self.arguments[2] == "AWS":
            if len(self.arguments)==3:
                print('AccessKeyID: \t{0}\nSecretAccessKey: \t{1}'.format(self.__read_config()["Access_Key_ID"], self.__read_config()["Secret_Access_Key"]))
                return

            if len(self.arguments)==4:
                print('You need to specify both AccessKeyID and SecretAccessKey to change them!!!')
                return

            if len(self.arguments) == 5:
                if self.__check_connection_to_bucket(self.arguments[3],self.arguments[4], self.__read_config()['GUID']):
                    data = {"GUID": self.__read_config()["GUID"], "Secret_Access_Key": self.arguments[3], "Access_Key_ID": self.arguments[4]}
                    with open(self.CONFIG_FILE, 'w') as outfile:
                        json.dump(data, outfile)
                    print('New credentials were saved to your configuration file.')
                    return
                else:
                    print('Error accessing S3 bucket!!!\nPlease provide correct credentials that have access to bucket you are using.')



if __name__ == '__main__':
    SSS3(sys.argv)


