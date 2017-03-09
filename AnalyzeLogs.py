# encoding: utf-8
import sys
import argparse
try:
    from tkinter import *
except:
    print ("Module 'tkinter' not found, you may have python 2.7 AND 3.5, please read the instructions")
    sys.exit(0)
try:
    import xlrd
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.ticker as ticker
    import matplotlib.cbook as cbook
    import matplotlib as mpl
    from matplotlib.mlab import csv2rec
    from matplotlib.cbook import get_sample_data
    import matplotlib.patches as mpatches
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, inch
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
    from reportlab.lib.styles import getSampleStyleSheet
except:
    print ("Some modules can't be found, extract the 'imports.rar' in the AnalyzeLogs folder")
    sys.exit(0)
from datetime import datetime
from datetime import date
from operator import itemgetter


# Constantes definidas
# São as frases que vão ser filtradas do logo, fácil alteração
# Só os nomes dos gráficos e do PDF que ficaram como antigos
first_phrase = 'Discussão visualizada'
second_phrase = 'Algum conteúdo foi publicado'

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

def pie_chart(not_sent,sent,see,write_see):
    # Data to plot
    explode1 = (0,0)
    explode2 = explode1

    colors = ['lightskyblue', 'lightcoral']
    sizes = [sent, not_sent]
    colors2 = ['gold', 'yellowgreen']
    sizes2 = [see, write_see]

    if  sent>not_sent:
        explode1 = (0.1, 0)
    elif not_sent>sent:      # explode biggest slice
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
    with plt.style.context('fivethirtyeight'):
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

def create_and_plot_lines(weekly_posts_list):
    # Plota o gráfico em linhas (bom para saber por dias)
    # Inverte as listas para ficar em ordem crescente
    weeks=[]
    # Cria um array de strings com os NUMEROS DAS weeks
    for x in range(len(weekly_posts_list)):
        weeks.append("Semana "+str(x+1))
    # Seta o X e Y para arrays de numeros
    x = np.array(range(len(weekly_posts_list)))
    y = np.array(weekly_posts_list)
    # Pega as weeks para colocar em baixo
    my_xticks = weeks
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

def plotgraph_bar(students):
    number = []
    people = []
    for student in students:
        number.append(student.num_participations)
        people.append(student.person_name[:15])
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
    participate = 0
    message = 0
    if phrase == first_phrase:
        participate = 1
    elif phrase == second_phrase :
        participate = 1
        message = 1
    if participate == 0 and message == 0:
        date = ["01/01/9999"]
    return message,participate,date

def update_interaction(phrase):
    #Para alunos que ja interagiram, apenas se atualiza esse novo tipo de interacao
    participate = 0
    message = 0
    if phrase == first_phrase:
        participate = 1
    elif phrase == second_phrase:
        participate = 1
        message = 1
    return message,participate

def amount_interactions_pie_chart(students):
    # Dado uma lista de Alunos retorna quantos participaram e quantos nã
    # Tambem quantos só visualizaram posts e quantos mandaram perguntas tb
    participate = 0
    non_participate = 0
    just_readers = 0
    read_writers = 0
    for x in students:
        if x.num_messages > 0 and x.num_participations > 0:
            participate += 1
            read_writers +=1
        elif x.num_participations > 0:
            just_readers +=1
            participate +=1
        else:
            non_participate +=1
    return participate,non_participate,just_readers,read_writers

def amount_messages(students):
    # Dado uma lista de Alunos retorna quantos enviaram mensagens
    # E quantos não enviaram
    sent = 0
    not_sent = 0
    for x in students:
        if x.num_messages > 0:
            sent += 1
    not_sent = len(students) - sent
    return sent,not_sent

def which_participate(students):
    # Devolve uma lista de Alunos que tiveram pelo menos UMA participação
    participate = []
    not_participate = []
    for student in students:
        if student.num_participations > 0:
            participate.append(student)
        else:
            not_participate.append(student)
    participate.sort(key=lambda student: student.num_participations, reverse=False)
    return participate,not_participate

def make_matriz(students):
    # Recebe uma lista de Alunos e devolve uma matriz com as infs relevantes desses alunos
    matriz=[]
    styleSheet = getSampleStyleSheet()
    P1 = Paragraph('''
        <para align=center spaceb=3><b>Nome do aluno</b></para>''',styleSheet["BodyText"])
    P2 =Paragraph('''
        <para align=center spaceb=3><b>Quantia de mensagens</b></para>''',styleSheet["BodyText"])
    P3 = Paragraph('''
        <para align=center spaceb=3><b>Quantia de participações</b></para>''',styleSheet["BodyText"])
    P4 = Paragraph('''
        <para align=center spaceb=3><b>Primeiro post/Participou</b></para>''',styleSheet["BodyText"])
    matriz.append([P1,P2,P3,P4])
    students.sort(key=lambda x: x.num_participations, reverse=True)
    students.sort(key=lambda x: x.num_messages, reverse=True)
    for student in students:
        if (student.first_post > convert_to_datetime("01/01/9998")):
            firstdate = "Não participou"
        else:
            firstdate = student.first_post
        matriz.append([student.person_name,student.num_messages,student.num_participations,firstdate])
    return matriz

