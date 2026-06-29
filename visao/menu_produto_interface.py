from tkinter import *
from modelo.produto import Produto
from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager
from persistencia.persistence_exception import PersistenceException
from visao.tabela_utils import TabelaOrdenavel

class FrameProdutos(Frame):
    def __init__(self, container, container2):
        super().__init__(container)

        Button(self, text="Cadastrar\nProduto", width=10, height=2, command=self.Chama_PCad).pack(side="left")
        Button(self, text="Editar\nProduto", width=10, height=2, command=self.Chama_PEdit).pack(side="left")
        Button(self, text="Remover\nProdutos", width=10, height=2, command=self.Chama_PRemove).pack(side="left")
        Button(self, text="Visualizar\npor ID", width=10, height=2, command=self.Chama_PVisual).pack(side="left")
        Button(self, text="Listar\nProdutos", width=10, height=2, command=self.Chama_PList).pack(side="left")

        self.cad = FramePCad(container2)
        self.edit = FramePEdit(container2)
        self.remove = FramePRemove(container2)
        self.visual = FramePVisual(container2)
        self.lista = FramePList(container2)

        self.frames = {self.cad, self.edit, self.remove, self.visual, self.lista}

    def Chama_PCad(self):
        for i in self.frames:
            i.pack_forget()

        self.cad.pack(fill="both", expand=True)

    def Chama_PEdit(self):
        for i in self.frames:
            i.pack_forget()

        self.edit.pack(fill="both", expand=True)

    def Chama_PRemove(self):
        for i in self.frames:
            i.pack_forget()

        self.remove.pack(fill="both", expand=True)

    def Chama_PVisual(self):
        for i in self.frames:
            i.pack_forget()

        self.visual.pack(fill="both", expand=True)
        self.visual.resultado.config(text="")

    def Chama_PList(self):
        for i in self.frames:
            i.pack_forget()

        self.lista.limpar_tela()
        self.lista.pack(fill="both", expand=True)

