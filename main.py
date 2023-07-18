import argparse
import requests
import time
from environs import Env
import telegram
import logging


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(process)d %(levelname)s %(message)s",
                        filename='/opt/Work_review_notifications/bot.log')
    logging.getLogger(__name__)
    logging.info('INFO')
    logging.warning('WARNING')
    logging.error('ERROR')
    logging.critical('CRITICAL')

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
    while True:
        try:
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
            print('Время ожидания вышло')
        except requests.exceptions.ConnectionError:
            print('Ошибка сети')
            time.sleep(5)


if __name__ == '__main__':
    main()