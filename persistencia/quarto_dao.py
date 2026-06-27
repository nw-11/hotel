from modelo.quarto import Quarto
from persistencia.entidade_dao import EntidadeDAO
from persistencia.arquivo_utils import (
    ARQ_QUARTOS,
    ler_linhas,
    escrever_linhas
)
from persistencia.persistence_exception import PersistenceException


class QuartoDAO(EntidadeDAO[Quarto]):
    def persistir(self):
        linhas = []

        for q in self._ordenadas_por_id():
            linhas.append([
                q.id,
                q.numero,
                q.tipo,
                q.diaria,
                int(q.disponivel)
            ])

        escrever_linhas(
            ARQ_QUARTOS,
            linhas
        )

    def recuperar(self):
        self.entidades.clear()

        for linha in ler_linhas(ARQ_QUARTOS):
            quarto = Quarto(
                linha[1],
                linha[2],
                float(linha[3]),
                bool(int(linha[4])),
                id=int(linha[0])
            )

            self.entidades.add(quarto)

    def carregarDisponiveis(self):
        disponiveis = [
            q for q in self._ordenadas_por_id()
            if q.disponivel
        ]

        if len(disponiveis) == 0:
            raise PersistenceException(
                "carregarTodos",
                "nenhum quarto disponível",
                None
            )

        return disponiveis
