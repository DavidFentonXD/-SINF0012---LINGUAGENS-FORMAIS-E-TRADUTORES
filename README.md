# Linguagem de Programação: TypeScript — Elementos Léxicos

---

## 1. Introdução

TypeScript é uma linguagem de programação de tipos estáticos compilada para JavaScript. É uma extensão do JavaScript que adiciona tipagem estática ao código, prevenindo erros e facilitando o desenvolvimento. Criado pela Microsoft e tornado open-source em 2012, tornou-se amplamente adotado por possibilitar a escrita de código mais confiável e de fácil manutenção.

---

## 2. Palavras Reservadas

As palavras reservadas têm significado especial na linguagem e não podem ser utilizadas como identificadores.

### Controle de fluxo

| Palavra    | Descrição                                  |
|------------|--------------------------------------------|
| `if`       | Testa uma condição                         |
| `else`     | Cláusula alternativa do if                 |
| `for`      | Inicia um laço for                         |
| `while`    | Inicia um laço while                       |
| `do`       | Inicia um laço do-while                    |
| `switch`   | Executa ações com base em uma variável     |
| `case`     | Caso dentro de um switch                   |
| `break`    | Sai de um laço                             |
| `continue` | Pula para a próxima iteração de um laço    |
| `return`   | Retorna um valor de uma função             |
| `default`  | Caso padrão em um switch                   |

### Declarações

| Palavra      | Descrição                        |
|--------------|----------------------------------|
| `let`        | Declara uma variável             |
| `const`      | Declara uma constante            |
| `function`   | Declara uma função               |
| `class`      | Define uma classe                |
| `interface`  | Define uma interface             |
| `enum`       | Define um tipo enumerado         |
| `type`       | Define um alias de tipo          |

### Modificadores de acesso e outros

| Palavra        | Descrição                              |
|----------------|----------------------------------------|
| `public`       | Acesso público                         |
| `private`      | Acesso privado                         |
| `protected`    | Acesso protegido                       |
| `static`       | Membro estático da classe              |
| `readonly`     | Propriedade somente leitura            |
| `extends`      | Estende uma classe                     |
| `implements`   | Implementa uma interface               |
| `new`          | Cria uma nova instância de uma classe  |
| `this`         | Acessa o objeto atual                  |
| `super`        | Acessa a classe pai                    |

### Tipos primitivos

| Palavra       | Descrição                                    |
|---------------|----------------------------------------------|
| `number`      | Tipo numérico                                |
| `string`      | Tipo texto                                   |
| `boolean`     | Tipo lógico (true/false)                     |
| `any`         | Qualquer tipo (sem verificação)              |
| `void`        | Ausência de valor de retorno                 |
| `null`        | Representa ausência de valor                 |
| `undefined`   | Variável não inicializada                    |
| `never`       | Tipo para funções que nunca retornam         |
| `symbol`      | Tipo símbolo único                           |
| `true`        | Literal booleano verdadeiro                  |
| `false`       | Literal booleano falso                       |

---

## 3. Operadores

### Aritméticos

| Operador | Descrição                    |
|----------|------------------------------|
| `+`      | Soma                         |
| `-`      | Subtração                    |
| `*`      | Multiplicação                |
| `/`      | Divisão                      |
| `%`      | Módulo (resto da divisão)    |
| `++`     | Incremento                   |
| `--`     | Decremento                   |

### Relacionais

| Operador | Descrição                          |
|----------|------------------------------------|
| `==`     | Igualdade                          |
| `!=`     | Diferente                          |
| `===`    | Igualdade estrita (valor e tipo)   |
| `!==`    | Diferença estrita                  |
| `<`      | Menor que                          |
| `>`      | Maior que                          |
| `<=`     | Menor ou igual                     |
| `>=`     | Maior ou igual                     |

### Atribuição

| Operador | Descrição                        |
|----------|----------------------------------|
| `=`      | Atribuição simples               |
| `+=`     | Atribuição com soma              |
| `-=`     | Atribuição com subtração         |
| `*=`     | Atribuição com multiplicação     |
| `/=`     | Atribuição com divisão           |
| `%=`     | Atribuição com módulo            |

### Lógicos

| Operador | Descrição              |
|----------|------------------------|
| `&&`     | E lógico (AND)         |
| `\|\|`   | OU lógico (OR)         |
| `!`      | NÃO lógico (NOT)       |
| `?:`     | Operador ternário      |

