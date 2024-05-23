
__app__ = "pyHomnie"
__version__ = "0.0.3"
__date__= "2024/05/15"

import re
import yaml

import logging
from pyHomie import properties, device, node, mqttClient, watchdog


class pyHomie(object):
    def __init__(self,logger='pyHomie')-> None:

        _libName = str(__name__.rsplit('.', 1)[-1])
        self._logHandler = logger + '.' + _libName
        self._log = logging.getLogger(self._logHandler + '.' + self.__class__.__name__)

        self._log.info('Start %s, %s' % (__app__, __version__))

        self.mqttClient = mqttClient.mqttClient(logger)

    def __del__(self):
        for id,instance in self.__dict__.items():
            if isinstance(instance, device.device):
                instance.setState('disconnected')

        self._log.info('Shutdown %s'%__app__)
        self.mqttClient.disconnect()


    def init(self,configfile='config.yaml'):
        with open(configfile, 'r') as f:
            config = yaml.safe_load(f)
            self._log.debug('Startup of Homie with config: %s'% config)

        mqttConfig = config.get('mqtt',None)
        homieConfig = config.get('homie',None)

        if mqttConfig is not None:
            self.initMqtt(mqttConfig)
        else:
            return False

        if homieConfig is not None:
            self.initHomie(homieConfig)
            self.startHomie()
        else:
            return False

        return True


    def initMqtt(self,config):
        if not self.mqttClient.connect(config.get('host','192.168.2.20')):
            self._log.critical('MQTT cannot be started')
            exit(-1)

    def initHomie(self,config):
        self._log.debug('Start pyHomie with configuration %s'% config)

        for deviceId, deviceValue in config.items():
            if not self._validateId(deviceId):
                self._log.critical('Validation of device ID failed: %s' % deviceId)
                return False

            deviceObj = device.device(id=deviceId, mqttObj=self.mqttClient, topic=deviceValue.get('topic', 'homie'), homie=deviceValue.get('homie', '4.0'), name=deviceValue.get('name', None), state=deviceValue.get('state', 'init'), logger=self._logHandler)
            setattr(self,deviceId,deviceObj)
           # self.deviceRegister.append(deviceObj)

            for nodeId,nodeValue in deviceValue.items():
                if isinstance(nodeValue, dict):
                    if not self._validateId(nodeId):
                        self._log.critical('Validation of node ID failed: %s'%nodeId)
                        return False

                    nodeObj = node.node(id=nodeId, device=deviceObj, name=nodeValue.get('name', ''), type=nodeValue.get('type', ''), logger=self._logHandler)
                    setattr(self,nodeId, nodeObj)
                   # print(nodeId,nodeObj)
                    deviceObj.registerNode(nodeId,nodeObj)
                #    self.nodeRegister.append(nodeObj)
                 #   print(self.__dict__)
                    for propertyId,propertyValue in nodeValue.items():
                        if isinstance(propertyValue,dict):
                            if not self._validateId(propertyId):
                                self._log.critical('Validation of property ID failed: %s' % propertyId)
                                return False
                 #           print(propertyId,propertyValue)
                           # module = importlib.import_module('pyHomie.api.properties#')
                           # print(module)
                            _type = getattr(properties, propertyValue.get('type', 'switch'))
                            #print('Type',propertyValue,_type)
                            self._log.debug('Get property type %s of propertyID %s'%(_type,propertyId))
                            #type=propertyValue.get('type','Switch')
                          #  propertyObj = _type(id=propertyId,node=nodeObj,name=propertyValue.get('name',''),settable=propertyValue.get('settable',False))
                            propertyObj = _type(propertyId, nodeObj, logger=self._logHandler, **propertyValue)
                            setattr(self,propertyId, propertyObj)
                            nodeObj.registerProperty(propertyId,propertyObj)

       # print(self.__dict__)

    def startHomie(self):
        print('run')
       # if isinstance(value,device) in self.__dict__.va
        for id,instance in self.__dict__.items():
            #print(_instance_object,isinstance(_object,device))
            if isinstance(instance, device.device):
               # print('True',device)
                instance.init()

    def start(self):
       # self.deviceRegister[0].init()
        self._updateTimer= watchdog.watchdog(60, self.statesUpdate)
        self._updateTimer.start()
        self._timeoutTimer= watchdog.watchdog(120, self.watchdogTimeout)
        self._timeoutTimer.start()

        for id, instance in self.__dict__.items():
            if isinstance(instance, device.device):
                instance.setState('ready')
    def stop(self):
        self._updateTimer.cancel()
        self._timeoutTimer.cancel()

        for id, instance in self.__dict__.items():
            if isinstance(instance, device.device):
                instance.setState('disconnected')

    def statesUpdate(self,value):
        self._log.debug('Homie $state update')
        for _instance,_object in self.__dict__.items():
            if isinstance(_instance, device.device):
               # print('True',key,value)
                _object.updateStates(value)
        #self.deviceRegister[0].updateStates(value)
        self._updateTimer.restart()

    def watchdogTimeout(self,value):
        if 'TIMEOUT' in value:
            self._log.critical('Watchdog timeout, set Homie $state to lost')
            for _instance, _object in self.__dict__.items():
                if isinstance(_instance, device.device):
                    # print('True',key,value)
                    _object.setState('lost')
           # self.deviceRegister[0].setState('lost')
        else:
            self._timeoutTimer.restart()

        return True

    def updateWatchdog(self) -> None:
        self._log.debug('Watchdog reset')
        self._timeoutTimer.restart()

    def getDevices(self) -> list:
        deviceList = []
        for id,instance in self.__dict__.items():
            if isinstance(instance, device.device):
                deviceList.append(id)
        return deviceList

    def getNodes(self) -> list:
        _list = []
        for id, instance in self.__dict__.items():
            if isinstance(instance, node.node):
                _list.append(id)
        return _list

    def getProperties(self) -> list:
        _list = []
        for id, instance in self.__dict__.items():
            if isinstance(instance, properties.propertyBase):
                _list.append(id)
        return _list

    def _validateId(self,id):
        if isinstance(id, str):
            r = re.compile("(^(?!\\-)[a-z0-9\\-]+(?<!\\-)$)")
            if r.match(id):
                if id in self.__dict__:
                    self._log.critical('Validation of ID failed: Duplicate ID: %s' % id)
                else:
                    self._log.debug('Validation of ID %s succeeded' % id)
                    return True
            else:
                self._log.critical('Validation of ID failed: Invalid ID %s provided'% id)
                return False



