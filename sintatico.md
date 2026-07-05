# 📐 Documentação Sintática da Linguagem TypeScript

## 1. Elementos Sintáticos

Um programa em TypeScript é composto por uma ou mais declarações de função ou blocos de comandos. Uma função TypeScript apresenta a seguinte sintaxe:

```
programa → funcdecl
         | funcdecl programa
         | comandos
         | comandos programa

funcdecl → signature
         | signatureproto body

signature → tipofunc ID "(" funcparametros ")" ":" tipo body
          | tipofunc ID "(" ")" ":" tipo body

signatureproto → tipofunc ID "(" funcparametros ")" ":" tipo ";"
               | tipofunc ID "(" ")" ":" tipo ";"

tipofunc → FUNCTION | CONST

funcparametros → ID ":" tipo
               | ID ":" tipo "," funcparametros

body → "{" comandos "}"
```

Onde `tipofunc` indica se a declaração é uma `function` ou `const`. O `ID` seguinte representa o nome da função. `funcparametros` lista os parâmetros com seus tipos — quando a função não recebe parâmetros, os parênteses aparecem vazios (`( )`), sem passar por `funcparametros`. O `tipo` indica o tipo de retorno. Uma função pode vir com o corpo já embutido em `signature` (`funcdecl → signature`), ou como um protótipo terminado em `;` (`signatureproto`) seguido de um `body` separado.

---

## 1.1 Comandos

Com relação aos comandos aceitos, TypeScript lida com declarações de variáveis, comandos de expressão, o comando de repetição `while`, o comando condicional `if`/`else`, o comando `for` e o comando `return`, conforme apresentado nas seguintes regras:

```
comandos → comando
         | comando comandos

comando → vardecl ";"
        | expressao ";"
        | RETURN expressao ";"
        | WHILE "(" expressao ")" bodyorcomando
        | IF "(" expressao ")" bodyorcomando
        | IF "(" expressao ")" bodyorcomando ELSE bodyorcomando
        | FOR "(" opexp ";" opexp ";" opexp ")" bodyorcomando

bodyorcomando → body | comando

opexp → expressao | VOID
```

O comando `while` inicia com a palavra reservada `while`, seguido por uma expressão entre parênteses e um `bodyorcomando`. O comando `if` funciona de forma similar, com suporte opcional à cláusula `else`. O comando `for` aceita três expressões opcionais separadas por `;`. O comando `return` retorna uma expressão e termina com `;`.

---

## 1.2 Declarações de Variáveis

TypeScript suporta declarações de variáveis utilizando `let`, `var` e `const`, todas acompanhadas obrigatoriamente de um tipo explícito. No caso de `const`, a variável deve ser inicializada no momento da declaração, pois seu valor não poderá ser reatribuído posteriormente.

A produção `tipodecl` representa apenas o modificador da declaração (`LET`, `VAR` ou `CONST`), enquanto o tipo é informado posteriormente pela produção `tipo`.
---

## 1.3 Expressões

TypeScript dá suporte a expressões aritméticas, relacionais, lógicas, chamadas de função (`call`), atribuição (`assign`), literais numéricos, booleanos, strings e identificadores. A sintaxe das expressões é apresentada pela seguinte regra:

```
expressao → expressao "+" expressao
          | expressao "-" expressao
          | expressao "*" expressao
          | expressao "/" expressao
          | expressao "%" expressao
          | expressao "**" expressao
          | expressao "++"
          | expressao "--"
          | expressao "+=" expressao
          | expressao "-=" expressao
          | expressao "*=" expressao
          | expressao "/=" expressao
          | expressao "%=" expressao
          | expressao "==" expressao
          | expressao "!=" expressao
          | expressao "===" expressao
          | expressao "!==" expressao
          | expressao "<" expressao
          | expressao ">" expressao
          | expressao "<=" expressao
          | expressao ">=" expressao
          | expressao "&&" expressao
          | expressao "||" expressao
          | "!" expressao
          | expressao "?" expressao ":" expressao
          | call
          | assign
          | vardecl
          | NINT
          | NFLOAT
          | string
          | TRUE
          | FALSE
          | ID
```

### 1.3.1 Chamadas de Função e Atribuição

TypeScript dá suporte a chamadas de função com e sem parâmetros. Um parâmetro pode ser qualquer expressão. Adicionalmente, TypeScript permite atribuir valores a variáveis:

```
call → ID "(" parametros ")"
     | ID "(" ")"

parametros → expressao
           | expressao "," parametros

assign → ID "=" expressao

string → STRINGD | STRINGS
```

---

## 2. Exemplos de Código

**Exemplo 1 — múltiplas funções com chamadas aninhadas:**

```typescript
function sumparabola(a: number, b: number, c: number): number {
    return a + b + c;
}

function some(a: number, b: number): number {
    a = 88 + 44;
    b = 70;
    sumparabola(1, 2, 3);
    if (b == 70) {
        while (true) {
            c = 38;
            sumparabola(5, true, false);
            while (c) {
                sumparabola(5, true, true);
            }
        }
    }
    soma();
    sumparabolac(2);
    return true;
}
```

**Exemplo 2 — declarações no nível de programa:**

```typescript
let a: number = 1;
let nome: string = "TypeScript";
let ativo: boolean = true;
```

> Nota: no nível de `programa`, comandos soltos (`comandos`) não têm chaves em volta — as chaves `{ }` só existem como parte de `body`, ou seja, dentro do corpo de uma função. Um bloco `{ ... }` sozinho fora de uma função não é reconhecido pela gramática atual.

**Exemplo 3 — comando `for` com incremento:**

```typescript
function soma(a: number, b: number): number {
    for (let i: number = 0; i < b; i++) {
        a = a + 1;
    }
    return a;
}
```

**Exemplo 4 — operador ternário e `if`/`else`:**

```typescript
function maximo(a: number, b: number): number {
    let resultado: number = a > b ? a : b;
    return resultado;
}
```
