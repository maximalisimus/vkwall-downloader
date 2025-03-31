import pathlib
import sys
import pickle
import base64
import webbrowser
from datetime import datetime
import time
import codecs
import json
import requests
import re

import subprocess, os, platform

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QAction, QMenu, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import QCoreApplication, Qt, QRegExp, QThread, pyqtSignal
from PyQt5.QtGui import QKeySequence, QRegExpValidator

from PIL import Image
import keyring

__author__ = 'Mikhail Artamonov'
author = __author__
__progname__ = str(pathlib.Path(sys.argv[0]).resolve().name)
progname = __progname__
__copyright__ = f"© The \"{__progname__}\". Copyright  by 2024."
copyrights = __copyright__
__credits__ = ["Mikhail Artamonov"]
credites = __credits__
__license__ = "GPL3"
licenses = __license__
__version__ = "1.0.0"
version = __version__
__maintainer__ = "Mikhail Artamonov"
maintainer = __maintainer__
__status__ = "Production"
status = __status__
__date__ = '10.06.2024'
date_source = __date__
__modifed__ = '10.06.2024'
modifed = __modifed__

number = 1

prefixer = pathlib.Path(sys.argv[0])

def RelativePath(thefile, thedir):
	return str(pathlib.Path(str(thefile)).resolve().relative_to(str(pathlib.Path(str(thedir)).resolve())))

stop_thread = False
progress_procent = 0
progress_bar = None

icon_settings = {
					'forms': RelativePath(str(prefixer.parent.joinpath('image').joinpath('vk-icon.png')), prefixer.parent),
					'clear': RelativePath(str(prefixer.parent.joinpath('image').joinpath('clear.png')), prefixer.parent),
					'delete': RelativePath(str(prefixer.parent.joinpath('image').joinpath('delete.png')), prefixer.parent),
					'save': RelativePath(str(prefixer.parent.joinpath('image').joinpath('save.png')), prefixer.parent),
					'refresh': RelativePath(str(prefixer.parent.joinpath('image').joinpath('refresh.png')), prefixer.parent),
					'uses': RelativePath(str(prefixer.parent.joinpath('image').joinpath('uses.png')), prefixer.parent),
					'load': RelativePath(str(prefixer.parent.joinpath('image').joinpath('load.png')), prefixer.parent),
					'view': RelativePath(str(prefixer.parent.joinpath('image').joinpath('view.png')), prefixer.parent),
					'notview': RelativePath(str(prefixer.parent.joinpath('image').joinpath('notview.png')), prefixer.parent),
					'receive': RelativePath(str(prefixer.parent.joinpath('image').joinpath('receive.png')), prefixer.parent),
					'download': RelativePath(str(prefixer.parent.joinpath('image').joinpath('download.png')), prefixer.parent),
					'upload': RelativePath(str(prefixer.parent.joinpath('image').joinpath('upload.png')), prefixer.parent),
					'prev': RelativePath(str(prefixer.parent.joinpath('image').joinpath('prev.png')), prefixer.parent),
					'saveconf': RelativePath(str(prefixer.parent.joinpath('image').joinpath('saveconf.png')), prefixer.parent),
					'yes': RelativePath(str(prefixer.parent.joinpath('image').joinpath('yes.png')), prefixer.parent),
					'no': RelativePath(str(prefixer.parent.joinpath('image').joinpath('no.png')), prefixer.parent),
					'help': RelativePath(str(prefixer.parent.joinpath('image').joinpath('help.png')), prefixer.parent),
					'folder': RelativePath(str(prefixer.parent.joinpath('image').joinpath('folder.png')), prefixer.parent),
					'info': RelativePath(str(prefixer.parent.joinpath('image').joinpath('info.png')), prefixer.parent),
					'stop': RelativePath(str(prefixer.parent.joinpath('image').joinpath('stop.png')), prefixer.parent),
					'next': RelativePath(str(prefixer.parent.joinpath('image').joinpath('next.png')), prefixer.parent)
				}

