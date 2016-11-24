# Script para analisar informações sobre interação de alunos das cadeiras de Introdução à Programação 
# no fórum de Dúvidas da respectiva cadeira no Moodle .

# O script deve ser chamado desde a linha de comando passando 3 ou 5 pârametros adicionais, além do nome do arquivo. 
# Os 2 pârametros adicionais servem para delimitar uma data na análise dos logs passados, caso não sejam passados esses
# 2 pârametros se usará o log inteiro como referência.

# O protótipo da chamada do script é:
#  <Nome_Do_Arquivo> <Num_Operação> <Nome_Arquivo_Alunos> <Nome_Contendo_Logs>
#  ou no caso de querer delimitar data:
#  <Nome_Do_Arquivo> <Num_Operação> <Nome_Arquivo_Alunos> <Nome_Contendo_Logs> <Data_Inicial> <Data_Final>

# As datas devem ser passadas como um argumento só e na forma dd/mm/ano.
# As operação deve ser passadas como um número e pode ser escolhida dentre as seguintes:

#  1 -  Quantos alunos enviaram mensagem e não enviaram .
#  2 -  Para cada aluno que participou, quantas vezes participou?
#  3 -  Estatisticas de cada aluno (saida em pdf).
#  4 -  Número de perguntas por semana.
#  9 -  Todos as operações acima sendo mostradas uma após a outra sem gerar arquivo de saida.
#  10 - Todos as operações acima sendo mostradas uma após a outra gerando arquivo de saida.
