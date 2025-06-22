import os
import time
import requests
from colorama import Fore, Style, init

init(autoreset=True)
# Cores
VERMELHO = '\033[91m'
BRANCO = '\033[97m'
RESET = '\033[0m'

def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""
{Fore.CYAN}  ██████╗ ██╗     ██╗  ██╗ ██████╗         ██████╗ ███████╗    ██████╗ ███████╗██╗   ██╗███████╗
{Fore.CYAN} ██╔═══██╗██║     ██║  ██║██╔═══██╗        ██╔══██╗██╔════╝    ██╔══██╗██╔════╝██║   ██║██╔════╝
{Fore.CYAN} ██║   ██║██║     ███████║██║   ██║        ██║  ██║█████╗      ██║  ██║█████╗  ██║   ██║███████╗
{Fore.CYAN} ██║   ██║██║     ██╔══██║██║   ██║        ██║  ██║██╔══╝      ██║  ██║██╔══╝  ██║   ██║╚════██║
{Fore.CYAN} ╚██████╔╝███████╗██║  ██║╚██████╔╝        ██████╔╝███████╗    ██████╔╝███████╗╚██████╔╝███████║
{Fore.CYAN}  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝         ╚═════╝ ╚══════╝    ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝
{Fore.RESET}""")

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma * 10) % 11
    if dig1 == 10:
        dig1 = 0
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma * 10) % 11
    if dig2 == 10:
        dig2 = 0
    return dig1 == int(cpf[9]) and dig2 == int(cpf[10])

def consultar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if not validar_cpf(cpf):
        print(VERMELHO + "CPF inválido." + RESET)
        return
    
    url = "https://encomendasdobrasil.com/api.php"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "cpf": cpf
    }
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        
        # Tente interpretar como JSON, se falhar mostra texto puro
        try:
            resultado = response.json()
            print(BRANCO + "Resultado da consulta CPF:")
            print(resultado)
        except ValueError:
            print(BRANCO + "Resposta da API:")
            print(response.text)
        
    except requests.exceptions.RequestException as e:
        print(VERMELHO + "Erro na consulta CPF:" + RESET, e)

def consultar_cnpj(cnpj):
    print(BRANCO + f"Consultando CNPJ: {cnpj}..." + RESET)
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if 'status' in data and data['status'] == 'ERROR':
            print(VERMELHO + "Erro: " + data.get('message', 'CNPJ inválido ou não encontrado.') + RESET)
        else:
            print(BRANCO + f"Nome: {data.get('nome')}")
            print(f"Fantasia: {data.get('fantasia')}")
            print(f"Situação: {data.get('situacao')}")
            print(f"Município: {data.get('municipio')}")
            print(f"UF: {data.get('uf')}")
            print(f"Abertura: {data.get('abertura')}")
            print(f"Natureza Jurídica: {data.get('natureza_juridica')}" + RESET)
    except Exception as e:
        print(VERMELHO + "Erro ao consultar CNPJ." + RESET)
        print(VERMELHO + str(e) + RESET)

def consultar_ip(ip):
    print(BRANCO + f"Consultando IP: {ip}..." + RESET)
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data['status'] == 'fail':
            print(VERMELHO + "IP inválido ou não encontrado." + RESET)
        else:
            print(BRANCO + f"País: {data.get('country')}")
            print(f"Região: {data.get('regionName')}")
            print(f"Cidade: {data.get('city')}")
            print(f"ISP: {data.get('isp')}")
            print(f"Organização: {data.get('org')}" + RESET)
    except Exception as e:
        print(VERMELHO + "Erro ao consultar IP." + RESET)
        print(VERMELHO + str(e) + RESET)
def enviar_likes_freefire():
    uid = input("\nDigite o ID do jogador Free Fire: ")
    quantidade = input("Quantidade de likes (padrão: 100): ") or "100"
    
    url = f"https://likes.ffgarena.cloud/api/likesvip_ff?uid={uid}&quantity={quantidade}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(BRANCO + "Likes enviados com sucesso!" + RESET)
            print("Resposta:", response.text)
        else:
            print(VERMELHO + "Erro ao enviar likes." + RESET)
            print(response.text)
    except Exception as e:
        print(VERMELHO + "Erro ao conectar com a API de likes." + RESET)
        print(str(e))

def consultar_id_freefire():
    uid = input("\nDigite o ID do jogador Free Fire para consulta: ")
    url = f"https://system.ffgarena.cloud/api/info_avatar?uid={uid}&region=br"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        basic = data.get("basicInfo", {})
        clan = data.get("clanBasicInfo", {})
        pet = data.get("petInfo", {})
        social = data.get("socialInfo", {})
        avatar_url = data.get("avatars", "N/A")

        print(BRANCO + "\n=== Informações do Jogador ===")
        print(f"Nickname      : {basic.get('nickname', 'N/A')}")
        print(f"Nível         : {basic.get('level', 'N/A')}")
        print(f"Likes         : {basic.get('liked', 'N/A')}")
        print(f"Rank          : {basic.get('rank', 'N/A')}")
        print(f"Pontos Rank   : {basic.get('rankingPoints', 'N/A')}")
        print(f"Região        : {basic.get('region', 'N/A')}")
        print(f"Tem passe elite? {'Sim' if basic.get('hasElitePass') else 'Não'}")

        print(BRANCO + "\n=== Informações do Clã ===")
        print(f"Nome do Clã   : {clan.get('clanName', 'N/A')}")
        print(f"Nível do Clã  : {clan.get('clanLevel', 'N/A')}")
        print(f"Membros       : {clan.get('memberNum', 'N/A')} de {clan.get('capacity', 'N/A')}")

        print(BRANCO + "\n=== Informações do Pet ===")
        print(f"Nome do Pet   : {pet.get('petName', 'N/A')}")
        print(f"Nível do Pet  : {pet.get('level', 'N/A')}")

        print(BRANCO + "\n=== Social ===")
        print(f"Frase         : {social.get('signature', 'N/A')}")

        print(BRANCO + "\n=== Avatar ===")
        print(f"URL da Imagem : {avatar_url}")

    except Exception as e:
        print(VERMELHO + "Erro ao consultar ID do jogador." + RESET)
        print(str(e))

def menu():
    print(BRANCO + "[1] Consultar CPF")
    print("[2] Consultar CNPJ")
    print("[3] Consultar IP")
    print("[4] Enviar Likes Free Fire")
    print("[5] Consultar ID Free Fire")
    print("[0] Sair\n" + RESET)

    escolha = input(VERMELHO + "Escolha uma opção: " + RESET)

    if escolha == "1":
        cpf = input("\nDigite o CPF (somente números): ")
        consultar_cpf(cpf)
    elif escolha == "2":
        cnpj = input("\nDigite o CNPJ (somente números): ")
        consultar_cnpj(cnpj)
    elif escolha == "3":
        ip = input("\nDigite o IP: ")
        consultar_ip(ip)
    elif escolha == "4":
        enviar_likes_freefire()
    elif escolha == "5":
        consultar_id_freefire()
    elif escolha == "0":
        print("\nSaindo...")
        time.sleep(1)
        exit()
    else:
        print("\nOpção inválida.")

    input("\nPressione Enter para voltar ao menu...")
    main()

def main():
    banner()
    menu()

if __name__ == "__main__":
    main()
