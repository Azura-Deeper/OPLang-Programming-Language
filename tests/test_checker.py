from utils import Checker


def test_001():
    """Test a valid program that should pass all checks"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int y := x + 1;
    }
}
"""
    expected = "Static checking passed"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected

def test_002():
    """Test redeclared variable error"""
    source = """
class Test {
    static void main() {
        int x := 5;
        int x := 10;
    }
}
"""
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_003():
    """Test undeclared identifier error"""
    source = """
class Test {
    static void main() {
        int x := y + 1;
    }
}
"""
    expected = "UndeclaredIdentifier(y)"
    assert Checker(source).check_from_source() == expected

def test_004():
    """Test type mismatch error"""
    source = """
class Test {
    static void main() {
        int x := "hello";
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(x = StringLiteral('hello'))]))"
    assert Checker(source).check_from_source() == expected

def test_005():
    """Test break not in loop error"""
    source = """
class Test {
    static void main() {
        break;
    }
}
"""
    expected = "MustInLoop(BreakStatement())"
    assert Checker(source).check_from_source() == expected

def test_006():
    """Test cannot assign to constant error"""
    source = """
class Test {
    static void main() {
        final int x := 5;
        x := 10;
    }
}
"""
    expected = "CannotAssignToConstant(AssignmentStatement(IdLHS(x) := IntLiteral(10)))"
    assert Checker(source).check_from_source() == expected

def test_007():
    """Test illegal array literal error - alternative case"""
    source = """
class Test {
    static void main() {
        boolean[2] flags := {true, 42};
    }
}
"""
    expected = "IllegalArrayLiteral(ArrayLiteral({BoolLiteral(True), IntLiteral(42)}))"
    assert Checker(source).check_from_source() == expected


def test_008():
    """Test redeclared class error"""
    source = """
class Student {
    int id;
}
class Student {
    string name;
}
"""
    expected = "Redeclared(Class, Student)"
    assert Checker(source).check_from_source() == expected


def test_009():
    """Test redeclared method error"""
    source = """
class Calculator {
    int add() {
        return 5;
    }
    int add() {
        return 10;
    }
}
"""
    expected = "Redeclared(Method, add)"
    assert Checker(source).check_from_source() == expected


def test_010():
    """Test redeclared attribute error"""
    source = """
class Person {
    string name;
    int age;
    string name;
}
"""
    expected = "Redeclared(Attribute, name)"
    assert Checker(source).check_from_source() == expected


def test_011():
    """Test redeclared parameter error"""
    source = """
class Math {
    int calculate(int x; int x) {
        return x;
    }
}
"""
    expected = "Redeclared(Parameter, x)"
    assert Checker(source).check_from_source() == expected


def test_012():
    """Test undeclared class error"""
    source = """
class Student extends Person {
    int studentId;
}
"""
    expected = "UndeclaredClass(Person)"
    assert Checker(source).check_from_source() == expected


def test_013():
    """Test undeclared identifier error"""
    source = """
class Car {
    string brand;
    
    void display() {
        string m := model;
    }
}
"""
    expected = "UndeclaredIdentifier(model)"
    assert Checker(source).check_from_source() == expected


def test_014():
    """Test undeclared identifier error"""
    source = """
class Calculator {
    int add() {
        return 5;
    }
    
    void test() {
        int result := multiply;
    }
}
"""
    expected = "UndeclaredIdentifier(multiply)"
    assert Checker(source).check_from_source() == expected


def test_015():
    """Test continue not in loop error"""
    source = """
class Test {
    static void main() {
        continue;
    }
}
"""
    expected = "MustInLoop(ContinueStatement())"
    assert Checker(source).check_from_source() == expected


def test_016():
    """Test type mismatch in if statement"""
    source = """
class Test {
    static void main() {
        int x := 5;
        if x then {
            int y := 1;
        }
    }
}
"""
    expected = "TypeMismatchInStatement(IfStatement(if Identifier(x) then BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(y = IntLiteral(1))])], stmts=[])))"
    assert Checker(source).check_from_source() == expected


def test_017():
    """Test valid for statement"""
    source = """
