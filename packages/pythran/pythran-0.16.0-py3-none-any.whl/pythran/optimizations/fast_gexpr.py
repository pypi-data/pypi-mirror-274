""" Optimize a[...] = b[...] + c when we have no conflicting aliasing """

from pythran.analyses import Aliases
from pythran.passmanager import Transformation

import gast as ast


class FastGExpr(Transformation):

    def __init__(self):
        self.update = False
        super(FastGExpr, self).__init__(Aliases)

    def as_gexpr(self, node):
        if not isinstance(node, ast.Subscript):
            return None
        if not isinstance(node.slice, ast.Slice):
            return None

        if not isinstance(node.value, ast.Name):
            return None

        return node.value, node.slice

    def may_alias(self, gexpr, value):
        if isinstance(value, ast.Constant):
            return False
        if isinstance(value, (ast.List, ast.Tuple)):
            return any(self.may_alias(gexpr, elt) for elt in value.elts)
        if isinstance(value, ast.UnaryOp):
            return self.may_alias(gexpr, value.operand)
        if isinstance(value, ast.BinOp):
            return any(self.may_alias(gexpr, elt) for elt in (value.left,
                                                              value.right))
        if isinstance(value, ast.Subscript):
            if not isinstance(value.value, ast.Name):
                return True
            return gexpr[0] in self.aliases[value.value]

        return True

    def is_no_alias(self, expr):
        if not isinstance(expr, ast.Call):
            return False
        func = expr.func
        if not isinstance(func, ast.Attribute):
            return False

        if not isinstance(func.value, ast.Attribute):
            return False

        if not isinstance(func.value.value, ast.Name):
            return False

        return (func.value.value.id == "builtins" and
                func.value.attr == "pythran" and
                func.attr == "no_alias")

    def visit_Assign(self, node):
        target, = node.targets
        value = node.value
        gexpr = self.as_gexpr(target)
        if not gexpr:
            return node

        if self.is_no_alias(value):
            return node

        if self.may_alias(gexpr, value):
            return node

        self.update = True

        func = ast.Attribute(
            value=ast.Attribute(value=ast.Name('builtins', ast.Load(),
                                               None, None),
                                attr="pythran", ctx=ast.Load()),
            attr="no_alias", ctx=ast.Load())
        node.value = ast.Call(func, args=[value], keywords=[])
        return node

