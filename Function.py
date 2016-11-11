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

def how_many_visua(log,name):
    # Retorna o numero de "aparições" de "a"
    a=0
    i=0
    # Verifica linha por linha se tem alguém com o mesmo nome, se tiver acrescenta no valor a ser devolvido
    for linha in log:
        if log[i].name == name:
            a=a+1
        i=i+1
    return a


def create_dic_name_number(log):
    # Cria um dicionario com "Nome da pessoa" : "Quantos visualizaçoes"
    dic={}
    i=0
    for linha in log:
        if not log[i].name in dic:
            dic[log[i].name] = how_many_visua(log,log[i].name)
        i=i+1
    return dic

def present_people(dic):
    # Recebe um dicionário e retorna uma lista com todos os nomes (keys)
    ppl = []
    for key in dic:
        ppl.append(key)
    return ppl

def sorted_number_dic(dic):
    # Recebe o dicionary e retorna 2 listas people and number
    import operator
    people=[]
    number=[]
    # Passa o dicionary para uma lista de tuplas e ordenada essa lista
    sorted_ = sorted(dic.items(), key = operator.itemgetter(1))
    people,number=zip(*sorted_)
    return people,number

def plotgraph(people,number):
    import matplotlib.pyplot as plt
    plt.rcdefaults()
    import numpy as np
    import matplotlib.pyplot as plt

    # Peoples e Number já estão atualizados e ordenados
    y_pos = np.arange(len(people))
    # Number = os numeros de cada people
    error = np.random.rand(len(people))
    plt.barh(y_pos, number,0.8, align='center', alpha=0.5)
    plt.yticks(y_pos, people)
    plt.xlabel('Perguntas')
    plt.title('Quantia de visitas ao fórum')

    plt.show()

def convert_to_datetime(log):
    from datetime import datetime
    for x in log:
        date_object = datetime.strptime(log[x].date,"%d/%m/%Y %H:%M")
    return date_object
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
    # Faz um for ignorando a primeira linha
    for linha in xlread(arquivo):
        if not linha[0] == "Hora":
            # Carrega as 9 características em 1 e vai para o próximo
            log[i] = Champion(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8])
            i=1+i
    dates=convert_to_datetime(log)
    print (dates)
    print ("Carregamento concluido")
    # Cria o dicionary
    dic=create_dic_name_number(log)
    # Inicializa as variaveis para ordenar o dicionary
    people,number=sorted_number_dic(dic)
    # Plota o grafico
    plotgraph(people,number)



#--------------------------------------------- PLOT GRAPH ------------------------------------#