html_fomr_style = {
						"url": "https://vk.com/apps?act=manage",
						"version_url": "https://dev.vk.com/ru/reference/versions",
						"form_ui": {
										"token": {
													"file_name": RelativePath(str(prefixer.parent.joinpath('forms').joinpath('token.ui')), prefixer.parent),
													"form_name": "token_form",
												},
										"main": {
													"file_name": RelativePath(str(prefixer.parent.joinpath('forms').joinpath('main.ui')), prefixer.parent),
													"form_name": "main_form",
											},
									},
						"forms": {									
									"dialogs": {
													"select_folder": {
																		"title": "Выбрать папку загрузок:",
																	},
													"save_file": {
																	"title": "Сохранение настроек",
																	"filter": "Настройки (*.conf)",
																	"initial_filter": "Настройки (*.conf)",
																},
													"open_file": {
																	"title": "Загрузка настроек",
																	"filter": "Настройки (*.conf)",
																	"initial_filter": "Настройки (*.conf)",
																},
												},
									"main": {
												"forms": {
															"title": "ВК Сохранение стены",
															"icon": f"{icon_settings['forms']}",
														},
												"version_label": {
																	"title": "Версия ВК API:",
																},
												"version_text": {
																	"title": "5.236",
																},
												"version_button": {
																		"title": "",
																		"icon": f"{icon_settings['help']}",
																},
												"token_label": {
																	"title": "Токен:",
																},
												"token_text": {
																	"title": "",
																},
												"domain_label": {
																	"title": "Домен группы:",
																},
												"domain_text": {
																	"title": "",
																},
												"ownerid_label": {
																	"title": "ownerid:",
																},
												"ownerid_text": {
																	"title": "",
																},
												"downloaddir_label": {
																		"title": "Загрузка:",
																	},
												"downloaddir_text": {
																		"title": "./download",
																	},
												"count_posts_label": {
																		"title": "Кол-во постов:",
																	},
												"count_posts_text": {
																		"title": "10",
																	},
												"offset_label": {
																	"title": "Смещение:",
																},
												"offset_text": {
																	"title": "0",
																},
												"datastop_label": {
																	"title": "Конечная дата:",
																},
												"datastop_text": {
																	"title": "..2",
																},
												"resized_checker": {
																		"title": "Уменшать фото",
																	},
												"saveurl_checker": {
																		"title": "Сохранить URL запроса",
																	},
												"view_button": {
																	"title": "",
																	"icon": f"{icon_settings['view']}",
																},
												"help_button": {
																	"title": "",
																	"icon": f"{icon_settings['help']}",
																},
												"selectdir_button": {
																		"title": "Выбрать папку",
																		"icon": f"{icon_settings['folder']}",
																	},
												"opendir_button": {
																	"title": "Открыть папку загрузок",
																	"icon": f"{icon_settings['folder']}",
																},
												"delete_button": {
																	"title": "Удалить",
																	"icon": f"{icon_settings['delete']}",
																},
												"refresh_button": {
																	"title": "Перезагрузить",
																	"icon": f"{icon_settings['refresh']}",
																},
												"apply_button": {
																	"title": "Применить",
																	"icon": f"{icon_settings['uses']}",
																},
												"savefile_button": {
																		"title": "Сохранить в файл",
																		"icon": f"{icon_settings['save']}",
																	},
												"loadfile_button": {
																		"title": "Загрузить из файла",
																		"icon": f"{icon_settings['load']}",
																	},
												"loadconf_button": {
																		"title": "Загрузить",
																		"icon": f"{icon_settings['upload']}",
																	},
												"allclear_button": {
																		"title": "Полная очистка",
																		"icon": f"{icon_settings['clear']}",
																	},
												"clear_button": {
																	"title": "Очистка",
																	"icon": f"{icon_settings['clear']}",
																},
												"resetconf_button": {
																		"title": "Сброс параметров запросов",
																		"icon": f"{icon_settings['clear']}",
																	},
												"saveconf_button": {
																		"title": "Сохранить",
																		"icon": f"{icon_settings['save']}",
																	},
												"receive_button": {
																	"title": "Запросить до даты",
																	"icon": f"{icon_settings['receive']}",
																},
												"download_button": {
																		"title": "Скачать данные",
																		"icon": f"{icon_settings['download']}",
																	},
												"receive_data_button": {
																			"title": "Запросить за дату",
																			"icon": f"{icon_settings['receive']}",
																		},
											},
									"token": {
												"title": "Информация о токене безопасности",
												"text": '<html><head/><body><p><span style=" font-weight:600;">VK token (ВК токен)</span> необходим для аутентификации и авторизации при работе с <span style=" text-decoration: underline;">API</span> социальной сети <span style=" text-decoration: underline;">ВКонтакте</span>. С его помощью приложения получают доступ к различным функциям и данным социальной сети, таким как получение информации о профиле, отправка сообщений, управление сообществами и многим другим функциям.</p><p>В данном приложении токен нужен только для того, чтобы скачивать данные с указанной группы <span style=" text-decoration: underline;">ВКонтакте</span> или со стены указанного человека.</p><p>Чтобы получить <span style=" font-weight:600;">VK token</span> необходимо добавить новое приложение в <span style=" text-decoration: underline;">API</span> настройках вашего аккаунта, т.е. в настройках для разработчиков.Для этого нажмите кнопку «Перейти в настройку» и добавьте новое приложение. Полученный токен вставьте в соответствующее поле в предыдущем окне программы.</p></body></html>',
												"icon_form": f"{icon_settings['forms']}",
												"icon_no": f"{icon_settings['prev']}",
												"icon_ok": f"{icon_settings['next']}",
												"btn_no": "Назад",
												"btn_ok": "Перейти в настройку",
												"sizes": {
															"geometry": {
																			"x": 0,
																			"y": 0,
																			"width": 512,
																			"height": 360,
																		},
															"minimum_size": {
																				"width": 480,
																				"height": 360,
																			},
															"maximum_size": {
																				"width": 1024,
																				"height": 800,
																			},
															"base_size": {
																			"width": 480,
																			"height": 360,
																		},
															"text_label": {
																			"width": 0,
																			"height": 296,
																		},
														},
											},
									"version": {
												"title": "Информация о версии ВК API",
												"text": '<html><head/><body><p><span style=" font-size:12pt; font-weight:600;">Версия VK API</span><span style=" font-size:12pt;"> — это параметр, который указывается в запросе и без которого нельзя сформировать запрос.</span></p><p><span style=" font-size:12pt;">Указывать можно как старую, так и более новую современную версию. Это удобно тем, что вам не придётся каждый раз переписывать всё взаимодействие с уже имеющимся интерфейсом системы запросов и ответов.</span></p><p><span style=" font-size:12pt;">Однако, версию увеличивают и улучшают не просто так. Чаще всего в новых исправляют различные ошибки старых и добавляют новый функционал.</span></p></body></html>',
												"icon_form": f"{icon_settings['forms']}",
												"icon_no": f"{icon_settings['prev']}",
												"icon_ok": f"{icon_settings['next']}",
												"btn_no": "Назад",
												"btn_ok": "Перейти в настройку",
												"sizes": {
															"geometry": {
																			"x": 0,
																			"y": 0,
																			"width": 512,
																			"height": 296,
																		},
															"minimum_size": {
																				"width": 480,
																				"height": 296,
																			},
															"maximum_size": {
																				"width": 1024,
																				"height": 800,
																			},
															"base_size": {
																			"width": 480,
																			"height": 296,
																		},
															"text_label": {
																			"width": 0,
																			"height": 240,
																		},
														},
											},
									"delete": {
												"title": "Удаление паролей",
												"text": "Вы действительно хотите удалить все пароли и данные из учетных данных системы?",
											},
									"savefile": {
													"title": "Сохранение данных в файл",
													"text": "Вы действительно хотите сохранить все настройки в файл?",
												},
									"loadfile": {
													"title": "Загрузка данных из файла",
													"text": "Вы действительно хотите загрузить все настройки из файла?\nВсе поля ввода будут изменены!",
												},
									"saveconf": {
													"title": "Сохранение учетных данных",
													"text": "Вы действительно хотите сохранить токен, домен и id группы или человека в учетных данных системы?",
												},
									"loadconf": {
													"title": "Загрузка учетных данных",
													"text": "Вы действительно хотите загрузить токен, домен и id группы или человека из учетных данных системы?",
												},
									"allclear": {
													"title": "Полная очистка",
													"text": "Вы действительно хотите очистить все поля ввода?",
												},
									"resetclear": {
														"title": "Сброс всех запросов",
														"text": "Вы действительно хотите полностью сбросить все изначальные параметры запросов?",
												},
								},
					}

