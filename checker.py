#SSL CHECKER and Website checker
import binascii
import os
import time
import csv
import socket
import ssl
import datetime
import http.client as httplib
import urllib.parse
from http.client import HTTPConnection

def website_code_status(url):
    try:
        protocol, host, path, query, fragment = urllib.parse.urlsplit(url)
        #Check for no schema given
        custom_protocol = 'Empty Protocol' if not protocol else protocol

        #validate schema for the correct requst
        if protocol == "http":
            conntype = httplib.HTTPConnection
        elif protocol == "https":
            conntype = httplib.HTTPSConnection
        else:
            raise ValueError("unsupported protocol: " + custom_protocol)
        
        conn = conntype(host)
        conn.request("HEAD", path)
        resp = conn.getresponse()
        conn.close()
        #print(dir(resp))
        print(resp.status)
        print(resp.reason)

        return True
    
    except Exception as e:
        print(f'[ERROR]: {e}')

#website_code_status('https://github.com/')
#website_code_status('https://githubfalse.com/')


class WebsitesChecker():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_file = None

    def __call__(self):
        try:
            return self.handle()
        except Exception as err:
            print(err)
            time.sleep(2)
        finally:
            print("Work Done, Closing checker")
            

    def handle(self):
        http_schema='http://url/'
        https_scham='https://url/'
        self.create_csv_file()
        file = open("websites.csv", 'r')
        csv_file = csv.DictReader(file)

        for websites in csv_file:
            enable = self.ssl_check(websites['website'])
            website = https_scham.replace('url', websites['website']) if enable else http_schema.replace('url', websites['website'])
            response = self.website_code_status(website)
            content_value = dict(
                website=website, 
                ssl='Active' if enable else 'Deactivate',
                reason=response[1][1],
                status=response[1][0]
            )
            self.csv_file.writerow(content_value)
            del content_value

    def create_csv_file(self):
        title = 'WebsitesChecked-'+binascii.hexlify(os.urandom(3)).decode()+'-T'+datetime.datetime.now().strftime('%H-%M-%S')
        csv_file = open(f'{title}.csv', mode='w', newline='')
        #File Map
        fieldnames = ['website','ssl', 'reason', 'status']

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        self.csv_file = writer

    def ssl_check(self, hostname):

        print(f'Checking SSL for: {hostname}')
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        conn.settimeout(3.0)

        try:
            conn.connect((hostname, 443))
            #Get the main info about the SSL cert
            ssl_info = conn.getpeercert()
            #Get expiration date of the SSL cert
            Exp_on = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
            print(f'{hostname} SSL Enable')
            #print(f'{hostname} expires on: {Exp_on}')
            #print('------------------------')
            #print('------------------------')
            return True
        except:
            print('domain has not SSL')
            #print('------------------------')
            #print('------------------------')
            return False

    def website_code_status(self, url):
        try:
            protocol, host, path, query, fragment = urllib.parse.urlsplit(url)
            #Check for no schema given
            custom_protocol = 'Empty Protocol' if not protocol else protocol

            #validate schema for the correct requst
            if protocol == "http":
                conntype = httplib.HTTPConnection
            elif protocol == "https":
                conntype = httplib.HTTPSConnection
            else:
                raise ValueError("unsupported protocol: " + custom_protocol)
            
            conn = conntype(host)
            conn.request("HEAD", path)
            resp = conn.getresponse()
            conn.close()
            #print(dir(resp))
            #print(resp.status)
            #print(resp.reason)

            values = [resp.status, resp.reason]

            return True, values
    
        except Exception as e:
            print(f'[ERROR]: {e}')
            values = [e, None]
            return False, values

checker = WebsitesChecker()
checker()