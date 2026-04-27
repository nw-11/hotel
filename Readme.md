# 🏨 Administrador Hoteleiro

Sistema de gerenciamento hoteleiro desenvolvido em Python como projeto universitário. Permite cadastrar hóspedes, quartos e reservas com itens extras, com persistência em arquivos de texto.

---

## 📁 Estrutura do Projeto

```
hotel/
├── programa.py               ← ponto de entrada
├── hospedes.txt              ← dados persistidos
├── quartos.txt
├── reservas.txt
├── itens_reserva.txt
├── ids.txt
├── modelo/
│   ├── __init__.py
│   ├── entidade.py           ← classe base abstrata
│   ├── hospede.py
│   ├── quarto.py
│   ├── reserva.py
│   ├── item_reserva.py
│   └── banco_de_dados.py     ← camada de persistência
└── visao/
    ├── __init__.py
    ├── menu_principal.py
    ├── menu_hospede.py
    ├── menu_quarto.py
    └── menu_reserva.py
```

---

## ▶️ Como rodar

**Pré-requisito:** Python 3.10 ou superior.

Na pasta raiz do projeto (`hotel/`), execute:

```bash
python programa.py
```

Os arquivos `.txt` de dados são criados automaticamente na primeira execução.

---

## 🗂️ Arquitetura

O projeto segue o padrão **MVC simplificado**, separado em duas camadas:

- **`modelo/`** — regras de negócio e persistência. Todas as entidades herdam da classe abstrata `Entidade`, que obriga a implementação de `salvar()`, `atualizar()` e `apagar()`.
- **`visao/`** — interface de terminal com menus interativos para cada entidade.

### Diagrama de classes

```
Entidade (ABC)
├── Hospede
├── Quarto
├── Reserva  ──── contém ──→  ItemReserva (0..*)
                 ──── usa  ──→  Hospede
                 ──── usa  ──→  Quarto

BancoDeDados  ←── usado por todas as entidades
```

---

## 💾 Persistência

Os dados são salvos em arquivos `.txt` separados por `;`, localizados na pasta raiz do projeto.

| Arquivo | Formato |
|---|---|
| `hospedes.txt` | `id;nome;cpf;email;telefone` |
| `quartos.txt` | `id;numero;tipo;diaria;disponivel` |
| `reservas.txt` | `id;hospede_id;quarto_id;checkin;checkout` |
| `itens_reserva.txt` | `id;reserva_id;nome;preco` |
| `ids.txt` | `proximo_hospede;proximo_quarto;proximo_reserva;proximo_item` |

---

## ⚙️ Funcionalidades

### Hóspedes
- Cadastrar, editar e remover hóspedes
- Buscar por ID ou por nome

### Quartos
- Cadastrar, editar e remover quartos
- Listar todos ou apenas os disponíveis
- Tipos: Standard, Luxo, Suite

### Reservas
- Criar reserva vinculando hóspede e quarto disponível
- Informar datas de check-in e check-out
- Adicionar e remover itens extras (frigobar, serviço de quarto, etc.)
- Cancelar reserva — quarto é liberado automaticamente
- Exibir total geral (diária + itens)

---

## 🧱 Tecnologias

- **Python 3.10+**
- Biblioteca padrão apenas (`abc`, `os`)
- Sem dependências externas