# PySwitch
PySwitch 是一个为 Windows 安装了多个 Python 环境提供快速切换的软件


## 使用
### 使用帮助

您在首次运行 pys 时，请先进行初始化（双击软件/pys --init），然后添加 Python 环境（使用 pys -a version=path）。
接着您就可以使用 pys 在 windows 上愉快的切换 Python 环境了。

### 参数
> -h/--help       : 使用帮助
> 
> -v/--version    : 软件版本信息
> 
> -a/--add        : 添加 Python 环境（version=path）
> 
> -r/--remove     : 删除 Python 环境 (version)
> 
> -u/--use        : 切换系统运行 Python 环境
> 
> --init          : 初始化
> 
> --py-version    : 当前系统运行 Python 版本 

### 使用范例
```bash
pys -u 3.7.2
```

## 安装
1. 下载 pys.exe 文件到本地
2. 双击 pys.exe 进行初始化
3. 添加已经安装 Python 环境


**注：** 如出现权限错误，请手动为 pys.exe 添加管理员权限，属性 -> 兼容性 -> 以管理员身份运动

![添加管理员权限](./set_admin.png)

