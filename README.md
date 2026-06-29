# Ventana — Administrador Hoteleiro

Sistema de administração hoteleira desenvolvido em **Python**, com interface gráfica em **Tkinter**, persistência em arquivos `.txt` e separação entre as camadas de **modelo**, **persistência**, **visão** e **testes**.

O projeto permite gerenciar hóspedes, quartos, produtos/serviços e reservas, seguindo uma arquitetura modular com entidades de domínio independentes da camada de armazenamento.

---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Arquitetura](#arquitetura)
- [Persistência](#persistência)
- [Regras de negócio](#regras-de-negócio)
- [Como executar](#como-executar)
- [Como executar os testes](#como-executar-os-testes)
- [Arquivos de dados](#arquivos-de-dados)
- [Tecnologias utilizadas](#tecnologias-utilizadas)

---

## Sobre o projeto

O **Ventana — Administrador Hoteleiro** é um sistema simples para controle de um hotel. Ele permite cadastrar e administrar:

- hóspedes;
- quartos;
- produtos e serviços;
- reservas;
- itens extras associados às reservas.

O sistema foi refatorado para separar corretamente as responsabilidades:

- o pacote `modelo` representa apenas o domínio da aplicação;
- o pacote `persistencia` gerencia armazenamento, recuperação e regras de persistência;
- o pacote `visao` contém a interface gráfica;
- o pacote `testes` valida as operações principais dos DAOs.

---

## Funcionalidades

### Hóspedes

- Cadastrar hóspede;
- Editar dados de hóspede;
- Remover hóspede;
- Visualizar hóspede por ID;
- Listar hóspedes;
- Buscar hóspede por nome.

### Quartos

- Cadastrar quarto;
- Editar quarto;
- Remover quarto;
- Visualizar quarto por ID;
- Listar todos os quartos;
- Listar apenas quartos disponíveis.

### Produtos e serviços

- Cadastrar produto ou serviço;
- Editar produto;
- Remover produto;
- Visualizar produto por ID;
- Listar produtos.

### Reservas

- Criar nova reserva;
- Editar datas da reserva;
- Cancelar reserva;
- Visualizar reserva por ID;
- Listar reservas;
- Adicionar produto extra à reserva.

---

## Estrutura de pastas

A estrutura principal do projeto é:

```text
projeto/
│
├── main.py
│
├── modelo/
│   ├── entidade.py
│   ├── hospede.py
│   ├── quarto.py
│   ├── produto.py
│   ├── reserva.py
│   └── item_reserva.py
│
├── persistencia/
│   ├── arquivo_utils.py
│   ├── dao_factory.py
│   ├── entidade_dao.py
│   ├── id_manager.py
│   └── persistence_exception.py
│
├── visao/
│   ├── menu_principal_interface.py
│   ├── menu_hospede_interface.py
│   ├── menu_quarto_interface.py
│   ├── menu_produto_interface.py
│   ├── menu_reserva_interface.py
│   ├── tabela_utils.py
│   └── Ventana.png
│
├── testes/
│   ├── teste_hospede_dao.py
│   ├── teste_quarto_dao.py
│   ├── teste_produto_dao.py
│   └── teste_reserva_dao.py
│
├── hospedes.txt
├── quartos.txt
├── produtos.txt
├── reservas.txt
├── itens_reserva.txt
└── ids.txt
```

---

## Arquitetura

O projeto segue uma separação em camadas.

### Camada de modelo

A camada `modelo` contém as entidades principais do sistema:

- `Entidade`;
- `Hospede`;
- `Quarto`;
- `Produto`;
- `Reserva`;
- `ItemReserva`.

As classes do modelo não possuem métodos de persistência. Elas representam apenas os dados e regras básicas do domínio.

A classe `Entidade` define a identidade dos objetos por meio do atributo `id`, permitindo comparação, igualdade e uso em conjuntos (`set`).

---

### Camada de persistência

A camada `persistencia` possui uma única classe DAO genérica:

```python
EntidadeDAO
```

Essa classe é responsável pelas operações básicas:

- `salvar`;
- `atualizar`;
- `apagar`;
- `carregar`;
- `carregarTodos`;
- `persistir`;
- `recuperar`.

Em vez de criar um DAO específico para cada entidade, o projeto usa uma única classe `EntidadeDAO` configurada pelo `DAOFactory`.

O `DAOFactory` cria uma instância de `EntidadeDAO` para cada tipo de entidade:

- `hospedeDAO`;
- `quartoDAO`;
- `produtoDAO`;
- `reservaDAO`.

Assim, o sistema mantém apenas uma instância de DAO para cada entidade.

---

### Camada de visão

A camada `visao` contém a interface gráfica feita com **Tkinter**.

A classe principal da interface é:

```python
Janela
```

Ela está localizada em:

```text
visao/menu_principal_interface.py
```

A interface utiliza menus e frames para alternar entre as funcionalidades de hóspedes, quartos, produtos e reservas.

---

### Camada de testes

A camada `testes` contém testes automatizados usando `unittest`.

Os testes verificam as principais operações de persistência:

- salvar com ID novo;
- impedir salvar com ID existente;
- atualizar entidade existente;
- impedir atualizar entidade inexistente;
- apagar entidade existente;
- impedir apagar entidade inexistente;
- carregar entidade existente;
- impedir carregar entidade inexistente.

Também são testadas regras específicas, como impedir a remoção de hóspede ou quarto com reserva ativa.

---

## Persistência

A persistência é feita em arquivos `.txt`, usando `;` como separador.

Os arquivos utilizados são:

```text
hospedes.txt
quartos.txt
produtos.txt
reservas.txt
itens_reserva.txt
ids.txt
```

O módulo `arquivo_utils.py` centraliza os caminhos dos arquivos e as funções auxiliares para leitura e escrita.

O arquivo `ids.txt` armazena os próximos IDs disponíveis para cada entidade.

---

## Regras de negócio

O sistema implementa algumas regras importantes.

### Identidade por ID

Cada entidade possui um atributo `id`.

Duas entidades são consideradas iguais quando possuem o mesmo `id`.

---

### Hóspede com reserva ativa

Um hóspede não pode ser removido se possuir uma reserva ativa.

Caso isso seja tentado, o sistema lança uma `PersistenceException`.

---

### Quarto com reserva ativa

Um quarto não pode ser removido se estiver associado a uma reserva ativa.

Caso isso seja tentado, o sistema lança uma `PersistenceException`.

---

### Disponibilidade de quarto

Quando uma reserva é criada, o quarto associado fica indisponível.

Quando uma reserva é cancelada, o quarto volta a ficar disponível.

---

### Datas da reserva

A data de saída deve ser posterior à data de entrada.

As datas devem seguir o formato:

```text
DD/MM/AAAA
```

---

### Produtos extras

Uma reserva pode possuir produtos extras associados a ela.

Cada item da reserva armazena:

- produto;
- quantidade;
- subtotal.

---

## Como executar

Na pasta raiz do projeto, execute:

```bash
python main.py
```

ou, dependendo da instalação do Python:

```bash
python3 main.py
```

O arquivo `main.py` recomendado é:

```python
from visao.menu_principal_interface import Janela
from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager


def main():
    IDManager.inicializar()
    DAOFactory.recuperarTodos()

    try:
        app = Janela()
        app.janela.mainloop()
    finally:
        DAOFactory.persistirTodos()


if __name__ == "__main__":
    main()
```

O bloco `finally` garante que os dados sejam persistidos quando a janela for fechada.

---

## Como executar os testes

Para executar todos os testes, rode o comando na raiz do projeto:

```bash
python -m unittest discover -s testes -v
```

ou:

```bash
python3 -m unittest discover -s testes -v
```

Para executar um teste específico:

```bash
python -m unittest testes.teste_hospede_dao -v
```

Exemplos:

```bash
python -m unittest testes.teste_quarto_dao -v
python -m unittest testes.teste_produto_dao -v
python -m unittest testes.teste_reserva_dao -v
```

---

## Arquivos de dados

Os arquivos `.txt` são criados automaticamente caso não existam.

Exemplo de conteúdo de `hospedes.txt`:

```text
1;Pedro;12345678900;pedro@email.com;32999999999
```

Exemplo de conteúdo de `quartos.txt`:

```text
1;101;Luxo;250.0;1
```

Exemplo de conteúdo de `produtos.txt`:

```text
1;Água;5.0;Bebidas
```

Exemplo de conteúdo de `reservas.txt`:

```text
1;1;1;10/06/2026;12/06/2026
```

Exemplo de conteúdo de `itens_reserva.txt`:

```text
1;1;2
```

---

## Tecnologias utilizadas

- Python 3;
- Tkinter;
- unittest;
- arquivos `.txt` para persistência.

---

## Observações

Este projeto foi desenvolvido com foco em:

- modularidade;
- separação de responsabilidades;
- uso de DAO genérico;
- persistência simples em arquivos;
- testes automatizados;
- interface gráfica com Tkinter.

A arquitetura atual evita que as entidades do pacote `modelo` conheçam detalhes de armazenamento, mantendo a responsabilidade de persistência centralizada no pacote `persistencia`.
