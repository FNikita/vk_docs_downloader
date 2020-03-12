from PyQt5 import QtWidgets, QtCore
from window import Ui_Form  
import sys
import vk_api
import requests
 
 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.linePassword.setEchoMode(QtWidgets.QLineEdit.Password)

        #self.ui.linePassword.setStyleSheet("background-color: rgb(28, 43, 255);")

        self.ui.pushButton.clicked.connect(self.resizeWindow)

    def log_in(self):
        login_str = self.ui.lineLogin_2.text()
        password_str = self.ui.linePassword.text()

        vkObj = vk_api.VkApi(login=login_str, password=password_str)

        try:
            vkObj.auth()
        except:
            self.ui.linePassword.setStyleSheet("background-color: rgb(28, 43, 255);")
        else:
            api = vkObj.get_api()
            self.documents = api.docs.get()["items"]
        self.clear_window()
        self.setGeometry(QtCore.QRect(0, 0, 500, 600))
        self.create_FormLayout()

    def clear_window(self):    
        items_list = self.findChildren(QtWidgets.QLineEdit)
        items_list.append(self.findChildren(QtWidgets.QLabel)[0])
        items_list.append(self.findChildren(QtWidgets.QLabel)[1])
        items_list.append(self.findChildren(QtWidgets.QPushButton)[0])
        
        for it in items_list:
            it.deleteLater()
       

    def resizeWindow(self):
        self.log_in()
        


    def create_FormLayout(self):
        layout = QtWidgets.QGridLayout()
        layout.setGeometry(QtCore.QRect(0, 0, 400, 550))
        for i in range(10):
            lable = QtWidgets.QLabel(self.documents[i]["title"])
            button = QtWidgets.QPushButton("download")
            button.setObjectName("btn"+str(i))
            button.clicked.connect(self.Download)
            layout.addWidget(lable, i, 0)
            layout.addWidget(button, i,1)


        group = QtWidgets.QGroupBox("Documents")
        group.setLayout(layout)
        self.ui.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 490, 500))
        group.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.ui.formLayout.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.ui.formLayout.addWidget(group)
        
        self.ui.formLayout = layout


    def Download(self):
        index = int(self.sender().objectName()[3:])
        el = self.documents[index]
        r = requests.get(el["url"])

        if r.status_code == 200:
            with open(el["title"], "wb") as output_file:
                output_file.write(r.content)

 
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
 
sys.exit(app.exec())