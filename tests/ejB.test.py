import unittest
from unittest.mock import patch
import io
import sys

#! Necesaria para checker.py
from exam import load_matrix, show_palindrome, show_longest_word, show_duplicated_words, menu

class TestEjB(unittest.TestCase):
    def test_load_matrix_invalid_row(self):
        """ 
        Test 1: Verifica que load_matrix retorne una lista vacía si row_num <= 0.
        Se espera que load_matrix(0, 3) devuelva [].
        """
        self.assertEqual(load_matrix(0, 3), [])

    def test_load_matrix_invalid_col(self):
        """
        Test 2: Verifica que load_matrix retorne una lista vacía si col_num <= 0.
        Se espera que load_matrix(2, 0) devuelva [].
        """
        self.assertEqual(load_matrix(2, 0), [])

    @patch('builtins.input', side_effect=["a", "b", "c", "d"])
    def test_load_matrix_valid(self, mock_input):
        """
        Test 3: Carga de matriz válida.
        Se simulan 4 llamadas a input para cargar una matriz de 2 filas y 2 columnas.
        Los inputs son: "a", "b", "c", "d", y se espera la matriz: [["a", "b"], ["c", "d"]].
        """
        result = load_matrix(2, 2)
        self.assertEqual(result, [["a", "b"], ["c", "d"]])

    def test_show_palindrome_found(self):
        """
        Test 4: Verifica que show_palindrome imprima los mensajes para las palabras palíndromas.
        Se proporciona una matriz con dos palabras palíndromas ("ana" y "noon") y otras no palíndromas.
        Se comprueba que se indiquen la fila y columna correctas en la salida.
        """
        matrix = [["ana", "test"], ["noon", "abc"]]
        captured_output = io.StringIO()
        sys.stdout = captured_output
        show_palindrome(matrix)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        # Se espera que "ana" (fila 0, columna 0) y "noon" (fila 1, columna 0) aparezcan en la salida.
        self.assertIn("la palabra: ", output)
        self.assertIn("ana", output)
        self.assertIn("fila:  0", output)
        self.assertIn("columna:  0", output)
        self.assertIn("noon", output)
        self.assertIn("fila:  1", output)

    def test_show_palindrome_not_found(self):
        """
        Test 5: Verifica que show_palindrome no imprima nada si no hay palabras palíndromas.
        Se utiliza una matriz sin palabras palíndromas.
        """
        matrix = [["abc", "def"], ["ghi", "jkl"]]
        captured_output = io.StringIO()
        sys.stdout = captured_output
        show_palindrome(matrix)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertEqual(output, "")

    def test_show_longest_word(self):
        """
        Test 6: Verifica que show_longest_word imprima correctamente la palabra con más caracteres.
        Se proporciona una matriz en la que "longestword" es la de mayor longitud.
        """
        matrix = [["hi", "hello"], ["test", "longestword"]]
        captured_output = io.StringIO()
        sys.stdout = captured_output
        show_longest_word(matrix)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("La palabra con más caracteres es: ", output)
        self.assertIn("longestword", output)

    def test_show_duplicated_words(self):
        """
        Test 7: Verifica que show_duplicated_words imprima correctamente las palabras duplicadas.
        Se utiliza una matriz en la que la palabra "dup" aparece en más de una posición.
        """
        matrix = [["dup", "unique"], ["dup", "another"]]
        captured_output = io.StringIO()
        sys.stdout = captured_output
        show_duplicated_words(matrix)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Las palabras duplicadas son: ", output)
        self.assertIn("dup", output)

    @patch('builtins.input', side_effect=[
        "1",      # Opción: Cargar Matriz
        "2",      # Número de filas
        "2",      # Número de columnas
        "a", "b", "c", "d",  # Valores para la matriz: row0: a, b; row1: c, d
        "2",      # Opción: Mostrar palíndromos
        "3",      # Opción: Mostrar palabra más larga
        "4",      # Opción: Mostrar palabras duplicadas
        "5"       # Opción: Salir
    ])
    def test_menu_full_flow(self, mock_input):
        """
        Test 8: Simula el flujo completo del menú.
        Se ingresan los datos para:
          - Cargar una matriz 2x2.
          - Mostrar palíndromos (aunque en este caso probablemente no se encuentren).
          - Mostrar la palabra más larga.
          - Mostrar palabras duplicadas.
          - Salir.
        Se captura la salida para verificar que se impriman los mensajes y datos esperados.
        """
        captured_output = io.StringIO()
        sys.stdout = captured_output
        menu()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        # Se verifica que se muestre el menú inicial
        self.assertIn("1. Cargar Matriz", output)
        # Verifica que la matriz cargada incluya "a", "b", "c" y "d"
        self.assertIn("a", output)
        self.assertIn("b", output)
        self.assertIn("c", output)
        self.assertIn("d", output)
        # Verifica la impresión de la opción de palabra más larga y duplicados
        self.assertIn("La palabra con más caracteres es: ", output)
        self.assertIn("Las palabras duplicadas son: ", output)

    @patch('builtins.input', side_effect=[
        "invalid",  # Opción inválida
        "5"         # Luego se ingresa la opción para salir
    ])
    def test_menu_invalid_option(self, mock_input):
        """
        Test 9: Verifica que el menú maneje correctamente una opción inválida.
        Se simula un ingreso de opción no válida, y se espera que se imprima "Opción inválida".
        Luego se ingresa "5" para salir.
        """
        captured_output = io.StringIO()
        sys.stdout = captured_output
        menu()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Opción inválida", output)
        
    def test_show_duplicated_words_no_duplicates(self):
        """
        Test 10: Verifica que show_duplicated_words imprima una lista vacía
        si no hay palabras duplicadas en la matriz.
        Se utiliza una matriz sin duplicados y se espera que la salida muestre una lista vacía.
        """
        matrix = [["a", "b"], ["c", "d"]]
        captured_output = io.StringIO()
        sys.stdout = captured_output
        show_duplicated_words(matrix)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Las palabras duplicadas son: ", output)
        self.assertIn("[]", output)

if __name__ == '__main__':
    unittest.main()
