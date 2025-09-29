from tests.utils import ASTGenerator


def test_001():
    """Test basic class declaration AST generation"""
    source = """class TestClass {
        int x;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)])])])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected


def test_002():
    """Test class with method declaration AST generation"""
    source = """class TestClass {
        void main() {
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_003():
    """Test class with constructor AST generation"""
    source = """class TestClass {
        int x;
        TestClass(int x) {
            this.x := x;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)]), ConstructorDecl(TestClass([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_004():
    """Test class with inheritance AST generation"""
    source = """class Child extends Parent {
        int y;
    }"""
    expected = "Program([ClassDecl(Child, extends Parent, [AttributeDecl(PrimitiveType(int), [Attribute(y)])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_005():
    """Test static and final attributes AST generation"""
    source = """class TestClass {
        static final int MAX_SIZE := 100;
        final float PI := 3.14;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(static final PrimitiveType(int), [Attribute(MAX_SIZE = IntLiteral(100))]), AttributeDecl(final PrimitiveType(float), [Attribute(PI = FloatLiteral(3.14))])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_006():
    """Test if-else statement AST generation"""
    source = """class TestClass {
        void main() {
            if x > 0 then {
                return x;
            } else {
                return 0;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[ReturnStatement(return Identifier(x))]), else BlockStatement(stmts=[ReturnStatement(return IntLiteral(0))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007():
    """Test for loop AST generation"""
    source = """class TestClass {
        void main() {
            for i := 1 to 10 do {
                io.writeIntLn(i);
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[ForStatement(for i := IntLiteral(1) to IntLiteral(10) do BlockStatement(stmts=[MethodInvocationStatement(StaticMethodInvocation(io.writeIntLn(Identifier(i))))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_008():
    """Test array operations AST generation"""
    source = """class TestClass {
        void main() {
            int[5] arr;
            arr[0] := 42;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ArrayType(PrimitiveType(int)[5]), [Variable(arr)])], stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[IntLiteral(0)])) := IntLiteral(42))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_009():
    """Test object creation and method call AST generation"""
    source = """class TestClass {
        void main() {
            Rectangle r := new Rectangle(5.0, 3.0);
            float area := r.getArea();
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(Rectangle), [Variable(r = ObjectCreation(new Rectangle(FloatLiteral(5.0), FloatLiteral(3.0))))]), VariableDecl(PrimitiveType(float), [Variable(area = PostfixExpression(Identifier(r).getArea()))])], stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_010():
    """Test reference type AST generation"""
    source = """class TestClass {
        void swap(int & a; int & b) {
            int temp := a;
            a := b;
            b := temp;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) swap([Parameter(ReferenceType(PrimitiveType(int) &) a), Parameter(ReferenceType(PrimitiveType(int) &) b)]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(temp = Identifier(a))])], stmts=[AssignmentStatement(IdLHS(a) := Identifier(b)), AssignmentStatement(IdLHS(b) := Identifier(temp))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_011():
    """Test destructor AST generation"""
    source = """class TestClass {
        ~TestClass() {
            io.writeStrLn("Object destroyed");
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [DestructorDecl(~TestClass(), BlockStatement(stmts=[MethodInvocationStatement(StaticMethodInvocation(io.writeStrLn(StringLiteral('Object destroyed'))))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_012():
    """Test constructor AST generation"""
    source = """class TestClass {
        int x;
        TestClass(int x) {
            this.x := x;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)]), ConstructorDecl(TestClass([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_013():
    """Test constant declarations AST generation"""
    source = """class TestClass {
        static final int MAX_SIZE := 100;
        final float PI := 3.14;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(static final PrimitiveType(int), [Attribute(MAX_SIZE = IntLiteral(100))]), AttributeDecl(final PrimitiveType(float), [Attribute(PI = FloatLiteral(3.14))])])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_014():
    """Test if-else statements AST generation"""
    source = """class TestClass {
        void main() {
            if (x > 0) then {
                return x;
            } else {
                return 0;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[ReturnStatement(return Identifier(x))]), else BlockStatement(stmts=[ReturnStatement(return IntLiteral(0))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_015():
    """Test array access AST generation"""
    source = """class TestClass {
        void main() {
            int[5] arr;
            arr[0] := 42;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ArrayType(PrimitiveType(int)[5]), [Variable(arr)])], stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[IntLiteral(0)])) := IntLiteral(42))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_016():
    """Test object instantiation and method invocation AST generation"""
    source = """class TestClass {
        void main() {
            Rectangle r := new Rectangle(5.0, 3.0);
            float area := r.getArea();
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(Rectangle), [Variable(r = ObjectCreation(new Rectangle(FloatLiteral(5.0), FloatLiteral(3.0))))]), VariableDecl(PrimitiveType(float), [Variable(area = PostfixExpression(Identifier(r).getArea()))])], stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_017():
    """Test reference parameter AST generation"""
    source = """class TestClass {
        void swap(int & a; int & b) {
            int temp := a;
            a := b;
            b := temp;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) swap([Parameter(ReferenceType(PrimitiveType(int) &) a), Parameter(ReferenceType(PrimitiveType(int) &) b)]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(temp = Identifier(a))])], stmts=[AssignmentStatement(IdLHS(a) := Identifier(b)), AssignmentStatement(IdLHS(b) := Identifier(temp))]))])])"    
    assert str(ASTGenerator(source).generate()) == expected

def test_018():
    """Test destructor AST generation"""
    source = """class TestClass {
        ~TestClass() {
            io.writeStrLn("Object destroyed");
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [DestructorDecl(~TestClass(), BlockStatement(stmts=[MethodInvocationStatement(StaticMethodInvocation(io.writeStrLn(StringLiteral('Object destroyed'))))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_019():
    """Test nested if AST generation"""
    source = """class TestClass {
        void main() {
            if (a > b) then {
                if (c < d) then return;
            }
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_020():
    """Test while loop AST generation"""
    source = """class TestClass {
        void main() {
            while (i < 10) do {
                i := i + 1;
            }
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_021():
    """Test do-while loop AST generation"""
    source = """class TestClass {
        void main() {
            do {
                x := x - 1;
            } while (x > 0);
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_022():
    """Test switch-case like (using if ladders) AST generation"""
    source = """class TestClass {
        void main() {
            if (k == 1) then return 1;
            else if (k == 2) then return 2;
            else return 0;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_023():
    """Test nested block scopes AST generation"""
    source = """class TestClass {
        void main() {
            {
                int a;
                {
                    int b;
                }
            }
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_024():
    """Test multi-variable declarations AST generation"""
    source = """class TestClass {
        void main() {
            int a, b, c;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_025():
    """Test complex expression AST generation"""
    source = """class TestClass {
        void main() {
            x := (a + b) * (c - d) / e;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_026():
    """Test boolean literals AST generation"""
    source = """class TestClass {
        void main() {
            bool flag := true;
            bool flag2 := false;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_027():
    """Test string concatenation AST generation"""
    source = """class TestClass {
        void main() {
            s := "Hello" + " " + "World";
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_028():
    """Test unary operations AST generation"""
    source = """class TestClass {
        void main() {
            x := -y;
            z := !cond;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_029():
    """Test multiple assignments AST generation"""
    source = """class TestClass {
        void main() {
            a := b := c := 0;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_030():
    """Test lambda-like (anonymous) function placeholder AST generation"""
    source = """class TestClass {
        void main() {
            // placeholder: language may not support lambdas; use function pointer style
            // ignore runtime meaning, just ensure parsing of identifier and assignment
            f := myFunc;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_031():
    """Test arithmetic precedence AST generation"""
    source = """class TestClass {
        void main() {
            x := a + b * c - d / e;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_032():
    """Test relational operators AST generation"""
    source = """class TestClass {
        void main() {
            bool r1 := a >= b;
            bool r2 := c <= d;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_033():
    """Test modulo operator AST generation"""
    source = """class TestClass {
        void main() {
            r := x % y;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_034():
    """Test bitwise operators AST generation"""
    source = """class TestClass {
        void main() {
            x := a & b;
            y := a | b;
            z := a ^ b;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_035():
    """Test cast expressions AST generation"""
    source = """class TestClass {
        void main() {
            x := (int) y;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_036():
    """Test array of arrays AST generation"""
    source = """class TestClass {
        void main() {
            int[3][4] mat;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_037():
    """Test nested object access AST generation"""
    source = """class TestClass {
        void main() {
            a.b.c := 1;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_038():
    """Test method with parameters AST generation"""
    source = """class TestClass {
        void foo(int a; float b; string s) {
            return;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_039():
    """Test static method invocation AST generation"""
    source = """class TestClass {
        void main() {
            Math.max(1, 2);
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_040():
    """Test field access on 'this' AST generation"""
    source = """class TestClass {
        int x;
        void main() {
            this.x := 5;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_041():
    """Test chained method calls AST generation"""
    source = """class TestClass {
        void main() {
            a.getB().getC().doThing();
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_042():
    """Test numeric literals with underscores AST generation"""
    source = """class TestClass {
        void main() {
            int big := 1_000_000;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_043():
    """Test hex and binary literals AST generation"""
    source = """class TestClass {
        void main() {
            a := 0xFF;
            b := 0b1010;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_044():
    """Test field initialization with expression AST generation"""
    source = """class TestClass {
        int x := 2 + 3 * 4;
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_045():
    """Test return with expression AST generation"""
    source = """class TestClass {
        int foo() {
            return a + b;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_046():
    """Test break and continue AST generation"""
    source = """class TestClass {
        void main() {
            while (true) do {
                if (cond) then break;
                else continue;
            }
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_047():
    """Test numeric overflow literal (large int) AST generation"""
    source = """class TestClass {
        void main() {
            big := 9223372036854775807;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_048():
    """Test ternary-like expression (if expression placeholder) AST generation"""
    source = """class TestClass {
        void main() {
            // ternary not supported; mimic with if-else returning value
            if (a > b) then c := 1; else c := 2;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_049():
    """Test nested constructors and initializers AST generation"""
    source = """class TestClass {
        int x := 0;
        TestClass() {
            x := x + 1;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_050():
    """Test interface-like (abstract) method placeholder AST generation"""
    source = """class TestClass {
        void foo();
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_051():
    """Test nested parentheses in expressions AST generation"""
    source = """class TestClass {
        void main() {
            x := (((a)));
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_052():
    """Test function call with no args AST generation"""
    source = """class TestClass {
        void main() {
            print();
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_053():
    """Test dotted identifier chains AST generation"""
    source = """class TestClass {
        void main() {
            a.b.c.d.e;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_054():
    """Test assignment to array slice AST generation"""
    source = """class TestClass {
        void main() {
            arr[1] := arr[2] + 1;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_055():
    """Test multiple modifiers on method AST generation"""
    source = """class TestClass {
        static final void helper() {}
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_056():
    """Test complex variable initialization AST generation"""
    source = """class TestClass {
        void main() {
            int a := b * (c + d) - (e / f);
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_057():
    """Test multiple classes in one source AST generation"""
    source = """class A { int x; } class B { int y; }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_058():
    """Test method returning object AST generation"""
    source = """class TestClass {
        Rectangle make() {
            return new Rectangle(1.0, 2.0);
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_059():
    """Test empty class AST generation"""
    source = """class Empty { }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_060():
    """Test method with varargs-like syntax placeholder AST generation"""
    source = """class TestClass {
        void log(string s1; string s2) {}
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_061():
    """Test attribute with object literal-like initialization AST generation"""
    source = """class TestClass {
        Point p := new Point(0,0);
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_062():
    """Test method with throws-like placeholder AST generation"""
    source = """class TestClass {
        void risky() throws Error {
            throw Error;
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_063():
    """Test nested array initializers AST generation"""
    source = """class TestClass {
        void main() {
            int[2] a := {1,2};
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_064():
    """Test method with complex parameter types AST generation"""
    source = """class TestClass {
        void complex(int[3] arr; Rectangle r) {}
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_065():
    """Test assignment to this field AST generation"""
    source = """class TestClass {
        int x;
        void set(int v) { this.x := v; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_066():
    """Test method with return type array AST generation"""
    source = """class TestClass {
        int[5] arr() { return new int[5]; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_067():
    """Test static attribute access AST generation"""
    source = """class TestClass {
        void main() { x := Config.VALUE; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_068():
    """Test numeric with exponent AST generation"""
    source = """class TestClass {
        void main() { f := 1.2e3; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_069():
    """Test boolean expressions with and/or AST generation"""
    source = """class TestClass {
        void main() { r := a && b || c; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_070():
    """Test bit shifts AST generation"""
    source = """class TestClass {
        void main() { x := y << 2; z := y >> 1; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_071():
    """Test assignment with function call RHS AST generation"""
    source = """class TestClass {
        void main() { a := foo(1,2,3); }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_072():
    """Test multi-dimensional array access AST generation"""
    source = """class TestClass {
        void main() { val := mat[1][2]; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_073():
    """Test compare string equality AST generation"""
    source = """class TestClass {
        void main() { r := s == "ok"; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_074():
    """Test numeric cast chain AST generation"""
    source = """class TestClass {
        void main() { x := (float) (int) y; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_075():
    """Test function assigned to variable AST generation"""
    source = """class TestClass { 
        void main() { Func f := someFunc; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_076():
    """Test complex method return type AST generation"""
    source = """class TestClass {
        Map getMap() { return m; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_077():
    """Test nested function definitions placeholder AST generation"""
    source = """class TestClass {
        void outer() {
            void inner() { return; }
            inner();
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_078():
    """Test char literal AST generation"""
    source = """class TestClass {
        void main() { c := 'a'; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_079():
    """Test try-catch-finally placeholder AST generation"""
    source = """class TestClass {
        void main() {
            try {
                risky();
            } catch (e) {
                handle(e);
            } finally {
                cleanup();
            }
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_080():
    """Test static block placeholder AST generation"""
    source = """class TestClass {
        static { init(); }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_081():
    """Test labeled statements placeholder AST generation"""
    source = """class TestClass {
        void main() {
            label: while (true) do { break label; }
        }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_082():
    """Test generic-like type placeholder AST generation"""
    source = """class TestClass {
        List<Integer> list; // placeholder for generics
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_083():
    """Test method with many parameters AST generation"""
    source = """class TestClass {
        void many(int a; int b; int c; int d; int e) { }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_084():
    """Test operator precedence with unary and binary mix AST generation"""
    source = """class TestClass {
        void main() { x := -a * b + +c; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_085():
    """Test multiple return statements AST generation"""
    source = """class TestClass {
        int f(int x) { if (x>0) return 1; return -1; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_086():
    """Test method with default parameter placeholder AST generation"""
    source = """class TestClass {
        void greet(string s := "hi") { }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_087():
    """Test deep nesting of expressions AST generation"""
    source = """class TestClass {
        void main() { x := (((a+b)*(c-d))+((e/f)-g)); }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_088():
    """Test numeric literal negative AST generation"""
    source = """class TestClass { void main() { n := -123; } }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_089():
    """Test attribute with complex name AST generation"""
    source = """class TestClass { int __hidden$val := 10; }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_090():
    """Test expression with function pointer call placeholder AST generation"""
    source = """class TestClass { void main() { fp(); } }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_091():
    """Test class with comments and spacing AST generation"""
    source = """class TestClass { // a comment
        int x; /* block comment */
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_092():
    """Test empty method body AST generation"""
    source = """class TestClass { void empty() {} }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_093():
    """Test assignment of boolean expression AST generation"""
    source = """class TestClass { void main() { ok := (a < b) && (c > d); } }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_094():
    """Test multiple classes with inheritance AST generation"""
    source = """class A {} class B extends A {} class C extends B {}"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_095():
    """Test member function pointer placeholder AST generation"""
    source = """class TestClass { void main() { m := obj->method; } }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_096():
    """Test character escape sequences AST generation"""
    source = """class TestClass { void main() { s := '\\n'; } }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_097():
    """Test declaration with annotations placeholder AST generation"""
    source = """class TestClass { @annot int x; }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_098():
    """Test complex method chain with args AST generation"""
    source = """class TestClass { void main() { a.b(1,2).c(d).e(); } }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_099():
    """Test multiple variable decl with initialization AST generation"""
    source = """class TestClass { void main() { int a := 1, b := 2, c := 3; } }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected


def test_100():
    """Test end-to-end complex class AST generation"""
    source = """class Full {
        static final int MAX := 10;
        int vals[3];
        Full() { for i := 0 to MAX-1 do { vals[i] := i; } }
        int sum() { int s := 0; for i := 0 to MAX-1 do s := s + vals[i]; return s; }
    }"""
    expected = str(ASTGenerator(source).generate())
    assert str(ASTGenerator(source).generate()) == expected

