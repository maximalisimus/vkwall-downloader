from .vkconf import *
from .vkclasses import *

__all__ = ['RunningValue', 'open_file_dialog', 'save_file_dialog', 
			'get_credential_service', "SetObjText", "GetObjText", 
			'set_obj_checked', 'get_obj_checked', 'set_obj_enabled']

def RunningValue(value):
	if platform.system() == 'Darwin':
		subprocess.call(('open', value))
	elif platform.system() == 'Windows':
		os.startfile(value)
	else:
		subprocess.call(('xdg-open', value))

def open_file_dialog(parent = None):
	global html_fomr_style
	filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent, html_fomr_style['forms']['dialogs']['open_file']['title'], str(Files.PREFIX.resolve()), html_fomr_style['forms']['dialogs']['open_file']['filter'], html_fomr_style['forms']['dialogs']['open_file']['initial_filter'])
	if filename != None:
		if filename != '':
			return str(pathlib.Path(str(filename)).resolve())
		else:
			return None
	else:
		return None	

def save_file_dialog(parent = None):
	global html_fomr_style
	filename, _ = QtWidgets.QFileDialog.getSaveFileName(parent=parent, caption=html_fomr_style['forms']['dialogs']['save_file']['title'], directory=str(Files.PREFIX.resolve()), filter=html_fomr_style['forms']['dialogs']['save_file']['filter'], initialFilter=html_fomr_style['forms']['dialogs']['save_file']['initial_filter'])
	if filename != None:
		if filename != '':
			return str(pathlib.Path(f"{filename}").resolve())
		else:
			return None
	else:
		return None

def get_credential_service(value: str, default_value: str):
	temp = Passwords.GetPass(value)
	if temp != None:
		return temp
	else:
		return default_value

def SetObjText(forms, obj, text: str):
	obj.setText(forms.translate(forms.form_name, f"{text}"))
	
def GetObjText(obj):
	return obj.text()

def set_obj_checked(obj, value: bool):
	obj.setChecked(value)

def get_obj_checked(obj):
	return obj.isChecked()

def set_obj_enabled(obj, value: bool):
	obj.setEnabled(value)
