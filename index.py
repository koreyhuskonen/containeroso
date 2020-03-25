from flask import Flask, Response, request, jsonify
from containeroso import createNetwork, destroyNetwork, getSSHPort

app = Flask(__name__)

@app.route('/api/create-network', methods=['POST'])
def create_network():
    if not request.data:
        return flask.Response(status=500)

    payload = request.get_json()
    createNetwork(payload)

    return Response(status=200)

@app.route('/api/delete-network', methods=['DELETE'])
def destroy_network():
    if not request.data:
        return flask.Response(status=500)

    payload   = request.get_json()
    networkId = payload["networkId"]
    destroyNetwork(networkId)

    return Response(status=200)

@app.route('/api/get-port', methods=['POST'])
def get_port():
    if not request.data:
        return flask.Response(status=500)

    payload   = request.get_json()
    machineId = payload["machineId"]
    port      = getSSHPort(machineId)

    return jsonify(HostPort=port)

if __name__ == '__main__':
    app.run()
