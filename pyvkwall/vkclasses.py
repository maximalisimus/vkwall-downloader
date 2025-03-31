from .vkconf import *

class AuthorInfo:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"Author: {author}\nProgname: {progname}\nVersion: {version}\n" + \
			f"Date of creation: {date_source}\nLast modified date: {modifed}\n" + \
			f"License: {licenses}\nCopyright: {copyrights}\nCredits: {credites}\n" + \
			f"Maintainer: {maintainer}\nStatus: {status}\n"

class Author:
	
	Info = AuthorInfo()

class Characters:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return '.-+_,()[]{}&@#='

class AlphabetRU:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return ''.join(list(map(chr, range(ord('а'),ord('я')+1, 1))))

class AlphabetEN:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return ''.join(list(map(chr, range(ord('a'),ord('z')+1, 1))))

class Integers:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return ''.join(list(map(str, list(range(0, 10, 1)))))

class Alphabet:
	
	symbols = Characters()
	alphabet_ru = AlphabetRU()
	alphabet_en = AlphabetEN()
	nums = Integers()

	@property
	def alphabet(self):
		return self.alphabet_ru + self.alphabet_ru.upper() + ' ' + self.alphabet_en + self.alphabet_en.upper() + self.symbols + self.nums

	def SetName(self, onname):
		return ''.join([x for x in onname if x in self.alphabet]).replace(' ', '_')

class Texts:
	
	@classmethod
	def GetOutText(cls, inText) -> str:
		output_text = json.dumps(inText, ensure_ascii=False)
		out_text = output_text.replace(r'\n','\r\n').replace('\\"','"').replace(' /','').replace('/ ',' ')
		output_text = out_text.lstrip(' "').rstrip('" ')
		return output_text

	@classmethod
	def SetCorrectFileName(cls, inputFileName):
		alphabet = Alphabet()
		return alphabet.SetName(inputFileName)

	@classmethod
	def SetQuoteString(cls, inputstr):
		return inputstr.replace('#', '%23')
	
	@classmethod
	def GetQuoteString(cls, inputstr):
		return inputstr.replace('%23', '#')

	@classmethod
	def GetHashTags(cls, inputstr):
		regexp = re.compile("\#")
		indexes = [match.start() for match in re.finditer(regexp, inputstr)]
		hashtags = []
		for x in indexes:
			hashtags.append(inputstr[x:].split(' ')[0])
		fulltags = set(hashtags)
		hashtags = list(map(cls.SetQuoteString, fulltags))
		return hashtags
	
	@staticmethod
	def StrToBase(inputSTR):
		str_bytes = inputSTR.encode('utf-8')
		return base64.b64encode(str_bytes).decode('utf-8')
	
	@staticmethod
	def BaseToSTR(inputBase):
		data = base64.b64decode(inputBase.encode('utf-8'))
		return data.decode('utf-8')

	@classmethod
	def EncodeDict(cls, inputDict: dict):
		for k in inputDict.keys():
			inputDict[k] = cls.StrToBase(inputDict[k])

	@classmethod
	def DecodeDict(cls, inputEncode: dict):
		for k in inputEncode.keys():
			inputEncode[k] = cls.BaseToSTR(inputEncode[k])

class ConfigFileName:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"config.json"

class INIConfigFileName:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"settings.json"

class StyleConfigName:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"style.json"

class SecretConfig:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return ["token", "domain", "ownerid"]

class GlobalConfig:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return ["download", "version", "count", "offset", "data_stop", "resize", "save_url"]

class PostFileName:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"posts.json"

class URLFileName:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"url.txt"

class Defaults:
	
	config_file_name = ConfigFileName()
	style_file_name = StyleConfigName()
	ini_file_name = INIConfigFileName()
	main_config = GlobalConfig()
	secret_config = SecretConfig()
	post_file_name = PostFileName()
	url_file_name = URLFileName()

