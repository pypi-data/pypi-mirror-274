
import sys
import json
from juham.base.jbase import JBase

class JGroup(JBase):
    """Group base class, that can consists of JBase and JGroup objects as children.
    Can be used for grouping home automation objects to larger logical entities.
    """

    def __init__(self, name):
        super().__init__(name)
        self.children = []
        
    
    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.mqtt_client.connected_flag = True
            self.mqtt_client.subscribe('kerttula/control')
                
      
    def on_message(self, client, userdata, msg):
        super().on_message(client, userdata, msg)
        m = json.loads(msg.payload.decode())
        self.warning(f"Message {str(m)} not handled")

    
    def run(self):
        self.info("Starting up mqtt clients...")
        for h in self.children:
            h.run()
        self.info('Starting up control client, press CTRL+C to exit...')
        self.mqtt_client.loop_forever()

    
    def add(self, h):
        self.children.append(h)

