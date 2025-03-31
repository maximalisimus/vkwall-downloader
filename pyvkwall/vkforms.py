from .vkclasses import *
from .vkfunc import *

class DefaultWidget(QWidget):
	
	def __init__(self, form_name: str):
		super().__init__()
		self.translate = QtCore.QCoreApplication.translate
		self.form_name = form_name

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	
	def clicked_connected(self, obj, func):
		obj.clicked.connect(func)
	
	def set_obj_icon(self, the_obj, icon_link: str):
		icon_obj = QtGui.QIcon()
		icon_obj.addPixmap(QtGui.QPixmap(str(pathlib.Path(f"{icon_link}"))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		the_obj.setIcon(icon_obj)

	def set_window_icon(self, icon_link: str):
		icon_win = QtGui.QIcon()
		icon_win.addPixmap(QtGui.QPixmap(str(pathlib.Path(f"{icon_link}"))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(icon_win)
		
	def set_title(self, title: str):
		self.setWindowTitle(self.translate(self.form_name, f"{title}"))

	def set_obj_text(self, obj, text: str):
		SetObjText(self, obj, text)
	
	def get_obj_text(self, obj):
		return GetObjText(obj)
	
	def set_geometry(self, left: int, top: int, width: int, height: int):
		self.setGeometry(left, top, width, height)
	
	def set_window_size(self, width: int, height: int):
		self.resize(width, height)

	def set_minimum_size(self, width: int, height: int):
		self.setMinimumSize(QtCore.QSize(width, height))

	def set_base_size(self, width: int, height: int):
		self.setBaseSize(QtCore.QSize(width, height))

	def set_maximum_size(self, width: int, height: int):
		self.setMaximumSize(QtCore.QSize(width, height))

class DefaultForms(DefaultWidget):
	
	def __init__(self, form_ui: str, form_name: str, style_name: str, parent = None):
		super(DefaultForms, self).__init__(form_name)
		uic.loadUi(str(pathlib.Path(str(form_ui)).resolve()), self)
		self.style_name = style_name
		self.parent = parent
		self.clipboard = QApplication.clipboard()

	def ReturnParent(self):
		if self.parent != None:
			self.parent.setEnabled(True)

	def closeEvent(self, event):
		self.ReturnParent()
		event.accept()

	def form_show(self):
		self.clear_clicked()
		self.center()
		self.show()

	def clear_clicked(self):
		global is_btn_clicked
		is_btn_clicked = False

class TokenForm(DefaultForms):
	
	def __init__(self, init_obj = None):
		global icon_settings, html_fomr_style
		super(TokenForm, self).__init__(html_fomr_style['form_ui']['token']['file_name'], html_fomr_style['form_ui']['token']['form_name'], 'token', init_obj)
		self.set_default_config()
		self.clicked_connected(self.button_prev, self.PrevClicked)
		self.clicked_connected(self.button_next, self.NextClicked)
	
	def set_default_config(self):
		global icon_settings, html_fomr_style
		self.set_title(html_fomr_style['forms'][self.style_name]['title'])
		self.set_window_icon(html_fomr_style['forms'][self.style_name]['icon_form'])
		self.set_obj_icon(self.button_prev, html_fomr_style['forms'][self.style_name]['icon_no'])
		self.set_obj_icon(self.button_next, html_fomr_style['forms'][self.style_name]['icon_ok'])
		self.set_obj_text(self.text_label, html_fomr_style['forms'][self.style_name]['text'])
		self.set_obj_text(self.button_prev, html_fomr_style['forms'][self.style_name]['btn_no'])
		self.set_obj_text(self.button_next, html_fomr_style['forms'][self.style_name]['btn_ok'])
		self.set_geometry(html_fomr_style['forms'][self.style_name]['sizes']['geometry']['x'], html_fomr_style['forms'][self.style_name]['sizes']['geometry']['y'], html_fomr_style['forms'][self.style_name]['sizes']['geometry']['width'], html_fomr_style['forms'][self.style_name]['sizes']['geometry']['height'])
		self.set_minimum_size(html_fomr_style['forms']['token']['sizes']['minimum_size']['width'], html_fomr_style['forms'][self.style_name]['sizes']['minimum_size']['height'])
		self.set_maximum_size(html_fomr_style['forms'][self.style_name]['sizes']['maximum_size']['width'], html_fomr_style['forms'][self.style_name]['sizes']['maximum_size']['height'])
		self.set_base_size(html_fomr_style['forms'][self.style_name]['sizes']['base_size']['width'], html_fomr_style['forms'][self.style_name]['sizes']['base_size']['height'])
		self.text_label.setMinimumSize(QtCore.QSize(html_fomr_style['forms'][self.style_name]['sizes']['text_label']['width'], html_fomr_style['forms'][self.style_name]['sizes']['text_label']['height']))
		self.text_label.adjustSize()
		self.text_label.setWordWrap(True)

	def PrevClicked(self):
		self.ReturnParent()
		self.hide()
	
	def NextClicked(self):
		global html_fomr_style
		self.clipboard.setText(html_fomr_style['url'])
		webbrowser.open(html_fomr_style['url'])

class VersionForm(TokenForm):
	
	def __init__(self, init_obj = None):
		global icon_settings, html_fomr_style
		super(VersionForm, self).__init__(init_obj)
		self.style_name = "version"
		self.set_default_config()
	
	def NextClicked(self):
		global html_fomr_style
		self.clipboard.setText(html_fomr_style['version_url'])
		webbrowser.open(html_fomr_style['version_url'])

class PostThread(QThread):
	# Create a counter thread
	change_value = pyqtSignal(int)
	
	def __init__(self, the_dataset, the_config):
		super().__init__()
		self.the_dataset = the_dataset
		self.the_config = the_config

	def run(self):
		posts = Files.read_write_json(str(self.the_dataset.downloaddir.joinpath(Defaults.post_file_name)), 'r')
		VKAPI.PostsProcess(self.the_config, posts, self.change_value)

class WaitThread(QThread):
	
	def __init__(self, pbar, func):
		super().__init__()
		self.pbar = pbar
		self.fine_func = func
	
	def run(self):
		while True:
			QtCore.QThread.sleep(1)
			value = self.pbar()
			if value >= 99:
				self.fine_func()
				break

class MainForm(DefaultWidget):
	
	def __init__(self):
		global icon_settings, html_fomr_style, default_config, progress_bar
		super(MainForm, self).__init__(html_fomr_style['form_ui']['main']['form_name'])
		uic.loadUi(str(pathlib.Path(str(html_fomr_style['form_ui']['main']['file_name'])).resolve()), self)
		self.is_view_no_view = False
		
		self.progress_bar.setMaximum(100)
		self.progress_bar.setMinimum(0)
		self.INITDefaultStyleConfig()
		self.BuildForm()		
		self.center()

	def BuildForm(self):
		self.INITPrimary()
		self.INITSecondary()
		self.button_connected()
		self.setValidatorses()
	
	def setValidatorses(self):
		self.regex_offset = QRegExp("[0-9]+")
		self.validator_offset = QRegExpValidator(self.regex_offset)
		self.offset_text.setValidator(self.validator_offset)
		
		self.regex_ownerid = QRegExp("-[0-9]+")
		self.validator_ownerid = QRegExpValidator(self.regex_ownerid)
		self.ownerid_text.setValidator(self.validator_ownerid)
		
		self.regex_count_posts = QRegExp("[0-9]+")
		self.validator_count_posts = QRegExpValidator(self.regex_count_posts)
		self.count_posts_text.setValidator(self.validator_count_posts)
		
	def set_obj_param(self, obj, style):
		global html_fomr_style
		self.set_obj_text(obj, html_fomr_style['forms']['main'][style]['title'])
		if "_button" in style:
			self.set_obj_icon(obj, html_fomr_style['forms']['main'][style]['icon'])
	
	def StyleApply(self):
		global icon_settings, html_fomr_style
		self.set_window_icon(html_fomr_style['forms']['main']['forms']['icon'])
		self.set_title(html_fomr_style['forms']['main']['forms']['title'])
		for k in html_fomr_style['forms']['main'].keys():
			if k != 'forms':
				if k in self.__dict__:
					self.set_obj_param(self.__dict__[k], k)
	
	def INITMainConfig(self):
		global icon_settings, html_fomr_style, default_config
		if Files.config_file.exists():
			self.config = Files.read_write_json(Files.config_file, 'r')
		else:
			self.config = Files.STRToJSON(Files.JSONToSTR(default_config))
	
	def INITDefaultStyleConfig(self):
		global icon_settings, html_fomr_style
		self.default_style_config = dict()
		self.default_style_config['icon_settings'] = Files.STRToJSON(Files.JSONToSTR(icon_settings))
		self.default_style_config['html_fomr_style'] = Files.STRToJSON(Files.JSONToSTR(html_fomr_style))
	
	def INITStyleConfig(self):
		global icon_settings, html_fomr_style, default_config
		if Files.style_config_file.exists():
			self.style_config = Files.read_write_json(Files.style_config_file, 'r')
		else:
			self.style_config = dict()
			self.style_config['icon_settings'] = Files.STRToJSON(Files.JSONToSTR(icon_settings))
			self.style_config['html_fomr_style'] = Files.STRToJSON(Files.JSONToSTR(html_fomr_style))
		icon_settings = Files.STRToJSON(Files.JSONToSTR(self.style_config['icon_settings']))
		html_fomr_style = Files.STRToJSON(Files.JSONToSTR(self.style_config['html_fomr_style']))
	
	def INITINIConfig(self, ini_file = None):
		global icon_settings, html_fomr_style, default_config
		if ini_file != None:
			ini_file_conf = pathlib.Path(str(ini_file)).resolve()
			if ini_file_conf.exists():
				self.ini_config = Files.read_write_json(ini_file_conf, 'r')
			else:
				self.ini_config = dict()
				for i in Defaults.main_config:
					self.ini_config[i] = ''
				for i in Defaults.secret_config:
					self.ini_config[i] = ''
				self.ini_config[Defaults.main_config[-2]] = False
				self.ini_config[Defaults.main_config[-1]] = True
		else:
			if Files.ini_config_file.exists():
				self.ini_config = Files.read_write_json(Files.ini_config_file, 'r')
			else:
				self.ini_config = dict()
				for i in Defaults.main_config:
					self.ini_config[i] = ''
				for i in Defaults.secret_config:
					self.ini_config[i] = ''
				self.ini_config[Defaults.main_config[-2]] = False
				self.ini_config[Defaults.main_config[-1]] = True
	
	def INITPrimary(self):
		global icon_settings, html_fomr_style, default_config
		self.INITMainConfig()
		self.INITStyleConfig()
		self.INITINIConfig()
		self.StyleApply()
		self.dataset = DataSet(downloaddir = './download', DateStop = '01.01.2010')
		self.old_resized = self.dataset.isresized
	
	def INITSecondary(self):
		self.token_form = TokenForm(self)
		self.version_form = VersionForm(self)
		self.version_form.set_default_config()

	def button_connected(self):
		self.clicked_connected(self.view_button, self.ViewNoViewBTNClicked)
		self.clicked_connected(self.help_button, self.HelpBTNClicked)
		self.clicked_connected(self.selectdir_button, self.SelectDirBTNClicked)
		self.clicked_connected(self.opendir_button, self.OpenDirBTNClicked)
		self.clicked_connected(self.delete_button, self.DeleteBTNClicked)
		self.clicked_connected(self.refresh_button, self.RefreshBTNClicked)
		self.clicked_connected(self.apply_button, self.ApplyBTNClicked)
		self.clicked_connected(self.savefile_button, self.SaveFileBTNClicked)
		self.clicked_connected(self.loadfile_button, self.LoadFileBTNClicked)
		self.clicked_connected(self.saveconf_button, self.SaveConfBTNClicked)
		self.clicked_connected(self.loadconf_button, self.LoadConfBTNClicked)
		self.clicked_connected(self.allclear_button, self.AllClearBTNClicked)
		self.clicked_connected(self.clear_button, self.ClearBTNClicked)
		self.clicked_connected(self.resetconf_button, self.ResetConfBTNClicked)
		self.clicked_connected(self.receive_button, self.ReceiveBTNClicked)
		self.clicked_connected(self.download_button, self.DownloadBTNClicked)
		self.clicked_connected(self.receive_data_button, self.ReceiveDataBTNClicked)
		self.clicked_connected(self.version_button, self.VersionBTNClicked)

	def ViewNoViewBTNClicked(self):
		global icon_settings
		self.is_view_no_view = not self.is_view_no_view
		if self.is_view_no_view:
			self.token_text.setEchoMode(QLineEdit.Normal)
			self.set_obj_icon(self.view_button, icon_settings['notview'])
		else:
			self.token_text.setEchoMode(QLineEdit.Password)
			self.set_obj_icon(self.view_button, icon_settings['view'])

	def HelpBTNClicked(self):
		self.setEnabled(False)
		self.token_form.form_show()
	
	def SelectDirBTNClicked(self):
		global html_fomr_style
		fdir = QFileDialog.getExistingDirectory(None, html_fomr_style['forms']['dialogs']['select_folder']['title'], '')
		if fdir != None:
			if fdir != '':
				self.set_obj_text(self.downloaddir_text, f"{Files.relative_path(fdir, Files.PREFIX)}/")
	
	def OpenDirBTNClicked(self):
		RunningValue(str(pathlib.Path(str(self.downloaddir_text.text())).resolve()))
	
	def ApplyCheckers(self):
		self.ini_config[Defaults.main_config[5]] = get_obj_checked(self.resized_checker)
		self.ini_config[Defaults.main_config[6]] = get_obj_checked(self.saveurl_checker)
		self.dataset.isresized = get_obj_checked(self.resized_checker)	
	
	def ApplyConfig(self):
		self.config[Defaults.secret_config[0]] = f"{self.get_obj_text(self.token_text)}"
		self.config[Defaults.secret_config[1]] = f"{self.get_obj_text(self.domain_text)}"
		self.config[Defaults.secret_config[2]] = f"{self.get_obj_text(self.ownerid_text)}"
		self.config[Defaults.main_config[1]] = f"{self.get_obj_text(self.version_text)}"
		self.config[Defaults.main_config[2]] = int(f"{self.get_obj_text(self.count_posts_text)}")
		self.config[Defaults.main_config[3]] = int(f"{self.get_obj_text(self.offset_text)}")
		self.dataset.downloaddir = f"{self.get_obj_text(self.downloaddir_text)}"
		self.dataset.datetrack.date_stop = f"{self.get_obj_text(self.datastop_text)}"
		self.dataset.ConvertDownloadDir()
		self.ApplyCheckers()
	
	def TextOnConfig(self):
		self.ini_config[Defaults.secret_config[0]] = str(Texts.StrToBase(f"{self.get_obj_text(self.token_text)}"))
		self.ini_config[Defaults.secret_config[1]] = str(Texts.StrToBase(f"{self.get_obj_text(self.domain_text)}"))
		self.ini_config[Defaults.secret_config[2]] = str(Texts.StrToBase(f"{self.get_obj_text(self.ownerid_text)}"))
		self.ini_config[Defaults.main_config[0]] = f"{self.get_obj_text(self.downloaddir_text)}"
		self.ini_config[Defaults.main_config[1]] = f"{self.get_obj_text(self.version_text)}"
		self.ini_config[Defaults.main_config[2]] = int(f"{self.get_obj_text(self.count_posts_text)}")
		self.ini_config[Defaults.main_config[3]] = int(f"{self.get_obj_text(self.offset_text)}")
		self.ini_config[Defaults.main_config[4]] = f"{self.get_obj_text(self.datastop_text)}"
		self.ini_config[Defaults.main_config[5]] = get_obj_checked(self.resized_checker)
		self.ini_config[Defaults.main_config[6]] = get_obj_checked(self.saveurl_checker)
		self.ApplyConfig()
	
	def ConfigOnText(self):
		self.set_obj_text(self.token_text, str(Texts.BaseToSTR(self.ini_config[Defaults.secret_config[0]])))
		self.set_obj_text(self.domain_text, str(Texts.BaseToSTR(self.ini_config[Defaults.secret_config[1]])))
		self.set_obj_text(self.ownerid_text, Texts.BaseToSTR(self.ini_config[Defaults.secret_config[2]]))
		self.set_obj_text(self.downloaddir_text, f"{self.ini_config[Defaults.main_config[0]]}")
		self.set_obj_text(self.version_text, f"{self.ini_config[Defaults.main_config[1]]}")
		self.set_obj_text(self.count_posts_text, f"{self.ini_config[Defaults.main_config[2]]}")
		self.set_obj_text(self.offset_text, f"{self.ini_config[Defaults.main_config[3]]}")
		self.set_obj_text(self.datastop_text, f"{self.ini_config[Defaults.main_config[4]]}")
		set_obj_checked(self.resized_checker, self.ini_config[Defaults.main_config[5]])
		set_obj_checked(self.saveurl_checker, self.ini_config[Defaults.main_config[6]])		
		self.ApplyConfig()
	
	def ApplyBTNClicked(self):
		self.TextOnConfig()
	
	def SaveFileBTNClicked(self):
		global icon_settings, html_fomr_style
		msg = QMessageBox.question(self, html_fomr_style['forms']['savefile']['title'], html_fomr_style['forms']['savefile']['text'], QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		if msg == QMessageBox.StandardButton.Yes:
			save_file = save_file_dialog(self)
			if save_file != None:
				self.TextOnConfig()
				Files.read_write_text(save_file, 'w', Files.JSONToSTR(self.ini_config))

	def LoadFileBTNClicked(self):
		global icon_settings, html_fomr_style
		msg = QMessageBox.question(self, html_fomr_style['forms']['loadfile']['title'], html_fomr_style['forms']['loadfile']['text'], QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		if msg == QMessageBox.StandardButton.Yes:
			open_file = open_file_dialog(self)
			if open_file != None:
				self.ini_config = Files.read_write_json(open_file, 'r')
				self.ConfigOnText()

	def SaveConfBTNClicked(self):
		global icon_settings, html_fomr_style
		msg = QMessageBox.question(self, html_fomr_style['forms']['saveconf']['title'], html_fomr_style['forms']['saveconf']['text'], QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		if msg == QMessageBox.StandardButton.Yes:
			self.TextOnConfig()
			Passwords.SetPass(Defaults.secret_config[0], self.ini_config[Defaults.secret_config[0]])
			Passwords.SetPass(Defaults.secret_config[1], self.ini_config[Defaults.secret_config[1]])
			Passwords.SetPass(Defaults.secret_config[2], self.ini_config[Defaults.secret_config[2]])
			Files.read_write_text(Files.ini_config_file, 'w', Files.JSONToSTR(self.ini_config))

	def LoadConfBTNClicked(self):
		global icon_settings, html_fomr_style
		msg = QMessageBox.question(self, html_fomr_style['forms']['loadconf']['title'], html_fomr_style['forms']['loadconf']['text'], QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		if msg == QMessageBox.StandardButton.Yes:
			self.ini_config = Files.read_write_json(Files.ini_config_file, 'r')
			self.ini_config[Defaults.secret_config[0]] = get_credential_service(Defaults.secret_config[0], self.ini_config[Defaults.secret_config[0]])
			self.ini_config[Defaults.secret_config[1]] = get_credential_service(Defaults.secret_config[1], self.ini_config[Defaults.secret_config[1]])
			self.ini_config[Defaults.secret_config[2]] = get_credential_service(Defaults.secret_config[2], self.ini_config[Defaults.secret_config[2]])
			self.ConfigOnText()
	
	def AllClearBTNClicked(self):
		global icon_settings, html_fomr_style, default_config
		msg = QMessageBox.question(self, html_fomr_style['forms']['allclear']['title'], html_fomr_style['forms']['allclear']['text'], QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		if msg == QMessageBox.StandardButton.Yes:
			self.set_obj_text(self.token_text, '')
			self.set_obj_text(self.domain_text, '')
			self.set_obj_text(self.ownerid_text, '')
			self.set_obj_text(self.downloaddir_text, './download')
			self.set_obj_text(self.version_text, '5.236')
			self.ClearBTNClicked()
			set_obj_checked(self.resized_checker, False)
			set_obj_checked(self.saveurl_checker, True)
			Files.read_write_file(Files.config_file, 'w', Files.JSONToSTR(default_config))
			Files.read_write_file(Files.style_config_file, 'w', Files.JSONToSTR(self.default_style_config))
			self.INITStyleConfig()
			self.INITMainConfig()
			self.StyleApply()
	
	def ClearBTNClicked(self):
		self.set_obj_text(self.count_posts_text, '10')
		self.set_obj_text(self.offset_text, '0')
		self.set_obj_text(self.datastop_text, '..2')
	
	def ResetConfBTNClicked(self):
		global icon_settings, html_fomr_style
		msg = QMessageBox.question(self, html_fomr_style['forms']['resetclear']['title'], html_fomr_style['forms']['resetclear']['text'], QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		if msg == QMessageBox.StandardButton.Yes:
			self.set_obj_text(self.token_text, '')
			self.set_obj_text(self.domain_text, '')
			self.set_obj_text(self.ownerid_text, '')
	
	def DeleteBTNClicked(self):
		global icon_settings, html_fomr_style
		msg = QMessageBox.question(self, html_fomr_style['forms']['delete']['title'], html_fomr_style['forms']['delete']['text'], QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
		if msg == QMessageBox.StandardButton.Yes:
			Passwords.DelPass(Defaults.secret_config[0])
			Passwords.DelPass(Defaults.secret_config[1])
			Passwords.DelPass(Defaults.secret_config[2])
			Files.ini_config_file.unlink(missing_ok=True)
	
	def RefreshBTNClicked(self):
		self.ini_config = Files.read_write_json(Files.ini_config_file, 'r')
		self.ini_config[Defaults.secret_config[0]] = get_credential_service(Defaults.secret_config[0], self.ini_config[Defaults.secret_config[0]])
		self.ini_config[Defaults.secret_config[1]] = get_credential_service(Defaults.secret_config[1], self.ini_config[Defaults.secret_config[1]])
		self.ini_config[Defaults.secret_config[2]] = get_credential_service(Defaults.secret_config[2], self.ini_config[Defaults.secret_config[2]])
		self.ConfigOnText()
	
	def ReceiveBTNClicked(self):
		self.progress_bar.setValue(0)
		set_obj_enabled(self.download_button, False)
		if get_obj_checked(self.saveurl_checker):
			VKAPI.save_posts(self.config, str(self.dataset.downloaddir.joinpath(Defaults.post_file_name)), str(self.dataset.downloaddir.joinpath(Defaults.url_file_name)))
		else:
			VKAPI.save_posts(self.config, str(self.dataset.downloaddir.joinpath(Defaults.post_file_name)), '')
		set_obj_enabled(self.download_button, True)
		self.progress_bar.setValue(100)
	
	def ReceiveDataBTNClicked(self):
		self.progress_bar.setValue(0)
		set_obj_enabled(self.download_button, False)
		if get_obj_checked(self.saveurl_checker):
			VKAPI.search_date(config, str(self.dataset.downloaddir.joinpath(Defaults.post_file_name)), str(self.dataset.downloaddir.joinpath(Defaults.url_file_name)))
		else:
			VKAPI.search_date(config, str(self.dataset.downloaddir.joinpath(Defaults.post_file_name)), '')
		set_obj_enabled(self.download_button, True)
		self.progress_bar.setValue(100)
	
	def DownloadPosts(self):
		self.thread = PostThread(self.dataset, self.config)
		self.thread.change_value.connect(self.set_pbar_value)
		self.thread.start()
		self._wait_thread = WaitThread(self.get_pbar_value, self.FineDownload)
		self._wait_thread.start()
		
	def FineDownload(self):
		self.old_resized = self.dataset.isresized
		progress_procent = 100
		self.set_pbar_value(100)
		self.control_enabled()
	
	def set_pbar_value(self, value: int):
		self.progress_bar.setValue(value)
	
	def get_pbar_value(self):
		return self.progress_bar.value()
	
	def control_enabled(self):
		set_obj_enabled(self.version_button, True)
		set_obj_enabled(self.view_button, True)
		set_obj_enabled(self.help_button, True)
		set_obj_enabled(self.selectdir_button, True)
		set_obj_enabled(self.resized_checker, True)
		set_obj_enabled(self.saveurl_checker, True)
		set_obj_enabled(self.opendir_button, True)
		set_obj_enabled(self.delete_button, True)
		set_obj_enabled(self.refresh_button, True)
		set_obj_enabled(self.apply_button, True)
		set_obj_enabled(self.savefile_button, True)
		set_obj_enabled(self.loadfile_button, True)
		set_obj_enabled(self.loadconf_button, True)
		set_obj_enabled(self.allclear_button, True)
		set_obj_enabled(self.clear_button, True)
		set_obj_enabled(self.saveconf_button, True)
		set_obj_enabled(self.resetconf_button, True)
		set_obj_enabled(self.receive_data_button, True)
		set_obj_enabled(self.receive_button, True)
		set_obj_enabled(self.download_button, True)
		progress_procent = 100
		self.set_pbar_value(100)
		self.old_resized = self.dataset.isresized
	
	def control_disable(self):
		set_obj_enabled(self.version_button, False)
		set_obj_enabled(self.view_button, False)
		set_obj_enabled(self.help_button, False)
		set_obj_enabled(self.selectdir_button, False)
		set_obj_enabled(self.resized_checker, False)
		set_obj_enabled(self.saveurl_checker, False)
		set_obj_enabled(self.opendir_button, False)
		set_obj_enabled(self.delete_button, False)
		set_obj_enabled(self.refresh_button, False)
		set_obj_enabled(self.apply_button, False)
		set_obj_enabled(self.savefile_button, False)
		set_obj_enabled(self.loadfile_button, False)
		set_obj_enabled(self.loadconf_button, False)
		set_obj_enabled(self.allclear_button, False)
		set_obj_enabled(self.clear_button, False)
		set_obj_enabled(self.saveconf_button, False)
		set_obj_enabled(self.resetconf_button, False)
		set_obj_enabled(self.receive_data_button, False)
		set_obj_enabled(self.receive_button, False)
		set_obj_enabled(self.download_button, False)
	
	def DownloadBTNClicked(self):
		global stop_thread, progress_procent
		progress_procent = 0
		self.set_pbar_value(0)
		self.control_disable()
		stop_thread = False
		if self.old_resized != self.dataset.isresized:
			data = DataSet()
			data.fcount('c3', -1)
			post_file_name = data.GenPostName
			if not post_file_name.exists():
				self.dataset.fcount.ResetCounter('c1').ResetCounter('c2').ResetCounter('c3').ResetCounter('c4')
			else:
				data.fcount('c3').ResetCounter('c4')	
		self.DownloadPosts()
		
	def VersionBTNClicked(self):
		self.setEnabled(False)
		self.version_form.form_show()