class Meta(type):
	
	def __init__(cls, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	@property
	def PREFIX(cls):
		global prefixer
		return prefixer.resolve().parent
	
	@property
	def config_file(cls):
		return cls.PREFIX.joinpath(Defaults.config_file_name)
	
	@property
	def ini_config_file(cls):
		return cls.PREFIX.joinpath(Defaults.ini_file_name)
	
	@property
	def style_config_file(cls):
		return cls.PREFIX.joinpath(Defaults.style_file_name)
	
class Files(metaclass=Meta):
	
	@staticmethod
	def relative_path(thefile, thedir):
		return RelativePath(thefile, thedir)
	
	@staticmethod
	def read_write_json(jfile, typerw, data = dict(), indent: int = 2):
		''' The function of reading and writing JSON objects. '''
		file_save = pathlib.Path(str(jfile)).resolve()
		file_name = Texts.SetCorrectFileName(str(file_save.name))
		file_save = pathlib.Path(str(jfile)).resolve().parent.joinpath(file_name)
		file_save.parent.mkdir(parents=True,exist_ok=True)
		with open(str(file_save), typerw) as fp:
			if 'r' in typerw:
				data = json.load(fp)
				return data
			else:
				json.dump(data, fp, indent=indent)

	@staticmethod
	def read_write_text(onfile, typerw, data = "", chcp = 'utf-8'):
		''' The function of reading and writing text files. '''
		file_save = pathlib.Path(str(onfile)).resolve()
		file_name = Texts.SetCorrectFileName(str(file_save.name))
		file_save = pathlib.Path(str(onfile)).resolve().parent.joinpath(file_name)
		file_save.parent.mkdir(parents=True,exist_ok=True)
		with codecs.open(str(file_save), typerw, chcp) as fp:
			if 'r' in typerw:
				data = fp.read()
				return data
			else:
				fp.write(data)
	
	@staticmethod
	def read_write_file(onfile, typerw, data = ""):
		''' The function of reading and writing text files. '''
		file_save = pathlib.Path(str(onfile)).resolve()
		file_name = Texts.SetCorrectFileName(str(file_save.name))
		file_save = pathlib.Path(str(onfile)).resolve().parent.joinpath(file_name)
		file_save.parent.mkdir(parents=True,exist_ok=True)
		with open(str(file_save), typerw) as fp:
			if 'r' in typerw:
				data = fp.read()
				return data
			else:
				fp.write(data)
	
	@staticmethod
	def read_write_obj(onfile, typerw, data: dict = dict()):
		file_save = pathlib.Path(str(onfile)).resolve()
		file_name = Texts.SetCorrectFileName(str(file_save.name))
		file_save = pathlib.Path(str(onfile)).resolve().parent.joinpath(file_name)
		file_save.parent.mkdir(parents=True,exist_ok=True)
		if 'r' in typerw:
			with open(str(file_save), 'rb') as fp:
				data = pickle.load(fp)
				return data
		else:
			with open(str(file_save), 'wb') as fp:
				pickle.dump(data, fp)
	
	@staticmethod
	def JSONToSTR(data_json: dict, onindent: int = 2) -> str:
		return json.dumps(data_json, indent=onindent, ensure_ascii=False)
	
	@staticmethod
	def STRToJSON(value: str) -> dict:
		return json.loads(value)
	
	@staticmethod
	def ResizeImage(InputImageFile, OutputImageFile, OnWidth, OnHeight, isShowOutputImage: bool = False):
		new_size = (OnWidth, OnHeight)
		resized = ''
		with Image.open(str(pathlib.Path(InputImageFile).resolve())) as image:
			ratio = min(float(new_size[0]) / image.size[0], float(new_size[1]) / image.size[1])
			new_width = int(image.size[0] * ratio)
			new_height = int(image.size[1] * ratio)		
			resized = image.resize((new_width, new_height))
		resized.save(str(pathlib.Path(OutputImageFile).resolve()))
		if isShowOutputImage:
			resized.show()

class Passwords:
	
	@staticmethod
	def SetPass(ServiceName: str, OnPass: str, OnUser: str = ''):
		if OnUser != '':
			keyring.set_password(ServiceName, OnUser, OnPass)
		else:
			keyring.set_password(ServiceName, str(pathlib.Path().home().name), OnPass)

	@staticmethod
	def GetPass(ServiceName: str, OnUser: str = ''):
		if OnUser != '':
			return keyring.get_password(ServiceName, OnUser)
		else:
			return keyring.get_password(ServiceName, str(pathlib.Path().home().name))

	@staticmethod
	def GetCredential(ServiceName: str):
		cred = keyring.get_credential(ServiceName,"")
		if cred is not None:
			return cred.username, cred.password
		else:
			return None, None

	@staticmethod
	def DelPass(ServiceName: str, OnUser: str = ''):
		cred = keyring.get_credential(ServiceName,"")
		if OnUser != '':
			if cred is not None:
				keyring.delete_password(ServiceName, OnUser)
				return keyring.get_password(ServiceName, OnUser)
			else:
				return None
		else:
			if cred is not None:
				keyring.delete_password(ServiceName, str(pathlib.Path().home().name))
				return keyring.get_password(ServiceName, str(pathlib.Path().home().name))
			else:
				return None

class ReadDateSTRNow:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return DateStamp.dateTimeToStr(datetime.now(),"%d.%m.%Y")

class ReadTimeSTRNow:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return DateStamp.dateTimeToStr(datetime.now(),"%H:%M:%S")

class ReadDateTimeSTRNow:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return DateStamp.dateTimeToStr(datetime.now(),"%d.%m.%Y-%H:%M:%S")

class DefaultDate:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return "01.01.2010"

class DateStamp:
	
	CurrentDate = ReadDateSTRNow()
	CurrentTime = ReadTimeSTRNow()
	CurrentDateTime = ReadDateTimeSTRNow()
	DefaultDate = DefaultDate()
	
	@staticmethod
	def stampToStr(timeStamp: int, strFormat = "%d.%m.%Y-%H:%M:%S") -> str:
		dateTime = datetime.fromtimestamp(timeStamp)
		datestr = dateTime.strftime(strFormat)
		return datestr
	
	@staticmethod
	def stampToDate(timeStamp: int):
		dateTime = datetime.fromtimestamp(timeStamp)
		return dateTime
	
	@staticmethod
	def stampToDateTime(timeStamp: int) -> datetime:
		dateTime = datetime.fromtimestamp(timeStamp)
		return dateTime

	@staticmethod
	def strToStamp(dateStr: str, strFormat = "%d.%m.%Y-%H:%M:%S") -> int:
		time_Tuple = datetime.strptime(dateStr, strFormat)
		outTimeStamp = time.mktime(time_Tuple.timetuple())
		return int(outTimeStamp)

	@staticmethod
	def dateTimeToStamp(dateTime: datetime) -> int:
		outTimeStamp = time.mktime(dateTime.timetuple())
		return int(outTimeStamp)

	@staticmethod
	def intToDate(dateINT: int, strFormat = "%d.%m.%Y-%H:%M:%S"):
		dateTime = datetime.strptime(dateINT, strFormat)
		return dateTime

	@staticmethod
	def dateTimeToStr(dateTime: datetime, strFormat = "%d.%m.%Y-%H:%M:%S") -> str:
		outDateTime = dateTime.strftime(strFormat)
		return outDateTime

	@staticmethod
	def strToDateTime(dateStr: str, strFormat = "%d.%m.%Y-%H:%M:%S") -> datetime:
		time_Tuple = datetime.strptime(dateStr, strFormat)
		return time_Tuple

	@classmethod
	def SetOutDateSTR(cls, value, strFormat = "%d.%m.%Y"):
		if type(value) == int:
			return cls.stampToStr(value,strFormat)
		elif type(value) == datetime:		
			return cls.dateTimeToStr(value,strFormat)
		elif type(value) == str:
			return value

class DateValue:

	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value):
		setattr(instance, self.name, DateStamp.SetOutDateSTR(value))

	def __call__(self):
		return self.value

	def __str__(self):
		return f"{self.value}"

