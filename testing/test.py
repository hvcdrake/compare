import requests
import json
import base64

face_file_name = "face11.jpg"
face_image_file = open(face_file_name, 'rb')
face_image = face_image_file.read()
face_encoded = base64.b64encode(face_image)

dni_file_name = "face12.jpg"
dni_image_file = open(dni_file_name, 'rb')
dni_image = dni_image_file.read()
dni_encoded = base64.b64encode(dni_image)

datos_extraidos = {}
datos_extraidos['img'] = "imagen_prueba_2"
js = json.dumps(datos_extraidos)

params = {
    "faceimg": face_encoded.decode("utf-8"),
    "dniimg": dni_encoded.decode("utf-8")
}

# c = face_encoded.decode("utf-8")
# print(c)

# print("Base64:" + str(encoded_string))
res = requests.post(url='http://localhost:8089/api/v1/DniVsFace',
					# url='https://comparingtry1.azurewebsites.net:8089/api/v1/DniVsFace',
                    json=params,
                    headers={'Content-Type': 'application/json'})

print(res.text)
