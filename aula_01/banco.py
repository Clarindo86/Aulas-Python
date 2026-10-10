usuarios=[
{"nome": "Alex Leonardo Clarindo de Lima",
  "email": "alexclarindo@hotmail.com",
  "telefone": "81 999083372",
  "cpf": "06986115431",
  "conta": "01074029-4",
  "agencia": "3295",
  "saldo": 7500.00},
  

{"nome": "Carolina  Vieira Andrade",
  "email": "caroleleli@outlook.com",
  "telefone": "81 994562226",
  "cpf": "06986115728",
  "conta": "01089029-9",
  "agencia": "3294",
    "saldo": 3500.00},


  {"nome": "Ryhan Naubert",
    "email": "Ryhan Naubert@outlook.com",
    "telefone": "81 984679731",
    "cpf": "02786245769",
    "conta": "01069015-3",
    "agencia": "3287",
    "saldo": 4500.00}
]
           
# Criar extrato para cada usuário, se ainda não existir
for usuario in usuarios:
    usuario.setdefault("extrato", [])

# Menu para escolher o usuário
while True:
    print("\n===== BANCO LEÃO DO NORTE =====")
    print("ESCOLHA O USUÁRIO")

    for indice, usuario in enumerate(usuarios, start=1):
        print(f"{indice} - {usuario['nome']}")

    print("0 - Sair")

    try:
        escolha = int(input("Escolha o usuário: "))
    except ValueError:
        print("Digite um número válido.")
        continue

    if escolha == 0:
        print("Programa encerrado.")
        break

    if escolha < 1 or escolha > len(usuarios):
        print("Usuário inválido.")
        continue

    usuario_atual = usuarios[escolha - 1]

    # Menu bancário
    while True:
        print(f"""
===== BANCO LEÃO DO NORTE =====
Titular: {usuario_atual['nome']}

1 - Mostrar saldo
2 - Sacar dinheiro
3 - Depositar dinheiro
4 - Transferir dinheiro
5 - Consultar extrato
0 - Escolher outro usuário
===============================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print(f"Titular: {usuario_atual['nome']}")
            print(f"Saldo: R$ {usuario_atual['saldo']:.2f}")

        elif opcao == "2":
            try:
                valor = float(input("Valor do saque: R$ "))

                if valor <= 0:
                    print("O valor deve ser maior que zero.")
                elif valor > usuario_atual["saldo"]:
                    print("Saldo insuficiente.")
                else:
                    usuario_atual["saldo"] -= valor
                    usuario_atual["extrato"].append(
                        f"Saque: - R$ {valor:.2f}"
                    )
                    print("Saque realizado!")
                    print(f"Saldo atual: R$ {usuario_atual['saldo']:.2f}")

            except ValueError:
                print("Digite um valor válido.")

        elif opcao == "3":
            try:
                valor = float(input("Valor do depósito: R$ "))

                if valor <= 0:
                    print("O valor deve ser maior que zero.")
                else:
                    usuario_atual["saldo"] += valor
                    usuario_atual["extrato"].append(
                        f"Depósito: + R$ {valor:.2f}"
                    )
                    print("Depósito realizado!")
                    print(f"Saldo atual: R$ {usuario_atual['saldo']:.2f}")

            except ValueError:
                print("Digite um valor válido.")

        elif opcao == "4":
            print("\n===== DESTINATÁRIOS =====")

            for indice, destino in enumerate(usuarios, start=1):
                if destino is not usuario_atual:
                    print(f"{indice} - {destino['nome']}")

            try:
                escolha_destino = int(input("Escolha o destinatário: "))

                if escolha_destino < 1 or escolha_destino > len(usuarios):
                    print("Destinatário inválido.")
                    continue

                destinatario = usuarios[escolha_destino - 1]

                if destinatario is usuario_atual:
                    print("Não é possível transferir para a própria conta.")
                    continue

                valor = float(input("Valor da transferência: R$ "))

                if valor <= 0:
                    print("O valor deve ser maior que zero.")
                elif valor > usuario_atual["saldo"]:
                    print("Saldo insuficiente.")
                else:
                    usuario_atual["saldo"] -= valor
                    destinatario["saldo"] += valor

                    usuario_atual["extrato"].append(
                        f"Transferência enviada para {destinatario['nome']}: "
                        f"- R$ {valor:.2f}"
                    )

                    destinatario["extrato"].append(
                        f"Transferência recebida de {usuario_atual['nome']}: "
                        f"+ R$ {valor:.2f}"
                    )

                    print("Transferência realizada com sucesso!")

            except ValueError:
                print("Digite uma opção ou valor válido.")

        elif opcao == "5":
            print(f"\n===== EXTRATO DE {usuario_atual['nome']} =====")

            if not usuario_atual["extrato"]:
                print("Nenhuma movimentação realizada.")
            else:
                for movimentacao in usuario_atual["extrato"]:
                    print(movimentacao)

            print(f"Saldo atual: R$ {usuario_atual['saldo']:.2f}")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")
# Criar extrato para cada usuário, se ainda não existir
for usuario in usuarios:
    usuario.setdefault("extrato", [])

# Menu para escolher o usuário
while True:
    print("\n===== BANCO LEÃO DO NORTE =====")
    print("ESCOLHA O USUÁRIO")

    for indice, usuario in enumerate(usuarios, start=1):
        print(f"{indice} - {usuario['nome']}")

    print("0 - Sair")

    try:
        escolha = int(input("Escolha o usuário: "))
    except ValueError:
        print("Digite um número válido.")
        continue

    if escolha == 0:
        print("Programa encerrado.")
        break

    if escolha < 1 or escolha > len(usuarios):
        print("Usuário inválido.")
        continue

    usuario_atual = usuarios[escolha - 1]

    # Menu bancário
    while True:
        print(f"""
===== BANCO LEÃO DO NORTE =====
Titular: {usuario_atual['nome']}

1 - Mostrar saldo
2 - Sacar dinheiro
3 - Depositar dinheiro
4 - Transferir dinheiro
5 - Consultar extrato
0 - Escolher outro usuário
===============================
""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print(f"Titular: {usuario_atual['nome']}")
            print(f"Saldo: R$ {usuario_atual['saldo']:.2f}")

        elif opcao == "2":
            try:
                valor = float(input("Valor do saque: R$ "))

                if valor <= 0:
                    print("O valor deve ser maior que zero.")
                elif valor > usuario_atual["saldo"]:
                    print("Saldo insuficiente.")
                else:
                    usuario_atual["saldo"] -= valor
                    usuario_atual["extrato"].append(
                        f"Saque: - R$ {valor:.2f}"
                    )
                    print("Saque realizado!")
                    print(f"Saldo atual: R$ {usuario_atual['saldo']:.2f}")

            except ValueError:
                print("Digite um valor válido.")

        elif opcao == "3":
            try:
                valor = float(input("Valor do depósito: R$ "))

                if valor <= 0:
                    print("O valor deve ser maior que zero.")
                else:
                    usuario_atual["saldo"] += valor
                    usuario_atual["extrato"].append(
                        f"Depósito: + R$ {valor:.2f}"
                    )
                    print("Depósito realizado!")
                    print(f"Saldo atual: R$ {usuario_atual['saldo']:.2f}")

            except ValueError:
                print("Digite um valor válido.")

        elif opcao == "4":
            print("\n===== DESTINATÁRIOS =====")

            for indice, destino in enumerate(usuarios, start=1):
                if destino is not usuario_atual:
                    print(f"{indice} - {destino['nome']}")

            try:
                escolha_destino = int(input("Escolha o destinatário: "))

                if escolha_destino < 1 or escolha_destino > len(usuarios):
                    print("Destinatário inválido.")
                    continue

                destinatario = usuarios[escolha_destino - 1]

                if destinatario is usuario_atual:
                    print("Não é possível transferir para a própria conta.")
                    continue

                valor = float(input("Valor da transferência: R$ "))

                if valor <= 0:
                    print("O valor deve ser maior que zero.")
                elif valor > usuario_atual["saldo"]:
                    print("Saldo insuficiente.")
                else:
                    usuario_atual["saldo"] -= valor
                    destinatario["saldo"] += valor

                    usuario_atual["extrato"].append(
                        f"Transferência enviada para {destinatario['nome']}: "
                        f"- R$ {valor:.2f}"
                    )

                    destinatario["extrato"].append(
                        f"Transferência recebida de {usuario_atual['nome']}: "
                        f"+ R$ {valor:.2f}"
                    )

                    print("Transferência realizada com sucesso!")

            except ValueError:
                print("Digite uma opção ou valor válido.")

        elif opcao == "5":
            print(f"\n===== EXTRATO DE {usuario_atual['nome']} =====")

            if not usuario_atual["extrato"]:
                print("Nenhuma movimentação realizada.")
            else:
                for movimentacao in usuario_atual["extrato"]:
                    print(movimentacao)

            print(f"Saldo atual: R$ {usuario_atual['saldo']:.2f}")

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")









  

        






