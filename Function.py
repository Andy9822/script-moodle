# encoding: utf-8
import xlrd
import os.path
import tkinter.filedialog as filedialog
from datetime import datetime
from datetime import date
from operator import itemgetter
import operator
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.cbook as cbook
from matplotlib.mlab import csv2rec
from matplotlib.cbook import get_sample_data
import re

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

def how_visua_name(log,name):
    # Retorna o numero de "aparições" de "a"
    a=0
    # Verifica linha por linha se tem alguém com o mesmo nome, se tiver acrescenta no valor a ser devolvido
    for linha in log:
        if log[linha].name == name:
            a=a+1
    return a

def how_visua_day(log,day):
    # Retorna quantos acessos ocorreu no Dia
    a=0
    #Verifica linha por linha se o dia foi acessado, se foi acrescenta 1
    for linha in log:
        if log[linha].date == day:
            a=a+1
    return a

def how_visua_day_name(log,day,name):
    # Retorna quantos acessos ocorreu no Dia
    a=0
    #Verifica linha por linha se o dia foi acessado por aquela pessoa, se for acrescenta 1
    for linha in log:
        if log[linha].date == day:
            if log[linha].name == name:
                a=a+1
    return a

def filter_names(log,names):
    # Recebe o Log e uma lista de nomes, retorna o Log somente com esses nomes
    log_filtered = {}
    i=0
    # Para todo nome em NAMES verifica se ele esta no log, se estiver coloca em log_filtered
    for x in log:
        if log[x].name in names:
            log_filtered[i]=log[x]
            i=i+1
    return log_filtered

def filter_days(log,first,last): # LEMBRAR: O FORMATO DEVE SER "DIAS/MES/ANO HORA:MINUTOS" Ex: 26/03/1996 05:51
    # Recebe o log e dois dias, retorna o log entre esses dois dias INCLUSIVE esses dias
    log_filtered={}
    i=0
    for x in log:
        if log[x].date >= first and log[x].date <= last:
            log_filtered[i]=log[x]
            i=i+1
    return log_filtered

def create_dic_name_number(log):
    # Cria um dicionario com "Nome da pessoa" : "Quantos visualizaçoes"
    dic={}
    for linha in log:
        if not log[linha].name in dic:
            dic[log[linha].name] = how_visua_name(log,log[linha].name)
    return dic

def create_dic_days_number(log):
    "NÃO ESTÁ SENDO USADO"
    # Cria um dicionario com "Dia" : "Quantidade de acessos"
    dic = {}
    for linha in log:
        if not log[linha].date in dic:
            dic[log[linha].date]= how_visua_day(log,log[linha].date)
    return dic

def create_and_plot_bar(log):
    # Cria o dicionary e plota o grafico em forma de barras (bom para saber por pessoa)
    # Cria o dicionary
    dic=create_dic_name_number(log)
    # Inicializa as variaveis para ordenar o dicionary
    people,number=sorted_number_dic(dic)
    # Plota o grafico
    plotgraph_bar(people,number)
    return dic

def create_and_plot_lines(log,names):
    # Plota o gráfico em linhas (bom para saber por dias)
    # Recebe o log e divide em 2 listas
    if not names:
        days,numbers = create_list(log)
        # Inverte as listas para ficar em ordem crescente
        days.reverse()
        numbers.reverse()
        # Seta o X e Y para arrays de numeros
        x = np.array(range(len(days)))
        y = np.array(numbers)
        # Pega as datas para colocar em baixo
        my_xticks = days
        plt.xticks(np.arange(min(x), max(x)+1,1.0),my_xticks, rotation=90)
        plt.ylabel('Número de acessos')
        plt.title('Todas as pessoas no log')
        with plt.style.context('fivethirtyeight'):
            plt.plot(x,y)
            plt.show()
    else:
        # Se tiver algo no names
        people=[]
        # Vai fazer uma lista de listas com Pessoa[dias,numeros]
        for x in names:
            numbers=[]
            days=[]
            for y in log:
                if not log[y].date in days:
                    # Faz uma lista de numeros acessados naquele dia pelo "x"
                    numbers.append(how_visua_day_name(log,log[y].date,x))
                    # Faz uma lista de datas
                    days.append(log[y].date)
            # Juntas as duas listas em 1 pessoa
            people.append([days,numbers])
            # People [x][0] = Dates People [x][1] = Acessos no dia
        for i in range(len(names)):
            # Vai plotar um gráfico para cada pessoa do names
            numbers=[]
            days=[]
            days = people[i][0]
            numbers = people[i][1]
            days.reverse()
            numbers.reverse()
            # Seta o X e Y para arrays de numeros
            x = np.array(range(len(days)))
            y = np.array(numbers)
            # Pega as datas para colocar em baixo
            my_xticks = days
            plt.xticks(np.arange(min(x), max(x)+1,1.0),my_xticks, rotation=90)
            plt.ylabel('Número de acessos')
            plt.title(names[i])
            plt.plot(x,y)
        # Vai mostrar o que foi plotado
        plt.show()

def create_and_plot_days_with_names(log):
    # Cria um gráfico com várias linhas e cada uma representa uma pessoas
    days,numbers = create_list(log)
    x = np.linspace(0, 10)
    with plt.style.context('fivethirtyeight'):
        fname = cbook.get_sample_data('msft.csv', asfileobj=False)
        # test 5; single subplot
        plt.plotfile(fname, ('date', 'open', 'high', 'low', 'close'), subplots=True)
        plt.show() # USO FUTURO

def create_list(log):
    # Recebe um log e cria duas listas com seus dias e seus acessos respectivos no mesmo indice
    days=[]
    numbers=[]
    for x in log:
        if not log[x].date in days:
            days.append(log[x].date)
            numbers.append(how_visua_day(log,log[x].date))
    return days,numbers

