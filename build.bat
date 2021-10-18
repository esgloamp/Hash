@REM 静默删除已存在的可执行程序
if exist dist (
	del /q .\dist
)

@REM 打包，程序入口为app.py，程序图标为icon.ico，打包模式为隐藏控制台（-w），单文件（-F）
Pyinstaller -F -w app.py -i .\assets\icon.ico

@REM 创建资源文件夹
if not exist .\dist\assets (
	mkdir .\dist\assets
)
@REM 静默复制图片到打包文件夹
@REM icon.png是程序在任务栏、任务管理器中的图标
@REM icon32.png是自定义标题栏左上角的图标
@REM close.png是自定义标题栏右上角的关闭图标
@REM min.png是自定义标题栏右上角的最小化图标
copy /y .\assets\icon.png .\dist\assets
copy /y .\assets\icon32.png .\dist\assets
copy /y .\assets\close.png .\dist\assets
copy /y .\assets\min.png .\dist\assets

@REM 静默递归删除打包临时文件
rd /s /q .\build

