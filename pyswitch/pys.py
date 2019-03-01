# -*- coding: utf-8 -*-


from __future__ import print_function
import os
import getopt
import sys
import bats
import time
import const
import admin



# 配置文件名
BAT_SAVE = False
CONFIG_FILE_NAME = 'config.conf'
CONFIG_SECTION_APP = 'app'
CONFIG_SECTION_ENVS = 'py_envs'

# 路径
FILE_PATH = os.path.abspath(sys.argv[0]);
if os.path.splitext(FILE_PATH)[1] == '.py':
	BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
else:
	BASE_PATH = os.path.dirname(os.path.realpath(sys.executable))
CONFIG_FILE_PATH = os.path.join(BASE_PATH, CONFIG_FILE_NAME)
TMPS_PATH = os.path.join(BASE_PATH, 'tmps')
BATS_PATH = TMPS_PATH

# Env 路径
SCRIPT_RUN_PATH = BASE_PATH
PYTHON_RUN_PATH = os.path.join(BASE_PATH, 'use')
PYTHON_SCRIPT_RUN_PATH = os.path.join(BASE_PATH, ('use' + os.path.sep + 'Scripts'))


# =================================
# 命令行
# =================================
class Cmder:

	def __init__(self):
		pass

	# 运行 cmd 命令
	def runcmd(self, cmd):
		time.sleep(0.1)
		print(u'执行命令：%s' % cmd)
		execute = os.popen(cmd)
		result = execute.read()
		print(result)
		return result


	# 连续运行多条 cmd 命令
	def runcmds(self, cmds):
		time.sleep(0.1)
		tmp_bat_file = os.path.join(BATS_PATH, 'tmp-' + str(time.time()) + '.bat')
		cmds = [cmd + '\n' for cmd in cmds]
		with open(tmp_bat_file, 'w') as f:
			f.writelines(cmds)
		self.runcmd(tmp_bat_file)
		self._remove_bat(tmp_bat_file)


	# 连续运行 bat 命令
	def runbat(self, bat):
		time.sleep(0.1)
		tmp_bat_file = os.path.join(BATS_PATH, 'tmp-' + str(time.time()) + '.bat') 
		with open(tmp_bat_file, 'w') as f:
			f.writelines(bat)
		self.runcmd(tmp_bat_file)
		self._remove_bat(tmp_bat_file)


	# 删除 bat 文件
	def _remove_bat(self, file):
		if not BAT_SAVE:
			time.sleep(2)
			os.remove(file)


	# 添加用户环境变量

	def append_user_env(self, key, value):
		self._append_env(False, key, value)
	

	# 添加系统环境变量
	def append_sys_env(self, key, value):
		self._append_env(True, key, value)

	# 添加环境变量
	def _append_env(self, is_sys, key, value):
		# 运行设置环境变量命令
		user = 'sys' if is_sys else 'me'
		cmds = bats.ADD_ENV.format(user=user, key=key, value=value)
		self.runbat(cmds)

	
	# 设置系统环境变量
	def set_sys_env(self, key, value):
		self._set_env(True, key, value)

	
	# 设置用户环境变量
	def set_user_env(self, key, value):
		self._set_env(False, key, value)


	# 设置环境变量
	def _set_env(self, is_sys, key, value):
		user = 'sys' if is_sys else 'me'
		cmds = bats.SET_ENV.format(user=user, key=key, value=value)
		self.runbat(cmds)
		


# =================================
# Python 环境
# =================================
class PyEnv:
	def __init__(self, cp, cp_name, section):
		self.cp = cp
		self.cp_name = cp_name
		self.section = section

	def list(self):
		return self.cp.items(self.section)

	def keys(self):
		return self.cp.options(self.section)

	def add(self, key, value):
		self.cp.set(self.section, key, value)
		self.cp.write(open(self.cp_name, 'w'))

	def remove(self, key):
		self.cp.remove_option(self.section, key)
		self.cp.write(open(self.cp_name, 'w'))



# =============== Main ===============

# 检测 [Tmps, Bats] 文件夹是否存在
if not os.path.exists(TMPS_PATH):
	os.mkdir(TMPS_PATH)
if not os.path.exists(BATS_PATH):
	os.mkdir(BATS_PATH)

# 检测是否存在配置文件，不存在则创建
if not os.path.exists(CONFIG_FILE_PATH):
	conf_strs = [
		'[app]',
		'init = False',
		'env_path = %s' % PYTHON_RUN_PATH,
		'env_cur = ',
		'',
		'[py_envs]',
		'system = system'
	]
	# 创建配置文件
	with open(CONFIG_FILE_PATH, 'w') as f:
		f.writelines([x + '\n' for x in conf_strs])

# 读取配置文件
if sys.version_info > (3, 0):
	import configparser
	cp = configparser.ConfigParser()
else:
	import ConfigParser
	cp = ConfigParser.SafeConfigParser()
