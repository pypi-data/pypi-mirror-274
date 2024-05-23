
from juham.base.jbase import JBase
from juham.database.jconsole import JConsole
from juham.pubsub.jpaho2 import JPaho2
from influxdb_client_3 import Point
import json

class JLog(JBase):
    """Time series class for log events. 
    Records all log events to 'log' time series database.
    """

    classId = 'JLog'
    
    def __init__(self, name='jlog'):
        super().__init__(name)

    
    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe('kukkila/log')

            
    def on_message(self, client, userdata, msg):
        m = json.loads(msg.payload.decode())
        point = (
            Point("log") 
            .tag("class", m['Class'])
            .field('source', m['Source']) 
            .field('msg', m['Msg'])
            .field('details', m['Details'])
            .field('Timestamp', m['Timestamp'])
            .time(self.epoc2utc(m['Timestamp']))
        )
        self.write(point)
                    
    @classmethod
    def register(cls):
        JBase.register();
        JBase.registerClass(cls.classId, cls)


def main():
    JBase.database_class_id = JConsole.get_class_id()
    JPaho2.host = 'localhost'
    JPaho2.port = 1883
    JBase.pubsub_class_id = JPaho2.get_class_id()

    JLog().run_forever()


if __name__ == "__main__":
    main()
    
