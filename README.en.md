# Telegram AI_GPT
## Изменить язык: [Русский](README.md)
***
Bot-advisor trained on own data, based on botsonic. Helps answer questions and make appointments.
## [LIVE](https://t.me/Inside_company_Bot)
## [DEMO](README.demo.md)
## Functionality:
1. Answers questions based on the context of the conversation
2. Accepts applications
3. Provides an opportunity to contact the manager
4. Implemented the mechanism of the request queue and the exponential growth of the response delay
5. Transfers user data to google sheets
## Commands:
**For convenience, it is recommended to add these commands to the side menu of the bot using [BotFather](https://t.me/BotFather).**
- restart - resets the history of correspondence with the bot;
- help - provides a list of available commands;

## Installation and use:
- Install dependencies:
```sh
pip install -r requirements.txt
```
- specify in the .env file:
   - Telegram bot token: **TELEBOT_TOKEN**=TOKEN
   - Bot ID: **BOT_ID**=ID (first digits from bot token, before :)
   - Manager username - the "manager" button will enter the specified profile: **MANAGER_USERNAME**=example (specified without @)
   - Google spreadsheet name: **SPREAD_NAME**=gpt
   - The name of the sheet on which the bot enters information: **LIST_BOT**=bids
   - botsonic token: **AI_TOKEN**=TOKEN
   - Endpoint botsoinc: **AI_ENDPOINT**=TOKEN
   - Message reset interval (in minutes): **RENEW_TIME**=2
   - Value for exponential delay calculation: **EXPONENT**=10.
- get file with credentials (connection parameters):\
https://console.cloud.google.com/ \
https://www.youtube.com/watch?v=bu5wXjz2KvU - instruction from 00:00 to 02:35\
Save the resulting file in the root of the project, with the name **service_account.json**
- provide service e-mail with access to the table (instruction in the video at the link above)
- run the project:
```sh
python3 main.py
```

## Features of use:
1. The header of the sheet with applications is filled in by the bot on its own, before starting it is enough to create a table and a sheet with the names specified in the .env file.