def present_people(dic):
    # Recebe um dicionário e retorna uma lista com todos os nomes (keys)
    ppl = []
    for key in dic:
        ppl.append(key)
    return ppl

def sorted_number_dic(dic):
    # Recebe o dicionary e retorna 2 listas people and number
    people=[]
    number=[]
    # Passa o dicionary para uma lista de tuplas e ordenada essa lista
    sorted_ = sorted(dic.items(), key = operator.itemgetter(1))
    people,number=zip(*sorted_)
    return people,number

def plotgraph_bar(people,number):
    plt.rcdefaults()
    # Peoples e Number já estão atualizados e ordenados
    y_pos = np.arange(len(people))
    # Number = os numeros de cada people
    error = np.random.rand(len(people))
    plt.barh(y_pos, number,0.8, align='center', alpha=0.5)
    plt.yticks(y_pos, people)
    plt.xlabel('Perguntas')
    plt.title('Quantia de visitas ao fórum')
    plt.show()

def convert_to_datetime(date_string):
    # Recebe uma Data em um String e converte para a class datetime
    # Recebe apenas a data com o comando. date
    date_object = datetime.strptime(date_string,"%d/%m/%Y").date()
    return date_object

def load_log(file_):
    # Recebe um arquivo EXCEL e retorna a log
    if not file_:
        return False
    else:
        print ("Carregando arquivo...")
        # Inicia a lista
        log={}
        i=0
        # Faz um for ignorando a primeira linha
        for linha in xlread(file_):
            if linha[0] != "Hora":
                # Carrega as 9 características em 1 e vai para o próximo
                # Separa a data em DATA[0] HORA[1]
                data_splited=(linha[0].split(' '))
                # Converte a data separada para datetime
                log[i] = Champion(convert_to_datetime(data_splited[0]),linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8])
                i=1+i
        print ("Carregamento concluido")
        return log

def is_date(string):
    # Recebe um string e verifica se está no formato date compatível
    format_= re.compile('.{2}/.{2}/.{4}')
    if format_.match(string):
        return True
    else:
        False

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
#---------------------------------------FUNCTIONS MENU----------------------------------------#
def menu_print_options_graph():
    print("""
    Choose the GRAPH
    1. Bars
    2. Lines
    """)

def menu_prints_options_with_or_without():
    print ("""
    1. Plot without filter
    2. Plot a graph with filter
    0. Exit
    """)

def menu_prints_options_filter():
    print("""
    1. Filter the people
    2. Filter the days
    3. Filter both """)

def menu_filter_names(log):
    naming = True
    names=[]
    while naming:
        names.append(input("""
        Insert the name: """))
        naming=input("""
        1. One more time
        0. Leave
        Continue? """)
        if naming == '0':
            naming=False
    # Filtra o log com os nomes
    log_filtered=filter_names(log,names)
    return log_filtered,names

def menu_filter_days(log):
    inserindo=True
    while inserindo:
        print ("""
        Format: DAY/MONTH/YEAR HOUR:MINUTES""")
        # Recebe os dois strings
        first=str(input("        First Day "))
        last=str(input("        Last Day "))
        # Testa se são do formato desejado, caso não continua no loop
        if is_date(first) and is_date(last):
            first=convert_to_datetime(first)
            last=convert_to_datetime(last)
            inserindo=False
        else:
            print("""
            Alguma data foi no formato errado""")
    # Filtra o log
    log_filtered=filter_days(log,first,last)
    return log_filtered

def menu_filter_days_names(log):
    names=[]
    log_filtered=menu_filter_days(log)
    log_filtered,names=menu_filter_names(log_filtered)
    return log_filtered,names

#------------------------------------------ MENU ---------------------------------------------#
# Define uma constante para arquivo
#file_ =  filedialog.askopenfilename()
file_ = "C:\\Users\\leona\\Desktop\\Script\\script-moodle\\logs.xlsx"
if file_ == False:
    print("Nenhum arquivo achado")
else:
    log=load_log(file_)
    menu_1 = True
    while menu_1:
        menu_prints_options_with_or_without() # 1- Sem, 2 - Com, 0 - Sair
        opt_menu_1 = input("        Choose W/OUT: ")
        if opt_menu_1 == '1':
            log_filtered=log
            names=[]
        if opt_menu_1 == '2':
            menu_2 = True
            while menu_2:
                menu_prints_options_filter()    # 1 - Pessoas, 2 - Dias, 3 - Ambos
                opt_menu_2 = input("        Choose Filter: ")
                if opt_menu_2 == '1':
                    log_filtered,names= menu_filter_names(log)
                    # Sai desse menu_2 caso tenha acertado a opção
                    menu_2 = False
                elif opt_menu_2 == '2':
                    log_filtered = menu_filter_days(log)
                    # Sai desse menu_2 caso tenha acertado a opção
                    menu_2 = False
                elif opt_menu_2 == '3':
                    log_filtered,names= menu_filter_days_names(log)
                    # Sai desse menu_2 caso tenha acertado a opção
                    menu_2 = False
                else:
                    print("        Opção não encontrada")
                    # Fica no menu se errour
        menu_3 = True
        while menu_3:
            menu_print_options_graph() # 1 - Bars, 2 - Lines
            opt_menu_3 = input("        Choose Graph: ")
            if opt_menu_3 == '1':
                create_and_plot_bar(log_filtered)
                menu_3 = False
            elif opt_menu_3 == '2':
                create_and_plot_lines(log_filtered,names)
                # Sai do menu_3
                menu_3 = False
        if opt_menu_1 == '0':
            # Sai do menu e do programa consequentemente
            menu_1 = False
        else:
            print("        Opção não encontrada")
