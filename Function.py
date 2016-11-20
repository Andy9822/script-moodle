# encoding: utf-8
import xlrd
import os.path
import tkinter.filedialog as filedialog
from tkinter import *
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
import matplotlib.patches as mpatches

def xlread(arq_xls):
    # Abre o arquivo
    xls = xlrd.open_workbook(arq_xls)
    # Pega a primeira planilha do arquivo
    plan = xls.sheets()[0]
    # Para i de zero ao numero de linhas da planilha
    for i in range(plan.nrows):
        # Le os valores nas linhas da planilha
        yield plan.row_values(i)

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

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def pieChart(notSent,sent,see,write_see):
    # Data to plot
    explode1 = (0,0)
    explode2 = explode1

    colors = ['lightskyblue', 'lightcoral']
    sizes = [sent, notSent]
    colors2 = ['gold', 'yellowgreen']
    sizes2 = [see, write_see]

    if  sent>notSent:
        explode1 = (0.1, 0)
    elif notSent>sent:      # explode biggest slice
        explode1 = (0, 0.1)

    if  see>write_see:
        explode2 = (0.1, 0)
    elif write_see>see:      # explode biggest slice
        explode2 = (0, 0.1)

    # Seto a cor e o nome de cada legenda forçadamente
    first_legend = mpatches.Patch(color='lightskyblue',label = 'Participaram')
    second_legend = mpatches.Patch(color = 'lightcoral', label = 'Não participaram')
    third_legend = mpatches.Patch(color='gold', label ='Só visualizam dúvidas alheias')
    fourth_legend = mpatches.Patch(color='yellowgreen', label ='Mandaram e visualizam')
    # Plot
    plt.pie(sizes, explode=explode1,  colors=colors,autopct=make_autopct(sizes), shadow=True, startangle=90,radius=1.65, center = (-2.5,0))
    plt.pie(sizes2, explode=explode2,  colors=colors2,autopct=make_autopct(sizes2), shadow=True, startangle=45,radius=1.65, center = (2.5,0))

    # Ploto as legendas forçadas
    plt.gca().add_artist(plt.legend(handles=[first_legend,second_legend],loc = 2))
    plt.legend(handles=[third_legend,fourth_legend],loc = 4)
    plt.axis('equal')
    plt.show()

def create_and_plot_bar(log):
    # Cria o dicionary e plota o grafico em forma de barras (bom para saber por pessoa)
    # Cria o dicionary
    dic=create_dic_name_number(log)
    # Inicializa as variaveis para ordenar o dicionary
    people,number=sorted_number_dic(dic)
    # Plota o grafico
    plotgraph_bar(people,number)
    return dic

def create_and_plot_lines(weeklyPostsList):
    # Plota o gráfico em linhas (bom para saber por dias)
    # Inverte as listas para ficar em ordem crescente
    semanas=[]
    # Cria um array de strings com os NUMEROS DAS SEMANAS
    for x in range(len(weeklyPostsList)):
        semanas.append("Semana "+str(x+1))
    # Seta o X e Y para arrays de numeros
    x = np.array(range(len(weeklyPostsList)))
    y = np.array(weeklyPostsList)
    # Pega as semanas para colocar em baixo
    my_xticks = semanas
    #plt.figure(figsize=(30,10))
    # esse 1.0 é a distancia entre eles, se aumentar não vai plotar todos
    plt.xticks(np.arange(min(x), max(x)+1,1.0),my_xticks, rotation=40, size = 13)
    #plt.locator_params(axis='x',nbins=45)
    plt.ylabel('Number of entries')
    plt.title('All the students')
    # Colore o grafico
    with plt.style.context('fivethirtyeight'):
        # Titulo do grafico
        plt.plot(x,y,label = 'Everyone')
        plt.legend()
        plt.show()
# FUNÇÃO COMENTADO, FAZ VARIOS GRAFOS
"""
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
        plt.show()"""
def plotgraph_bar(Alunos):
    number = []
    people = []
    for x in Alunos:
        number.append(x.numParticipations)
        people.append(x.personName[:15])
    plt.rcdefaults()
    # Peoples e Number já estão atualizados e ordenados
    y_pos = np.arange(len(people))
    # Number = os numeros de cada people
    error = np.random.rand(len(people))
    #plt.figure(figsize=(30,10))
    with plt.style.context('fivethirtyeight'):
        plt.barh(y_pos, number,1, align='center', alpha=0.5)
        plt.yticks(y_pos, people,size = 9)
        plt.xlabel('Participações')
        plt.title('Quantia de visitas ao fórum')
    plt.show()

