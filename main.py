from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QPushButton
import sys
import gui
import socket
from threading import *
import time

class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):

	def __init__(self, parent=None):
		super(ExampleApp, self).__init__(parent)
		self.setupUi(self)
		self.lineEdit.setText("verystrongpasswprd")
		self.lineEdit_2.setText("7171")
		self.lineEdit_3.setText("192.168.0.1")
		self.senha = None
		self.ip = None
		self.porta = None
		self.s = None


	def clickMethod(self):
		t1=Thread(target=self.Receive)
		t1.start()


	def sendCommand(self):
		t2=Thread(target=self.Envia)
		t2.start()   		
  
	def Envia(self):
		cmd = (self.lineEdit_4.text()+'\r')	
		self.s.sendall(cmd.encode('utf-8'))
		self.lineEdit_4.setText('')
 
	def Receive(self): 
		self.senha = self.lineEdit.text()+'\r'
		self.ip = self.lineEdit_3.text()
		self.porta = self.lineEdit_2.text()


		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
			host = self.ip
			port = int(self.porta)
			try:
				self.s.connect((host, port)) 
			except:
				dlg = QMessageBox(self)
				dlg.setWindowTitle("Erro de Engano")
				dlg.setText("Sem resposta do servidor")				
				dlg.exec()
			x = (str(self.s.recv(1024), 'utf-8'))
			print(x) 
			self.textEdit.append(x)
			self.s.sendall(self.senha.encode('utf-8'))


			while True:
				data = (str(self.s.recv(1024), 'utf-8'))
				datasplit = data.split()
				try:
					if ((datasplit[1][:7]=="DROPOFF") and (datasplit[3]=="20" ) and (datasplit[4]=="Completed")):
						with open("logFileName.txt", "a") as f:
							f.write(data)
							f.close()
				except:
					None
				print(data)
				self.textEdit.append(data)
				self.textEdit.moveCursor(QtGui.QTextCursor.End)
			if not data: 
				None


def main():

	app = QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	app.exec_()


if __name__ == '__main__':

	main()

