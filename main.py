import os
import os.path
import sys

from PyQt5 import uic
# PYQT
from PyQt5.QtWidgets import *


# from typing import Set


# UI파일 연결
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # base_path : py code directory
    return os.path.join(base_path, "resource/", relative_path)


form = resource_path('word.ui')
form_class = uic.loadUiType(form)[0]

count = 0
page = 0

# 폴더가 없는 경우 생성
if (os.path.isdir("./resource/test_word/")) != 1:
    os.makedirs("./resource/test_word/")


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 버튼에 기능을 연결하는 코드
        self.bt_check.clicked.connect(self.buttonF_check)
        self.word_next_PushButton.clicked.connect(self.buttonNext_check)
        self.word_rm_PushButton.clicked.connect(self.buttonDel_check)

    # 체크 버튼 클릭
    def buttonF_check(self):
        # 표시창 정리
        self.te.clear()
        global page

        # 선택한 페이지 불러오기
        page = int(self.book_page_SpinBox.value())

        file_name = "./resource/test_resource/" + str(page) + ".txt"
        file = open(file_name, 'r', encoding='utf-8')
        text = file.read()
        file.close()

        # 불러온 내용을 표시창으로
        self.te.append(text)

        # 시작
        self.buttonNext_check(0)

    def buttonNext_check(self, state):
        global count
        global page

        # 단어 목록 txt 파일 불러오기
        word_f_name = "./resource/test_word_all/" + str(page) + ".txt"
        word_f = open(word_f_name, 'r', encoding='utf-8')

        data = word_f.readlines()
        word_f.close()

        # 처음부터 단어 끝까지
        if int(count) <= int(len(data)):

            # 만약 check 버튼을 눌러서 왔을 경우
            if state == 0:

                # 첫 단어가 아닐 때
                if count != 0:

                    # 단어의 뜻 수정이 안되었을 때
                    if self.word_mean_LineEdit.text() == "":

                        # 선택된 뜻으로 저장
                        mean = self.word_mean_ComboBox.currentText()

                    else:
                        # 단어 뜻이 수정되면, 그것으로 저장
                        mean = self.word_mean_LineEdit.text()

                    # 단어 위치 특수 분류(원래는 줄 수)
                    if self.word_line_LineEdit.text() == "a":
                        line = "제목"
                    elif self.word_line_LineEdit.text() == "b":
                        line = "단어풀이"
                    elif self.word_line_LineEdit.text() == "c":
                        line = "읽기 전에"
                    elif self.word_line_LineEdit.text() == "d":
                        line = "도움말"
                    elif self.word_line_LineEdit.text() == "e":
                        line = "페이지 옆"
                    else:
                        # 입력한 페이지로 저장
                        line = self.word_line_LineEdit.text()

                    # 단어와 페이지, 위치, 뜻을 하나의 문장으로
                    text = self.word_name_LineEdit.text() + "|" + str(page) + "-" + line + "|" + mean

                    print(text)

                    # 저장
                    write_f_name = "./resource/test_word/" + str(page) + ".txt"
                    write_f = open(write_f_name, 'a', encoding='utf-8')
                    write_f.write(text + "\n")
                    self.te.append(text)
                    write_f.close()

                # 아마 마지막 단어일 듯...?
            if int(count) != int(len(data)):
                self.word_name_LineEdit.clear()
                self.word_mean_LineEdit.clear()

                word_name = data[count]
                self.word_mean_ComboBox.clear()

                self.word_name_LineEdit.setText(word_name.split('|')[0])
                self.word_mean_ComboBox.addItems(word_name.strip().split('|')[1:])

                self.persent_label.setText(str(count + 1) + "/" + str(len(data)))

            # 다음 단어로
            count = count + 1

    def buttonDel_check(self):
        # 삭제 버튼시 저장하지 않고 다음 단어로
        self.buttonNext_check(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
