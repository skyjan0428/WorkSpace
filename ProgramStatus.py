import copy
from itertools import tee


class ProgramStatus(object):
    """
    This ProgramStatus class will be instantiated at the following position:
        1. disassemble() in Main.py (2 occurrences)
        2. execute_ins() in symbolic_execution.py (2 occurrences)
    """
    def __init__(self, stack, global_name, var_name, const, parent_const, arg_count):
        self.stack = stack
        
 
        self.global_name = global_name # a list ['test4']
        self.global_value = {} 
        self.init_global_value()

        global_sets = self.global_value.copy()
        global_sets.update(parent_const)
        self.set_global_value(global_sets)

        self.var_name = var_name
        self.var_value = {}
        self.init_var_value(arg_count)

        self.const = const
        self.parent_const = parent_const
        self.arg_count = arg_count

        self.path_condition = []
        self.first_bbl_in_loop = False
        self.ins_counter = 0
        self.ins_dist = {}
        for i in range(1, 164):
            self.ins_dist[i] = 0

        self.input_count = 0

    def __str__(self):
        return str(self.stack) + ",Global_name : " + str(self.global_name) + ",Var_name:" + str(self.var_name) + ",Const:" + str(self.const) + ",Parent_const:" + str(self.parent_const) + ",Arg_count" + str(self.arg_count)
    def init_var_value(self, argcount):
        # All the local variables are initialized as None.
        # All the function arguments are initialized as symbolic variables.
        func_arg = self.var_name[:argcount]
        for var in self.var_name:
            if var in func_arg:
                self.var_value[var] = '*%s' % str(var)
            else:
                self.var_value[var] = None

    def init_global_value(self):
        # All the global variables are initialized as None.
        for glo in self.global_name:
            self.global_value[glo] = None

    def set_global_value(self, global_value):
        self.global_value = global_value

    def set_var_value(self, var_value):
        self.var_value = var_value

    def adjust_var_value(self, key, value):
        self.var_value[key] = value

    def set_path_condition(self, pc):
        self.path_condition = pc

    def set_ins_counter(self, ic):
        self.ins_counter = ic

    def set_ins_dist(self, id):
        self.ins_dist = id

    def set_input_count(self, count):
        self.input_count = count

    def get_copy_stack(self):
        copied = []
        for index, s in enumerate(self.stack[:]):
            # print("get_copy_stack", index, s)
            try:
                if isinstance(s, dict):
                    s = s.copy()
                # elif isinstance(s, tuple):
                #     copied.append(tuple(s))
                # elif isinstance(s, list):
                #     s = copy.deepcopy(s)
                elif hasattr(s, '__iter__') and hasattr(s, 'next') and not isinstance(s, type):
                    s, ori = tee(s)
                    self.stack[index] = ori
            except:
                pass
            copied.append(s)

        return copied

    def get_copy_global(self):
        return copy.deepcopy(self.global_name)

    def get_copy_global_val(self):
        return self.global_value.copy()

    def get_copy_local(self):
        return copy.deepcopy(self.var_name)

    def get_copy_local_val(self):
        return self.var_value.copy()

    def get_copy_const(self):
        return copy.deepcopy(self.const)

    def get_copy_path_condition(self):
        pcs = []
        for pc in self.path_condition:
            pcs.append(pc)
        return pcs

    def get_copy_ins_dist(self):
        return self.ins_dist.copy()

    def __copy__(self):
        stack = self.get_copy_stack()
        global_name = self.get_copy_global()
        global_value = self.get_copy_global_val()
        var_name = self.get_copy_local()
        var_value = self.get_copy_local_val()
        const = self.get_copy_const()
        parent_const = self.parent_const
        ins_counter = self.ins_counter
        arg_count = self.arg_count
        ins_dist = self.get_copy_ins_dist()
        input_count = self.input_count

        pcs = self.get_copy_path_condition()

        nps = ProgramStatus(stack, global_name, var_name, const, parent_const, arg_count)
        nps.set_global_value(global_value)
        nps.set_var_value(var_value)
        nps.set_path_condition(pcs)
        nps.set_ins_counter(ins_counter)
        nps.set_ins_dist(ins_dist)
        nps.set_input_count(input_count)
        return nps


