import asyncio
import configargparse
import logging
import json
import bleach
from dotenv import load_dotenv
load_dotenv()


SPECIAL_SYMBOLS_FOR_MARKING_END_OF_MESSAGE = '\n\n'


async def main(args):
    reader, writer = await asyncio.open_connection(args.host, args.port)
    await readline(reader)
    try:


        await submit_message(writer)
        await readline(reader)
        if not args.message:
            message = input('message: ')
        await submit_message(writer, message)
    finally:
        writer.close()


async def is_authenticated(args, reader, writer):
    if not args.token:
        nickname, account_hash = await register(reader, writer, args.username)
        if not nickname:
            print('Что-то пошло не так. Попробуйте перезапустить регистрацию.')
            return
        print(f'Ваш итоговый никнейм: {nickname}, ваш персоональный hash токен: {account_hash} сохраните его!')
        return
    nickname = await authorise(reader, writer, args.token)
    if not nickname:
        print('Неизвестный токен. Проверьте его или зарегистрируйтесь заново.')
        return False
    print(f'Вы авторизованы как: {nickname}')
    return True


async def authorise(reader, writer, token):
    await submit_message(writer, token)
    text = await readline(reader)
    try:
        json_data = json.loads(text)
        return json_data['nickname']
    except ValueError:
        return None


async def register(reader, writer, username):
    await submit_message(writer, '')
    await readline(reader)
    if not username:
        username = input('Введите имя пользователя для регистрации: ')
    await submit_message(writer, username)
    text = await readline(reader)
    try:
        json_data = json.loads(text)
        return json_data['nickname'], json_data['account_hash']
    except ValueError:
        return None, None


async def submit_message(writer, text=''):
    logging.debug(f'Output: {text}')
    text = bleach.clean(text)
    text += SPECIAL_SYMBOLS_FOR_MARKING_END_OF_MESSAGE
    data = text.encode('utf-8')
    writer.write(data)
    await writer.drain()


async def readline(reader):
    data = await reader.readline()
    text = data.decode()
    logging.debug(f'Input: {text}')
    return text


if __name__ == '__main__':
    parser = configargparse.ArgParser()
    parser.add('--host', help='Адрес сервера minechat', env_var='MINECHAT_HOST')
    parser.add('--port', help='Порт для отправки сообщений', env_var='MINECHAT_PORT_FOR_WRITING')
    parser.add('--log', help='Путь к файлу для логирования ввода / вывода', env_var='MINECHAT_LOG')
    parser.add('--username', help='Имя пользователя по умолчанию', env_var='USERNAME')
    parser.add('--token', help='Персоональный hash токен для авторизации', env_var='TOKEN')
    parser.add('--message', help='Текст сообщения по умолчанию', env_var='MESSAGE')
    args = parser.parse_args()
    if args.log:
        logging.basicConfig(filename=args.log, level=logging.DEBUG)
    try:
        asyncio.run(main(args))
    except TimeoutError:
        print('Нет соединения.')
    except KeyboardInterrupt:
        pass