def convert_to_datetime(date_string):
    # Recebe uma Data em um String e converte para a class datetime
    # Recebe apenas a data com o comando. date
    date_object = datetime.strptime(date_string,"%d/%m/%Y").date()
    return date_object

def analyze_interaction(phrase,date):
    #Quando um novo aluno aparece, se analiza essa nova interacao do novo aluno
    participa = 0
    mensagem = 0
    if phrase == "Discussão visualizada":
        participa = 1
    elif phrase == "Algum conteúdo foi publicado" :
        participa = 1
        mensagem = 1
    if participa == 0 and mensagem == 0:
        date = ["01/01/9999"]

    return mensagem,participa,date

def update_interaction(phrase):
    #Para alunos que ja interagiram, apenas se atualiza esse novo tipo de interacao
    participa = 0
    mensagem = 0
    if phrase == "Discussão visualizada":
        participa = 1
    elif phrase == "Algum conteúdo foi publicado" :
        participa = 1
        mensagem = 1
    return mensagem,participa


def amount_interactions_pieChart(Alunos):
    # Dado uma lista de Alunos retorna quantos participaram e quantos nã
    #Tambem quantos só visualizaram posts e quantos mandaram perguntas tb
    participate = 0
    nonParticipate = 0
    justReaders = 0
    readWriters = 0
    for x in Alunos:
        if x.numMessages > 0 and x.numParticipations > 0:
            participate += 1
            readWriters +=1
        elif x.numParticipations > 0:
            justReaders +=1
            participate +=1
        else:
            nonParticipate +=1

    return participate,nonParticipate,justReaders,readWriters

def amount_messages(Alunos):
    # Dado uma lista de Alunos retorna quantos enviaram mensagens
    # E quantos não enviaram
    sent = 0
    not_sent = 0
    for x in Alunos:
        if x.numMessages > 0:
            sent += 1
    not_sent = len(Alunos) - sent
    return sent,not_sent

def which_participate(Alunos):
    # Devolve uma lista de Alunos que tiveram pelo menos UMA participação
    Epic_Alunos = []
    Poor_Students = []

    for x in Alunos:
        if x.numParticipations > 0:
            Epic_Alunos.append(x)
        else:
            Poor_Students.append(x)

    return Epic_Alunos,Poor_Students

#--------------------------- CONSISTÊNCIAS ------------------------------------#
def names_excel(file_):
    # Dado um arquivo excel no formato [w/e][w/e][Nome]....[w/e]
    # Retorna uma lista desses nomes
    if not file_:
        return False
    else:
        print("Carregando nomes...")
        # Inicia a lista
        names = []
        for linha in xlread(file_):
            if not linha[2] in names:
                names.append(linha[2])
        return names

def name_in_Aluno(Alunos,name):
    # Recebe uma lista de hero e um nome, retorna se essa nome esta na lista
    for x in Alunos:
        if x.personName == name:
            return True
    return False

def appendGhostStudents(studentsNameList,studentsList):
    for name in studentsNameList:
        if not name_in_Aluno(studentsList,name):
            studentsList.append(Aluno(name,0,0,convert_to_datetime("01/01/9999")))


def manageExistantStudent(studentsList,excelName,excelPhrase,inicial,final,data_splited,weeklyPostsList):
    for x in studentsList:
        if x.personName == excelName:
            newMessage,newParticipations = update_interaction(excelPhrase)
            x.numMessages += newMessage
            x.numParticipations += newParticipations
            #Se foi passado um intervalo de tempo e aluno criou um post, precisa ser atualizada lista de posts por semana
            if inicial and newMessage:
                weeklyPostsList = updateWeeklyPosts(weeklyPostsList,data_splited[0],inicial,final)
            #Se data eh menor que a de antes, pega essa nova
            if convert_to_datetime(data_splited[0]) < x.firstPost:
                x.firstPost = convert_to_datetime(data_splited[0])
    return studentsList,weeklyPostsList

def updateWeeklyPosts(weeklyPostsList,date_str,inicial,final):
    # Recebe a data do post e calcula em qual semana foi postado
    # para preencher na semana correspondente na lista
    date = convert_to_datetime(date_str)
    date = date.isocalendar()[1]
    date = date - inicial
    if date>= 0 and date <= (final-inicial):
        weeklyPostsList[date] += 1
    return weeklyPostsList


