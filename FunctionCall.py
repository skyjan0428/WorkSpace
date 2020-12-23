import copy


class FunctionCall(object):
    def __init__(self):
        self.top_item = None
        self.load_attr = []
        self.args = None

    def set_top_item(self, t):
        self.top_item = t
    def get_top_item(self):
        return self.top_item

    def add_attr(self, a):
        self.load_attr.append(a)

    def set_args(self, args):
        self.args = args

    def get_args(self):
        return self.args

    def __str__(self):
        attrs = copy.deepcopy(self.load_attr)
        top_item = self.top_item
        attrs_str = ''
        final_op = ''

        if hasattr(top_item, '__call__'):
            top_item = top_item.__name__

        while attrs:
            attrs_str += '.' + attrs.pop()

        if str(type(top_item)) == "<type 'classobj'>":
            return top_item()
        return top_item.__str__() + attrs_str + self.args.__str__()


class FunctionArgs(object):
    def __init__(self):
        self.arg_stack = []

    def pop(self):
        return self.arg_stack.pop()

    def push(self, arg):
        self.arg_stack.append(arg)

    def peek(self):
        if self.arg_stack:
            return self.arg_stack[-1]
        else:
            raise Exception('Peek on an empty Stack')

    def isEmpty(self):
        if len(self.arg_stack) == 0:
            return True
        return False

    def __copy__(self):
        lst =[]
        for a in self.arg_stack:
            lst.append(a)
        return lst
        # return copy.deepcopy(self.arg_stack)
    def to_list(self):
        copy_stack = self.arg_stack
        lst = []
        while(copy_stack):
            arg = copy_stack.pop()
            lst.append(arg)
        return lst
    def to_tuple(self):
        return tuple(self.to_list())
    def __str__(self):
        s = '('
        self.arg_stack.reverse()
        for index, arg in enumerate(self.arg_stack):
            if not isinstance(arg, str):
                arg = str(arg)

            if index == len(self.arg_stack) - 1:
                s += arg
            else:
                s += arg + ', '
        self.arg_stack.reverse()
        # copy_stack = copy.deepcopy(self.arg_stack)
        # while copy_stack:
        #     arg = copy_stack.pop()
        #     if not isinstance(arg, str):
        #         arg = str(arg)

        #     if not copy_stack:
        #         s += arg
        #     else:
        #         s += arg + ', '

        s += ')'
        return s