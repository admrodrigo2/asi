import os
import subprocess
import re
import json


def camelcase(string):
    string = re.sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return string[0].lower() + string[1:]


def write_password(password, new_password_file):
    new_password_file.write(password + "\n")
    new_password_file.write((password.lower() + "\n", '')[password.lower() == password])
    new_password_file.write((password.lower() + "\n", '')[password.upper() == password])
    new_password_file.write((password.lower() + "\n", '')[password.swapcase() == password])


def apply_all_regex(password, new_password_file):
    regex = json.loads(open('regex.json', 'r').read())
    all_pass = password + ''
    for i in regex.keys():
        r = re.compile(i, re.IGNORECASE)
        res = re.sub(r, regex[i], password)
        all_pass = re.sub(r, regex[i], all_pass)

        if res != password:
            new_password_file.write(res + "\n")

    new_password_file.write(all_pass + "\n")


def transform_password(new_password_file):
    for password in open('passwords.txt'):
        password = camelcase(password.replace("\n", ""))
        new_password_file.write(password + "\n")
        apply_all_regex(password, new_password_file)


def cmdline(command):
    proc = subprocess.Popen(str(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return err


def decript():
    arquivos = os.listdir(r'/home/matheussn/Documents/arquivos')
    lista_senha = 'new_password.txt'
    arquivo_saida = 'decifrado.txt'
    arquvivo_resultado = 'resultado.txt'

    for arq_crito in sorted(arquivos):
        print(arq_crito)
        for password in open(lista_senha):
            senha = password.strip()
            cmd = "openssl enc -d -aes-256-cbc -pbkdf2 -salt -in /home/matheussn/Documents/arquivos/{} -out {} -k '{}'".format(
                arq_crito,
                arquivo_saida,
                senha)
            if b"bad decrypt" not in cmdline(cmd):
                # print("Deu certo")
                arquivo1 = open(arquivo_saida, 'r')
                arquivo2 = open(arquvivo_resultado, 'a')
                try:
                    conteudo = arquivo1.readline()
                    arquivo2.write(senha + ' - ' + arq_crito + ' - ' + conteudo + "\n")
                except UnicodeDecodeError:
                    print('Caracter invalido.')
                arquivo1.close()
                arquivo2.close()


if __name__ == '__main__':
    new_password_file = open('new_password.txt', 'a')
    transform_password(new_password_file)

    decript()
