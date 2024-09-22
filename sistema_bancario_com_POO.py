from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereço):
        self.endereco = endereço
        self.contas = []

    def realizar_transacao(self, conta, transação):
        transação.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereço):
        super().__init__(endereço)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n A operação falhou! Saldo insuficiente!")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True

        else:
            print("\nOperação falhou! Valor inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
        else:
            print("\nOperação falhou! Valor inválido")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transação):
        self._transacoes.append(
            {
                "tipo": transação.__class__.__name__,
                "valor": transação.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property # type: ignore
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
def menu():
    clientes = []
    while True:
        print("\nMenu:")
        print("1. Criar Cliente")
        print("2. Criar Conta Corrente")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Verificar Saldo")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do cliente: ")
            data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
            cpf = input("CPF: ")
            endereco = input("Endereço: ")
            cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
            clientes.append(cliente)
            print("Cliente criado com sucesso!")

        elif opcao == "2":
            if not clientes:
                print("Nenhum cliente cadastrado. Crie um cliente primeiro.")
                continue

            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if cliente:
                numero_conta = len(cliente.contas) + 1
                conta = ContaCorrente.nova_conta(cliente, numero_conta)
                cliente.adicionar_conta(conta)
                print(f"Conta criada com sucesso! Número da conta: {conta.numero}")
            else:
                print("Cliente não encontrado.")

        elif opcao == "3":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if cliente:
                numero_conta = int(input("Informe o número da conta: "))
                conta = next((c for c in cliente.contas if c.numero == numero_conta), None)

                if conta:
                    valor = float(input("Valor do depósito: R$ "))
                    Deposito(valor).registrar(conta)
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")

        elif opcao == "4":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if cliente:
                numero_conta = int(input("Informe o número da conta: "))
                conta = next((c for c in cliente.contas if c.numero == numero_conta), None)

                if conta:
                    valor = float(input("Valor do saque: R$ "))
                    Saque(valor).registrar(conta)
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")

        elif opcao == "5":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if cliente:
                numero_conta = int(input("Informe o número da conta: "))
                conta = next((c for c in cliente.contas if c.numero == numero_conta), None)

                if conta:
                    print(f"Saldo da conta {conta.numero}: R$ {conta.saldo:.2f}")
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")

        elif opcao == "6":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
