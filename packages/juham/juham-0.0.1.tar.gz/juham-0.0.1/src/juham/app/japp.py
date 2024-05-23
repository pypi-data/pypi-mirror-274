from juham.base.jbase import JBase
from juham.base.jgroup import JGroup
from juham.ts.jlog import JLog
from juham.base.jobject import JObject
from juham.database.jinflux import JInflux
from juham.pubsub.jpaho2 import JPaho2

class JApp(JGroup):
    """Default application class. Configures JBase class with JPaho2 MQTT and JInflux time series database.
    It is up to the sub classes to initialize appropriate JInflux toke, org, host and database attributes
    to match the Influx account in question.
    """

    def __init__(self, name):
        super().__init__(name)
        print('instantiating japp')
        self.children = []
        self.add(JLog()) # to write log events to time series database
        
    @classmethod
    def register(cls):
        JGroup.register()
        # Influx v3
        JBase.database_class_id = JInflux.get_class_id()
        JInflux.token = None
        JInflux.org = None
        JInflux.host = None
        JInflux.database=None
        # Configure mqtt network
        JPaho2.host = 'localhost'
        JPaho2.port = 1883
        JBase.pubsub_class_id = JPaho2.get_class_id()


