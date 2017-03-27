import collections
import hashlib
import sys
import json
import os
import boto3
import ctypes
import re
import uuid
from os.path import expanduser

import botocore


class SSS3:
    aws_access_key_id = None
    aws_secret_access_key = None
    config = None
    arguments = None

    COMMANDS = ['init', 'i', 'status', 's', 'clone', 'pull', 'push', 'commit', 'c', 'help', 'h', 'config', 'connect','add','remove']
    FOLDER_NAME = '.sss3'
    CONFIG_FILE = './{0}/config.json'.format(FOLDER_NAME)
    CONTENT_FILE='./{0}/content.json'.format(FOLDER_NAME)
    TEMP_FILE = './{0}/temp.json'.format(FOLDER_NAME)
    home_directory = '{0}/aws/credentials'.format(expanduser("~"))
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = home_directory



# Helper-Functions----------------------------------------START------------------------------------------------------------------

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
    def __check_creation_of_bucket(self, session, bucketname, remove=True):
        s3 = session.resource('s3')
        try:
            s3.create_bucket(Bucket=bucketname)
            bucket = s3.Bucket(bucketname)
            if remove==True:
                bucket.delete()

            return True
        except Exception as e:
            if 'BucketAlreadyOwnedByYou' in str(e):
                return True
            print (e)
            return False

    #Check if valid domain name
    def __check_valid_domain(self,domain):
        if not re.search(u'^[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*$', domain) is not None:
            return False
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


    def __check_config_folder_exists(self):
        if os.path.isdir(self.FOLDER_NAME):
            if os.path.isfile(self.CONFIG_FILE):
                if os.path.isfile(self.CONTENT_FILE):
                    return True
            else:
                return False
        else:
            return False


    def __check_config_online(self,bucket):
        exists=False
        try:
            bucket.Object(self.CONTENT_FILE[2:]).load()
            exists=True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                exists = False
            else:
                raise
        return exists



    # izdelaj json na podlagi poti-------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------
    #zdruzi 2 slovarja zaradi problema pri slovar.update
    def __dict_update(self,d, u):
        for k, v in u.iteritems():
            if isinstance(d, collections.Mapping):
                if isinstance(v, collections.Mapping):
                    r = self.__dict_update(d.get(k, {}), v)
                    d[k] = r
                else:
                    d[k] = u[k]
            else:
                d = {k: u[k]}
        return d

    #izdelaj drevesno strukturo jsona s podane poti in zadnji del poti poslje v __folder_structure_json da pridobi full json
    def __nested_dict(self,path, level=0):
        tmp = path.split("/")
        dict = {tmp[level]: {"children": {}}}
        if level == len(tmp) - 1:
            dict = self.__folder_structure_json(path)
        else:
            dict[tmp[level]]["children"] = self.__nested_dict(path, level + 1)
        return dict

    #izdelaj json strukturo na podlagi poti
    def __folder_structure_json(self,path):
        if path.endswith("/"):
            path = path[:-1]
        if path == ".":
            dict = {}
        else:
            dict = {os.path.basename(path): {}}
        if os.path.isdir(path):
            if not path == ".":
                dict[os.path.basename(path)] = {"children": {}}
            for key in os.listdir(path):
                if path == ".":
                    dict.update(self.__folder_structure_json(path + "/" + key))
                else:
                    dict[os.path.basename(path)]["children"].update(self.__folder_structure_json(path + "/" + key))
        else:
            dict[os.path.basename(path)] = {
                'type': 'file',
                'last_modified_timestamp': os.stat(path).st_mtime,
                'created_timestamp': os.stat(path).st_ctime,
                'size': os.path.getsize(path),
                'crc': hashlib.md5(open(path, 'r').read()).hexdigest()
            }

        return dict

    # -----------------------------------------------------------------------------------------------------------------------


    #create path list from dictionary
    def __json_path_print(self,dict, prefix=""):
        list = []
        for key in dict:
            if 'children' in dict[key]:
                list.extend(self.__json_path_print(dict[key]['children'], prefix + key + "/"))
            else:
                list.append(prefix + key)
        return list


    #upload directory with given path
    def __uploadDirectoryjson(self,bucket):
        d = json.loads(open(self.CONTENT_FILE).read())
        list=self.__json_path_print(d)
        for key in list:
            bucket.upload_file(Key=key, Filename=key)
        return True


    #download online content and check differences with local content
    def __diference_on_content(self,bucket,way):
        onlinecontent = (bucket.Object(self.CONTENT_FILE[2:])).get()["Body"].read()
        onlinejson = json.loads(onlinecontent)
        local = json.loads(open(self.CONTENT_FILE).read())
        if(way):
            difference=self.__jsondiff(onlinejson, local, '', [])
            with open(self.CONTENT_FILE, 'w') as outfile:
                json.dump(self.__dict_update(local,onlinejson), outfile, indent=2)
            return difference
        else:
            return self.__jsondiff(local,onlinejson,'',[])


    def __jsondiff(self,local, online, path='', todo=[]):
        for key in local.keys():
            if not online.has_key(key):
                if local[key].has_key('children'):
                    todo = todo + self.__json_path_print(local[key]["children"], path + key + "/")
                else:
                    todo.append(path + key)
            else:
                if local[key].has_key('children'):
                    todo = todo+self.__jsondiff(local[key]["children"], online[key]["children"], path + key + "/")
                else:
                    if local[key]["last_modified_timestamp"] > online[key]["last_modified_timestamp"]:
                        todo.append(path + key)
        return todo

    #update .sss3 folder and write it to content.json
    def __update_contentjson(self):
        localjson = json.loads(open(self.CONTENT_FILE).read())
        with open(self.CONTENT_FILE, 'w') as outfile:
            json.dump(self.__dict_update(localjson, self.__nested_dict(self.CONTENT_FILE[2:])), outfile, indent=2)


