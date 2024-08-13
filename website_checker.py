#SSL CHECKER and Website checker
import socket
import ssl
import datetime
import http.client as httplib
import urllib.parse

def ssl_check(hostname):

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
        print(f'{hostname} expires on: {Exp_on}')
        print('------------------------')
        print('------------------------')
        return True
    except:
        print('domain has not SSL')
        print('------------------------')
        print('------------------------')
        return False

domains = ['github.com', 'githubfalse.com']
for hostname in domains:
    ssl_check(hostname)

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

#website_code_status('github.com')
#website_code_status('githubdalse.com')



