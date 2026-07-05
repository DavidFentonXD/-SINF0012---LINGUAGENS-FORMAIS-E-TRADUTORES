import os

from ExpressionLanguageSint import lexer, parser
import AssemblyST as st
from AssemblyVisitor import AssemblyVisitor
from SemanticVisitor import SemanticVisitor

# teste_erro_semantico.ts contem erros de tipo de proposito, so pra mostrar
# que a analise semantica detecta os problemas (mesmo assim ele ainda gera
# assembly normalmente).
TESTES = [
    "teste_call.ts",
    "teste_for.ts",
    "teste_if.ts",
    "teste_while.ts",
    "teste_erro_semantico.ts",
]


def roda_teste(caminho):
    print("=" * 60)
    print(f"# Teste: {caminho}")
    print("=" * 60)

    if not os.path.exists(caminho):
        print(f"[arquivo nao encontrado: {caminho}]\n")
        return

    with open(caminho, "r", encoding="utf-8") as f:
        codigo_fonte = f.read()

    st.reset()

    lexer.input(codigo_fonte)
    resultado = parser.parse(lexer=lexer, debug=False)

    if resultado is None:
        print("[erro de sintaxe -- nao foi possivel analisar este teste]\n")
        return

    print("--- Analise Semantica ---")
    st.reset()
    svisitor = SemanticVisitor()
    resultado.accept(svisitor)
    print(f"Foram encontrados {svisitor.getnerros()} erro(s) semantico(s)")

    print("\n--- Assembly (MIPS) ---")
    st.reset()
    avisitor = AssemblyVisitor()
    resultado.accept(avisitor)
    print(avisitor.get_code())
    print()


def main():
    for nome in TESTES:
        roda_teste(nome)


if __name__ == "__main__":
    main()
