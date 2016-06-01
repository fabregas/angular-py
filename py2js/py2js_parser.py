
import ast
from ast import *

class JsOut:
    def __init__(self):
        self.buf = ""
        self.ident = ""

    def add(self, item):
        for line in item.splitlines():
            self.buf += "{}{}\n".format(self.ident, line)

    def more_ident(self):
        self.ident += '\t'

    def less_ident(self):
        self.ident = self.ident[:-1]


class Py2JsParser(NodeVisitor):
    def __init__(self):
        self.out = JsOut()

    def _get_operator(self, left, right, op):
        opname = ""
        if isinstance(op, Add):
            opname = '+'
        elif isinstance(op, Sub):
            opname = '-'
        elif isinstance(op, Mult):
            opname = '*'
        elif isinstance(op, Div):
            opname = '/'
        elif isinstance(op, Mod):
            opname = '%'
        elif isinstance(op, FloorDiv):
            return "Math.floor({}/{})".format(left, right)
        elif isinstance(op, Pow):
            return "Math.pow({}, {})".format(left, right)
        else:
            raise RuntimeError("Unknown operator: {}".format(op))
        # basic operator case
        return "({} {} {})".format(left, opname, right)

    def _get_unary_operator(self, op):
        # Invert | Not | UAdd | USub
        if isinstance(op, Not):
            return "!"
        else:
            raise RuntimeError("Unknown unary operator: {}".format(op))

    def _get_bool_operator(self, op):
        if isinstance(op, And):
            return "&&"
        elif isinstance(op, Or):
            return "||"
        else:
            raise RuntimeError("Unknown bool operator: {}".format(op))

    def _get_comparator(self, cm):
        if isinstance(cm, Eq):
            return "__fab__eq"
        elif isinstance(cm, NotEq):
            return "__fab__neq"
        elif isinstance(cm, Lt):
            return "__fab__lt"
        elif isinstance(cm, LtE):
            return "__fab__lte"
        elif isinstance(cm, Gt):
            return "__fab__gt"
        elif isinstance(cm, GtE):
            return "__fab__gte"
        # Is | IsNot | In | NotIn

    def _get_slice(self, sl):
        if isinstance(sl, Slice):
            if sl.step is not None:
                raise RuntimeError("slice step is not supported!")
            ret = '.slice({}'.format(self._get_value(sl.lower) or 0)
            if sl.upper is not None:
                ret += ', {})'.format(self._get_value(sl.upper))
            else:
                ret += ')'
        elif isinstance(sl, ExtSlice):
            raise Exception('not implemented ExtSlice at {}'.format(sl.lineno))
        elif isinstance(sl, Index):
            return '[{}]'.format(self._get_value(sl.value))

    def _get_value(self, val):
        if isinstance(val, Str):
            return 'PyStr("%s")'%self._esc_js_str(val.s)
        elif isinstance(val, Bytes):
            return 'PyStr("%s")'%val.s.decode()
        elif isinstance(val, NameConstant):
            NAME_CONST = {False: 'false', True: 'true', None: 'null'}
            v = NAME_CONST.get(val.value)
            if v is None:
                raise RuntimeError(
                    "Unknown name constant: {}".format(val.value))
            return v
        elif isinstance(val, Name):
            return val.id
        elif isinstance(val, keyword):
            return "{}={}".format(val.arg, self._get_value(val.value))
        elif isinstance(val, Attribute):
            a_val = self._get_value(val.value)
            #if isinstance(val.value, Str):
            #    a_val = "PyStr({})".format(a_val)
            return "{}.{}".format(a_val, val.attr)
        elif isinstance(val, Num):
            return str(val.n)
        elif isinstance(val, Dict):
            return "{" + ",".join(["{}: {}".format(k,v) for (k,v) in zip(val.keys, val.values)]) + "}"
        elif isinstance(val, Tuple) or isinstance(val, List):
            return '[%s]'% ', '.join([self._get_value(v) for v in val.elts])
        elif isinstance(val, BinOp):
            return self._get_operator(
                self._get_value(val.left), self._get_value(val.right), val.op)
        elif isinstance(val, UnaryOp):
            op = self._get_unary_operator(val.op)
            return "({} {})".format(op, self._get_value(val.operand))
        elif isinstance(val, BoolOp):
            op = self._get_bool_operator(val.op)
            return "({} {} {})".format(
                self._get_value(val.values[0]), op, self._get_value(val.values[1]))
        elif isinstance(val, Compare):
            if len(val.ops) > 1:
                raise RuntimeError('multiple comparation is not supported now')
            return "{}({}, {})".format(
                self._get_comparator(val.ops[0]),
                self._get_value(val.left),
                self._get_value(val.comparators[0]))
        elif isinstance(val, Subscript):
            return "{}{}".format(
                self._get_value(val.value), self._get_slice(val.slice))
        elif isinstance(val, Call):
            func = self._get_value(val.func)
            if val.keywords:
                keywords = ', '.join(
                    [self._get_value(v) for v in val.keywords])
            else:
                keywords = ''
            if keywords and val.args:
                keywords = ', ' + keywords
            return "{}({}{})".format(
                func, ', '.join([self._get_value(v) for v in val.args]),
                keywords)
        elif isinstance(val, ListComp):
            gen = val.generators[0]
            ifv = gen.ifs[0]
            if ifv:
                if_val = "\n\t\tif (!{}) {{continue;}}".format(
                    self._get_value(ifv))
            else:
                if_val = ""
            return ("__tmp__ = new Array();"
                    "\n\tvar __iterable__ = {0};"
                    "\n\tfor (var __i__=0; __i__<__iterable__.length; __i__++) {{"
                    "\n\t\t{1} = __iterable__[__i__];{2}"
                    "\n\t\t__tmp__.push({3});"
                    "\n\t}}".format(self._get_value(gen.iter),
                                    self._get_value(gen.target),
                                    if_val,
                                    self._get_value(val.elt)))
        elif isinstance(val, DictComp):
            gen = val.generators[0]
            key, value = gen.target.elts
            ifv = gen.ifs[0]
            if ifv:
                if_val = "\n\t\tif (!{}) {{continue;}}".format(
                    self._get_value(ifv))
            else:
                if_val = ""
            return ("__tmp__ = {{}};"
                    "\n\tvar __dict__ = {0};"
                    "\n\tfor (var __key__ in __dict__) {{"
                    "\n\t{1} = __key__;"
                    "\n\t\t{2} = __dict__[__key__];{3}"
                    "\n\t\t__tmp__[{4}] = {5};"
                    "\n\t}}".format(self._get_value(gen.iter),
                                    self._get_value(key),
                                    self._get_value(value),
                                    if_val,
                                    self._get_value(val.key),
                                    self._get_value(val.value)))
        else:
            raise RuntimeError('unknown value: {} at line#{}'.format(
                val, val.lineno))

    def _parse_body_line(self, item):
        if isinstance(item, Assign):
            prev = None
            for target in item.targets:
                if isinstance(target, Tuple) or isinstance(target, List):
                    t_val = '__unpack__'
                else:
                    t_val = self._get_value(target)

                if prev:
                    self.out.add('{} = {};'.format(t_val, prev))
                else:
                    self.out.add(
                        '{} = {};'.format(t_val, self._get_value(item.value)))
                prev = t_val
                if t_val == '__unpack__':
                    for i, v in enumerate(target.elts):
                        self.out.add('{} = __unpack__[{}];'.format(
                            self._get_value(v), i))
        elif isinstance(item, Return):
            self.out.add('return {}'.format(self._get_value(item.value)))
        elif isinstance(item, If):
            self.out.add('if ({}) {{'.format(self._get_value(item.test)))
            self.out.more_ident()
            for line in item.body:
                self._parse_body_line(line)
            self.out.less_ident()
            if item.orelse:
                raise RuntimeError('orlese not implemented yet')
            self.out.add('}')
        elif isinstance(item, For):
            #target, expr iter, stmt* body, stmt* orelse
            target = self._get_value(item.target)
            iter_name = "{}__iterator".format(target)
            self.out.add("var {} = {};".format(
                iter_name, self._get_value(item.iter)))
            self.out.add("for (var {}__idx in {}) {{".format(
                target, iter_name))
            self.out.more_ident()
            self.out.add("{0} = {1}[{0}__idx];".format(target, iter_name))
            for line in item.body:
                self._parse_body_line(line)
            self.out.less_ident()
            if item.orelse:
                raise RuntimeError('orlese not implemented yet')
            self.out.add('}')
        elif isinstance(item, Try):
            self.out.add('try {')
            self.out.more_ident()
            for line in item.body:
                self._parse_body_line(line)
            self.out.less_ident()
            self.out.add('catch() { /*fixme*/ }')
        elif isinstance(item, Expr):
            self.out.add(self._get_value(item.value))
        elif isinstance(item, With):
            raise RuntimeError('>>> WARNING: WITH is unsupported!')
        elif isinstance(item, Import):
            print(">>> WARNING: [import]", item.names, item.lineno)
            self.out.add('//fixme import')
        elif isinstance(item, Raise):
            self.out.add("throw {}".format(self._get_value(item.exc)))
        elif isinstance(item, Assert):
            cond = self._get_value(item.test)
            if not item.msg:
                msg = '"Invalid condition ({})"'.format(self._esc_js_str(cond))
            else:
                msg = self._get_value(item.msg)
            self.out.add("if (!({})) throw {}".format(cond, msg))
        else:
            raise RuntimeError('unknown body line: {}'.format(item))

    def _esc_js_str(self, s):
        return s.replace('"', '\\"')

    def _parse_func(self, func, method_prefix=''):
        #'name', 'args', 'body', 'decorator_list', 'returns'
        args = []
        defaults = []
        for a in func.args.args:
            args.append(a.arg)
        for d in func.args.defaults:
            defaults.append(self._get_value(d))

        ddec = ''
        for i, default in enumerate(reversed(defaults)):
            a = args[-i-1]
            ddec += '\n\tif (typeof {} === "undefined") {} = {}'.format(
                a, a, default)

        if method_prefix:
            args.pop(0)

        self.out.add("{}function {}({}) {{{}".format(
            method_prefix, func.name, ', '.join(args), ddec))

        if method_prefix:
            self.out.add('\tvar self = this;')

        self.out.more_ident()
        for line in func.body:
            self._parse_body_line(line)
        self.out.less_ident()
        self.out.add("}")

        #print(func.decorator_list)
        #print(func.returns)

    def visit_ClassDef(self, node):
        #'name', 'bases', 'keywords', 'body', 'decorator_list'
        assigns = []
        for item in node.body:
            if isinstance(item, Assign):
                targets = self._get_targets(item.targets)
                value = self._get_value(item.value)
                assigns += zip(targets, [value])
            elif isinstance(item, FunctionDef):
                self._parse_func(
                    item, "\n{}__C.prototype.{} = ".format(node.name, item.name))
            else:
                raise RuntimeError("unsupported {}".format(item))

        static_vars = '\n\t'.join(['this.%s = %s'%(k,v) for k,v in assigns])
        self.out.add('function %s__C(params) {\n\t%s'
                     '\n\tthis.__init__.apply(this, params);\n}' %
                     (node.name, static_vars))
        self.out.add('function %s() {'
                     '\n\treturn (new %s__C(arguments));'
                     '\n}'%(node.name, node.name))
        if node.bases:
            self.out.add('_fab_extends(%s, %s);'%
                         (node.name, node.bases[0].id))


    def visit_FunctionDef(self, node):
        self._parse_func(node)

    def visit_Call(self, node):
        self.out.add(self._get_value(node))

    def visit_Assign(self, node):
        self._parse_body_line(node)

    def visit_Assert(self, node):
        self._parse_body_line(node)

    def result(self):
        return self.out.buf

'''
test_src = """
class PyStr:
    def __init__(self, val):
        self.val = val

    def inspect(self):
        return self.val

    def toJSON(self):
        return self.val

    def valueOf(self):
        return self.val
"""

#node = ast.parse(source=test_src)
node = ast.parse(source=open('test_js.py').read())


p = Py2JsParser()
p.visit(node)
print(p.out.buf)

"""
for nn in ast.iter_child_nodes(node):
    print(nn)
    for n in ast.iter_child_nodes(nn):
        print('   ', n)
"""

'''
