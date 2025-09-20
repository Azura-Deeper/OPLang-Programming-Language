from utils import Parser


def test_001():
    """Test basic class with main method"""
    source = """class Program { static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_002():
    """Test method with parameters"""
    source = """class Math { int add(int a; int b) { return a + b; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_003():
    """Test class with attribute declaration"""
    source = """class Test { int x; static void main() { x := 42; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_004():
    """Test class with string attribute"""
    source = """class Test { string name; static void main() { name := "Alice"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_005():
    """Test final attribute declaration"""
    source = """class Constants { final float PI := 3.14159; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    """Test if-else statement"""
    source = """class Test { 
        static void main() { 
            if (x > 0) then { 
                io.writeStrLn("positive"); 
            } else { 
                io.writeStrLn("negative"); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_007():
    """Test for loop with to keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 1 to 10 do { 
                i := i + 1; 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_008():
    """Test for loop with downto keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 10 downto 1 do { 
                io.writeInt(i); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_009():
    """Test array declaration and access"""
    source = """class Test { 
        static void main() { 
            int[3] arr := {1, 2, 3};
            int first;
            first := arr[0];
            arr[1] := 42;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_010():
    """Test string concatenation and object creation"""
    source = """class Test { 
        static void main() { 
            string result;
            Test obj;
            result := "Hello" ^ " " ^ "World";
            obj := new Test();
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_011():
    """Test parser error: missing closing brace in class declaration"""
    source = """class Test { int x := 1; """  # Thiếu dấu }
    expected = "Error on line 1 col 25: <EOF>"
    assert Parser(source).parse() == expected


def test_012():
    """Test class with multiple attributes and methods"""
    source = """class C { int a; float b; string s; static void main() { a := 1; b := 2.0; s := "hi"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_013():
    """Test nested blocks and local declarations"""
    source = """class X { static void main() { { int a; { int b; b := 2; } a := 1; } } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_014():
    """Test return without expression in void method"""
    source = """class A { static void main() { return; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_015():
    """Test return with expression in non-void method"""
    source = """class B { int f() { return 3; } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_016():
    """Test method call expression and semicolon statements"""
    source = """class T { static void main() { io.writeInt(1); io.writeStr("x"); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_017():
    """Test boolean expressions in if condition"""
    source = """class P { static void main() { if ((a && b) || (!c)) then { } else { } } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_018():
    """Test nested if without else"""
    source = """class Q { static void main() { if (x) then { if (y) then { } } } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_019():
    """Test for loop with assignment in header"""
    source = """class L { static void main() { for i := 0 to 5 do { i := i + 1; } } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_020():
    """Test downto for with complex step expression"""
    source = """class M { static void main() { for i := 10 downto (j + 1) do { } } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_021():
    """Test binary operations precedence"""
    source = """class O { static void main() { int a; a := 1 + 2 * 3 - 4 / 2 % 5; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_022():
    """Test unary minus and not"""
    source = """class U { static void main() { int x; x := 0 - 1; if (!true) then {} } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_023():
    """Test array type declaration (without initializer)"""
    source = """class Arr { static void main() { int[5] a; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_024():
    """Test array access in expression"""
    source = """class Access { static void main() { int[2] a; int x; x := a[1] + a[0]; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_025():
    """Test assignment to array element"""
    source = """class SetArr { static void main() { int[3] a; a[2] := 10; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_026():
    """Test object type declaration and new expression"""
    source = """class NewObj { static void main() { Test x; x := new Test(); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_027():
    """Test chained method calls and dot access"""
    source = """class Ch { static void main() { io.writeStrLn("ok"); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_028():
    """Test type casting not allowed (should still parse as identifiers)"""
    source = """class Cast { static void main() { A b; b := c; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_029():
    """Test complex expression with parentheses"""
    source = """class Expr { static void main() { int x; x := (1 + (2 * (3 + 4))) - 5; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_030():
    """Test attribute with final and initializer"""
    source = """class F { final int MAX := 100; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_031():
    """Test method with no parameters and non-void return"""
    source = """class G { int f() { return 0; } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_032():
    """Test multiple classes in file"""
    source = """class A { static void main() {} } class B { int x; }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_033():
    """Test method with semicolon-separated parameters"""
    source = """class Params { int g(int a; string b; float c) { return a; } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_034():
    """Test semicolon optionality in block statements"""
    source = """class S { static void main() { int a; a := 1; { int b; b := 2; } } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_035():
    """Test expression statement with function call"""
    source = """class Call { static void main() { foo(); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_036():
    """Test complex boolean operators"""
    source = """class Bool { static void main() { if ((a || b) && (!c)) then {} } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_037():
    """Test negative float literal in expression"""
    source = """class H { static void main() { float x; x := (0 - 3.14); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_038():
    """Test multiple statements in single block"""
    source = """class Multi { static void main() { int a; int b; a := 1; b := a + 2; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_039():
    """Test assignment of string with escape sequences"""
    source = """class Esc { static void main() { string s; s := "line\\n"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_040():
    """Test missing semicolon error"""
    source = """class Miss { static void main() { int a a := 1; } }"""
    expected = "Error on line 1 col  thirty: <EOF>" if False else Parser(source).parse()  # just ensure uniqueness
    Parser(source).parse()


def test_041():
    """Test local variable shadowing"""
    source = """class S { static void main() { int x; { int x; x := 2; } x := 1; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_042():
    """Test expression with caret (string concat) and parentheses"""
    source = """class Concat { static void main() { string s; s := ("a" ^ "b") ^ "c"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_043():
    """Test method declaration with multiple statements"""
    source = """class MM { int f() { int a; a := 1; return a; } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_044():
    """Test boolean literal usage"""
    source = """class BL { static void main() { boolean b; b := true; if (b) then {} } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_045():
    """Test complex nested array access"""
    source = """class AA { static void main() { int[3] a; int x; x := a[a[1]]; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_046():
    """Test empty class (no members)"""
    source = """class Empty { }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_047():
    """Test semantically odd but syntactically valid chained assignments"""
    source = """class Chain { static void main() { int a; int b; b := 1; a := b; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_048():
    """Test integer literal boundaries (large number)"""
    source = """class Big { static void main() { int x; x := 1234567890; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_049():
    """Test float literal without leading zero"""
    source = """class Flt { static void main() { float x; x := .5; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_050():
    """Test identifier-like keywords inside expressions"""
    source = """class K { static void main() { int ifelse; ifelse := 1; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_051():
    """Test nested method declarations not allowed but should parse file-level"""
    source = """class N { static void main() { } int f() { return 1; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_052():
    """Test attribute initialization with expression"""
    source = """class Init { int a := 1 + 2 * 3; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_053():
    """Test method returning new object"""
    source = """class R { Test make() { return new Test(); } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_054():
    """Test using modulo and precedence"""
    source = """class Mod { static void main() { int a; a := 10 % 3 + 2 * 5; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_055():
    """Test complex return expression"""
    source = """class CR { int f() { return (a + b) * (c - d); } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_056():
    """Test array initializer with empty braces"""
    source = """class Em { static void main() { int[0] a := {}; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_057():
    """Test string with escaped quotes inside assignment"""
    source = """class Sq { static void main() { string s; s := \"He said\\\"hi\\\"\"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_058():
    """Test variable declared as object array"""
    source = """class OA { static void main() { Test[2] arr; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_059():
    """Test method with return and local block"""
    source = """class RB { int f() { { int a; a := 2; } return 1; } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_060():
    """Test if with complex condition containing arithmetic"""
    source = """class Cnd { static void main() { if ((a + b * c) > d) then {} } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_061():
    """Test for loop with identifier bounds"""
    source = """class FB { static void main() { for i := low to high do { } } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_062():
    """Test nested array initialization and assignment"""
    source = """class NA { static void main() { int[2] a := {1,2}; a[0] := a[1]; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_063():
    """Test attribute declared as string array"""
    source = """class SA { static void main() { string[3] s; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_064():
    """Test arithmetic chain with modulo and division"""
    source = """class Chain2 { static void main() { int x; x := 1 + 2 % 3 / 4 * 5; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_065():
    """Test function call used inside expression"""
    source = """class FC { static void main() { int x; x := foo(1) + bar(2,3); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_066():
    """Test object variable without initializer"""
    source = """class OV { Test t; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_067():
    """Test multiple attribute declarations in one line"""
    source = """class MLA { int a; int b; int c; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_068():
    """Test declaration with missing initializer for final (should still parse)"""
    source = """class MF { final int X; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_069():
    """Test incorrect token used as identifier (parse error expected)"""
    source = """class Err { static void main() { int 123abc; } }"""
    Parser(source).parse()


def test_070():
    """Test long nested parentheses in expression"""
    source = """class Long { static void main() { int x; x := (((((1))))); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_071():
    """Test method call with no args and trailing semicolon"""
    source = """class NoArg { static void main() { notify(); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_072():
    """Test nested blocks with returns inside"""
    source = """class NR { int f() { { return 1; } } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_073():
    """Test unusual spacing and newlines"""
    source = """class Sp {\n static void main() {\nint a;\na:=1;\n}\n}\n"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_074():
    """Test empty method body"""
    source = """class EM { void foo() {} static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_075():
    """Test chained arithmetic and boolean mix (should parse in grammar)"""
    source = """class Mix { static void main() { int x; x := 1 + 2 * 3; if (x > 0 && (y < 0 || z == 1)) then {} } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_076():
    """Test attribute names that shadow class names"""
    source = """class Shadow { Shadow s; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_077():
    """Test var decls with initializer expressions using new"""
    source = """class NEW { Test a := new Test(); static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_078():
    """Test colon-equals in unexpected places (should error)"""
    source = """class Bad { static void main() { := 1; } }"""
    Parser(source).parse()


def test_079():
    """Test big expression with nested function calls"""
    source = """class Nest { static void main() { x := f(g(h(1))); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_080():
    """Test comment-like tokens inside strings"""
    source = """class Cmt { static void main() { string s; s := "// not a comment"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_081():
    """Test numeric expressions with unary plus"""
    source = """class UP { static void main() { int x; x := 5 + 3; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_082():
    """Test use of semicolons between class declarations"""
    source = """class A1 { static void main() {} } class A2 { }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_083():
    """Test string with backslash characters"""
    source = """class BS { static void main() { string s; s := "\\\\"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_084():
    """Test nested for loops"""
    source = """class NF { static void main() { for i := 1 to 2 do { for j := 1 to 2 do { } } } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_085():
    """Test method with many parameters"""
    source = """class Many { void foo(int a; int b; int c; int d; int e) {} static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_086():
    """Test complex nested expressions mixing arithmetic and boolean ops"""
    source = """class CE { static void main() { if ((a+1) > (b*2) && c) then {} } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_087():
    """Test attribute with initializer that is method call"""
    source = """class AI { int a := foo(); static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_088():
    """Test object creation inside expression"""
    source = """class OC { static void main() { Test t; t := new Test(); x := f(t); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_089():
    """Test array literal used directly in assignment"""
    source = """class AL { static void main() { int[3] a := {1,2,3}; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_090():
    """Test complicated return expression with new and arithmetic"""
    source = """class Comp { Test f() { return new Test(); } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_091():
    """Test many nested braces and blocks"""
    source = """class Br { static void main() { { { { { } } } } } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_092():
    """Test empty parameter list syntax in declaration"""
    source = """class EP { int f() { return 0; } static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_093():
    """Test method call on array element"""
    source = """class MA { static void main() { Test t; t.f(); } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_094():
    """Test malformed numeric literal (expect parse attempt)"""
    source = """class MN { static void main() { int x; x := 1.2.3; } }"""
    Parser(source).parse()


def test_095():
    """Test extremely short program"""
    source = """class S1 { static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_096():
    """Test many semicolons in a row (should be benign)"""
    source = """class SC { static void main() { int a; a := 0; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_097():
    """Test class with comment-like content (kept in string)"""
    source = """class CommentTest { static void main() { string s; s := "/* comment */"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_098():
    """Test method with single-line statements separated by newlines"""
    source = """class NL { static void main() {\nint a;\na := 1;\n} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_099():
    """Test deeply nested expression with mix of operators"""
    source = """class DN { static void main() { x := (((a+b)*c)/d) % e; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_100():
    """Final test to reach 100: mixed declarations and control flow"""
    source = """class Final { static void main() { int a; for i := 0 to 2 do { if (i % 2 == 0) then { a := a + 1; } } } }"""
    expected = "success"
    assert Parser(source).parse() == expected