class Strings:
	
	@classmethod
	def verify_str(cls, value):
		if type(value) != str:
			raise TypeError('Enter the string!')
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: str):
		self.verify_str(value)
		setattr(instance, self.name, value)

class Counter:
	
	def __init__(self, value: int = 0):
		self.value = value
	
	def __call__(self, value: int = 1):
		self.value += value
		return self

	def __str__(self):
		return f"{self.value}"

class Base:
	
	__slots__ = ['__dict__']
		
	def __init__(self):
		self.except_list = []
	
	def __str__(self):
		''' For STR Function output paramters. '''
		return '\t' + '\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in self.except_list and '__' not in x)
	
	def __repr__(self):
		''' For Debug Function output paramters. '''
		return f"{self.__class__}:\n\t" + \
				'\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in self.except_list and '__' not in x)

class Arguments(Base):
	
	def __init__(self, *args, **kwargs):
		super(Arguments, self).__init__()
	
	def __getattr__(self, attrname):
		''' Access to a non-existent variable. '''
		return None

class DateTracking(Base):
	
	date_start = DateValue()
	date_stop = DateValue()
	date_curr = DateValue()
	full_curr = Strings()
	
	def __init__(self, DateCurr: str = '', DateStart: str = '', DateStop: str = ''):
		super(DateTracking, self).__init__()
		if DateStart == '':
			self.date_start = DateStamp.dateTimeToStr(datetime.now(), "%d.%m.%Y")
		else:
			self.date_start = DateStart
		if DateStop == '':
			self.date_stop = '01.01.2000'
		else:
			self.date_stop = DateStop
		if DateCurr == '':
			self.date_curr = DateStamp.dateTimeToStr(datetime.now(), "%d.%m.%Y")
		else:
			self.date_curr = DateCurr
		full_curr = DateStamp.CurrentDateTime # %d.%m.%Y-%H:%M:S

class FolderCount(Base):
	
	limit = 100
	
	@classmethod
	def SetLimit(cls, value: int):
		cls.limit = value
	
	def __init__(self, c1 = 1, c2 = 1, c3 = 1, c4 = 1):
		super(FolderCount, self).__init__()
		self.c1 = Counter(c1)
		self.c2 = Counter(c2)
		self.c3 = Counter(c3)
		self.c4 = Counter(c4)
		self.except_list.append('ResetCounter')
		self.except_list.append('SetLimit')
		self.except_list.append('Limitation')
	
	def __getattr__(self, attrname):
		''' Access to a non-existent variable. '''
		return None

	def __call__(self, attrname, value: int  = 1):
		if attrname in ['c1', 'c2', 'c3', 'c4']:
			self.__dict__[attrname](value)
			self.Limitation()
		return self

	def ResetCounter(self, attrname, value: int = 1):
		if attrname in ['c1', 'c2', 'c3', 'c4']:
			self.__dict__[attrname].value = value
		return self

	def Limitation(self):
		if self.c2.value%self.limit == 0 and self.c3.value%self.limit == 0:
			self.c1()
			self.ResetCounter('c4')
		if self.c3.value%self.limit == 0:
			self.c2()
			self.ResetCounter('c4')

