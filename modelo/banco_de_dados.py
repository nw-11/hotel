#biblioteca para mexer nos arquivos do computador
import os

# Pasta onde ficam os arquivos de dados (mesma pasta deste módulo)
_DIR = os.path.dirname(__file__)

_ARQ_HOSPEDES  = os.path.join(_DIR, "hospedes.txt")
_ARQ_QUARTOS   = os.path.join(_DIR, "quartos.txt")
_ARQ_RESERVAS  = os.path.join(_DIR, "reservas.txt")
_ARQ_ITENS     = os.path.join(_DIR, "itens_reserva.txt")
_ARQ_IDS       = os.path.join(_DIR, "ids.txt")

SEP = ";"   # separador de campos


class Bancodedados:
    """
    Camada de persistência usando arquivos de texto (.txt) separados por ';'.

    Formato de cada arquivo:
        hospedes.txt      →  id;nome;cpf;email;telefone
        quartos.txt       →  id;numero;tipo;diaria;disponivel
        reservas.txt      →  id;hospede_id;quarto_id;checkin;checkout
        itens_reserva.txt →  id;reserva_id;nome;preco
        ids.txt           →  proximo_id_hospede;proximo_id_quarto;proximo_id_reserva;proximo_id_item

    Todos os métodos são @classmethod — nunca instancie essa classe.
    """

    # ------------------------------------------------------------------
    # INICIALIZAÇÃO
    # ------------------------------------------------------------------

    @classmethod
    def inicializar(cls):
        """Cria os arquivos de dados se ainda não existirem."""
        for caminho in (_ARQ_HOSPEDES, _ARQ_QUARTOS, _ARQ_RESERVAS, _ARQ_ITENS):
            if not os.path.exists(caminho):
                open(caminho, "w", encoding="utf-8").close()

        if not os.path.exists(_ARQ_IDS):
            with open(_ARQ_IDS, "w", encoding="utf-8") as f:
                f.write("1;1;1;1")   # próximos IDs: hospede;quarto;reserva;item

    # ------------------------------------------------------------------
    # CONTROLE DE IDs
    # ------------------------------------------------------------------

    @classmethod
    def _ler_ids(cls):
        with open(_ARQ_IDS, "r", encoding="utf-8") as f:
            return [int(p) for p in f.read().strip().split(SEP)]

    @classmethod
    def _salvar_ids(cls, ids):
        with open(_ARQ_IDS, "w", encoding="utf-8") as f:
            f.write(SEP.join(str(i) for i in ids))

    @classmethod
    def _proximo_id_hospede(cls):
        ids = cls._ler_ids(); novo = ids[0]; ids[0] += 1; cls._salvar_ids(ids); return novo

    @classmethod
    def _proximo_id_quarto(cls):
        ids = cls._ler_ids(); novo = ids[1]; ids[1] += 1; cls._salvar_ids(ids); return novo

    @classmethod
    def _proximo_id_reserva(cls):
        ids = cls._ler_ids(); novo = ids[2]; ids[2] += 1; cls._salvar_ids(ids); return novo

    @classmethod
    def _proximo_id_item(cls):
        ids = cls._ler_ids(); novo = ids[3]; ids[3] += 1; cls._salvar_ids(ids); return novo

    # ------------------------------------------------------------------
    # LEITURA / ESCRITA GENÉRICA
    # ------------------------------------------------------------------

    @classmethod
    def _ler_linhas(cls, caminho):
        """Retorna lista de listas de campos. Ignora linhas vazias."""
        with open(caminho, "r", encoding="utf-8") as f:
            return [l.strip().split(SEP) for l in f if l.strip()]

    @classmethod
    def _escrever_linhas(cls, caminho, linhas):
        """Recebe lista de listas de campos e escreve no arquivo."""
        with open(caminho, "w", encoding="utf-8") as f:
            for campos in linhas:
                f.write(SEP.join(str(c) for c in campos) + "\n")

    # ------------------------------------------------------------------
    # HÓSPEDE
    # formato: id;nome;cpf;email;telefone
    # ------------------------------------------------------------------

    @classmethod
    def salva_hospede(cls, hospede):
        if hospede.id is None:
            hospede.id = cls._proximo_id_hospede()
            with open(_ARQ_HOSPEDES, "a", encoding="utf-8") as f:
                f.write(SEP.join([
                    str(hospede.id), hospede.nome, hospede.cpf,
                    hospede.email, hospede.telefone
                ]) + "\n")
        else:
            cls.atualiza_hospede(hospede)

    @classmethod
    def atualiza_hospede(cls, hospede):
        linhas = cls._ler_linhas(_ARQ_HOSPEDES)
        for i, campos in enumerate(linhas):
            if int(campos[0]) == hospede.id:
                linhas[i] = [
                    str(hospede.id), hospede.nome, hospede.cpf,
                    hospede.email, hospede.telefone
                ]
                break
        cls._escrever_linhas(_ARQ_HOSPEDES, linhas)

    @classmethod
    def apaga_hospede(cls, hospede):
        linhas = cls._ler_linhas(_ARQ_HOSPEDES)
        novas  = [l for l in linhas if int(l[0]) != hospede.id]
        if len(novas) == len(linhas):
            return False
        cls._escrever_linhas(_ARQ_HOSPEDES, novas)
        return True

    @classmethod
    def busca_hospede(cls, id):
        from .hospede import Hospede
        for campos in cls._ler_linhas(_ARQ_HOSPEDES):
            if int(campos[0]) == id:
                h = Hospede(campos[1], campos[2], campos[3], campos[4], id=int(campos[0]))
                h.persistido = True
                return h
        return None

    @classmethod
    def lista_hospedes(cls):
        from .hospede import Hospede
        hospedes = []
        for campos in cls._ler_linhas(_ARQ_HOSPEDES):
            h = Hospede(campos[1], campos[2], campos[3], campos[4], id=int(campos[0]))
            h.persistido = True
            hospedes.append(h)
        return hospedes

    @classmethod
    def busca_hospedes_por_nome(cls, nome):
        from .hospede import Hospede
        hospedes = []
        for campos in cls._ler_linhas(_ARQ_HOSPEDES):
            if nome.lower() in campos[1].lower():
                h = Hospede(campos[1], campos[2], campos[3], campos[4], id=int(campos[0]))
                h.persistido = True
                hospedes.append(h)
        return hospedes

    # ------------------------------------------------------------------
    # QUARTO
    # formato: id;numero;tipo;diaria;disponivel
    # ------------------------------------------------------------------

    @classmethod
    def salva_quarto(cls, quarto):
        if quarto.id is None:
            quarto.id = cls._proximo_id_quarto()
            with open(_ARQ_QUARTOS, "a", encoding="utf-8") as f:
                f.write(SEP.join([
                    str(quarto.id), quarto.numero, quarto.tipo,
                    str(quarto.diaria), str(int(quarto.disponivel))
                ]) + "\n")
        else:
            cls.atualiza_quarto(quarto)

    @classmethod
    def atualiza_quarto(cls, quarto):
        linhas = cls._ler_linhas(_ARQ_QUARTOS)
        for i, campos in enumerate(linhas):
            if int(campos[0]) == quarto.id:
                linhas[i] = [
                    str(quarto.id), quarto.numero, quarto.tipo,
                    str(quarto.diaria), str(int(quarto.disponivel))
                ]
                break
        cls._escrever_linhas(_ARQ_QUARTOS, linhas)

    @classmethod
    def apaga_quarto(cls, quarto):
        linhas = cls._ler_linhas(_ARQ_QUARTOS)
        novas  = [l for l in linhas if int(l[0]) != quarto.id]
        if len(novas) == len(linhas):
            return False
        cls._escrever_linhas(_ARQ_QUARTOS, novas)
        return True

    @classmethod
    def busca_quarto(cls, id):
        from .quarto import Quarto
        for campos in cls._ler_linhas(_ARQ_QUARTOS):
            if int(campos[0]) == id:
                q = Quarto(campos[1], campos[2], float(campos[3]), bool(int(campos[4])), id=int(campos[0]))
                q.persistido = True
                return q
        return None

    @classmethod
    def lista_quartos(cls):
        from .quarto import Quarto
        quartos = []
        for campos in cls._ler_linhas(_ARQ_QUARTOS):
            q = Quarto(campos[1], campos[2], float(campos[3]), bool(int(campos[4])), id=int(campos[0]))
            q.persistido = True
            quartos.append(q)
        return quartos

    @classmethod
    def lista_quartos_disponiveis(cls):
        return [q for q in cls.lista_quartos() if q.disponivel]

    # ------------------------------------------------------------------
    # RESERVA
    # formato: id;hospede_id;quarto_id;checkin;checkout
    # ------------------------------------------------------------------

    @classmethod
    def salva_reserva(cls, reserva):
        if reserva.id is None:
            reserva.id = cls._proximo_id_reserva()
            with open(_ARQ_RESERVAS, "a", encoding="utf-8") as f:
                f.write(SEP.join([
                    str(reserva.id), str(reserva.hospede.id),
                    str(reserva.quarto.id), reserva.checkin, reserva.checkout
                ]) + "\n")
            # marca quarto como indisponível
            reserva.quarto.disponivel = False
            cls.atualiza_quarto(reserva.quarto)
        else:
            cls.atualiza_reserva(reserva)

    @classmethod
    def atualiza_reserva(cls, reserva):
        linhas = cls._ler_linhas(_ARQ_RESERVAS)
        for i, campos in enumerate(linhas):
            if int(campos[0]) == reserva.id:
                linhas[i] = [
                    str(reserva.id), str(reserva.hospede.id),
                    str(reserva.quarto.id), reserva.checkin, reserva.checkout
                ]
                break
        cls._escrever_linhas(_ARQ_RESERVAS, linhas)

    @classmethod
    def apaga_reserva(cls, reserva):
        linhas = cls._ler_linhas(_ARQ_RESERVAS)
        novas  = [l for l in linhas if int(l[0]) != reserva.id]
        if len(novas) == len(linhas):
            return False
        cls._escrever_linhas(_ARQ_RESERVAS, novas)

        # apaga itens vinculados
        itens = cls._ler_linhas(_ARQ_ITENS)
        cls._escrever_linhas(_ARQ_ITENS, [l for l in itens if int(l[1]) != reserva.id])

        # libera o quarto
        reserva.quarto.disponivel = True
        cls.atualiza_quarto(reserva.quarto)
        return True

    @classmethod
    def busca_reserva(cls, id):
        from .reserva import Reserva
        for campos in cls._ler_linhas(_ARQ_RESERVAS):
            if int(campos[0]) == id:
                hospede = cls.busca_hospede(int(campos[1]))
                quarto  = cls.busca_quarto(int(campos[2]))
                r = Reserva(hospede, quarto, campos[3], campos[4], id=int(campos[0]))
                r.itens = cls._carrega_itens(r.id)
                r.persistido = True
                return r
        return None

    @classmethod
    def lista_reservas(cls):
        from .reserva import Reserva
        reservas = []
        for campos in cls._ler_linhas(_ARQ_RESERVAS):
            hospede = cls.busca_hospede(int(campos[1]))
            quarto  = cls.busca_quarto(int(campos[2]))
            r = Reserva(hospede, quarto, campos[3], campos[4], id=int(campos[0]))
            r.itens = cls._carrega_itens(r.id)
            r.persistido = True
            reservas.append(r)
        return reservas

    # ------------------------------------------------------------------
    # ITEM DE RESERVA
    # formato: id;reserva_id;nome;preco
    # ------------------------------------------------------------------

    @classmethod
    def salva_item(cls, item, reserva_id):
        if item.id is None:
            item.id = cls._proximo_id_item()
            with open(_ARQ_ITENS, "a", encoding="utf-8") as f:
                f.write(SEP.join([
                    str(item.id), str(reserva_id), item.nome, str(item.preco)
                ]) + "\n")
        else:
            cls.atualiza_item(item)

    @classmethod
    def atualiza_item(cls, item):
        linhas = cls._ler_linhas(_ARQ_ITENS)
        for i, campos in enumerate(linhas):
            if int(campos[0]) == item.id:
                linhas[i] = [str(item.id), campos[1], item.nome, str(item.preco)]
                break
        cls._escrever_linhas(_ARQ_ITENS, linhas)

    @classmethod
    def apaga_item(cls, item):
        linhas = cls._ler_linhas(_ARQ_ITENS)
        novas  = [l for l in linhas if int(l[0]) != item.id]
        if len(novas) == len(linhas):
            return False
        cls._escrever_linhas(_ARQ_ITENS, novas)
        return True

    @classmethod
    def _carrega_itens(cls, reserva_id):
        """Retorna lista de ItemReserva vinculados à reserva."""
        from .item_reserva import ItemReserva
        itens = []
        for campos in cls._ler_linhas(_ARQ_ITENS):
            if int(campos[1]) == reserva_id:
                item = ItemReserva(campos[2], float(campos[3]), id=int(campos[0]))
                item.persistido = True
                itens.append(item)
        return itens