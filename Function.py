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
import matplotlib as mpl
from matplotlib.mlab import csv2rec
from matplotlib.cbook import get_sample_data
import re
import math
import pylab as pl

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
        #plt.figure(figsize=(30,10))
        # esse 1.0 é a distancia entre eles, se aumentar não vai plotar todos
        plt.xticks(np.arange(min(x), max(x)+1,1.0),my_xticks, rotation=290, size = 13)
        #plt.locator_params(axis='x',nbins=45)
        plt.ylabel('Número de acessos')
        plt.title('Todas as pessoas no log')
        # Colore o grafico
        with plt.style.context('fivethirtyeight'):
            # Titulo do grafico
            plt.plot(x,y,label = 'Everyone')
            plt.legend()
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
            #plt.figure(figsize=(30,10))
            my_yticks = names
            plt.xticks(np.arange(min(x), max(x)+1,1.0),my_xticks, rotation=290, size = 13)
            plt.ylabel('Número de acessos')
            # Titulo do grafico
            plt.title("Gráfico separado por pessoas")
            # Colore o gráfico
            with plt.style.context('fivethirtyeight'):
                # esse "=" é a legenda da pessoa
                plt.plot(x,y,label = names[i])
        # Vai mostrar o que foi plotado
        plt.legend()
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
    #plt.figure(figsize=(30,10))
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

#--------------------------- CONSISTÊNCIAS ------------------------------------#
def compare_people(log_name,list_names):
    # Compara um Nome com uma Lista de Nomes
    #S e esse nome for igual a qualquer uma da lista Retorna True, se não False
    for x in list_names:
        if log_name == x.upper() or log_name == 'Nome completo':
            return True
    return False

def who_exclude():
    # Pergunta se quer tirar alguém, se responder sim
    # Vai fazer append com a lista["Nome completo"]
    # Com os outros nomes e retornar essa lista de strings
    typing = input("Do you want filter off someone? 1. YES  0. NO ")
    if typing == '1' or typing == 'YES' or typing == "Y":
        typing = True
    elif typing == '0' or typing == 'NO' or typing == "N":
        typing = False
    else:
        typing = False
        print("Standart filter")
    names=["Nome completo"]
    while typing:
        names.append(str(input("Name: ")))
        print("1. One more time 0. Leave")
        typing=input("Choice: ")
        if typing == '0':
            typing = False
    return names

def nomes_excel(file_):
    # Dado um arquivo excel no formato [w/e][w/e][Nome]....[w/e]
    # Retorna uma lista desses nomes
    if not file_:
        return False
    else:
        print("Carregando nomes...")
        # Inicia a lista
        names = []
        for linha in xlread(file_):
            if not compare_people(linha[2],names):
                names.append(linha[2]).upper()
        return names

def visualizacoes(log,name):
    # Recebe o LOG e um NOME, retorna o numero de mensagens e participacoes nesse log
    participa = 0
    mensagem = 0
    for linha in log:
        if log[linha].name == name:
            if log[linha].event == 'Discussão visualizada':
                participa = participa + 1
            elif log[linha].event == 'Algum conteúdo foi publicado':
                participa = participa + 1
                mensagem = mensagem + 1
    print (participa)
    print (mensagem)
    return participa,mensagem

def load_log(file_):
    # Recebe um arquivo EXCEL e retorna a log
    # Também pergunta se deseja retirar alguém do log
    if not file_:
        return False
    else:
        names=who_exclude()
        print ("Carregando arquivo...")
        # Inicia o dic   # MUDAR DEPOIS #
        log={}
        i=0
        # Faz um for ignorando a primeira linha
        for linha in xlread(file_):
            if not compare_people(linha[1],names):
                # Carrega as 9 características em 1 e vai para o próximo
                # Separa a data em DATA[0] HORA[1]
                data_splited=(linha[0].split(' '))
                # Converte a data separada para datetime
                log[i] = Champion(convert_to_datetime(data_splited[0]),linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8])
                i=1+i
        print ("Carregamento concluido")
        return log


def load_logGUI(file_,names):
    # Recebe um arquivo EXCEL e retorna a log
    # Também pergunta se deseja retirar alguém do log
    if not file_:
        return False
    else:
        print ("Carregando arquivo...")
        # Inicia a lista
        names=["Nome completo"]
        log={}
        i=0
        # Faz um for ignorando a primeira linha
        for linha in xlread(file_):
            if not compare_people(linha[1],names):
                # Carrega as 9 características em 1 e vai para o próximo
                # Separa a data em DATA[0] HORA[1]
                data_splited=(linha[0].split(' '))
                # Converte a data separada para datetime
                log[i] = Champion(convert_to_datetime(data_splited[0]),linha[1],linha[2],linha[3],linha[4],linha[5],linha[6],linha[7],linha[8])
                i=1+i
        print ("Carregamento concluido")
        return log


