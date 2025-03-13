import unittest
from unittest.mock import patch
import io
import sys


#! Necesaria para checker.py
from exam import load_matrix, print_matrix, count_letters, main
# Se asume que las siguientes funciones se han importado:
# - load_matrix
# - print_matrix
# - count_letters
# - main

"""
#? Cada Trabajo presentado, si opta por la opción de ser evaluado con tests unitarios debe respetar lo siguiente: 
- Entregar un solo archivo con su nombre y apellido y la extension .py
- El archivo puede contener la cantidad de funciones que necesite pero debe respetar el nombre de las siguientes funciones principales:

  - load_matrix: esta función encapsula toda la lógica referida a cargar una matriz de palabras sus argumentos son num_col (numero de columnas) y num_row (numero de filas). Debe retornar una matriz de palabras.
  
  - print_matrix: esta función encapsula toda la lógica referida a imprimir una matriz de palabras. Sus argumentos son una matriz de palabras. No retorna nada. Imprime la matriz.
  
  - count_letters: esta función encapsula toda la lógica referida a contar letras en una matriz de palabras. Sus argumentos son el tipo de letra a contar (vocal o consonante) y una matriz de palabras. No retorna nada. Modifica la matriz de palabras.
  
  - main: esta función es la principal del script. Debe solicitar al usuario el numero de filas y cargar una matriz de palabras. Luego debe imprimir la matriz, solicitar al usuario el tipo de letra a contar (vocal o consonante) y contar las letras en la matriz. Por ultimo debe imprimir la matriz resultante. No retorna nada.


A continuación se presentan las firmas de cada una de las funciones mencionadas:

!Como leer una firma? En python podemos usar Duck Typing para especificar el tipo de dato requerido en cada argumento y el tipo de dato devuelto por la función. Por ejemplo, la siguiente firma:

! def ejemplo_funcion(a: int, b: str) -> List[int]:
! - Recibe dos argumentos, 'a' de tipo entero y 'b' de tipo string.
! - Retorna una lista de enteros.


? def load_matrix(num_row: int, num_col: int) -> List[List[str]]:

? def print_matrix(matrix: List[List[str]]) -> None:

? def count_letters(letter_type: Literal["consonant", "vowel"], matrix: List[List[str]]) -> None:

? def main() -> None:
"""

