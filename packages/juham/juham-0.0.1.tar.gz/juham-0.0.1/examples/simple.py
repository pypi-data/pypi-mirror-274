
"""!@mainpage

<h2>Simple</h2>

<p>
Minimal example application built on top of <b>Juham</b> - Juha's Ultimate Home Automation Masterpiece (or Mess, for now)
</p>

<p>
Requires paho Mosquitto MQTT 
</p>

<p>
This header is in 'Doxygen' format (should perhaps be replaced with some native Python tool)
</p>


"""

from juham.base.jbase import JBase
from juham.base.jgroup import JGroup
from juham.app.japp import JApp
from juham.base.jobject import JObject
from juham.database.jconsole import JConsole
from juham.pubsub.jpaho2 import JPaho2

def main():

    # Use 'JConsole' as replacement for time series database, for minimal dependencies
    JBase.database_class_id = JConsole.get_class_id()
    # You want to create Influx account (v3) and replace JConsole with JInflux
    # JBase.database_class_id = JInflux.get_class_id()
    # JInflux.token = 'your token'
    # JInflux.org = 'your organization'
    # JInflux.host = 'Url to your influx site'
    # JInflux.database='database name'
    # JBase.database_class_id = JInflux.get_class_id()
    
    # Configure mqtt network 
    JPaho2.host = 'localhost'
    JPaho2.port = 1883
    JBase.pubsub_class_id = JPaho2.get_class_id()

    simple = JApp('simple')
    
    # start 
    simple.run()
    
    
if __name__ == "__main__":
    main()


