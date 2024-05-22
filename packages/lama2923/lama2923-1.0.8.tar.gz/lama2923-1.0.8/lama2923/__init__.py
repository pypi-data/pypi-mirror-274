
# python version = 3.11
import os
import time
import socket
from colorama import Fore, Style, init
import requests

if os.name == 'nt':
    import msvcrt

def ekran_temizle():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        raise NotImplementedError("Unsupported Operating System!")

def geçen_süreyi_hesapla(start_time, end_time):
    if not (isinstance(start_time, (int, float)) and isinstance(end_time, (int, float))):
        raise TypeError("Only time.time() or tzaman() values are accepted!")

    time_difference = end_time - start_time
    seconds = int(time_difference)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(hours, 60)
    days, hours = divmod(hours, 24)
    milliseconds = int((time_difference - int(time_difference)) * 100)
    
    return {
        "Milliseconds": milliseconds,
        "Seconds": seconds if seconds > 0 else None,
        "Minutes": minutes if minutes > 0 else None,
        "Hours": hours if hours > 0 else None,
        "Days": days if days > 0 else None
    }

def tzaman():
    return time.time()
    
def Gokkusagı(YAZI, DÖNGÜ, Hız, bölüm):
    def hız_kontrol():
        if Hız not in ['Yavaş', 'Slow', 'Hızlı', None]:
            raise ValueError("Invalid speed value. Choose 'Yavaş', 'Slow', 'Hızlı', or None.")

    def bölüm_kontrol():
        if bölüm not in ['Tam', 'Yarı', 'Çeyrek', None]:
            raise ValueError("Invalid section value. Choose 'Tam', 'Yarı', 'Çeyrek', or None.")

    hız_kontrol()
    bölüm_kontrol()      
    
    init(autoreset=True)
    if not isinstance(DÖNGÜ, int):
        print("DÖNGÜ must be an integer!")
        time.sleep(3)
        ekran_temizle()
        exit(1)

    renkler = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

    YAZI_uzunluğu = len(YAZI)
    
    if bölüm in ['Tam', None]:
        bölüm_sayısı1 = 238
        bölüm_sayısı2 = bölüm_sayısı1 - 2
    elif bölüm == 'Yarı':
        bölüm_sayısı1 = 119
        bölüm_sayısı2 = bölüm_sayısı1 - 2
    elif bölüm == 'Çeyrek':
        bölüm_sayısı1 = 59
        bölüm_sayısı2 = bölüm_sayısı1 - 2 
               
    while True:
        if DÖNGÜ <= 0:
            break
        
        for i in range(1, bölüm_sayısı1 - YAZI_uzunluğu):
            for renk in renkler:
                if Hız in ['Yavaş', 'Slow']:
                    time.sleep(0.001)  
                elif Hız == 'Hızlı':
                    pass
                elif Hız is None:
                    time.sleep(0.0001)    
                print(" " * i + renk + YAZI)

        for i in range(bölüm_sayısı2 - YAZI_uzunluğu, 0, -1):
            for renk in renkler:
                if Hız in ['Yavaş', 'Slow']:
                    time.sleep(0.001)  
                elif Hız == 'Hızlı':
                    pass
                elif Hız is None:
                    time.sleep(0.0001)   
                print(" " * i + renk + YAZI)

def port_kontrol(ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip_address, port))
    sock.close()

    return result == 0

def internet_kontrol():
    try:
        response = requests.get("http://www.google.com", timeout=2.5)
        return True
    except requests.ConnectionError:
        return False

def lprint(*yazı, end="\n", sep=" ", delay=0.10):
    yazı = map(str, yazı)
    birleşik_kelime = sep.join(yazı)
    kelime_len = len(birleşik_kelime)

    for char in birleşik_kelime:
        print(char, end="", flush=True)
        time.sleep(delay)

    print(end=end)

def otodüzeltmeyi_temizle():
    if os.name == 'nt':
        while msvcrt.kbhit():
            msvcrt.getch()

def linput(*yazı, end="", sep=" ", delay=0.10, otodt=False):
    lprint(*yazı, end=end, sep=sep, delay=delay)
    if otodt and os.name == 'nt':
        otodüzeltmeyi_temizle()
    return input()

def çoğul_eki(yazı=None):
    if not isinstance(yazı, (str, int)):
        raise TypeError("Only integer and string values are accepted.")

    unsuz_harfler = ['b', 'c', 'ç', 'd', 'f', 'g', 'ğ', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 'ş', 't', 'v', 'y', 'z']
    unlu_harfler = ['a', 'e', 'ı', 'i', 'o', 'ö', 'u', 'ü']
    lar_eki_alanlar = ["o", "u", "a", "ı"]
    ler_eki_alanlar = ["e", "ö", "ü", "i"]

    for char in str(yazı)[::-1]:
        if char not in unsuz_harfler:
            break

    return "ler" if char in ler_eki_alanlar else "lar"

