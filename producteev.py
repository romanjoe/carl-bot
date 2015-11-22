from __future__ import print_function
import httplib2
import socket
import sys
import requests

import json

from telegram import BotRoutines

bot_act = BotRoutines()

from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

BASE_URL = 'https://www.producteev.com'
OAUTH_AUTH = BASE_URL + '/oauth/v2/auth'
OAUTH_TOKEN = BASE_URL + '/oauth/v2/token'
OAUTH_REVOKE = BASE_URL + '/oauth/v2/revoke'

REDIRECT_URI = 'http://localhost:8080'

CLIENT_ID = '564dafa4b0fa098476000003_4wy9lqspla800g4osow4ww4kwckwo4cs8sw40oo4sgg0wwgc0c'
CLIENT_SECRET = '3dovrg34jjwg8844gckg84w4sw40cgss44k4g4c0s44ss0go8o'
CREDENTIALS_FILE = "producteev_credentials.json"


class Producteev():

    def __init__(self, caller_id, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.caller_id = caller_id
        self.http = self.authorize_client()


    def __get_credentials(self):

        flow = OAuth2WebServerFlow(self.client_id,
                                   self.client_secret,
                                   scope='',
                                   redirect_uri=self.redirect_uri,
                                   auth_uri=OAUTH_AUTH,
                                   token_uri=OAUTH_TOKEN,
                                   revoke_uri=OAUTH_REVOKE)

        storage = Storage(CREDENTIALS_FILE)
        credentials = storage.get()

        if not credentials or credentials.invalid:
            if flags:
                #credentials = tools.run_flow(flow=flow, storage=storage, flags=flags)
        ########
                if not flags.noauth_local_webserver:
                    success = False
                    port_number = 0
                    for port in flags.auth_host_port:
                        port_number = port
                        try:
                            httpd = tools.ClientRedirectServer((flags.auth_host_name, port),
                                                         tools.ClientRedirectHandler)
                        except socket.error:
                            pass
                        else:
                            success = True
                            break
                    flags.noauth_local_webserver = not success
                    if not success:
                        print('Failed to start a local webserver listening '
                              'on either port 8080')
                        print('or port 8090. Please check your firewall settings and locally')
                        print('running programs that may be blocking or using those ports.')
                        print()
                        print('Falling back to --noauth_local_webserver and continuing with')
                        print('authorization.')
                        print()

                if not flags.noauth_local_webserver:
                    oauth_callback = 'http://%s:%s/' % (flags.auth_host_name, port_number)
                else:
                    oauth_callback = client.OOB_CALLBACK_URN
                flow.redirect_uri = oauth_callback
                authorize_url = flow.step1_get_authorize_url()

                #bot_act.send_text(self.caller_id, authorize_url)

                code = 0
                #
                # if not flags.noauth_local_webserver:
                #     # import webbrowser
                #     # webbrowser.open(authorize_url, new=1, autoraise=True)
                #     print('Your browser has been opened to visit:')
                #     print()
                #     print('    ' + authorize_url)
                #     print()
                #     print('If your browser is on a different machine then '
                #           'exit and re-run this')
                #     print('application with the command-line parameter ')
                #     print()
                #     print('  --noauth_local_webserver')
                #     print()
                # else:
                #     print('Go to the following link in your browser:')
                #     print()
                #     print('    ' + authorize_url)
                #     print()
                # code = 0
                # if not flags.noauth_local_webserver:
                #     httpd.handle_request()
                #     if 'error' in httpd.query_params:
                #         sys.exit('Authentication request was rejected.')
                #     if 'code' in httpd.query_params:
                #         code = httpd.query_params['code']
                #     else:
                #         print('Failed to find "code" in the query parameters '
                #               'of the redirect.')
                #         sys.exit('Try running with --noauth_local_webserver.')
                # else:
                #    code = input('Enter verification code: ').strip()

                try:
                    credentials = flow.step2_exchange(code, http=None)
                except client.FlowExchangeError as e:
                    sys.exit('Authentication has failed: %s' % e)

                storage.put(credentials)
                credentials.set_store(storage)
                print('Authentication successful.')

########

                print ('Credentials stored to' + CREDENTIALS_FILE)
        return credentials

    def authorize_client(self):

        credentials = self.__get_credentials()

        http = credentials.authorize(httplib2.Http())

        return http

    def get_project(self):
        # payload = {'Authorization:Bearer' : 'MzUxMWYwNDE5YjE1MGU0M2JhODYzZmNkYjRhZTJkMzJjMmNhNzcxODAyOTIxYWU0MmYxMDI1NTM3MjUwOTRhNw'} # Or simply set the Authorization header of your request with Bearer THEACCESSTOKEN
        # r = requests.get('https://www.producteev.com/api/projects/564b0a9eb0fa09b376000000', headers=payload)
        # print (r.content())
        url = BASE_URL + "/api/users/me/default_project" # '/api/projects/' + '564b0a86b0fa09c376000002'

        print (url)

        response, content = self.http.request(url, 'GET', None, None)


        print (content)
        c = json.loads(content)
        cc = c['project']
        project_title = cc['title']
        project_id = cc['id']
        ccc = cc['creator']
        first_name = ccc['firstname']
        last_name = ccc['lastname']
        email = ccc['email']
        url = cc['url']
        last_updated_at = ccc['updated_at']
#        unread_notifications = ccc['unread_notifications']

        print ('Project: ' + project_title)
        print ('Project ID: ' + project_id)
        print ('URL: ' + url)
        print ('Creator: ' + first_name + ' ' + last_name)
        print ('Creator email: ' + email)
        print ('Last updated at: ' + last_updated_at)
#        print ('Unread notifications : ' + str(unread_notifications))

        result = 'Project: ' + project_title + '\n' + \
                 'Project ID: ' + project_id + '\n' + \
                 'URL: ' + url + '\n' + \
                 'Creator: ' + first_name + ' ' + last_name + '\n' + \
                 'Creator email: ' + email + '\n' + \
                 'Last updated at: ' + last_updated_at + '\n'
#                 'Unread notifications : ' + str(unread_notifications)

        #print (cc.keys())
        #print (ccc.keys())

        return result
