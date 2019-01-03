import os
from src.coderunbot import CodeRunBot


API_TOKEN = '782542203:AAHz3rCUYBgHW_WePqy6F47jGxg1g9FtAuQ'

# webhook settings
WEBHOOK_HOST = 'https://code-run-bot.herokuapp.com'
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT')

if __name__ == '__main__':
    code_run_bot = CodeRunBot(API_TOKEN, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_HOST, WEBHOOK_PATH)
    code_run_bot.run()