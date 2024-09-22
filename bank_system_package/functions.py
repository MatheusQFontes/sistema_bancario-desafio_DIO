class Conta:
    LIMITE_DE_SAQUES_DIÁRIO = 3 

    def __init__(self):
        self.saldo = 0
        self.extrato = []
        self.saques_diarios = 0

    def menu(self):
        while True:
            try:
                opção = str(input(f'''Olá, bem-vindo ao sistema bancário!
                            O que você deseja hoje?
                            (D) Realizar Depósito
                            (S) Realizar Saque
                            (E) Verificar Extrato
                            (Q) Sair
                                                    Saldo: R${self.saldo:.2f}
                            ''')).strip().upper()
            except ValueError:
                print('Opcão inválida!\nPor favor, tente novamente.')
                continue

            if opção == 'D':
                self.depositar()
            elif opção == 'S':
                self.sacar()
            elif opção == 'E':
                self.visualizar_extrato()
            elif opção == 'Q':
                print('Obrigado por usar o sistema bancário!\nVolte sempre.')
                break
            else:
                print('Opção inválida! Por favor, tente novamente!')

    def depositar(self):
        while True:
            try:
                depósito = float(input('Digite o valor do depósito: R$'))
                if depósito > 0:
                    self.saldo += depósito
                    self.extrato.append(f'Depósito: +R${depósito:.2f}')
                    print(f'Depósito realizado com sucesso!\nSaldo em conta: R${self.saldo:.2f}')
                    break
                else:
                    print('Valor inválido! Por favor, digite um valor positivo!')
            except ValueError:
                print('Valor inválido! Por favor, digite um número inteiro ou um número com um "." como separador decimal.')

    def sacar(self):
        while True:
            try:
                saque = float(input('Digite o valor do saque: R$'))
                if saque > 0 and saque <= 500 and saque <= self.saldo and self.saques_diarios < Conta.LIMITE_DE_SAQUES_DIÁRIO:
                    self.saldo -= saque
                    self.extrato.append(f'Saque: -R${saque:.2f}')
                    self.saques_diarios += 1
                    print(f'Saque realizado com sucesso!\nSaldo em conta: R${self.saldo:.2f}')
                    break
                elif saque > 500:
                    print('Não é possível realizar esse saque, pois o limite de saque é de R$500.00!')
                elif self.saques_diarios >= Conta.LIMITE_DE_SAQUES_DIÁRIO:
                    print('Você atingiu o limite de saques diários!')
                    break
                elif saque > self.saldo:
                    print(f'Seu saldo é insuficiente.\nSaldo em conta: R${self.saldo:.2f}')
                    break
                else:
                    print('Valor inválido! Por favor, digite um valor positivo!')
            except ValueError:
                print('Valor inválido! Por favor, digite um número inteiro ou um número com um "." como separador decimal.')

    def visualizar_extrato(self):
        print('\n===============Extrato da conta===============')
        if not self.extrato:
            print('Nenhuma operação foi efetuada.')
        else:
            for operação in self.extrato:
                print('~', operação)
        print('==============================================')
        print(f'Saldo da conta: R${self.saldo:.2f}')