---

## 4. Delimitadores

| Símbolo | Uso                                  |
|---------|--------------------------------------|
| `;`     | Fim de comando                       |
| `,`     | Separação de parâmetros              |
| `:`     | Tipagem                              |
| `( )`   | Expressões e chamadas de funções     |
| `{ }`   | Blocos de comandos                   |
| `[ ]`   | Listas e arrays                      |
| `.`     | Acesso a propriedades                |
| `?`     | Propriedade ou parâmetro opcional    |

---

## 5. Identificadores

Identificadores são nomes dados a variáveis, funções, classes e outros elementos. Regras:

- O primeiro caractere deve ser uma letra, sublinhado (`_`) ou cifrão (`$`).
- Os caracteres seguintes podem ser letras, números, sublinhados ou cifrões.
- Não podem ser palavras reservadas da linguagem.
- São sensíveis a maiúsculas e minúsculas (case-sensitive).
- Devem ter nomes significativos e descritivos.

**Exemplos válidos:**
```ts
_variavel
nome13
somar_4_vezes
$valor
```

**Exemplos inválidos:**
```ts
1variavel    // inicia com número
meu-nome     // contém hífen
let          // palavra reservada
```

---

## 6. Literais

### 6.1 Literais Numéricos

```ts
let idade = 30;           // inteiro decimal
let cor = 0xff0000;       // inteiro hexadecimal
let preco = 19.99;        // ponto flutuante
let distancia = 1.23e6;   // notação científica
```

### 6.2 Literais Booleanos

```ts
let ativo = true;
let inativo = false;
```

### 6.3 Literais de String

```ts
let nome = "David";
let cidade = 'São Paulo';
let mensagem = `Olá, ${nome}!`;
```

### 6.4 Sequências de Escape

| Escape | Descrição        |
|--------|------------------|
| `\n`   | Nova linha       |
| `\t`   | Tabulação        |
| `\'`   | Aspas simples    |
| `\"`   | Aspas duplas     |
| `\\`   | Barra invertida  |

---

## 7. Comentários

**Comentário de linha:**
```ts
// Este é um comentário de linha única
```

**Comentário de bloco:**
```ts
/*
   Este é um
   comentário de múltiplas linhas
*/
```

---

## 8. Ordem de Precedência dos Operadores

Operadores com maior nível são avaliados primeiro. Use parênteses para alterar a ordem.

| Nível      | Operadores           | Descrição                                    |
|------------|----------------------|----------------------------------------------|
| 1 (maior)  | `( )`                | Agrupamento / chamada de função              |
| 2          | `++ --`              | Incremento e decremento (pós-fixo)           |
| 3          | `! ~ ++ --`          | NOT lógico, NOT bitwise, inc/dec (pré-fixo)  |
| 4          | `* / %`              | Multiplicação, divisão e módulo              |
| 5          | `+ -`                | Adição e subtração                           |
| 6          | `<< >> >>>`          | Deslocamento de bits                         |
| 7          | `< <= > >=`          | Relacionais (comparação)                     |
| 8          | `== != === !==`      | Igualdade e diferença                        |
| 9          | `&`                  | AND bitwise                                  |
| 10         | `^`                  | XOR bitwise                                  |
| 11         | `\|`                 | OR bitwise                                   |
| 12         | `&&`                 | AND lógico                                   |
| 13         | `\|\|`               | OR lógico                                    |
| 14         | `?:`                 | Operador ternário                            |
| 15 (menor) | `= += -= *= /= %=`   | Atribuição                                   |

**Exemplos:**
```ts
2 + 3 * 4             // resultado: 14  (* antes de +)
(2 + 3) * 4           // resultado: 20  (parênteses primeiro)
true || false && false // resultado: true  (&& antes de ||)
```

---

## 9. Erros Léxicos

Qualquer símbolo ou sequência que não se enquadre nas regras léxicas é considerado erro léxico. Exemplos:

- Identificador iniciado com número: `1nome`
- Uso de caracteres especiais não permitidos: `nome@`, `meu#var`
- String não fechada: `"texto sem fechar`
- Símbolo desconhecido na linguagem: `@`, `#`

---

*Referência: https://www.typescriptlang.org/pt/*
