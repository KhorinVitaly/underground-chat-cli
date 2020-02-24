import asyncio
import configargparse
import logging
import json
from dotenv import load_dotenv
load_dotenv()


async def main(args):
    reader, writer = await asyncio.open_connection(args.host, args.port)
    await readline(reader)
    if args.token:
        await authorise(reader, writer, args.token)
        await submit_message(writer)
        await readline(reader)
        if args.message:
            await submit_message(writer, args.message)
        else:
            message = input('message: ')
            await submit_message(writer, message)
    else:
        await register(reader, writer, args.username)


async def authorise(reader, writer, token):
    await submit_message(writer, token)
    text = await readline(reader)
    try:
        json_data = json.loads(text)
    except ValueError:
        print('Неизвестный токен. Проверьте его или зарегистрируйтесь заново.')


async def register(reader, writer, username):
    await submit_message(writer, '')
    await readline(reader)
    if username:
        await submit_message(writer, username)
    else:
        username = input('nickname: ')
        await submit_message(writer, username)
    text = await readline(reader)
    try:
        json_data = json.loads(text)
        nickname = json_data['nickname']
        account_hash = json_data['account_hash']
        print(f'Ваш итоговый никнейм : {nickname}, персоональный hash токен {account_hash} сохраните его!')
    except ValueError:
        print('Что-то пошло не так. Попробуйте перезапустить регистрацию.')


async def submit_message(writer, text=''):
    text += '\n\n'
    logging.debug(f'Output: {text}')
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
    parser.add('--host', help='host for listening', env_var='MINECHAT_HOST')
    parser.add('--port', help='port for listening', env_var='MINECHAT_PORT_FOR_WRITING')
    parser.add('--log', help='file to logging input output', env_var='MINECHAT_LOG')
    parser.add('--username', help='username in minechat', env_var='USERNAME')
    parser.add('--token', help='personal hash token for auth', env_var='TOKEN')
    parser.add('--message', help='default message text', env_var='MESSAGE')
    args = parser.parse_args()
    if args.log:
        logging.basicConfig(filename=args.log, level=logging.DEBUG)
    try:
        asyncio.run(main(args))
    except TimeoutError:
        print('Нет соединения.')
    except KeyboardInterrupt:
        pass
