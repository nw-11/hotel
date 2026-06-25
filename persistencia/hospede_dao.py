from modelo.hospede import Hospede
from persistencia.persistence_exception import PersistenceException
from persistencia.arquivo_utils import *


class HospedeDAO:

    def salvar(self, hospede):

        linhas = ler_linhas(ARQ_HOSPEDES)

        for linha in linhas:

            if int(linha[0]) == hospede.id:

                raise PersistenceException(
                    "salvar",
                    "Hospede já existe",
                    hospede.id
                )

        linhas.append([
            hospede.id,
            hospede.nome,
            hospede.cpf,
            hospede.email,
            hospede.telefone
        ])

        escrever_linhas(
            ARQ_HOSPEDES,
            linhas
        )

    def atualizar(self, hospede):

        linhas = ler_linhas(
            ARQ_HOSPEDES
        )

        encontrou = False

        for i, linha in enumerate(linhas):

            if int(linha[0]) == hospede.id:

                linhas[i] = [
                    hospede.id,
                    hospede.nome,
                    hospede.cpf,
                    hospede.email,
                    hospede.telefone
                ]

                encontrou = True

        if not encontrou:

            raise PersistenceException(
                "atualizar",
                "Hospede inexistente",
                hospede.id
            )

        escrever_linhas(
            ARQ_HOSPEDES,
            linhas
        )

    def apagar(self, id):

        linhas = ler_linhas(
            ARQ_HOSPEDES
        )

        novas = [
            l for l in linhas
            if int(l[0]) != id
        ]

        if len(linhas) == len(novas):

            raise PersistenceException(
                "apagar",
                "Hospede inexistente",
                id
            )

        escrever_linhas(
            ARQ_HOSPEDES,
            novas
        )

    def carregar(self, id):

        linhas = ler_linhas(
            ARQ_HOSPEDES
        )

        for linha in linhas:

            if int(linha[0]) == id:

                return Hospede(
                    linha[1],
                    linha[2],
                    linha[3],
                    linha[4],
                    int(linha[0])
                )

        raise PersistenceException(
            "carregar",
            "Hospede não encontrado",
            id
        )

    def carregarTodos(self):

        linhas = ler_linhas(
            ARQ_HOSPEDES
        )

        if len(linhas) == 0:

            raise PersistenceException(
                "carregarTodos",
                "Nenhum hospede salvo",
                None
            )

        hospedes = []

        for linha in linhas:

            hospedes.append(

                Hospede(
                    linha[1],
                    linha[2],
                    linha[3],
                    linha[4],
                    int(linha[0])
                )
            )

        hospedes.sort()

        return hospedes