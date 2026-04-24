from ..modelo.banco_de_dados import Bancodedados
from ..modelo.hospede import Hospede

class Menu_Hospede():
    def __init__(self):
        pass
        #não vai ter nada, pois usamos banco de dados

#MÉTODOS HÓSPEDES------------------------------------------------------------------
    def add_Hospede(self, hospede):
        Bancodedados.salva_hospede(hospede)
        
    def create_Hospede(self):
        tnome = input("Nome: ")
        tcpf = input("CPF: ")
        temail = input("Email: ")
        ttelefone = input("Telefone: ")
        tHospede = Hospede(tnome, tcpf, temail, ttelefone)
        return tHospede        

    
    def visualize_Hospede(self, tid):
        tHospede = Bancodedados.busca_hospede(tid)
        if tHospede is not None:
            print(tHospede)
        else:
            print("Hóspede não encontrado.")

    def apaga_Hospede(self, hospede):
        if hospede.apagar():
            print("\nHóspede removido com êxito.")
        else:
            print("\nERRO: Hóspede inexistente.")


#MÉTODO EDIT-----------------------------------------------------------

    def edit_Hospede(self, hospede):
        while True:
            print("O que você quer alterar?")
            print("1 - Nome")
            print("2 - CPF")
            print("3 - E-mail")
            print("4 - Telefone")
            print("5 - Sair")

            tescolhaH = int(input("Digite sua escolha: "))

            if tescolhaH == 1:
                hospede.nome = input("Novo nome: ")

            elif tescolhaH == 2:
                hospede.cpf = input("Novo CPF: ")

            elif tescolhaH == 3:
                hospede.email = input("Novo E-mail: ")

            elif tescolhaH == 4:
                hospede.telefone = input("Novo Telefone: ")

            elif tescolhaH == 5:
                break
            
            else:
                print("Digite um número válido!")

#MÉTODO MENU------------------------------------------------------------------

    def menu(self):
        while True:
            print("\n MENU DE HÓSPEDES")
            print("\n1 - Adicionar Hóspede")
            print("2 - Editar Hóspede")
            print("3 - Remover Hóspede")
            print("4 - Visualizar a partir de ID")
            print("5 - Visualizar todos os hóspedes")
            print("6 - Sair")

            escolhaH = int(input("\nDigite um número: "))

            if escolhaH == 1: #ADICIONAR
                tHospede = self.create_Hospede()
                tHospede.salvar()

            elif escolhaH == 2: #EDITAR
                tHospede = Bancodedados.busca_hospede(int(input("Digite o ID do hóspede: ")))
                if tHospede is not None:
                    self.edit_Hospede(tHospede)
                else:
                    print("Hóspede não encontrado.")

            elif escolhaH == 3: #REMOVER
                tid = int(input("\nDigite o ID do Hóspede: "))
                tHospede = Bancodedados.busca_hospede(tid)
                if tHospede is not None:
                    self.apaga_Hospede(tHospede)
                else:
                    print("\nERRO: Hóspede inexistente.")
                


            elif escolhaH == 4: #VISUALIZAR A PARTIR DE ID
                tid = int(input("\nDigite o ID do Hóspede: "))
                print("\nINFORMAÇÕES DO HÓSPEDE: \n")
                self.visualize_Hospede(tid)


            elif escolhaH == 5: #VISUALIZAR TODOS
                print("\nLISTA DE HÓSPEDES: \n")
                qtd = 0
                for hospede in Bancodedados.lista_hospedes():
                    qtd += 1
                    print(hospede)
                    print()
                if qtd == 0:
                    print("Nenhum hóspede cadastrado\n")

            elif escolhaH == 6: #SAIR
                break

            else:
                print("Escolha um número válido!")