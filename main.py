from websocket_server import WebsocketServer
import json
import time

# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])

def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])

# Called when a client sends a message
def message_received(client, server, message):
    def handleCreateGame(client, server, message):
        server.send_message_to_all(json.dumps({"action": "createGameResult",
                                               "data": {"battleId": message["requestId"], "gameStarted": True}}))

        time.sleep(5)
        response = {
            "battleId": message["battleId"],
            "replayId": 123456,
            "playerResults": [{"playerFafId": message["participants"][0], "result":"victory"}] +
                [{"playerFafId": id, "result": "death", "killedBy": message["participants"][0]}
                    for id in message["participants"][1:]]
        }
        # response["requestId"] = message["requestId"]

        response_json = json.dumps({"action": "gameResult", "data": response})

        print("Client(%d) message response: %s" % (client["id"], response_json))
        server.send_message_to_all(response_json)

    print("Client(%d) message received: %s" % (client['id'], message))
    request = json.loads(message)

    if request["action"] == "createGame":
        handleCreateGame(client, server, request["data"])
    else:
        print("unknown message")




PORT = 9001
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
