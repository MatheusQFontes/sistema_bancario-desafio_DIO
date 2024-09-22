#Variáveis
LIMITE_DE_SAQUES_DIÁRIO = 3
contas = []
usuarios = []
conta = None  # Começa sem uma conta ativa
agencia = "0001"

# Funções
# Menu de opções do usuário
def menu(conta):
    while True:
        if conta is None:
            print("Nenhuma conta válida encontrada. Crie uma nova conta antes de realizar operações.")
        try:
            opção = str(input(f'''O que você deseja hoje?
                        (D) Realizar Depósito
                        (S) Realizar Saque
                        (E) Verificar Extrato
                        (NU) Criar um novo usuário
                        (NC) Criar uma nova conta
                        (Q) Sair
                        ''' if conta else "(NC) Criar nova conta\n(NU) Criar novo usuário\n(Q) Sair\n")).strip().upper()
        except ValueError:
            print('Opcão inválida! Por favor, tente novamente.')
            continue

        if conta and opção == 'D':
            depositar(conta)
        elif conta and opção == 'S':
            sacar(conta)
        elif conta and opção == 'E':
            visualizar_extrato(conta)
        elif opção == 'NU':
            criar_usuario(usuarios)
        elif opção == 'NC':
            numero_conta = len(contas) + 1
            nova_conta = criar_conta(agencia, numero_conta, usuarios)
            if nova_conta:
                contas.append(nova_conta)
                conta = nova_conta  # Atualiza a conta ativa
                print(f"Conta {nova_conta['numero_conta']} criada com sucesso!")
        elif opção == 'Q':
            print("Obrigado por usar o sistema bancário!")
            break
        else:
            print('Opção inválida! Por favor, tente novamente!')


def depositar(conta):
    while True:
        try:
            depósito = float(input('Digite o valor do depósito: R$'))
            if depósito > 0:
                conta["saldo"] += depósito 
                conta["extrato"].append(f'Depósito: +R${depósito:.2f}')
                print(f'Depósito realizado com sucesso!\nSaldo em conta: R${conta["saldo"]:.2f}')
                break
            else:
                print('Valor inválido! Por favor, digite um valor positivo!')
        except ValueError:
            print('Valor inválido! Por favor, digite um número válido.')


def sacar(conta):
    while True:
        try:
            saque = float(input('Digite o valor do saque: R$'))
            if saque > 0 and saque <= 500 and saque <= conta["saldo"] and conta["saques_diarios"] < LIMITE_DE_SAQUES_DIÁRIO:
                conta["saldo"] -= saque
                conta["extrato"].append(f'Saque: -R${saque:.2f}')
                conta["saques_diarios"] += 1
                print(f'Saque realizado com sucesso!\nSaldo em conta: R${conta["saldo"]:.2f}')
                break
            elif saque > 500:
                print('O limite de saque é de R$500.00.')
            elif conta["saques_diarios"] >= LIMITE_DE_SAQUES_DIÁRIO:
                print('Você atingiu o limite de saques diários!')
                break
            elif saque > conta["saldo"]:
                print(f'Saldo insuficiente.\nSaldo em conta: R${conta["saldo"]:.2f}')
                break
            else:
                print('Valor inválido! Digite um valor positivo.')
        except ValueError:
            print('Valor inválido! Digite um número válido.')


def visualizar_extrato(conta):
    print('\n===============Extrato da conta===============')
    if not conta["extrato"]:
        print('Nenhuma operação foi efetuada.')
    else:
        for operação in conta["extrato"]:
            print('~', operação)
    print('==============================================')
    print(f'Saldo da conta: R${conta["saldo"]:.2f}')


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": [], "saques_diarios": 0}
    
    print("\nUsuário não encontrado!")
    return None


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


if __name__ == "__main__":
    menu(conta)
