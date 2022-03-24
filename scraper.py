from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError, PeerFloodError
from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.errors.common import MultiError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
from time import sleep
from telethon.tl.functions.channels import GetFullChannelRequest

# Provide the necessary info to start the scraping.
accounts = [
    { # If you want to generate your own api_id and api_hash: visit https://my.telegram.org/auth and create your own app.
        'api_id': '', 
        'api_hash': '',
        'phone': ''
    }
]
source_group = 'paxful_philippines_community' # Enter the name of the group you want to scrape [note: Make sure that this group exist]
destination_group = 'newTestArc' # Enter the name of the group where the users will be added. [note: Make sure that this group exist]


# Validate Session
account = accounts[0]
api_id = account['api_id']
api_hash = account['api_hash']
phone = account['phone']
client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    try:
        client.send_code_request(phone)
        print('not authenticated')
    except PhoneNumberBannedError:
        print('phone banned')
        sys.exit()

# Extract Users
group = client.get_entity(source_group)
members = []
members = client.iter_participants(group, aggressive=True)
channel_full_info = client(GetFullChannelRequest(group))
cont = channel_full_info.full_chat.participants_count
users = []
try:
    for index, member in enumerate(members):
        print(f"{index+1}/{cont}", end="\r")
        if index%100 == 0:
            sleep(3)
        if not member.bot:
            if member.username:
                username = member.username
            else:
                username = ''
            users.append({
                'username': username,
                'user_id': member.id,
                'access_hash': member.access_hash,
                'group': group.title,
                'group_id': group.id
            })
except PeerFloodError:
    pass
except MultiError:
    pass

# Verify the Destination Group
target_group = client.get_entity(destination_group)
entity = InputPeerChannel(target_group.id, target_group.access_hash)
source_group = target_group.title

# Adding users to the Destination Group
print(f'Adding members to {source_group}')
added_users = []
n = 0
for user in users:
    n += 1
    added_users.append(user)
    if n % 50 == 0:
        print(f'Sleep 2 min to prevent possible account ban')
        sleep(120)
    try:
        if user['username'] == "":
            continue
        user_to_add = client.get_input_entity(user['username'])
        client(InviteToChannelRequest(entity, [user_to_add]))
        print(f' {user["username"]} joined {source_group}')
        usr_id = user['user_id']
        sleep(30)
    except PeerFloodError:
        sys.exit('Aborted. Peer Flood Error')
    except UserPrivacyRestrictedError:
        print('User Privacy Restriction')
        continue
    except KeyboardInterrupt:
        print('Aborted. Keyboard Interrupt')
    except:
        print(f'Some Other error in adding')
        continue
sys.exit()