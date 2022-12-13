This script - demonstration of working with Api Monobank. It allows you to make balance top up in telegram bot from any Ukrainian card, or just through google pay. First you need to install the latest version of python, and the necessary libraries

>pip install pyTelegramBotAPI

>pip install monobank

>pip install requests

Next, through any code editor open the file config.py and configure it. tg - API token telegram bot, which you can get in the bot @botfather. admin - admin admin bot, you can get it in the bot @userinfobot. Api_mono - monobank API token, which can be obtained here https://api.monobank.ua . And link_mono - link to the jar, which you can get inside the application
To start the project - just run main.py through python
The script was implemented through a comment. When you first run the bot - a person entered into the database, in the column "Code" is written to him randomly generated kommentariy. Every 2 minutes the bot receives the bank statement and cycles through all the payment comments. If the comment coincides with a comment of some person from the database, the bot will credit the received amount to the user's balance, and also creates a new comment and assigns it to the person

