grammar gramatica;
root : expressions  EOF;
expressions : expr+;
expr : assign
    | printi
    | printx
    | area
    | perimeter
    | vertices
    | centroid
    | color
    | inside
    | equal
    | regular
    | draw
    | condicional
    ;

op : ide
    | llista
    | op '*' op
    | op '+' op
    | '#' op
    | '!' NUM
    | '(' op ')'
    ;

assign : ide ':=' op;
printi : 'print' op;
printx : 'print' S;
area : 'area' op;
perimeter : 'perimeter' op;
vertices : 'vertices' op;
centroid : 'centroid' op;
color : 'color' ide  ','  '{'  NUM  NUM  NUM  '}';
inside : 'inside' op ',' op;
equal : 'equal' op ',' op;
regular : 'regular' op;
draw : 'draw' S (',' op)+;

condicio : 'True'
        | 'False'
        | NUM '>' NUM
        | NUM '<' NUM
        | NUM '==' NUM
        | NUM '!=' NUM
        | NUM '>=' NUM
        | NUM '<=' NUM
        ;

condicional : 'if' condicio expressions ('elif' condicio expressions)* 'endif'
            | 'if' condicio expressions ('elif' condicio expressions)* 'else' expressions 'endif'
            ;

llista : '[' ']' | '[' point+ ']';
point : NUM  NUM;
ide : LLETRA (NUM | LLETRA | '_')*;

NUM : [0-9]+ |  [0-9]+ '.' [0-9]+ | '-' [0-9]+ | '-' [0-9]+ '.' [0-9]+;
LLETRA : [a-zA-Z]+;

S : '"' ~[\r\n"]* '"';
Comment : '//' (~('\n'|'\r'))* -> skip;
WS : [ \r\n\t]+ -> skip ;
WORD : [a-zA-Z\u0080-\u00FF]+ ;