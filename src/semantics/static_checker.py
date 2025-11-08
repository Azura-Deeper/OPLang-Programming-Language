"""
Static Semantic Checker for OPLang programming language.
This module implements comprehensive static semantic analysis including
scope management, type checking, and error detection.
"""

from typing import Dict, List, Optional, Set, Union, Any
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .static_error import *


class Symbol:
    """Base class for symbol table entries."""
    
    def __init__(self, name: str, symbol_type: str):
        self.name = name
        self.type = symbol_type


class VariableSymbol(Symbol):
    """Symbol for variables and constants."""
    
    def __init__(self, name: str, var_type: str, is_final: bool = False):
        super().__init__(name, var_type)
        self.is_final = is_final


class MethodSymbol(Symbol):
    """Symbol for methods."""
    
    def __init__(self, name: str, return_type: str, params: List[tuple], is_static: bool = False):
        super().__init__(name, return_type)
        self.params = params  # List of (param_name, param_type)
        self.is_static = is_static


class AttributeSymbol(Symbol):
    """Symbol for class attributes."""
    
    def __init__(self, name: str, attr_type: str, is_static: bool = False, is_final: bool = False):
        super().__init__(name, attr_type)
        self.is_static = is_static
        self.is_final = is_final


class ClassSymbol(Symbol):
    """Symbol for classes."""
    
    def __init__(self, name: str, superclass: Optional[str] = None):
        super().__init__(name, "class")
        self.superclass = superclass
        self.attributes: Dict[str, AttributeSymbol] = {}
        self.methods: Dict[str, MethodSymbol] = {}