class DataSet:
	
	_instance = None
	
	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
			
			download_dir = args[0] if len(args) >= 1 else kwargs.get('downloaddir', './')
			ondatecurr = args[1] if len(args) >= 2 else kwargs.get('DateCurr','')
			ondatestart = args[2] if len(args) >= 3 else kwargs.get('DateStart','')
			ondatestop = args[3] if len(args) >= 4 else kwargs.get('DateStop','')
			isurl = args[4] if len(args) >= 5 else kwargs.get('isurl',True)
			istext = args[5] if len(args) >= 6 else kwargs.get('istext',True)
			isResized = args[6] if len(args) >= 7 else kwargs.get('isresized',True)
			width = args[7] if len(args) >= 8 else kwargs.get('width',1024)
			height = args[8] if len(args) >= 9 else kwargs.get('height',800)
			isOneText = args[9] if len(args) >= 10 else kwargs.get('isonetext',False)
			onc1 = args[10] if len(args) >= 11 else kwargs.get('c1',1)
			onc2 = args[11] if len(args) >= 12 else kwargs.get('c2',1)
			onc3 = args[12] if len(args) >= 13 else kwargs.get('c3',1)
			onc4 = args[13] if len(args) >= 14 else kwargs.get('c4',1)
			
			cls._instance.datetrack = DateTracking(ondatecurr, ondatestart, ondatestop)
			cls._instance.fcount = FolderCount(onc1, onc2, onc3, onc4)
			cls._instance.downloaddir = pathlib.Path(str(download_dir)).resolve()
			cls._instance.isurl = isurl
			cls._instance.istext = istext
			cls._instance.isresized = isResized
			cls._instance.fullname_filesaved = ''
			cls._instance.width = width
			cls._instance.height = height
			cls._instance.isonetext = isOneText
			cls._instance.max_width = 0
			cls._instance.max_height = 0
			cls._instance.sep = '.'
			
		return cls._instance

	def ConvertDownloadDir(self):
		self.downloaddir = pathlib.Path(str(self.downloaddir)).resolve()
		return self

	@property
	def GenImageName(self):
		self.ConvertDownloadDir()
		if self.isresized:
			return self.downloaddir.joinpath(f"{self.fcount.c1.value}_50").joinpath(f"{self.fcount.c2.value}_{self.datetrack.date_start}_{self.datetrack.date_stop}_resized").joinpath(f"{self.fcount.c3.value}_{self.datetrack.date_curr}").joinpath(f"{self.fcount.c4.value}")
		else:
			return self.downloaddir.joinpath(f"{self.fcount.c1.value}_50").joinpath(f"{self.fcount.c2.value}_{self.datetrack.date_start}_{self.datetrack.date_stop}").joinpath(f"{self.fcount.c3.value}_{self.datetrack.date_curr}").joinpath(f"{self.fcount.c4.value}")

	@property
	def GenPostName(self):
		self.ConvertDownloadDir()
		if not self.isonetext:
			if self.isresized:
				return self.downloaddir.joinpath(f"{self.fcount.c1.value}_50").joinpath(f"{self.fcount.c2.value}_{self.datetrack.date_start}_{self.datetrack.date_stop}_resized").joinpath(f"{self.fcount.c3.value}_{self.datetrack.date_curr}").joinpath(f"Post-{self.datetrack.date_curr}.txt")
			else:
				return self.downloaddir.joinpath(f"{self.fcount.c1.value}_50").joinpath(f"{self.fcount.c2.value}_{self.datetrack.date_start}_{self.datetrack.date_stop}").joinpath(f"{self.fcount.c3.value}_{self.datetrack.date_curr}").joinpath(f"Post-{self.datetrack.date_curr}.txt")
		else:
			return self.downloaddir.joinpath("All-Posts.txt")

	def __str__(self):
		''' For STR Function output paramters. '''
		return f"downloaddir: {self.downloaddir}\n" + \
				f"datetrack:\n{self.datetrack}\n"+ \
				f"fcount:\n{self.fcount}"
	
	def __repr__(self):
		''' For Debug Function output paramters. '''
		return f"{self.__class__}:\n" + \
				f"downloaddir: {self.downloaddir}\n" + \
				f"datetrack:\n{self.datetrack}\n"+ \
				f"fcount:\n{self.fcount}"

