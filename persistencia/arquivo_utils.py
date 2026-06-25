import os


DIR = os.path.dirname(os.path.dirname(__file__))

SEP = ";"

ARQ_HOSPEDES = os.path.join(DIR, "hospedes.txt")
ARQ_QUARTOS = os.path.join(DIR, "quartos.txt")
ARQ_RESERVAS = os.path.join(DIR, "reservas.txt")
ARQ_ITENS = os.path.join(DIR, "itens_reserva.txt")
ARQ_PRODUTOS = os.path.join(DIR, "produtos.txt")


def ler_linhas(caminho):

    if not os.path.exists(caminho):
        open(caminho, "w", encoding="utf-8").close()

    with open(caminho, "r", encoding="utf-8") as f:
        return [
            linha.strip().split(SEP)
            for linha in f
            if linha.strip()
        ]


def escrever_linhas(caminho, linhas):

    with open(caminho, "w", encoding="utf-8") as f:

        for campos in linhas:
            f.write(
                SEP.join(str(c) for c in campos)
                + "\n"
            )