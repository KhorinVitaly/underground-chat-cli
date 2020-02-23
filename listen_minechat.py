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


async def listen_chat(reader, logfile):
    text = ''
    while True:
        try:
            data = await reader.readline()
            text += await get_text_from_bytes(data)
            if text:
                str_datetime = datetime.datetime.now().strftime("%d %m %Y %H:%M:%S")
                message = f'{str_datetime} {text}'
                asyncio.create_task(write_to_file(logfile, message))
                print(message)
                text = ''
            await asyncio.sleep(1)
        except ConnectionResetError:
            print('Разрыв соединения. Повторная попытка.')
            return


async def get_text_from_bytes(data):
    try:
        return data.decode()
    except UnicodeDecodeError:
        return ''


async def write_to_file(filepath, text):
    async with AIOFile(filepath, 'a') as afp:
        await afp.write(text)


def sig_interrupt():
    for task in asyncio.Task.all_tasks():
        task.cancel()


if __name__ == '__main__':
    parser = configargparse.ArgParser()
    parser.add('--host', help='host for listening', env_var='MINECHAT_HOST')
    parser.add('--port', help='port for listening', env_var='MINECHAT_PORT')
    parser.add('--history', help='file to logging chat', env_var='MINECHAT_HISTORY')
    arguments = parser.parse_args()
    try:
        asyncio.run(main(arguments))
    except KeyboardInterrupt:
        pass

