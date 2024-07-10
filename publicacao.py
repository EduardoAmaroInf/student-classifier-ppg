# arquivo publicacao.py

class Publicacao:
    def calcular_nota(self):
        """
        Calcula a nota da publicação com base no Qualis e se é o primeiro autor.
        """
        nota = 0
        qualis = self.qualis.upper()

        # Definir a nota base com base no Qualis
        if qualis == 'A1':
            nota = 5
        elif qualis == 'A2':
            nota = 4.38
        elif qualis == 'A3':
            nota = 3.75
        elif qualis == 'A4':
            nota = 3.13
        elif qualis == 'B1':
            nota = 2.5
        elif qualis == 'B2':
            nota = 1
        elif qualis == 'B3':
            nota = 0.5
        elif qualis == 'B4':
            nota = 0.25
        else:
            nota = 0.20  # sem qualis

        # Ajustar a nota se o aluno não for o primeiro autor
        if self.primeiro_autor.lower() != 'sim':
            nota = round(nota / 3, 2)  # Dividir a nota por 3 se não for o primeiro autor

        return nota

    def __init__(self, dados):
        self.titulo = dados.get('Título da publicação', '')
        self.local = dados.get('Local de publicação', '')
        self.tipo = dados.get('Tipo da publicação', '')
        self.qualis = dados.get('Qualis do local de publicação', '')
        self.comprovacao = dados.get('Comprovação de publicação ou aceite de publicação (PDF)', '')
        self.primeiro_autor = dados.get('Primeiro autor', '')
        self.nota = self.calcular_nota()