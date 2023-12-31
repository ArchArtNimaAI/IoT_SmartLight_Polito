import cherrypy
import os
from LedManager import *
import json


class LightREST(object):
    exposed = True

    def __init__(self):
        conf = json.load(open("settings.json"))
        broker = conf["broker"]
        port = conf["port"]
        self.led_client = LedManager("LedCommander", "IoT/Orlando/led", broker, port)
        self.led_client.start()

    def GET(self):
        return open('index.html')

    def PUT(self, *uri):
        command = uri[0]
        self.led_client.publish(command)


if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.session.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        # You need to include the part below if you want to activate the css and gice to the button a nicer look
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './css'
        }
    }
    cherrypy.tree.mount(LightREST(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()