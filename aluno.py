import os
import csv
import urllib.request
from urllib.error import URLError
from publicacao import Publicacao
import pandas as pd

class Aluno:
    def __init__(self, dados):
        self.nome_completo = dados['Nome Completo']
        self.data_nascimento = dados['Data de nascimento']
        self.email = dados['Seu e-mail']
        self.nome_mae = dados['Nome da mãe']
        self.cpf = dados['CPF']
        self.carteira_identidade = dados['Carteira de Identidade, no caso de candidatas/os de nacionalidade brasileira, ou passaporte, no caso de candidatas/os de nacionalidade estrangeira']
        self.data_emissao_rg = dados['Data de emissão da carteira de identidade']
        self.orgao_emissor_rg = dados['Órgão emissor da carteira de identidade e estado emissor']
        self.numero_titulo_eleitoral = dados['Número do título eleitoral']
        self.numero_documento_militar = dados['Número de série do documento militar']
        self.endereco_residencial = dados['Endereço residencial']
        self.cidade_residencia = dados['Cidade de residência']
        self.estado_residencia = dados['Estado de residência']
        self.telefone_contato = dados['Telefone para contato']
        self.link_lattes = dados['Link para o currículo Lattes']
        self.reservas_vagas = dados['Reservas de vagas']
        self.numero_siape = dados['Informe o número do seu SIAPE ligado a UFPel para confirmar a candidatura às quotas de vagas para servidores da Universidade']
        self.nome_curso_1 = dados['Nome do Curso']
        self.tipo_curso_1 = dados['Tipo de curso']
        self.instituicao_curso_1 = dados['Instituição']
        self.ano_conclusao_curso_1 = dados['Ano de conclusão']
        self.nome_curso_2 = dados['Nome do curso']
        self.tipo_curso_2 = dados['Tipo de curso']
        self.instituicao_curso_2 = dados['Instituição']
        self.ano_conclusao_curso_2 = dados['Ano de conclusão']
        self.local_trabalho = dados['Local de trabalho']
        self.atuacao = dados['Atuação']
        self.ingles_leitura = dados['Língua Inglesa (Leitura)']
        self.ingles_escrita = dados['Língua Inglesa (Escrita)']
        self.ingles_fala = dados['Língua Inglesa (Fala)']
        self.tipo_inscricao = dados['Tipo de inscrição']
        self.semestre_ingresso = dados['Em que semestre faria o ingresso?']
        self.orientador_preferencial = dados['Orientador preferencial']
        self.segunda_opcao = dados['Segunda opção']
        self.terceira_opcao = dados['Terceira opção']
        self.dedicacao_integral_curso = dados['Você teria dedicação integral para o curso?']
        self.manter_vinculo_empregaticio = dados['Você manteria vínculo empregatício durante a execução do curso?']
        self.interesse_bolsa_programa = dados['Você tem interesse em concorrer a uma bolsa do programa?']
        self.projeto_doutorado_pdf = dados['Enviar arquivo PDF contendo o Projeto de Doutorado e Memorial Acadêmico, conforme especificado no edital.']
        self.curriculo_lattes = dados['Currículo Lattes']
        self.diploma_graduacao = dados['Diploma de graduação OU atestado de conclusão de curso OU atestado de provável formando OU atestado de provável formando indicando que irá concluir o curso até 30 de julho de 2023 no caso de ingresso em 2023/2']
        self.diploma_mestrado = dados['Se aplicável, cópia do diploma de mestrado OU comprovação de cumprimento de todos requisitos para obtenção do diploma OU atestado indicando que irá concluir o seu curso de mestrado até 30 de julho de 2023 no caso de ingresso em 2023/2']
        self.historico_graduacao = dados['Histórico escolar de Graduação']
        self.historico_mestrado = dados['Histórico escolar de Mestrado']
        self.carteira_identidade = dados['Carteira de Identidade']
        self.cpf_copia = dados['CPF, se não disponível na carteira de identidade;']
        self.titulo_eleitor = dados['Título de eleitor']
        self.certificado_quitacao_militar = dados['Certificado de quitação com serviço militar, ou equivalente, se aplicável']
        self.certidao_casamento = dados['Certidão de Casamento, no caso de mudança do nome']
        self.comprovante_pagamento = dados['Comprovante de pagamento ou comprovante de isenção da taxa de inscrição']
        self.documentacao_edital = dados['Documentação relativa a seção 6(l), 6(m), 6(n), 6(o), 6(p) ou 6(q), se aplicável']
        self.outro_documento = dados['Outro documento se necessário de acordo com o Edital']
        self.id_usuario = dados['ID do Usuário']
        self.timestamp = dados['Timestamp']
        self.last_updated = dados['Last Updated']
        self.created_by = dados['Created By']
        self.updated_by = dados['Updated By']
        self.draft = dados['Draft']
        self.ip = dados['IP']
        self.id = dados['ID']
        self.key = dados['Key']
        self.nota_historico = None
        self.media_publicacoes = None
        self.media_historico = None
        self.nota_final = None
        self.publicacoes = []
        self.adicionar_publicacoes(dados)
        self.calcular_media_publicacoes()

    def calcular_media_publicacoes(self):
        """
        Calcula a média de publicações do aluno com base nas publicações e no tipo de inscrição.
        """
        if self.tipo_inscricao.lower() == 'mestrado':
            publicacoes_consideradas = self.publicacoes[:3]  # Considerar as 3 primeiras publicações
            divisor = 3
        elif self.tipo_inscricao.lower() == 'doutorado':
            publicacoes_consideradas = self.publicacoes[:5]  # Considerar as 5 primeiras publicações
            divisor = 5
        else:
            self.nota_total = 0  # Caso o tipo de inscrição não seja especificado corretamente
            return

        soma_pontuacoes = sum(publicacao.nota for publicacao in publicacoes_consideradas)
        self.media_publicacoes = round(soma_pontuacoes / divisor, 2)  # Dividir e arredondar para duas casas decimais

    def calcular_media_historico(self):
        """
        Calcula a média do histórico do aluno com base na nota do histórico.
        """
        if self.nota_historico <= 5.0:
            self.media_historico = 0.0
        else:
            self.media_historico = self.nota_historico - 5.0

        self.media_historico = round(self.media_historico, 2)  # Arredondar para duas casas decimais

    def calcular_nota_final(self):
        """
        Calcula a nota final.
        """
        self.nota_final = self.media_historico + self.media_publicacoes

    def adicionar_publicacoes(self, dados):
    # Método para adicionar publicações dinamicamente
        for chave, valor in dados.items():
            
            if chave.startswith('Título da publicação') and valor:
                # Monta as chaves para os outros campos da publicação
                local_chave = f'Local de publicação'
                tipo_chave = f'Tipo da publicação'
                qualis_chave = f'Qualis do local de publicação'
                comprovacao_chave = f'Comprovação de publicação ou aceite de publicação (PDF)'
                primeiro_autor_chave = f'Primeiro autor'

                # Obtém os valores correspondentes aos outros campos da publicação
                local = dados.get(local_chave, '')
                tipo = dados.get(tipo_chave, '')
                qualis = dados.get(qualis_chave, '')
                comprovacao = dados.get(comprovacao_chave, '')
                primeiro_autor = dados.get(primeiro_autor_chave, '')

                # Cria um dicionário para os dados da publicação
                dados_publicacao = {
                    'Título da publicação': valor,
                    'Local de publicação': local,
                    'Tipo da publicação': tipo,
                    'Qualis do local de publicação': qualis,
                    'Comprovação de publicação ou aceite de publicação (PDF)': comprovacao,
                    'Primeiro autor': primeiro_autor
                }

                # Cria a instância de Publicacao apenas se houver um título de publicação válido
                publicacao = Publicacao(dados_publicacao)
                self.publicacoes.append(publicacao)

    def baixar_arquivos(self):
        """
        Método para baixar os arquivos dos links fornecidos para o aluno.
        Os arquivos são salvos em uma pasta com o nome do aluno.
        """
        nome_aluno = self.nome_completo
        pasta_aluno = f'{nome_aluno}_documentos'
        os.makedirs(pasta_aluno, exist_ok=True)

        # Lista de colunas que contêm links para os arquivos
        colunas_links = [
            self.projeto_doutorado_pdf,
            self.comprovacao_publicacao_1,
            self.comprovacao_publicacao_2,
            self.comprovacao_publicacao_3,
            self.comprovacao_publicacao_4,
            self.comprovacao_publicacao_5,
            self.curriculo_lattes,
            self.diploma_graduacao,
            self.diploma_mestrado,
            self.historico_graduacao,
            self.historico_mestrado,
            self.carteira_identidade,
            self.cpf_copia,
            self.titulo_eleitor,
            self.certificado_quitacao_militar,
            self.certidao_casamento,
            self.comprovante_pagamento,
            self.documentacao_edital,
            self.outro_documento
        ]

        for link in colunas_links:
            if link:
                try:
                    # Extrai o nome do arquivo do link
                    nome_arquivo = link.split('/')[-2] + '.pdf'
                    caminho_arquivo = os.path.join(pasta_aluno, nome_arquivo)

                    # Baixa o arquivo e salva no diretório do aluno
                    urllib.request.urlretrieve(link, caminho_arquivo)
                    print(f'Arquivo {nome_arquivo} baixado para {pasta_aluno}.')
                except URLError as e:
                    print(f'Erro ao baixar {nome_arquivo}: {str(e)}')

    @staticmethod
    def ler_csv(nome_arquivo):
        """
        Método estático para ler o arquivo CSV e retornar os dados como uma lista de objetos Aluno.
        Cada objeto Aluno representa uma linha do CSV.
        """
        dados_alunos = []
        df = pd.read_csv(nome_arquivo, encoding='utf-8')

        for index, row in df.iterrows():
            aluno = Aluno(row)
            dados_alunos.append(aluno)
        return dados_alunos

    @staticmethod
    def ler_csv_medias(nome_arquivo_medias):
        # Método para ler o segundo arquivo CSV de médias
        medias = {}
        with open(nome_arquivo_medias, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                nome_completo = row['Nome Completo']
                cpf = row['CPF']
                media = float(row['Média'])
                chave = (nome_completo, cpf)
                medias[chave] = media
        return medias
