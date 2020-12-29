import time, threading, sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt5 import QtGui, uic, QtWidgets
from pynput.mouse import Button, Controller
from pynput.keyboard import KeyCode, Key, Listener
#from pynput import keyboard

qtCreatorFile = 'clicker.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QMainWindow, Ui_MainWindow):
    def keys(self):
        self.f_keys = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12']
        self.f_triggers = [Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6, Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12]

    def checkDelay(self, valueToCheck):
        if valueToCheck.isdecimal() == False:
            return True
        return False

    def clickingButton(self):
        if self.radio_LeftClick.isChecked():
            return Button.left
        else:
            return Button.right

    def middleClick(self):
        return self.check_MiddleClick.isChecked()
            
    def clickDelay(self):
        return self.lineEdit_ClickDelay.text()

    def scrollChoose(self):
        if self.check_ScrollOnly.isChecked():
            return 'only'
        return self.check_Scrolling.isChecked()

    def startStopKey(self):
        startStopKey = self.lineEdit_StartStopKey.text()
        startStopKey = startStopKey.lower()
        lenOfValue = len(startStopKey)
        if lenOfValue == 1:
            startStopKey = KeyCode(char = startStopKey)
        elif startStopKey == '':
            return 'NONE'
        elif lenOfValue >= 2:
            found = 0
            for i in range(0, 12):
                if startStopKey == self.f_keys[i]:
                    startStopKey = self.f_triggers[i]
                    found = 1
                    break
            if found == 0:
                return 'NONE'
        return startStopKey
        
    def exitKey(self):
        exitKey = self.lineEdit_ExitKey.text()
        exitKey = exitKey.lower()
        lenOfValue = len(exitKey)
        if lenOfValue == 1:
            exitKey = KeyCode(char = exitKey)
        elif exitKey == '':
            return 'NONE'
        elif lenOfValue >= 2:
            found = 0
            for i in range(0, 12):
                if exitKey == self.f_keys[i]:
                    exitKey = self.f_triggers[i]
                    found = 1
                    break
            if found == 0:
                return 'NONE'
        return exitKey
        
    def getInputs(self):
        self.keys()
        button = self.clickingButton()
        middle = self.middleClick()
        delay = self.clickDelay()
        startKey = self.startStopKey()
        exitKey = self.exitKey()
        scroll = self.scrollChoose()
        errorMessage = 'Invalid input!'
        
        if self.checkDelay(delay):
            self.lineEdit_ClickDelay.setText(errorMessage)
        else:
            delay = int(delay) / 1000
            
        if startKey == 'NONE':
            self.lineEdit_StartStopKey.setText(errorMessage)
        if exitKey == 'NONE':
            self.lineEdit_ExiKey.setText(errorMessage)
        
        return button, middle, delay, startKey, exitKey, scroll
            
    def startProgram(self):
        button, middle, delay, startKey, exitKey, scroll = self.getInputs()
        
        if startKey == 'NONE' or exitKey == 'NONE' or self.lineEdit_ClickDelay.text() == 'Invalid input!':
            return
        
        class MouseControl(threading.Thread):
            def __init__(self, delay, button, middle, scroll):
                    super().__init__()
                    self.running = False
                    self.program_running = True
                    self.delay = delay
                    self.button = button
                    self.middle = middle
                    self.scroll = scroll

            def start_clicking(self):
                self.running = True
                if self.scroll != 'only':
                    if self.delay == 0:
                        Controller().release(self.button)
                    if self.middle:
                        Controller().release(Button.middle)

            def stop_clicking(self):
                self.running = False
                if self.scroll != 'only':
                    if self.delay == 0:
                        Controller().release(self.button)
                    if self.middle:
                        Controller().release(Button.middle)

            def exit(self):
                self.stop_clicking()
                self.program_running = False
                if self.scroll != 'only':
                    if self.delay == 0:
                        Controller().release(self.button)

            def run(self):
                while self.program_running:
                    while self.running:
                        if self.scroll == False:
                            if self.delay == 0:
                                Controller().press(self.button)
                                time.sleep(0.1)
                            else:
                                Controller().click(self.button)
                                time.sleep(self.delay)
                                if self.middle:
                                    Controller().click(Button.middle)
                                    time.sleep(self.delay)
                        elif self.scroll == 'only':
                            Controller().scroll(0, 1)
                            time.sleep(0.1)
                        elif self.scroll:
                            if self.delay == 0:
                                Controller().press(self.button)
                                Controller().scroll(0, 1)
                                time.sleep(0.1)
                            else:
                                Controller().click(self.button)
                                time.sleep(self.delay)
                                Controller().scroll(0, 1)
                                time.sleep(0.1)
                                if self.middle:
                                    Controller().click(Button.middle)
                                    time.sleep(self.delay)
                                    
        global mouse_thread
        mouse_thread = MouseControl(delay, button, middle, scroll)
        mouse_thread.start()
        
        def on_press(key):
            if key == startKey:
                if mouse_thread.running:
                    mouse_thread.stop_clicking()
                else:
                    mouse_thread.start_clicking()
            elif key == exitKey:
                mouse_thread.exit()
                listener.stop()
                    
        with Listener(on_press = on_press) as listener:
            listener.join()
        
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.startButton.clicked.connect(self.startProgram)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Window = MyApp()
    Window.show()
    sys.exit(app.exec_())
