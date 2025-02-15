import unittest
from unittest.mock import patch, MagicMock
import subprocess
import tkinter as tk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import python_gui.gui as gui


class TestCryptoFunctions(unittest.TestCase):

    @patch('python_gui.gui.subprocess.run')
    @patch('python_gui.gui.messagebox.showinfo')
    def test_encrypt_file_success(self, mock_showinfo, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=''
        )
        input_path = "test_input.txt"
        output_path = "test_output.enc"
        key = "156cb7d2f1523f4948364800c2feb9087845a9cef2b53592bbfa592a49af0751"
        gui.function_from_rust.encrypt_file_rust(input_path, output_path, key)
        
        mock_run.assert_called_with(
            ["../rust_func/target/release/file_encryption.exe", "encrypt", input_path, output_path, key],
            check=True, text=True, capture_output=True
        )
        mock_showinfo.assert_called_with("Success", "File successfully encrypted")

    @patch('python_gui.gui.subprocess.run')
    @patch('python_gui.gui.messagebox.showerror')
    def test_encrypt_file_failure(self, mock_showerror, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, cmd="cmd")
        input_path = "test_input.txt"
        output_path = "test_output.enc"
        key = "156cb7d2f1523f4948364800c2feb9087845a9cef2b53592bbfa592a49af0751"
        
        gui.function_from_rust.encrypt_file_rust(input_path, output_path, key)
        
        mock_showerror.assert_called_with("Error", "Error: incorrect file path")


    @patch('python_gui.gui.subprocess.run')
    @patch('python_gui.gui.messagebox.showinfo')
    def test_decrypt_file_success(self, mock_showinfo, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=''
        )
        input_path = "test_input.enc"
        output_path = "test_output.txt"
        key = "156cb7d2f1523f4948364800c2feb9087845a9cef2b53592bbfa592a49af0751"
        
        gui.function_from_rust.decrypt_file_rust(input_path, output_path, key)
        
        mock_run.assert_called_with(
            ["../rust_func/target/release/file_encryption.exe", "decrypt", input_path, output_path, key],
            check=True, text=True, capture_output=True
        )
        mock_showinfo.assert_called_with("Success", "File decrypted")


    @patch('python_gui.gui.subprocess.run')
    @patch('python_gui.gui.messagebox.showerror')
    def test_decrypt_file_failure(self, mock_showerror, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, cmd="cmd")
        input_path = "test_input.enc"
        output_path = "test_output.txt"
        key = "156cb7d2f1523f4948364800c2feb9087845a9cef2b53592bbfa592a49af0751"
        
        gui.function_from_rust.decrypt_file_rust(input_path, output_path, key)
        
        mock_showerror.assert_called_with("Error", "Error: incorrect encryption key")


    @patch('python_gui.gui.subprocess.run')
    def test_generate_key_rust(self, mock_run):
        dummy_output = "Сгенерированный ключ: ABCDEF"
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=dummy_output
        )
        
        dummy_entry = MagicMock()
        gui.key_entry = dummy_entry
        
        gui.function_from_rust.generate_key_rust()
        
        dummy_entry.delete.assert_called_with(0, tk.END)
        dummy_entry.insert.assert_called_with(0, "ABCDEF")


if __name__ == '__main__':
    unittest.main()