def loadErikaLog(file_,studentsNames):
    #Recebe uma lista com nomes dos alunos EM MAIUSCULA
    #Devolve uma lista apenas com os estudantes e suas infos das participações no forum de duvidas
    studentsList = []
    names=["Nome completo"]

    if not file_:
        return studentsList
    else:
        # Faz um for ignorando a primeira linha
        for linha in xlread(file_):
            if not compare_people(linha[1],names):
                data_splited=(linha[0].split(' '))
                novoMane = True
                #Testa se pessoa da vez eh um estudante e precisa ser tratado
                if linha[1] in studentsNames:
                    for x in studentsList:
                        if x.personName == linha[1]:
                            novoMane = False
                            break
                    if novoMane:
                        #Se eh um mane novo nois so adiciona ele mesmo
                        participa = 0
                        mensagem = 0
                        if linha[5] == "Discussão visualizada":
                            participa = 1
                        elif linha[5] == "Algum conteúdo foi publicado" :
                            participa = 1
                            mensagem = 1
                        #Antes de fazer append verifica se nessa primeira aparicao dele ele ja interagiu
                        studentsList.append( Hero(linha[1],mensagem,participa,convert_to_datetime(data_splited[0])) )
                    elif not novoMane :
                        #Nao eh primeira vez do student, tem que ver se precisa atualizar alguma coisa
                        for x in studentsList:
                            if x.personName == linha[1]:
                                if linha[5] == "Algum conteúdo foi publicado" :
                                    #Se publicou conteudo, é mensagem a mais e participacao a mais (!!!!!!!talvez desconsiderar participacao e ser so mensagem !!!!!!)
                                    x.numMessages += 1
                                    x.numParticipations += 1
                                    if convert_to_datetime(data_splited[0]) < x.firstPost:
                                        #Se data eh menor que a de antes, pega essa nova
                                        x.firstPost = convert_to_datetime(data_splited[0])
                                elif linha[5] == "Discussão visualizada":
                                    #Se eh so discussao visualizada, so add participacao por ter visto perguntas de coleguinhas
                                    x.numParticipations += 1
                                    if convert_to_datetime(data_splited[0]) < x.firstPost:
                                        #Se data eh menor que a de antes, pega essa nova
                                        x.firstPost = convert_to_datetime(data_splited[0])
    return studentsList


def is_date(string):
    # Recebe um string e verifica se está no formato date compatível
    format_1= re.compile('.{2}/.{2}/.{4}')
    format_2 = re.compile('.{2}/.{1}/.{4}')
    format_3 = re.compile('.{1}/.{2}/.{4}')
    format_4 = re.compile('.{1}/.{1}/.{4}')
    if format_1.match(string) or format_2.match(string) or format_3.match(string) or format_4.match(string) :
        return True
    else:
        False

def testNameInLog(log,names):
    # Retorna true se tem apariçao"de "name" no log passado
    # Verifica linha por linha se tem alguém com o mesmo nome, se tiver seta como true
    for x in range(len(names)):
        if how_visua_name(log,names[x]) != 0:
            return True
    return False

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

class Hero:
    def __init__(self,personName,numMessages,numParticipations,firstPost):
        self.personName = personName
        self.numMessages = numMessages
        self.numParticipations = numParticipations
        self.firstPost =  firstPost

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

    while naming:
        names.append(input("""
        Insert the name: """).upper())
        naming=input("""
        1. One more time
        0. Leave
        Continue? """)
        if naming == '0':
            if testNameInLog(log,names):
                naming=False
            else:
                print ("""\n        No one is in the log, please insert someone who is in the log""")
    # Filtra o log com os nomes
    log_filtered=filter_names(log,names)
    return log_filtered,names


def menu_filter_namesGUI(log,names):
    if testNameInLog(log,names):
        log=filter_names(log,names)
    else:
        print ("""\nNo one is in the log, will be considerated all the people """)
    return log

