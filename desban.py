import requests
from requests.exceptions import RequestException, HTTPError
import logging
from datetime import datetime
import os
import re


log_file = 'enviar_reclamacao.log'
if os.path.exists(log_file):
    os.remove(log_file)

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


url = 'https://ffsuporte.garena.com/support/tickets/new?ticket_form=tenho_dúvidas_ou_problemas_com_o_jogo%2C_evento%2C_loja%2C_itens_ou_recompensas'


form_data_template = {
    'ticket[subject]': 'Solicitação de Revisão de Banimento da Conta Free Fire',
    'ticket[description]': """
    Prezado Suporte da Garena,

    Solicito a revisão do banimento da minha conta no Free Fire. Abaixo, forneço as informações para facilitar a análise do meu caso:

    - Nome de Usuário: {username}
    - ID da Conta: {account_id}
    - Endereço de E-mail Associado à Conta: {email}
    - Data e Hora Aproximada do Banimento: {date_time}
    - Descrição do Problema: {problem_description}

    Acredito que o banimento possa ter sido um erro. Sou um jogador que respeita as regras e gostaria de entender o motivo do banimento e, se possível, recuperar o acesso à minha conta.

    Estou à disposição para fornecer qualquer informação adicional necessária para resolver este problema.

    Agradeço pela atenção e aguardo uma resposta.

    Atenciosamente,

    {full_name}
    {email}
    {phone_number}
    """,
    'ticket[priority]': 'normal',
}


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*',
    'Connection': 'keep-alive',
}

def validar_email(email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("O endereço de e-mail fornecido é inválido.")

def validar_telefone(phone_number):
    
    if phone_number and not re.match(r'^\+?[1-9]\d{1,14}$', phone_number):
        raise ValueError("O número de telefone fornecido é inválido.")

def preparar_dados(username, account_id, email, date_time, problem_description, full_name, phone_number):
    
    description = form_data_template['ticket[description]'].format(
        username=username,
        account_id=account_id,
        email=email,
        date_time=date_time,
        problem_description=problem_description,
        full_name=full_name,
        phone_number=phone_number
    )
    return {
        'ticket[description]': description,
        'ticket[subject]': form_data_template['ticket[subject]'],
        'ticket[priority]': form_data_template['ticket[priority]'],
    }

def enviar_formulario(url, data, headers):

    try:
        logging.info(f"Iniciando o envio de solicitação para: {url}")
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  
        
        # Exibe a resposta completa para depuração
        logging.info(f"Status code: {response.status_code}")
        logging.info(f"Resposta do servidor: {response.text}")

        if response.status_code == 200:
            logging.info("Relatório enviado com sucesso!")
            print("Relatório enviado com sucesso!")
        else:
            logging.error(f"Falha ao enviar o relatório. Status code: {response.status_code}")
            print(f"Falha ao enviar o relatório. Status code: {response.status_code}")
    except HTTPError as http_err:
        logging.error(f"Erro HTTP ao enviar o relatório: {http_err}")
        print(f"Erro HTTP ao enviar o relatório: {http_err}")
    except RequestException as req_err:
        logging.error(f"Erro ao enviar o relatório: {req_err}")
        print(f"Erro ao enviar o relatório: {req_err}")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        print(f"Erro inesperado: {e}")

def validar_dados(username, account_id, email, date_time, problem_description, full_name, phone_number):

    if not username or not account_id or not email or not date_time or not problem_description or not full_name:
        raise ValueError("Todos os campos obrigatórios devem ser preenchidos, exceto o número de telefone.")
    
    validar_email(email)
    validar_telefone(phone_number)
    
    try:
        datetime.strptime(date_time, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError("A data e hora devem estar no formato AAAA-MM-DD HH:MM.")

def coletar_informacoes():
    
    while True:
        try:
            username = input("Digite o nome de usuário do jogo: ").strip()
            account_id = input("Digite o ID da conta: ").strip()
            email = input("Digite o endereço de e-mail associado à conta: ").strip()
            date_time = input("Digite a data e hora aproximada do banimento (por exemplo 2024-09-18 14:30 ): ").strip()
            problem_description = input("Descreva o que você acredita ter causado o banimento ou o que aconteceu: ").strip()
            full_name = input("Digite seu nome completo: ").strip()
            phone_number = input("Digite seu número de telefone (opcional): ").strip()

            validar_dados(username, account_id, email, date_time, problem_description, full_name, phone_number)
            return username, account_id, email, date_time, problem_description, full_name, phone_number
        except ValueError as ve:
            print(f"Erro de validação: {ve}. Tente novamente.")
            logging.warning(f"Erro de validação: {ve}.")
        except Exception as e:
            print(f"Erro inesperado: {e}. Tente novamente.")
            logging.error(f"Erro inesperado: {e}.")

def salvar_arquivo(nome_arquivo, conteudo):
    
    try:
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(conteudo)
        logging.info(f"Conteúdo salvo com sucesso em {nome_arquivo}")
    except IOError as e:
        logging.error(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")
        print(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")

def ler_arquivo(nome_arquivo):
    
    try:
        with open(nome_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
        logging.info(f"Conteúdo lido com sucesso de {nome_arquivo}")
        return conteudo
    except IOError as e:
        logging.error(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
        print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
        return ""

def main():
    
    username, account_id, email, date_time, problem_description, full_name, phone_number = coletar_informacoes()
    dados_preparados = preparar_dados(username, account_id, email, date_time, problem_description, full_name, phone_number)
    conteudo = "\n".join(f"{key}: {value}" for key, value in dados_preparados.items())
    
    salvar_arquivo("dados_preparados.txt", conteudo)  

    enviar_formulario(url, dados_preparados, headers)

if __name__ == '__main__':
    main()