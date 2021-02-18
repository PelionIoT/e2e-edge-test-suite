# pylint: disable=bad-continuation
"""
WebSocket notification channel related helpers.
"""

import base64
import datetime
import json
import logging
import queue
import threading
from time import sleep

from ws4py.client.threadedclient import WebSocketClient
from ws4py.exc import WebSocketException

from pelion_systest_lib.tools import build_random_string

log = logging.getLogger(__name__)


class WebsSocketNotificationChannel:

    def __init__(self, cloud_api, api_key, configuration=None):
        log.info('Register and open WebSocket notification channel')
        self.api_key = api_key
        self.cloud_api = cloud_api
        cloud_api.connect.register_websocket_channel(api_key,
                                                     configuration=configuration,
                                                     expected_status_code=[200, 201])
        # IOTNS-205
        sleep(5)
        # Get host part from api address
        host = cloud_api.rest_api.api_gw.split('//')[1]

        log.info('Opening WebSocket handler')
        self.ws = WebSocketRunner('wss://{}/v2/notification/websocket-connect'.format(host),
                                  api_key)
        self.handler = WebSocketHandler(self.ws)

    def close(self):
        try:
            self.ws.close()
        except BaseException as e:
            log.warning('Websocket closing error: {}'.format(e))
        sleep(2)
        log.info('Deleting WebSocket channel')
        self.cloud_api.connect.delete_websocket_channel(self.api_key, expected_status_code=204)


