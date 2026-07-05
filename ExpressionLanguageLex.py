import ply.lex as lex

# Analisador lexico de TypeScript (subconjunto usado na linguagem)

reserved = {
    'abstract' : 'ABSTRACT',
    'any' : 'ANY',
    'as' : 'AS',
    'asserts' : 'ASSERTS',
    'async': 'ASYNC',
    'await' : 'AWAIT',
    'boolean' : 'BOOLEAN',
    'break' : 'BREAK',
    'case' : 'CASE',
    'catch' : 'CATCH',
    'class' : 'CLASS',
    'const' : 'CONST',
    'constructor' : 'CONSTRUCTOR',
    'continue' : 'CONTINUE',
    'debugger' : 'DEBUGGER',
    'declare' : 'DECLARE',
    'default' : 'DEFAULT',
    'delete' : 'DELETE',
    'do' : 'DO',
    'else' : 'ELSE',
    'enum' : 'ENUM',
    'export' : 'EXPORT',
    'extends' : 'EXTENDS',
    'false' : 'FALSE',
    'finally' : 'FINALLY',
    'for' : 'FOR',
    'from' : 'FROM',
    'function' : 'FUNCTION',
    'get' : 'GET',
    'global' : 'GLOBAL',
    'if' : 'IF',
    'implements' : 'IMPLEMENTS',
    'import' : 'IMPORT',
    'in' : 'IN',
    'infer' : 'INFER',
    'instanceof' : 'INSTANCEOF',
    'interface' : 'INTERFACE',
    'internal' : 'INTERNAL',
    'is' : 'IS',
    'keyof' : 'KEYOF',
    'let' : 'LET',
    'module' : 'MODULE',
    'namespace' : 'NAMESPACE',
    'never' : 'NEVER',
    'new' : 'NEW',
    'null' : 'NULL',
    'number' : 'NUMBER',
    'object' : 'OBJECT',
    'of' : 'OF',
    'package' : 'PACKAGE',
    'private' : 'PRIVATE',
    'protected' : 'PROTECTED',
    'public' : 'PUBLIC',
    'readonly' : 'READONLY',
    'require' : 'REQUIRE',
    'return' : 'RETURN',
    'set' : 'SET',
    'static' : 'STATIC',
    'string' : 'STRING',
    'super' : 'SUPER',
    'switch' : 'SWITCH',
    'symbol' : 'SYMBOL',
    'this' : 'THIS',
    'throw' : 'THROW',
    'true' : 'TRUE',
    'try' : 'TRY',
    'type' : 'TYPE',
    'typeof' : 'TYPEOF',
    'undefined' : 'UNDEFINED',
    'unique' : 'UNIQUE',
    'unknown' : 'UNKNOWN',
    'var' : 'VAR',
    'void' : 'VOID',
    'while' : 'WHILE',
    'with' : 'WITH',
    'yield' : 'YIELD',
}

tokens = [
    'ID',
    'NINT',
    'NFLOAT',
    'STRINGD',
    'STRINGS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'INCREMENT',
    'EXPO',
    'INCREMENTN',
    'DECREMENT',
    'DECREMENTN',
    'TIMESINCREMENT',
    'DIVIDEINCREMENT',
    'MODINCREMENT',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'SEMICOLON',
    'COLON',
    'INTER',
    'DOT',
    'ASSIGN',
    'EQ',
    'EEQ',
    'NEQ',
    'NNEQ',
    'LT',
    'LE',
    'GT',
    'GE',
    'AND',
    'OR',
    'NOT',
    'COMMENTMULTI',
    'COMMENT',
    'OCTAL',
    'HEXADECIMAL',
    'SQUOTE',
    'DQUOTE',
    'BAR',
] + list (reserved.values())


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_INCREMENT = r'\+\+'
t_EXPO = r'\*\*'
t_DECREMENT = r'--'
t_ASSIGN = r'='
t_INCREMENTN = r'\+='
t_DECREMENTN = r'-='
t_TIMESINCREMENT = r'\*='
t_DIVIDEINCREMENT = r'/='
t_MODINCREMENT = r'%='
t_EQ = r'=='
t_EEQ = r'==='
t_NEQ = r'!='
t_NNEQ = r'!=='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_INTER = r'\?'
t_COLON = r':'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_DQUOTE = r'\"'
t_SQUOTE = r'\''
t_BAR = r'\|'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    if t.type == 'TRUE':
        t.value = True
    elif t.type == 'FALSE':
        t.value = False
    elif t.type == 'NULL':
        t.value = None
    return t


# Regras com prefixo (0x.../0o...) precisam vir antes de t_NINT, senao
# o \d+ de NINT casa so o "0" e quebra o resto do numero.
def t_HEXADECIMAL(t):
    r'0x[0-9a-fA-F]+'
    t.value = int(t.value, 16)
    return t

def t_OCTAL(t):
    r'0o[0-7]+'
    t.value = int(t.value, 8)
    return t

def t_NFLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NINT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRINGD(t):
    r'\"[^\"\n]*\"'
    t.value = t.value[1:-1]
    return t

def t_STRINGS(t):
    r'\'[^\'\n]*\''
    t.value = t.value[1:-1]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere invalido: {t.value[0]}")
    t.lexer.skip(1)

def t_COMMENT(t):
    r'//.*\n'
    pass

def t_COMMENTMULTI(t):
    r'/\*.*\*/'
    pass

def t_BRANCO(t):
    r'[\t ]+'
    pass

lexer = lex.lex()