def create_weeklyPostsList(inicial, final):
    # Calcula intervalo de semanas e cria
    # preenche uma lista desses n elementos com zero (0)
    weeklyPostsList = []
    inicial = inicial.isocalendar()[1]
    final = final.isocalendar()[1]
    amountWeeks = final - inicial
    # Acrescenta 1 no amountweek para contar a PROPRIA semana
    for x in range(amountWeeks+1):
        weeklyPostsList.append(0)
    return weeklyPostsList,inicial,final

    # Recebe uma lista com nomes dos alunos para filtrar o log gerado pelo Moodle e pode receber um intervalo definido de datas para a consulta das infos
def loadErikaLog(file_,studentsNamesFile,inicial_str,final_str):
    # Devolve uma lista com os estudantes e suas infos das participações no forum de duvidas e uma lista com o numero de postagens por semana
    studentsList = []
    weeklyPostsList = []
    studentsNameList = names_excel(studentsNamesFile)
    # Converte as datas para DateTime
    inicial = convert_to_datetime(inicial_str)
    final = convert_to_datetime(final_str)
    if not file_:
        return studentsList,weeklyPostsList
    else:
        #Se foi passado um intervalo de tempo, precisa ser criada lista de posts por semana
        if inicial:
            weeklyPostsList, inicial,final =  create_weeklyPostsList(inicial,final)
        for linha in xlread(file_):
            if linha[1] != "Nome completo":
                data_splited=(linha[0].split(' '))
                if linha[1] in studentsNameList:
                #Testa se pessoa da vez eh um estudante. Se for, analiza se ja foi visto antes ou primeira aparição e se precisa ser tratado
                    if not name_in_Aluno(studentsList,linha[1]):
                        newMessages,newParticipations,data_splited = analyze_interaction(linha[5],data_splited)
                        if inicial and newMessages:
                            weeklyPostsList = updateWeeklyPosts(weeklyPostsList,data_splited[0],inicial,final)
                        studentsList.append(Aluno(linha[1],newMessages,newParticipations,convert_to_datetime(data_splited[0])))
                    else:
                        studentsList,weeklyPostsList = manageExistantStudent(studentsList,linha[1],linha[5],inicial,final,data_splited,weeklyPostsList)

        appendGhostStudents(studentsNameList,studentsList)
        return studentsList,weeklyPostsList

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

class Aluno:
    def __init__(self,personName,numMessages,numParticipations,firstPost):
        self.personName = personName
        self.numMessages = numMessages
        self.numParticipations = numParticipations
        self.firstPost =  firstPost

#---------------------------------------FUNCTIONS MENU-------------------------#
def menu_options():
    print("""
    Choose the GRAPH
    1. Quantos enviaram mensagem e não enviaram? Gráfico
    2. Para cada aluno que participou, quantas vezes cada alunou participou?
    3. Para cada aluno que participou, qual foi sua primeira participação?
    4. Número de perguntas por semana.
    5. Quais alunos participaram ao longo do semestre?
    0. Sair
    """)
#--------------------------MENU do pai vianna----------------------------------#
def menuXuxu():
    window = Tk()
    window.withdraw()
    print("ESCOLHA O EXCEL COM OS NOMES")
    namesFile_ =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Excel files","*.xlsx"),("all files","*.*")))
    print("ESCOLHA O EXCEL COM O LOG")
    file_ =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Excel files","*.xlsx"),("all files","*.*")))
    studentslist,weeklyPostsList = loadErikaLog(file_,namesFile_,"02/08/2016","02/11/2016")
    window.destroy()
    #pie chart
    Yesparticipate,nonParticipate,justReaders,readWriters = amount_interactions_pieChart(studentslist)
    listParticipants,listAbsents=which_participate(studentslist)
    loop = True
    while(loop):
        menu_options()
        option = input("Escolha: ")
        if option == '1':
            pieChart(nonParticipate,Yesparticipate,justReaders,readWriters)
        elif option == '2':
            for x in listParticipants:
                print (str(x.personName) + ("\nMensagens: ") + str(x.numMessages) + (" Participações: ") + str(x.numParticipations))
                print('\n\n')
            plotgraph_bar(listParticipants)
        elif option == '3':
            for x in listParticipants:
                print (str(x.personName) + ("\nFirst post: ") + str(x.firstPost))
                print('\n\n')
        elif option == '4':
            create_and_plot_lines(weeklyPostsList)
        elif option == '5':
            for x in listParticipants:
                print (("Participou: ") + str(x.personName))
            print ("\n")
            for x in listAbsents:
                print (("Não participou: ") + str (x.personName))
        elif option == '0':
            loop = False
        else:
            print ("Opção não encontrada")



# Main que chama menu xuxu

menuXuxu()