def names_excel(file_):
    # Dado um arquivo excel no formato [w/e][w/e][Nome]....[w/e]
    # Retorna uma lista desses nomes
    # Inicia a lista
    names = []
    for row in xlread(file_):
        if not row[2] in names:
            names.append(row[2])
    return names

def name_in_student(students,name):
    # Recebe uma lista de hero e um nome, retorna se essa nome esta na lista
    for student in students:
        if student.person_name == name:
            return True
    return False

def append_ghost_students(students_name_list,students_list):
    for name in students_name_list:
        if not name_in_student(students_list,name):
            students_list.append(Aluno(name,0,0,convert_to_datetime("01/01/9999")))

def manage_existant_student(students_list,excel_name,excel_phrase,first_date,last_date,data_splited,weekly_posts_list):
    for student in students_list:
        if student.person_name == excel_name:
            newMessage,newParticipations = update_interaction(excel_phrase)
            student.num_messages += newMessage
            student.num_participations += newParticipations
            #Se foi passado um intervalo de tempo e aluno criou um post, precisa ser atualizada lista de posts por semana
            if  newMessage:
                weekly_posts_list = update_weekly_posts(weekly_posts_list,data_splited[0],first_date,last_date)
            # Verifica se foi alguma ação pre selecionada
            if excel_phrase == first_phrase or excel_phrase == second_phrase:
                #Se data eh menor que a de antes, atualiza a atual
                if convert_to_datetime(data_splited[0]) < student.first_post:
                    student.first_post = convert_to_datetime(data_splited[0])
    return students_list,weekly_posts_list

def update_weekly_posts(weekly_posts_list,date_str,start,end):
    # Recebe a data do post e calcula em qual semana foi postado
    # para preencher na semana correspondente na lista
    date = convert_to_datetime(date_str)
    date = date.isocalendar()[1]
    date = date - start
    if date>= 0 and date <= abs(end-start):
        weekly_posts_list[date] += 1
    return weekly_posts_list

def load_date_range(file_):
    last_date = '01/01/0001'
    first_date = '01/01/9999'
    for row in xlread(file_):
        if row[1] != "Nome completo":
            data_splited=(row[0].split(' '))
            if convert_to_datetime(last_date) < convert_to_datetime(data_splited[0]):
                last_date = data_splited[0]
            if convert_to_datetime(first_date) > convert_to_datetime(data_splited[0]):
                first_date = data_splited[0]
    return first_date,last_date

def create_weekly_posts_list(first_date, last_date):
    # Calcula intervalo de semanas e cria
    # preenche uma lista desses n elementos com zero (0)
    weekly_posts_list = []
    first_date = first_date.isocalendar()[1]
    last_date = last_date.isocalendar()[1]
    amount_weeks = abs(last_date - first_date)
    # Acrescenta 1 no amountweek para contar a PROPRIA semana
    for x in range(amount_weeks+1):
        weekly_posts_list.append(0)
    return weekly_posts_list,first_date,last_date

def load_log(file_,students_names_file,first_date,last_date):
    # Recebe uma lista com nomes dos alunos para filtrar o log gerado pelo Moodle e pode receber um intervalo definido de datas para a consulta das infos
    # Devolve uma lista com os estudantes e suas infos das participações no forum de duvidas e uma lista com o numero de postagens por semana
    students_list = []
    weekly_posts_list = []
    students_name_list = names_excel(students_names_file)
    first_date = convert_to_datetime(first_date)
    last_date = convert_to_datetime(last_date)

    if not file_:
        return students_list,weekly_posts_list
    else:
        # Cria as semanas
        weekly_posts_list, inicial_week,final_week =  create_weekly_posts_list(first_date,last_date)
        for linha in xlread(file_):
            if linha[1] != "Nome completo":
                data_splited=(linha[0].split(' '))
                # Verifica se o nome está na lista de estudante e se a data está entre o inicio e o final
                if linha[1] in students_name_list and last_date >= (convert_to_datetime(data_splited[0])) and first_date <= (convert_to_datetime(data_splited[0])):
                #Testa se pessoa da vez eh um estudante. Se for, analiza se ja foi visto antes ou primeira aparição e se precisa ser tratado
                    if not name_in_student(students_list,linha[1]):
                        newMessages,newParticipations,data_splited = analyze_interaction(linha[5],data_splited)
                        if  newMessages:
                            weekly_posts_list = update_weekly_posts(weekly_posts_list,data_splited[0],inicial_week,final_week)
                        students_list.append(Aluno(linha[1],newMessages,newParticipations,convert_to_datetime(data_splited[0])))
                    else:
                        students_list,weekly_posts_list = manage_existant_student(students_list,linha[1],linha[5],inicial_week,final_week,data_splited,weekly_posts_list)

        append_ghost_students(students_name_list,students_list)
        print("Done")
        return students_list,weekly_posts_list

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

