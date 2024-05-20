JSON extracter es una herramienta que permite extraer objetos JSON implícitos en un texto. Este paquete busca automáticamente cualquier JSON válido dentro de un texto dado y lo extrae para su uso posterior.

Características
Detecta y extrae JSON implícito en cualquier texto.
Fácil de usar con una API sencilla.
Instalación
Puedes instalar JSON extracter usando pip:

pip install json-extracter

Uso
Aquí tienes un ejemplo básico de cómo usar JSON extracter:

python
Copiar código
from json-extracter import json_parse

texto = """
Este es un ejemplo de texto que contiene un JSON implícito: 
{"name": "John", "age": 30, "city": "New York"} y aquí continúa el texto.
"""

json_extraido = json_parse(texto)

for json_obj in json_extraido:
    print(json_obj)

Salida esperada
json
Copiar código
{"name": "John", "age": 30, "city": "New York"}
API
extract_json(texto)

texto (str): El texto que contiene el JSON implícito.
Retorna: Una lista de objetos JSON extraídos del texto.
Contribuir
¡Las contribuciones son bienvenidas! Si tienes ideas, encuentra un error o quieres mejorar el proyecto, por favor abre un issue o envía un pull request.

Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

Contacto
Para cualquier pregunta o comentario, por favor contacta a edgar.edgarroman@gmail.com.