#Helper-Functions----------------------------------------END------------------------------------------------------------------

    def __init__(self, arguments):
        self.arguments = arguments

        if len(self.arguments) < 2:
            self.__help()
            return

        cmd = self.arguments[1]
        if cmd not in self.COMMANDS:
            self.__help()
            return

        if cmd in ['init', 'i']:
            self.__init()

        if cmd == 'config':
            self.__config()

        if cmd == 'push':
            self.__push()

        if cmd == 'add':
            self.__add()

        if cmd == 'remove':
            self.__remove()

        if cmd == 'pull':
            self.__pull()

        if cmd == 'clone':
            self.__clone()


    def __help(self):
        print('usage: sss3 <command> [<args>]\n\nCommands:\n\tinit\tCreate an empty repository\n\tconfig\tView or set values for this repositories configuration')
        return

    def __init(self):
        if len(self.arguments) > 5 or len(self.arguments) < 2:
            self.__help()
            return

        if os.path.isfile(self.CONFIG_FILE):
            print('Directory already initialised')
            return

        # if directory is not inicialized
        if len(self.arguments) == 5:
            if self.__check_valid_domain(self.arguments[2]):
                # check if creation of bucket is possible
                session = boto3.Session(aws_access_key_id=self.arguments[3], aws_secret_access_key=self.arguments[4])
                if self.__check_creation_of_bucket(session, self.arguments[2], False):
                    self.__check_hidden_folder_exists()
                    data = {"GUID": self.arguments[2].lower(), "Secret_Access_Key": self.arguments[4],
                            "Access_Key_ID": self.arguments[3]}
                    with open(self.CONFIG_FILE, 'w') as outfile:
                        json.dump(data, outfile)
                    with open(self.CONTENT_FILE, 'w') as outfile:
                        json.dump({}, outfile)
                    print('Repository initialised!')
            else:
                print('You entered invalid domain name!!!\nPlease enter GUID that is also a valid domain name.')
            return

        if len(self.arguments) == 3:
            if self.__check_valid_domain(self.arguments[2]):
                session = boto3.Session()
                if self.__check_creation_of_bucket(session, self.arguments[2], False):
                    self.__check_hidden_folder_exists()
                    data = {"GUID": self.arguments[2].lower()}
                    with open(self.CONFIG_FILE, 'w') as outfile:
                        json.dump(data, outfile)
                    with open(self.CONTENT_FILE, 'w') as outfile:
                        json.dump({}, outfile)
                    print('Repository initialised!')
                    return

        if len(self.arguments) == 2:
            session = boto3.Session()
            guid = uuid.uuid4()
            if self.__check_creation_of_bucket(session, str(guid), False):
                self.__check_hidden_folder_exists()
                data = {"GUID": guid}
                with open(self.CONFIG_FILE, 'w') as outfile:
                    json.dump(data, outfile)
                with open(self.CONTENT_FILE, 'w') as outfile:
                    json.dump({}, outfile)
                print('Repository initialised!')
                return
        self.__help()



    def __status(self):
        print('Status')
        #print
        return

    def __clone(self):
        if len(self.arguments)==5:
            session = boto3.Session(aws_access_key_id=self.arguments[3], aws_secret_access_key=self.arguments[4])
            try:
                s3 = session.resource('s3')
                bucket = s3.Bucket(self.arguments[2])
                #Download everything from S3 cloud
                for key in bucket.objects.all():
                    if os.path.dirname(key.key) != '':
                        if not (os.path.isdir(os.path.dirname(key.key))):
                            os.makedirs(os.path.dirname(key.key))
                    bucket.download_file(key.key, key.key)
                    print "File downloaded: " + key.key + " complete"
                data = {"GUID": self.arguments[2].lower,"Secret_Access_Key":self.arguments[4],"Access_Key_ID":self.arguments[3]}
                with open(self.CONFIG_FILE, 'w') as outfile:
                    json.dump(data, outfile)
            except Exception as e:
                print e
            return



        self.__help()
        return


    def __add(self):
        #print all differences between local and content.json
        if len(self.arguments)==2:
            local = json.loads(open(self.CONTENT_FILE).read())
            print "Different files between directory and SSS3 content are:"
            for key in  self.__jsondiff(self.__nested_dict("."), local, '', []):
                print key
            return
        if self.__check_config_folder_exists():
            for path in self.arguments[2:]:
                if os.path.exists(path):
                    #load local json
                    localjson = json.loads(open(self.CONTENT_FILE).read())
                    #update local json with new dict
                    with open(self.CONTENT_FILE, 'w') as outfile:
                        json.dump(self.__dict_update(localjson, self.__nested_dict(path)), outfile, indent=2)
                    self.__update_contentjson()

                else:
                    print "Error: File:",path,"missing!"
        else:
            print "Configuration setup missing, please run init command first."
            return
        return


    def __remove(self):
        if len(self.arguments)<3:
            print "Please specify files to remove"
            return
        if self.__check_config_folder_exists():
            for path in self.arguments[2:]:
                if os.path.exists(path):
                    print ""

                else:
                    print "Error: File:",path,"missing, it wont be added!"
        else:
            print "Configuration setup missing, please run init command first."
            return


    def __pull(self):
        if len(self.arguments)==2:
            if self.__check_config_folder_exists():
                config = self.__read_config()
                session = boto3.Session(aws_access_key_id=config["Access_Key_ID"],
                                        aws_secret_access_key=config["Secret_Access_Key"])
                s3 = session.resource('s3')
                bucket = s3.Bucket(config["GUID"])
                if self.__check_config_online(bucket):
                    todownload = self.__diference_on_content(bucket, True)
                    for key in todownload:
                        if os.path.dirname(key)!='':
                            if not (os.path.isdir(os.path.dirname(key))):
                                os.makedirs(os.path.dirname(key))
                        bucket.download_file(key, key)
                        print "File downloaded: "+key+" complete"
                else:
                    print "Online configuration missing"
                    return
            else:
                print "Configuration setup missing, please run init command first."
                return
        else:
            self.__help()
            return

        return


    def __push(self):
        if len(self.arguments) == 2:
            if self.__check_config_folder_exists():
                config=self.__read_config()
                session = boto3.Session(aws_access_key_id=config["Access_Key_ID"], aws_secret_access_key=config["Secret_Access_Key"])
                s3 = session.resource('s3')
                bucket = s3.Bucket(config["GUID"])

                #check if configuration on cloud exists
                if self.__check_config_online(bucket):
                    toupload=self.__diference_on_content(bucket,False)
                    if self.CONTENT_FILE[2:] in toupload:
                        #merge new config with onlineconfig
                        onlinecontent = (bucket.Object(self.CONTENT_FILE[2:])).get()["Body"].read()
                        onlinejson = self.__dict_update(json.loads(onlinecontent), json.loads(open(self.CONTENT_FILE).read()))
                        with open(self.TEMP_FILE, 'w') as outfile:
                            json.dump(onlinejson, outfile)
                        toupload.remove(self.CONTENT_FILE[2:])
                        bucket.upload_file(Key=self.CONTENT_FILE[2:], Filename=self.TEMP_FILE)
                        os.remove(self.TEMP_FILE)
                    for key in toupload:
                        bucket.upload_file(Key=key, Filename=key)
                        print "File uploaded",os.path.basename(key)
                else:
                    self.__update_contentjson()
                    self.__uploadDirectoryjson(bucket)

                #<---------HELPERS--------->
                #self.__uploadDirectory(".", bucket)
                #s3.Bucket('sss3-push-test').objects.delete()
                #s3.meta.client.upload_file('test.txt', 'sss3-push-test', 'test.txt')
                #bucket.upload_file(Key=".sss3/content.json", Filename=".sss3/content.json")
                #print for testing bucket
                #data = open('test.txt', 'rb')
                #s3.Bucket('sss3-push-test').put_object(Key='test.txt', Body=data)

                #for key in bucket.objects.all():
                #    print(key.key)

                # <---------HELPERS--------->

                return
            else:
                print "Configuration setup missing, please run init command first."
                return
        self.__help()



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


