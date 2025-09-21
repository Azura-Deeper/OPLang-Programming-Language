grammar OPLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options { language=Python3; }

program: classDecl* EOF;

classDecl: CLASS ID ( EXTENDS ID )? LB member* RB;

member: varDecl | methodDecl;

varDecl: STATIC? FINAL? type variableDeclList SEMI;
variableDeclList: variableDecl (COMMA variableDecl)*;
variableDecl: ID (LBR INTLIT RBR)? (ASSIGN expr)?;

methodDecl: STATIC? type? ID LP paramList? RP body
          | TILDE ID LP paramList? RP body
          ;
paramList: param (SEMI param)*;
param: type AMP? ID;

type: (INT | FLOAT | STRING_TYPE | BOOLEAN | VOID | ID) (LBR INTLIT RBR)? ;

body: LB stmt* RB;
stmt: varDecl
    | assignStmt SEMI
    | methodCall SEMI
    | ifStmt
    | forStmt
    | returnStmt SEMI
    | exprStmt SEMI
    | body
    ;

assignStmt: lvalue ASSIGN expr;

lvalue: ID (LBR expr RBR)?
      | ID DOT ID (LBR expr RBR)?
      | THIS DOT ID
      | THIS LBR expr RBR
      ;
methodCall: ID DOT ID LP exprList? RP
          | ID LP exprList? RP
          | THIS DOT ID LP exprList? RP
          | THIS LP exprList? RP
          ;
exprStmt: expr;
exprList: expr (COMMA expr)*;

expr: expr (AND|OR) expr                #logicalExpr
    | expr (EQ|NEQ|LT|LE|GT|GE) expr    #relationalExpr
    | expr (PLUS|MINUS) expr            #addExpr
    | expr (MUL|DIV|MOD) expr           #mulExpr
    | expr CONCAT expr                  #concatExpr
    | NOT expr                          #notExpr
    | LP expr RP                        #parenExpr
    | postfixExpr                        #atomExpr
    ;

ifStmt: IF LP expr RP THEN (body | stmt) (ELSE (body | stmt))?;
forStmt: FOR ID ASSIGN expr (TO | DOWNTO) expr DO (body | stmt);
returnStmt: RETURN expr?;

atom: INTLIT
    | FLOATLIT
    | STRING
    | TRUE
    | FALSE
    | NIL
    | ID
    | THIS
    | ID LBR expr RBR
    | THIS LBR expr RBR
    | ID LP exprList? RP
    | THIS LP exprList? RP
    | NEW ID LP exprList? RP
    | LB exprList? RB
    ;

postfixExpr
    : atom ( (DOT ID (LP exprList? RP)? ) | (LP exprList? RP) | (LBR expr RBR) )*
    ;

WS: [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BODY_COMMENT: '/*' .*? '*/' -> skip;

ANNOT: '@' [a-zA-Z_] [a-zA-Z_0-9$]* -> skip;

CLASS: 'class';
EXTENDS: 'extends';
STATIC: 'static';
VOID: 'void';
NEW: 'new';
THIS: 'this';
FINAL: 'final';
IF: 'if';
THEN: 'then';
ELSE: 'else';
FOR: 'for';
TO: 'to';
DOWNTO: 'downto';
DO: 'do';
RETURN: 'return';
TRUE: 'true';
FALSE: 'false';
NIL: 'nil';
BREAK: 'break';
CONTINUE: 'continue';
INT: 'int';
FLOAT: 'float';
STRING_TYPE: 'string';
BOOLEAN: 'boolean';

AMP: '&';
TILDE: '~';

PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
MOD: '%';
BACKSLASH: '\\';
EQ: '==';
NEQ: '!=';
LT: '<';
LE: '<=';
GT: '>';
GE: '>=';
AND: '&&';
OR: '||';
NOT: '!';
ASSIGN: ':=';
CONCAT: '^';
DOT: '.';
BITOR: '|';
LP: '(';
RP: ')';
LBR: '[';
RBR: ']';
LB: '{';
RB: '}';
COMMA: ',';
SEMI: ';';
COLON: ':';

ID: [a-zA-Z_] [a-zA-Z_0-9$]*;
INTLIT: '0' | [1-9] [0-9]*;
FLOATLIT: ([0-9]+ ('.' [0-9]*)? | '.' [0-9]+) ([eE][+-]?[0-9]+)?;

CHAR: '\'' ( ESC | ~['\\\r\n] ) '\'' { self.text = self.text[1:-1]; };

fragment ESC: '\\' [btnfr"\\];

STRING
    : '"' ( ESC | ~["\\\r\n] )* '"'
      { self.text = self.text[1:-1] ; }
    ;

ILLEGAL_ESCAPE
    : '"' ( ESC | ~["\\\r\n] )* '\\' ~[btnfr"\\] ( ~["\\\r\n] )* '"'
      {
          import re
          s = self.text[1:-1]
          m = re.search(r'\\[^btnfr"\\]', s)
          if m:
              self.text = s[:m.end()]
          else:
              self.text = s
      }
    ;

UNCLOSE_STRING
    : '"' ( ESC | ~["\\\r\n] )*  { self.text = self.text[1:] }
    ;
ERROR_CHAR: . ;