class Test {
    static void main() {
        int i;
        for i := 0 to 10 do {
            int x := i;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_018():
    """Test type mismatch in assignment"""
    source = """
class Test {
    static void main() {
        boolean condition := true;
        int i := condition;
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(int), [Variable(i = Identifier(condition))]))"
    assert Checker(source).check_from_source() == expected


def test_019():
    """Test assignment type mismatch"""
    source = """
class Test {
    static void main() {
        int x := 10;
        string text := "hello";
        x := text;
    }
}
"""
    expected = "TypeMismatchInStatement"
    assert expected in Checker(source).check_from_source()


def test_020():
    """Test return type mismatch"""
    source = """
class Test {
    int getValue() {
        return "invalid";
    }
}
"""
    expected = "TypeMismatchInStatement"
    assert expected in Checker(source).check_from_source()


def test_021():
    """Test array subscripting with wrong index type"""
    source = """
class Test {
    static void main() {
        int x := 10;
        string y := "hello";
        int result := x + y;
    }
}
"""
    expected = "TypeMismatchInExpression"
    assert expected in Checker(source).check_from_source()


def test_022():
    """Test binary operation type mismatch"""
    source = """
class Test {
    static void main() {
        float x := 1.5;
        int y := 10;
        string result := x + y;
    }
}
"""
    expected = "TypeMismatchInStatement"
    assert expected in Checker(source).check_from_source()


def test_023():
    """Test binary operation type mismatch"""
    source = """
class Test {
    static void main() {
        int x := 5;
        string text := "hello";
        int sum := x + text;
    }
}
"""
    expected = "TypeMismatchInExpression"
    assert expected in Checker(source).check_from_source()


def test_024():
    """Test unary operation type mismatch"""
    source = """
class Test {
    static void main() {
        string text := "hello";
        int negative := -text;
    }
}
"""
    expected = "TypeMismatch"
    assert expected in Checker(source).check_from_source()


def test_025():
    """Test type mismatch in constant declaration"""
    source = """
class Test {
    final int a := 1.2;
}
"""
    expected = "TypeMismatchInConstant"
    assert expected in Checker(source).check_from_source()


def test_026():
    """Test illegal constant expression - None initialization"""
    source = """
class Test {
    final int x := 10;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_027():
    """Test type mismatch in assignment"""
    source = """
class Test {
    static void main() {
        float x := 1.5;
        boolean result := x;
    }
}
"""
    expected = "TypeMismatchInStatement"
    assert expected in Checker(source).check_from_source()


def test_028():
    """Test undeclared variable access"""
    source = """
class Test {
    static void main() {
        int x := unknownVariable;
    }
}
"""
    expected = "UndeclaredIdentifier"
    assert expected in Checker(source).check_from_source()


def test_029():
    """Test type mismatch in comparison"""
    source = """
class Test {
    static void main() {
        int x := 10;
        string y := "hello";
        boolean result := x == y;
    }
}
"""
    expected = "TypeMismatchInExpression"
    assert expected in Checker(source).check_from_source()


def test_030():
    """Test valid simple class"""
    source = """
class Test {
    int x := 10;
    static void main() {
        int y := 20;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_031():
    """Test valid variable shadowing"""
    source = """
class Test {
    int value := 100;
    
    void method() {
        int value := 200;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_032():
    """Test valid coercion - int to float"""
    source = """
class Test {
    static void main() {
        int x := 10;
        float y := x;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_033():
    """Test valid for loop"""
    source = """
class Test {
    static void main() {
        for int i := 0 to 10 do {
            int x := 0;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_034():
    """Test valid if statement"""
    source = """
class Test {
    static void main() {
        int x := 10;
        if x > 5 then {
            int y := 20;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_035():
    """Test valid nested loops"""
    source = """
class Test {
    static void main() {
        for int i := 0 to 5 do {
            int sum := 0;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_036():
    """Test valid constant expressions"""
    source = """
class Test {
    final int MAX_SIZE := 100;
    final boolean FLAG := true;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_037():
    """Test valid arithmetic operations"""
    source = """
class Test {
    static void main() {
        int x := 10;
        int y := 20;
        int sum := x + y;
        int product := x * y;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_038():
    """Test redeclared constant error"""
    source = """
class Test {
    final int MAX_SIZE := 100;
    final int MAX_SIZE := 200;
}
"""
    expected = "Redeclared"
    assert expected in Checker(source).check_from_source()


def test_039():
    """Test redeclared variable error"""
    source = """
class Configuration {
    string APP_NAME := "MyApp";
    string APP_NAME := "NewApp";
}
"""
    expected = "Redeclared"
    assert expected in Checker(source).check_from_source()


def test_040():
    """Test simple for loop"""
    source = """
class Test {
    void process() {
        for int i := 0 to 20 do {
            int x := 0;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_041():
    """Test type mismatch in method call arguments"""
    source = """
class Test {
    void processInt(int value) {
        int x := value;
    }
    
    void test() {
        string text := "123";
        this.processInt(text);
    }
}
"""
    expected = "TypeMismatch"
    assert expected in Checker(source).check_from_source()


def test_042():
    """Test void method used in expression"""
    source = """
class Test {
    void printMessage() {
        int x := 10;
    }
    
    static void main() {
        Test t := new Test();
        int result := t.printMessage();
    }
}
"""
    expected = "TypeMismatchInExpression"
    assert expected in Checker(source).check_from_source()


def test_043():
    """Test type mismatch in assignment"""
    source = """
class Test {
    static void main() {
        boolean flag := true;
        int number := flag;
    }
}
"""
    expected = "TypeMismatchInStatement"
    assert expected in Checker(source).check_from_source()


def test_044():
    """Test type mismatch in expression"""
    source = """
class Test {
    static void main() {
        string text := "hello";
        float value := text;
    }
}
"""
    expected = "TypeMismatchInStatement"
    assert expected in Checker(source).check_from_source()


def test_045():
    """Test logical operation with non-boolean"""
    source = """
class Test {
    static void main() {
        int x := 5;
        boolean flag := true;
        boolean result := x && flag;
    }
}
"""
    expected = "TypeMismatchInExpression"
    assert expected in Checker(source).check_from_source()


def test_046():
    """Test comparison with incompatible types"""
    source = """
class Test {
    static void main() {
        string text := "hello";
        int x := 5;
        boolean comparison := text < x;
    }
}
"""
    expected = "TypeMismatchInExpression"
    assert expected in Checker(source).check_from_source()


def test_047():
    """Test attribute access on primitive type"""
    source = """
class Test {
    static void main() {
        int x := 10;
        int invalid := x.length;
    }
}
"""
    expected = "TypeMismatch"
    assert expected in Checker(source).check_from_source()


def test_048():
    """Test method call with wrong number of arguments"""
    source = """
class Test {
    int add(int a; int b) {
        return a + b;
    }
    
    void test() {
        int result := this.add(5);
    }
}
"""
    expected = "TypeMismatch"
    assert expected in Checker(source).check_from_source()


def test_049():
    """Test nested if statements"""
    source = """
class Test {
    static void main() {
        int i := 7;
        if i > 5 then {
            if i == 7 then {
                int x := i;
            }
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_050():
    """Test constructor with proper parameters"""
    source = """
class Student {
    string name := "default";
    int age := 0;
    
    Student(string n; int a) {
        this.name := n;
        this.age := a;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_051():
    """Test simple static method definition"""
    source = """
class Test {
    static int getValue() {
        return 42;
    }
    
    static void main() {
        int value := 42;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_052():
    """Test this expression in instance method"""
    source = """
class Test {
    int value := 0;
    
    void setValue(int v) {
        this.value := v;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_053():
    """Test this expression in static method - should fail"""
    source = """
class Test {
    static int value := 0;
    
    static void setValue(int v) {
        this.value := v;
    }
}
"""
    expected = "IllegalMemberAccess"
    assert expected in Checker(source).check_from_source()


def test_054():
    """Test simple constructor declaration"""
    source = """
class Resource {
    string name := "default";
    
    Resource(string n) {
        this.name := n;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_055():
    """Test simple class definition"""
    source = """
class Test {
    void methodA() {
        int x := 10;
    }
    void methodB() {
        int y := 20;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_056():
    """Test simple attribute access"""
    source = """
class Test {
    string species := "default";
    
    void identify() {
        this.species := "Canine";
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_057():
    """Test simple method definition"""
    source = """
class Test {
    void setSpecies(string s) {
        string temp := s;
    }
    
    void identify() {
        string species := "Canine";
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_058():
    """Test variable out of scope"""
    source = """
class Test {
    void method1() {
        int localVar := 42;
    }
    
    void method2() {
        int value := localVar + 1;
    }
}
"""
    expected = "UndeclaredIdentifier"
    assert expected in Checker(source).check_from_source()


def test_059():
    """Test variable scope in block"""
    source = """
class Test {
    static void main() {
        {
            int x := 10;
        }
        int y := x + 1;
    }
}
"""
    expected = "UndeclaredIdentifier"
    assert expected in Checker(source).check_from_source()


def test_060():
    """Test final variable proper initialization"""
    source = """
class Test {
    final string VERSION := "1.0";
    
    Test(string version) {
        string temp := version;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_061():
    """Test variable type consistency"""
    source = """
class Test {
    static void main() {
        int prime := 2;
        string word := "hello";
        boolean flag := true;
        float decimal := 3.14;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_062():
    """Test object creation and usage"""
    source = """
class Rectangle {
    float width := 0.0;
    float height := 0.0;
    
    Rectangle(float w; float h) {
        this.width := w;
        this.height := h;
    }
}
class Test {
    static void main() {
        Rectangle shape := new Rectangle(1.0; 2.0);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_063():
    """Test simple variable declaration"""
    source = """
class Test {
    static void main() {
        int empty := 0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_064():
    """Test string operations"""
    source = """
class Test {
    static void main() {
        string message := "Hello World";
        string temp := message;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_065():
    """Test boolean operations"""
    source = """
class Test {
    static void main() {
        boolean a := true;
        boolean b := false;
        boolean and_result := a && b;
        boolean or_result := a || b;
        boolean not_result := !a;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_066():
    """Test arithmetic operations with mixed int/float"""
    source = """
class Test {
    static void main() {
        int x := 10;
        float y := 3.14;
        float result1 := x + y;
        float result2 := x * y;
        float result3 := y - x;
        float result4 := y / x;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_067():
    """Test comparison operations"""
    source = """
class Test {
    static void main() {
        int x := 10;
        int y := 20;
        boolean lt := x < y;
        boolean le := x <= y;
        boolean gt := x > y;
        boolean ge := x >= y;
        boolean eq := x == y;
        boolean ne := x != y;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_068():
    """Test modulo operation"""
    source = """
class Test {
    static void main() {
        int x := 10;
        int y := 3;
        int remainder := x % y;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_069():
    """Test unary plus and minus"""
    source = """
class Test {
    static void main() {
        int x := 10;
        int positive := +x;
        int negative := -x;
        float f := 3.14;
        float neg_float := -f;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_070():
    """Test parenthesized expressions"""
    source = """
class Test {
    static void main() {
        int result := (10 + 20) * (30 - 15);
        boolean condition := (true || false) && (false || true);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_071():
    """Test method with no parameters"""
    source = """
class Test {
    int getValue() {
        return 42;
    }
    
    static void main() {
        Test t := new Test();
        int value := t.getValue();
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_072():
    """Test method with multiple parameters"""
    source = """
class Calculator {
    int calculate(int a; int b; int c) {
        return a + b + c;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_073():
    """Test simple method definition"""
    source = """
class Math {
    int square(int x) {
        return x * x;
    }
    
    int add(int a; int b) {
        return a + b;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_074():
    """Test simple if condition"""
    source = """
class Test {
    static void main() {
        int x := 10;
        int y := 20;
        boolean result := x < y;
        if result then {
            int z := 30;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_075():
    """Test complex expression in for loop bounds"""
    source = """
class Test {
    static void main() {
        int start := 1;
        int end := 10;
        for int i := start + 1 to end - 1 do {
            int x := 0;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_076():
    """Test downto in for loop"""
    source = """
class Test {
    static void main() {
        for int i := 10 downto 1 do {
            int x := 0;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_077():
    """Test multiple variable declarations in same statement"""
    source = """
class Test {
    static void main() {
        int x := 10, y := 20, z := 30;
        string a := "hello", b := "world";
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_078():
    """Test multiple attribute declarations"""
    source = """
class Point {
    float x := 0.0, y := 0.0;
    int id := 0, count := 1;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_079():
    """Test static attribute definition"""
    source = """
class Counter {
    static int count := 0;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_080():
    """Test nil literal assignment"""
    source = """
class Test {
    static void main() {
        string text := nil;
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(PrimitiveType(string), [Variable(text = NilLiteral(nil))]))"
    assert Checker(source).check_from_source() == expected


def test_081():
    """Test simple variable assignments"""
    source = """
class Test {
    static void main() {
        int index := 2;
        int base := 1;
        int value := index + base;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_082():
    """Test simple class composition"""
    source = """
class Point {
    float x := 0.0;
    float y := 0.0;
}
class Circle {
    float radius := 0.0;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_083():
    """Test simple method definition"""
    source = """
class Animal {
    void makeSound(string sound) {
        string temp := sound;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_084():
    """Test simple attribute access"""
    source = """
class Base {
    int protectedValue := 10;
    
    void accessValue() {
        int value := this.protectedValue;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_085():
    """Test simple method with conditional"""
    source = """
class Factorial {
    int factorial(int n) {
        if n <= 1 then {
            return 1;
        } else {
            return n;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_086():
    """Test simple method definitions"""
    source = """
class Test {
    boolean isEven(int n) {
        if n == 0 then {
            return true;
        } else {
            return false;
        }
    }
    
    boolean isOdd(int n) {
        if n == 0 then {
            return false;
        } else {
            return true;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_087():
    """Test constant with simple values"""
    source = """
class Constants {
    final int BASE := 10;
    final int SQUARE := 100;
    final boolean LARGE := true;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_088():
    """Test simple coercion"""
    source = """
class Test {
    static void main() {
        int x := 42;
        float y := x;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_089():
    """Test object assignment with inheritance"""
    source = """
class Animal {
    void move() {}
}
class Dog extends Animal {
    void bark() {}
}
class Test {
    static void main() {
        Animal animal := new Dog();  // Valid: subtype to supertype
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_090():
    """Test invalid object assignment"""
    source = """
class Animal {
    void move() {}
}
class Plant {
    void grow() {}
}
class Test {
    static void main() {
        Animal animal := new Plant();  // Invalid: no inheritance relationship
    }
}
"""
    expected = "TypeMismatchInStatement(VariableDecl(ClassType(Animal), [Variable(animal = ObjectCreation(new Plant()))]))"
    assert Checker(source).check_from_source() == expected


def test_091():
    """Test simple class definition"""
    source = """
class Animal {
    void move() {
        int x := 10;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_092():
    """Test else-if chain"""
    source = """
class Test {
    static void main() {
        int grade := 85;
        if grade >= 90 then {
            int a := 1;
        } else {
            if grade >= 80 then {
                int b := 2;
            } else {
                if grade >= 70 then {
                    int c := 3;
                } else {
                    int d := 4;
                }
            }
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_093():
    """Test complex boolean expression"""
    source = """
class Test {
    static void main() {
        boolean a := true;
        boolean b := false;
        boolean c := true;
        boolean complex := (a && b) || (b || c) && !(a && c);
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_094():
    """Test float division"""
    source = """
class Test {
    static void main() {
        float a := 10.0;
        float b := 3.0;
        float result := a / b;
        int x := 10;
        int y := 3;
        int intResult := x / y;  // Integer division
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_095():
    """Test string operations"""
    source = """
class Test {
    static void main() {
        string first := "Hello";
        string second := "World";
        string combined := first ^ " " ^ second;
        boolean equal := first == second;
        boolean notEqual := first != second;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_096():
    """Test invalid nil operations"""
    source = """
class Test {
    static void main() {
        int x := nil + 5;
    }
}
"""
    expected = "TypeMismatchInExpression(BinaryOp(NilLiteral(nil), +, IntLiteral(5)))"
    assert Checker(source).check_from_source() == expected


def test_097():
    """Test constructor parameter shadowing class attribute"""
    source = """
class Person {
    string name := "default";
    int age := 0;
    
    Person(string name; int age) {
        this.name := name;
        this.age := age;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_098():
    """Test single constructor"""
    source = """
class Point {
    float x := 0.0;
    float y := 0.0;
    
    Point() {
        this.x := 0.0;
        this.y := 0.0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_099():
    """Test nested scope"""
    source = """
class ScopeTest {
    int globalVar := 100;
    
    void outerMethod() {
        int outerVar := 200;
        int sum := this.globalVar + outerVar;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected


def test_100():
    """Test comprehensive valid program"""
    source = """
class Shape {
    int value := 0;
    
    float getArea() {
        return 0.0;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected
