import requests
import colorama
from colorama import Fore, Style
from threading import Thread
import os
import time

colorama.init()
os.system('cls' if os.name == 'nt' else 'clear')

StyleBright = Style.BRIGHT
sent = 0

print(f"""
      
      
$$$$$$$\  $$\     $$\       $$$$$$$$\  $$$$$$\  $$$$$$$\  $$$$$$$$\  $$$$$$\  $$\   $$\ 
$$  __$$\ \$$\   $$  |      \__$$  __|$$  __$$\ $$  __$$\ \____$$  |$$  __$$\ $$$\  $$ |
$$ |  $$ | \$$\ $$  /          $$ |   $$ /  $$ |$$ |  $$ |    $$  / $$ /  $$ |$$$$\ $$ |
$$$$$$$\ |  \$$$$  /           $$ |   $$$$$$$$ |$$$$$$$  |   $$  /  $$$$$$$$ |$$ $$\$$ |
$$  __$$\    \$$  /            $$ |   $$  __$$ |$$  __$$<   $$  /   $$  __$$ |$$ \$$$$ |
$$ |  $$ |    $$ |             $$ |   $$ |  $$ |$$ |  $$ | $$  /    $$ |  $$ |$$ |\$$$ |
$$$$$$$  |    $$ |             $$ |   $$ |  $$ |$$ |  $$ |$$$$$$$$\ $$ |  $$ |$$ | \$$ |
\_______/     \__|             \__|   \__|  \__|\__|  \__|\________|\__|  \__|\__|  \__|
                                                                                       
                                                                                                                                                                                                                                                      

{StyleBright + Fore.RED} > {Fore.RESET}Opções de Reporte
{Fore.RED} [1]{Fore.RESET} Conteúdo Ilegal           {Fore.GREEN}:: 1
{Fore.RED} [2]{Fore.RESET} Assédio                   {Fore.GREEN}:: 2
{Fore.RED} [3]{Fore.RESET} Spam/Phishing             {Fore.GREEN}:: 3
{Fore.RED} [4]{Fore.RESET} Automutilação             {Fore.GREEN}:: 4
{Fore.RED} [5]{Fore.RESET} Conteúdo NSFW             {Fore.GREEN}:: 5
""")

token = input(f"{Fore.BLUE} > Token: {Fore.RESET}")
headers = {'Authorization': token}

check = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
if check.status_code != 200:
    print(f"{Fore.RED} > Token inválido.")
    input("\nPressione Enter para sair...")
    exit()

guild_id = input(f"{Fore.BLUE} > ID do Servidor: {Fore.RESET}")
channel_id = input(f"{Fore.BLUE} > ID do Canal: {Fore.RESET}")
message_id = input(f"{Fore.BLUE} > ID da Mensagem: {Fore.RESET}")
reason = input(f"{Fore.BLUE} > Opção de reporte: {Fore.RESET}")

def report():
    global sent
    payload = {
        'channel_id': channel_id,
        'guild_id': guild_id,
        'message_id': message_id,
        'reason': reason
    }

    local_headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'DiscordBot (https://discord.com, v1)'
    }

    for _ in range(10):  # Limite de 10 tentativas por thread
        try:
            response = requests.post('https://discord.com/api/v9/report', headers=local_headers, json=payload)
            if response.status_code == 201:
                sent += 1
                print(f"{Fore.GREEN} > Report enviado com sucesso! {Fore.YELLOW}Total: {sent}")
            elif response.status_code == 401:
                print(f"{Fore.RED} > Token inválido.")
                break
            else:
                print(f"{Fore.RED} > Erro ao reportar. Status: {response.status_code}")
            time.sleep(1)  # Espera entre requisições
        except Exception as e:
            print(f"{Fore.RED} > Exceção: {e}")
            break

for _ in range(100):
    Thread(target=report, daemon=True).start()

# Aguarda o Enter para manter a janela aberta
input("\nPressione Enter para sair...")