class TestEjA(unittest.TestCase):
    def test_load_matrix_invalid_row(self):
        """
        Test 1: Caso edge para load_matrix con row_num <= 0.Se verifica que al pasar 0 filas, la función retorne una lista vacía.
        """
        self.assertEqual(load_matrix(0, 3), [])

    def test_load_matrix_invalid_col(self):
        """
        Test 2: Caso edge para load_matrix con col_num <= 0.Se verifica que al pasar 0 columnas, la función retorne una lista vacía.
        """
        self.assertEqual(load_matrix(2, 0), [])

    @patch('builtins.input', side_effect=["word1", "word2", " ", "word3", "word4", " "])
    def test_load_matrix_valid(self, mock_input):
        """
        Test 3: Funcionamiento general de load_matrix.Se simulan 6 llamadas a input para una matriz de 2 filas y 3 columnas.Los inputs simulados se corresponden con:- Fila 1: "word1", "word2", " " - Fila 2: "word3", "word4", " "Se verifica que la matriz cargada sea la esperada.
        """
        expected = [["word1", "word2", " "], ["word3", "word4", " "]]
        result = load_matrix(2, 3)
        self.assertEqual(result, expected)

    def test_print_matrix_empty(self):
        """
        Test 4: Caso edge para print_matrix.Se verifica que al pasar una matriz vacía, no se imprima nada.
        """
        captured_output = io.StringIO()
        sys.stdout = captured_output  # Redirige stdout
        print_matrix([])
        sys.stdout = sys.__stdout__     # Restaura stdout
        self.assertEqual(captured_output.getvalue(), "")


    def test_count_letters_vowels(self):
        """
        Test 5: Funcionamiento de count_letters para contar vocales.Se utiliza una matriz de una fila:[["hello", "world", ""]]En "hello" hay 2 vocales (e, o) y en "world" 1 (o), total = 3.
        Se espera que la última posición se reemplace por 3.
        """
        matrix = [["hello", "world", ""]]
        count_letters("vowel", matrix)
        self.assertEqual(matrix, [["hello", "world", 3]])

    def test_count_letters_consonants(self):
        """
        Test 6: Funcionamiento de count_letters para contar consonantes.Se utiliza la misma matriz:[["hello", "world", ""]]En "hello" hay 3 consonantes (h, l, l) y en "world" hay 4 (w, r, l, d), total = 7.Se espera que la última posición se reemplace por 7.
        """
        matrix = [["hello", "world", ""]]
        count_letters("consonant", matrix)
        self.assertEqual(matrix, [["hello", "world", 7]])

    @patch('builtins.input', side_effect=["2", "hello", "world", "x", "foo", "bar", "y", "vowel"])
    def test_main_function(self, mock_input):
        """
        Test 7: Funcionamiento general de la función main.Se simulan los siguientes inputs:- "2": número de filas.- Para la primera fila: "hello", "world", "x".- Para la segunda fila: "foo", "bar", "y".- "vowel": opción para contar vocales.El conteo esperado:- Fila 1: "hello" (2 vocales) + "world" (1 vocal) = 3.- Fila 2: "foo" (2 vocales) + "bar" (1 vocal) = 3.Se captura la salida por consola para verificar que aparecen los valores de las matrices antes y después de la modificación.
        """
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        # Se verifica que se impriman los elementos originales y luego se vea el conteo modificado.
        self.assertIn("hello", output)
        self.assertIn("world", output)
        self.assertIn("foo", output)
        self.assertIn("bar", output)
        # Se espera que, luego de contar vocales, la última columna tenga el valor "3"
        self.assertIn("3", output)
        self.assertIn("matriz luego de contar las letras", output)

    def test_count_letters_empty_matrix(self):
        """
        Test 8: Caso edge para count_letters.Se verifica que al pasar una matriz vacía, la función no haga cambios ni lance errores.
        """
        matrix = []
        count_letters("vowel", matrix)
        self.assertEqual(matrix, [])

    def test_count_letters_non_letters(self):
        """
        Test 9: Funcionamiento de count_letters en una matriz con caracteres no alfabéticos.Se utiliza la matriz:[["123", "!!", ""]]Tanto para contar vocales como consonantes, se espera un total de 0.
        """
        # Prueba para vocales.
        matrix = [["123", "!!", ""]]
        count_letters("vowel", matrix)
        self.assertEqual(matrix, [["123", "!!", 0]])
        # Se reinicia la matriz para probar consonantes.
        matrix = [["123", "!!", ""]]
        count_letters("consonant", matrix)
        self.assertEqual(matrix, [["123", "!!", 0]])
        
        
    def test_print_matrix_row_count(self):
      """
      Test 10: Verificar que se imprima una línea por cada fila.Se verifica que, al imprimir la matriz, se genere una línea por cada fila.Para ello, se utiliza una matriz de prueba con 3 filas y se cuenta el número de líneas en la salida capturada.
      """
      matrix = [["abc", "de"], ["fgh", "ijk"], ["lm", "nopq"]]
      captured_output = io.StringIO()
      sys.stdout = captured_output  # Redirige stdout
      print_matrix(matrix)
      sys.stdout = sys.__stdout__     # Restaura stdout
      # Se dividen las líneas de la salida y se elimina la línea vacía final (si la hay)
      output_lines = [line for line in captured_output.getvalue().splitlines() if line]
      self.assertEqual(len(output_lines), len(matrix))

if __name__ == '__main__':
    unittest.main()
