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
        aluno.media_historico = medias[chave]
    
    # aluno.baixar_arquivos()

# Agora cada aluno terá o atributo aluno.media_historico com sua respectiva média histórica
for aluno in alunos:
    print(f"Nome: {aluno.nome_completo}, CPF: {aluno.cpf}, Média Histórico: {aluno.media_historico}")
    
    for idx, publicacao in enumerate(aluno.publicacoes, 1):
        print(f"Publicação {idx}:")
        print(f"  Título: {publicacao.titulo}")
        print(f"  Local: {publicacao.local}")
        print(f"  Tipo: {publicacao.tipo}")
        print(f"  Qualis: {publicacao.qualis}")
        print(f"  Comprovação: {publicacao.comprovacao}")
