import argparse
import requests
import time
from environs import Env
import telegram
import logging


logger = logging.getLogger('Бот логер')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
                        #filename='/opt/Work_review_notifications/bot.log')
    logger.setLevel(logging.DEBUG)
    env = Env()
    env.read_env()
    telegram_token = env.str('TELEGRAM_TOKEN')
    api_key = env.str('DEVMAN_API_KEY')
    chat_id = env.int('TG_CHAT_ID')
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', help='Укажите ваш id', type=int, default=chat_id)
    bot = telegram.Bot(token=telegram_token)
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {api_key}'}
    params = {'timestamp': ''}
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info('Бот запущен')
    while True:
        try:
            x = 10 / 0
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            review_information = response.json()
            if review_information['status'] == 'found':
                params['timestamp'] = review_information['last_attempt_timestamp']
                if review_information['new_attempts'][0]['is_negative']:
                    bot.send_message(text=f'''У вас проверили работу '{review_information['new_attempts'][0]['lesson_title']}'.\
                                              К сожалению в работе нашлись ошибки. Ссылка на работу\
                                              {review_information['new_attempts'][0]['lesson_url']}''', chat_id=chat_id)
                else:
                    bot.send_message(text=f'''У вас проверили работу '{review_information['new_attempts'][0]['lesson_title']}'.\
                                              Преподавателю все понравилось, можно приступать к следующему уроку!''', chat_id=chat_id)
        except requests.exceptions.Timeout:
            logger.error('Время ожидания вышло')
        except requests.exceptions.ConnectionError:
            logger.error('Ошибка сети')
            time.sleep(5)
        except Exception as error:
            logger.exception(f'Бот упал с ошибкой: {error}')


if __name__ == '__main__':
    main()