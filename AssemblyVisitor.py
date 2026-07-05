from AbstractVisitor import AbstractVisitor
from ExpressionLanguageSint import *
import SintaxeAbstrata as sa
import AssemblyST as st


def getAssemblyType(tipo=None):
    # so usamos .word pra tudo (number/string/boolean); MIPS trabalha em
    # palavras de 4 bytes e strings nao sao geradas de verdade aqui.
    return ".word"


class AssemblyVisitor(AbstractVisitor):

    def __init__(self):
        st.beginScope(st.SCOPE_MAIN)

        self.funcs = []
        self.text = []
        self.text.append(".text")
        self.text.append("    move $fp, $sp")

        self.data = set()
        self.rotulos = {}

    def novo_rotulo(self, nome):
        if nome not in self.rotulos:
            self.rotulos[nome] = 0
        rotulo = f"{nome}_{self.rotulos[nome]}"
        self.rotulos[nome] += 1
        return rotulo

    def getList(self):
        # main gera no .text; dentro de uma funcao, gera em .funcs
        return self.text if st.getScope() == st.SCOPE_MAIN else self.funcs

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

    def visitVarDeclID(self, varDeclID):
        name = varDeclID.id
        if st.getScope() == st.SCOPE_MAIN:
            self.data.add((name, getAssemblyType()))
        else:
            code = self.getList()
            st.addVar(name, getAssemblyType())
            code.append("    addi $sp, $sp, -4")

    def visitVarDeclIDAssign(self, varDeclIDAssign):
        name = varDeclIDAssign.id
        code = self.getList()
        varDeclIDAssign.expressao.accept(self)
        if st.getScope() == st.SCOPE_MAIN:
            self.data.add((name, getAssemblyType()))
            code.append(f"    sw $v0, {name}($zero)")
        else:
            st.addVar(name, getAssemblyType())
            bind = st.getBindable(name)
            code.append("    addi $sp, $sp, -4")
            code.append(f"    sw $v0, {bind[st.OFFSET]}($fp)")

    def visitVarDeclIDAssignID(self, varDeclIDAssignID):
        pass

    def visitVarDeclIDAssignList(self, varDeclIDAssignList):
        pass

    def visitVarDeclIDAssignListTIPO(self, varDeclIDAssignListTIPO):
        pass

    # ---------------- Declaracao de funcoes ----------------

    def visitFuncDeclSignature(self, funcDeclSignature):
        funcDeclSignature.signature.accept(self)
        funcDeclSignature.body.accept(self)
        st.endScope()

    def visitSignatureFunc(self, signatureFunc):
        params = []
        if signatureFunc.funcparametros is not None:
            params = signatureFunc.funcparametros.accept(self)
        st.addFunction(signatureFunc.id, params, getAssemblyType())
        st.beginScope(signatureFunc.id)

        code = self.getList()
        code.append(f"{signatureFunc.id}:")
        code.append("    move $fp, $sp")

        for k in range(0, len(params), 2):
            st.addVar(params[k], params[k + 1])

        if st.getSP() != 0:
            code.append(f"    addi $sp, $sp, {st.getSP()}")

    # ---------------- Parametros de funcao ----------------

    def visitFuncParametrosID(self, funcParametrosID):
        return [funcParametrosID.id, getAssemblyType()]

    def visitFuncParametrosIDList(self, funcParametrosIDList):
        resto = funcParametrosIDList.funcParametros.accept(self)
        return [funcParametrosIDList.id, getAssemblyType()] + resto

    # ---------------- Corpo de funcao ----------------

    def visitBodyComandos(self, bodyComandos):
        bodyComandos.comandos.accept(self)

    def visitBodyOrComando(self, bodyOrComando):
        bodyOrComando.body.accept(self)

    def visitBodyOrComando2(self, bodyOrComando2):
        bodyOrComando2.comando.accept(self)

    # ---------------- Comandos ----------------

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
        comandoReturn.expressao.accept(self)
        code = self.getList()
        code.append("    move $sp, $fp")
        code.append("    jr $ra")

    def visitComandoWhile(self, comandoWhile):
        code = self.getList()
        rotulo_inicio = self.novo_rotulo("whilestm")
        rotulo_fim = self.novo_rotulo("fim_whilestm")
        code.append(f"{rotulo_inicio}:")
        comandoWhile.expressao.accept(self)
        code.append(f"    beq $v0, $zero, {rotulo_fim}")
        comandoWhile.bodyorcomando.accept(self)
        code.append(f"    j {rotulo_inicio}")
        code.append(f"{rotulo_fim}:")

    def visitComandoIf(self, comandoIf):
        code = self.getList()
        rotulo_fim = self.novo_rotulo("fim_if")
        comandoIf.expressao.accept(self)
        code.append(f"    beq $v0, $zero, {rotulo_fim}")
        comandoIf.bodyorcomando.accept(self)
        code.append(f"{rotulo_fim}:")

    def visitComandoIfElse(self, comandoIfElse):
        code = self.getList()
        rotulo_else = self.novo_rotulo("else")
        rotulo_fim = self.novo_rotulo("fim_ifelse")
        comandoIfElse.expressao.accept(self)
        code.append(f"    beq $v0, $zero, {rotulo_else}")
        comandoIfElse.bodyorcomando1.accept(self)
        code.append(f"    j {rotulo_fim}")
        code.append(f"{rotulo_else}:")
        comandoIfElse.bodyorcomando2.accept(self)
        code.append(f"{rotulo_fim}:")

    def visitComandoFor(self, comandoFor):
        code = self.getList()
        rotulo_inicio = self.novo_rotulo("forstm")
        rotulo_fim = self.novo_rotulo("fim_forstm")
        comandoFor.expressao1.accept(self)
        code.append(f"{rotulo_inicio}:")
        comandoFor.expressao2.accept(self)
        code.append(f"    beq $v0, $zero, {rotulo_fim}")
        comandoFor.bodyorcomando.accept(self)
        comandoFor.expressao3.accept(self)
        code.append(f"    j {rotulo_inicio}")
        code.append(f"{rotulo_fim}:")

    def visitExpOpexp(self, expOpexp):
        if expOpexp.expressao is not None:
            expOpexp.expressao.accept(self)

    # ---------------- Expressoes aritmeticas/logicas ----------------
    # Padrao comum: avalia expressao1, empilha, avalia expressao2,
    # desempilha, aplica a operacao. Resultado fica em $v0.

    def _binaria(self, expressao1, expressao2, instrucao):
        code = self.getList()
        expressao1.accept(self)
        code.append("    addi $sp, $sp, -4")
        st.addSP(-4)
        code.append("    sw $v0, 0($sp)")
        expressao2.accept(self)
        code.append("    lw $t0, 0($sp)")
        code.append("    addi $sp, $sp, 4")
        st.addSP(4)
        code.append(f"    {instrucao} $v0, $t0, $v0")

    def visitExpressaoPlus(self, e):
        self._binaria(e.expressao1, e.expressao2, "add")

    def visitExpressaoMinus(self, e):
        self._binaria(e.expressao1, e.expressao2, "sub")

    def visitExpressaoMult(self, e):
        self._binaria(e.expressao1, e.expressao2, "mul")

    def visitExpressaoDiv(self, e):
        self._binaria(e.expressao1, e.expressao2, "div")

    def visitExpressaoMod(self, e):
        code = self.getList()
        e.expressao1.accept(self)
        code.append("    addi $sp, $sp, -4")
        st.addSP(-4)
        code.append("    sw $v0, 0($sp)")
        e.expressao2.accept(self)
        code.append("    lw $t0, 0($sp)")
        code.append("    addi $sp, $sp, 4")
        st.addSP(4)
        code.append("    div $t0, $v0")
        code.append("    mfhi $v0")

    def visitExpressaoAnd(self, e):
        self._binaria(e.expressao1, e.expressao2, "and")

    def visitExpressaoOr(self, e):
        self._binaria(e.expressao1, e.expressao2, "or")

    def visitExpressaoGreater(self, e):
        self._binaria(e.expressao1, e.expressao2, "sgt")

    def visitExpressaoLess(self, e):
        self._binaria(e.expressao1, e.expressao2, "slt")

    def visitExpressaoGreaterEqual(self, e):
        self._binaria(e.expressao1, e.expressao2, "sge")

    def visitExpressaoLessEqual(self, e):
        self._binaria(e.expressao1, e.expressao2, "sle")

    def visitExpressaoEqual(self, e):
        self._binaria(e.expressao1, e.expressao2, "seq")

    def visitExpressaoNotEqual(self, e):
        self._binaria(e.expressao1, e.expressao2, "sne")

    def visitExpressaoEEQ(self, e):
        self._binaria(e.expressao1, e.expressao2, "seq")

    def visitExpressaoNNEQ(self, e):
        self._binaria(e.expressao1, e.expressao2, "sne")

    def visitExpressaoNOT(self, e):
        code = self.getList()
        e.expressao.accept(self)
        code.append("    xori $v0, $v0, 1")

    def visitExpressaoExpo(self, e):
        code = self.getList()
        e.expressao1.accept(self)
        code.append("    addi $sp, $sp, -4")
        st.addSP(-4)
        code.append("    sw $v0, 0($sp)")
        e.expressao2.accept(self)
        code.append("    lw $t0, 0($sp)")
        code.append("    addi $sp, $sp, 4")
        st.addSP(4)
        code.append("    move $t1, $v0")
        code.append("    li $v0, 1")
        rotulo_laco = self.novo_rotulo("potexp")
        rotulo_fim = self.novo_rotulo("fim_potexp")
        code.append(f"{rotulo_laco}:")
        code.append(f"    beq $t1, $zero, {rotulo_fim}")
        code.append("    mul $v0, $v0, $t0")
        code.append("    addi $t1, $t1, -1")
        code.append(f"    j {rotulo_laco}")
        code.append(f"{rotulo_fim}:")

    def _incr_decr(self, e, delta):
        code = self.getList()
        if not isinstance(e.expressao, sa.ExpressaoID):
            e.expressao.accept(self)
            return
        nome = e.expressao.id
        bind = st.getBindable(nome)
        e.expressao.accept(self)
        code.append(f"    addi $t0, $v0, {delta}")
        if bind is not None and st.getScope(nome) == st.SCOPE_MAIN:
            code.append(f"    sw $t0, {nome}($zero)")
        elif bind is not None:
            code.append(f"    sw $t0, {bind[st.OFFSET]}($fp)")

    def visitExpressaoIncrement(self, e):
        self._incr_decr(e, 1)

    def visitExpressaoDecrement(self, e):
        self._incr_decr(e, -1)

    def _incr_decr_composto(self, e, instrucao):
        code = self.getList()
        if not isinstance(e.expressao1, sa.ExpressaoID):
            e.expressao2.accept(self)
            return
        nome = e.expressao1.id
        e.expressao1.accept(self)
        code.append("    addi $sp, $sp, -4")
        st.addSP(-4)
        code.append("    sw $v0, 0($sp)")
        e.expressao2.accept(self)
        code.append("    lw $t0, 0($sp)")
        code.append("    addi $sp, $sp, 4")
        st.addSP(4)
        code.append(f"    {instrucao} $v0, $t0, $v0")
        bind = st.getBindable(nome)
        if bind is not None and st.getScope(nome) == st.SCOPE_MAIN:
            code.append(f"    sw $v0, {nome}($zero)")
        elif bind is not None:
            code.append(f"    sw $v0, {bind[st.OFFSET]}($fp)")

    def visitExpressaoIncrementn(self, e):
        pass

    def visitExpressaoDecrementn(self, e):
        pass

    def visitExpressaoMultincrement(self, e):
        self._incr_decr_composto(e, "mul")

    def visitExpressaoDivideincrement(self, e):
        self._incr_decr_composto(e, "div")

    def visitExpressaoModincrement(self, e):
        self._incr_decr_composto(e, "rem")

    def visitExpressaoFIM(self, e):
        code = self.getList()
        rotulo_else = self.novo_rotulo("ternario_else")
        rotulo_fim = self.novo_rotulo("fim_ternario")
        e.expressao1.accept(self)
        code.append(f"    beq $v0, $zero, {rotulo_else}")
        e.expressao2.accept(self)
        code.append(f"    j {rotulo_fim}")
        code.append(f"{rotulo_else}:")
        e.expressao3.accept(self)
        code.append(f"{rotulo_fim}:")

    # ---------------- Valores literais / atomos ----------------

    def visitExpressaoInt(self, e):
        code = self.getList()
        code.append(f"    li $v0, {e.int}")

    def visitExpressaoFloat(self, e):
        pass

    def visitExpressaoString(self, e):
        pass

    def visitExpressaoID(self, e):
        code = self.getList()
        bind = st.getBindable(e.id)
        if bind is None:
            return
        if st.getScope(e.id) == st.SCOPE_MAIN:
            code.append(f"    lw $v0, {e.id}($zero)")
        else:
            code.append(f"    lw $v0, {bind[st.OFFSET]}($fp)")

    def visitExpressaoBool(self, e):
        code = self.getList()
        valor = 1 if e.bool is True else 0
        code.append(f"    li $v0, {valor}")

    def visitExpressaoNum(self, e):
        pass

    def visitExpressaoVardecl(self, e):
        e.varDecl.accept(self)

    def visitstring(self, s):
        pass

    def visittipo(self, t):
        pass

    def visittipodecl(self, t):
        pass

    def visittipodecltipo(self, t):
        pass

    # ---------------- Atribuicao ----------------

    def visitExpressaoAssign(self, e):
        e.assign.accept(self)

    def visitAssignAssign(self, assign):
        code = self.getList()
        assign.exp.accept(self)
        bind = st.getBindable(assign.id)
        if bind is None:
            if st.getScope() == st.SCOPE_MAIN:
                self.data.add((assign.id, getAssemblyType()))
            else:
                st.addVar(assign.id, getAssemblyType())
                code.append("    addi $sp, $sp, -4")
            bind = st.getBindable(assign.id)
        if st.getScope(assign.id) == st.SCOPE_MAIN:
            code.append(f"    sw $v0, {assign.id}($zero)")
        else:
            code.append(f"    sw $v0, {bind[st.OFFSET]}($fp)")

    def visitNoAssign(self, e):
        pass

    # ---------------- Chamada de funcao ----------------

    def visitExpressaoCall(self, e):
        code = self.getList()
        code.append("    addi $sp, $sp, -8")
        st.addSP(-8)
        oldSP = st.getSP()
        code.append("    sw $ra, 0($sp)")
        code.append("    sw $fp, 4($sp)")
        e.call.accept(self)
        code.append("    lw $fp, 4($sp)")
        code.append("    lw $ra, 0($sp)")
        code.append("    addi $sp, $sp, 8")
        st.addSP(oldSP - st.getSP())
        st.addSP(8)

    def visitParamsCall(self, paramsCall):
        code = self.getList()
        paramsCall.params.accept(self)
        code.append(f"    jal {paramsCall.id}")

    def visitNoParamsCall(self, noParamsCall):
        code = self.getList()
        code.append(f"    jal {noParamsCall.id}")

    def visitSingleParams(self, params):
        code = self.getList()
        params.exp.accept(self)
        st.addSP(-4)
        code.append(f"    sw $v0, {st.getSP()}($fp)")

    def visitCompoundParams(self, params):
        code = self.getList()
        params.exp.accept(self)
        st.addSP(-4)
        code.append(f"    sw $v0, {st.getSP()}($fp)")
        params.params.accept(self)

    def visitSingleListexp(self, l):
        pass

    def visitCompoundListexp(self, l):
        pass

    # ---------------- Stubs de classes-base abstratas ----------------

    def visitVarDecl(self, x):
        pass

    def visitFuncDecl(self, x):
        pass

    def visitSignature(self, x):
        pass

    def visitFuncParametros(self, x):
        pass

    def visitBody(self, x):
        pass

    def visitBodyComando(self, x):
        pass

    def visitComando(self, x):
        pass

    def visitExpressao(self, x):
        pass

    def visitCall(self, x):
        pass

    def visitParams(self, x):
        pass

    def visitAssign(self, x):
        pass

    # ---------------- Geracao final do codigo ----------------

    def get_code(self):
        finalcode = []
        if self.data:
            for nome, tipo in self.data:
                finalcode.insert(0, f"    {nome}: {tipo} 0")
            finalcode.insert(0, ".data")
        finalcode = finalcode + self.text
        finalcode.append("    j end")
        finalcode = finalcode + self.funcs
        finalcode.append("\nend:\n    li $v0, 10\n    syscall")
        return "\n".join(finalcode)


def main():
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            codigo_fonte = f.read()
    else:
        codigo_fonte = '''
        function soma (a: number, b: number): number {
            return a + b;
        }
        '''
    lexer.input(codigo_fonte)
    parser = yacc.yacc()
    resultado = parser.parse(debug=False)
    print("# Gera Assembly")
    assemblyvisitor = AssemblyVisitor()
    resultado.accept(assemblyvisitor)
    print(assemblyvisitor.get_code())


if __name__ == "__main__":
    main()
