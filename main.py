import os
import csv
import urllib.request
from urllib.error import URLError
from aluno import Aluno

# Exemplo de uso:
nome_arquivo_csv = 'inscricoes.csv'
nome_arquivo_medias = 'historico.csv'
nome_arquivo_notas_projetos_doutorado = 'notas_projetos_doutorado.csv'

# Ler os dados dos alunos
alunos = Aluno.ler_csv(nome_arquivo_csv)

# Ler as médias históricas
medias = Aluno.ler_csv_historico(nome_arquivo_medias)

# Ler as notas projeto doutorado
notas_projetos = Aluno.ler_csv_projeto(nome_arquivo_notas_projetos_doutorado)

# Associar a média histórica aos alunos correspondentes
for aluno in alunos:
    chave = (aluno.nome_completo, aluno.cpf)

    if chave in medias:
        aluno.nota_historico = medias[chave]

    if chave in notas_projetos:
        aluno.media_projeto_doutorado = notas_projetos[chave]
        print(notas_projetos)
    
    aluno.calcular_media_historico()
    aluno.calcular_nota_final()
    
    aluno.baixar_arquivos()

# Separar e ordenar os alunos de mestrado e doutorado
alunos_mestrado = [aluno for aluno in alunos if aluno.tipo_inscricao.lower() == 'mestrado']
alunos_mestrado.sort(key=lambda x: x.nota_final, reverse=True)

alunos_doutorado = [aluno for aluno in alunos if aluno.tipo_inscricao.lower() == 'doutorado']
alunos_doutorado.sort(key=lambda x: x.nota_final, reverse=True)

# Definir cabeçalhos para os arquivos CSV
cabecalhos = ['Classificação', 'Nome Completo', 'CPF', 'Nota Histórico', 'Média Publicações', 'Média Histórico', 'Nota Final']
cabecalhos_doutorado = ['Classificação', 'Nome Completo', 'CPF', 'Nota Histórico', 'Média Publicações', 'Média Histórico', 'Média Projeto Doutorado', 'Nota Final']

# Abrir arquivo CSV para escrita - Alunos de Mestrado
with open('classificacao_alunos_mestrado.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Escrever cabeçalhos
    writer.writerow(cabecalhos)
    
    # Escrever dados de cada aluno
    for posicao, aluno in enumerate(alunos_mestrado, 1):
        linha = [
            posicao,
            aluno.nome_completo,
            aluno.cpf,
            aluno.nota_historico,
            aluno.media_publicacoes,
            aluno.media_historico,
            aluno.nota_final
        ]
        writer.writerow(linha)

# Abrir arquivo CSV para escrita - Alunos de Doutorado
with open('classificacao_alunos_doutorado.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Escrever cabeçalhos
    writer.writerow(cabecalhos_doutorado)
    
    # Escrever dados de cada aluno
    for posicao, aluno in enumerate(alunos_doutorado, 1):
        linha = [
            posicao,
            aluno.nome_completo,
            aluno.cpf,
            aluno.nota_historico,
            aluno.media_publicacoes,
            aluno.media_historico,
            aluno.media_projeto_doutorado,
            aluno.nota_final
        ]
        writer.writerow(linha)


print(f'Arquivo classificacao_alunos_mestrado.csv e classificacao_alunos_doutorado.csv gerado com sucesso!')