def menu_filter_days(log):
    inserindo=True
    while inserindo:
        print ("""
        Format: DAY/MONTH/YEAR""")
        # Recebe os dois strings
        first=str(input("        First Day "))
        last=str(input("        Last Day "))
        # Testa se são do formato desejado, caso não continua no loop
        if is_date(first) and is_date(last):
            first=convert_to_datetime(first)
            last=convert_to_datetime(last)
            inserindo=False
        else:
            print("""\n        Alguma data foi no formato errado""")
    # Filtra o log
    log_filtered=filter_days(log,first,last)
    return log_filtered

def menu_filter_days_names(log):
    names=[]
    log_filtered=menu_filter_days(log)
    log_filtered,names=menu_filter_names(log_filtered)
    return log_filtered,names

#------------------------------------------ MENU do pai vianna---------------------------------------------#
file_ =  filedialog.askopenfilename()
log = load_log(file_)
visualizacoes(log,'IVONE MALUF MEDERO')
def menuXuxu():
    #Define uma constante para arquivo
    file_ =  filedialog.askopenfilename()
    #file_ = "C:\\Users\\leona\\Desktop\\Script\\script-moodle\\logs.xlsx"
    if file_ == False:
        print("Nenhum arquivo achado")
    else:
        log=load_log(file_)
        menu_1 = True
        while menu_1:
            menu_prints_options_with_or_without() # 1- Sem, 2 - Com, 0 - Sair
            opt_menu_1 = input("        Choose W/OUT: ")
            # Inicializa variavel
            names=[]
            if opt_menu_1 == '1':
                # Inicializa log_filtered
                log_filtered=log
            elif opt_menu_1 == '2':
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
                        # Fica no menu se errar
            menu_3 = True
            if opt_menu_1 == '0':
                # Sai do menu e do programa consequentemente
                menu_1 = False
                menu_3 = False
            elif opt_menu_1 != '1' and opt_menu_1 != '2' and opt_menu_1 != '0':
                print("        Opção não encontrada")
                menu_3 = False
            while menu_3:
                menu_print_options_graph() # 1 - Bars, 2 - Lines
                opt_menu_3 = input("        Choose Graph: ")
                if opt_menu_3 == '1':
                    # Se escolheu BARS plota BAR
                    create_and_plot_bar(log_filtered)
                    # Sai do menu_3
                    menu_3 = False
                elif opt_menu_3 == '2':
                    # Se escolheu LINES plota LINES
                    create_and_plot_lines(log_filtered,names)
                    # Sai do menu_3
                    menu_3 = False




#------------------------------------------ MENU  Graphical User Interface ---------------------------------------------#
#


# Define uma constante para arquivo
#file_ =  filedialog.askopenfilename()
#file_ = "C:\\Users\\leona\\Desktop\\Script\\script-moodle\\logs.xlsx"

def mainMenuGraph(file_,log,filterOption,names,inicial,final):

    log_filtered = log
    print("data inicio = ",inicial)
    print("data final  = ", final)
    print("filter option =  ",filterOption)


    if  is_date(inicial):
        print("considerei que tinha date")
        inicial = convert_to_datetime(inicial)
        final = convert_to_datetime(final)
        log_filtered=filter_days(log,inicial,final)

    if log_filtered:
        if filterOption == 1:
            # Se escolheu BARS plota BAR
            create_and_plot_bar(log_filtered)

        elif filterOption == 2:
            # Se escolheu LINES plota LINES
            create_and_plot_lines(log_filtered,names)
    else:
        print("Log vazio\nNao tem nada nesse intervalo c as especificacoes passadas")


# ''
###########################################################################################
from tkinter import *

