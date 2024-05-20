import base64
import requests


class RequestHandler:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    # Function used to retrieve a possible request from the server
    # it returns the string with the type of request or error in case of error during the request
    # possible strings:
    # NONE - there isn't any pending request for this device
    # UPDATE_MODEL - the server is sending a new model that the device must run
    # RETRIEVE_MODEL - the server is requesting to send the current updated model
    # RETRIEVE_DATA - the server is requesting to send the current updated data
    # error - some error occurred during the request
    def openCommunication(self):
        url = f'{self.url}/dev/openComm?deviceName={self.name}'
        response = requests.post(url)
        if response.status_code == 200:
            return response.content
        return "error"

    # Functon used to retrieve the model from the server. Is performed after the receiving of UPDATE_MODEL
    # it returns the model. In case of error, it returns the string 'error'
    def retrieveModel(self):
        url = f'{self.url}/dev/retrieveModel?deviceName={self.name}'
        response = requests.get(url)
        if response.status_code == 200:
            decoded = base64.b64decode(response.content).decode('utf-8')
            return decoded
        return "error"

    # Function used to send the model to the server. Is performed after the receiving of RETRIEVE_MODEL
    # it returns 'error' in case of error during the request, otherwise nothing
    def sendModel(self, modelName, model):
        url = f'{self.url}/dev/sendModel'
        encoded_model = base64.b64encode(model).decode('utf-8')
        body = {
            'modelName': modelName,
            'deviceName': self.name,
            'model': encoded_model
        }
        response = requests.post(url, json=body)
        if response.status_code != 200:
            return "error"

    # Function used to send the data to the server. Is performed after the receiving of RETRIEVE_DATA
    # it returns 'error' in case of error, otherwise nothing
    def sendData(self, data):
        url = f'{self.url}/dev/sendData'
        encoded_data = base64.b64encode(data).decode('utf-8')
        body = {
            'deviceName': self.name,
            'data': encoded_data
        }
        response = requests.post(url, json=body)
        if response.status_code != 200:
            return "error"
