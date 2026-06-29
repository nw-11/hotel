import os

from persistencia.arquivo_utils import ARQ_IDS, SEP


class IDManager:
    @staticmethod
    def inicializar():
        if not os.path.exists(ARQ_IDS):
            with open(ARQ_IDS, "w", encoding="utf-8") as f:
                f.write("1;1;1;1")

    @staticmethod
    def _ler_ids():
        IDManager.inicializar()
        with open(ARQ_IDS, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()

        partes = conteudo.split(SEP) if conteudo else ["1", "1", "1", "1"]

        while len(partes) < 4:
            partes.append("1")

        return [int(x) for x in partes[:4]]

    @staticmethod
    def _salvar_ids(ids):
        with open(ARQ_IDS, "w", encoding="utf-8") as f:
            f.write(SEP.join(str(i) for i in ids))

    @staticmethod
    def proximo_id_hospede():
        ids = IDManager._ler_ids()
        novo = ids[0]
        ids[0] += 1
        IDManager._salvar_ids(ids)
        return novo

    @staticmethod
    def proximo_id_quarto():
        ids = IDManager._ler_ids()
        novo = ids[1]
        ids[1] += 1
        IDManager._salvar_ids(ids)
        return novo

    @staticmethod
    def proximo_id_reserva():
        ids = IDManager._ler_ids()
        novo = ids[2]
        ids[2] += 1
        IDManager._salvar_ids(ids)
        return novo

    @staticmethod
    def proximo_id_produto():
        ids = IDManager._ler_ids()
        novo = ids[3]
        ids[3] += 1
        IDManager._salvar_ids(ids)
        return novo
