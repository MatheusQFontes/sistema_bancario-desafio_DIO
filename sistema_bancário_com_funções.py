#Variáveis
LIMITE_DE_SAQUES_DIÁRIO = 3
#Funções
def criar_conta():
    return {"saldo" : 0, "extrato" : [], "saques_diarios" : 0}


#Menu de opções do usuário
def menu():
    conta = criar_conta()
    while True:
        try:
            opção = str(input(f'''Olá, bem-vindo ao sistema bancário!
                        O que você deseja hoje?
                        (D) Realizar Depósito
                        (S) Realizar Saque
                        (E) Verificar Extrato
                        (Q) Sair
                                                Saldo: R${conta["saldo"]:.2f}
                        ''')).strip().upper()
        except ValueError:
            print('Opcão inválida!\nPor favor, tente novamente.')
        #Opcão de depósito
        if opção == 'D':
            depositar(conta)
        #Opção de saque
        elif opção == 'S':
            sacar(conta)
        #Opção de extrato
        elif opção == 'E':
            visualizar_extrato(conta)
        #Opção de saída
        elif opção == 'Q':
            print('Obrigado por usar o sistema bancário!\nVolte sempre.')
            break
        #Opção inválida
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
            print('Valor inválido! Por favor, digite um número inteiro ou um número com um "." como separador decimal.')


def sacar(conta):
    while True:
            try:
                saque = float(input('Digite o valor do saque: R$'))
                if saque > 0 and saque <= 500 and saque <= conta["saldo"] and conta["saques_diarios"] < LIMITE_DE_SAQUES_DIÁRIO:
                    conta["saldo"] -= saque
                    conta["extrato"].append(f'Saque:    -R${saque:.2f}')
                    conta["saques_diarios"] += 1
                    print(f'Saque realizado com sucesso!\nSaldo em conta: R${conta["saldo"]:.2f}')
                    break
                elif saque > 500:
                    print('Não é possível realizar esse saque, pois o limite de saque dessa conta é de R$500.00!')
                elif conta["saques_diarios"] >= LIMITE_DE_SAQUES_DIÁRIO:
                    print('Não é possível realizar essa operação, pois você atingiu o limite de saques diários!')
                    break
                elif saque > conta["saldo"]:
                    print(f'Não é possível realizar essa operação. Seu saldo é insuficiente.\nSaldo em conta: R${conta["saldo"]:.2f}')
                    break
                else:
                    print('Valor inválido! Por favor, digite um valor positivo!')
            except ValueError:
                  print('Valor inválido! Por favor, digite um número inteiro ou um número com um "." como separador decimal.')


def visualizar_extrato(conta):
    print('\n===============Extrato da conta===============')
    if conta["extrato"] == []:
        print('Nenhuma operação foi efetuada.')
    for operação in conta["extrato"]:
        print('~', operação)
    print('==============================================')
    print(f'Saldo da conta: R${conta["saldo"]:.2f}')


if __name__ == "__main__":
    menu()