@REM 静默删除已存在的可执行程序
if exist dist (
	del /q .\dist
)

@REM 打包，程序入口为app.py，程序图标为icon.ico，打包模式为隐藏控制台（-w），单文件（-F）
Pyinstaller -F -w app.py -i icon.ico

@REM 静默复制图片到打包文件夹
@REM icon.png是程序在任务栏、任务管理器中的图标
@REM icon32.png是自定义标题栏左上角的图标
@REM close.png是自定义标题栏右上角的关闭图标
@REM min.png是自定义标题栏右上角的最小化图标
copy /y .\icon.png .\dist
copy /y .\icon32.png .\dist
copy /y .\close.png .\dist
copy /y .\min.png .\dist

@REM 静默递归删除打包临时文件
rd /s /q .\build

