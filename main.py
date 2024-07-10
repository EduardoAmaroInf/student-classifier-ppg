import os
import csv
import urllib.request
from urllib.error import URLError
from aluno import Aluno

# Exemplo de uso:
nome_arquivo_csv = 'inscricoes.csv'
nome_arquivo_medias = 'historico.csv'

# Ler os dados dos alunos
alunos = Aluno.ler_csv(nome_arquivo_csv)

# Ler as médias históricas
medias = Aluno.ler_csv_medias(nome_arquivo_medias)

# Associar a média histórica aos alunos correspondentes
for aluno in alunos:
    chave = (aluno.nome_completo, aluno.cpf)

    if chave in medias:
        aluno.nota_historico = medias[chave]
    
    aluno.calcular_media_historico()
    aluno.calcular_nota_final()
    
    # aluno.baixar_arquivos()

alunos.sort(key=lambda x: x.nota_final, reverse=True)

# Definir cabeçalhos para o arquivo CSV
cabecalhos = ['Classificação', 'Nome Completo', 'CPF', 'Nota Histórico', 'Média Publicações', 'Média Histórico', 'Nota Final']

# Abrir arquivo CSV para escrita
with open('classificacao_alunos_mestrado.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # Escrever cabeçalhos
    writer.writerow(cabecalhos)
    
    # Escrever dados de cada aluno
    for posicao, aluno in enumerate(alunos, 1):
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

print(f'Arquivo classificacao_alunos_mestrado.csv gerado com sucesso!')
