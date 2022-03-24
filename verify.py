from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import sys

api_id = int(sys.argv[1])
api_hash = str(sys.argv[2])
phone = str(sys.argv[3])

client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)

try:
    client.start()
    print(f'n\n[+] Logged in - {phone}')
    client.disconnect()
except PhoneNumberBannedError:
    print(f'{phone} is banned! Filter it using option 2')