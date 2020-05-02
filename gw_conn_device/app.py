from flask import Flask, jsonify, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "welcome ECC"

@app.route('/peakvalue', methods = ['POST'])
def peakValue():
    if request.method == "POST":
        try:
            strMessag = request.data
            strMessage = strMessag.decode('utf-8')
            dictMessage = literal_eval(strMessage)
            
            targetPower = int(dictMessage['peakvalue'])

            _LOGGER.debug("Change targetPower Value: %s", targetPower)

            result = data_model.assemble_data(targetPower)

            for i in range(SAMIN747_RETRY_COUNT):
                data_model.sendMsg(result)
                dictDeviceStatus = data_model.receiveMsg()

                if int(dictDeviceStatus["targetPower"]) == targetPower :
                    print("Control Success")
                    history_db.setControlHistory("auto", targetPower, "ai", CONTROL_SUCCESS_CODE)
                    
                    _LOGGER.debug("Success Change targetPower: %s", targetPower)

                    return "success"
                else:
                    _LOGGER.error("Fail Change targetPower: %s", targetPower)
                    print("Control Fail")
                    
            history_db.setControlHistory("auto", targetPower, "ai", CONTROL_FAIL_CODE)
            
        except Exception as e :
            print(e)
            return "fail"

@app.route('/dc_check', methods = ['GET'])
def dcCheck():
    if request.method == "GET":
        dictDeviceStatus = data_model.receiveMsg()
        
        _LOGGER.debug("receive status of device: %s", dictDeviceStatus)

        if dictDeviceStatus != None:
            try:
                history_db.setDeviceHistory(dictDeviceStatus['targetPower'], dictDeviceStatus['predictPower'], dictDeviceStatus['currentPower'])
                res = requests.post('http://localhost:9090/dc_status', data = dictDeviceStatus)

                _LOGGER.debug("Send status of device to broker")

            except Exception as e:
                _LOGGER.errer(e)
                return "fail"

            return "success"

        else:
            _LOGGER.error("Fail reading status of device")
            return "fail"

app.run(host="localhost", port="8080")