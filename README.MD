# 🧑‍🏫 Herramienta de Corrección Automática para Exámenes de Programación

## 📝 Descripción

Este proyecto es una **herramienta de corrección automática** para exámenes de programación y pruebas técnicas. La herramienta permite la corrección de programas basándose en *pruebas unitarias* y en *análisis semántico* de la calidad del código fuente, a través de un flujo de trabajo impulsado por IA.

## 🚀 Cómo utilizarlo

Para utilizar la herramienta, siga estos pasos:

### 1️⃣ Estructura de carpetas

Respete la siguiente estructura de carpetas:

```bash
📁 Directorio principal
├── 📁 parciales    (archivos de los estudiantes)
├── 📁 tests        (pruebas unitarias)
├── 📁 informes     (resultados generados)
└── 📄 checker.py   (script principal)
```

### 2️⃣ Archivo de pruebas unitarias

Cree un archivo de pruebas unitarias en la carpeta tests. Este archivo debe contener **obligatoriamente** la siguiente línea de código:

```python
#! Necesaria para checker.py
from exam import funcA, funcB, ..., funcN
```

Debe crear una clase extendida de `unittest.TestCase` y definir los métodos de prueba para cada función a evaluar. Por ejemplo:

```python
class TestEjA(unittest.TestCase):
    def test_load_matrix_invalid_row(self):
        """
        Test 1: Caso edge para load_matrix con row_num <= 0.Se verifica que al pasar 0 filas, la función retorne una lista vacía.
        """
        self.assertEqual(load_matrix(0, 3), [])
```

*Nota:* Es importante incluir una descripción detallada del caso de prueba en el docstring del método, ya que esto se usara por el agente de IA y se incluira en el informe de resultados.

### 3️⃣ Archivos a Evaluar

Cargue todos los archivos a evaluar en la carpeta parciales. Estos archivos deben exportar las funciones que se desean corregir. En caso de no contar con una función en particular, esa prueba se dará como fallida, especificando que no se encontró dicha función.

### 4️⃣ Configuración de variables de entorno

Cree un archivo .env en la raíz del proyecto con las siguientes variables:

```bash
WEBHOOK_URL=URL del webhook al workflow de IA
WEBHOOK_SECRET=Auth del webhook
```

### 5️⃣ Instalación de dependencias

Instale las dependencias usando pip:

```bash
# Se requiere Python 3.5+
pip install -r requirements.txt
```

### 6️⃣ Configuracion de Checker

Debe configurar el archivo checker.py con la siguientes constantes:

```python
UTEST_DIR = "tests" # Carpeta de pruebas unitarias
UTEST_FILENAME = "ejB.test.py" # suite de tests a utilizar
EXAMS_DIR = "parciales" # Carpeta de examenes
ASSIGNMENT = "En el siguiente ejercicio debe..." # Consigna del ejercicio a evaluar
```

Si opto por la estructura de carpetas sugerida, no es necesario modificar estas constantes. Unicamente *ASSIGNMENT* .

### 7️⃣ Ejecución

Ejecute el script principal:

```bash
python checker.py
```

### 8️⃣ Interpretación de resultados

Los resultados se guardan automáticamente en la carpeta informes con el siguiente formato:

- **Archivo Excel**: `informes/results_YYYYMMDD_HHMMSS.xlsx`
- **Organización**: Un reporte por alumno con las siguientes secciones:
  - 📊 **Resumen general**: Nombre, porcentaje de pruebas pasadas y nota sugerida
  - 📝 **Informe detallado**: Análisis cualitativo del código por IA
  - 🧪 **Pruebas individuales**: Lista de todas las pruebas con su resultado (PASSED/FAILED)
  - 📈 **Confianza**: Nivel de certeza en la evaluación automática

### 9️⃣ Solución de problemas comunes

| Problema | Posible solución |
|----------|-----------------|
| ❌ **No se encuentran los archivos** | Verifique que los archivos estén en la carpeta parciales con extensión `.py` |
| ❌ **Error de importación** | Verifique que el archivo de test tenga la línea `from exam import ...` |
| ❌ **Sin respuesta del servicio IA** | Revise las credenciales en .env y su conexión a internet |
| ❌ **No se generan informes** | Verifique que exista la carpeta informes con permisos de escritura |

## 👨‍💻 Desarrolladores

