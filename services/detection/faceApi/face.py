import requests
import json as json

url = "https://brazilsouth.api.cognitive.microsoft.com/face/v1.0/"
api_key = "73e4782c3e3e4b46a727bf498e8241b8"
# FaceAttributes=age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup


class Face(object):
    """An object used to request for Azure Face Api:

    Attributes:
        byte_image: Byte format image
        azureFaceId: Face Id in azure plataform of the biggest face
    """

    def __init__(self, img):
        """Return a Face for using Azure Face Api:
        """
        self.byte_image = img
        self.azureFaceId = self.detect()

    def detect(self):
        """ Execute de API: https://brazilsouth.api.cognitive.microsoft.com/face/v1.0/detect
            Set the faceId returned from Detect API
        """
        data = self.byte_image.read()

        res = requests.post(url = url + 'detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,gender,headPose,smile,emotion,noise',
                    data = data,
                    headers = {'Content-Type': 'application/octet-stream', 'Ocp-Apim-Subscription-Key':api_key})
        # Json decoding
        obj = json.loads(res.text)
        self.response = res.text
        print (str(self.response))

        return obj[0]['faceId']

    def verify(self, anotherId):
        js = {'faceId1': self.azureFaceId, 'faceId2': anotherId}
        res = requests.post(url=url + 'verify',
                    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': api_key},
                    json = js
                    )
        # Json decoding
        obj = json.loads(res.text)
        print(res.text)

        return (obj['isIdentical'], obj['confidence'])

    def getAzureId(self):
        return self.azureFaceId
