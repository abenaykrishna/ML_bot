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
        self.popular_questions_group = QGroupBox('Popular Question')
        self.popular_questions_layout = QVBoxLayout()
        self.popular_questions = ["What is AWS Cloud?","How do I create an AWS account?","What are AWS regions and availability zones?","How do I launch a virtual machine (EC2 instance) on AWS?","What is Amazon S3 and how do I use it for storage?"]
        self.question_buttons = []


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

        #adding the popular questions buttons
        for question in self.popular_questions:
            button = QPushButton(question)
            button.setStyleSheet(
                """
            QPushButton{
                background_color: #FFFFFF;
                border: 2px solid #00AEFF;
                colour: #00AEFF;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover{
                background-color:#00AEFF;
                color: #FFFFFF;
            }
                """
            )
            #when clicked on a question the question is taken as input
            button.clicked.connect(lambda _,q=question: self.input_field.setText(q))
            self.popular_questions_layout.addWidget(button)
            self.question_buttons.append(button)
        self.popular_questions_group.setLayout(self.popular_questions_layout)
        layout.addWidget(self.popular_questions_group)

        #set the layout
        self.setLayout(layout)

        #set the window properties
        self.setWindowTitle('AWS cloud Advice Bot')
        self.setGeometry(200,200,600,600)

        #connect the submit button to the functionwhich queries OpenAI's API
        self.submit_button.clicked.connect(self.get_answer)

    def get_answer(self):
        question = self.input_field.text()
        completion = openai.ChatCompletion.create(
            model  = "gpt-3.5-turbo",
            messages = [{"role":"user","content":"You are Amazon Web Services cloud expert. Answer the following question in a concise way or with bullet point."},
                        {"role":"user","content":f'{question}'}],
            max_tokens = 1024,
            n =1,
            stop=None,
            temperature=0.7
        )

        answer = completion.choices[0].message.content

        self.answer_field.setText(answer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
