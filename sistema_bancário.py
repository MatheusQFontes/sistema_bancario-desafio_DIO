#Variáveis
LIMITE_DE_SAQUES_DIÁRIO = 3
saques_diarios = 0
valor_em_conta = 0
extrato = []
opção = ''
#Menu de opções do usuário
while True:
    opção = ''
    try:
        opção = str(input(f'''Olá, bem-vindo ao sistema bancário!
                    O que você deseja hoje?
                    (D) Realizar Depósito
                    (S) Realizar Saque
                    (E) Verificar Extrato
                    (Q) Sair
                                            Saldo: R${valor_em_conta:.2f}
                    ''')).strip().upper()
    except ValueError:
        print('Opcão inválida!\nPor favor, tente novamente.')
    #Opcão de depósito
    if opção == 'D':
        while True:
            try:
                depósito = float(input('Digite o valor do depósito: R$'))
                if depósito > 0:
                    valor_em_conta += depósito 
                    extrato.append(f'Depósito: +R${depósito:.2f}')
                    print(f'Depósito realizado com sucesso!\nSaldo em conta: R${valor_em_conta:.2f}')
                    break
                else:
                    print('Valor inválido! Por favor, digite um valor positivo!')
            except ValueError:
                print('Valor inválido! Por favor, digite um número inteiro ou um número com um "." como separador decimal.')
    #Opção de saque
    elif opção == 'S':
        while True:
            try:
                saque = float(input('Digite o valor do saque: R$'))
                if saque > 0 and saque <= 500 and saque <= valor_em_conta and saques_diarios < LIMITE_DE_SAQUES_DIÁRIO:
                    valor_em_conta -= saque
                    extrato.append(f'Saque:    -R${saque:.2f}')
                    saques_diarios += 1
                    print(f'Saque realizado com sucesso!\nSaldo em conta: R${valor_em_conta:.2f}')
                    break
                elif saque > 500:
                    print('Não é possível realizar esse saque, pois o limite de saque dessa conta é de R$500.00!')
                elif saques_diarios >= LIMITE_DE_SAQUES_DIÁRIO:
                    print('Não é possível realizar essa operação, pois você atingiu o limite de saques diários!')
                    break
                elif saque > valor_em_conta:
                    print(f'Não é possível realizar essa operação. Seu saldo é insuficiente.\nSaldo em conta: R${valor_em_conta:.2f}')
                    break
                else:
                    print('Valor inválido! Por favor, digite um valor positivo!')
            except ValueError:
                  print('Valor inválido! Por favor, digite um número inteiro ou um número com um "." como separador decimal.')
    #Opção de extrato
    elif opção == 'E':
        print('\n===============Extrato da conta===============')
        if extrato == []:
            print('Nenhuma operação foi efetuada.')
        for operação in extrato:
            print('~', operação)
        print('==============================================')
        print(f'Saldo da conta: R${valor_em_conta:.2f}')
    #Opção de saída
    elif opção == 'Q':
        print('Obrigado por usar o sistema bancário!\nVolte sempre.')
        break
    #Opção inválida
    else:
        print('Opção inválida! Por favor, tente novamente!')