# -*- coding: utf-8 -*-
import string
import random

# Generar un random de longitud 6 para el nombre de la imagen
def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    a = ''.join(random.choice(chars) for x in range(size))
    return a + ".jpg"
