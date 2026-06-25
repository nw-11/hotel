from modelo.quarto import Quarto
from persistencia.persistence_exception import PersistenceException
from persistencia.arquivo_utils import *


class QuartoDAO:

    def salvar(self, quarto):

        linhas = ler_linhas(ARQ_QUARTOS)

        for linha in linhas:

            if int(linha[0]) == quarto.id:

                raise PersistenceException(
                    "salvar",
                    "Quarto já existe",
                    quarto.id
                )

        linhas.append([
            quarto.id,
            quarto.numero,
            quarto.tipo,
            quarto.diaria,
            int(quarto.disponivel)
        ])

        escrever_linhas(
            ARQ_QUARTOS,
            linhas
        )

    def atualizar(self, quarto):

        linhas = ler_linhas(
            ARQ_QUARTOS
        )

        encontrou = False

        for i, linha in enumerate(linhas):

            if int(linha[0]) == quarto.id:

                linhas[i] = [
                    quarto.id,
                    quarto.numero,
                    quarto.tipo,
                    quarto.diaria,
                    int(quarto.disponivel)
                ]

                encontrou = True

        if not encontrou:

            raise PersistenceException(
                "atualizar",
                "Quarto inexistente",
                quarto.id
            )

        escrever_linhas(
            ARQ_QUARTOS,
            linhas
        )

    def apagar(self, id):

        linhas = ler_linhas(
            ARQ_QUARTOS
        )

        novas = [
            l for l in linhas
            if int(l[0]) != id
        ]

        if len(novas) == len(linhas):

            raise PersistenceException(
                "apagar",
                "Quarto inexistente",
                id
            )

        escrever_linhas(
            ARQ_QUARTOS,
            novas
        )

    def carregar(self, id):

        linhas = ler_linhas(
            ARQ_QUARTOS
        )

        for linha in linhas:

            if int(linha[0]) == id:

                return Quarto(
                    linha[1],
                    linha[2],
                    float(linha[3]),
                    bool(int(linha[4])),
                    int(linha[0])
                )

        raise PersistenceException(
            "carregar",
            "Quarto não encontrado",
            id
        )

    def carregarTodos(self):

        linhas = ler_linhas(
            ARQ_QUARTOS
        )

        if len(linhas) == 0:

            raise PersistenceException(
                "carregarTodos",
                "Nenhum quarto salvo",
                None
            )

        quartos = []

        for linha in linhas:

            quartos.append(

                Quarto(
                    linha[1],
                    linha[2],
                    float(linha[3]),
                    bool(int(linha[4])),
                    int(linha[0])
                )
            )

        quartos.sort()

        return quartos

    def carregarDisponiveis(self):

        quartos = self.carregarTodos()

        return [
            q for q in quartos
            if q.disponivel
        ]