default_config = {
					'url': 'https://api.vk.com/method/wall.get?',
					'album_url': 'https://api.vk.com/method/photos.get?',
					'version': '5.236',
					'count': 10,
					'offset': 2,
					'sep': '.',
					'root': 'response.items',
					'data': 'date',
					'id': 'id',
					'wall': 'https://vk.com/wall',
					'hashtag': 'https://vk.com/feed?section=search&q=',
					'inner_post': 'vk.com/@',
					'text': 'text',
					'image': {
								'width': 'width',
								'height': 'height',
								'url': 'url'
							},
					'attachments': 'attachments',
					'copy_history': 'copy_history.attachments',
					'copy_history_text': 'text',
					'obj_type': 'type',
					'attach': {
								'photo': {
											'text': [],
											'save': [],
											'download': True,
											'isone': False,
											'list': 'sizes',
											'ext': 'jpg',
											'isimage': True,
											'isalbum': False
										},
								'album': {
											'text': ['title'],
											'save': ['id'],
											'download': True,
											'isone': False,
											'list': 'sizes',
											'ext': 'jpg',
											'isimage': True,
											'isalbum': True
										},
								'video': {
											'text': ['title', 'description'],
											'save': ['https://vk.com/video', 'owner_id', '_', 'id'],
											'download': True,
											'isone': False,
											'list': 'image',
											'ext': 'jpg',
											'isimage': True,
											'isalbum': False
										},
								'link': {
											'text': ['title', 'description'],
											'save': ['url'],
											'download': False,
											'isone': False,
											'list': '',
											'ext': '',
											'isimage': False,
											'isalbum': False
										},
								'audio': {
											'text': [],
											'save': ['url', '\n', 'artist', '-', 'title'],
											'download': True,
											'isone': True,
											'list': 'url',
											'ext': 'mp3',
											'isimage': False,
											'isalbum': False
										},
								'doc': {
											'text': [],
											'save': ['title', '\n', 'url'],
											'download': True,
											'isone': True,
											'list': 'url',
											'ext': 'ext',
											'isimage': False,
											'isalbum': False
										},
								'poll': {
											'text': ['question'],
											'save': [],
											'download': False,
											'isone': False,
											'list': 'answers.text',
											'ext': '',
											'isimage': False,
											'isalbum': False
										}
							}
				}
