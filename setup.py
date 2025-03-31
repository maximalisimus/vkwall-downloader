from setuptools import setup, find_packages
from os.path import join, dirname

# python -m pip install --upgrade pip
# python -m pip install pip setuptools virtualenv virtualenvwrapper-win --upgrade pip setuptools virtualenv virtualenvwrapper-win

#Debian: $ sudo apt install python-virtualenv python3-virtualenv python3-venv virtualenv python3-virtualenvwrapper python-distlib python-filelock python3-platformdirs python-stevedore
#Archlinux: $ sudo pacman -S python-distlib python-filelock python-platformdirs python-stevedore python-virtualenv python-virtualenvwrapper
#Python PIP: $ python -m pip install --upgrade pip setuptools distlib filelock platformdirs stevedore virtualenv virtualenvwrapper --upgrade
#Windows PIP / PIP: $ pip install setuptools virtualenv virtualenvwrapper-win --upgrade

## Package
# pip install pyinstaller pillow requests keyring pyqt5 pyqt5-tools

# $ pyinstaller main.py

# --onefile — сборка в один файл, т.е. файлы .dll не пишутся.
# --windowed -при запуске приложения, будет появляться консоль.
# --noconsole — при запуске приложения, консоль появляться не будет.
# --icon=app.ico — добавляем иконку в окно.
# --paths — возможность вручную прописать путь к необходимым файлам, если pyinstaller
# не может их найти(например: --paths D:\python35\Lib\site-packages\PyQt5\Qt\bin)

# $ pyinstaller --onefile --noconsole --icon=image/vk-icon.ico --paths image/ --paths forms/ --paths pyvkwall/ main.py

# python setup.py sdist bdist_wheel
# python setup.py install
# pip install .

setup(
    name='pyvkwall',
    version='1.0.0',
    long_description=open(join(dirname(__file__), 'README.md'),  encoding='utf-8').read(),
    author='Mikhail Artamonov',
    author_email='maximalis171091@yandex.ru',
    url='https://github.com/maximalisimus/pyvkwall.git',
    packages=find_packages(include=['pyvkwall', '*.py']),
    include_package_data=True,
    entry_points={
        'console_scripts': ['pyvkwall=pyvkwall.vkwall:run']
    },
    keywords = ["pyvkwall", "vk", "wall", 'download'],
	classifiers = [
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Development Status :: 3 public release",
		"License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE Version 3 (GPL3)",
		"Operating System :: Linux",
		"Operating System :: Windows",
		"Topic :: Utilities",
		],
	python_requires='>=3.10',
	install_requires=[
        'requests',
        'pillow',
        'keyring',
        'pyqt5',
        'pyqt5-tools'
    ],
)
