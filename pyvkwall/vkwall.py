from .vkforms import *

def run():	
	app = QApplication([])
	main_form = MainForm()
	main_form.show()
	app.exec()

