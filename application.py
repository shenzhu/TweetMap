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
        # Run local elasticsearch
        #query = {"query": {"match_all": {}}}
        #results = es.search(index = 'twitter', doc_type = 'tweet', size = 1000, body = query)
        queryURL = 'Type Your AWS Elasticsearch Endpoint'
        #queryURL = 'http://localhost:9201/twitter/_search?q=*:*&size=1000'
        response = requests.get(queryURL)
        results = json.loads(response.text)

        # # Run using aws elasticsearch
        # queryURL = 'http://search-twettermap-bykoa2l2xfb6sbkpjrcripyaaa.us-west-2.es.amazonaws.com/tweetmap/_search?q=*:*&size=1000'
        # response = requests.get(queryURL)
        # print("QUERY EXECUTED AGAIN")
        # print response.text
        # results = json.loads(response)
        print("INIT MAP")
    else:
        #print message
        #results = es.search(index = 'twitter',size = 1000, q = message)

        #print message
        queryKeyWord = message.replace(' ', '%20')
        queryURL = 'Type Your AWS Elasticsearch Endpoint'
        #print queryURL
        response = requests.get(queryURL)
        results = json.loads(response.text)
        print("SEARCH" + str(message))
    
    #print("Executed")

    # Find locations of each tweet
    locations = {}
    locations['locaiton'] = []
    for result in results['hits']['hits']:
        locations['locaiton'].append(result['_source']['location'])
        #print result['_source']['location']
    locationsJSON = json.dumps(locations)
    # print(locationsJSON)
    # send(locationsJSON)
    
    send(json.dumps(locations))


if __name__ == '__main__':

    # Before flask starts, start the elasticsearch service at localhost:9201
    #es = Elasticsearch([{'host': 'localhost', 'port': 9201}])

    socketio.run(application, debug=True)