- [Alejo Torres](https://github.com/AlejoTorres2001)

## 📚 Guía para alumnos

Cada trabajo presentado debe respetar lo siguiente:

- Entregar **un solo archivo** con su nombre y apellido y la extensión`.py`
- El archivo puede contener la cantidad de funciones que necesite para resolver el problema. Pero debe **respetar los nombres** de las funciones principales designadas para cada ejercicio.

### 🔹 Ejercicio Obligatorio 1 - Tema A

- **`load_matrix`**: Esta función encapsula toda la lógica referida a cargar una matriz de palabras. Sus argumentos son `num_col` (número de columnas) y `num_row` (número de filas). Debe retornar una matriz de palabras.
  
- **`print_matrix`**: Esta función encapsula toda la lógica referida a imprimir una matriz de palabras. Su argumento es una matriz de palabras. No retorna nada. Imprime la matriz.
  
- **`count_letters`**: Esta función encapsula toda la lógica referida a contar letras en una matriz de palabras. Sus argumentos son el tipo de letra a contar (vocal o consonante) y una matriz de palabras. No retorna nada. Modifica la matriz de palabras.
  
- **`main`**: Esta función es la principal del script. Debe solicitar al usuario el número de filas y cargar una matriz de palabras. Luego debe imprimir la matriz, solicitar al usuario el tipo de letra a contar (vocal o consonante) y contar las letras en la matriz. Por último debe imprimir la matriz resultante. No retorna nada.

### 🔹 Ejercicio Obligatorio 1 - Tema B

- **`load_matrix`**: Esta función encapsula toda la lógica referida a cargar una matriz de palabras. Sus argumentos son `num_row` (número de filas) y `num_col` (número de columnas). Debe retornar una matriz de palabras.

- **`show_palindrome`**: Esta función se encarga de identificar y mostrar las palabras palíndromas contenidas en la matriz, indicando la fila y la columna donde se encuentran dichas palabras.

- **`show_longest_word`**: Esta función identifica y muestra la palabra con más caracteres de la matriz.

- **`show_duplicated_words`**: Esta función detecta y muestra las palabras que se repiten en la matriz.

- **`menu`**: Esta función es la interfaz principal del script. Debe mostrar un menú con las siguientes opciones:
  - Cargar la matriz
  - Mostrar palíndromos
  - Mostrar la palabra más larga
  - Mostrar las palabras duplicadas
  - Salir
  
  Cada opción invoca la función correspondiente. La función `menu` no retorna nada.

## 💡 Tips para alumnos - ¿Cómo leer la firma de una función?

En Python podemos usar *anotaciones de tipo* para especificar el tipo de dato requerido en cada argumento y el tipo de dato devuelto por la función. Por ejemplo, la siguiente firma:

```python
def ejemplo_funcion(a: int, b: str) -> List[int]:
```

Significa:

- Recibe dos argumentos: `a` de tipo entero y `b` de tipo string
- Retorna una lista de enteros

## 📋 Firmas de funciones - Referencia

### Ejercicio Obligatorio 1 - Tema A

```python
def load_matrix(num_row: int, num_col: int) -> List[List[str]]:
    # Implementación aquí

def print_matrix(matrix: List[List[str]]) -> None:
    # Implementación aquí

def count_letters(letter_type: Literal["consonant", "vowel"], matrix: List[List[str]]) -> None:
    # Implementación aquí

def main() -> None:
    # Implementación aquí
```

Notas adicionales:

- **`Literal["consonant", "vowel"]`**: Literal es una clase que permite definir valores específicos que puede tomar un argumento. En este caso, el argumento letter_type puede ser "consonant" o "vowel".**Unicamente**

- **`List[List[str]]`**: Se refiere a un vector, que dentro tiene vectores cuyos elementos son de tipo string.

### Ejercicio Obligatorio 1 - Tema B

```python
def load_matrix(row_num: int, col_num: int) -> list[list[str]]:  
    # Implementación aquí

def show_palindrome(matrix: list[list[str]]) -> None:
    # Implementación aquí

def show_longest_word(matrix: list[list[str]]) -> None:
    # Implementación aquí

def show_duplicated_words(matrix: list[list[str]]) -> None:
    # Implementación aquí

def menu() -> None:
    # Implementación aquí  
```

---

## 📊 Formato de evaluación

Los resultados de la evaluación se presentan en un informe Excel detallado que incluye:

- Resultados de las pruebas unitarias
- Análisis automático del código
- Calificación sugerida
- Comentarios detallados sobre el código
