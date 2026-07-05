# Analise semantica: percorre a AST calculando o tipo de cada
# expressao/comando e reportando erro quando dois tipos incompativeis
# se encontram (soma, comparacao, atribuicao, retorno, chamada de
# funcao). Usa o Visitor pretty-printer so pra mostrar, na mensagem de
# erro, qual expressao/comando deu problema. Reaproveita a tabela de
# simbolos do AssemblyST.py (mesma pilha de escopos, so que o campo
# TYPE guarda o tipo semantico em vez do tamanho em memoria).

from AbstractVisitor import AbstractVisitor
from visitor import Visitor
import SintaxeAbstrata as sa
import AssemblyST as st

NUMBER = 'number'
STRING = 'string'
BOOLEAN = 'boolean'


def coercion(tipo1, tipo2):
    """Dado dois tipos, devolve o tipo resultante da operacao (ou None se
    forem incompativeis). So numeros operam com numeros."""
    if tipo1 == NUMBER and tipo2 == NUMBER:
        return NUMBER
    return None


class SemanticVisitor(AbstractVisitor):

    def __init__(self):
        self.printer = Visitor()
        self.n_errors = 0
        st.reset()
        st.beginScope(st.SCOPE_MAIN)

    def getnerros(self):
        return self.n_errors

    def _erro(self, node, mensagem):
        self.n_errors += 1
        print(f"\n\t[Erro semantico] {mensagem}")
        try:
            print("\t  Expressao/comando: ", end='')
            node.accept(self.printer)
            print()
        except Exception:
            pass

    # ---------------- Programa ----------------

    def visitProgramaFuncDecl(self, programa):
        programa.funcdecl.accept(self)

    def visitProgramaFuncDeclPrograma(self, programa):
        programa.funcdecl.accept(self)
        programa.programa.accept(self)

    def visitProgramaComandos(self, programa):
        programa.comandos.accept(self)

    def visitProgramaComandosPrograma(self, programa):
        programa.comandos.accept(self)
        programa.programa.accept(self)

    # ---------------- Declaracao de variaveis ----------------

    def visitVarDecl(self, x):
        pass

    def visitVarDeclID(self, varDeclID):
        tipoDeclarado = varDeclID.tipo.accept(self)
        st.addVar(varDeclID.id, tipoDeclarado)
        return tipoDeclarado

    def visitVarDeclIDAssign(self, varDeclIDAssign):
        tipoDeclarado = varDeclIDAssign.tipo.accept(self)
        tipoExpr = varDeclIDAssign.expressao.accept(self)
        if tipoExpr is not None and tipoDeclarado != tipoExpr:
            self._erro(
                varDeclIDAssign.expressao,
                f"A variavel '{varDeclIDAssign.id}' foi declarada como "
                f"'{tipoDeclarado}', mas recebeu um valor do tipo '{tipoExpr}'."
            )
        st.addVar(varDeclIDAssign.id, tipoDeclarado)
        return tipoDeclarado

    def visitVarDeclIDAssignID(self, varDeclIDAssignID):
        pass

    def visitVarDeclIDAssignList(self, varDeclIDAssignList):
        tipoDeclarado = varDeclIDAssignList.tipo.accept(self)
        if varDeclIDAssignList.listexp is not None:
            tipos = varDeclIDAssignList.listexp.accept(self)
            for t in tipos:
                if t is not None and t != tipoDeclarado:
                    self._erro(
                        varDeclIDAssignList.listexp,
                        f"O array '{varDeclIDAssignList.id}' foi declarado "
                        f"como '{tipoDeclarado}[]', mas contem um elemento "
                        f"do tipo '{t}'."
                    )
        st.addVar(varDeclIDAssignList.id, tipoDeclarado + "[]")
        return tipoDeclarado + "[]"

    def visitVarDeclIDAssignListTIPO(self, v):
        tipo1 = v.tipo1.accept(self)
        tipo2 = v.tipo2.accept(self)
        if v.listexp is not None:
            tipos = v.listexp.accept(self)
            for t in tipos:
                if t is not None and t != tipo1 and t != tipo2:
                    self._erro(
                        v.listexp,
                        f"O array '{v.id}' foi declarado como "
                        f"'({tipo1}|{tipo2})[]', mas contem um elemento do "
                        f"tipo '{t}'."
                    )
        st.addVar(v.id, f"({tipo1}|{tipo2})[]")
        return f"({tipo1}|{tipo2})[]"

    # ---------------- Declaracao de funcoes ----------------

    def visitFuncDecl(self, x):
        pass

    def visitFuncDeclSignature(self, funcDeclSignature):
        funcDeclSignature.signature.accept(self)
        funcDeclSignature.body.accept(self)
        st.endScope()

    # ---------------- Assinatura das funcoes ----------------

    def visitSignature(self, x):
        pass

    def visitSignatureFunc(self, signatureFunc):
        params = []
        if signatureFunc.funcparametros is not None:
            params = signatureFunc.funcparametros.accept(self)
        tipoRetorno = signatureFunc.tipo2.accept(self)
        st.addFunction(signatureFunc.id, params, tipoRetorno)
        st.beginScope(signatureFunc.id)
        for k in range(0, len(params), 2):
            st.addVar(params[k], params[k + 1])

    # ---------------- Parametros de funcao ----------------

    def visitFuncParametros(self, x):
        pass

    def visitFuncParametrosID(self, f):
        return [f.id, f.tipo.accept(self)]

    def visitFuncParametrosIDList(self, f):
        return [f.id, f.tipo.accept(self)] + f.funcParametros.accept(self)

    # ---------------- Corpo de funcao ----------------

    def visitBody(self, x):
        pass

    def visitBodyComandos(self, bodyComandos):
        if bodyComandos.comandos is not None:
            bodyComandos.comandos.accept(self)

    def visitBodyComando(self, x):
        pass

    def visitBodyOrComando(self, bodyOrComando):
        bodyOrComando.body.accept(self)

    def visitBodyOrComando2(self, bodyOrComando2):
        bodyOrComando2.comando.accept(self)

    # ---------------- Comandos ----------------

    def visitComando(self, x):
        pass

    def visitSingleComando(self, singleComando):
        singleComando.comando.accept(self)

    def visitCompoundComando(self, compoundComando):
        compoundComando.comando.accept(self)
        compoundComando.comandos.accept(self)

    def visitComandoVarDecl(self, comandoVarDecl):
        comandoVarDecl.varDecl.accept(self)

    def visitComandoExpressao(self, comandoExpressao):
        comandoExpressao.expressao.accept(self)

    def visitComandoReturn(self, comandoReturn):
        tipoExpr = comandoReturn.expressao.accept(self)
        escopo = st.getScope()
        bind = st.getBindable(escopo) if escopo != st.SCOPE_MAIN else None
        if bind is not None and tipoExpr is not None and tipoExpr != bind[st.TYPE]:
            self._erro(
                comandoReturn.expressao,
                f"A funcao '{escopo}' deveria retornar '{bind[st.TYPE]}', "
                f"mas o retorno encontrado eh do tipo '{tipoExpr}'."
            )

    def visitComandoWhile(self, comandoWhile):
        tipoCond = comandoWhile.expressao.accept(self)
        if tipoCond is not None and tipoCond != BOOLEAN:
            self._erro(
                comandoWhile.expressao,
                f"A condicao do 'while' deveria ser 'boolean', mas eh do "
                f"tipo '{tipoCond}'."
            )
        comandoWhile.bodyorcomando.accept(self)

    def visitComandoIf(self, comandoIf):
        tipoCond = comandoIf.expressao.accept(self)
        if tipoCond is not None and tipoCond != BOOLEAN:
            self._erro(
                comandoIf.expressao,
                f"A condicao do 'if' deveria ser 'boolean', mas eh do tipo "
                f"'{tipoCond}'."
            )
        comandoIf.bodyorcomando.accept(self)

    def visitComandoIfElse(self, comandoIfElse):
        tipoCond = comandoIfElse.expressao.accept(self)
        if tipoCond is not None and tipoCond != BOOLEAN:
            self._erro(
                comandoIfElse.expressao,
                f"A condicao do 'if' deveria ser 'boolean', mas eh do tipo "
                f"'{tipoCond}'."
            )
        comandoIfElse.bodyorcomando1.accept(self)
        comandoIfElse.bodyorcomando2.accept(self)

    def visitComandoFor(self, comandoFor):
        comandoFor.expressao1.accept(self)
        tipoCond = comandoFor.expressao2.accept(self)
        if tipoCond is not None and tipoCond != BOOLEAN:
            self._erro(
                comandoFor.expressao2,
                f"A condicao do 'for' deveria ser 'boolean', mas eh do "
                f"tipo '{tipoCond}'."
            )
        comandoFor.bodyorcomando.accept(self)
        comandoFor.expressao3.accept(self)

    def visitExpOpexp(self, expOpexp):
        if expOpexp.expressao is not None:
            return expOpexp.expressao.accept(self)
        return None

    # ---------------- Expressoes: literais / atomos ----------------

    def visitExpressao(self, x):
        pass

    def visitExpressaoID(self, e):
        bind = st.getBindable(e.id)
        if bind is None:
            self._erro(e, f"A variavel '{e.id}' foi usada mas nunca foi declarada.")
            return None
        return bind[st.TYPE]

    def visitExpressaoInt(self, e):
        return NUMBER

    def visitExpressaoFloat(self, e):
        return NUMBER

    def visitExpressaoString(self, e):
        return e.string.accept(self)

    def visitstring(self, s):
        return STRING

    def visitExpressaoBool(self, e):
        return BOOLEAN

    def visitExpressaoNum(self, e):
        return NUMBER

    # ---------------- Expressoes aritmeticas ----------------

    def _checaAritmetica(self, e, operador):
        tipo1 = e.expressao1.accept(self)
        tipo2 = e.expressao2.accept(self)
        resultado = coercion(tipo1, tipo2)
        if resultado is None and tipo1 is not None and tipo2 is not None:
            self._erro(
                e,
                f"Operacao '{operador}' invalida entre os tipos '{tipo1}' "
                f"e '{tipo2}' (esperado 'number' dos dois lados)."
            )
        return resultado

    def visitExpressaoPlus(self, e):
        tipo1 = e.expressao1.accept(self)
        tipo2 = e.expressao2.accept(self)
        if tipo1 == STRING and tipo2 == STRING:
            return STRING
        resultado = coercion(tipo1, tipo2)
        if resultado is None and tipo1 is not None and tipo2 is not None:
            self._erro(
                e,
                f"Operacao '+' invalida entre os tipos '{tipo1}' e "
                f"'{tipo2}' (esperado 'number'+'number' ou 'string'+'string')."
            )
        return resultado

    def visitExpressaoMinus(self, e):
        return self._checaAritmetica(e, '-')

    def visitExpressaoMult(self, e):
        return self._checaAritmetica(e, '*')

    def visitExpressaoDiv(self, e):
        return self._checaAritmetica(e, '/')

    def visitExpressaoMod(self, e):
        return self._checaAritmetica(e, '%')

    def visitExpressaoExpo(self, e):
        return self._checaAritmetica(e, '**')

    def visitExpressaoMultincrement(self, e):
        return self._checaAritmetica(e, '*=')

    def visitExpressaoDivideincrement(self, e):
        return self._checaAritmetica(e, '/=')

    def visitExpressaoModincrement(self, e):
        return self._checaAritmetica(e, '%=')

    def visitExpressaoIncrement(self, e):
        tipo = e.expressao.accept(self)
        if tipo is not None and tipo != NUMBER:
            self._erro(e, f"Operador '++' exige 'number', recebeu '{tipo}'.")
        return NUMBER

    def visitExpressaoDecrement(self, e):
        tipo = e.expressao.accept(self)
        if tipo is not None and tipo != NUMBER:
            self._erro(e, f"Operador '--' exige 'number', recebeu '{tipo}'.")
        return NUMBER

    def visitExpressaoIncrementn(self, e):
        return e.expressao1.accept(self) if hasattr(e, 'expressao1') else None

    def visitExpressaoDecrementn(self, e):
        return e.expressao1.accept(self) if hasattr(e, 'expressao1') else None

    # ---------------- Expressoes relacionais ----------------

    def _checaRelacional(self, e, operador):
        tipo1 = e.expressao1.accept(self)
        tipo2 = e.expressao2.accept(self)
        if tipo1 == NUMBER and tipo2 == NUMBER:
            return BOOLEAN
        if tipo1 is not None and tipo2 is not None:
            self._erro(
                e,
                f"Comparacao '{operador}' invalida entre os tipos "
                f"'{tipo1}' e '{tipo2}' (esperado 'number' dos dois lados)."
            )
        return None

    def visitExpressaoGreater(self, e):
        return self._checaRelacional(e, '>')

    def visitExpressaoLess(self, e):
        return self._checaRelacional(e, '<')

    def visitExpressaoGreaterEqual(self, e):
        return self._checaRelacional(e, '>=')

    def visitExpressaoLessEqual(self, e):
        return self._checaRelacional(e, '<=')

    # ---------------- Expressoes de igualdade ----------------

    def _checaIgualdade(self, e, operador):
        tipo1 = e.expressao1.accept(self)
        tipo2 = e.expressao2.accept(self)
        if tipo1 is not None and tipo2 is not None and tipo1 != tipo2:
            self._erro(
                e,
                f"Comparacao '{operador}' entre tipos diferentes: "
                f"'{tipo1}' e '{tipo2}'."
            )
        return BOOLEAN

    def visitExpressaoEqual(self, e):
        return self._checaIgualdade(e, '==')

    def visitExpressaoNotEqual(self, e):
        return self._checaIgualdade(e, '!=')

    def visitExpressaoEEQ(self, e):
        return self._checaIgualdade(e, '===')

    def visitExpressaoNNEQ(self, e):
        return self._checaIgualdade(e, '!==')

    # ---------------- Expressoes logicas ----------------

    def _checaLogica(self, e, operador):
        tipo1 = e.expressao1.accept(self)
        tipo2 = e.expressao2.accept(self)
        if tipo1 == BOOLEAN and tipo2 == BOOLEAN:
            return BOOLEAN
        if tipo1 is not None and tipo2 is not None:
            self._erro(
                e,
                f"Operador '{operador}' exige 'boolean' dos dois lados, "
                f"recebeu '{tipo1}' e '{tipo2}'."
            )
        return None

    def visitExpressaoAnd(self, e):
        return self._checaLogica(e, '&&')

    def visitExpressaoOr(self, e):
        return self._checaLogica(e, '||')

    def visitExpressaoNOT(self, e):
        tipo = e.expressao.accept(self)
        if tipo is not None and tipo != BOOLEAN:
            self._erro(e, f"Operador '!' exige 'boolean', recebeu '{tipo}'.")
        return BOOLEAN

    def visitExpressaoFIM(self, e):
        tipoCond = e.expressao1.accept(self)
        if tipoCond is not None and tipoCond != BOOLEAN:
            self._erro(
                e.expressao1,
                f"A condicao do operador ternario deveria ser 'boolean', "
                f"mas eh do tipo '{tipoCond}'."
            )
        tipo2 = e.expressao2.accept(self)
        tipo3 = e.expressao3.accept(self)
        if tipo2 is not None and tipo3 is not None and tipo2 != tipo3:
            self._erro(
                e,
                f"Os dois ramos do operador ternario tem tipos diferentes: "
                f"'{tipo2}' e '{tipo3}'."
            )
        return tipo2 if tipo2 is not None else tipo3

    # ---------------- Atribuicao ----------------

    def visitAssign(self, x):
        pass

    def visitExpressaoAssign(self, e):
        return e.assign.accept(self)

    def visitAssignAssign(self, assign):
        tipoExpr = assign.exp.accept(self)
        bind = st.getBindable(assign.id)
        if bind is None:
            st.addVar(assign.id, tipoExpr)
            return tipoExpr
        if tipoExpr is not None and bind[st.TYPE] != tipoExpr:
            self._erro(
                assign,
                f"A variavel '{assign.id}' eh do tipo '{bind[st.TYPE]}', "
                f"mas recebeu um valor do tipo '{tipoExpr}'."
            )
        return bind[st.TYPE]

    def visitNoAssign(self, e):
        pass

    def visitExpressaoVardecl(self, e):
        return e.varDecl.accept(self)

    # ---------------- Chamada de funcao ----------------

    def visitCall(self, x):
        pass

    def visitExpressaoCall(self, e):
        return e.call.accept(self)

    def visitParamsCall(self, paramsCall):
        bind = st.getBindable(paramsCall.id)
        if bind is None or bind[st.BINDABLE] != st.FUNCTION:
            self._erro(
                paramsCall,
                f"'{paramsCall.id}' nao eh uma funcao, ou nao foi declarada "
                f"antes desta chamada."
            )
            return None
        tiposPassados = paramsCall.params.accept(self)
        tiposEsperados = list(bind[st.PARAMS][1::2])
        if tiposPassados != tiposEsperados:
            self._erro(
                paramsCall,
                f"Chamada invalida de '{paramsCall.id}'. Tipos passados: "
                f"{tiposPassados}. Tipos esperados pela assinatura: "
                f"{tiposEsperados}."
            )
            return None
        return bind[st.TYPE]

    def visitNoParamsCall(self, noParamsCall):
        bind = st.getBindable(noParamsCall.id)
        if bind is None or bind[st.BINDABLE] != st.FUNCTION:
            self._erro(
                noParamsCall,
                f"'{noParamsCall.id}' nao eh uma funcao, ou nao foi "
                f"declarada antes desta chamada."
            )
            return None
        tiposEsperados = list(bind[st.PARAMS][1::2])
        if len(tiposEsperados) != 0:
            self._erro(
                noParamsCall,
                f"Chamada invalida de '{noParamsCall.id}'. A funcao espera "
                f"{len(tiposEsperados)} parametro(s) ({tiposEsperados}), "
                f"mas nenhum foi passado."
            )
            return None
        return bind[st.TYPE]

    # ---------------- Parametros ----------------

    def visitParams(self, x):
        pass

    def visitSingleParams(self, params):
        return [params.exp.accept(self)]

    def visitCompoundParams(self, params):
        return [params.exp.accept(self)] + params.params.accept(self)

    # ---------------- Listas de expressoes (arrays) ----------------

    def visitSingleListexp(self, l):
        return [l.expressao.accept(self)]

    def visitCompoundListexp(self, l):
        return [l.expressao.accept(self)] + l.listexp.accept(self)

    # ---------------- tipo / tipodecl ----------------

    def visittipo(self, t):
        return t.tipo

    def visittipodecl(self, t):
        return t.tipo

    def visittipodecltipo(self, t):
        return t.tipo2.accept(self)


def main():
    import sys
    from ExpressionLanguageSint import lexer, parser

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            codigo_fonte = f.read()
    else:
        codigo_fonte = '''
        function soma(a: number, b: number): number {
            return a + b;
        }
        '''

    lexer.input(codigo_fonte)
    resultado = parser.parse(lexer=lexer, debug=False)

    print("#imprime erros semanticos encontrados")
    svisitor = SemanticVisitor()
    if resultado is not None:
        resultado.accept(svisitor)
    print(f"Foram encontrados {svisitor.getnerros()} erro(s)")


if __name__ == "__main__":
    main()