class VKAPI:

	# cls.DownloadFiles(ImageFileName, image_file_ext, URLImage)

	@classmethod
	def DownloadFiles(cls, TheFileName, TheFileEXT, URLFile, isStream: bool = True):
		if isStream:
			the_file = requests.get(URLFile, stream=True)
		else:
			the_file = requests.get(URLFile)
		if the_file.status_code == 200:
			data = DataSet()
			data.fullname_filesaved = f"{str(TheFileName)}.{str(TheFileEXT)}"
			Files.read_write_file(data.fullname_filesaved, 'wb', the_file.content)

	@staticmethod
	def get_post_url(url, version, token, ownerid, domain, count, offset):
		if ownerid != '':
			response = requests.get(url,
									params={
												'v': version,
												'access_token': token,
												'domain': domain,
												'owner_id': ownerid,
												'count': count,
												'offset': offset,
												'filter': 'all'
											}
									)
		else:
			response = requests.get(url,
									params={
												'v': version,
												'access_token': token,
												'domain': domain,
												'count': count,
												'offset': offset,
												'filter': 'all'
											}
									)
		return response.url

	@classmethod
	def get_posts(cls, root, sep, url, version, token, ownerid, domain, count, offset):
		if ownerid != '':
			response = requests.get(url,
									params={
												'v': version,
												'access_token': token,
												'domain': domain,
												'owner_id': ownerid,
												'count': count,
												'offset': offset,
												'filter': 'all'
											}
									)
		else:
			response = requests.get(url,
									params={
												'v': version,
												'access_token': token,
												'domain': domain,
												'count': count,
												'offset': offset,
												'filter': 'all'
											}
									)
		data = response.json()
		if len(root) >= 1:
			for item in root.split(sep):
				data = data[item]
		return data

	@classmethod
	def get_inner_post(cls, url):
		response = requests.get(url)
		return response.text
	
	@classmethod
	def search_date(cls, json_params, json_file, url_file = ''):
		
		data = DataSet()
		
		if url_file != '':
			on_url = cls.get_post_url(json_params['url'], json_params['version'], json_params['token'], json_params['ownerid'], json_params['domain'], json_params['count'], json_params['offset'])
			# url, version, token, ownerid, domain, count, offset
			Files.read_write_file(url_file, 'w', on_url)
		
		fine_date = DateStamp.strToDateTime(data.datetrack.date_stop, '%d.%m.%Y').replace(hour=0, minute=0, second=0, microsecond=0)
		
		post = cls.get_posts(json_params['root'], json_params['sep'], json_params['url'], json_params['version'], json_params['token'], json_params['ownerid'], json_params['domain'], json_params['count'], json_params['offset'])
		# root, sep, url, version, token, ownerid, domain, count, offset
		current_date = DateStamp.stampToDate(post[0][json_params['data']])
		out_posts = []
		offset = json_params['offset']
		count = json_params['count']
		while current_date > fine_date:
			post = cls.get_posts(json_params['root'], json_params['sep'], json_params['url'], json_params['version'], json_params['token'], json_params['ownerid'], json_params['domain'], count, offset)
			# root, sep, url, version, token, ownerid, domain, count, offset
			current_date = DateStamp.stampToDate(post[count-1][json_params['data']])
			offset += count
			for i in range(0, len(post), 1):
				the_date = DateStamp.stampToDate(post[i][json_params['data']]).replace(hour=0, minute=0, second=0, microsecond=0)
				if the_date.date() == fine_date.date():
					out_posts.append(post[i])
		Files.read_write_json(json_file, 'w', out_posts)

	@classmethod
	def save_posts(cls, json_params, json_file, url_file = ''):
		
		data = DataSet()
		
		if url_file != '':
			on_url = cls.get_post_url(json_params['url'], json_params['version'], json_params['token'], json_params['ownerid'], json_params['domain'], json_params['count'], json_params['offset'])
			# url, version, token, ownerid, domain, count, offset
			Files.read_write_file(url_file, 'w', on_url)
		
		fine_date = DateStamp.strToDateTime(data.datetrack.date_stop, '%d.%m.%Y')
		
		post = cls.get_posts(json_params['root'], json_params['sep'], json_params['url'], json_params['version'], json_params['token'], json_params['ownerid'], json_params['domain'], json_params['count'], json_params['offset'])
		# root, sep, url, version, token, ownerid, domain, count, offset
		current_date = DateStamp.stampToDate(post[0][json_params['data']])
		out_posts = []
		offset = json_params['offset']
		count = json_params['count']
		while current_date > fine_date:
			post = cls.get_posts(json_params['root'], json_params['sep'], json_params['url'], json_params['version'], json_params['token'], json_params['ownerid'], json_params['domain'], count, offset)
			# root, sep, url, version, token, ownerid, domain, count, offset
			current_date = DateStamp.stampToDate(post[count-1][json_params['data']])
			out_posts.extend(post)
			offset += count
		Files.read_write_json(json_file, 'w', out_posts)

	@classmethod
	def get_album(cls, root, sep, url, version, token, ownerid, albumid):
		response = requests.get(url,
								params={
											'v': version,
											'access_token': token,
											'owner_id': ownerid,
											'album_id': albumid
										}
								)
		data = response.json()
		if len(root) >= 1:
			for item in root.split(sep):
				data = data[item]
		return data

	@classmethod
	def save_album(cls, json_params):
		data = DataSet()
		on_url = cls.get_album(json_params['root'], json_params['sep'], json_params['album_url'], json_params['version'], json_params['token'], json_params['ownerid'], json_params['album_id'])
		album_name = data.GenPostName.parent.joinpath(f"album-{json_params['album_id']}.json")
		json_params['album_name'] = str(album_name.resolve())
		Files.read_write_json(json_params['album_name'], 'w', on_url)
		return on_url

	@classmethod
	def AlbumProcess(cls, attach_param, elem_type, attach_obj):
		data = DataSet()
		obj_param = attach_param['attach'].get(elem_type, '')
		ext_file = obj_param['ext']
		if obj_param != '':
			if obj_param['download']:
				if not obj_param['isone']:
					for imgs in attach_obj:
						obj_list = ''
						if len(obj_param['list'].split(data.sep)) > 1 and type(imgs.get(obj_param['list'].split(data.sep)[0], dict())) == dict:
							obj_list = imgs.get(obj_param['list'].split(data.sep)[0], {})
							for k in range(1, len(obj_param['list'].split(data.sep)), 1):
								obj_list = obj_list.get(obj_param['list'].split(data.sep)[k], {})
						else:
							obj_list = imgs.get(obj_param['list'], '')
						if obj_list != '':
							image_url = cls.GetMaxImage(attach_param['image'], obj_list)
							image_name = data.GenImageName
							cls.DownloadFiles(image_name, ext_file, image_url)
							data.fcount.c4()
							if data.isresized:
								if data.width < data.max_width:
									Files.ResizeImage(data.fullname_filesaved, data.fullname_filesaved, data.width, data.height)
								if data.height < data.max_height:
									Files.ResizeImage(data.fullname_filesaved, data.fullname_filesaved, data.width, data.height)
				else:
					obj_list = attach_obj.get(obj_param['list'], '')
					if obj_list != '':
						image_url = cls.GetMaxImage(attach_param['image'], obj_list)
						image_name = data.GenImageName
						cls.DownloadFiles(image_name, ext_file, image_url)
						data.fcount.c4()
						if data.isresized:
							if data.width < data.max_width:
								Files.ResizeImage(data.fullname_filesaved, data.fullname_filesaved, data.width, data.height)
							if data.height < data.max_height:
								Files.ResizeImage(data.fullname_filesaved, data.fullname_filesaved, data.width, data.height)

	@classmethod
	def GetMaxImage(cls, json_params, onimage):
		data = DataSet()
		width = onimage[0].get(json_params['width'], 0)
		height = onimage[0].get(json_params['height'], 0)
		out_url = onimage[0].get(json_params['url'], '')
		for i in range(0, len(onimage), 1):
			if width < onimage[i].get(json_params['width'], 0):
				width = onimage[i].get(json_params['width'], 0)
				height = onimage[i].get(json_params['height'], 0)
				out_url = onimage[i].get(json_params['url'], '')
			if height < onimage[i].get(json_params['width'], 0):
				width = onimage[i].get(json_params['width'], 0)
				height = onimage[i].get(json_params['height'], 0)
				out_url = onimage[i].get(json_params['url'], '')
		data.max_width = width
		data.max_height = height
		return out_url

	@classmethod
	def ProcessImage(cls, attach_param, attach_obj, elem_type):
		data = DataSet()
		obj_param = attach_param['attach'].get(elem_type, '')
		ext_file = obj_param['ext']
		if obj_param != '':
			if obj_param['download']:
				if not obj_param['isone']:
					obj_list = ''
					if len(obj_param['list'].split(data.sep)) > 1 and type(attach_obj.get(obj_param['list'].split(data.sep)[0], dict())) == dict:
						obj_list = attach_obj.get(obj_param['list'].split(data.sep)[0], {})
						for k in range(1, len(obj_param['list'].split(data.sep)), 1):
							obj_list = obj_list.get(obj_param['list'].split(data.sep)[k], {})
					else:
						obj_list = attach_obj.get(obj_param['list'], '')
					if obj_list != '':
						image_url = cls.GetMaxImage(attach_param['image'], obj_list)
						image_name = data.GenImageName
						cls.DownloadFiles(image_name, ext_file, image_url)
						if data.isresized:
							if data.width < data.max_width:
								Files.ResizeImage(data.fullname_filesaved, data.fullname_filesaved, data.width, data.height)
							if data.height < data.max_height:
								Files.ResizeImage(data.fullname_filesaved, data.fullname_filesaved, data.width, data.height)
				else:
					obj_list = ''
					if len(obj_param['list'].split(data.sep)) > 1 and type(attach_obj.get(obj_param['list'].split(data.sep)[0], dict())) == dict:
						obj_list = attach_obj.get(obj_param['list'].split(data.sep)[0], {})
						for k in range(1, len(obj_param['list'].split(data.sep)), 1):
							obj_list = obj_list.get(obj_param['list'].split(data.sep)[k], {})
					else:
						obj_list = attach_obj.get(obj_param['list'], '')
					if obj_list != '':
						image_url = obj_list
						image_name = data.GenImageName
						cls.DownloadFiles(image_name, ext_file, image_url)
						if data.isresized:
							if data.width < data.max_width:
								Files.ResizeImage(data.fullname_filesaved, data.fullname_filesaved, data.width, data.height)
							if data.height < data.max_height:
								Files.ResizeImage(data.fullname_filesaved, data.fullname_filesaved, data.width, data.height)
				data.fcount.c4()	

	@classmethod
	def OtherProcess(cls, attach_param, attach_obj):
		data = DataSet()
		if attach_param['download']:
			ext_file = attach_param['ext']
			if attach_param['isone']:
				obj_file_name = data.GenImageName
				ext_file = attach_obj.get(attach_param['ext'], attach_param['ext'])
				obj_url = ''
				if len(attach_param['list'].split(data.sep)) > 1 and type(attach_obj.get(attach_param['list'].split(data.sep)[0], dict())) == dict:
					obj_url = attach_obj.get(attach_param['list'].split(data.sep)[0], {})
					for k in range(1, len(attach_param['list'].split(data.sep)), 1):
						obj_url = obj_url.get(attach_param['list'].split(data.sep)[k], {})
				else:
					obj_url = attach_obj.get(attach_param['list'], '')
				if obj_url != '':
					cls.DownloadFiles(obj_file_name, ext_file, obj_url)
			else:
				question = attach_obj.get(attach_param['list'].split(data.sep)[0], '')
				if question != '':
					post_file_name = data.GenPostName
					out_text = ''
					for elem in question:
						for k in range(1, len(attach_param['list'].split(data.sep)), 1):
							if 'http' in elem.get(attach_param['list'].split(data.sep)[k], ''):
								ext_file = elem.get(attach_param['ext'], attach_param['ext'])
								obj_file_name = data.GenImageName
								cls.DownloadFiles(obj_file_name, ext_file, elem.get(attach_param['list'].split(data.sep)[k], ''))
							else:
								out_text += Texts.GetOutText(elem.get(attach_param['list'].split(data.sep)[k], '')) + '\n'
					if data.istext:
						Files.read_write_text(post_file_name, 'a', f"{out_text}\r\n")
			data.fcount.c4()
		else:
			if attach_param['list'] != '':
				if data.istext:
					post_file_name = data.GenPostName
					out_text = ''
					question = attach_obj.get(attach_param['list'].split(data.sep)[0], '')
					if question != '':
						for elem in question:
							for k in range(1, len(attach_param['list'].split(data.sep)), 1):
								out_text += elem.get(attach_param['list'].split(data.sep)[k], '') + '\r\n'
					Files.read_write_text(post_file_name, 'a', f"{out_text}\r\n")

	@classmethod
	def ProcessText(cls, attach_param, attach_obj):
		global number
		data = DataSet()
		if data.istext:
			post_file_name = data.GenPostName
			out_text = ''
			for item in attach_param['text']:
				get_elem = ''
				if len(item.split(data.sep)) > 1:
					get_elem = attach_obj.get(item, {})
					for ins in range(1, len(item.split(data.sep)), 1):
						get_elem = get_elem.get(item.split(data.sep)[ins], {})
				else:
					get_elem = attach_obj.get(item, '')
				out_text += Texts.GetOutText(str(get_elem)) + '\r\n'
			for item in attach_param['save']:
				if not 'http' in f"{item}" and len(item.split(data.sep)) > 1:
					out_text_two = attach_obj.get(item.split(data.sep)[0], {})
					for item_two in range(1, len(item.split(data.sep)), 1):
						out_text_two = out_text_two.get(item.split(data.sep)[item_two], {})
					out_text += Texts.GetOutText(str(out_text_two)) + '\n'
				elif attach_param['inner_post'] in f"{attach_obj.get(item, item)}" and 'http' in f"{attach_obj.get(item, item)}":
					inner_post_file = f"{data.GenPostName}-{number}.html"
					out_text_two = cls.get_inner_post(attach_obj.get(item, item))
					Files.read_write_text(inner_post_file, 'w', out_text_two)
					number+=1
				else:
					out_text += Texts.GetOutText(attach_obj.get(item, item))
			Files.read_write_text(post_file_name, 'a', f"{out_text}\r\n")
	
	@classmethod
	def AttachProcess(cls, attach_param, attach_obj):
		data = DataSet()
		data.sep = attach_param['sep']
		for j in range(0, len(attach_obj), 1):
			type_elem = attach_obj[j].get(attach_param['obj_type'], '')
			if type_elem != '':
				curr_elem = attach_obj[j].get(type_elem, '')
				if curr_elem != '':
					params = attach_param['attach'].get(type_elem, '')
					params['inner_post'] = attach_param['inner_post']
					if params != '':
						cls.ProcessText(params, curr_elem)
						if params['isimage']:
							if params['isalbum']:
								attach_param['album_id'] = curr_elem[params['save'][0]]
								album_data = cls.save_album(attach_param)
								cls.AlbumProcess(attach_param, type_elem, album_data)
							else:
								cls.ProcessImage(attach_param, curr_elem, type_elem)
						else:
							cls.OtherProcess(params, curr_elem)

	@classmethod
	def ProcessHashTags(cls, hashtag_url, onText):
		all_hashtags = Texts.GetHashTags(onText)
		urls_hashtags = [f"{hashtag_url}{x}" for x in all_hashtags]
		return urls_hashtags

	@classmethod
	def PostsProcess(cls, json_params, posts, signal_value = None):
		global stop_thread, progress_procent, progress_bar
		data = DataSet()
		data.datetrack.date_start = DateStamp.stampToStr(posts[0][json_params['data']], '%d.%m.%Y')
		post_file_name = ''
		copy_history_param = json_params['copy_history'].split(json_params['sep'])[0]
		
		N2 = len(posts)
		progress_procent = 0
		
		for i in range(0, len(posts), 1):
			data.datetrack.date_curr = DateStamp.stampToStr(posts[i][json_params['data']], '%d.%m.%Y')
			data.datetrack.full_curr = DateStamp.stampToStr(posts[i][json_params['data']], '%d.%m.%Y-%H:%M')
			
			progress_procent = int((i/N2)*100)
			
			if data.istext:
				post_file_name = data.GenPostName
				Files.read_write_text(post_file_name, 'a', f"\r\n-----------\r\n")
				if data.isurl:
					wall_url  = f"{json_params['wall']}{json_params['ownerid']}_{posts[i][json_params['id']]}"
					Files.read_write_text(post_file_name, 'a', f"{wall_url}\r\n-----------\r\n")
				
				Files.read_write_text(post_file_name, 'a', f"{data.datetrack.full_curr}\r\n-----------\r\n\r\n")
				
				the_text = Texts.GetOutText(posts[i][json_params['text']])
				Files.read_write_text(post_file_name, 'a', the_text)
				Files.read_write_text(post_file_name, 'a', f"\r\n")
				
				full_hashtags = cls.ProcessHashTags(json_params['hashtag'], the_text)
				for ht in full_hashtags:
					Files.read_write_text(post_file_name, 'a', f"\r\n{ht}\r\n")
			
			attch_elem = posts[i].get(json_params['attachments'], '')
			if attch_elem != '':
				cls.AttachProcess(json_params, attch_elem)
			
			if copy_history_param != '':
				copy_history_q = posts[i].get(copy_history_param, '')
				if copy_history_q != '':
					copy_history = posts[i].get(copy_history_param, {})
					if type(copy_history) == list:
						for item in copy_history:
							
							attch_elem = item.get(json_params['copy_history'].split(json_params['sep'])[1], '')
							if attch_elem != '':
								cls.AttachProcess(json_params, attch_elem)
							
							if data.istext:
								copy_history_text = item.get(json_params['copy_history_text'], '')
								if copy_history_text != '':
									Files.read_write_text(post_file_name, 'a', Texts.GetOutText(copy_history_text))
									Files.read_write_text(post_file_name, 'a', f"\r\n")
					
									full_hashtags = cls.ProcessHashTags(json_params['hashtag'], copy_history_text)
									for ht in full_hashtags:
										Files.read_write_text(post_file_name, 'a', f"\r\n{ht}\r\n")
					else:
						
						attch_elem = copy_history.get(json_params['copy_history'].split(json_params['sep'])[1], '')
						if attch_elem != '':
							cls.AttachProcess(json_params, attch_elem)
						
						if data.istext:
							copy_history_text = copy_history.get(json_params['copy_history_text'], '')
							if copy_history_text != '':
								Files.read_write_text(post_file_name, 'a', Texts.GetOutText(copy_history_text))
								Files.read_write_text(post_file_name, 'a', f"\r\n")
				
								full_hashtags = cls.ProcessHashTags(json_params['hashtag'], copy_history_text)
								for ht in full_hashtags:
									Files.read_write_text(post_file_name, 'a', f"\r\n{ht}\r\n")			
			if data.istext:
				Files.read_write_text(post_file_name, 'a', f"\r\n-----------\r\n")
			
			data.fcount('c3').ResetCounter('c4')
			
			if signal_value != None:
				signal_value.emit(progress_procent)
		stop_thread = True
		if signal_value != None:
			signal_value.emit(100)
