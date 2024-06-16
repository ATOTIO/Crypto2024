import string
import sys
from collections import Counter
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox

class SubstitutionCipherTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.key_mapping = self.generate_default_key_mapping()  # 默认的密钥映射
        self.single_letter_suggestions = {}  # 单字母建议
        self.double_letter_suggestions = {}  # 双字母建议
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Input Fields
        self.ciphertext_label = QLabel("Ciphertext:")
        self.ciphertext_input = QTextEdit()
        
        # Key Mapping Inputs
        key_mapping_layout = QGridLayout()
        self.key_input_boxes = {}
        row, col = 0, 0
        for index, letter in enumerate(string.ascii_lowercase):
            label = QLabel(f"{letter.upper()} =")
            input_box = QLineEdit()
            input_box.setMaxLength(1)
            key_mapping_layout.addWidget(label, row, col)
            key_mapping_layout.addWidget(input_box, row, col + 1)
            self.key_input_boxes[letter] = input_box
            
            col += 2
            if (index + 1) % 7 == 0:  # 每行显示7个字母
                col = 0
                row += 1
        
        # Buttons
        button_layout = QHBoxLayout()
        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_text)
        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_text)
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze_text)
        self.update_key_button = QPushButton("Update Key Mapping")
        self.update_key_button.clicked.connect(self.update_key_mapping)
        button_layout.addWidget(self.encrypt_button)
        button_layout.addWidget(self.decrypt_button)
        button_layout.addWidget(self.analyze_button)
        
        # Output Fields
        self.decrypted_text_label = QLabel("Decrypted Text:")
        self.decrypted_text_output = QTextEdit()
        self.decrypted_text_output.setReadOnly(True)
        
        # Single Letter Analysis and Suggestions
        single_letter_layout = QHBoxLayout()
        
        self.single_letter_frequency_label = QLabel("Single\nFreq:")
        self.single_letter_frequency_output = QTextEdit()
        self.single_letter_frequency_output.setReadOnly(True)
        
        self.single_letter_suggestion_label = QLabel("Single\nSugg:")
        self.single_letter_suggestion_output = QTextEdit()
        self.single_letter_suggestion_output.setReadOnly(True)
        
        single_letter_layout.addWidget(self.single_letter_frequency_label)
        single_letter_layout.addWidget(self.single_letter_frequency_output)
        single_letter_layout.addWidget(self.single_letter_suggestion_label)
        single_letter_layout.addWidget(self.single_letter_suggestion_output)
        
        # Double Letter Analysis and Suggestions
        double_letter_layout = QHBoxLayout()
        
        self.double_letter_frequency_label = QLabel("Double \nFreq:")
        self.double_letter_frequency_output = QTextEdit()
        self.double_letter_frequency_output.setReadOnly(True)
        
        self.double_letter_suggestion_label = QLabel("Double \nSugg:")
        self.double_letter_suggestion_output = QTextEdit()
        self.double_letter_suggestion_output.setReadOnly(True)
        
        double_letter_layout.addWidget(self.double_letter_frequency_label)
        double_letter_layout.addWidget(self.double_letter_frequency_output)
        double_letter_layout.addWidget(self.double_letter_suggestion_label)
        double_letter_layout.addWidget(self.double_letter_suggestion_output)
        
        # Layout
        layout.addWidget(self.ciphertext_label)
        layout.addWidget(self.ciphertext_input)
        layout.addLayout(key_mapping_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.update_key_button)
        layout.addWidget(self.decrypted_text_label)
        layout.addWidget(self.decrypted_text_output)
        layout.addLayout(single_letter_layout)
        layout.addLayout(double_letter_layout)
        
        self.setLayout(layout)
        self.setWindowTitle("Substitution Cipher Tool")
        self.show()
    
    def encrypt_text(self):
        plaintext = self.ciphertext_input.toPlainText()
        encrypted_text = self.encrypt(plaintext.lower(), self.key_mapping)
        self.decrypted_text_output.setText(encrypted_text)
    
    def decrypt_text(self):
        ciphertext = self.ciphertext_input.toPlainText()
        decrypted_text = self.decrypt(ciphertext.lower(), self.key_mapping)
        self.decrypted_text_output.setText(decrypted_text)
    
    def analyze_text(self):
        ciphertext = self.ciphertext_input.toPlainText()
        
        # Update key mapping based on input boxes
        self.update_key_mapping()
        
        # Perform decryption based on current key mapping
        partial_decryption = self.decrypt(ciphertext.lower(), self.key_mapping)
        
        # Frequency analysis
        single_freq_analysis = self.single_letter_frequency_analysis(ciphertext)
        double_freq_analysis = self.double_letter_frequency_analysis(ciphertext)
        
        # Generate suggestions based on frequency analysis
        self.generate_suggestions(single_freq_analysis, double_freq_analysis)
        
        # Update output fields
        single_frequency_analysis_text = ""
        for letter, freq in sorted(single_freq_analysis.items(), key=lambda x: x[1], reverse=True):
            single_frequency_analysis_text += f"{letter}: {freq:.2%}\n"
        
        double_frequency_analysis_text = ""
        for letters, freq in sorted(double_freq_analysis.items(), key=lambda x: x[1], reverse=True):
            double_frequency_analysis_text += f"{letters}: {freq:.2%}\n"
        
        self.single_letter_frequency_output.setText(single_frequency_analysis_text)
        self.double_letter_frequency_output.setText(double_frequency_analysis_text)
        
        # Display suggestions
        self.display_suggestions()
    
    def update_key_mapping(self):
        # Update key mapping based on input boxes
        for letter in string.ascii_lowercase:
            self.key_mapping[letter] = self.key_input_boxes[letter].text().lower() or letter
        QMessageBox.information(self, "Update Key Mapping", "Key mapping updated successfully!")
    
    def encrypt(self, plaintext, key_mapping):
        table = str.maketrans(string.ascii_lowercase, ''.join(key_mapping.get(c, c) for c in string.ascii_lowercase))
        return plaintext.translate(table)
    
    def decrypt(self, ciphertext, key_mapping):
        table = str.maketrans(''.join(key_mapping.get(c, c) for c in string.ascii_lowercase), string.ascii_lowercase)
        return ciphertext.translate(table)
    
    def single_letter_frequency_analysis(self, text):
        # Count single letter frequencies
        letter_counts = Counter(c for c in text if c.isalpha())
        total_letters = sum(letter_counts.values())
        return {letter: count / total_letters for letter, count in letter_counts.items()}
    
    def double_letter_frequency_analysis(self, text):
        # Count double letter frequencies
        pairs = [text[i:i+2] for i in range(len(text) - 1)]
        pair_counts = Counter(pair for pair in pairs if all(c.isalpha() for c in pair))
        total_pairs = sum(pair_counts.values())
        return {pair: count / total_pairs for pair, count in pair_counts.items()}
    
    def generate_default_key_mapping(self):
        # Generate a default key mapping (identity mapping)
        return {c: c for c in string.ascii_lowercase}
    
    def generate_suggestions(self, single_freq_analysis, double_freq_analysis):
        # Generate suggestions based on frequency analysis
        self.single_letter_suggestions = {}
        self.double_letter_suggestions = {}
        
        # Generate suggestions from single letter frequency analysis
        sorted_single_freq = sorted(single_freq_analysis.items(), key=lambda x: x[1], reverse=True)
        most_common_letters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u']
        
        for i, (letter, _) in enumerate(sorted_single_freq):
            self.single_letter_suggestions[letter] = most_common_letters[i % len(most_common_letters)]
        
        # Generate suggestions from double letter frequency analysis
        sorted_double_freq = sorted(double_freq_analysis.items(), key=lambda x: x[1], reverse=True)
        most_common_digraphs = ['th', 'he', 'in', 'er', 'an', 're', 'nd', 'at', 'on', 'nt', 'ha', 'es', 'st', 'en', 'ed', 'to', 'it', 'ou', 'ea', 'hi']
        
        for i, (digraph, _) in enumerate(sorted_double_freq):
            self.double_letter_suggestions[digraph] = most_common_digraphs[i % len(most_common_digraphs)]
    
    def display_suggestions(self):
        # Display suggestions in the GUI
        single_suggestions_text = ""
        for letter, suggestion in self.single_letter_suggestions.items():
            single_suggestions_text += f"{letter}: {suggestion}\n"
        self.single_letter_suggestion_output.setText(single_suggestions_text)
        
        double_suggestions_text = ""
        for digraph, suggestion in self.double_letter_suggestions.items():
            double_suggestions_text += f"{digraph}: {suggestion}\n"
        self.double_letter_suggestion_output.setText(double_suggestions_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SubstitutionCipherTool()
