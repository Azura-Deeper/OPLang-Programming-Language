"""
Static error classes for OPLang semantic analysis.
This module defines all the semantic error types used by the static checker.
"""


class StaticError(Exception):
    """Base class for all static semantic errors."""
    
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class Redeclared(StaticError):
    """Error for redeclared entities."""
    
    def __init__(self, kind, name):
        super().__init__(f"Redeclared({kind}, {name})")
        self.kind = kind
        self.name = name


class UndeclaredIdentifier(StaticError):
    """Error for undeclared identifiers."""
    
    def __init__(self, name):
        super().__init__(f"UndeclaredIdentifier({name})")
        self.name = name


class UndeclaredClass(StaticError):
    """Error for undeclared classes."""
    
    def __init__(self, name):
        super().__init__(f"UndeclaredClass({name})")
        self.name = name


class UndeclaredAttribute(StaticError):
    """Error for undeclared attributes."""
    
    def __init__(self, name):
        super().__init__(f"UndeclaredAttribute({name})")
        self.name = name


class UndeclaredMethod(StaticError):
    """Error for undeclared methods."""
    
    def __init__(self, name):
        super().__init__(f"UndeclaredMethod({name})")
        self.name = name


class CannotAssignToConstant(StaticError):
    """Error for assignment to constant."""
    
    def __init__(self, statement):
        super().__init__(f"CannotAssignToConstant({statement})")
        self.statement = statement


class TypeMismatchInStatement(StaticError):
    """Error for type mismatch in statements."""
    
    def __init__(self, statement):
        super().__init__(f"TypeMismatchInStatement({statement})")
        self.statement = statement


class TypeMismatchInExpression(StaticError):
    """Error for type mismatch in expressions."""
    
    def __init__(self, expression):
        super().__init__(f"TypeMismatchInExpression({expression})")
        self.expression = expression


class TypeMismatchInConstant(StaticError):
    """Error for type mismatch in constant declarations."""
    
    def __init__(self, const_decl):
        super().__init__(f"TypeMismatchInConstant({const_decl})")
        self.const_decl = const_decl


class MustInLoop(StaticError):
    """Error for break/continue outside loop."""
    
    def __init__(self, statement):
        super().__init__(f"MustInLoop({statement})")
        self.statement = statement


class IllegalConstantExpression(StaticError):
    """Error for illegal constant expression."""
    
    def __init__(self, expression):
        super().__init__(f"IllegalConstantExpression({expression})")
        self.expression = expression


class IllegalArrayLiteral(StaticError):
    """Error for illegal array literal."""
    
    def __init__(self, array_literal):
        super().__init__(f"IllegalArrayLiteral({array_literal})")
        self.array_literal = array_literal


class IllegalMemberAccess(StaticError):
    """Error for illegal member access."""
    
    def __init__(self, access):
        super().__init__(f"IllegalMemberAccess({access})")
        self.access = access