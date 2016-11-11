# encoding: utf-8
import xlrd
import os.path
import tkinter.filedialog as filedialog
#file_path_string = filedialog.askopenfile(mode ="r", )

def xlread(arq_xls):
    # Abre o arquivo
    xls = xlrd.open_workbook(arq_xls)
    # Pega a primeira planilha do arquivo
    plan = xls.sheets()[0]
    # Para i de zero ao numero de linhas da planilha
    for i in range(plan.nrows):
        # Le os valores nas linhas da planilha
        yield plan.row_values(i)

def rangerows(arq_xls):
    # Retorna o numero de linhas de um arquivo EXCEL
    # Abre o arquivo
    xls = xlrd.open_workbook(arq_xls)
    # Pega a primeira planilha do arquivo
    plan = xls.sheets()[0]
    return plan.nrows

def how_many_post(log,name):
    # Retorna o numero de "aparições" de "a"
    a=0
    i=0
    # Verifica linha por linha se tem alguém com o mesmo nome, se tiver acrescenta no valor a ser devolvido
    for linha in xlread(arquivo):
        if log[i].name == name:
            a=a+1
        i=i+1
    return a

def create_dic(log):
    # Cria um dicionario com "Nome da pessoa" : "Quantos visualizaçoes"
    dic={}
    i=0
    for linha in xlread(arquivo):
        if not log[i].name in dic:
            dic[log[i].name] = how_many_post(log,log[i].name)
        i=i+1
    return dic

def present_people(dic):
    # Recebe um dicionário e retorna uma lista com todos os nomes (keys)
    ppl = []
    for key in dic:
        ppl.append(key)
    return ppl

def sort_dic(dic):
    for w in sorted(dic,key=dic.get, reverse=True):
        dic_sorted=dic[w]
    return dic_sorted

# You are a CHAMPION BRO
class Champion:
    def __init__(self, date, name, affected, component, context, event, description, source, ip):
        self.date = date
        self.name = name
        self.affected = affected
        self.component = component
        self.context = context
        self.event = event
        self.description = description
        self.source = source
        self.ip = ip

#------------------------------------------ main ---------------------------------------------#
# Dicionario utilizado
dic={}
# Define uma constante para arquivo
#arquivo =  filedialog.askopenfilename()
arquivo = "C:\\Users\\leona\\Desktop\\Script\\script-moodle\\logs.xlsx"
# Se não tiver arquivo só printa "Nenhum arquivo achado"
if not arquivo:
    print ("Nenhum arquivo achado")
else:
    print ("Carregando arquivo...")
    # Inicia a lista
    log={}
    i=0
    # For para inserir as 9 categorias de cada um na lista
    for linha in xlread(arquivo):
            # Carrega as 9 características em 1 e vai para o próximo
            log[i] = Champion(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8])
            print (log[i].name)
            i=1+i
    print ("Carregamento concluido")
    dic=create_dic(log)

from operator import itemgetter
from collections import OrderedDict

#--------------------------------------------- PLOT GRAPH ------------------------------------#
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
print (sort_dic(dic))
# Example data
people = sort_dic(dic)
y_pos = np.arange(len(people))
performance=[]
for x in dic:
    performance.append(dic[x])

plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, people)
plt.xlabel('Perguntas')
plt.title('Quantia de visitas ao fórum')

plt.show()