class Interface(Frame):

    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.escolheuArquivo = False
        self.escolheuFiltro = False
        self.escolheuInteravalo = False
        self.escolheuGrafico = False
        self.podeMostrar =  False
        self.parent = master
        self.initUI()
        self.inicio = "oi"
        self.final = "oi"
        self.namesFilter =[]
        self.namesExclude = ["Nome completo"]
        self.log = {}
        self.filterOption = IntVar()
        self.filterButtons()




    def initUI(self):

        self.parent.title("Simple menu")

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Escolher arquivo...", command=self.chooseFile)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

    def onExit(self):
        self.quit()


    def exName(self):
        newName = self.excludePerson.get()
        print("tamanho = ", len(self.namesExclude))
        if all(x.isalpha() or x.isspace() for x in newName) and newName!= "":
            newName =  newName.upper()
            if newName in self.namesExclude:
                print("Esse nome ja foi adicionado antes ao filtro")
            else:
                self.namesExclude.append(newName)
                print(self.namesExclude)
                print("excluido")
        else:
            print("Nomes so podem ter letras e espaços mane")
        self.excludePerson.delete(0,END)
        self.excludePerson.insert(0,"")


    def addName(self):
        newName = self.entryPerson.get().upper()
        if all(x.isalpha() or x.isspace() for x in newName) and newName not in self.namesFilter and newName != "":
            self.namesFilter.append(newName)
            print(self.namesFilter)
        else:
            print("SO QUERO LETRAS MANE")
        self.entryPerson.delete(0,END)
        self.entryPerson.insert(0,"pega na pika q ela goza")


    def update_Grafico(self):
        self.chosenGraphic = self.tipoGrafico.get()
        self.escolheuGrafico  = True

    def rodaGraph(self):
        if  self.escolheuFiltro == True  and self.escolheuArquivo == True:
            self.log=load_logGUI(self.file_ , ["Nome completo"])
            chosenPeople = self.namesFilter
            booleanTest =  True
            if len(self.namesFilter) > 0  and len(self.namesExclude) > 1:
                chosenPeople = [name for name in self.namesFilter if name not in self.namesExclude]
                self.log = load_logGUI(self.file_,["Nome completo"])
            else:
                self.log = load_logGUI(self.file_,self.namesExclude)
            if len(chosenPeople) > 0:
                if testNameInLog(self.log,chosenPeople) ==  False:
                    print("Erro:Nenhuma das pessoas inseridas acessaram no intervalo determinado")
                    booleanTest = False
                else:
                    self.log = menu_filter_namesGUI(self.log,chosenPeople)

            if booleanTest:
                mainMenuGraph(self.file_ ,self.log,self.typeGraphic,chosenPeople,self.inicio,self.final)
        else:
            print("Escolha e preencha todas as opcoes necessarias")


    def rodaStats(self):
        if  self.escolheuFiltro == True and self.escolheuInteravalo ==  True and self.escolheuArquivo == True:
            print("Vamo clan STATS")
        else:
            print("Escolha e preencha todas as opcoes necessarias para fazer statistics")

    def update_Option(self):
        self.typeGraphic = self.filterOption.get()
        print(self.typeGraphic)
        if self.escolheuFiltro == False:
            self.escolheuFiltro = True
            self.filterButtons()
        else:
            self.escolheuFiltro = True

    def confirmDates(self):
        self.inicio = self.startDate.get()
        self.final = self.finalDate.get()
        if is_date(self.inicio) and is_date(self.final):
            self.escolheuInteravalo = True
            print("Intervalo correto")
        else:
            print("Not invervalo")
            self.inicio ="oi"

    def fecharPrograma(self):
        exit()

    def resetNames(self):
        self.namesFilter =[]
        self.namesExclude = ["Nome completo"]
        self.log = {}

    def resetDates(self):
        self.inicio = "oi"
        self.final = "oi"

    def chooseFile(self):
        # Define uma constante para arquivo
        self.file_ =  filedialog.askopenfilename()
        names=["Nome completo"]
        #file_ = "C:\\Users\\Andy\\Desktop\\Python\\logs.xlsx"
        # Da load no arquivo e transforma em um dicionary com classe
        self.log=load_logGUI(self.file_ , names)
        if self.log == False:
            print("Nenhum arquivo achado")
        else:
            print("PEGUEI CARALHO")
            self.resetNames()
            self.escolheuArquivo =  True
            self.filterButtons()

    def filterButtons(self):

        #self.botaoArquivo = Button(self, text = "Escolher arquivo dos logs...",bd = 5,relief = RAISED,bg = "gray",fg = "black",command = self.chooseFile ).grid( row = 0, column = 0)

        if self.escolheuArquivo == True :
            #Label(self,highlightthickness= 3, fg = "white",bg = "gray",text = "Escolha qual filtro utilizar ",bd = 3,relief=GROOVE,anchor=W).grid(row = 0,column = 0)

            #Label(self,highlightthickness= 3, fg = "white",bg = "gray",text = "Escolha o intervalo de tempo ",bd = 3,relief=GROOVE,anchor=W).grid(row = 0,column = 1, sticky = W)

            Label(self, text = "Selecione um filtro:",state = ACTIVE).grid(row= 1,column = 0, sticky =W)

            self.option = IntVar()

            Label(self, text = " ",state = ACTIVE).grid(row= 2,column = 0, sticky =W)


            #Bloco dos botoes e entradas dos filtros de datas
            self.infoData1 = Label(self, text = "Data inicial (dd/mm/ano)")
            self.infoData1.grid(row= 1,column = 1,sticky = W)
            self.infoData2 = Label(self, text =  "Data final (dd/mm/ano)")
            self.infoData2.grid(row= 1,column = 2,columnspan = 2,sticky = W)
            self.startDate = Entry(self,width = 22)
            self.startDate.grid(row = 2, column = 1,sticky = W)
            self.finalDate = Entry(self,width = 22)
            self.finalDate.grid(row = 2, column = 2,sticky = W)
            self.confirmDatesBtn =  Button(self,text = "                            Confirmar Datas                                ",bd = 2,command = self.confirmDates)
            self.confirmDatesBtn.grid(row = 3, column = 1, sticky = W, columnspan = 2)

            self.resetDatesBtn =  Button(self,text = "         Resetar Datas        ",bd = 2,command = self.resetDates)
            self.resetDatesBtn.grid(row = 10, column = 2, sticky = SW)

            #Bloco dos botoes e entrads de filros de pessoas
            self.infoPessoas = Label(self, text =  "Filtrar por pessoas  ")
            self.infoPessoas.grid(row= 5,column = 1, columnspan = 2)
            self.entryPerson = Entry(self,width = 21)
            self.entryPerson.grid(row = 6, column = 1,sticky = W)
            self.confirmAddPerson =  Button(self,text = "Adicionar pessoa",height = 1,width = 17,bd = 2,command = self.addName)
            self.confirmAddPerson.grid(row = 7, column = 1, sticky = W)
            self.excludePerson = Entry(self,width = 21)
            self.excludePerson.grid(row = 6, column = 2,sticky = W)
            self.confirmExcludePerson =  Button(self,text = "Excluir pessoa ",height = 1,width = 17,bd = 2,command = self.exName)
            self.confirmExcludePerson.grid(row = 7, column = 2, sticky = W)
            self.resetPeople =  Button(self,text = "Resetar filtros de pessoas ",width = 18,bd = 2,command = self.resetNames)
            self.resetPeople.grid(row = 10, column = 1, sticky = SW)

            if self.escolheuFiltro:
                self.runButton =  Button(self,text = "  Plot Graph",bg = "green", fg = "white",width = 16,height = 3,command = self.rodaGraph)
                self.runButton.grid(row = 6, column = 0,rowspan = 2, sticky = W)

            self.runButton =  Button(self,text = "  Plot Statistics",bg = "gray", fg = "white",width = 16,height = 3,command = self.rodaStats)
            self.runButton.grid(row = 9, column = 0,rowspan = 2, sticky = SW)

            Label(self, text = " ",state = ACTIVE).grid(row= 5,column = 0, sticky =W)

            self.title6 = Label(self, text = " ",state = ACTIVE)
            self.title6.grid(row= 8,column = 0, sticky =W)

            #self.tipoGrafico = IntVar()
            #self.barrasButton = Radiobutton(self,text = "Nº acessos totais ",indicatoron = 1,variable = self.tipoGrafico, value = 1 ,command = self.update_Grafico)
            #self.barrasButton.grid(row = 8,column = 0,sticky = W)

            #self.linesButton = Radiobutton(self,text = "Nº acessos por dia  ",indicatoron = 1,variable = self.tipoGrafico, value = 2 ,command = self.update_Grafico)
            #self.linesButton.grid(row = 9,column = 0,sticky = W)

            self.accessButton = Radiobutton(self,text = "Acessos por pessoa ",bd = 2,relief =  GROOVE,indicatoron = 1,variable = self.filterOption, value = 1 ,command = self.update_Option)
            self.accessButton.grid(row = 3,column = 0,sticky = W)

            self.daysButton = Radiobutton(self,text = "Acessos por dia        ",bd = 2,relief =  GROOVE,indicatoron = 1,variable = self.filterOption, value = 2 ,command = self.update_Option)
            self.daysButton.grid(row = 4,column = 0,sticky = W)

            #self.aviso = Text(self, height = 2, width = 35,relief = RAISED,bd = 5,state = DISABLED).grid(row = 9, column = 0,sticky = W,columnspan = 2)


def menuAndy():
    window = Tk()
    window.title("GUI")
    window.geometry("500x300")
    b = Interface(window)
    window.mainloop()


qualMenu = input("1 para menu em CMD(ou y ou yes ou Y)\nQualquer outra coisa para menu em GUI\n")

if qualMenu == "1" or  qualMenu == "y" or qualMenu == "yes" or qualMenu == "Y"  :
    menuXuxu()
else:
    menuAndy()




#--------------------------------------------- PLOT GRAPH ------------------------------------#
