from modelo.hospede import Hospede
from persistencia.entidade_dao import EntidadeDAO
from persistencia.arquivo_utils import (
    ARQ_HOSPEDES,
    ler_linhas,
    escrever_linhas
)


class HospedeDAO(EntidadeDAO[Hospede]):
    def persistir(self):
        linhas = []

        for h in self._ordenadas_por_id():
            linhas.append([
                h.id,
                h.nome,
                h.cpf,
                h.email,
                h.telefone
            ])

        escrever_linhas(
            ARQ_HOSPEDES,
            linhas
        )

    def recuperar(self):
        self.entidades.clear()

        for linha in ler_linhas(ARQ_HOSPEDES):
            hospede = Hospede(
                linha[1],
                linha[2],
                linha[3],
                linha[4],
                id=int(linha[0])
            )

            self.entidades.add(hospede)
