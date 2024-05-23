
__app__ = "MQTT-Interface"
__version__ = "3.0"
__date__= "2021/04/25"


import os
import sys
import uuid
import time
import logging
import paho.mqtt.client as mqtt

class SingleTonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



#class mqttClient(metaclass=SingleTonMeta):
class mqttClient(object):
    def __init__(self,logger='logger'):

        _libName = str(__name__.rsplit('.', 1)[-1])
        self._log = logging.getLogger(logger + '.' + _libName + '.' + self.__class__.__name__)

        self._log.info('Start %s, %s' % (__app__, __version__))

        self._mqttc = None
        self._state = 'INIT'

        self._callbackOnConnect = None

    def __del__(self):
        self._log.info('Shutdown %s'%__app__)

    def will_set(self,topic,msg,retain=False,qos=0):
        self._mqttc.will_set(topic,msg,retain,qos)

    def callbackOnConnect(self,callback):
        self._callbackOnConnect = callback
        print(self._callbackOnConnect)

    def connect(self, host, port=1883, **options):
        self._log.debug('Connect with options(%s, %s, %s)' % (host, port, options))

        self._mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        self._mqttc.on_message = self.on_message
        if self._callbackOnConnect is not None:
            self._mqttc.on_connect = self._callbackOnConnect
        else:
            self._mqttc.on_connect = self.on_connect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe
        self._mqttc.on_disconnect = self.on_disconnect
        self._mqttc.on_log =  self.on_log()

        try:
            self._mqttc.connect(
            host = host,  # The only non-optional parameter
            port = port,
            keepalive=60,
            clean_start = mqtt.MQTT_CLEAN_START_FIRST_ONLY
        )
            self._mqttc.loop_start()
            self._log.info('Connected to mqtt with ClientID(%s)' % (host))
            self._state = 'CONNECTED'

        except OSError:
            self._log.error('Connect Failed')
            self._state = 'FAILD'
            return False

        return True

    def disconnect(self):
        self._log.info('Disconnected from MQTT')
        if self._state == 'CONNECTED':
            self._mqttc.disconnect()
        else:
            self._log.error('Not in connected state')

    def publish(self,topic,msg,retain=True,qos=1):
        self._mqttc.publish(topic,msg,retain,qos)


    def subscribe(self,topic,callback=None):
        if callback:
            print('add callback')
            self._mqttc.message_callback_add(topic,callback)

        (_result, _mid) = self._mqttc.subscribe(topic)


    def on_publish(self, client, userdata, mid, rc, properties):
        self._log.debug('Methode: on_publish(%s, %s, %s, %s, %s)' % (client, userdata, mid, rc, properties))
      #  self._state['PUBLISHED'] =mid
        return True

    def on_subscribe(self,mqttc,obj,mid,granted_qos,properties):
        print('Methode: on_subscribe(%s, %s, %s, %s)' % (mqttc, obj, mid, granted_qos))
        return True

    def on_message(self, client, userdata, message):
        self._log.debug('Methode: on_message(%s, %s, %s)' % (client, userdata, message))

        return message

    def on_connect(self,client, userdata, flags, rc, properties):
        self._log.debug('Methode: on_connect %s, %s, %s , %s' % (client, userdata, flags, rc))
        if rc == mqtt.CONNACK_ACCEPTED:
            self._log.debug('MQTT connected')
            self._state = 'CONNECTED'
        else:
            self._log.error('MQTT failed to connect: {}'.format(rc))
            self._state ='FAILED TO CONNECT'

    def on_disconnect(self,client, userdata, flags, rc, properties):
        self._log.debug('Methode: on_dissconnect(%s, %s, %s)' % (client, userdata, rc))
        if rc != 0:
            self._log.error('Unexpected disconnection.')
            self._state = 'DISCONNECTED'
        print('Dissconnect')
        return True

    def on_log(self):
        pass




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('mqttclient')

    mqttc1 = mqttClient('mqttClient')
    mqttc2 = mqttClient('mqtt')
    print(mqttc1,mqttc2)
    mqttc1.connect('192.168.2.20')
    x = 1
    while True:
        time.sleep(5)
       # sys.stdout.write('.')
        mqttc1.publish(topic='TEST001/TEST',msg=x,retain=True,qos=0)
        mqttc1.publish('TEST007/TEST',x, True, 1)
        x=x+1


