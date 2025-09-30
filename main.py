def is_literal(formula):
    if formula.isalpha() and formula.isupper():
        return True
    if formula.startswith('~') and formula[1:].isalpha() and formula[1:].isupper():
        return True
    return False


def not_literal(literal):
    if literal.startswith('~'):
        return literal[1:]
    else:
        return '~' + literal


def ramo_fechado(ramo):
    literais = [f for f in ramo if is_literal(f)]
    for lit in literais:
        negacao_literal = not_literal(lit)
        if negacao_literal in literais:
            return True  # Fechado (Contradição)
    return False


def aplica_regras(formula):
    # Tira parênteses externos
    if formula.startswith('(') and formula.endswith(')'):
        formula = formula.replace('(', '').replace(')', '')

    if formula.startswith('~(') and formula.endswith(')'):
        sub_formula = formula[2:-1].strip()

        # Regra 6: ~(A v B)
        if 'v' in sub_formula:
            print("Regra 6 aplicada")
            A, B = sub_formula.split('v', 1)
            return [['~' + A.strip(), '~' + B.strip()]]

        # Regra 7: ~(A > B)
        elif '>' in sub_formula:
            print("Regra 7 aplicada")
            A, B = sub_formula.split('>', 1)
            return [[A.strip(), '~' + B.strip()]]

        # Regra 5: ~(A ^ B)
        elif '^' in sub_formula:
            print("Regra 5 aplicada")
            A, B = sub_formula.split('^', 1)
            return [['~' + A.strip()], ['~' + B.strip()]]

    # Regra 3: A > B
    elif '>' in formula:
        print("Regra 3 aplicada")
        A, B = formula.split('>', 1)
        return [['~' + A.strip()], [B.strip()]]

    # Regra 1: A ^ B
    elif '^' in formula:
        print("Regra 1 aplicada")
        A, B = formula.split('^', 1)
        return [[A.strip(), B.strip()]]

    # Regra 2: A v B
    elif 'v' in formula:
        print("Regra 2 aplicada")
        A, B = formula.split('v', 1)
        return [[A.strip()], [B.strip()]]

    # Regra 4: ~~A
    elif formula.startswith('~~'):
        print("Regra 4 aplicada")
        return [[formula[2:]]]

    # Caso contrário
    return []


# Algoritmo Principal
def tableau_semantico(bd_formulas, query):
    # Inicialização do conjunto inicial de fórmulas: fórmulas do BD + negação da pergunta
    formulas = bd_formulas.copy()
    if is_literal(query):
        formulas.append('~' + query)
    else:
        formulas.append(('~(' + query + ')'))

    # Lista de ramos a serem explorados
    ramos_abertos = [formulas]

    qtd_ramos_explorados = 0
    print(f"Iniciando Tableau para: {ramos_abertos[0]}")

    while ramos_abertos:
        # Seleciona o próximo ramo a ser explorado
        ramo_atual = ramos_abertos.pop(0)

        print(f"\nExplorando Ramo: {ramo_atual}")
        qtd_ramos_explorados += 1

        # Verificar Fechamento: se o ramo atual contém uma contradição
        if ramo_fechado(ramo_atual):
            print("RAMO FECHADO (Contradição Encontrada: P e ~P)")
            continue  # Passa para o próximo ramo

        # Selecionar fórmula para decomposição (prioriza não literais)
        formulas_para_decompor = None
        for formula in ramo_atual:
            if not is_literal(formula):
                formulas_para_decompor = formula
                break

        # Conclusão do Ramo (se não houver mais decomposições possíveis)
        if formulas_para_decompor is None:
            print("RAMO ABERTO (Modelo Encontrado para a Negação)")
            print(f"\nQuantidade de ramos explorados: {qtd_ramos_explorados}")
            return False

        # Aplica Regras de Decomposição
        print(f"Decompondo: {formulas_para_decompor}")

        ramo_atual.remove(formulas_para_decompor)
        sub_ramos = aplica_regras(formulas_para_decompor)

        # Adiciona os novos ramos à lista de abertos
        for ramo in sub_ramos:
            novo_ramo = ramo_atual + ramo
            ramos_abertos.append(novo_ramo)
            print(f"Novo sub-ramo criado: {novo_ramo}")

    # Se o loop terminar e não houver retorno falso significa que todos os ramos foram fechados
    print("\nTODOS OS RAMOS FECHARAM.")
    print(f"Quantidade de ramos explorados: {qtd_ramos_explorados}")
    return True


print("*-------------------- TABLEAU SEMÂNTICO --------------------*")

print("OBS1: Digite os literais com letras maiúsculas")
print("OBS2: Operadores aceitos: ~ / ^ / v / > / ( )")

# Entrada de dados
continua = True
database = []
while continua:
    database.append(input("\nEntre com uma fórmula do banco de dados: "))
    continua = input("Deseja continuar digitando fórmulas? [S/N]: ")
    if continua.lower() in 'n':
        continua = False

query = input("\nEntre com uma pergunta: ")


#  -------------------- Exemplos vistos em aula --------------------  #

# Exemplo 1 - Resultado esperado: True
# database = ['(A v B) > C', 'C > (D^E)', 'A']
# query = 'E v F'

# Exemplo 2 - Resultado esperado: True
# database = ['~(~A ^ ~B)', '~C > ~A']
# query = '~(B ^ ~C) > C'

# Exemplo 3 - Resultado esperado: False
# database = ['A v C', '~B > A']
# query = 'A > C'

# Exemplo 4 - Resultado esperado: True
# database = ['A v B v C', 'A > (C v ~D)', 'A > ~C', 'B > C', 'C > ~D']
# query = '~D v E'

# Exemplo 5 - Resultado esperado: True
# database = ['A > (B v C)', 'B > D', 'F > (D ^ E)', 'A v F', '(C ^ A) > D']
# query = 'D'


# Resultado do tableau semântico
print("\nVamos verificar se é Consequência Lógica:")
resultado = tableau_semantico(database, query)
print(f"\nResultado Final: {resultado}")