def sıralama_eki(number, ek_derecesi=1, Çoğul_eki=False):
    if not isinstance(number, int):
        raise TypeError("Value must be an integer.")

    ek_map = {
        "0": "ıncı", "1": "inci", "2": "nci", "3": "üncü", "4": "üncü",
        "5": "inci", "6": "ıncı", "7": "nci", "8": "inci", "9": "uncu"
    }

    ek = ek_map.get(str(number)[-1], "uncu")
    if Çoğul_eki:
        return ek + çoğul_eki(ek)
    
    dereceler = ["", "sin", "siniz", "yiz", "yim"]
    return ek + dereceler[ek_derecesi - 1]

def kurallı_sayı(Numbers=0):
    if not isinstance(Numbers, (int, float, str)):
        raise TypeError("Value must be an integer, float, or a numeric string.")
    
    Numbers = str(float(Numbers)).replace('.', ',')
    integer_part, fractional_part = Numbers.split(',')

    formatted_integer_part = ".".join([
        integer_part[max(i - 3, 0):i]
        for i in range(len(integer_part), 0, -3)
    ][::-1])

    return f"{formatted_integer_part},{fractional_part}"

def terskurallı_sayı(Numbers=0):
    if not isinstance(Numbers, str):
        raise TypeError("Value must be a string.")
    return Numbers.replace(".", "").replace(",", ".")

class TokenIsNotWork(Exception):
    pass