class Scope:
    """Represents a scope in the symbol table."""
    
    def __init__(self, name: str, parent: Optional["Scope"] = None):
        self.name = name
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}
        
    def define(self, symbol: Symbol):
        """Define a symbol in this scope."""
        if symbol.name in self.symbols:
            return False  # Already exists
        self.symbols[symbol.name] = symbol
        return True
        
    def resolve(self, name: str) -> Optional[Symbol]:
        """Resolve a symbol by name, checking parent scopes."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None


class StaticChecker(ASTVisitor):
    """Static semantic checker for OPLang."""
    
    def __init__(self):
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        self.classes: Dict[str, ClassSymbol] = {}
        self.current_class: Optional[ClassSymbol] = None
        self.current_method: Optional[MethodSymbol] = None
        self.in_loop = False
        self.error_found = False
        
    def check_program(self, program: Program):
        """Main entry point for static checking."""
        try:
            self.visit(program)
        except StaticError as e:
            raise e
    
    def enter_scope(self, name: str):
        """Enter a new scope."""
        new_scope = Scope(name, self.current_scope)
        self.current_scope = new_scope
        return new_scope
        
    def exit_scope(self):
        """Exit the current scope."""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def type_to_string(self, node_type: Type) -> str:
        """Convert type node to string representation."""
        if isinstance(node_type, PrimitiveType):
            return node_type.type_name
        elif isinstance(node_type, ArrayType):
            element_type = self.type_to_string(node_type.element_type)
            return f"{element_type}[{node_type.size}]"
        elif isinstance(node_type, ClassType):
            return node_type.class_name
        elif isinstance(node_type, ReferenceType):
            ref_type = self.type_to_string(node_type.referenced_type)
            return f"{ref_type}&"
        else:
            return "unknown"
    
    def type_compatible(self, from_type: str, to_type: str) -> bool:
        """Check if types are compatible (including coercion rules)."""
        if from_type == to_type:
            return True
        
        # int can coerce to float
        if from_type == "int" and to_type == "float":
            return True
            
        # Subtype can coerce to supertype
        if from_type in self.classes and to_type in self.classes:
            return self.is_subtype(from_type, to_type)
            
        return False
    
    def is_subtype(self, child_class: str, parent_class: str) -> bool:
        """Check if child_class is a subtype of parent_class."""
        if child_class == parent_class:
            return True
        
        if child_class not in self.classes:
            return False
            
        current = self.classes[child_class]
        while current.superclass:
            if current.superclass == parent_class:
                return True
            if current.superclass not in self.classes:
                break
            current = self.classes[current.superclass]
        
        return False
    
    def get_expression_type(self, expr: Expr) -> str:
        """Get the type of an expression."""
        if isinstance(expr, IntLiteral):
            return "int"
        elif isinstance(expr, FloatLiteral):
            return "float"
        elif isinstance(expr, BoolLiteral):
            return "boolean"
        elif isinstance(expr, StringLiteral):
            return "string"
        elif isinstance(expr, NilLiteral):
            return "nil"
        elif isinstance(expr, Identifier):
            symbol = self.current_scope.resolve(expr.name)
            if symbol:
                return symbol.type
            else:
                raise UndeclaredIdentifier(expr.name)
        elif isinstance(expr, BinaryOp):
            return self.get_binary_op_type(expr)
        elif isinstance(expr, UnaryOp):
            return self.get_unary_op_type(expr)
        elif isinstance(expr, PostfixExpression):
            return self.get_postfix_type(expr)
        elif isinstance(expr, ObjectCreation):
            if expr.class_name not in self.classes:
                raise UndeclaredClass(expr.class_name)
            return expr.class_name
        elif isinstance(expr, ArrayLiteral):
            if not expr.value:  # Empty array
                return "unknown[]"
            # Check all elements have same type
            first_type = self.get_expression_type(expr.value[0])
            for elem in expr.value[1:]:
                elem_type = self.get_expression_type(elem)
                if elem_type != first_type:
                    raise IllegalArrayLiteral(expr)
            return f"{first_type}[]"
        elif isinstance(expr, StaticMemberAccess):
            return self.get_static_member_type(expr)
        elif isinstance(expr, ThisExpression):
            if self.current_class:
                return self.current_class.name
            return "unknown"
        elif isinstance(expr, ParenthesizedExpression):
            return self.get_expression_type(expr.expr)
        else:
            return "unknown"
    
    def get_binary_op_type(self, expr: BinaryOp) -> str:
        """Get type of binary operation."""
        left_type = self.get_expression_type(expr.left)
        right_type = self.get_expression_type(expr.right)
        
        # Arithmetic operators
        if expr.operator in ["+", "-", "*", "/", "%"]:
            if left_type in ["int", "float"] and right_type in ["int", "float"]:
                # If either is float, result is float
                if left_type == "float" or right_type == "float":
                    return "float"
                return "int"
            else:
                raise TypeMismatchInExpression(expr)
        
        # String concatenation
        elif expr.operator == "^":
            if left_type == "string" and right_type == "string":
                return "string"
            else:
                raise TypeMismatchInExpression(expr)
        
        # Comparison operators
        elif expr.operator in ["==", "!=", "<", "<=", ">", ">="]:
            if left_type in ["int", "float"] and right_type in ["int", "float"]:
                return "boolean"
            elif left_type == right_type:
                return "boolean"
            else:
                raise TypeMismatchInExpression(expr)
        
        # Logical operators
        elif expr.operator in ["&&", "||"]:
            if left_type == "boolean" and right_type == "boolean":
                return "boolean"
            else:
                raise TypeMismatchInExpression(expr)
        
        else:
            raise TypeMismatchInExpression(expr)
    
    def get_unary_op_type(self, expr: UnaryOp) -> str:
        """Get type of unary operation."""
        operand_type = self.get_expression_type(expr.operand)
        
        if expr.operator in ["+", "-"]:
            if operand_type in ["int", "float"]:
                return operand_type
            else:
                raise TypeMismatchInExpression(expr)
        elif expr.operator == "!":
            if operand_type == "boolean":
                return "boolean"
            else:
                raise TypeMismatchInExpression(expr)
        else:
            raise TypeMismatchInExpression(expr)
    
    def get_postfix_type(self, expr: PostfixExpression) -> str:
        """Get type of postfix expression."""
        primary_type = self.get_expression_type(expr.primary)
        result_type = primary_type
        
        for op in expr.postfix_ops:
            if isinstance(op, ArrayAccess):
                # Check if current type is array
                if not result_type.endswith("]"):
                    raise TypeMismatchInExpression(expr)
                # Check index is int
                index_type = self.get_expression_type(op.index)
                if index_type != "int":
                    raise TypeMismatchInExpression(expr)
                # Extract element type
                result_type = result_type.split("[")[0]
            elif isinstance(op, MemberAccess):
                # Check if current type is a class
                if result_type not in self.classes:
                    raise TypeMismatchInExpression(expr)
                # Find attribute in class
                class_symbol = self.classes[result_type]
                if op.member_name not in class_symbol.attributes:
                    raise UndeclaredAttribute(op.member_name)
                attr = class_symbol.attributes[op.member_name]
                # Check if accessing static member via instance
                if attr.is_static:
                    raise IllegalMemberAccess(expr)
                result_type = attr.type
            elif isinstance(op, MethodCall):
                # Check if current type is a class
                if result_type not in self.classes:
                    raise TypeMismatchInExpression(expr)
                # Find method in class
                class_symbol = self.classes[result_type]
                if op.method_name not in class_symbol.methods:
                    raise UndeclaredMethod(op.method_name)
                method = class_symbol.methods[op.method_name]
                # Check if accessing static method via instance
                if method.is_static:
                    raise IllegalMemberAccess(expr)
                # Check if method returns void (not allowed in expression)
                if method.type == "void":
                    raise TypeMismatchInExpression(expr)
                # Check arguments
                self.check_method_arguments(op.args, method.params)
                result_type = method.type
        
        return result_type
    
    def get_static_member_type(self, expr: StaticMemberAccess) -> str:
        """Get type of static member access."""
        if expr.class_name not in self.classes:
            raise UndeclaredClass(expr.class_name)
        
        class_symbol = self.classes[expr.class_name]
        
        # Check if it's an attribute
        if expr.member_name in class_symbol.attributes:
            attr = class_symbol.attributes[expr.member_name]
            if not attr.is_static:
                raise IllegalMemberAccess(expr)
            return attr.type
        
        # Check if it's a method (not allowed in expression unless called)
        if expr.member_name in class_symbol.methods:
            raise TypeMismatchInExpression(expr)  # Method reference without call
        
        raise UndeclaredAttribute(expr.member_name)
    
    def check_method_arguments(self, args: List[Expr], params: List[tuple]):
        """Check method call arguments against parameters."""
        if len(args) != len(params):
            raise TypeMismatchInExpression(f"Wrong number of arguments")
        
        for i, (arg, (param_name, param_type)) in enumerate(zip(args, params)):
            arg_type = self.get_expression_type(arg)
            if not self.type_compatible(arg_type, param_type):
                raise TypeMismatchInExpression(f"Argument {i+1} type mismatch")
    
    def is_constant_expression(self, expr: Expr) -> bool:
        """Check if expression is a valid constant expression."""
        if expr is None:
            return False
        
        if isinstance(expr, (IntLiteral, FloatLiteral, BoolLiteral, StringLiteral)):
            return True
        
        if isinstance(expr, BinaryOp):
            return (self.is_constant_expression(expr.left) and 
                   self.is_constant_expression(expr.right))
        
        if isinstance(expr, UnaryOp):
            return self.is_constant_expression(expr.operand)
        
        if isinstance(expr, Identifier):
            symbol = self.current_scope.resolve(expr.name)
            return symbol and isinstance(symbol, (AttributeSymbol, VariableSymbol)) and symbol.is_final
        
        # Arrays, method calls, etc. are not constant
        return False
    
    # Visitor methods
    def visit_program(self, node: Program, o: Any = None):
        # First pass: collect all class declarations
        for class_decl in node.class_decls:
            if class_decl.name in self.classes:
                raise Redeclared("Class", class_decl.name)
            self.classes[class_decl.name] = ClassSymbol(class_decl.name, class_decl.superclass)
        
        # Second pass: process class contents
        for class_decl in node.class_decls:
            self.visit(class_decl)
    
    def visit_class_decl(self, node: ClassDecl, o: Any = None):
        # Check superclass exists
        if node.superclass and node.superclass not in self.classes:
            raise UndeclaredClass(node.superclass)
        
        self.current_class = self.classes[node.name]
        class_scope = self.enter_scope(f"class_{node.name}")
        
        # Process members
        for member in node.members:
            self.visit(member)
        
        self.exit_scope()
        self.current_class = None
    
    def visit_attribute_decl(self, node: AttributeDecl, o: Any = None):
        attr_type = self.type_to_string(node.attr_type)
        
        for attr in node.attributes:
            # Check for redeclaration
            if attr.name in self.current_class.attributes:
                raise Redeclared("Attribute", attr.name)
            
            # Check initialization type compatibility
            if attr.init_value:
                if node.is_final:
                    if not self.is_constant_expression(attr.init_value):
                        raise IllegalConstantExpression(attr.init_value)
                
                init_type = self.get_expression_type(attr.init_value)
                if not self.type_compatible(init_type, attr_type):
                    if node.is_final:
                        raise TypeMismatchInConstant(node)
                    else:
                        raise TypeMismatchInStatement(node)
            
            # Add to class symbol table
            attr_symbol = AttributeSymbol(attr.name, attr_type, node.is_static, node.is_final)
            self.current_class.attributes[attr.name] = attr_symbol
    
    def visit_attribute(self, node: Attribute, o: Any = None):
        # Handled in visit_attribute_decl
        pass
    
    def visit_method_decl(self, node: MethodDecl, o: Any = None):
        return_type = self.type_to_string(node.return_type)
        
        # Check for redeclaration
        if node.name in self.current_class.methods:
            raise Redeclared("Method", node.name)
        
        # Create method symbol
        params = [(p.name, self.type_to_string(p.param_type)) for p in node.params]
        method_symbol = MethodSymbol(node.name, return_type, params, node.is_static)
        self.current_class.methods[node.name] = method_symbol
        
        # Enter method scope
        self.current_method = method_symbol
        method_scope = self.enter_scope(f"method_{node.name}")
        
        # Add parameters to scope
        for param in node.params:
            param_symbol = VariableSymbol(param.name, self.type_to_string(param.param_type))
            if not method_scope.define(param_symbol):
                raise Redeclared("Parameter", param.name)
        
        # Visit method body
        self.visit(node.body)
        
        # Exit method scope
        self.exit_scope()
        self.current_method = None
    
    def visit_constructor_decl(self, node: ConstructorDecl, o: Any = None):
        # Similar to method but no return type
        if node.name in self.current_class.methods:
            raise Redeclared("Method", node.name)
        
        params = [(p.name, self.type_to_string(p.param_type)) for p in node.params]
        method_symbol = MethodSymbol(node.name, "void", params, False)
        self.current_class.methods[node.name] = method_symbol
        
        self.current_method = method_symbol
        method_scope = self.enter_scope(f"constructor_{node.name}")
        
        for param in node.params:
            param_symbol = VariableSymbol(param.name, self.type_to_string(param.param_type))
            if not method_scope.define(param_symbol):
                raise Redeclared("Parameter", param.name)
        
        self.visit(node.body)
        
        self.exit_scope()
        self.current_method = None
    
    def visit_destructor_decl(self, node: DestructorDecl, o: Any = None):
        # Similar to constructor
        if node.name in self.current_class.methods:
            raise Redeclared("Method", node.name)
        
        method_symbol = MethodSymbol(node.name, "void", [], False)
        self.current_class.methods[node.name] = method_symbol
        
        self.current_method = method_symbol
        method_scope = self.enter_scope(f"destructor_{node.name}")
        
        self.visit(node.body)
        
        self.exit_scope()
        self.current_method = None
    
    def visit_parameter(self, node: Parameter, o: Any = None):
        # Handled in method/constructor declarations
        pass
    
    def visit_primitive_type(self, node: PrimitiveType, o: Any = None):
        pass
    
    def visit_array_type(self, node: ArrayType, o: Any = None):
        pass
    
    def visit_class_type(self, node: ClassType, o: Any = None):
        pass
    
    def visit_reference_type(self, node: ReferenceType, o: Any = None):
        pass
    
    def visit_block_statement(self, node: BlockStatement, o: Any = None):
        # Enter block scope
        block_scope = self.enter_scope("block")
        
        # Process variable declarations
        for var_decl in node.var_decls:
            self.visit(var_decl)
        
        # Process statements
        for stmt in node.statements:
            self.visit(stmt)
        
        # Exit block scope
        self.exit_scope()
    
    def visit_variable_decl(self, node: VariableDecl, o: Any = None):
        var_type = self.type_to_string(node.var_type)
        
        for var in node.variables:
            # Check for redeclaration
            if var.name in self.current_scope.symbols:
                raise Redeclared("Variable", var.name)
            
            # Check initialization
            if var.init_value:
                if node.is_final:
                    if not self.is_constant_expression(var.init_value):
                        raise IllegalConstantExpression(var.init_value)
                
                init_type = self.get_expression_type(var.init_value)
                if not self.type_compatible(init_type, var_type):
                    if node.is_final:
                        raise TypeMismatchInConstant(node)
                    else:
                        raise TypeMismatchInStatement(node)
            elif node.is_final:
                # Final variables must be initialized
                raise IllegalConstantExpression(node)
            
            # Add to scope
            var_symbol = VariableSymbol(var.name, var_type, node.is_final)
            self.current_scope.define(var_symbol)
    
    def visit_variable(self, node: Variable, o: Any = None):
        # Handled in visit_variable_decl
        pass
    
    def visit_assignment_statement(self, node: AssignmentStatement, o: Any = None):
        # Check if assigning to constant
        if isinstance(node.lhs, IdLHS):
            symbol = self.current_scope.resolve(node.lhs.name)
            if symbol and isinstance(symbol, (VariableSymbol, AttributeSymbol)) and symbol.is_final:
                raise CannotAssignToConstant(node)
        elif isinstance(node.lhs, PostfixLHS):
            # Check if accessing final attribute through member access
            # This would require more complex analysis
            pass
        
        # Type check assignment
        lhs_type = self.get_lhs_type(node.lhs)
        rhs_type = self.get_expression_type(node.rhs)
        
        if not self.type_compatible(rhs_type, lhs_type):
            raise TypeMismatchInStatement(node)
    
    def get_lhs_type(self, lhs: LHS) -> str:
        """Get the type of left-hand side in assignment."""
        if isinstance(lhs, IdLHS):
            symbol = self.current_scope.resolve(lhs.name)
            if not symbol:
                raise UndeclaredIdentifier(lhs.name)
            return symbol.type
        elif isinstance(lhs, PostfixLHS):
            return self.get_postfix_type(lhs.postfix_expr)
        return "unknown"
    
    def visit_if_statement(self, node: IfStatement, o: Any = None):
        # Check condition is boolean
        condition_type = self.get_expression_type(node.condition)
        if condition_type != "boolean":
            raise TypeMismatchInStatement(node)
        
        # Visit branches
        self.visit(node.then_stmt)
        if node.else_stmt:
            self.visit(node.else_stmt)
    
    def visit_for_statement(self, node: ForStatement, o: Any = None):
        # Check start and end expressions are integers
        start_type = self.get_expression_type(node.start_expr)
        end_type = self.get_expression_type(node.end_expr)
        
        if start_type != "int":
            raise TypeMismatchInStatement(node)
        if end_type != "int":
            raise TypeMismatchInStatement(node)
        
        # Check if variable is final
        symbol = self.current_scope.resolve(node.variable)
        if symbol and isinstance(symbol, (VariableSymbol, AttributeSymbol)) and symbol.is_final:
            raise CannotAssignToConstant(node)
        
        # Enter loop context
        old_in_loop = self.in_loop
        self.in_loop = True
        
        # Visit body
        self.visit(node.body)
        
        # Restore loop context
        self.in_loop = old_in_loop
    
    def visit_break_statement(self, node: BreakStatement, o: Any = None):
        if not self.in_loop:
            raise MustInLoop(node)
    
    def visit_continue_statement(self, node: ContinueStatement, o: Any = None):
        if not self.in_loop:
            raise MustInLoop(node)
    
    def visit_return_statement(self, node: ReturnStatement, o: Any = None):
        if not self.current_method:
            return  # Should not happen in well-formed AST
        
        return_type = self.get_expression_type(node.value)
        expected_type = self.current_method.type
        
        if not self.type_compatible(return_type, expected_type):
            raise TypeMismatchInStatement(node)
    
    def visit_method_invocation_statement(self, node: MethodInvocationStatement, o: Any = None):
        # Check the method invocation
        self.visit(node.method_invocation)
    
    def visit_id_lhs(self, node: IdLHS, o: Any = None):
        pass
    
    def visit_postfix_lhs(self, node: PostfixLHS, o: Any = None):
        pass
    
    def visit_binary_op(self, node: BinaryOp, o: Any = None):
        # Type checking is done in get_binary_op_type
        self.get_binary_op_type(node)
    
    def visit_unary_op(self, node: UnaryOp, o: Any = None):
        # Type checking is done in get_unary_op_type
        self.get_unary_op_type(node)
    
    def visit_postfix_expression(self, node: PostfixExpression, o: Any = None):
        # Type checking is done in get_postfix_type
        self.get_postfix_type(node)
    
    def visit_method_call(self, node: MethodCall, o: Any = None):
        pass
    
    def visit_member_access(self, node: MemberAccess, o: Any = None):
        pass
    
    def visit_array_access(self, node: ArrayAccess, o: Any = None):
        pass
    
    def visit_object_creation(self, node: ObjectCreation, o: Any = None):
        # Check class exists
        if node.class_name not in self.classes:
            raise UndeclaredClass(node.class_name)
        
        # Check constructor arguments if needed
        # This would require more detailed constructor analysis
    
    def visit_static_member_access(self, node: StaticMemberAccess, o: Any = None):
        # Type checking done in get_static_member_type
        self.get_static_member_type(node)
    
    def visit_method_invocation(self, node: MethodInvocation, o: Any = None):
        # Visit the postfix expression
        self.visit(node.postfix_expr)
    
    def visit_static_method_invocation(self, node: StaticMethodInvocation, o: Any = None):
        # Check class exists
        if node.class_name not in self.classes:
            raise UndeclaredClass(node.class_name)
        
        # Check method exists and is static
        class_symbol = self.classes[node.class_name]
        if node.method_name not in class_symbol.methods:
            raise UndeclaredMethod(node.method_name)
        
        method = class_symbol.methods[node.method_name]
        if not method.is_static:
            raise IllegalMemberAccess(node)
        
        # Check arguments
        self.check_method_arguments(node.args, method.params)
    
    def visit_identifier(self, node: Identifier, o: Any = None):
        # Check if identifier is declared
        symbol = self.current_scope.resolve(node.name)
        if not symbol:
            raise UndeclaredIdentifier(node.name)
    
    def visit_this_expression(self, node: ThisExpression, o: Any = None):
        # Can only use 'this' in non-static methods
        if not self.current_method or self.current_method.is_static:
            raise TypeMismatchInExpression(node)
    
    def visit_parenthesized_expression(self, node: ParenthesizedExpression, o: Any = None):
        self.visit(node.expr)
    
    def visit_int_literal(self, node: IntLiteral, o: Any = None):
        pass
    
    def visit_float_literal(self, node: FloatLiteral, o: Any = None):
        pass
    
    def visit_bool_literal(self, node: BoolLiteral, o: Any = None):
        pass
    
    def visit_string_literal(self, node: StringLiteral, o: Any = None):
        pass
    
    def visit_array_literal(self, node: ArrayLiteral, o: Any = None):
        # Check all elements have same type
        if node.value:
            first_type = self.get_expression_type(node.value[0])
            for elem in node.value[1:]:
                elem_type = self.get_expression_type(elem)
                if elem_type != first_type:
                    raise IllegalArrayLiteral(node)
    
    def visit_nil_literal(self, node: NilLiteral, o: Any = None):
        pass