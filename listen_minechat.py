import asyncio
from aiofile import AIOFile
import datetime
import configargparse
from dotenv import load_dotenv
load_dotenv()


async def main(args):
    while True:
        try:
            reader, writer = await asyncio.open_connection(args.host, args.port)
            await listen_chat(reader, args.history)
        except TimeoutError:
            print('Нет соединения. Повторная попытка через 3 сек.')
            await asyncio.sleep(3)
        except ConnectionResetError:
            print('Разрыв соединения. Повторная попытка.')
        finally:
            writer.close()


async def listen_chat(reader, history_file=None):
    while True:
        data = await reader.readline()
        if not data:
            continue
        str_datetime = datetime.datetime.now().strftime("%d %m %Y %H:%M:%S")
        message = f'{str_datetime} {data.decode()}'
        if history_file:
            asyncio.create_task(write_to_file(history_file, message))
        print(message)


async def write_to_file(filepath, text):
    async with AIOFile(filepath, 'a') as afp:
        await afp.write(text)


if __name__ == '__main__':
    parser = configargparse.ArgParser()
    parser.add('--host', help='Адрес сервера minechat', env_var='MINECHAT_HOST')
    parser.add('--port', help='Порт для прослушивания сообщений чата', env_var='MINECHAT_PORT_FOR_LISTENING')
    parser.add('--history', help='Путь к фалу для логирования истории чата', env_var='MINECHAT_HISTORY')
    args = parser.parse_args()
    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        pass

