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
    labels = 'Participaram', 'Não participaram'
    sizes = [sent, notSent]
    colors = ['gold', 'yellowgreen']
    if  sent>notSent:
        explode1 = (0.1, 0)
    elif notSent>sent:      # explode biggest slice
        explode1 = (0, 0.1)

    labels2 = 'Só visualizam dúvidas alheias', 'Mandaram e visualizam'
    sizes2 = [see, write_see]
    colors2 = ['lightskyblue', 'lightcoral']
    if  see>write_see:
        explode2 = (0.1, 0)
    elif write_see>see:      # explode biggest slice
        explode2 = (0, 0.1)

    # Plot
    plt.pie(sizes, explode=explode1,  colors=colors2,autopct=make_autopct(sizes), shadow=True, startangle=90,radius=1.65, center = (-2.5,0))

    plt.pie(sizes2, explode=explode2,  colors=colors,autopct=make_autopct(sizes2), shadow=True, startangle=45,radius=1.65, center = (2.5,0))




    first_legend = plt.legend(labels,loc = 2)
    ax = plt.gca().add_artist(first_legend)
    second_legend = plt.legend(labels2,loc = 4,ncol=1)



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

def create_and_plot_lines(weeklylist):
    # Plota o gráfico em linhas (bom para saber por dias)
    # Inverte as listas para ficar em ordem crescente
    semanas=[]
    # Cria um array de strings com os NUMEROS DAS SEMANAS
    for x in range(len(weeklylist)):
        semanas.append("Semana "+str(x+1))
    # Seta o X e Y para arrays de numeros
    x = np.array(range(len(weeklylist)))
    y = np.array(weeklylist)
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
    justSee = 0
    writeSee = 0
    for x in Alunos:
        if x.numMessages > 0 and x.numParticipations > 0:
            participate += 1
            writeSee +=1
        elif x.numParticipations > 0:
            justSee +=1
            participate +=1
        else:
            nonParticipate +=1

    return participate,nonParticipate,justSee,writeSee

def amount_interactions(Alunos):
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
    for x in Alunos:
        if x.numParticipations > 0:
            Epic_Alunos.append(x)
    return Epic_Alunos

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


def updateWeeklyPosts(weeklyList,date_str,inicial,final):
    # Recebe a data do post e calcula em qual semana foi postado
    # para preencher na semana correspondente na lista
    date = convert_to_datetime(date_str)
    date = date.isocalendar()[1]
    date = date - inicial
    if date>= 0 and date <= (final-inicial):
        weeklyList[date] += 1
    return weeklyList


def create_weeklyList(inicial, final):
    # Calcula intervalo de semanas e cria
    # preenche uma lista desses n elementos com zero (0)
    weeklyList = []
    inicial = inicial.isocalendar()[1]
    final = final.isocalendar()[1]
    amountWeeks = final - inicial
    # Acrescenta 1 no amountweek para contar a PROPRIA semana
    for x in range(amountWeeks+1):
        weeklyList.append(0)
    return weeklyList,inicial,final


def loadErikaLog(file_,studentsNames,inicial_str,final_str):
    # Recebe uma lista com nomes dos alunos para filtrar o log gerado pelo Moodle e pode receber um intervalo definido de datas para a consulta das infos
    # Devolve uma lista  com os estudantes e suas infos das participações no forum de duvidas e uma lista com o numero de postagens por semana
    studentsList = []
    names=["Nome completo"]
    # Converte as datas para DateTime
    inicial = convert_to_datetime(inicial_str)
    final = convert_to_datetime(final_str)
    if not file_:
        return studentsList
    else:
        #Se foi passado um intervalo de tempo, precisa ser criada lista de posts por semana
        if inicial:
            weeklyList, inicial,final =  create_weeklyList(inicial,final)
        for linha in xlread(file_):
            if not linha[1] in names:
                data_splited=(linha[0].split(' '))
                if linha[1] in studentsNames:
                    #Testa se pessoa da vez eh um estudante e precisa ser tratado
                    if not name_in_Aluno(studentsList,linha[1]):
                        #Se eh um novo estudante, analiza tipo de interacao
                        newMessages,newParticipations,data_splited = analyze_interaction(linha[5],data_splited)
                        #Se foi passado um intervalo de tempo e criou um post, precisa ser atualizada lista de posts por semana
                        if inicial and newMessages:
                            weeklyList = updateWeeklyPosts(weeklyList,data_splited[0],inicial,final)
                        studentsList.append(Aluno(linha[1],newMessages,newParticipations,convert_to_datetime(data_splited[0])))
                    else:
                        #Nao eh primeira vez do student, tem que ver se precisa atualizar alguma coisa
                        for x in studentsList:
                            if x.personName == linha[1]:
                                newMessage,newParticipations = update_interaction(linha[5])
                                x.numMessages += newMessage
                                x.numParticipations += newParticipations
                                #Se foi passado um intervalo de tempo e aluno criou um post, precisa ser atualizada lista de posts por semana
                                if inicial and newMessage:
                                    weeklyList = updateWeeklyPosts(weeklyList,data_splited[0],inicial,final)
                                #Se data eh menor que a de antes, pega essa nova
                                if convert_to_datetime(data_splited[0]) < x.firstPost:
                                    x.firstPost = convert_to_datetime(data_splited[0])
        return studentsList,weeklyList

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
    1. Quantos participaram e como participaram?
    2. Para cada aluno que participou, quantas vezes cada alunou participou?
    3. Para cada aluno que participou, qual foi sua primeira participação?
    4. Número de perguntas por semana.
    5. Quais alunos participaram ao longo do semestre?
    0. Sair
    """)
#--------------------------MENU do pai vianna----------------------------------#
def menuXuxu():
    root = Tk()
    root.withdraw()
    print("ESCOLHA O EXCEL COM OS NOMES")
    file_ =  filedialog.askopenfilename()
    namelist = names_excel(file_)
    print("ESCOLHA O EXCEL COM O LOG")
    file_ =  filedialog.askopenfilename()
    studentslist,weeklyList = loadErikaLog(file_,namelist,"02/08/2016","02/11/2016")
    root.destroy()
    loop = True
    sent,not_sent=amount_interactions(studentslist)
    #pie chart
    Yesparticipate,nonParticipate,justSee,writeSee = amount_interactions_pieChart(studentslist)

    participate=which_participate(studentslist)
    while(loop):
        menu_options()
        option = input("Escolha: ")
        if option == '1':
            print("Quantia que acessou: " ,sent)
            print("Quantia que não acessou: ",not_sent)
            pieChart(nonParticipate,Yesparticipate,justSee,writeSee)
        elif option == '2':
            for x in participate:
                print (str(x.personName) + ("\nMensagens: ") + str(x.numMessages) + (" Participações: ") + str(x.numParticipations))
                print('\n\n')
            plotgraph_bar(participate)
        elif option == '3':
            for x in participate:
                print (str(x.personName) + ("\nFirst post: ") + str(x.firstPost))
                print('\n\n')
        elif option == '4':
            create_and_plot_lines(weeklyList)
        elif option == '5':
            for x in participate:
                print (("Participou: ") + str(x.personName))
        elif option == '0':
            loop = False
        else:
            print ("Opção não encontrada")

#-------------------- MENU  Graphical User Interface --------------------------#
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






#--------------------------------------------- PLOT GRAPH ------------------------------------#


# Main que chama menu xuxu

menuXuxu()
