import json
import os
import re
import subprocess
from multiprocessing import Process


def replaceTo(string, rep):
    string = re.sub(r"(_|-|[.]|\s|'|`)+", "_", string).title().replace("_", rep)
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
        res = password[0] + re.sub(r, regex[i], password[1:])
        all_pass = all_pass[0] + re.sub(r, regex[i], all_pass[1:])

        if res != password:
            new_password_file.write(res + "\n")

    new_password_file.write(all_pass + "\n")


def transform_password(new_password_file):
    print("init Transform Passwords")
    for password in open('passwords.txt'):
        password = password.replace("\n", "")

        apply_all_regex(replaceTo(password, "@"), new_password_file)
        apply_all_regex(replaceTo(password, "!"), new_password_file)

        password = replaceTo(password, "")
        new_password_file.write(password + "\n")
        new_password_file.write(password[0].lower() + password[1:] + "\n")
        apply_all_regex(password, new_password_file)
    print("End Transform Passwords")


def cmdline(command):
    proc = subprocess.Popen(str(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return err


def decript(arq_crito):
    lista_senha = 'new_password.txt'
    arquivo_saida = 'decifrado.txt'
    arquvivo_resultado = 'resultado.txt'
    arquivo_saida = arq_crito.replace(".enc", "") + '-' + arquivo_saida
    encontrar = 'teste'
    arq_in = 'arquivos/'
    arq_out = 'decifrado/'
    count = 0
    for password in open(lista_senha):
        senha = password.strip()
        cmd = "openssl enc -d -aes-256-cbc -pbkdf2 -salt -in {} -out {} -k {}".format(
            arq_in + arq_crito,
            arq_out + arquivo_saida,
            senha)
        if b"bad decrypt" not in cmdline(cmd):
            arquivo1 = open('decifrado/' + arquivo_saida, 'r')
            arquivo2 = open(arquvivo_resultado, 'a')
            try:
                conteudo = arquivo1.readline()
                if conteudo.strip() == encontrar:
                    arquivo2.write(senha + ' - ' + arq_crito + ' - ' + conteudo + "\n")
                    arquivo1.close()
                    arquivo2.close()
                    break
            except UnicodeDecodeError:
                pass
            arquivo1.close()
            arquivo2.close()
        count += 1

    print("file: {} password count: {}".format(arq_crito, count))


if __name__ == '__main__':

    if not os.path.isfile('new_password.txt'):
        new_password_file = open('new_password.txt', 'w+')
        transform_password(new_password_file)
        new_password_file.close()

    arquivos = os.listdir(r'arquivos')
    threads = []

    for arq_crito in arquivos:
        p = Process(target=decript, args=(arq_crito,))
        p.start()
        threads.append(p)

    for t in threads:
        t.join()
