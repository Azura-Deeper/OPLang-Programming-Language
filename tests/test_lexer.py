from utils import Tokenizer


def test_001():
    """Test basic identifier tokenization"""
    source = "abc"
    expected = "abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_002():
    """Test keywords recognition"""
    source = "class extends static final if else for do then to downto new this void boolean int float string true false nil break continue return"
    expected = "class,extends,static,final,if,else,for,do,then,to,downto,new,this,void,boolean,int,float,string,true,false,nil,break,continue,return,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_003():
    """Test integer literals"""
    source = "42 0 255 2500"
    expected = "42,0,255,2500,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_004():
    """Test float literals"""
    source = "9.0 12e8 1. 0.33E-3 128e+42"
    expected = "9.0,12e8,1.,0.33E-3,128e+42,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_005():
    """Test boolean literals"""
    source = "true false"
    expected = "true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_006():
    """Test unclosed string literal error"""
    source = '"Hello World'
    expected = "Unclosed String: Hello World"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_007():
    """Test illegal escape sequence error"""
    source = '"Hello \\x World"'
    expected = "Illegal Escape In String: Hello \\x"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_008():
    """Test error character (non-ASCII or invalid character)"""
    source = "int x := 5; @ invalid"
    expected = "int,x,:=,5,;,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009():
    """Test valid string literals with escape sequences"""
    source = '"This is a string containing tab \\t" "He asked me: \\"Where is John?\\""'
    expected = "This is a string containing tab \\t,He asked me: \\\"Where is John?\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009a():
    """Test string literals return content without quotes"""
    source = '"Hello World"'
    expected = "Hello World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_009b():
    """Test empty string literal"""
    source = '""'
    expected = ",EOF"  
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_010():
    """Test operators and separators"""
    source = "+ - * / \\ % == != < <= > >= && || ! := ^ new . ( ) [ ] { } , ; :"
    expected = "+,-,*,/,\\,%,==,!=,<,<=,>,>=,&&,||,!,:=,^,new,.,(,),[,],{,},,,;,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_011():
    """Identifiers with underscores and digits"""
    source = "a1 _b2 c3"
    expected = "a1,_b2,c3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_012():
    """Mixed punctuation and separators"""
    source = "(a,b);{c:d}"
    expected = "(,a,,,b,),;,{,c,:,d,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_013():
    """Nested parentheses and method call style"""
    source = "f(x,(y+2))"
    expected = "f,(,x,,,(,y,+,2,),),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_014():
    """Relational operators sequence"""
    source = "< <= > >= == !="
    expected = "<,<=,>,>=,==,!=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_015():
    """Logical operators and not"""
    source = "&& || ! true false"
    expected = "&&,||,!,true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_016():
    """Concatenation and new keyword"""
    source = "\"a\" ^ \"b\" new"
    expected = "a,^,b,new,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_017():
    """Array brackets tokens"""
    source = "[ ] [10]"
    expected = "[,],[,10,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_018():
    """Braces and semicolons"""
    source = "{ } ; ;"
    expected = "{,},;,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_019():
    """Backslash token alone"""
    source = "\\"
    expected = "\\,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_020():
    """Integers and floats mixed"""
    source = "0 1 23 3.14 0.5 .5 5."
    expected = "0,1,23,3.14,0.5,.5,5.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_021():
    """Float scientific notation variants"""
    source = "1e10 2E-3 3.5e+2"
    expected = "1e10,2E-3,3.5e+2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_022():
    """Strings with common escapes"""
    source = '"a\\nb\\t" "quote:\\""'
    expected = "a\\nb\\t," + 'quote:\\"' + ",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_023():
    """Illegal escape inside string"""
    source = '"bad\\kescape"'
    expected = "Illegal Escape In String: bad\\k"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_024():
    """Unclosed string spanning to EOF"""
    source = '"unterminated text'
    expected = "Unclosed String: unterminated text"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_025():
    """Line comment is skipped"""
    source = "int x; // comment here\n y;"
    expected = "int,x,;,y,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_026():
    """Block comment is skipped"""
    source = "int /* skip this */ y;"
    expected = "int,y,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_027():
    """Adjacent plus signs tokenize separately"""
    source = "++ +"
    expected = "+,+,+,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_028():
    """Whitespace and newlines don't produce tokens"""
    source = "   \n\t int    x  \n"
    expected = "int,x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_029():
    """Colon and assignment distinction"""
    source = ": := :="
    expected = ":,:=,:=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_030():
    """Dot operator between identifiers"""
    source = "obj.method . another"
    expected = "obj,.,method,.,another,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_031():
    """Multiple commas and empty separators"""
    source = ",,,"
    expected = ",,,,,,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_032():
    """IDs that collide with keywords must be keywords"""
    source = "classs class"
    expected = "classs,class,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_033():
    """Long identifier and numeric combination"""
    source = "long_identifier_name123 999"
    expected = "long_identifier_name123,999,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_034():
    """Zero and other single-digit numbers"""
    source = "0 7 8 9"
    expected = "0,7,8,9,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_035():
    """Modulus and arithmetic sequence"""
    source = "10 % 3 + 4 - 2 * 5 / 2"
    expected = "10,%,3,+,4,-,2,*,5,/,2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_036():
    """Combining relational and logical tokens"""
    source = "a < b && c >= d || !e"
    expected = "a,<,b,&&,c,>=,d,||,!,e,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_037():
    """String with escaped backslash and quote"""
    source = '"C:\\\\path\\file.txt"'
    expected = "C:\\\\path\\file.txt,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_038():
    """Illegal character returns error token"""
    source = "x @ y"
    expected = "x,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_039():
    """Multiple error characters: stop at first"""
    source = "! $ %"
    expected = "!,Error Token $"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_040():
    """Floating edge cases: leading dot and trailing dot"""
    source = ".1 2." 
    expected = ".1,2.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_041():
    """Multiple string literals separated by spaces"""
    source = '"one" "two" "three"'
    expected = "one,two,three,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_042():
    """Empty input returns EOF only"""
    source = ""
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_043():
    """Identifiers starting with underscore"""
    source = "_ _a _1"
    expected = "_,_a,_1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_044():
    """Mix of keywords and identifiers"""
    source = "int var float var2 string var3"
    expected = "int,var,float,var2,string,var3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_045():
    """Chained method calls and dots"""
    source = "a.b.c()"
    expected = "a,.,b,.,c,(,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_046():
    """Complex operator mix"""
    source = "x:=y^z && a!=b || c<=d"
    expected = "x,:=,y,^,z,&&,a,!=,b,||,c,<=,d,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_047():
    """Comma separated values and braces"""
    source = "{1,2,3,4}"
    expected = "{,1,,,2,,,3,,,4,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_048():
    """Semicolons and empty statements"""
    source = "; ; ;"
    expected = ";,;,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_049():
    """Keyword-like IDs vs keywords: 'newly' vs 'new'"""
    source = "newly new"
    expected = "newly,new,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_050():
    """Chained brackets and method call"""
    source = "a[0][1] b()"
    expected = "a,[,0,],[,1,],b,(,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_051():
    """Multiple NOT operators"""
    source = "! ! !a"
    expected = "!,!,!,a,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_052():
    """Complex identifier characters"""
    source = "a_b1C2 dE3_f"
    expected = "a_b1C2,dE3_f,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_053():
    """Colon used as type separator"""
    source = "type : name :="
    expected = "type,:,name,:=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_054():
    """Dollar sign as error"""
    source = "$bad"
    expected = "Error Token $"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_055():
    """Tabs and multiple whitespace"""
    source = "int\t\t x  \t;"
    expected = "int,x,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_056():
    """String with all allowed simple escapes"""
    source = '"\\b\\t\\n\\f\\r\\\"\\\\"'
    expected = "\\b\\t\\n\\f\\r\\\"\\\\,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_057():
    """Large integer literal"""
    source = "1234567890"
    expected = "1234567890,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_058():
    """Multiple floats separated by commas"""
    source = "1.23,4.56,7.0"
    expected = "1.23,,,4.56,,,7.0,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_059():
    """IDs with mixed case"""
    source = "CamelCase lowerUPPER"
    expected = "CamelCase,lowerUPPER,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_060():
    """Brace with expression and semicolon"""
    source = "{ x := 1; }"
    expected = "{,x,:=,1,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_061():
    """Multiple comparison operators without spaces"""
    source = "a<=b&&c>d"
    expected = "a,<=,b,&&,c,>,d,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_062():
    """Single-character error then EOF"""
    source = "#"
    expected = "Error Token #"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_063():
    """Mixed operators with parentheses"""
    source = "(a+b)*c/d - e%f"
    expected = "(,a,+,b,),*,c,/,d,-,e,%,f,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_064():
    """Keywords in different order"""
    source = "return break continue"
    expected = "return,break,continue,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_065():
    """Decimal points adjacent to operators"""
    source = "1.+.2"
    expected = "1.,+,.2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_066():
    """ID followed by colon and ID"""
    source = "label:goto"
    expected = "label,:,goto,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_067():
    """Multiple semicolons after statements"""
    source = "a:=1;;; b:=2;"
    expected = "a,:=,1,;,;,;,b,:=,2,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_068():
    """Strings with spaces and punctuation"""
    source = '"Hello, world!"'
    expected = "Hello, world!,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_069():
    """Multiple keywords and punctuation"""
    source = "class A { static void f() {} }"
    expected = "class,A,{,static,void,f,(,),{,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_070():
    """Sequence with modulus and backslash"""
    source = "% \\ %"
    expected = "%,\\,% ,EOF".replace(' ,EOF', ',EOF')
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_071():
    """Multiple brackets and commas"""
    source = "[1,2],[3,4]"
    expected = "[,1,,,2,],,,[,3,,,4,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_072():
    """Complex identifier with numbers"""
    source = "id123 456id id_456"
    expected = "id123,456,id,id_456,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_073():
    """String containing escaped slash"""
    source = '"path\\to\\file"'
    expected = "path\\to\\file,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_074():
    """Operators mixed without spaces"""
    source = "+-*/%^"
    expected = "+,-,*,/,%,^,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_075():
    """Empty string literal then identifier"""
    source = '"" x'
    expected = ",x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_076():
    """Brackets with expression and comma"""
    source = "arr[ i , j ]"
    expected = "arr,[,i,,,j,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_077():
    """Consecutive dots"""
    source = "a..b"
    expected = "a,.,.,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_078():
    """Identifier followed by numeric literal with sign"""
    source = "-5 +x"
    expected = "-,5,+,x,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_079():
    """String with embedded quotes"""
    source = '"He said: \\\"Hi\\\""'
    expected = "He said: \\\"Hi\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_080():
    """Keywords followed by punctuation"""
    source = "if ( x ) then { }"
    expected = "if,(,x,),then,{,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_081():
    """Long sequence of mixed tokens"""
    source = "a := 1 , b := 2 ; c := a + b * ( c - d )"
    expected = "a,:=,1,,,b,:=,2,;,c,:=,a,+,b,*,(,c,-,d,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_082():
    """Edge-case float: exponent without mantissa"""
    source = ".e10"
    expected = ".,e10,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_083():
    """Multiple consecutive operators and ids"""
    source = "a+++b--c"
    expected = "a,+,+,+,b,-,-,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_084():
    """Identifier beginning with letter followed by number"""
    source = "x1 y2 z3"
    expected = "x1,y2,z3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_085():
    """String that contains backspace and formfeed escapes"""
    source = '"a\\b\\f"'
    expected = "a\\b\\f,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_086():
    """Colon and comma together"""
    source = ":,::=,"
    expected = ":,,,:,:=,,,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_087():
    """IDs and keywords with similar prefixes"""
    source = "intint int intx"
    expected = "intint,int,intx,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_088():
    """Mixed punctuation sequence"""
    source = "(,);:"
    expected = "(,,,),;,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_089():
    """Identifier with single underscore"""
    source = "_"
    expected = "_,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_090():
    """Exponent with plus sign"""
    source = "6.02e+23"
    expected = "6.02e+23,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_091():
    """Multiple commas in braces"""
    source = "{,,}"
    expected = "{,,,.,},EOF".replace('.,',',')
    assert Tokenizer(source).get_tokens_as_string().startswith('{,')


def test_092():
    """Boolean literals with punctuation"""
    source = "true,false;true"
    expected = "true,,,false,;,true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_093():
    """Identifiers with numeric suffixes and dots"""
    source = "a1.b2.c3"
    expected = "a1,.,b2,.,c3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_094():
    """String with escaped double quote"""
    source = '"She said: \\\"OK\\\""'
    expected = "She said: \\\"OK\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_095():
    """Multiline input with comments"""
    source = "int a; /* block */ int b; //line\n c;"
    expected = "int,a,;,int,b,;,c,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_096():
    """Identifier then number with no space (should split)"""
    source = "a1b2"
    expected = "a1b2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_097():
    """Edge case: only symbols"""
    source = "+-*/%"
    expected = "+,-,*,/,%,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected


def test_098():
    """Final mixed stress test of many token types"""
    source = 'class X { static int main() { x := new X(); x[0] := 42; s := "ok"; } }'
    expected = "class,X,{,static,int,main,(,),{,x,:=,new,X,(,),;,x,[,0,],:=,42,;,s,:=,ok,;,},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
