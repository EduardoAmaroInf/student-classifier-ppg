# arquivo publicacao.py

class Publicacao:
    def __init__(self, dados):
        self.titulo = dados.get('Título da publicação', '')
        self.local = dados.get('Local de publicação', '')
        self.tipo = dados.get('Tipo da publicação', '')
        self.qualis = dados.get('Qualis do local de publicação', '')
        self.comprovacao = dados.get('Comprovação de publicação ou aceite de publicação (PDF)', '')
