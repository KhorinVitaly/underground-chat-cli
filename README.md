# Underground chat CLI

Пример реализации взаидойствения с чатом на TCP сокетах с помощью Python и asyncio.

Содержит два скрипта: listen_minechat.py для отслеживания истории чата и minechat_client.py 
для подключения к чату и отправки сообщений.

## Как установить

Для работы скриптов нужен Python версии не ниже 3.7. Для установки необходимых зависимостей, в терминале 
наберите команду:

```bash
pip install -r requirements.txt
```

## Как запустить 

Для запуска скрипта для отслеживания истории чата, в терминале наберите команду:

```bash
python listen_minechat.py
```

Для подключения к чату и отправки сообщения:

```bash
python minechat_client.py
```

### Параметры и переменные окружения

При запуске скрипта listen_minechat.py вы можете указать следующие необязательные параметры:
* --host - адрес сервера чата;
* --port - соответственно порт для отслеживания истории;
* --history - путь к файлу для логирования истории чата.

```bash
python listen_minechat.py --host minechat.dvmn.org --port 5000 --history ./chat_hystory.log
```

Альтернативной явдяется установка переменных окружения: 
* MINECHAT_HOST 
* MINECHAT_PORT_FOR_LISTENING
* MINECHAT_HISTORY

```bash
export MINECHAT_HOST=minechat.dvmn.org && export MINECHAT_PORT_FOR_LISTENING=5000
```

Также при запуске minechat_client доступны следующие параметры:
* --host - адрес сервера чата;
* --port - соответственно порт для подключения;
* --log - путь к файлу для логирования истории ввода / вывода, что помогает в отладке скрипта;
* --username - имя пользователя, которое будет использоваться по умолчанию для регистрации;
* --token - персоональный hash токен необходимый для авторизации уже существующего пользователя;
* --message - текст сообщения для отправки в чат.

```bash
python listen_minechat.py --host minechat.dvmn.org --port 5050 --username Pepe --message 'Всем привет в этом чатике!'
```

Альтернативной также явдяется установка соответствующих переменных окружения: 
* MINECHAT_HOST 
* MINECHAT_PORT_FOR_WRITING
* MINECHAT_LOG
* USERNAME
* TOKEN
* MESSAGE

```bash
export MINECHAT_HOST=minechat.dvmn.org && export MINECHAT_PORT_FOR_WRITING=5050
```

Также поддерживается использование .env файлов для описания переменных окружения:
```
MINECHAT_HOST=minechat.dvmn.org
MINECHAT_PORT_FOR_LISTENING=5000
MINECHAT_PORT_FOR_WRITING=5050
MINECHAT_HISTORY=./chat.log
```

# Цели проекта

Код написан в учебных целях — это урок в курсе по Ассинхронному программированию на Python на сайте [Devman](https://dvmn.org)..