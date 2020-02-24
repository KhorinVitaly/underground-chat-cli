import asyncio
from aiofile import AIOFile
import datetime
import configargparse
from dotenv import load_dotenv
load_dotenv()


async def connection_holder(args):
    while True:
        try:
            reader, writer = await asyncio.open_connection(args.host, args.port)
            await listen_chat(reader)
        except TimeoutError:
            print('Нет соединения. Повторная попытка через 3 сек.')
            await asyncio.sleep(3)
        except ConnectionResetError:
            print('Разрыв соединения. Повторная попытка.')


async def listen_chat(reader, history_file=None):
    text = ''
    while True:
        data = await reader.readline()
        text += data.decode()
        if text:
            str_datetime = datetime.datetime.now().strftime("%d %m %Y %H:%M:%S")
            message = f'{str_datetime} {text}'
            if history_file:
                asyncio.create_task(write_to_file(history_file, message))
            print(message)
            text = ''
        await asyncio.sleep(1)


async def write_to_file(filepath, text):
    async with AIOFile(filepath, 'a') as afp:
        await afp.write(text)


if __name__ == '__main__':
    parser = configargparse.ArgParser()
    parser.add('--host', help='host for listening', env_var='MINECHAT_HOST')
    parser.add('--port', help='port for listening', env_var='MINECHAT_PORT_FOR_LISTENING')
    parser.add('--history', help='file to logging chat', env_var='MINECHAT_HISTORY')
    args = parser.parse_args()

    try:
        asyncio.run(connection_holder(args))
    except KeyboardInterrupt:
        pass

