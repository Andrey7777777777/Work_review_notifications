# Бот проверки статуса домашних заданий на сайте dvmn.org

 ## Запуск

 - Скачайте код. Установите зависимости:
 ```sh
pip install -r requirements.txt
```
- Создайте файл с переменными окружения ".env" рядом с main.py и запишите туда данные в таком формате: ПЕРЕМЕННАЯ=значение.
Переменные окружения:
- TELEGRAM_TOKEN - токен телеграм бота, инструкция по созданию бота: https://medium.com/spidernitt/how-to-create-your-own-telegram-bot-63d1097999b6
- DEVMAN_API_KEY - токен сайта dvmn.org: https://dvmn.org/api/docs/
- TG_CHAT_ID - Ваш id в телеграмме, для получения id напишите боту по ссылке: https://telegram.me/userinfobot
Запуск бота с id указанным в переменной окружения:
```sh
python main.py
```
Также можно явно указать id в командной строке:
```sh
python main.py 123456789
```
 Чтобы бот начал вам присылать уведомления о проверке домашних заданий, необходимо отправить ему любое сообщение.

## Запуск через Docker

 - Установите Docker по инструкции в зависимости от вашей операционной системы: https://docs.docker.com/engine/install/


 - создать образ:

 ```commandline
 docker build -t work_review_notifications .
 ```
 - Запуск контейнера с учетом переменного окружения:
 ```commandline
 docker run -p 3001:8001 --env-file .env --name devman_bot_1 work_review_notifications 
 ```

## Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](https://dvmn.org).