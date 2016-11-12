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

def create_and_plot_names(log):
    # Cria o dicionary e plota o grafico em forma de barras (bom para saber por pessoa)
    # Cria o dicionary
    dic=create_dic_name_number(log)
    # Inicializa as variaveis para ordenar o dicionary
    people,number=sorted_number_dic(dic)
    # Plota o grafico
    plotgraph_bar(people,number)
    return dic

def create_and_plot_days(log,names):
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
            print(days)
            print(numbers)
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
        plt.show()

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

#------------------------------------------ MENU ---------------------------------------------#
# Define uma constante para arquivo
#file_ =  filedialog.askopenfilename()
file_ = "C:\\Users\\leona\\Desktop\\Script\\script-moodle\\logs.xlsx"
if file_ == False:
    print("Nenhum arquivo achado")
else:
    log=load_log(file_)
    type_graph=True
    while type_graph:
        print("""
        Choose the GRAPH
        1. Bars
        2. Lines
        0. Exit
        """)
        type_graph = input("        Your type: ")
        if type_graph == '1':
            answer=True
            while answer:
                print ("""
                1. Plot without filter
                2. Plot a graph with filter
                3.
                0. Quit
                """)
                answer = input ("        What would you like to do ?  ")
                if answer == '1':
                    # Plota o gráfico
                    create_and_plot_names(log)
                elif answer == '2':
                    print("""
                    1. Filter the people
                    2. Filter the days
                    3. Filter both """)
                    # Escolhe a opção e faz os if's
                    filtering = input ("""
                    What filter ?  """)
                    if filtering == '1':
                        # Se for 1 vai fazer 1 laço pegando todos os nomes desejados a serem filtrados e plota o gráfico
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
                        # Plota o gráfico
                        create_and_plot_names(log_filtered)
                    elif filtering == '2':
                        # Se for 2 vai filtrar o log entre as 2 datas dada
                        print ("""
                        Format: DAY/MONTH/YEAR HOUR:MINUTES""")
                        first=convert_to_datetime(str(input("First Day ")))
                        last=convert_to_datetime(str(input("Last Day ")))
                        # Filtra o log
                        log_filtered=filter_days(log,first,last)
                        # Plota o gráfico
                        create_and_plot_names(log_filtered)
                    elif filtering == '3':
                        # Se for 3 faz os dois filtros e junta no final
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
                        # Filtro de dias
                        print ("      Format: DAY/MONTH/YEAR HOUR:MINUTES")
                        first=convert_to_datetime(str(input("First Day ")))
                        last=convert_to_datetime(str(input("Last Day ")))
                        # Filtra o log filtrado por nomes com dias agora
                        log_filtered=filter_days(log_filtered,first,last)
                        # Plota o gráfico
                        create_and_plot_names(log_filtered)
                        filtering = False
                    else:
                        # Se digitar outra opção diz que não encontrou
                        print ("""
                        Option not found
                        """)
                elif answer == '0':
                    # Se a resposta for sair, type_graph vai receber False e lá em baixo answer já recebe False
                    type_graph = False
                else:
                    # Se digitar outra opção diz que não encontrou
                    print ("""
                    Option not found
                    """)
                # Para sempre voltar para a escolha de GRAPH's
                answer = False
        elif type_graph == '2':
            answer=True
            while answer:
                print ("""
                1. Plot without filter
                2. Plot a graph with filter
                3.
                0. Quit
                """)
                answer = input ("        What would you like to do ?  ")
                if answer == '1':
                    # Plota o gráfico
                    create_and_plot_days(log_filtered,[])
                elif answer == '2':
                    print("""
                    1. Filter the people
                    2. Filter the days
                    3. Filter both """)
                    # Escolhe a opção e faz os if's
                    filtering = input ("""
                    What filter ?  """)
                    if filtering == '1':
                        # Se for 1 vai fazer 1 laço pegando todos os nomes desejados a serem filtrados e plota o gráfico
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
                        # Plota o gráfico
                        create_and_plot_days(log_filtered,names)
                    elif filtering == '2':
                        # Se for 2 vai filtrar o log entre as 2 datas dada
                        print ("""
                        Format: DAY/MONTH/YEAR HOUR:MINUTES""")
                        first=convert_to_datetime(str(input("First Day ")))
                        last=convert_to_datetime(str(input("Last Day ")))
                        # Filtra o log
                        log_filtered=filter_days(log,first,last)
                        # Plota o gráfico
                        create_and_plot_days(log_filtered,[])
                    elif filtering == '3':
                        # Se for 3 faz os dois filtros e junta no final
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
                        # Filtro de dias
                        print ("      Format: DAY/MONTH/YEAR HOUR:MINUTES")
                        first=convert_to_datetime(str(input("First Day ")))
                        last=convert_to_datetime(str(input("Last Day ")))
                        # Filtra o log filtrado por nomes com dias agora
                        log_filtered=filter_days(log_filtered,first,last)
                        # Plota o gráfico
                        create_and_plot_days(log_filtered,names)
                        filtering = False
                    else:
                        # Se digitar outra opção diz que não encontrou
                        print ("""
                        Option not found
                        """)
                elif answer == '0':
                    # Se a resposta for sair, type_graph vai receber False e lá em baixo answer já recebe False
                    type_graph = False
                else:
                    # Se digitar outra opção diz que não encontrou
                    print ("""
                    Option not found
                    """)
                # Para sempre voltar para a escolha de GRAPH's
                answer = False
        if type_graph == '0':
            # Sai do programa
            type_graph = False
#--------------------------------------------- PLOT GRAPH ------------------------------------#
