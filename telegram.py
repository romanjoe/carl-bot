import requests
import time
import fnmatch

API_BASE = 'https://api.telegram.org/bot'
TOKEN = '152394201:AAE6wwKF-y9gddMrXUTAnGNbGrifJKFHU-I'
URL_TOKEN = API_BASE + TOKEN

DEBUG = True


class Bot(object):
    """
    Abstract class
    """

    def __init__(self, api_base, token):
        self.api_base = api_base
        self.token = token

    @staticmethod
    def log_event(text):
        event = '%s >> %s' % (time.ctime(), text)
        print event

    @staticmethod
    def post_request(data, api_call):

        if DEBUG:
            Bot.log_event('Sending json %s to %s' % (data, data['chat_id'], ))
            # TODO: make more precise function fro logging

        response = requests.post(URL_TOKEN + api_call, data=data)

        if not response.status_code == 200:
            return False

        # TODO add raise exceptions for other codes

        return response.json()


class Telegram(Bot):

    """
    Telegram bot class, implements API calls
    """

    api = {'getMe': '/getMe',
           'sendMessage': '/sendMessage',
           'forwardMessage': '/forwardMessage',
           'sendPhoto': '/sendPhoto',
           'sendAudio': '/sendAudio',
           'sendDocument' : '/sendDocument',
           'sendSticker': '/sendSticker',
           'sendVideo': '/sendVideo',
           'sendVoice': '/sendVoice',
           'sendLocation': '/sendLocation',
           'sendChatAction': '/getUserProfilePhotos',
           'getUpdates': '/getUpdates',
           'setWebhook': '/setWebhook',
           'getFile': '/getFile'}

    def __init__(self, api_base=API_BASE, token=TOKEN):
        self.api_base = api_base
        self.token = token
        self.offset = 0
        self.chat_id = 0

    def get_me(self):

        if DEBUG:
            self.log_event('Sending getMe to check token is correct')

        data = {}
        return self.post_request(data, self.api['getMe'])

    def send_message(self, text):

        """
        Method to send text messages
        APIdoc URL: https://core.telegram.org/bots/api#sendmessage

        :param text: message to send
        :return: Message json object type - https://core.telegram.org/bots/api#message
        """
        if DEBUG:
            self.log_event('Sending text to %s: %s' % (self.chat_id, text))

        data = {'chat_id': self.chat_id, 'text': text}
        return self.post_request(data, self.api['sendMessage'])

    def forward_message(self, chat_id, from_chat_id, message_id):

        """
        Method for forwarding messages, using id's

        APIdoc URL: https://core.telegram.org/bots/api#forwardmessage

        :param chat_id: from what chat to forward
        :param from_chat_id: to which chat forward
        :param message_id: which message to forward
        :return: Message json object with sent message
        """

        data = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
        return self.post_request(data, self.api['forwardMessage'])

    def send_photo(self, chat_id, photo, caption='',
                   reply_to_message_id='', reply_markup=''):

        """
        Send photo by id (already uploaded to telegram) or as object of this type
        https://core.telegram.org/bots/api#inputfile

        APIdoc URL: https://core.telegram.org/bots/api#sendphoto

        :param chat_id: must
        :param photo: must
        :param caption: optional
        :param reply_to_message_id: optional
        :param reply_markup: optional
        :return:
        """

        data = {'chat_id': chat_id, 'photo': photo,
                'caption': caption, 'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup}

        return self.post_request(data, self.api['sendPhoto'])

    def send_audio(self, chat_id, audio, duration='',
                   performer='', title='', reply_to_message_id='',
                   reply_markup=''):

        """
        Send audio by id (already uploaded to telegram) or as object of this type
        https://core.telegram.org/bots/api#inputfile

        APIdoc URL: https://core.telegram.org/bots/api#sendaudio

        :param chat_id: must
        :param audio: must
        :param duration: optional
        :param performer: optional
        :param title: optional
        :param reply_to_message_id: optional
        :param reply_markup: optional
        :return: Message json object with sent message
        """

        data = {'chat_id': chat_id, 'audio': audio,
                'duration': duration, 'performer': performer,
                'title': title, 'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup}

        return self.post_request(data, self.api['sendAudio'])

    def send_document(self, chat_id, document, reply_to_message_id, reply_markup):
        """
        Send document by id (already uploaded to telegram) or as object of this type
        https://core.telegram.org/bots/api#inputfile

        APIdoc URL: https://core.telegram.org/bots/api#senddocument

        :param chat_id: must
        :param document: must
        :param reply_to_message_id: optional
        :param reply_markup: optional
        :return: Message json object with sent message
        """

        data = {'chat_id': chat_id, 'document': document,
                'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup}

        return self.post_request(data, self.api['sendDocument'])

    def send_sticker(self, chat_id, sticker, reply_to_message_id, reply_markup):
        """
        Send sticker by id (already uploaded to telegram) or as object of this type
        https://core.telegram.org/bots/api#inputfile

        APIdoc URL: https://core.telegram.org/bots/api#senddocument

        :param chat_id: must
        :param sticker: must
        :param reply_to_message_id: optional
        :param reply_markup: optional
        :return: Message json object with sent message
        """

        data = {'chat_id': chat_id, 'sticker': sticker,
                'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup}

        return self.post_request(data, self.api['sendSticker'])

    def send_video(self, chat_id, video, duration='',
                   caption='', reply_to_message_id='',
                   reply_markup=''):

        """
        Send video by id (already uploaded to telegram) or as object of this type
        https://core.telegram.org/bots/api#inputfile

        APIdoc URL: https://core.telegram.org/bots/api#sendvideo

        :param chat_id: must
        :param video: must
        :param duration: optional
        :param caption: optional
        :param reply_to_message_id: optional
        :param reply_markup: optional
        :return: Message json object with sent message
        """

        data = {'chat_id': chat_id, 'video': video,
                'duration': duration, 'caption': caption,
                'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup}

        return self.post_request(data, self.api['sendVideo'])

    def send_voice(self, chat_id, voice, duration='',
                   reply_to_message_id='', reply_markup=''):

        """
        Send voice by id (already uploaded to telegram) or as object of this type
        https://core.telegram.org/bots/api#inputfile

        APIdoc URL: https://core.telegram.org/bots/api#sendvoice

        :param chat_id: must
        :param voice: must
        :param duration: optional
        :param reply_to_message_id: optional
        :param reply_markup: optional
        :return: Message json object with sent message
        """

        data = {'chat_id': chat_id, 'voice': voice,
                'duration': duration, 'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup}

        return self.post_request(data, self.api['sendVoice'])

    def send_location(self, chat_id, latitude, longitude,
                      reply_to_message_id='', reply_markup=''):

        """
        Send latitude by id (already uploaded to telegram) or as object of this type
        https://core.telegram.org/bots/api#inputfile

        APIdoc URL: https://core.telegram.org/bots/api#sendlocation

        :param chat_id: must
        :param latitude: must
        :param longitude: must
        :param reply_to_message_id: optional
        :param reply_markup: optional
        :return: Message json object with sent message
        """

        data = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude,
                'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup}

        return self.post_request(data, self.api['sendLocation'])

    def send_chat_action(self, chat_id, action):

        """
        This method can tell bot what to do if he need some time to process request,
        for example to record and upload video

        :param chat_id:
        :param action: Types of action to broadcast:
                        @typing@ for text messages
                        @upload_photo@ for photos
                        @record_video@ or @upload_video@ for videos
                        @record_audio@ or @upload_audio@ for audio files
                        @upload_document@ for general files
                        @find_location@ for location data.
        :return: Message json object with sent message
        """

        data = {'chat_id': chat_id, 'action': action}
        return self.post_request(data, self.api['sendChatAction'])

    def get_updates(self, limit=1):

        """
        This method for receiving array of updates
        Link for description: https://core.telegram.org/bots/api#getupdates

        :parameter limit: sets maximum amount of messages to request. default = 1
        :return: An Array of Update json objects is returned https://core.telegram.org/bots/api#update
        """

        data = {'offset': self.offset + 1, 'limit': limit, 'timeout': 0}
        return self.post_request(data, self.api['getUpdates'])

    def get_file(self, file_id):

        """
        This method return a download link for a requested file by id

        :param file_id:
        :return: download link for requested file
        """

        data = {'file_id': file_id}
        message = self.post_request(data, self.api['getFile'])
        file_path = message['file_path']

        download_link = ('https://api.telegram.org/file/bot' + TOKEN + file_path)

        return download_link



    # def parse_update(self, message):
    #
    #     for update in message.json()['result']:
    #         self.offset = update['update_id']
    #         if not 'message' in update or not 'text' in update['message']:
    #             self.log_event('Unknown update' % update)
    #             continue
    #
    #         self.chat_id = update['message']['chat']['id']
    #         name = update['message']['chat']['first_name']
    #
    #         if self.chat_id != ADMIN_ID:
    #             self.send_text("You're not my Master!", self.chat_id)
    #             self.log_event('Unauthorized access attempt')
    #             continue
    #
    #         message = update['message']['text']
    #         parameters = (self.offset, name, self.chat_id, message)
    #         self.log_event('Message (id%s) from %s (id%s): "%s"' % parameters)
    #
    #         run_command(*parameters)

















class BotRoutines:

    def __init__(self):
#        self.text = ''
        self.caller_id = 1
        # self.URL_BASE = 'https://api.telegram.org/bot'
        # self.TOKEN = '152394201:AAE6wwKF-y9gddMrXUTAnGNbGrifJKFHU-I'
        # self.URL_TOKEN = URL_BASE + TOKEN

    @staticmethod
    def send_text(caller_id, text):
        BotRoutines.log_event('Sending text to %s: %s' % (caller_id, text))

        data = {'text': text, 'chat_id': caller_id}
        request = requests.post(URL_TOKEN + '/sendMessage', data=data)

        if not request.status_code == 200:
            return False
        return request.json()['ok']

    @staticmethod
    def client_secret():
        files = os.listdir('.')
        for secret_json in files:
            if fnmatch.fnmatch(secret_json, "client_secret*"):
                os.rename(secret_json, 'client_secret.json')
                break

    def get_text(chat_id):
        #log_event('Sending text to %s: %s' % (chat_id, text))

        data = {'chat_id': chat_id, 'text': text}
        request = requests.post(URL_TOKEN + '/getMessage', data=data)

        if not request.status_code == 200:
            return False
        return request.json()['message']