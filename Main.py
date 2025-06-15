import re


OPERADORES = {'+': 'Sim_adição', '-': 'Sim_subtração', '*': 'Sim_multiplicação', '/': 'Sim_divisão'}
PARENTESES = {'(': 'Abre_parênteses', ')': 'Fecha_parênteses'}


def analisar_tokens(expressao):
    tokens = []
    expressao = expressao.replace(" ", "")
    padrao = r'\d+\.\d+|\d+|[()+\-*/]'
    matches = re.findall(padrao, expressao)

    for m in matches:
        if m.isdigit() or re.fullmatch(r'\d+\.\d+', m):
            tokens.append((m, 'Identificador'))
        elif m in OPERADORES:
            tokens.append((m, OPERADORES[m]))
        elif m in PARENTESES:
            tokens.append((m, PARENTESES[m]))
        else:
            tokens.append((m, 'Desconhecido'))

    return tokens


def analisar_gramatica(tokens):
    pos = 0

    def E():
        nonlocal pos
        derivacoes = []
        i_result, i_deriv = I()
        derivacoes += i_deriv

        if pos < len(tokens) and tokens[pos][0] in OPERADORES:
            op = tokens[pos][0]
            derivacoes.append(f"O → {op}")
            pos += 1
            e_result, e_deriv = E()
            derivacoes += e_deriv
            return True, ["E → I O E"] + derivacoes
        else:
            return True, ["E → I"] + derivacoes

    def I():
        n_result, n_deriv = N()
        return True, ["I → N"] + n_deriv

    def N():
        nonlocal pos
        token = tokens[pos][0]
        derivacoes = []
        if token == '(':
            derivacoes.append("N → ( E )")
            pos += 1
            e_result, e_deriv = E()
            derivacoes += e_deriv
            if tokens[pos][0] == ')':
                pos += 1
                return True, derivacoes
            else:
                raise Exception("Erro: parêntese fechado esperado")
        elif re.fullmatch(r'\d+\.\d+', token):
            partes = token.split('.')
            derivacoes.append(f"N → D.D")
            derivacoes.append(f"D → {partes[0]}")
            derivacoes.append(f"D → {partes[1]}")
            pos += 1
            return True, derivacoes
        elif token.isdigit():
            derivacoes.append(f"N → D")
            derivacoes.append(f"D → {token}")
            pos += 1
            return True, derivacoes
        else:
            raise Exception("Erro: número ou parêntese esperado")

    try:
        _, derivacoes = E()
        return derivacoes
    except Exception as e:
        return [str(e)]


def processar_expressao(expressao):
    print("Expressão:")
    print(expressao)

    print("\nTabela de Tokens")
    print("Token\tCódigo")
    tokens = analisar_tokens(expressao)
    for t, c in tokens:
        print(f"{t}\t{c}")

    print("\nGramática (Derivações):")
    derivacoes = analisar_gramatica(tokens)
    for d in derivacoes:
        print(d)



if __name__ == "__main__":
    exp = input("Digite a expressão matemática: ")
    processar_expressao(exp)