class WebSocketHandler:
    """
    Class to handle messages via WebSocket callback
    :param ws: WebSocket Runner class
    """

    def __init__(self, ws):
        self.ws = ws

    @property
    def api_key(self):
        """
        Make able to use exactly right apikey in other places
        :return: api key
        """
        return self.ws.api_key

    def check_registration(self, device_id):
        """
        Check if WebSocket has registration message(s)

        :param device_id: string
        :return:
        """
        for item in self.ws.events['registrations']:
            # If asked device_id is found return its data. Otherwise return False
            if item['ep'] == device_id:
                return item
        return False

    def check_deregistration(self, device_id):
        """
        Check if WebSocket has de-registration message(s) for given device id

        :param device_id: string
        :return:
        """
        for item in self.ws.events['de-registrations']:
            # If asked device_id is found return its data. Otherwise return False
            if item['ep'] == device_id:
                return item
        return False

    def check_registration_updates(self, device_id):
        """
        Check if WebSocket has registration updates message(s) for given device id

        :param device_id: string
        :return: False / dict
        """
        for item in self.ws.events['reg-updates']:
            # If asked device_id is found return its data. Otherwise return False
            if item['ep'] == device_id:
                return item
        return False

    def check_registration_expiration(self, device_id):
        """
        Check if CALLBACK-HANDLER has registrations expired message(s) for given device id

        :param device_id: string
        :return: False / dict
        """
        for item in self.ws.events['registrations-expired']:
            # If asked device_id is found return its data. Otherwise return False
            if item['ep'] == device_id:
                return item
        return False

    def get_notifications(self):
        """
        Get all notifications from WebSocket data

        :return: dict
        """
        return self.ws.events['notifications']

    def get_async_response(self, async_response_id):
        """
        Get async-response from WebSocket data for given async_id

        :param async_response_id: string
        :return: dict
        """
        return self.ws.async_responses.get(async_response_id)

    def wait_for_multiple_notification(self, device_id, expected_notifications, timeout=30, assert_errors=False):
        """
        Wait for given device id + resource path(s) + expected value(s) to appear in CALLBACK-HANDLER

        :param device_id: string
        :param expected_notifications: list of dicts of resource paths with expected values
                                        [{'resource_path': 'expected_value'},
                                        {'resource_path_2}: {'excepted_value_2},
                                        ...
                                        ]
        :param timeout: int
        :param assert_errors: boolean for user if to fail test case in case of expected notifications not received
        :return: False / list of received notifications or fail the test case if confirm_resp=True
        """
        item_list = []
        for _ in range(timeout):
            notifications = self.get_notifications()
            for item in notifications:
                if item['ep'] == device_id:
                    # Check if received notification contains any combinations defined in expected_notifications.
                    # If found, append item to item_list. If as many items are found as are expected, return list.
                    if [expect_item for expect_item in expected_notifications if
                        item['path'] in expect_item.keys() and base64.b64decode(
                            item['payload']).decode('utf8') in expect_item.values()]:
                        item_list.append(item)
                        if len(item_list) == len(expected_notifications):
                            return item_list
            sleep(1)
        log.debug('Expected {}, found only {}!'.format(expected_notifications, item_list))
        if assert_errors:
            assert False, 'Failed to receive all expected notifications from device on websocket channel by ' \
                          'timeout:{} seconds'.format(timeout)
        return False

    def wait_for_notification(self, device_id, resource_path, expected_value, timeout=30, assert_errors=False, delay=1):
        """
        Wait for given device id + resource path + expected value to appear in WebSocket

        :param device_id: string
        :param resource_path: string
        :param expected_value: string
        :param timeout: int
        :param assert_errors: boolean for user if to fail test case in case of expected notification not received
        :param delay: Delay to check notification
        :return: dict or fail the test case if confirm_resp=True
        """
        wait = 0
        expected_value = str(expected_value)
        while wait <= timeout:
            for item in self.ws.events['notifications']:
                if item['ep'] == device_id and item['path'] == resource_path and \
                        base64.b64decode(item['payload']).decode('utf8') == expected_value:
                    return item
            sleep(delay)
            wait += delay
        if assert_errors:
            assert False, 'Failed to receive notification from device on websocket channel by timeout: {}'.format(
                timeout)
        return False

    def wait_for_async_response(self, async_response_id, timeout=30, assert_errors=False):
        """
        Wait for given async-response to appear in WebSocket data

        :param async_response_id: string
        :param timeout: int
        :param assert_errors: boolean for user if to fail test case in case of expected response not received
        :return: dict or fail the test case if confirm_resp=True
        """
        for _ in range(timeout):
            async_response = self.ws.async_responses.get(async_response_id)
            if async_response:
                return async_response
            sleep(1)
        if assert_errors:
            assert False, 'Failed to receive async response from device with async_id:{} on websocket channel by ' \
                          'timeout:{} seconds'.format(async_response_id, timeout)
        return False

    def wait_for_registration(self, device_id, timeout=30):
        """
        Wait for given device id registration to appear in WebSocket

        :param device_id: string
        :param timeout: int
        :return: False / dict
        """
        for _ in range(timeout):
            registration = self.check_registration(device_id)
            if registration:
                return registration
            sleep(1)
        return False

    def wait_for_registration_updates(self, device_id, timeout=30):
        """
        Wait for given device id registration update notification to appear in WebSocket

        :param device_id: string
        :param timeout: int
        :return: False / dict
        """
        for _ in range(timeout):
            registration = self.check_registration_updates(device_id)
            if registration:
                return registration
            sleep(1)
        return False

    def wait_for_registration_expiration(self, device_id, timeout=30):
        """
        Wait for given device id registration expiration notification to appear in WebSocket

        :param device_id: string
        :param timeout: int
        :return: False / dict
        """
        for _ in range(timeout):
            registration = self.check_registration_expiration(device_id)
            if registration:
                return registration
            sleep(1)
        return False

    def wait_for_deregistration(self, device_id, timeout=30):
        """
        Wait for given device id de-registration to appear in WebSocket

        :param device_id: string
        :param timeout: int
        :return: False / dict
        """
        for _ in range(timeout):
            deregistration = self.check_deregistration(device_id)
            if deregistration:
                return deregistration
            sleep(1)
        return False


