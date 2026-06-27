from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from modelo.entidade import Entidade
from persistencia.persistence_exception import PersistenceException

E = TypeVar("E", bound=Entidade)


class EntidadeDAO(Generic[E], ABC):
    def __init__(self):
        self.entidades: set[E] = set()

    def salvar(self, entidade: E):
        if entidade in self.entidades:
            raise PersistenceException(
                "salvar",
                "entidade já existe no conjunto",
                entidade
            )

        self.entidades.add(entidade)

    def atualizar(self, entidade: E):
        existente = None

        for e in self.entidades:
            if e.id == entidade.id:
                existente = e
                break

        if existente is None:
            raise PersistenceException(
                "atualizar",
                "entidade não encontrada no conjunto",
                entidade
            )

        self.entidades.remove(existente)
        self.entidades.add(entidade)

    def apagar(self, id):
        existente = None

        for e in self.entidades:
            if e.id == id:
                existente = e
                break

        if existente is None:
            raise PersistenceException(
                "apagar",
                "id não encontrado no conjunto",
                id
            )

        self.entidades.remove(existente)
        return existente

    def carregar(self, id):
        for e in self.entidades:
            if e.id == id:
                return e

        raise PersistenceException(
            "carregar",
            "id não encontrado no conjunto",
            id
        )

    def carregarTodos(self):
        if len(self.entidades) == 0:
            raise PersistenceException(
                "carregarTodos",
                "conjunto vazio",
                None
            )

        return sorted(
            list(self.entidades),
            key=lambda e: e.id
        )

    def _ordenadas_por_id(self):
        return sorted(
            list(self.entidades),
            key=lambda e: e.id
        )

    @abstractmethod
    def persistir(self):
        pass

    @abstractmethod
    def recuperar(self):
        pass