def make_pdf(matriz):
    doc = SimpleDocTemplate("alunos_moodle.pdf", pagesize=letter)
    # container for the 'Flowable' objects
    elements = []

    t=Table(matriz,style= [('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
     ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
     ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
     ('BACKGROUND', (0, 0), (-1, 0), colors.gray)])
    t._argW[3]=1.5*inch

    elements.append(t)
    # write the document to disk
    doc.build(elements)
    print("Foi gerado alunos_moodle.pdf")

class Aluno:
    def __init__(self,person_name,num_messages,num_participations,first_post):
        self.person_name = person_name
        self.num_messages = num_messages
        self.num_participations = num_participations
        self.first_post =  first_post
#--------------------------DEVELOPMENT----------------------------------#
def development(option,names_file_,file_,starting_date,final_date):
    # Coloca a lista de estudantes e as semanas/post nessas variaveis
    students_list,weekly_posts_list = load_log(file_,names_file_,starting_date,final_date)
    # Seleciona quem participa, não participa, só le e quem le e escreve (com números/genérico)
    participate,non_participate,just_readers,read_writers = amount_interactions_pie_chart(students_list)
    # Novamente coloca quem participa e quem não participa (exato, quem fez cada)
    list_participants,list_absents=which_participate(students_list)
    if option == '1': # Se for 1 a opção, plota o gráfico de pizza
        pie_chart(non_participate,participate,just_readers,read_writers)
    elif option == '2': # Se for 2 plota o gráfico de barras
        plotgraph_bar(list_participants)
    elif option == '3': # Se for 3 gera o pdf
        matriz=make_matriz(students_list)
        make_pdf(matriz)
    elif option == '4': # Se for 4 faz o gráfico de linhas
        create_and_plot_lines(weekly_posts_list)
    elif option == '10' or option == '9': # Se for 9 só vai fazer a pizza e as barras
        pie_chart(non_participate,participate,just_readers,read_writers)
        plotgraph_bar(list_participants)
        if option == '10':  # Se for 10 vai fazer tudo
            matriz=make_matriz(students_list)
            make_pdf(matriz)
        create_and_plot_lines(weekly_posts_list)

# Cria os argumentos que o programa vai receber, e faz as flags, requires e os helps
commands = argparse.ArgumentParser(description="""Script Analyze Logs Moodle INF UFRGS""")
commands.add_argument('students', help = 'File that contains the students names in EXCEL')
commands.add_argument('log',help = 'File that contains the log in EXCEL')
commands.add_argument('option',help ='''# # 1 -  Quantos alunos enviaram mensagem e não enviaram.
# # 2 -  Para cada aluno que participou, quantas vezes participou?
# # 3 -  Estatisticas de cada aluno (saida em pdf).
# # 4 -  Número de perguntas por semana.
# # 9 -  Todos as operações acima sendo mostradas uma após a outra sem gerar arquivo de saida.
# # 10 - Todos as operações acima sendo mostradas uma após a outra gerando arquivo de saida.''')
commands.add_argument('-f','--firstdate',help='First date dd/mm/aaaa',required=False)
commands.add_argument('-l','--lastdate',help='Last date dd/mm/aaaa',required=False)
args = commands.parse_args()

# Consistência na hora de receber os parâmetros
def cmd_consistency(args):
    try:
        for row in xlread(args.students):
            isinstance(row[2],str)
            break # Sim esse break é feio, mas é só para não perder tempo rodando todo esse for
    except OSError:
        print('NAMES File not found, please be sure the file is in the same folder and select the excel NAMES file')
        sys.exit()
    except TypeError:
        print('NAMES Wrong File, please select the excel NAMES file')
        sys.exit()
    try:
        for row in xlread(args.log):
            isinstance(row[1],str)
            break
    except OSError:
        print('LOG File not found, please be sure the file is in the same folder and select the excel LOG file')
        sys.exit()
    except TypeError:
        print('LOG Wrong File, please select the excel LOG file')
        sys.exit()
    try:
        if args.option == '1' or args.option == '2' or args.option == '3' or args.option == '4' or args.option == '9' or args.option == '10':
            x=1
        else:
            x=1/0
    except:
        print ("Not a valid option, type -h for help")
        sys.exit()
    try:
        first=convert_to_datetime(args.firstdate)
        last=convert_to_datetime(args.lastdate)
    except TypeError:
        print("Input date is none. Everything in the log will be processed")
        print("Loading...")
        # Caso ele não tenha colocado data, pega a data mais recente do log e a mais distante
        # e retorna
        first,last=load_date_range(args.log)
    except ValueError:
        print("Some date is in wrong format, please format is DD/MM/AAAA")
        sys.exit()
    return first,last



first_day,last_day = cmd_consistency(args)

development(args.option,args.students,args.log,first_day,last_day)