cp.read(CONFIG_FILE_PATH)

cmder = Cmder()
pyenv = PyEnv(cp, CONFIG_FILE_PATH, CONFIG_SECTION_ENVS)



"""return list
版本列表
"""
def list_versions():
	return pyenv.list()


"""return version
Python 版本
"""
def py_version():
	return cp.get(CONFIG_SECTION_APP, 'env_cur')


""" return 
打印版本列表
"""
def print_list_versions():
	versions = sorted(list_versions())
	if len(versions) <= 0:
		print('您未配置/安装任何版本')
	for (key, value) in versions:
		if key == py_version():
			print('v %s *' % key)
		else:
			print('v %s' % key)


"""
打印当前 Python 版本
"""
def print_py_version():
	cur_version = py_version()
	if cur_version:
		print('v %s' % cur_version)
	else:
		print(u'当前为系统指定版本')

"""
添加 python 环境
"""
def add_py_env(env):
	if len(env) != 2:
		print(u'您输入的格式有误')
	elif not os.path.exists(env[1]):
		print(u'您输入的路径不存在')
	else:
		pyenv.add(env[0], env[1])
		print(u'添加成功')


"""
删除 python 环境
"""
def remove_py_env(key):
	if key not in pyenv.keys():
		print(u'您未配置/安装该版本')
	elif key == 'system':
		print(u'无法删除该版本')
	else:
		pyenv.remove(key)
		print(u'删除成功')


"""
切换前检查
"""
def switch_check(version):
	# if not admin.is_admin():
	# 	print(u'请以管理员权限运行')
	# 	return False
	if version not in pyenv.keys():
		print(u'您未配置/安装该版本，请先进行安装')
		return False
	if version == py_version():
		print(u'当前已是 %s' % version)
		return False
	return True


"""
切换环境
"""
def switch_path(version):
	if not switch_check(version):
		sys.exit(0)

	# 路径
	e_path = cp.get(CONFIG_SECTION_APP, 'env_path')
	p_path = cp.get(CONFIG_SECTION_ENVS, version)

	if os.path.exists(e_path):
		# 如果已存在该软件链接文件，则删除
		cmder.runcmd(r'rd %s' % e_path )

	if version != 'system':
		# 创建软件链接
		cmder.runbat(bats.SWITCH_PYTHON.format(e_path, p_path))
	# 保存版本信息
	cp.set(CONFIG_SECTION_APP, 'env_cur', version)
	cp.write(open(CONFIG_FILE_PATH, 'w'))
	# 打印提示信息
	print(u'已成功切换至：Python %s' % version)



"""
添加运行环境
"""
def __add_run_path():
	path_env_str = os.getenv('PY_SWITCH')
	if (path_env_str is None) or (BASE_PATH not in path_env_str):
		cmder.append_user_env('PY_SWITCH', BASE_PATH)
	if (path_env_str is None) or (PYTHON_RUN_PATH not in path_env_str):
		cmder.append_user_env('PY_SWITCH', PYTHON_RUN_PATH)
	if (path_env_str is None) or (PYTHON_SCRIPT_RUN_PATH not in path_env_str):
		cmder.append_user_env('PY_SWITCH', PYTHON_SCRIPT_RUN_PATH)
	if (r'%PY_SWITCH%' not in os.getenv('path')):
		cmder.append_user_env('path', '%%PY_SWITCH%%')


"""
初始化
"""
def __init():
	# 添加环境变量
	__add_run_path()
	print(u'初始化完成')
	# 设置已初始化
	cp.set(CONFIG_SECTION_APP, 'init', 'True')
	cp.write(open(CONFIG_FILE_PATH, 'w'))



if __name__ == '__main__':

	# 未初始化
	if not cp.getboolean(CONFIG_SECTION_APP, 'init'):
		__init()
		sys.exit()


	# 参数
	try:
		opts, args = getopt.getopt(sys.argv[1:], "a:r:u:hvl", ['init', 'py-version', 'add', 'remove', 'use=', 'help', 'version', 'list'])

		if len(opts) > 0:
			for op, value in opts:
				if op in ("-h", "--help"):
					print(const.help)
					sys.exit()
				elif op in ("-v", "--version"):
					print(const.version)
					sys.exit()
				elif op in ("--init"):
					__init()
					sys.exit()
				elif op in ("-l", "--list"):
					print_list_versions()
					sys.exit()
				elif op in ("--py-version"):
					print_py_version()
					sys.exit()
				elif op in ("-a", "--add"):
					env = value.split('=')
					add_py_env(env)
				elif op in ("-r", "--remove"):
					remove_py_env(value.split('=')[0])
				elif op in ("-u", "--use"):
					switch_path(value)
					sys.exit()
				else:
					print(const.help)
		else:
			print(u'请输入需要切换的版本号')
	except getopt.GetoptError as err:
		print(const.help)
		sys.exit(1)


