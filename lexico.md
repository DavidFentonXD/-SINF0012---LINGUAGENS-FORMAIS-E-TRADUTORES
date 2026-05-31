# ✨ Linguagem TypeScript — Elementos Léxicos

TypeScript é uma linguagem de programação de tipagem estática compilada para JavaScript. É uma extensão do JavaScript que adiciona tipos ao código, prevenindo erros e facilitando o desenvolvimento. Criada pela Microsoft e tornada open-source em 2012, tornou-se amplamente adotada para escrita de código mais confiável e de fácil manutenção.

A seguir, destacamos seus elementos léxicos.

---

#### 1. Palavras Reservadas

TypeScript apresenta as seguintes palavras reservadas:

| Palavra | Descrição |
|---|---|
| `if` | Testa uma condição |
| `else` | Cláusula alternativa do if |
| `for` | Inicia um laço for |
| `while` | Inicia um laço while |
| `do` | Inicia um laço do-while |
| `return` | Retorna um valor de uma função |
| `let` | Declara uma variável |
| `const` | Declara uma constante |
| `function` | Declara uma função |
| `true` | Literal booleano verdadeiro |
| `false` | Literal booleano falso |
| `null` | Representa ausência de valor |

---

#### 2. Operadores

TypeScript apresenta operadores aritméticos de **soma (`+`)**, **subtração (`-`)**, **multiplicação (`*`)**, **divisão (`/`)**, **módulo (`%`)** e **exponenciação (`**`)**. Também apresenta o operador `=` para atribuições simples, além das versões compostas `+=`, `-=`, `*=`, `/=` e `%=`. Para comparação, apresenta os operadores `==`, `===`, `!=`, `!==`, `<`, `>`, `<=` e `>=`. Por fim, apresenta os operadores lógicos `&&`, `||` e `!`.

TypeScript possui a seguinte tabela de precedência, apresentada na ordem crescente de precedência:

| Grau de Precedência | Operador | Associatividade |
|---|---|---|
| 1 | `= += -= *= /= %=` | Direita para Esquerda |
| 2 | `\|\|` | Esquerda para Direita |
| 3 | `&&` | Esquerda para Direita |
| 4 | `== != === !==` | Esquerda para Direita |
| 5 | `< <= > >=` | Esquerda para Direita |
| 6 | `+ -` | Esquerda para Direita |
| 7 | `* / %` | Esquerda para Direita |
| 8 | `**` | Direita para Esquerda |
| 9 | `! ++ --` (prefixo) | Direita para Esquerda |
| 10 | `++ --` (posfixo) | Esquerda para Direita |
| 11 | `()` | Esquerda para Direita |

---

#### 3. Delimitadores

Comandos em TypeScript utilizam **`;`** como delimitador de fim de instrução. Parâmetros de funções utilizam **`,`** como separador. O símbolo **`:`** é usado para indicar o tipo de uma variável ou parâmetro. TypeScript utiliza **`( )`** para expressões e chamadas de função, **`{ }`** para blocos de comandos e **`[ ]`** para listas e índices. O símbolo **`.`** é utilizado para acesso a propriedades.

---

#### 4. Identificadores

Para identificadores, TypeScript apresenta regra bastante empregada em diferentes linguagens de programação. TypeScript aceita como identificador válido qualquer sequência de símbolos iniciada por **letras**, **`_`** ou **`$`**. Após esse símbolo inicial, o identificador pode conter **letras**, **`_`**, **`$`** e **números**. Identificadores são sensíveis a maiúsculas e minúsculas e não podem ser palavras reservadas da linguagem.

Abaixo, alguns exemplos de identificadores válidos:

    _variavel
    nome13
    somar_4_vezes
    $valor

---

#### 5. Literais

TypeScript dá suporte a literais inteiros decimais e hexadecimais, literais de ponto flutuante (com suporte a notação científica), literais booleanos (`true` e `false`) e literais de string com aspas simples, aspas duplas ou template literals com acento grave.

    let idade = 30;           // inteiro decimal
    let cor = 0xff0000;       // inteiro hexadecimal
    let preco = 19.99;        // ponto flutuante
    let distancia = 1.23e6;   // notação científica
    let ativo = true;         // booleano
    let nome = "David";       // string com aspas duplas
    let cidade = 'São Paulo'; // string com aspas simples

---

#### 6. Comentários

TypeScript suporta comentários de linha única e de múltiplas linhas. Comentários são ignorados pelo compilador e não afetam a execução do código.

Comentário de linha única:

    // Este é um comentário de linha única

Comentário de múltiplas linhas:

    /*
       Este é um
       comentário de múltiplas linhas
    */

---

#### 7. Erros Léxicos

Qualquer símbolo ou sequência que não se enquadre em nenhum dos itens apresentados é considerado erro léxico. Exemplos:

- Identificador iniciado com número: `1nome`
- Uso de caracteres especiais não permitidos: `nome@`, `meu#var`
- String não fechada: `"texto sem fechar`
- Símbolo desconhecido na linguagem: `@`, `#`

Adicionalmente, TypeScript ignora espaços em branco e tabulações. As quebras de linha são utilizadas para informar ao léxico em que ponto ele se encontra no processo de análise, informação recuperada através da variável `lineno`.
