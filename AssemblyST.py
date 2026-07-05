# Tabela de simbolos usada pelo AssemblyVisitor e pelo SemanticVisitor.

SCOPE_MAIN = "main"

SCOPE = "scope"
OFFSET = "offset"
TYPE = "type"
PARAMS = "params"
BINDABLE = "bindable"
FUNCTION = "fun"
VARIABLE = "var"

_scopes = []       # um dict por escopo aberto (nome -> binding)
_scopeNames = []    # nome de cada escopo (paralelo a _scopes)
_spStack = []       # stack pointer relativo, um valor por escopo aberto


def reset():
    _scopes.clear()
    _scopeNames.clear()
    _spStack.clear()


def beginScope(name):
    _scopes.append({})
    _scopeNames.append(name)
    _spStack.append(0)


def endScope():
    _scopes.pop()
    _scopeNames.pop()
    _spStack.pop()


def getScope(name=None):
    """Sem argumento devolve o escopo atual. Com um nome, devolve em qual
    escopo essa variavel foi declarada, ou None se nao existir."""
    if name is None:
        return _scopeNames[-1] if _scopeNames else SCOPE_MAIN
    for i in reversed(range(len(_scopes))):
        if name in _scopes[i]:
            return _scopeNames[i]
    return None


def addSP(delta):
    _spStack[-1] += delta


def getSP():
    return _spStack[-1] if _spStack else 0


def addVar(name, type_):
    addSP(-4)
    _scopes[-1][name] = {
        BINDABLE: VARIABLE,
        TYPE: type_,
        OFFSET: getSP(),
        SCOPE: getScope(),
    }


def addFunction(name, params, type_):
    # Funcoes sao sempre registradas no escopo mais externo (main), ja
    # que nao sao aninhadas nessa gramatica. 'params' e uma lista
    # [id1, tipo1, id2, tipo2, ...].
    _scopes[0][name] = {
        BINDABLE: FUNCTION,
        TYPE: type_,
        PARAMS: params,
        SCOPE: SCOPE_MAIN,
    }


def getBindable(name):
    for i in reversed(range(len(_scopes))):
        if name in _scopes[i]:
            return _scopes[i][name]
    return None
