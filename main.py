import sys
import sqlite3
import sqlite3 as lite
import random
from PIL import Image, ImageDraw, ImageFilter
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, uic


# Окно ВХОДА\РЕГИСТРАЦИИ
class Register(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('qt/register.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Окно входа')
        self.em = MainWindow()
        self.em.hide()

        # установка иконки
        self.pixmap = QPixmap('media/icon.jpg')
        self.lb_icon.setPixmap(self.pixmap)

        self.enter_denied.hide()
        self.label.hide()
        self.label2.hide()
        self.label3.hide()

        self.btn_changing.clicked.connect(self.run2)
        self.btn_inform.clicked.connect(self.run1)
        self.btn.clicked.connect(self.run)
        self.btn_tabl.clicked.connect(self.run3)

        # спрятать\показать строки подтверждения
        self.func = lambda x: x.show() if x.isHidden() else x.hide()
        self.rb_enter.toggled.connect(lambda: self.func(self.lb_pw2))
        self.rb_enter.toggled.connect(lambda: self.func(self.passw2))

        # подключение модуля ЗАПОМНИТЬ МЕНЯ
        con = sqlite3.connect("db/remember.db")
        cur = con.cursor()
        log = cur.execute('''SELECT login FROM info''').fetchall()

        for elem in log:
            self.login.setText(elem[0])
        pas = cur.execute('''SELECT password FROM info''').fetchall()

        for elem in pas:
            self.passw1.setText(elem[0])

        con.commit()
        con.close()

    #Открытие Таблицы Рекордов
    def run3(self):
        self.hide()
        ex.show()

    # модуль открытия окна Смены пароля
    def run2(self):
        ch.show()
        self.hide()

    #модуль открытия окна Информации
    def run1(self):
        inf.show()
        self.hide()

    #модуль запуска
    def run(self):
        if self.rb_register.isChecked():
            self.register()

        elif self.rb_enter.isChecked():
            if self.cb_rem.isChecked():
                self.remember()
            else:
                self.enter()



    # реализация модуля ЗАПОМНИТЬ МЕНЯ
    def remember(self):
        if self.passw1.text() == '' or self.login.text() == '':
            self.label2.show()
        else:
            self.label2.hide()

            log = self.login.text()
            pas = self.passw1.text()

            self.enter()

            con = sqlite3.connect("db/remember.db")
            cur = con.cursor()
            cur.execute(f'INSERT INTO info(login, password) VALUES("{log}","{pas}")')

            con.commit()
            con.close()

    # реализация модуля РЕГИСТРАЦИЯ
    def register(self):
        if self.passw1.text() == '' or self.login.text() == '' or self.passw2.text() == '':
            self.label2.show()
        else:
            self.label2.hide()
            if self.passw1.text() != self.passw2.text():
                self.label3.show()
                self.label2.hide()
            else:
                self.label3.hide()

                log = self.login.text()
                pas = self.passw1.text()

                # подключение необходимой БД
                con = sqlite3.connect("db/log_pas.db")
                cur = con.cursor()
                cur.execute(f'INSERT INTO info(login, password) VALUES("{log}","{pas}")')

                con.commit()
                con.close()

                self.label.show()

    # Реализация модуля ВХОД
    def enter(self):
        if self.passw1.text() == '' or self.login.text() == '':
            self.label2.show()
        else:

            self.label2.hide()
            global log
            log = self.login.text()
            pas = self.passw1.text()

            # очищение необходимой БД
            con = sqlite3.connect("db/remember.db")
            cur = con.cursor()
            cur.execute("""DELETE from info""").fetchall()

            con.commit()
            con.close()

            # подключение необходимой БД
            con = sqlite3.connect("db/log_pas.db")
            cur = con.cursor()
            result_login = cur.execute(f"""SELECT login FROM info""").fetchall()
            for elem in result_login:
                if log == elem[0]:
                    result = cur.execute(f"""SELECT password FROM info
                                                    WHERE login = "{log}" """).fetchone()
                    if pas in result:
                        em.show()
                        er.hide()

            con.close()

            if log not in result_login:
                self.enter_denied.show()
            else:
                result = cur.execute(f"""SELECT password FROM info
                                    WHERE login = "{log}" """).fetchone()
                print(result)
                if pas in result:
                    self.check_rem()
                else:
                    self.enter_denied.show()

            con.close()

#Окно С таблицей рекордов
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('qt/UI1.ui', self)
        self.connection = sqlite3.connect("db/log_pas.db")
        self.btn_revers.clicked.connect(self.run1)
        # По умолчанию будем выводить все данные из таблицы films
        self.textEdit.setPlainText("SELECT login, time4, time5, time6 FROM info")
        # Получим результат запроса,
        # который ввели в текстовое поле
        query = self.textEdit.toPlainText()
        res = self.connection.cursor().execute(query).fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        # При закрытии формы закроем и наше соединение
        # с базой данных
        self.connection.close()

    def run1(self):
        er.show()
        self.hide()

# Игровое окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('qt/tabel.ui', self)
        self.setWindowTitle('Игровое окно')
        self.btn_revers.clicked.connect(self.run1)
        self.btn_gener.clicked.connect(self.run)
        self.btn_restart.clicked.connect(self.restart)

        self.counter = 0
        self.minutes = '00'
        self.seconds = '00'
        self.miliseconds = '00'
        self.startWatch = False

        self.label = QLabel(self)
        self.label.setGeometry(10, 550, 150, 70)

        self.start = QPushButton("Start", self)
        self.start.setGeometry(0, 0, 1, 1)
        self.start.pressed.connect(self.Start)

        # Модуль отвычающий за таймер
        timer = QTimer(self)
        timer.timeout.connect(self.showCounter)
        timer.start(100)

    def run1(self):
        er.show()
        self.hide()

    # модуль рестрата
    def restart(self):
        self.startWatch = False
        self.counter = 0
        self.minutes = '00'
        self.seconds = '00'
        self.miliseconds = '00'
        self.label.setText(str(self.counter))

        for i in range(len(self.buttons)):
            self.buttons[i].hide()

    def run(self):
        if self.rb4.isChecked():
            self.gen4()
        elif self.rb5.isChecked():
            self.gen5()
        elif self.rb6.isChecked():
            self.gen6()

    # модуль проверки правильности нажатия
    def checking(self, name):
        if int(name.text()) == 1:
            self.Start()

        if self.cor_values.index(int(name.text())) == 0:
            name.hide()
            self.cor_values.remove(int(name.text()))

            if self.rb4.isChecked() and int(name.text()) == 16:
                self.timerbd4()
                self.Start()
            elif self.rb5.isChecked() and int(name.text()) == 25:
                self.timerbd5()
                self.Start()
            elif self.rb6.isChecked() and int(name.text()) == 36:
                self.timerbd6()
                self.Start()
    #внос рекорда в БД
    def timerbd4(self):
        global log
        # подключение необходимой БД
        con = sqlite3.connect("db/log_pas.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT time4 FROM info 
                                WHERE login = "{log}" """).fetchone()
        for elem in result:
            k = elem

        if k == None:
            con = sqlite3.connect("db/log_pas.db")
            cur = con.cursor()
            cur.execute(f"""UPDATE info SET time4 = "{self.counter}" WHERE login = "{log}" """)
            con.commit()
        else:
            if self.counter < int(elem):
                con = sqlite3.connect("db/log_pas.db")
                cur = con.cursor()
                cur.execute(f"""UPDATE info SET time4 = "{self.counter}" WHERE login = "{log}" """)
                con.commit()
            else:
                pass

        # внос рекорда в БД
    def timerbd5(self):
        global log
        # подключение необходимой БД
        con = sqlite3.connect("db/log_pas.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT time5 FROM info 
                                    WHERE login = "{log}" """).fetchone()
        for elem in result:
            k = elem

        if k == None:
            con = sqlite3.connect("db/log_pas.db")
            cur = con.cursor()
            cur.execute(f"""UPDATE info SET time5 = "{self.counter}" WHERE login = "{log}" """)
            con.commit()
        else:
            if self.counter < int(elem):
                con = sqlite3.connect("db/log_pas.db")
                cur = con.cursor()
                cur.execute(f"""UPDATE info SET time5 = "{self.counter}" WHERE login = "{log}" """)
                con.commit()
            else:
                pass

        # внос рекорда в БД
    def timerbd6(self):
        global log
        # подключение необходимой БД
        con = sqlite3.connect("db/log_pas.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT time6 FROM info 
                                    WHERE login = "{log}" """).fetchone()
        for elem in result:
            k = elem

        if k == None or len(result) == 0:
            con = sqlite3.connect("db/log_pas.db")
            cur = con.cursor()
            cur.execute(f"""UPDATE info SET time6 = "{self.counter}" WHERE login = "{log}" """)
            con.commit()
        else:
            if self.counter < int(elem):
                con = sqlite3.connect("db/log_pas.db")
                cur = con.cursor()
                cur.execute(f"""UPDATE info SET time6 = "{self.counter}" WHERE login = "{log}" """)
                con.commit()
            else:
                pass



    # генерация поля 4х4
    def gen4(self):
        self.values = []
        self.cor_values = []
        self.buttons = []

        for i in range(16):
            self.values.append(i + 1)
            self.cor_values.append(i + 1)

        j, k, l = 0, 0, 0

        for i in range(16):
            text = int(random.choice(self.values))
            text1 = str(text)

            self.btn = QPushButton(text1, self)
            self.btn.setFixedSize(93, 93)

            # вторая колонка
            if k == 4:
                j = 1
                k = 0
            # третья колонка
            if l == 1:
                j = 2
                k = 0
            # четвертая колонка
            if l == 2:
                j = 3
                k = 0
            x = (j + 1) * 93
            y = (k + 1) * 93

            k += 1
            l += 0.25

            self.btn.move(x, y)
            self.btn.show()
            self.btn.setStyleSheet('border-style: outset;'
                                   'background-color: rgb(194, 255, 129);'
                                   'border-width: 1px;'
                                   'border-radius: 5px;'
                                   'border-color: black;'
                                   'padding: 1px;'
                                   'font-size: 14pt;')
            self.btn.clicked.connect(lambda ch, p=self.btn: self.checking(p))

            self.buttons.append(self.btn)
            self.values.remove(text)

    # генерация поля 5х5
    def gen5(self):
        self.values = []
        self.cor_values = []
        self.buttons = []

        for i in range(25):
            self.values.append(i + 1)
            self.cor_values.append(i + 1)

        j, k, l = 0, 0, 0

        for i in range(25):
            text = int(random.choice(self.values))
            text1 = str(text)

            self.btn = QPushButton(text1, self)
            self.btn.setFixedSize(93, 93)
            # вторая колонка
            if k == 5:
                j = 1
                k = 0
            # третья колонка
            if l == 1:
                j = 2
                k = 0
            # четвертая колонка
            if l == 1.9999999999999998:
                j = 3
                k = 0
            # пятая колонка
            if l == 3.0000000000000004:
                j = 4
                k = 0

            x = (j + 1) * 93
            y = (k + 1) * 93

            k += 1
            l += 0.2

            self.btn.move(x, y)
            self.btn.show()
            self.btn.setStyleSheet('border-style: outset;'
                                   'background-color: rgb(194, 255, 129);'
                                   'border-width: 1px;'
                                   'border-radius: 5px;'
                                   'border-color: black;'
                                   'padding: 1px;'
                                   'font-size: 14pt;')
            self.btn.clicked.connect(lambda ch, p=self.btn: self.checking(p))

            self.buttons.append(self.btn)
            self.values.remove(text)

    # Генерация поля 6х6
    def gen6(self):
        self.values = []
        self.cor_values = []
        self.buttons = []

        for i in range(36):
            self.values.append(i + 1)
            self.cor_values.append(i + 1)

        j, k, l = 0, 0, 0

        for i in range(36):
            text = int(random.choice(self.values))
            text1 = str(text)

            self.btn = QPushButton(text1, self)
            self.btn.setFixedSize(80, 80)
            # вторая колонка
            if k == 6:
                j = 1
                k = 0
            # третья колонка
            if l == 0.6:
                j = 2
                k = 0
            # четвертая колонка
            if l == 1.2:
                j = 3
                k = 0
            # пятая колонка
            if l == 1.8000000000000005:
                j = 4
                k = 0
            # шестая колонка
            if l == 2.400000000000001:
                j = 5
                k = 0

            x = (j + 1) * 80
            y = (k + 1) * 80

            k += 1
            l += 0.1

            self.btn.move(x, y)
            self.btn.show()
            self.btn.setStyleSheet('border-style: outset;'
                                   'background-color: rgb(194, 255, 129);'
                                   'border-width: 1px;'
                                   'border-radius: 5px;'
                                   'border-color: black;'
                                   'padding: 1px;'
                                   'font-size: 14pt;')
            self.btn.clicked.connect(lambda ch, p=self.btn: self.checking(p))

            self.buttons.append(self.btn)
            self.values.remove(text)

    # Реализация модуля ТАЙМЕР
    def showCounter(self):
        if self.startWatch:
            # перевод в милисекунды
            self.counter += 1
            cntr = int((self.counter / 10 - int(self.counter / 10)) * 10)
            self.miliseconds = '0' + str(cntr)
            # перевод на секунды
            if int(self.counter / 10) < 10:
                self.seconds = '0' + str(int(self.counter / 10))
            else:
                self.seconds = str(int(self.counter / 10))
            # перевод на минуты
            if self.counter / 10 == 60.0:
                self.seconds = '00'
                self.counter = '00'
                min = int(self.minutes) + 1

                if min < 10:
                    self.minutes = '00' + str(min)
                else:
                    self.minutes = str(min)

        # вывод на секундомер
        self.text = self.minutes + ':' + self.seconds + ':' + self.miliseconds

        self.label.setText(self.text)
        # установка цвета
        self.label.setText('<h1 style = "color:blue" >' + self.text + '< /h1 >')

    # модуль СТРАТ\СТОП таймера
    def Start(self):
        if self.start.text() == 'Stop':
            self.start.setText('Resume')
            self.startWatch = False
        else:
            self.startWatch = True
            self.start.setText('Stop')


# Окно СМЕНЫ ПАРОЛЯ
class Change(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('qt/change.ui', self)
        self.initUI()

    def initUI(self):
        self.btn_revers.clicked.connect(self.run1)
        self.enter_denied.hide()
        self.label2.hide()
        self.label3.hide()
        self.label_5.hide()

        self.setWindowTitle('Окно смены пароля')
        self.btn_go.clicked.connect(self.run)

    def run1(self):
        er.show()
        self.hide()
    #основной модуль запуска
    def run(self):
        if self.passw1.text() == '' or self.login.text() == '' \
                or self.passw2.text() == '' or self.passw3.text() == '':
            self.label2.show()
        else:
            self.label2.hide()

            log = self.login.text()
            pas = self.passw1.text()

            # подключение необходимой БД
            con = sqlite3.connect("db/log_pas.db")
            cur = con.cursor()
            result_login = cur.execute(f"""SELECT login FROM info""").fetchall()
            for elem in result_login:
                if log == elem[0]:
                    result = cur.execute(f"""SELECT password FROM info
                                                    WHERE login = "{log}" """).fetchone()
                    if pas in result:
                        if self.passw3.text() != self.passw2.text():
                            self.label3.show()
                            self.label2.hide()
                        else:
                            self.label3.hide()

                            log = self.login.text()
                            pas = self.passw1.text()
                            pas1 = self.passw3.text()

                            # подключение необходимой БД
                            con = sqlite3.connect("db/log_pas.db")
                            cur = con.cursor()

                            # удаление старых данных
                            cur.execute('DELETE from info WHERE login LIKE {} AND password LIKE {}'.format(log, pas))
                            # добавление новых
                            cur.execute(f'INSERT INTO info(login, password) VALUES("{log}","{pas1}")')

                            con.commit()
                            con.close()
                            self.label_5.show()
                            self.hide()
                            er.show()

            con.close()

            if log not in result_login:
                self.enter_denied.show()
            else:
                result = cur.execute(f"""SELECT password FROM info
                                    WHERE login = "{log}" """).fetchone()
                print(result)
                if pas in result:
                    self.check_rem()
                else:
                    self.enter_denied.show()

            con.close()

#Окно ИНФОРМАЦИИ
class Inform(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('qt/inform.ui', self)
        self.initUI()

    def run1(self):
        er.show()
        self.hide()

    def initUI(self):
        self.btn_revers.clicked.connect(self.run1)
        self.setWindowTitle('Информация')

        self.label = QLabel(self)
        self.label.move(1, 1)
        self.label.setFixedSize(501, 370)
        self.label.setStyleSheet("QLabel{font-size: 9.5pt;}")
        self.label.setText("Таблица Шульте - таблица случайно расположенных чисел, \n"
                           "обычно размером 5x5 элементов и обычно состоит из цифр. \n"
                           "Но тут вы сможете попробывать и другие режимы\n"
                           "Это упражнение способствует развитию скорочтения,\n "
                           "потому что улучшает периферийное зрение,\n "
                           "так же помогает развивать память.\n"
                           "Таблицу Шульте необходимо проходить смотря строго \n"
                           "в центр таблицы и периферийным, боковым зрением находить \n"
                           "цифры или буквы в порядке их возрастания. Это вам такой совет :) \n"
                           "Чем быстрее будут найдены все цифры или буквы в порядке их возрастания, тем лучше. \n"
                           "Во время прохождения упражнения , лучше ничего не проговаривать про себя.\n"
                           "Так как это может пагубно повлиять на результат\n"
                           "Эти упражнения способствуют развитию развитию интеллекта \n"
                           " и скорочтения. Также для достижения результата \n"
                           "необходимо тренироваться каждый день, но будьте аккуратны. \n"
                           "Когда замечаете, что скорость выполнения\n"
                           " упражнения падает следует прекратить тренировку и отдохнуть, \n"
                           "потом приступить снова. \n"
                           "Играйте и наслаждайтесь ;)\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    er = Register()
    em = MainWindow()
    ch = Change()
    inf = Inform()
    ex = Example()
    er.show()
    sys.exit(app.exec())
