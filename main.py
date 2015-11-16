import os
import fnmatch
import requests
import time
import subprocess as sp

import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

INTERVAL = 10
ADMIN_ID = 162457279
URL_BASE = 'https://api.telegram.org/bot'
TOKEN = '152394201:AAE6wwKF-y9gddMrXUTAnGNbGrifJKFHU-I'
URL_TOKEN = URL_BASE + TOKEN

""" Copy the credentials from the console """

CLIENT_ID = '251746268845-gk3fdoc0pqspsjq0q3svthvdeggjbr4v.apps.googleusercontent.com'
CLIENT_SECRET = 'ffLzVzAgrkifWaFhZZK3BlUS'

""" Check https://developers.google.com/derive/scopes """
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
""" Redirect URI fron installed apps  """
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
""" Path to file to uplodad to gdive """
FILENAME = "doc.txt"

offset = 0
from_id = 0
"""
"""

def check_updates():
    global offset
    global from_id
    data = {'offset': offset + 1, 'limit': 5, 'timeout': 0}

    try:
        request = requests.post(URL_TOKEN + '/getUpdates', data=data)
    except:
        log_event('Error update')

    if not request.status_code == 200: return False
    if not request.json()['ok']: return False
    for update in request.json()['result']:
        offset = update['update_id']
        if not 'message' in update or not 'text' in update['message']:
            log_event('Unknown update' % update)
            continue

        from_id = update['message']['chat']['id']
        name = update['message']['chat']['first_name']

        if from_id != ADMIN_ID:
            send_text("You're not my Master!", from_id)
            log_event('Unauthorized access attempt')
            continue

        message = update['message']['text']
        parameters = (offset, name, from_id, message)
        log_event('Message (id%s) from %s (id%s): "%s"' % parameters)

        run_command(*parameters)

"""
"""
def post_document(caller_id):
    """ Go throught the OAuth 2.0 flow and retrieve credentials """
    flow = OAuth2WebServerFlow(
        CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print('Go to the following link in your browser: ' + authorize_url)
    send_text(from_id, authorize_url)

    code = raw_input('Enter verification code, you got: ').strip()
    credentials = flow.step2_exchange(code)

    """ Create an httplib2 object and authorize it with our credentials """
    http = httplib2.Http()
    http = credentials.authorize(http)

    drive_service = build('drive', 'v2', http=http)

    """ Insert a file """
    media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)

    body = {'title': 'My Doc',
            'description': 'A test document',
            'mimeType': 'text/plain'}


    file = drive_service.files().insert(body=body, media_body=media_body).execute()
    pprint.pprint(file)


"""
"""

def send_text(chat_id, text):
    log_event('Sending text to %s: %s' % (chat_id, text))

    data = {'chat_id': chat_id, 'text': text}
    request = requests.post(URL_TOKEN + '/sendMessage', data=data)

    if not request.status_code == 200:
        return False
    return request.json()['ok']

"""
"""


def log_event(text):
    event = '%s >> %s' % (time.ctime(), text)
    print event


def run_command(offset, name, from_id, cmd):
    if cmd == '/ping':
        send_text(from_id, 'pong')

    elif cmd == '/start':
        send_text(from_id, "Hi, ma name is Carl, Carl. "
                           "You can make me do various actions,"
                           "show system info, post and take images"
                           "and other, not all implemented yet, so"
                           "try /help to get available actions.")
        show_help(from_id)

    elif cmd == '/help':
        show_help(from_id)

    elif cmd == '/uptime':
        check_uptime(from_id)

    elif cmd == '/kernel':
        check_kernel_version(from_id)

    elif cmd == '/inet':
        check_inet_interface(from_id)

    elif cmd == '/check_cam':
        check_camera_connection(from_id)

    elif cmd == '/posttodrive':
        post_document(from_id)

"""
"""


def show_help(caller_id):
    send_text(caller_id, 'You can use the following caommands: \n' +
                         '/help - to show this message \n' +
                         '/ping - to get pong \n' +
                         '/uptime - to check uptime on host \n' +
                         '/kernel - to find a kernel version of host \n' +
                         '/inet - to display interfaces configuration \n' +
                         '/check_cam - to check if camera is connected to host \n')

"""
"""


def check_uptime(caller_id):
    send_text(caller_id, "Checking uptime on RPi2 at home")
    uptime = sp.check_output(["uptime"])
    print uptime
    send_text(caller_id, uptime)


def check_inet_interface(caller_id):
    send_text(caller_id, "Inet interfaces on RPi2")
    inet = sp.check_output("ip link", stderr=sp.STDOUT, shell=True)
    print inet
    send_text(caller_id, inet)
"""
"""


def check_camera_connection(caller_id):
    camera = ''
    send_text(caller_id, "Checking if camera is connected to RPi2")
    devs = os.listdir("/dev")
    for dev in devs:
        if fnmatch.fnmatch(dev, "video*"):
            camera = "/dev/" + dev
            send_text(caller_id, "Found camera at %s" % camera)
            break
    if camera == '':
        send_text(from_id, "No cameras found")

"""
"""


def check_kernel_version(caller_id):
    send_text(caller_id, "Kernel version on RPi2")
    kernel = sp.check_output(["uname", "-a"])
    print kernel
    send_text(caller_id, kernel)

"""
"""

if __name__ == '__main__':
    while True:
        try:
            check_updates()
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print 'Interrupted by user'
            break
