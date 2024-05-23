
import os
import time
import datetime
import uuid
import socket
import logging
from pyHomie import node


#from node import node



class device(object):

    def __init__(self,id,mqttObj,topic='homie',homie='4.0.0',name='',state='init',logger='logger'):

        _libName = str(__name__.rsplit('.', 1)[-1])
        self._log = logging.getLogger(logger + '.' + _libName + '.' + self.__class__.__name__)

        self.deviceId = id
        self.mqttObj = mqttObj
        self.baseTopic = topic

        self.homieVersion = homie
        self.name = name
        self.state = 'init'

        self.nodesRegister = {}
        self.extendsions = ['stats','firmware']
        self.implementation = os.name

        self._fw_name = "python-homie"
        self._fw_version =  '0.0.2'

        self.interval = 60

        self._log.info('Create Device Objact ID: %s'%(self.deviceId))

    def __del__(self):
        self._log.debug('Delete device %s'%(self.deviceId))


   # @property
   # def node(self):
    #    return self.__dict__

    #@node.setter
    def node(self,value):
        self.__dict__[value] = node('name')
        return True

    def setState(self,state):
        self._log.info('The Homie $state device attribute changed from %s to %s' % (self.state, state))
        self.state = state
       # print('publish state',self.topic,self.state)
        self.mqttObj.publish("/".join((self.topic,"$state")), self.state, retain=True, qos=1)
        return True

    def registerNode(self,id,nodeObj):
        self._log.info('NodeID %s registered as device %s'%(id,self.deviceId))
      #  print('regisertNode',id)
        setattr(self,id,nodeObj)
    #    self.nodesRegister[id] = nodeObj
      #  print(self.__dict__)
        return True

    def init(self):
        #self.mqttObj = mqttObj
        self._log.info('Start initalisation of device ID: %s'% self.deviceId)
        self.topic = "/".join((self.baseTopic, self.deviceId))
        self.start_time = time.time()

        #set last will
        self.mqttObj.will_set("/".join((self.topic,"$state")),'lost',retain=True)
        self.publish()
        self.publish_extensions()
        self._log.info('Completed initialisation of device ID: %s'% self.deviceId)
      #  print('init device completed')

        for id, instance in self.__dict__.items():
       #     print('init node', id, instance, isinstance(instance, node.node))
            if isinstance(instance, node.node):
              #  print('init Node', id, instance)
                instance.init(self.mqttObj,self.topic)
     #   for nodeName, nodeObj in self.nodesRegister.items():
      #      nodeObj.init(self.mqttObj,self.topic)

    def publish(self):
        self.mqttObj.publish("/".join((self.topic,"$homie")),self.homieVersion,retain=True,qos=1)
        self.mqttObj.publish("/".join((self.topic,"$name")), self.name, retain=True, qos=1)
        self.mqttObj.publish("/".join((self.topic,"$state")), self.state, retain=True, qos=1)
        self.mqttObj.publish("/".join((self.topic, "$implementation")), os.name, retain=True, qos=1)
        nodes=[]
        for id, instance in self.__dict__.items():
            if isinstance(instance, node.node):
                nodes.append(instance.id)
        self.mqttObj.publish("/".join((self.topic, "$nodes")),",".join(nodes),retain=True,qos=1)

    # self.mqttObj.publish("/".join((self.topic, "$nodes")), ",".join([node.id for node in self.nodesRegister.values()]))


    def publish_extensions(self):
        # extensions = ",".join(EXTENSIONS)

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac_address = ':'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        # print(extensions)

        self.mqttObj.publish("/".join((self.topic, "$extensions")), ",".join(([item for item in self.extendsions])))

        if "firmware" in self.extendsions:
            # self.mqttc.publish_firmware(retain, qos)
            self.mqttObj.publish("/".join((self.topic, "$localip")), ip_address)
            self.mqttObj.publish("/".join((self.topic, "$mac")),mac_address)
            self.mqttObj.publish("/".join((self.topic, "$fw/name")), self._fw_name)
            self.mqttObj.publish("/".join((self.topic, "$fw/version")), self._fw_version)
          #  self.mqttObj.publish("/".join((self.topic, "$implementation")), self._implementation)

        if "stats" in self.extendsions:
            self.mqttObj.publish("/".join((self.topic, "$stats/interval")), self.interval)
            self.mqttObj.publish("/".join((self.topic, "$stats/uptime")), time.time() - self.start_time)
            self.mqttObj.publish("/".join((self.topic, "$stats/lastupdate")),datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    def updateStats(self):
        self.mqttObj.publish("/".join((self.topic, "$stats/uptime")), time.time() - self.start_time)
        self.mqttObj.publish("/".join((self.topic, "$stats/lastupdate")),datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))