import subprocess
import sys
import os
import argparse

def cmdline(command):
    proc = subprocess.Popen(str(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return err

def trocaLetras(tipo,senha):
    if tipo == 'maketrans':
        trantab = str.maketrans('abcdefghikloqstvxy', '@8(63#9#1<i095+<%?')
        senha = senha.lower()
        senha = senha.translate(trantab)
        senha = senha.replace("w", "uu")
    elif tipo == 'upper':
        senha = senha.upper()
    elif tipo == 'lower':
        senha = senha.lower()
    elif tipo == 'swapcase':
        senha = senha.swapcase()

    return senha


if __name__ == '__main__':

    arquivos = os.listdir(r'C:\Users\Rodrigo\Documents\Loto\simpleaes\Arquivos')
    lista_senha = 'starwar_new.txt'
    arquivo_saida = 'decifrado.txt'
    arquvivo_resultado = 'resultado.txt'
    testes_palavras = ['normal','swapcase','lower','upper','maketrans']

    for arq_crito in arquivos:
        with open(lista_senha) as f:
            senha = f.readline()
            while senha:
                senha = senha.strip()
                for tipo_de_teste in testes_palavras:
                    if tipo_de_teste != 'normal':
                        senha = trocaLetras(tipo_de_teste,senha)
                    if len(senha) > 0:
                        print(senha)
                        cmd = "openssl enc -d -aes-256-cbc -pbkdf2 -salt -in {} -out {} -k {}".format(arq_crito,arquivo_saida,senha)
                        if b"bad decrypt" not in cmdline(cmd):
                            print("Deu certo")
                            arquivo1 = open(arquivo_saida,'r')
                            arquivo2 = open(arquvivo_resultado,'a')
                            try:
                                conteudo = arquivo1.readline()
                                arquivo2.write(senha + ' - ' + arq_crito + ' - ' + conteudo + "\n")
                            except UnicodeDecodeError:
                                print('Caracter invalido.')
                            arquivo1.close()
                            arquivo2.close()
                try:
                    senha = f.readline()
                except UnicodeDecodeError:
                    print('Caracter invalido.')
