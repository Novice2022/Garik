# Garik – pc assistant (Release v. 1.0)

## Dev stack

### Python

* Modules
  * asyncio
  * json
  * subprocess
  * typing
  * webbrowser
  * pyautogui
  * pyperclip
  * keyboard
* Arcitecture – OOP with SOLID
* Metaclass (**Singleton** realisation)
* Voice models
  * vosk (Russian lite version)
  * google recognition

### **C#**

* Development
  * asynchronous
  * multyprocessing
* WPF
  * **MVVM** pattern

### PostgreSQL

## Installing details

1) Before cloning the repository You must be located in `C:\Projects\Garik\`
2) You have to restore database on you local pc with  `Garik\Database\Migration.sql` file (just run as DDL SQL code)
3) Edit passowrd in `C:\Projects\Garik\Application\Garik\Backend\DataBase.cs` at line 13 to Your PostgreSQL password for `postgre` - (default) superuser and edit user to the same user (`postgre`)
4) [Setup JetBrains Mono](https://www.jetbrains.com/lp/mono/) font on your PC to use Garik how it's conceived.

**By Garik – [t.me\Garik_Novice2022](https://t.me/Garik_Novice2022)**
