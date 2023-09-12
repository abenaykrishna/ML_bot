import typing
from PyQt5 import QtCore
import constants
import sys
import openai
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget,QLabel, QLineEdit,QPushButton,QVBoxLayout, QHBoxLayout,QGroupBox, QTextEdit

openai.api_key = constants.API_KEY

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    #creating user interface panel
    def init_ui(self):
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap('pink_scene.png').scaled(150,150,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        
        self.input_label = QLabel('Ask a question')
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Type here ......')
        self.answer_label = QLabel('Answer:')
        self.answer_field = QTextEdit()
        self.answer_field .setReadOnly(True)
        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet(
            """
            QPushButton{
                background_color: #4CAF50;
                border: none;
                colour: white;
                padding: 15px 32px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover{
                background-color:#3eBe41;
            }
            """
        )
        #creating a layout for popular questions 
        layout = QVBoxLayout()
        layout.setContentsMargins(10,10,10,10)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)

        #Adding Logo
        layout.addWidget(self.logo_label,alignment=Qt.AlignCenter)

        #Add input Field
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)
        layout.addLayout(input_layout)

        #Add answer field
        layout.addWidget(self.answer_field)
        layout.addWidget(self.answer_label)


        #set the layout
        self.setLayout(layout)

        #set the window properties
        self.setWindowTitle('Explaining code......')
        self.setGeometry(600,600,600,600)

        #connect the submit button to the functionwhich queries OpenAI's API
        self.submit_button.clicked.connect(self.get_answer)

    def get_answer(self):
        question = self.input_field.text()
        completion = openai.ChatCompletion.create(
            model  = "gpt-3.5-turbo",
            messages = [{
              "role": "system",
              "content": "You will be provided with a piece of code, and your task is to explain it in a concise way and your task is to extract a list of keywords or key concepts from it and"
            },
            {"role": "user", "content": question}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        answer = completion.choices[0].message.content

        self.answer_field.setText(answer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




