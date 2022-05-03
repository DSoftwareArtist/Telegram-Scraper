from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import sys

api_id = int((input)'api id: ')
api_hash = str((input)'api hash: ')
phone = str((input)'api phone: ')

client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)

try:
    client.start()
    print(f'n\n[+] Logged in - {phone}')
    client.disconnect()
except PhoneNumberBannedError:
    print(f'{phone} is banned! Filter it using option 2')
