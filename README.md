# Gugul

Este repositorio es una api de Flask para brindar servicio de un buscador. El algoritmo implementado es el modelo vectroial para establecer la similitud de una query con todos los documentos del corpus.


### Instalar dependencias

```
pip install -r requirements.txt
```

### Para correr la aplicacion 
```
python run.py
```


### Disenno completo del sistema segun cada etapa de la recuperacion de informacion. debe especificar las consideraciones y argumentos para la eleccion y aplicacion de los modelos y enfoques adoptados.

Decidimos trabajar el modelo vectorial porque es un modelo que ha demostrado ser eficiente en SRI con repositorios grandes y de variadas tematicas. En comparacion con el modelo booleano es mejor para proposito general, pues para booleano es recomendado que la informacion que se trata de recolectar sea de un mismo tema, ademas de que es mas recomendable usar por expertos, no sucede asi con el vectorial, en cuyo caso puede ser usado facilmente por usuarios no expertos.

para el desarrollo del modelo usamos el esquema de ponderacion *tf-idf* pues para los documentos este esquema mejora el rendimiento de la recuperacion. La estrategia de coincidencia parcial que usa el modelo permite la recuperacion de los documentos que mas se aproximen a los requerimientos de la consulta. La estrategia permite ordenar los documentos por orden de similitud con la consulta.

Un problema a resolver en el modelo es que  los terminos indexados del documento son mutuamente independiantes. Aunque en realidad existe relacion entre algunos terminos en el documento. Aunque podria significar una limitacion del modelo simplifica el proceso de recuperacion y en algunos casos mejora el rendimiento aunque a la hora de extraccion el proceso no sea tan abstracto como sistemas mas inteligantes. El analisis de la correlacion requiere que se tangan enfoques mas avanzados en el sistema.

### Presentacion de las herramientas empleadas para la programacion y aspectos mas importantes del codigo.

El proyecto esta dividido en dos aplicaciones. Una que es el sistema de recuperacion y la otra que es la Api que consume los recursos para interactuar con el usuario.

#### Gugul_Back
Una aplicacion usa Flask para generar un servicio que nos retornara dada una query todos los documentos que mas similitud tengan son esa query.

##### Estructura del proyecto
```
  |-document_handler.py
  |-documents.py
  |-readcrancollection.py
  |-REARME.md
  |-requierments.txt
  |-run.py
  |-tester.py
```

En `document_handler.py` esta la implementacion del sistema. Esta implementacion tiene una coleccion de documentos. A la hora de contruir el contenedor se llaman a varias funciones que inicializan y realizan parte del proceso de la recuperacion , como tokenizar el texto y extraer las frecuencias para posteriores calculos con las consultas que se hagan.

En `documents.py` hay una clase que me representa un documentos para el corpus. Este representacion del documento tiene un `id` (que me representa un entero unico para identificar el documento) , un `title` el titulo del documento , `author` que me representan los autores del documento, `text` que me representa el cuerpo del documento.

En `readcrancollectio.py` hay varias rutinas para leer y extraer los documentos del test `cran` y realizar varias pruebas de similitud con los datos obtenido de el sistema de recuperacion implementado.

En `README.md` esta este documento con todo las partes de la implementacion del sistema y algunas particularidades de esta solucion.

En `requirements.txt` estan los requerimientos de dependencias del proyecto que deben instalarse antes de que se corra la aplicacion. el comando que debe correr se en el directorio del proyecto (es decir donde se encuentra el fichero ***requierements.txt***) es: ```pip install -r requirements.txt```

En `run.py` ese encuentra una aplicacion de flask sencialla para correr el sistema de recuperacion como un servicio para ser consumido por otra aplicacion `Gugul_Front` (que es el UI de la aplicacion)

En `tester.py` se encuentra un sistema de pruebas para testear el sistema con los datos de las pruebas que se pasaron en las colecciones de prueba.


### Análisis crítico de las ventajas y desventajas del sistema desarrollado.

Se ha mostrado la arquitectura del modelo vectorial lo suficientemente abierto y flexible para ser usado en labores docentes, asi como investigaciones. La sencillez deesta arquitectura permitira tanto la facil observacion de resultados y estructuras intermedias como la modificacion y anadido de nuevos modulos y por tanto permite experimentar con el modelo. Puede ser usado en la docencia de alguans materias relacionadas directamente con la extraccion automatizada de informacion  


### Recomendaciones para trabajos futuros que mejoren la propuesta.

Para mejoras del sistema se propone al integracion con algoritmos de `Crawling`. Ademas se puede trabajar en el reconociemito de entidades que ayuden a una mejor vinculacion entre diferenctes token de los documentos que guardan relacion y pueden rindar mucha informacion a la hora de determinar el peso de un documento en el ambito de la busqueda . Tambien se puede trabajar en correcciones basicas como en interacciones con los usuarios que permitan al sistema saber que tan provechoso le fueron los resultado de la apliacion para una consulta dada, la informacion recolectada se podria usar para proximas consultas similares o iguales.