class Discord:
    class User:
        def __init__(self, token):
            self.token = str(token)
            response = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': self.token})
            if response.status_code != 200:
                raise TokenIsNotWork('Token is not working!')

        def send_message(self, Channel_id, Message, files=None):
            payload = {'content': str(Message)}
            headers = {'Authorization': self.token}
            if files is not None and isinstance(files, list):
                files_data = {
                    os.path.basename(file_name): open(file_name, "rb").read()
                    for file_name in files if os.path.getsize(file_name) > 0
                }
                response = requests.post(f'https://discord.com/api/v9/channels/{Channel_id}/messages', data=payload, files=files_data, headers=headers)
            else:
                response = requests.post(f'https://discord.com/api/v9/channels/{Channel_id}/messages', data=payload, headers=headers)
            return response.status_code
        
        def delete_message(self, Channel_id, Message_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}', headers=headers)
            return response.status_code
        
        def edit_message(self, Channel_id, Message_id, Message_Content):
            headers = {'Authorization': self.token}
            payload = {'content': str(Message_Content)}
            response = requests.patch(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}', json=payload, headers=headers)
            return response.status_code
        
        def get_channel_messages(self, Channel_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/channels/{Channel_id}/messages', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code

        def get_channel_message(self, Channel_id, Message_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code

        def add_reaction(self, Channel_id, Message_id, emoji):
            headers = {'Authorization': self.token}
            emoji = requests.utils.quote(emoji)
            response = requests.put(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}/reactions/{emoji}/@me', headers=headers)
            return response.status_code
        
        def remove_reaction(self, Channel_id, Message_id, emoji):
            headers = {'Authorization': self.token}
            emoji = requests.utils.quote(emoji)
            response = requests.delete(f'https://discord.com/api/v9/channels/{Channel_id}/messages/{Message_id}/reactions/{emoji}/@me', headers=headers)
            return response.status_code

        def get_channel_info(self, Channel_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/channels/{Channel_id}', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
    
        def get_guild_dms(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/channels', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code   

        def send_reply_message(self, Channel_id, Message, ReplyMessage_id):
            payload = {'content': str(Message), 'message_reference': {'message_id': ReplyMessage_id}}
            headers = {'Authorization': self.token}
            response = requests.post(f'https://discord.com/api/v9/channels/{Channel_id}/messages', data=payload, headers=headers)
            return response.status_code
        
        def change_user_nickname(self, Guild_id, Nickname):
            headers = {'Authorization': self.token}
            payload = {'nick': str(Nickname)}
            response = requests.patch(f'https://discord.com/api/v9/guilds/{Guild_id}/members/@me/nick', json=payload, headers=headers)
            return response.status_code

        def get_author_info(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
        
        def get_author_relationships(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
        
        def send_friend_request(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.put(f'https://discord.com/api/v9/users/@me/relationships/{User_id}', headers=headers)
            return response.status_code
        
        def remove_friend(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{User_id}', headers=headers)
            return response.status_code
        
        def block_user(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.put(f'https://discord.com/api/v9/users/@me/relationships/{User_id}/block', headers=headers)
            return response.status_code
        
        def unblock_user(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{User_id}/block', headers=headers)
            return response.status_code

        def get_author_channels(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
        
        def get_author_guilds(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
        
        def get_author_settings(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/settings', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
            
        def get_author_connections(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/connections', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
        
        def get_user_info(self, User_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/users/{User_id}', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code

        def get_all_guilds(self):
            headers = {'Authorization': self.token}
            response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
        
        def get_guild(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
            
        def kick_member(self, Guild_id, Member_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/guilds/{Guild_id}/members/{Member_id}', headers=headers)
            return response.status_code
        
        def ban_member(self, Guild_id, Member_id, delete_message_days=0):
            headers = {'Authorization': self.token}
            data = {'delete_message_days': delete_message_days}
            response = requests.put(f'https://discord.com/api/v9/guilds/{Guild_id}/bans/{Member_id}', headers=headers, json=data)
            return response.status_code
        
        def unban_member(self, Guild_id, Member_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/guilds/{Guild_id}/bans/{Member_id}', headers=headers)
            return response.status_code
        
        def get_guild_bans(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/bans', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
            
        def get_guild_channels(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/channels', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
        
        def get_guild_members(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/members', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
            
        def get_guild_roles(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/guilds/{Guild_id}/roles', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
            
        def get_user_connections(self, id):
            headers = {'Authorization': self.token}
            response = requests.get(f'https://discord.com/api/v9/users/{id}/connections', headers=headers)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code

        def create_guild(self, Guild_name, Region='europe', Verification_level=0, Default_message_notifications=0, Explicit_content_filter=0, Roles=None, Channels=None):
            headers = {'Authorization': self.token}
            payload = {
                'name': str(Guild_name),
                'region': str(Region),
                'verification_level': int(Verification_level),
                'default_message_notifications': int(Default_message_notifications),
                'explicit_content_filter': int(Explicit_content_filter)
            }
            if Roles is not None and isinstance(Roles, list):
                payload['roles'] = Roles
            if Channels is not None and isinstance(Channels, list):
                payload['channels'] = Channels
            response = requests.post('https://discord.com/api/v9/guilds', json=payload, headers=headers)
            return response.status_code
    
        def delete_guild(self, Guild_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/guilds/{Guild_id}', headers=headers)
            return response.status_code

       

        def edit_guild(self, Guild_id, Guild_name, Region='europe', Verification_level=0, Default_message_notifications=0, Explicit_content_filter=0, Roles=None, Channels=None):
                    headers = {'Authorization': self.token}
                    payload = {
                        'name': str(Guild_name),
                        'region': str(Region),
                        'verification_level': int(Verification_level),
                        'default_message_notifications': int(Default_message_notifications),
                        'explicit_content_filter': int(Explicit_content_filter)
                    }
                    if Roles is not None and isinstance(Roles, list):
                        payload['roles'] = Roles
                    if Channels is not None and isinstance(Channels, list):
                        payload['channels'] = Channels
                    response = requests.patch(f'https://discord.com/api/v9/guilds/{Guild_id}', json=payload, headers=headers)
                    return response.status_code
        
        def create_guild_role(self, Guild_id, Role_name):
            headers = {'Authorization': self.token}
            payload = {'name': str(Role_name)}
            response = requests.post(f'https://discord.com/api/v9/guilds/{Guild_id}/roles', json=payload, headers=headers)
            return response.status_code
        
        def delete_guild_role(self, Guild_id, Role_id):
            headers = {'Authorization': self.token}
            response = requests.delete(f'https://discord.com/api/v9/guilds/{Guild_id}/roles/{Role_id}', headers=headers)
            return response.status_code

    class Webhook:
        def __init__(self, webhook_url):
            self.WebhookUrl = str(webhook_url)
            
        def send_webhook(self, Content='', embed=None, files=None):
            def format_embed(embed):
                formatted_embed = {}
                all_args3 = {'fields': ['name', 'value', 'inline']}
                all_args2 = {'footer': ['text', 'icon_url'], 'image': ['url'], 'thumbnail': ['url']}
                all_args1 = ['title', 'description', 'color', 'url']

                for arg in all_args1:
                    if arg in embed:
                        formatted_embed[arg] = embed[arg]
    
                for arg, keys in all_args2.items():
                    if arg in embed:
                        formatted_embed[arg] = {key: embed[arg][key] for key in keys if key in embed[arg]}
    
                if 'fields' in embed:
                    formatted_embed['fields'] = [{arg: field[arg] for arg in all_args3['fields'] if arg in field} for field in embed['fields']]
    
                return formatted_embed
    
            data = {'content': Content}
    
            if embed:
                data['embeds'] = [format_embed(embed)]
            
            if files and isinstance(files, list):
                files_data = {os.path.basename(file_name): open(file_name, "rb").read() for file_name in files if os.path.getsize(file_name) > 0}
                response = requests.post(self.WebhookUrl, data=data, files=files_data)
            else:
                response = requests.post(self.WebhookUrl, json=data)
            return response.status_code
        
        def delete_specific_message(self, Message_id):
            response = requests.delete(f'{self.WebhookUrl}/messages/{Message_id}')
            return response.status_code
        
        def get_specific_message(self, Message_id):
            response = requests.get(f'{self.WebhookUrl}/messages/{Message_id}')
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
            
        def get_webhook_info(self):
            response = requests.get(self.WebhookUrl)
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
                
        def get_messages(self):
            response = requests.get(f'{self.WebhookUrl}/messages')
            return response.status_code, response.json() if response.status_code == 200 else response.status_code
