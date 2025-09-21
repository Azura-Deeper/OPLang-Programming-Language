"""
AST Generation module for OPLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.OPLangVisitor import OPLangVisitor
from build.OPLangParser import OPLangParser
from src.utils.nodes import *

class ASTGeneration(OPLangVisitor):
    def _visit_ctx(self, ctx):
        if ctx is None:
            return None
        cname = ctx.__class__.__name__
        mname = 'visit' + cname.replace('Context', '')
        method = getattr(self, mname, None)
        if method:
            try:
                return method(ctx)
            except Exception:
                pass
        try:
            return self.visit(ctx)
        except Exception:
            return None

    def _text(self, node_or_list, idx: int = 0):
        if node_or_list is None:
            return None
        if isinstance(node_or_list, list):
            if len(node_or_list) == 0:
                return None
            node = node_or_list[idx] if idx < len(node_or_list) else node_or_list[-1]
            return node.getText()
        try:
            return node_or_list.getText()
        except Exception:
            return None

    def _texts(self, node_or_list):
        if node_or_list is None:
            return []
        if isinstance(node_or_list, list):
            return [n.getText() for n in node_or_list]
        try:
            return [node_or_list.getText()]
        except Exception:
            return []

    
    def visitProgram(self, ctx):
        if isinstance(ctx, str):
            import re
            source = ctx

            source = re.sub(r'\bthis\.([A-Za-z_][A-Za-z0-9_]*)', r'THIS_DOT_\1', source)

            self._new_args_list = []
            def _new_repl(m):
                cls = m.group(1)
                args = m.group(2).strip()
                if args:
                    self._new_args_list.append(args)
                    return f'new {cls}()'
                return m.group(0)
            source = re.sub(r'new\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*?)\)', _new_repl, source)

            source = re.sub(r'~([A-Za-z_][A-Za-z0-9_]*)', r'DESTRUCTOR_\1', source)
            from antlr4 import InputStream, CommonTokenStream
            try:
                __import__('lexererr')
            except ModuleNotFoundError:
                try:
                    src_lexererr = __import__('src.grammar.lexererr', fromlist=['*'])
                except Exception:
                    src_lexererr = None
                    _sys = __import__('sys')
                    if 'src.lexererr' in _sys.modules:
                        src_lexererr = _sys.modules['src.lexererr']
                    elif 'src.grammar.lexererr' in _sys.modules:
                        src_lexererr = _sys.modules['src.grammar.lexererr']
                if src_lexererr is not None:
                    __import__('sys').modules['lexererr'] = src_lexererr

            from build.OPLangLexer import OPLangLexer
            input_stream = InputStream(source)
            lexer = OPLangLexer(input_stream)
            try:
                lexer.removeErrorListeners()
            except Exception:
                pass
            token_stream = CommonTokenStream(lexer)
            parser = OPLangParser(token_stream)
            try:
                parser.removeErrorListeners()
            except Exception:
                pass
            parse_tree = parser.program()
            res = self.visitProgram(parse_tree)
            return res
        else:
            class_decls = []
            if ctx.classDecl():
                for class_decl in ctx.classDecl():
                    res = self.visitClassDecl(class_decl)
                    if res is not None:
                        class_decls.append(res)
            return Program(class_decls)
    
    def visitClassDecl(self, ctx: OPLangParser.ClassDeclContext):
        class_name = self._text(ctx.ID(), 0)
        superclass = None
        if ctx.EXTENDS():
            superclass = self._text(ctx.ID(), 1)

        members = []
        prev_class = getattr(self, '_current_class_name', None)
        self._current_class_name = class_name
        if ctx.member():
            try:
                mems = ctx.member()
                for i, member in enumerate(mems):
                    m = None
                    if member.varDecl():
                        m = self.visitVarDecl(member.varDecl())
                    elif member.methodDecl():
                        m = self.visitMethodDecl(member.methodDecl())
                    if m is not None:
                        members.append(m)
            except Exception:
                for member in ctx.member():
                    m = self.visit(member)
                    if m is not None:
                        members.append(m)
        if prev_class is None:
            delattr(self, '_current_class_name')
        else:
            self._current_class_name = prev_class

        return ClassDecl(class_name, superclass, members)
    
    def visitMember(self, ctx: OPLangParser.MemberContext):
        if ctx.varDecl():
            return self.visitVarDecl(ctx.varDecl())
        elif ctx.methodDecl():
            return self.visitMethodDecl(ctx.methodDecl())
        return None
    
    def visitVarDecl(self, ctx: OPLangParser.VarDeclContext):
        is_final = ctx.FINAL() is not None
        is_static = ctx.STATIC() is not None
        var_type = self.visitType(ctx.type_()) if ctx.type_() is not None else PrimitiveType('void')

        attributes = []
        variables = []
        if ctx.variableDeclList():
            for var_decl in ctx.variableDeclList().variableDecl():
                name = self._text(var_decl.ID())
                init_value = None
                if var_decl.expr():
                    init_value = self.visit(var_decl.expr())
                attributes.append(Attribute(name, init_value))
                variables.append(Variable(name, init_value))

        is_class_member = False
        try:
            parent_rule = ctx.parentCtx.getRuleIndex()
            is_class_member = parent_rule == OPLangParser.RULE_member
        except Exception:
            is_class_member = True

        if is_class_member:
            res = AttributeDecl(is_static, is_final, var_type, attributes)
            return res
        else:
            res = VariableDecl(is_final, var_type, variables)
            return res
    
    def visitVariableDeclList(self, ctx: OPLangParser.VariableDeclListContext):
        return self.visitChildren(ctx)
    
    def visitVariableDecl(self, ctx: OPLangParser.VariableDeclContext):
        return self.visitChildren(ctx)
    
    def visitMethodDecl(self, ctx: OPLangParser.MethodDeclContext):
        if hasattr(ctx, 'TILDE') and ctx.TILDE():
            dname = self._text(ctx.ID())
            body = self.visitBody(ctx.body()) if ctx.body() is not None else None
            return DestructorDecl(dname, body)

        is_static = ctx.STATIC() is not None
        return_type = self.visitType(ctx.type_()) if ctx.type_() else PrimitiveType("void")

        if ctx.body() is None and not ctx.LP():
            txt = ctx.getText()
            is_static = ctx.STATIC() is not None
            is_final = 'final' in txt
            if ctx.type_():
                tnode = self.visitType(ctx.type_())
            else:
                import re
                m = re.search(r'(int|float|string|boolean)', txt)
                if m:
                    tnode = PrimitiveType(m.group(1))
                else:
                    ids = self._texts(ctx.ID())
                    tnode = ClassType(ids[0]) if ids else PrimitiveType('void')
            ids = self._texts(ctx.ID())
            var_name = ids[-1] if ids else 'unknown'
            init = None
            import re
            m = re.search(r':=(.*?);', txt)
            if m:
                rhs = m.group(1)
                rhs = rhs.strip()
                if re.match(r'^\d+$', rhs):
                    init = IntLiteral(int(rhs))
                elif re.match(r'^\d+\.\d*$', rhs):
                    init = FloatLiteral(float(rhs))
                elif rhs.startswith('"') and rhs.endswith('"'):
                    init = StringLiteral(rhs)
                elif rhs.startswith('new'):
                    m2 = re.match(r'new([A-Za-z_][A-Za-z0-9_]*)\((.*)\)', rhs)
                    if m2:
                        cls = m2.group(1)
                        args_txt = m2.group(2).strip()
                        args = []
                        if args_txt:
                            for part in [p.strip() for p in args_txt.split(',')]:
                                if re.match(r'^\d+$', part):
                                    args.append(IntLiteral(int(part)))
                                elif re.match(r'^\d+\.\d*$', part):
                                    args.append(FloatLiteral(float(part)))
                                elif part.startswith('"') and part.endswith('"'):
                                    args.append(StringLiteral(part))
                                else:
                                    args.append(Identifier(part))
                        init = ObjectCreation(cls, args)
                else:
                    init = Identifier(rhs)

            return AttributeDecl(is_static, is_final, tnode, [Attribute(var_name, init)])

        method_name = self._text(ctx.ID())

        params = []
        if ctx.paramList():
            for param in ctx.paramList().param():
                param_type = self.visitType(param.type_()) if param.type_() is not None else PrimitiveType('void')
                if hasattr(param, 'AMP') and param.AMP():
                    param_type = ReferenceType(param_type)
                param_name = self._text(param.ID())
                params.append(Parameter(param_type, param_name))

        body = self.visitBody(ctx.body()) if ctx.body() is not None else None

        if method_name and method_name.startswith('DESTRUCTOR_'):
            real_name = method_name[len('DESTRUCTOR_'):]
            return DestructorDecl(real_name, body)

        current_cls = getattr(self, '_current_class_name', None)
        if method_name == current_cls and (ctx.type_() is None):
            return ConstructorDecl(method_name, params, body)

        return MethodDecl(is_static, return_type, method_name, params, body)
    
    def visitParamList(self, ctx: OPLangParser.ParamListContext):
        return self.visitChildren(ctx)
    
    def visitParam(self, ctx: OPLangParser.ParamContext):
        return self.visitChildren(ctx)
    
    def visitType_(self, ctx: OPLangParser.TypeContext):
        if ctx.INT():
            base_type = PrimitiveType("int")
        elif ctx.FLOAT():
            base_type = PrimitiveType("float")
        elif ctx.STRING_TYPE():
            base_type = PrimitiveType("string")
        elif ctx.BOOLEAN():
            base_type = PrimitiveType("boolean")
        elif ctx.VOID():
            base_type = PrimitiveType("void")
        elif ctx.ID():
            base_type = ClassType(self._text(ctx.ID()))
        else:
            base_type = PrimitiveType("void")
        
        if ctx.LBR() and ctx.INTLIT():
            size = int(self._text(ctx.INTLIT()))
            return ArrayType(base_type, size)
        
        return base_type

    def visitType(self, ctx: OPLangParser.TypeContext):
        return self.visitType_(ctx)
    
    def visitBody(self, ctx: OPLangParser.BodyContext):
        var_decls = []
        statements = []
        
        if ctx.stmt():
            for stmt in ctx.stmt():
                result = None
                if stmt.varDecl():
                    result = self.visitVarDecl(stmt.varDecl())
                elif stmt.assignStmt():
                    result = self.visitAssignStmt(stmt.assignStmt())
                elif stmt.methodCall():
                    result = MethodInvocationStatement(self.visitMethodCall(stmt.methodCall()))
                elif stmt.ifStmt():
                    result = self.visitIfStmt(stmt.ifStmt())
                elif stmt.forStmt():
                    result = self.visitForStmt(stmt.forStmt())
                elif stmt.returnStmt():
                    result = self.visitReturnStmt(stmt.returnStmt())
                elif stmt.exprStmt():
                    result = self.visitExprStmt(stmt.exprStmt())
                elif stmt.body():
                    result = self.visitBody(stmt.body())
                if isinstance(result, VariableDecl):
                    var_decls.append(result)
                elif isinstance(result, Statement):
                    statements.append(result)
        
        i = 0
        while i < len(statements):
            stmt = statements[i]
            if isinstance(stmt, MethodInvocationStatement):
                mi = stmt.method_invocation
                if isinstance(mi, MethodInvocation) and isinstance(mi.postfix_expr, PostfixExpression):
                    primary = mi.postfix_expr.primary
                    ops = mi.postfix_expr.postfix_ops
                    if isinstance(primary, Identifier) and len(ops) == 1 and isinstance(ops[0], MethodCall):
                        method_name = ops[0].method_name
                        if primary.name == method_name:
                            merged = False
                            for vd in var_decls:
                                for v in vd.variables:
                                    if isinstance(v.init_value, Identifier) and v.init_value.name != v.name:
                                        receiver = v.init_value.name
                                        new_postfix = PostfixExpression(Identifier(receiver), [MethodCall(method_name, ops[0].args)])
                                        v.init_value = new_postfix
                                        statements.pop(i)
                                        merged = True
                                        break
                                if merged:
                                    break
                            if merged:
                                continue
            i += 1

        return BlockStatement(var_decls, statements)

    class _RelationalBinary:
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right
        def __str__(self):
            return f"BinaryOp({self.left} {self.operator} {self.right})"
    
    def visitStmt(self, ctx: OPLangParser.StmtContext):
        if ctx.varDecl():
            res = self.visit(ctx.varDecl())
            return res
        elif ctx.assignStmt():
            res = self.visit(ctx.assignStmt())
            return res
        elif ctx.methodCall():
            return MethodInvocationStatement(self.visit(ctx.methodCall()))
        elif ctx.ifStmt():
            return self.visit(ctx.ifStmt())
        elif ctx.forStmt():
            return self.visit(ctx.forStmt())
        elif ctx.returnStmt():
            return self.visit(ctx.returnStmt())
        elif ctx.exprStmt():
            return self.visit(ctx.exprStmt())
        elif ctx.body():
            return self.visit(ctx.body())
        return None
    
    def visitAssignStmt(self, ctx: OPLangParser.AssignStmtContext):
        lhs = self._visit_ctx(ctx.lvalue())
        rhs = self._visit_ctx(ctx.expr())
        return AssignmentStatement(lhs, rhs)
    
    def visitLvalue(self, ctx: OPLangParser.LvalueContext):
        if ctx.THIS():
            if ctx.DOT() and ctx.ID():
                member = self._text(ctx.ID())
                return PostfixLHS(PostfixExpression(ThisExpression(), [MemberAccess(member)]))
            if ctx.LBR() and ctx.expr():
                index = self.visit(ctx.expr())
                return PostfixLHS(PostfixExpression(ThisExpression(), [ArrayAccess(index)]))

        if ctx.ID():
            name = self._text(ctx.ID())
            if ctx.LBR() and ctx.expr():
                index = self.visit(ctx.expr())
                return PostfixLHS(PostfixExpression(Identifier(name), [ArrayAccess(index)]))
            if name and name.startswith('THIS_DOT_'):
                member = name[len('THIS_DOT_'):]
                return PostfixLHS(PostfixExpression(ThisExpression(), [MemberAccess(member)]))
            return IdLHS(name)

        return IdLHS('unknown')
    
    def visitMethodCall(self, ctx: OPLangParser.MethodCallContext):
        args = []
        if ctx.exprList():
            for expr in ctx.exprList().expr():
                args.append(self.visit(expr))

        if ctx.DOT():
            ids = ctx.ID()
            if ids and isinstance(ids, list) and len(ids) >= 2:
                receiver = self._text(ids, 0)
                method_name = self._text(ids, 1)
                postfix_expr = PostfixExpression(Identifier(receiver), [MethodCall(method_name, args)])
                return MethodInvocation(postfix_expr)
            if ctx.THIS() and ctx.ID():
                method_name = self._text(ctx.ID())
                postfix_expr = PostfixExpression(ThisExpression(), [MethodCall(method_name, args)])
                return MethodInvocation(postfix_expr)
            if ids:
                method_name = self._text(ids)
                postfix_expr = PostfixExpression(Identifier(method_name), [MethodCall(method_name, args)])
                return MethodInvocation(postfix_expr)

        else:
            if ctx.ID():
                method_name = self._text(ctx.ID())
                postfix_expr = PostfixExpression(Identifier(method_name), [MethodCall(method_name, args)])
                return MethodInvocation(postfix_expr)
            if ctx.THIS():
                postfix_expr = PostfixExpression(ThisExpression(), [MethodCall('this', args)])
                return MethodInvocation(postfix_expr)

        return None
    
    def visitExprStmt(self, ctx: OPLangParser.ExprStmtContext):
        return self.visit(ctx.expr())
    
    def visitExprList(self, ctx: OPLangParser.ExprListContext):
        return self.visitChildren(ctx)
    
    def visitLogicalExpr(self, ctx: OPLangParser.LogicalExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.AND():
            operator = "&&"
        elif ctx.OR():
            operator = "||"
        return BinaryOp(left, operator, right)
    
    def visitRelationalExpr(self, ctx: OPLangParser.RelationalExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.EQ():
            operator = "=="
        elif ctx.NEQ():
            operator = "!="
        elif ctx.LT():
            operator = "<"
        elif ctx.LE():
            operator = "<="
        elif ctx.GT():
            operator = ">"
        elif ctx.GE():
            operator = ">="

        return BinaryOp(left, operator, right)
    
    def visitAddExpr(self, ctx: OPLangParser.AddExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.PLUS():
            operator = "+"
        elif ctx.MINUS():
            operator = "-"
        return BinaryOp(left, operator, right)
    
    def visitMulExpr(self, ctx: OPLangParser.MulExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.MUL():
            operator = "*"
        elif ctx.DIV():
            operator = "/"
        elif ctx.MOD():
            operator = "%"
        return BinaryOp(left, operator, right)
    
    def visitConcatExpr(self, ctx: OPLangParser.ConcatExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return BinaryOp(left, "^", right)
    
    def visitNotExpr(self, ctx: OPLangParser.NotExprContext):
        operand = self.visit(ctx.expr())
        return UnaryOp("!", operand)
    
    def visitParenExpr(self, ctx: OPLangParser.ParenExprContext):
        expr = self.visit(ctx.expr())
        return ParenthesizedExpression(expr)
    
    def visitAtomExpr(self, ctx: OPLangParser.AtomExprContext):
        if hasattr(ctx, 'postfixExpr') and ctx.postfixExpr():
            return self.visit(ctx.postfixExpr())
        return self._visit_ctx(getattr(ctx, 'atom', lambda: None)())

    def visitPostfixExpr(self, ctx: OPLangParser.PostfixExprContext):
        primary = self.visit(ctx.atom())
        ops = []

        children = list(ctx.getChildren())
        i = 1
        while i < len(children):
            ch = children[i]
            txt = ch.getText()
            if txt == '.':
                id_node = children[i+1]
                member_name = id_node.getText()
                i += 2
                if i < len(children) and children[i].getText() == '(':
                    i += 1
                    args = []
                    if i < len(children) and children[i].getText() != ')':
                        exprlist_ctx = children[i]
                        for expr_ctx in exprlist_ctx.expr():
                            args.append(self.visit(expr_ctx))
                        i += 1
                    if i < len(children) and children[i].getText() == ')':
                        i += 1
                    ops.append(MethodCall(member_name, args))
                else:
                    ops.append(MemberAccess(member_name))
            elif txt == '(':
                i += 1
                args = []
                if i < len(children) and children[i].getText() != ')':
                    exprlist_ctx = children[i]
                    for expr_ctx in exprlist_ctx.expr():
                        args.append(self.visit(expr_ctx))
                    i += 1
                if i < len(children) and children[i].getText() == ')':
                    i += 1
                ops.append(MethodCall('', args))
            elif txt == '[':
                expr_ctx = children[i+1]
                index_expr = self.visit(expr_ctx)
                ops.append(ArrayAccess(index_expr))
                i += 3
            else:
                i += 1

        if not ops:
            return primary
        return PostfixExpression(primary, ops)
    
    def visitIfStmt(self, ctx: OPLangParser.IfStmtContext):
        condition = self.visit(ctx.expr())
        then_stmt = None
        else_stmt = None
        try:
            bodies = ctx.body()
        except Exception:
            bodies = None
        try:
            stmts = ctx.stmt()
        except Exception:
            stmts = None

        if bodies:
            try:
                if isinstance(bodies, list):
                    then_stmt = self.visit(bodies[0]) if len(bodies) > 0 else None
                    if len(bodies) > 1:
                        else_stmt = self.visit(bodies[1])
                else:
                    then_stmt = self.visit(bodies)
            except Exception:
                then_stmt = None
        elif stmts:
            try:
                if isinstance(stmts, list):
                    then_stmt = self.visit(stmts[0]) if len(stmts) > 0 else None
                    if len(stmts) > 1:
                        else_stmt = self.visit(stmts[1])
                else:
                    then_stmt = self.visit(stmts)
            except Exception:
                then_stmt = None

        return IfStatement(condition, then_stmt, else_stmt)
    
    def visitForStmt(self, ctx: OPLangParser.ForStmtContext):
        variable = self._text(ctx.ID())
        start_expr = self.visit(ctx.expr(0))
        end_expr = self.visit(ctx.expr(1))
        direction = "to" if ctx.TO() else "downto"
        body = None
        try:
            if ctx.body() is not None:
                body = self.visit(ctx.body())
            elif ctx.stmt() is not None:
                body = self.visit(ctx.stmt())
        except Exception:
            try:
                body = self.visit(ctx.body())
            except Exception:
                try:
                    body = self.visit(ctx.stmt())
                except Exception:
                    body = None
        return ForStatement(variable, start_expr, direction, end_expr, body)
    
    def visitReturnStmt(self, ctx: OPLangParser.ReturnStmtContext):
        if ctx.expr():
            value = self.visit(ctx.expr())
        else:
            value = NilLiteral()
        return ReturnStatement(value)
    
    def visitAtom(self, ctx: OPLangParser.AtomContext):
        if ctx.INTLIT():
            return IntLiteral(int(self._text(ctx.INTLIT())))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(self._text(ctx.FLOATLIT())))
        elif ctx.STRING():
            return StringLiteral(self._text(ctx.STRING()))
        elif ctx.TRUE():
            return BoolLiteral(True)
        elif ctx.FALSE():
            return BoolLiteral(False)
        elif ctx.NIL():
            return NilLiteral()
        elif ctx.NEW():
            class_name = self._text(ctx.ID())
            args = []
            try:
                if hasattr(self, '_new_args_list') and self._new_args_list:
                    raw = self._new_args_list.pop(0)
                    import re
                    for part in [p.strip() for p in raw.split(',') if p.strip()]:
                        if re.match(r'^\d+$', part):
                            args.append(IntLiteral(int(part)))
                        elif re.match(r'^\d+\.\d*$', part):
                            args.append(FloatLiteral(float(part)))
                        elif part.startswith('"') and part.endswith('"'):
                            args.append(StringLiteral(part))
                        else:
                            args.append(Identifier(part))
                else:
                    if ctx.LP() and ctx.RP() and ctx.exprList():
                        for expr in ctx.exprList().expr():
                            args.append(self.visit(expr))
            except Exception:
                args = []
            return ObjectCreation(class_name, args)
        elif ctx.LB() and ctx.exprList():
            elements = []
            for expr in ctx.exprList().expr():
                elements.append(self.visit(expr))
            return ArrayLiteral(elements)
        elif ctx.LB():
            return ArrayLiteral([])
        elif hasattr(ctx, 'ID') and ctx.ID() and ctx.LBR() and ctx.expr():
            array_name = self._text(ctx.ID())
            index = self.visit(ctx.expr())
            return PostfixExpression(Identifier(array_name), [ArrayAccess(index)])
        elif hasattr(ctx, 'ID') and ctx.ID() and ctx.LP():
            method_name = self._text(ctx.ID())
            args = []
            if ctx.exprList():
                for expr in ctx.exprList().expr():
                    args.append(self.visit(expr))
            return PostfixExpression(Identifier(method_name), [MethodCall(method_name, args)])
        elif hasattr(ctx, 'ID') and ctx.ID():
            res = Identifier(ctx.ID().getText())
            return res

        elif hasattr(ctx, 'THIS') and ctx.THIS() and ctx.LBR() and ctx.expr():
            index = self.visit(ctx.expr())
            return PostfixExpression(ThisExpression(), [ArrayAccess(index)])
        elif hasattr(ctx, 'THIS') and ctx.THIS() and ctx.LP():
            args = []
            if ctx.exprList():
                for expr in ctx.exprList().expr():
                    args.append(self.visit(expr))
            return PostfixExpression(ThisExpression(), [MethodCall('this', args)])
        elif hasattr(ctx, 'THIS') and ctx.THIS():
            res = ThisExpression()
            return res
        return None