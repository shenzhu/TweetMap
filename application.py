from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import json
import requests

application = Flask(__name__)

socketio = SocketIO(application)

@application.route('/')
def hello_world():
    return render_template('TwitterMap.html')


@socketio.on('message')
def handleConnected(message):
    
    if message == 'Init':
        # Run using aws elastic search
        queryURL = 'Type Your AWS Elasticsearch Endpoint'
        response = requests.get(queryURL)
        results = json.loads(response.text)

        print("INIT MAP")
    else:

        queryKeyWord = message.replace(' ', '%20')
        queryURL = 'Type Your AWS Elasticsearch Endpoint'
        #print queryURL
        response = requests.get(queryURL)
        results = json.loads(response.text)
        print("SEARCH" + str(message))
    

    # Find locations of each tweet
    locations = {}
    locations['locaiton'] = []
    for result in results['hits']['hits']:
        locations['locaiton'].append(result['_source']['location'])
        #print result['_source']['location']
    locationsJSON = json.dumps(locations)

    
    send(json.dumps(locations))


if __name__ == '__main__':
    socketio.run(application, debug=True)
