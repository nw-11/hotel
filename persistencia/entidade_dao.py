from typing import Generic, TypeVar

from modelo.entidade import Entidade
from persistencia.persistence_exception import PersistenceException
from persistencia.arquivo_utils import ler_linhas, escrever_linhas

E = TypeVar("E", bound=Entidade)


class EntidadeDAO(Generic[E]):

    def __init__(
        self,
        nome_entidade,
        arquivo=None,
        para_linha=None,
        de_linha=None,
        persistir_func=None,
        recuperar_func=None,
        apos_salvar=None,
        antes_apagar=None,
        apos_apagar=None
    ):
        self.nome_entidade = nome_entidade
        self.arquivo = arquivo
        self.para_linha = para_linha
        self.de_linha = de_linha
        self.persistir_func = persistir_func
        self.recuperar_func = recuperar_func
        self.apos_salvar = apos_salvar
        self.antes_apagar = antes_apagar
        self.apos_apagar = apos_apagar
        self.entidades: set[E] = set()

    # ------------------------------------------------------------
    # métodos auxiliares
    # ------------------------------------------------------------

    def _buscar_por_id(self, id):
        for entidade in self.entidades:
            if entidade.id == id:
                return entidade

        return None

    def _ordenadas_por_id(self, entidades=None):
        if entidades is None:
            entidades = self.entidades

        return sorted(
            list(entidades),
            key=lambda entidade: entidade.id
        )

    # ------------------------------------------------------------
    # operações principais
    # ------------------------------------------------------------

    def salvar(self, entidade: E):
        if entidade in self.entidades:
            raise PersistenceException(
                "salvar",
                f"{self.nome_entidade} já existe no conjunto",
                entidade
            )

        self.entidades.add(entidade)

        if self.apos_salvar is not None:
            self.apos_salvar(entidade)

    def atualizar(self, entidade: E):
        if entidade not in self.entidades:
            raise PersistenceException(
                "atualizar",
                f"{self.nome_entidade} não encontrada no conjunto",
                entidade
            )

        self.entidades.remove(entidade)
        self.entidades.add(entidade)

    def apagar(self, id):
        entidade = self._buscar_por_id(id)

        if entidade is None:
            raise PersistenceException(
                "apagar",
                f"id de {self.nome_entidade} não encontrado no conjunto",
                id
            )

        if self.antes_apagar is not None:
            self.antes_apagar(entidade)

        self.entidades.remove(entidade)

        if self.apos_apagar is not None:
            self.apos_apagar(entidade)

        return entidade

    def carregar(self, id):
        entidade = self._buscar_por_id(id)

        if entidade is None:
            raise PersistenceException(
                "carregar",
                f"id de {self.nome_entidade} não encontrado no conjunto",
                id
            )

        return entidade

    def carregarTodos(self):
        if len(self.entidades) == 0:
            raise PersistenceException(
                "carregarTodos",
                f"conjunto de {self.nome_entidade} vazio",
                None
            )

        return self._ordenadas_por_id()

    def filtrar(self, criterio):
        filtradas = [
            entidade
            for entidade in self.entidades
            if criterio(entidade)
        ]

        return self._ordenadas_por_id(filtradas)

    # ------------------------------------------------------------
    # persistência em arquivo
    # ------------------------------------------------------------

    def persistir(self):
        if self.persistir_func is not None:
            self.persistir_func(self)
            return

        if self.arquivo is None or self.para_linha is None:
            raise PersistenceException(
                "persistir",
                f"configuração ausente para {self.nome_entidade}",
                self.nome_entidade
            )

        linhas = [
            self.para_linha(entidade)
            for entidade in self._ordenadas_por_id()
        ]

        escrever_linhas(
            self.arquivo,
            linhas
        )

    def recuperar(self):
        if self.recuperar_func is not None:
            self.recuperar_func(self)
            return

        if self.arquivo is None or self.de_linha is None:
            raise PersistenceException(
                "recuperar",
                f"configuração ausente para {self.nome_entidade}",
                self.nome_entidade
            )

        self.entidades.clear()

        for linha in ler_linhas(self.arquivo):
            entidade = self.de_linha(linha)
            self.entidades.add(entidade)