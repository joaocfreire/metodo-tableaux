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
    # Regra 4: ~~A
    if formula.startswith('~~'):
        return [[formula[2:]]]

    # Regra 1: A ^ B
    if '^' in formula:
        A, B = formula.split('^', 1)
        return [[A.strip(), B.strip()]]

    elif '~(' in formula and formula.endswith(')'):
        sub_formula = formula[2:-1].strip()

        # Regra 6: ~(A v B)
        if 'v' in sub_formula:
            A, B = sub_formula.split('v', 1)
            return [['~' + A.strip(), '~' + B.strip()]]

        # Regra 7: ~(A > B)
        elif '>' in sub_formula:
            A, B = sub_formula.split('>', 1)
            return [[A.strip(), '~' + B.strip()]]

        # Regra 5: ~(A ^ B)
        elif '^' in sub_formula:
            A, B = sub_formula.split('^', 1)
            return [['~' + A.strip()], ['~' + B.strip()]]

    # Regra 2: A v B
    elif 'v' in formula:
        A, B = formula.split('v', 1)
        return [[A.strip()], [B.strip()]]

    # Regra 3: A > B
    elif '>' in formula:
        A, B = formula.split('>', 1)
        return [['~' + A.strip()], [B.strip()]]

    # Se a fórmula for uma negação de atômica (~P)
    return []


# Algoritmo Principal
def metodo_tableau(bd_formulas, query):
    # Inicialização do conjunto inicial de fórmulas: fórmulas do BD + negação da pergunta
    formulas = bd_formulas.copy()
    formulas.append(('~(' + query + ')'))

    # Lista de ramos a serem explorados
    ramos_abertos = [formulas]

    print(f"Iniciando Tableau para: {ramos_abertos[0]}")

    while ramos_abertos:
        # Seleciona o próximo ramo a ser explorado
        ramo_atual = ramos_abertos.pop(0)

        print(f"\nExplorando Ramo: {ramo_atual}")

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
    return True


print("--------------- MÉTODO DE TABLEAU ---------------")

# Entrada de dados
continua = True
database = []
while continua:
    database.append(input("\nEntre com uma fórmula do banco de dados: "))
    continua = input("Deseja continuar digitando fórmulas? [S/N]: ")
    if continua.lower() in 'n':
        continua = False

query = input("\nEntre com uma pergunta: ")

# Resultado do metodo de tableau
print("\nVamos verificar se é Consequência Lógica:")
resultado = metodo_tableau(database, query)
print(f"\nResultado Final: {resultado}")
