# -*- coding: utf-8 -*-

SET_ENV=r'''
@echo
set %{key}%={value}
echo %{key}%

if {user}==sys (
	setx /M｛key｝ "%{key}%"
) else (
	setx {key} "%{key}%"
)
'''


ADD_ENV=r'''
@echo off

if {user}==sys (
	set regPath= HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session" "Manager\Environment
) else (
	set regPath= HKEY_CURRENT_USER\Environment
)

set key={key}
set value={value}
:: 判断是否存在该路径
reg query %regPath% /v %key% 1>nul 2>nul
if %ERRORLEVEL%==0 (
	:: 取值
	For /f "tokens=3* delims= " %%i in ('Reg Query %regPath% /v %key% ') do (
		if "%%j"=="" (Set oldValue=%%i) else (Set oldValue=%%i %%j)
	)
) else Set oldValue="."

:: 备份注册表
reg export %regPath% %~dp0%~n0.reg
:: 写入环境变量
if "%oldValue%"=="." (
	reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%value%" /f
) else (
	reg add %regPath% /v %key% /t REG_EXPAND_SZ /d "%oldValue%;%value%" /f
)
'''

SWITCH_PYTHON=r'''
@echo off

:init
 setlocal DisableDelayedExpansion
 set cmdInvoke=1
 set winSysFolder=System32
 set "batchPath=%~0"
 for %%k in (%0) do set batchName=%%~nk
 set "vbsGetPrivileges=%temp%\OEgetPriv_%batchName%.vbs"
 setlocal EnableDelayedExpansion

:checkPrivileges
  NET FILE 1>NUL 2>NUL
  if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
  if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)

  ECHO Set UAC = CreateObject^("Shell.Application"^) > "%vbsGetPrivileges%"
  ECHO args = "ELEV " >> "%vbsGetPrivileges%"
  ECHO For Each strArg in WScript.Arguments >> "%vbsGetPrivileges%"
  ECHO args = args ^& strArg ^& " "  >> "%vbsGetPrivileges%"
  ECHO Next >> "%vbsGetPrivileges%"

  if '%cmdInvoke%'=='1' goto InvokeCmd 

  ECHO UAC.ShellExecute "!batchPath!", args, "", "runas", 1 >> "%vbsGetPrivileges%"
  goto ExecElevation

:InvokeCmd
  ECHO args = "/c """ + "!batchPath!" + """ " + args >> "%vbsGetPrivileges%"
  ECHO UAC.ShellExecute "%SystemRoot%\%winSysFolder%\cmd.exe", args, "", "runas", 1 >> "%vbsGetPrivileges%"

:ExecElevation
 "%SystemRoot%\%winSysFolder%\WScript.exe" "%vbsGetPrivileges%" %*
 exit /B

:gotPrivileges
 setlocal & cd /d %~dp0
 if '%1'=='ELEV' (del "%vbsGetPrivileges%" 1>nul 2>nul  &  shift /1)

mklink /d {0} {1}

'''