class WebSocketRunner:
    """
    Class for handling WebSocket connection and storing data from notification service
    :param api: string URL for WebSocket connection endpoint
    :param api_key: string
    """

    def __init__(self, api, api_key):
        self.async_responses = {}
        self.events = {'registrations': [], 'notifications': [], 'reg-updates': [], 'de-registrations': [],
                       'registrations-expired': []}
        self.run = False
        self.exit = False
        self.ws = None
        self.message_queue = queue.Queue()
        self.ret_code = []
        self._api_url = api
        self._api_key = api_key

        self.open()

    @property
    def api_key(self):
        """
        Make able to use exactly right apikey in other places
        :return: api key
        """
        return self._api_key

    def _input_thread(self, api, api_key):
        """
        Runner's input thread
        :param api: Api
        :param api_key: Api key
        """
        while self.run:
            try:
                self.ws = CallbackClient(self.message_queue, api, protocols=['wss', 'pelion_{}'.format(api_key)])
                log.debug('Connecting WebSocket')
                self.ws.connect()
                log.debug('Run forever WebSocket handler')
                self.ws.run_forever()
                if self.exit:
                    self.ret_code = self.ws.ret_code
                    log.info('WebSocket handler exited with return code {} and size  {}'.format(self.ret_code,
                                                                                                len(self.ret_code)))
                else:
                    self.ret_code = self.ws.ret_code
                    log.error('WebSocket handler exited  return code {} and size  {}'.format(self.ret_code,
                                                                                             len(self.ret_code)))
            except (WebSocketException, RuntimeError) as e:
                if 'Unauthorized' in e:
                    log.error('Failed to connect WebSocket! {}'.format(e))
                    sleep(1)
                    self.run = False
                log.warning('WebSocket failed, retrying! {}'.format(e))
                sleep(1)
            sleep(1)
        log.info('WebSocket input thread was stopped.')

    def _handle_thread(self):
        """
        Runner's handle thread
        """
        while self.run:
            data = self.message_queue.get()
            if data == {}:
                log.info('Received callback is empty')
            for notification_type, notification_value in data.items():
                log.debug('Callback contains %s', notification_type)
                self._handle_content(notification_type, notification_value)

    def open(self):
        """
        Open WebSocket threads
        """
        if self.run:
            log.warning('WebSocket threads are already running!')
            return

        log.info('Starting WebSocket threads')
        self.exit = False
        self.run = True
        _it = threading.Thread(target=self._input_thread, args=(self._api_url, self._api_key),
                               name='websocket_{}'.format(build_random_string(3)))
        _ht = threading.Thread(target=self._handle_thread, name='messages_{}'.format(build_random_string(3)))
        _it.setDaemon(True)
        _ht.setDaemon(True)
        _it.start()
        _ht.start()

    def close(self):
        """
        Close WebSocket threads
        """
        log.info('Closing WebSocket threads')
        self.exit = True
        self.run = False
        try:
            self.ws.close()
        except (WebSocketException, RuntimeError) as e:
            log.warning('WebSocket close failed! {}'.format(e))

    def _handle_content(self, notification_type, data):
        """
        Handle received content
        :param notification_type: Notification type
        :param data: Content data
        """
        for content in data:
            date_now = datetime.datetime.utcnow().isoformat('T') + 'Z'
            # De-registrations is plain list, need to convert it to dict. Otherwise just add timestamp
            if notification_type in ('de-registrations', 'registrations-expired'):
                content = {'dt': date_now, 'ep': content}
            else:
                content['dt'] = date_now
            # Async-responses are saved by response, others are pushed to list
            if notification_type == 'async-responses':
                self.async_responses[content['id']] = content
            else:
                self.events[notification_type].append(content)


class CallbackClient(WebSocketClient):
    """
    WebSocket callback client class
    """

    def __init__(self, message_queue, api, protocols):
        super().__init__(api, protocols=protocols)
        self.message_queue = message_queue
        self.api = api
        self.ret_code = []

    def opened(self):
        """
        WebSocket opened logging
        """
        log.info('WebSocket opened to {}'.format(self.api))

    def closed(self, code, reason=None):
        """
        WebSocket closed logging
        """
        self.ret_code.append(code)
        log.info('WebSocket closed with code {} reason {}'.format(code, reason))

    def received_message(self, message):
        """
        WebSocket message received
        """
        log.debug('WebSocket Received: {}'.format(message))
        self.message_queue.put(json.loads(str(message)))
