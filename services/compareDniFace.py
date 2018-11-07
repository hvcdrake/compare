# Import region
from flask import Flask, request, Response, redirect
from flasgger import Swagger
import logging
import nltk
import json
from Utils import random_generator
import base64
import requests
import detection.DetectionClass as det
from flask_cors import CORS, cross_origin
import os
# from applicationinsights.flask.ext import AppInsights
# import requests_cache
# End region

# Constructors region
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/api/v1/DniVsFace": {"origins": "http://localhost:30676"}})
cors = CORS(app, resources={r"/api/v1/DniVsFace": {"origins": "*"}})

app.config["SWAGGER"] = {
    "title": "API YANBAL.comparing.Python",
    "uiversion": 2,
}
# app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = PARAMETERS.instrumentation_key
# appinsights = AppInsights(app)

swagger = Swagger(
    app,
    template={
        "openapi": "3.0.0",
        "info": {
            "title": "API YANBAL.comparing.Python",
            "version": "1.00"
        },
        "consumes": [
            "application/json",
        ],
        "produces": [
            "application/json",
        ],
    },
)
# End region


def stringFromPath(path):
    file_name = path
    image_file = open(file_name, 'rb')
    image = image_file.read()
    encoded = base64.b64encode(image)
    return encoded.decode("utf-8")


@app.route('/api/v1/DniVsFace', methods=['POST'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def DniVsFace():
    # region Swagger
    """ Comparing face vs identity card (dni)
    ---
    tags:
      - Comparacion Face Vs Dni
    parameters:
      - in: body
        name: body
        schema:
            face-img:
                type: string
                description: imagen en base64
                default: none
            dni-img:
                type: string
                description: imagen en base64
                default: none
    responses:
      200:
            face-img-pro:
                type: string
                description: imagen en base64
                default: none
            dni-img-pro:
                type: string
                description: imagen en base64
                default: none
            result:
                type: boolean
                description: true / false
            confidence:
                type: float
                description: beetween 0 and 1
        examples:
    """
    # endregion

    data = request.get_json(silent=True)
    # data = request.get_data()

    #print(str(data))
    print("face-img:" + str(data["faceimg"][0:20]))
    print("dni-img:" + str(data["dniimg"][0:20]))

    base64img_face = data["faceimg"]
    base64img_dni = data["dniimg"]

    name_temp_face = random_generator(size=8)
    name_temp_dni = random_generator(size=8)
    # Convierte el string en base64 a arreglo de bytes
    # base64img = base64img.decode("utf-8")
    bytes_ = base64.b64decode(base64img_face)
    with open(name_temp_face, 'wb') as f:
        f.write(bytes_)

    bytes_ = base64.b64decode(base64img_dni)
    with open(name_temp_dni, 'wb') as f:
        f.write(bytes_)

    del(bytes_)
    base64img_face = None
    base64img_dni = None
    del(data)

    # Initialize objects
    d = det.DetectionFace()
    # video = cv2.VideoCapture(0)

    print("Detectando rostro en DNI ...")
    face1 = d.detection(name_temp_face, name_temp_face[0:-4] + "_face")

    print("Detectando rostro en DNI ...")
    face2 = d.detection(name_temp_dni, name_temp_dni[0:-4] + "_dni")

    j = {}
    if (face1 is not None and face2 is not None):
        comp_result = face1.verify(face2.getAzureId())
        print(comp_result)
        j["result"] = comp_result[0]
        j["confidence"] = comp_result[1]
        j["faceimgpro"] = stringFromPath("processed/p_" + name_temp_face[0:-4] + "_face.jpg")
        j["dniimgpro"] = stringFromPath("processed/p_" + name_temp_dni[0:-4] + "_dni.jpg")
        j["error"] = None
        os.remove(name_temp_face)
        os.remove(name_temp_dni)
        print("Succeeded in processing")
    else:
        j["faceimgpro"] = stringFromPath(name_temp_face)
        j["dniimgpro"] = stringFromPath(name_temp_dni)
        j["result"] = False
        j["confidence"] = 0.0
        j["error"] = "No hemos podido detectar un rostro. Por favor intenta nuevamente."

    if face1 is not None:
        j["faceimgpro"] = stringFromPath("processed/p_" + name_temp_face[0:-4] + "_face.jpg")
        os.remove("processed/p_" + name_temp_face[0:-4] + "_face.jpg")
    if face2 is not None:
        j["dniimgpro"] = stringFromPath("processed/p_" + name_temp_dni[0:-4] + "_dni.jpg")
        os.remove("processed/p_" + name_temp_dni[0:-4] + "_dni.jpg")

    js = json.dumps(j)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.errorhandler(500)
def server_error(e):
    logging.exception('Ha ocurrido un error durante la petición.')
    return """
    Un error interno ha ocurrido : <pre>{}</pre>
    """.format(e), 500


def prepareAllAndGetFlaskApp():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    return app


if __name__ == '__main__':
    prepareAllAndGetFlaskApp()
    Port = 8089
    app.run(host='0.0.0.0', port=Port, threaded=True, debug=True)