class FramePCad(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getProdutoDAO()

        linha_nome = Frame(self)
        linha_nome.pack(anchor="w", pady=5)

        Label(linha_nome, text="Nome:", width=12, anchor="e").pack(side="left")
        self.Enome = Entry(linha_nome, width=30)
        self.Enome.pack(side="left")

        linha_preco = Frame(self)
        linha_preco.pack(anchor="w", pady=5)

        Label(linha_preco, text="Preço:", width=12, anchor="e").pack(side="left")
        self.Epreco = Entry(linha_preco, width=15)
        self.Epreco.pack(side="left")

        linha_categoria = Frame(self)
        linha_categoria.pack(anchor="w", pady = 5)

        Label(linha_categoria, text="Categoria:", width=12, anchor="e").pack(side="left")
        self.categoria = StringVar(value=Produto.CATEGORIAS[-1])
        OptionMenu(linha_categoria, self.categoria, *Produto.CATEGORIAS).pack(side="left")

        Button(self, text="Salvar", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        self.nome = self.Enome.get()
        self.preco = self.Epreco.get()
        categoria = self.categoria.get()

        if self.nome == "" or self.preco == "" or categoria == "":
            self.msg.config(text="Erro: Informacoes insuficientes.", fg="red")
        else:
            try:
                self.preco = float(self.preco)
                if self.preco <= 0:
                    raise ValueError

                produto = Produto(self.nome, self.preco, categoria)
                produto.id = IDManager.proximo_id_produto()
                self.dao.salvar(produto)

                self.msg.config(text="Produto cadastrado com sucesso.", fg="black")
                self.after(3000, lambda: self.msg.config(text=""))

                self.Enome.delete(0, END)
                self.Epreco.delete(0, END)
                self.categoria.set(Produto.CATEGORIAS[-1])
            except PersistenceException as e:
                self.msg.config(text=str(e), fg="red")
            except ValueError:
                self.msg.config(text="Preco invalido", fg="red")
            except Exception as e:
                self.msg.config(text=str(e), fg="red")
class FramePEdit(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getProdutoDAO()

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        linha_nome = Frame(self)
        linha_nome.pack(anchor="w", pady=5)

        Label(linha_nome, text="Nome:", width=12, anchor="e").pack(side="left")
        self.Enome = Entry(linha_nome, width=30)
        self.Enome.pack(side="left")

        linha_preco = Frame(self)
        linha_preco.pack(anchor="w", pady=5)

        Label(linha_preco, text="Preço:", width=12, anchor="e").pack(side="left")
        self.Epreco = Entry(linha_preco, width=15)
        self.Epreco.pack(side="left")

        linha_categoria = Frame(self)
        linha_categoria.pack(anchor="w", pady = 5)

        Label(linha_categoria, text="Categoria:", width=12, anchor="e").pack(side="left")
        self.categoria = StringVar(value=Produto.CATEGORIAS[-1])
        OptionMenu(linha_categoria, self.categoria, *Produto.CATEGORIAS).pack(side="left")


        Button(self, text="Salvar Alterações", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        self.id = self.Eid.get()
        self.nome = self.Enome.get()
        self.preco = self.Epreco.get()
        categoria = self.categoria.get()
        if self.nome == "" or self.preco == "" or categoria == "" or self.id == "":
            self.msg.config(text="Erro: Informacoes insuficientes.", fg="red")
        elif not self.id.isdigit():
            self.msg.config(text="ID Invalido", fg="red")
        else:
            try:
                produto = self.dao.carregar(int(self.id))
                produto.nome = self.nome
                self.preco = float(self.preco)
                if self.preco <= 0:
                    raise ValueError
                produto.preco = self.preco
                produto.categoria = categoria

                self.dao.atualizar(produto)
                self.msg.config(text="Produto atualizado com sucesso.", fg="black")
                self.after(3000, lambda: self.msg.config(text=""))
                self.Eid.delete(0, END)
                self.Enome.delete(0, END)
                self.Epreco.delete(0, END)
                self.categoria.set(Produto.CATEGORIAS[-1])
            except PersistenceException as e:
                self.msg.config(text=str(e), fg="red")
            except ValueError:
                self.msg.config(text="Preco invalido", fg="red")
            except Exception as e:
                self.msg.config(text=str(e), fg="red")


class FramePRemove(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getProdutoDAO()

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Remover", command=self.remove).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def remove(self):
        self.id = self.Eid.get()
        if self.id == "":
            self.msg.config(text="Informe um ID.", fg="red")
        elif not self.id.isdigit():
            self.msg.config(text="ID inválido", fg="red")
        else:
            try:
                self.dao.apagar(int(self.id))
                self.msg.config(text="Produto removido com sucesso.", fg="black")
                self.Eid.delete(0, END)
                self.after(3000, lambda: self.msg.config(text=""))
            except PersistenceException as e:
                self.msg.config(text=str(e), fg="red")


class FramePVisual(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getProdutoDAO()


        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Visualizar", command=self.visualizar).pack(pady=10)

        self.resultado = Label(self)
        self.resultado.pack()

    def visualizar(self):
        self.id = self.Eid.get()
        if(not self.id.isdigit()):
            self.resultado.config(text="ID inválido", fg="red")
        else:
            try:
                p = self.dao.carregar(int(self.id))
                self.resultado.config(text=f"Nome : {p.nome}  |  Preço : {p.preco}  |  Categoria : {p.categoria}", fg="black")
            except PersistenceException as e:
                self.resultado.config(text=str(e), fg="red")

class FramePList(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getProdutoDAO()
        Button(self, text="Listar Produtos", command=self.listar).pack(pady=10)

        self.tabela = TabelaOrdenavel(
            self,
            [
                ("id", "ID", 60, lambda produto: produto.id),
                ("nome", "Nome", 220, lambda produto: produto.nome),
                ("preco", "Preco", 100, lambda produto: produto.preco),
                ("categoria", "Categoria", 160, lambda produto: produto.categoria),
            ]
        )
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def listar(self):
        try:
            self.tabela.carregar(self.dao.carregarTodos())
        except PersistenceException as e:
            self.tabela.mostrar_erro(str(e))

    def limpar_tela(self):
        self.tabela.limpar()
