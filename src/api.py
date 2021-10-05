from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config["DEBUG"] = True

location_count = 0
fault_count = 0


def get_mock_data():

    with open(os.path.join(os.getcwd(), "src", "db.json")) as file:
        mock_data = json.load(file)

    return mock_data


@app.route('/Get/DeviceStatusInfo', methods=['POST'])
def get_device_status_info():
    request_obj = request.json
    parsed_data = get_mock_data()['deviceStatusInfo']
    data = next((obj for obj in parsed_data
                 if obj['vehicleID'] == request_obj["vehicleId"]), None)
    global location_count
    location_count = location_count + 1
    return jsonify(data["coordinates"][location_count])


@app.route('/GetFeed/FaultData', methods=['GET'])
def get_vehicle_fault_data():
    global fault_count
    fault_count = fault_count + 1
    if fault_count is 4:
        return "Faulted Vehicle"
    return "Ok"


@app.route('/GetFeed/StatusData', methods=['POST'])
def get_vehicle_status_data():
    request_obj = request.json
    parsed_data = get_mock_data()['vehicleStatusData']
    data = list(filter(lambda obj: ((obj['dateTime'] >= request_obj["fromDate"]) and
                                    (obj['dateTime'] <= datetime.now().isoformat()[:-3] + "Z")),
                       parsed_data))

    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
