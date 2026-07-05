# GLC da Linguagem de Programação TypeScript

Terminais são representados pelos elementos cuja grafia está em maiúsculo, bem como pelos símbolos que estão entre aspas duplas (`"`).

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

tipofunc → FUNCTION
         | CONST

funcparametros → ID ":" tipo
               | ID ":" tipo "," funcparametros

body → "{" comandos "}"

comandos → comando
         | comando comandos

comando → RETURN expressao ";"
        | expressao ";"
        | WHILE "(" expressao ")" bodyorcomando
        | IF "(" expressao ")" bodyorcomando
        | IF "(" expressao ")" bodyorcomando ELSE bodyorcomando
        | FOR "(" opexp ";" opexp ";" opexp ")" bodyorcomando
        | vardecl ";"

bodyorcomando → body
              | comando

opexp → expressao
      | VOID

vardecl → tipodecl ID ":" tipo
        | tipodecl ID ":" tipo "=" expressao
        | tipodecl ID ":" tipo "[" "]" "=" "[" "]"
        | tipodecl ID ":" tipo "[" "]" "=" "[" listexp "]"

tipodecl → LET
         | VAR
         | CONST

tipo → STRING
     | NUMBER
     | BOOLEAN

listexp → expressao
        | expressao "," listexp

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

call → ID "(" parametros ")"
     | ID "(" ")"

parametros → expressao
           | expressao "," parametros

assign → ID "=" expressao

string → STRINGD
       | STRINGS
```
