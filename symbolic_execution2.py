import copy
import opcode
import dis
import inspect
import pygraphviz as pgv
from BranchCondition import BranchCondition
from ProgramStatus import ProgramStatus
from FunctionCall import FunctionCall, FunctionArgs
# from FunctionArgs import FunctionArgs
from types import FunctionType
from generate_cfg import generate_cfg
import inspect
import sys
import random

is_call  = False
is_while = False
global count
count = 0
global write_file_stack
write_file_stack = []

class SymbolicExecution(object):
    def __init__(self, cfg, ps, start_addr=0):
        self.nodes, self.edges = cfg
        self.ps = ps #stack is here
        self.start_addr = start_addr
        self.results = []
        self.bool_str = '3'

    def run(self):
        self.symbolic_execution(self.nodes, self.edges, self.start_addr, self.ps)

    def add_results(self, res):
        self.results.append(res)

    def get_results(self):
        return self.results

    def symbolic_execution(self, nodes, edges, exe_bbl, ps):
        

        next_states = self.execute_bbl(nodes, edges, exe_bbl, ps)
        
        if next_states == None:
            return
        for ns in next_states:
            if ns[1] is None:
                continue
            
            self.symbolic_execution(nodes, edges, ns[1], ns[0])
            

        print('[INFO]: Symbolic execution strating from %s has finished' % exe_bbl)

    def execute_bbl(self, nodes, edges, bbl_id, ps):
        #execute a basic block

        next_state = []
        nps = ps
        ja = []
        bc = None
        nps_list = [(ps, ja, bc)]
        # print(nodes[bbl_id].is_loop_condition)
        
        if nodes[bbl_id].is_loop_condition:
            nps.first_bbl_in_loop = True
        # Executing the instructions in this bbl
        bbl_ins = nodes[bbl_id].get_instructions()
        for ins in bbl_ins:

            temp = []
            
            # There will be one or more ProgramStatus to be carried
            for rps in nps_list[:]:
                ins_arg = None
                # print("ins", ins.arg)
                if ins.opcode in opcode.hasjrel:
                    ins_arg = int(ins.symbol_str)
                    # print 'hasjrel'
                else:
                    # print 'not has'
                    ins_arg = ins.arg
                # print("ins", rps[0].get_copy_stack())
                # print("ins", rps[0])
                # print('ps', rps[0].__str__())
                # print('ins_arg', ins_arg)
                # print 'rps', ins.mnemonic, ins.arg

                ps_list = self.execute_ins([ins.mnemonic, ins_arg], rps[0])
                # print(ps_list)
                # if ps_list == None:
                #     return None
                # print(ps_list)
                # if len(ps_list) > 2 and ps_list[1] == 24:
                #     return self.execute_bbl(nodes, edges, 24, ps)
                # print ps_list[0][2]
                temp += ps_list

            # print(temp)
            nps_list = temp
            
        # Generating the next_state object
        for rps in nps_list[:]:

            nps = rps[0]
            ja = rps[1]
            bc = rps[2]
            # print('end', nps.__str__(), ja, bc)
            if nps.first_bbl_in_loop:
                nps.first_bbl_in_loop = False

            # print bbl_ins[-1].mnemonic
            if bbl_ins[-1].mnemonic == 'SETUP_LOOP':
                nodes[nodes[bbl_id].next_bbl].is_loop_condition = True

            # Jumping point is None, go to the un-condition edge
            if not ja:
                un_conditional_bbl = nodes[bbl_id].next_bbl

                next_state.append((nps, un_conditional_bbl))

            # ja is -1: go both edges & duplicate next_state
            elif ja[0] == -1 and bc is not None:
                copy_nps = nps.__copy__()
                if bc.true_address is None:
                    nps.path_condition.append('not( %s )' % bc.condition)
                    next_state.append((nps, bc.false_address))
                    
                    bc.true_address = nodes[bbl_id].next_bbl
                    copy_nps.path_condition.append(bc.condition)
                    next_state.append((copy_nps, bc.true_address))
                elif bc.false_address is None:
                    nps.path_condition.append(bc.condition)
                    next_state.append((nps, bc.true_address))

                    bc.false_address = nodes[bbl_id].next_bbl
                    copy_nps.path_condition.append('not( %s )' % bc.condition)
                    next_state.append((copy_nps, bc.false_address))
                else:
                    raise Exception('BranchAddressException @ execute_bbl()')
            # 1 assigned jumping point
            elif len(ja) == 1 and ja[0] >= 0:
                next_state.append((nps, ja[0]))
            else:
                raise Exception('JumpingPointException @ execute_bbl()')

        print('[DEBUG]: current bbl: %s, jumping point: %s' % (bbl_id, [n[1] for n in next_state]))

        return next_state

    def execute_ins(self, instruction, ps):
        global count, write_file_stack
        
        count+= 1
        print('[DEBUG]: current instruction: %s' % instruction[0])
        exe_stack = ps.get_copy_stack()
        exe_global = ps.get_copy_global()
        exe_global_value = ps.get_copy_global_val()
        exe_vars = ps.get_copy_local()
        exe_var_value = ps.get_copy_local_val()
        exe_const = ps.get_copy_const()
        exe_pc = ps.get_copy_path_condition()
        exe_ic = ps.ins_counter + 1
        exe_id = ps.ins_dist
        exe_input_count = ps.input_count

        if len(write_file_stack) == 0:
            write_file = open("%s.txt" % 'Client_Main', "w")
            file_name = "main"
            write_file.write("\\begin{table} \\begin{center} \\caption{Results of Stack(%s)} \\label{tab:Results of Stack(Client)} \\begin{tabular}{m{4cm}| m{12cm} |} \\hline " % file_name)
            nums = 0
        else:
            # print(write_file_stack)
            f = write_file_stack.pop()
            write_file = f[0]
            file_name = f[1]
            nums = f[2]
        # line = "%s %s & %s & Global: %s  Var: %s Const: %s \\\\  \\hline " % (instruction[0], str(instruction[1]), str(exe_stack), str(exe_global_value), str(exe_var_value), str(exe_const))
        line = "%s %s & %s \\\\ \\hline " % (instruction[0], str(instruction[1]), str(exe_stack))
        line = line.replace("_", "\\_")
        write_file.write(line)
        nums += 1
        if nums > 15:
            write_file.write("\\end{tabular} \\end{center} \\end{table} \\\\")
            write_file.write("\\begin{table} \\begin{center} \\caption{Results of Stack(%s)} \\label{tab:Results of Stack} \\begin{tabular}{m{4cm}| m{12cm} |} \\hline " % file_name)
            nums = 0
        write_file_stack.append([write_file, file_name, nums])

        # print(exe_stack)
        # print(exe_global_value)
        # print(exe_var_value)
        # print(exe_const)
        # print(exe_stack)
        # print(exe_var_value)

        
        # print exe_stack
        bc = None
        jump_addr = []

        if instruction[0] == 'STOP_CODE':
            exe_id[0] += 1
            pass
        # 1, def
        elif instruction[0] == 'POP_TOP':
            exe_id[1] += 1
            try:
                exe_stack.pop()
            except:
                pass
        # 2, def
        elif instruction[0] == 'ROT_TWO':
            exe_id[2] += 1
            tos = exe_stack.pop()
            tos1 = exe_stack.pop()

            exe_stack.append(tos)
            exe_stack.append(tos1)
        # 3, def
        elif instruction[0] == 'ROT_THREE':
            exe_id[3] += 1
            tos = exe_stack.pop()
            tos1 = exe_stack.pop()
            tos2 = exe_stack.pop()

            exe_stack.append(tos)
            exe_stack.append(tos2)
            exe_stack.append(tos1)
        # 4, def
        elif instruction[0] == 'DUP_TOP':
            exe_id[4] += 1
            tos = exe_stack.pop()
            dup_tos = copy.deepcopy(tos)

            exe_stack.append(tos)
            exe_stack.append(dup_tos)
        # 5, def
        elif instruction[0] == 'ROT_FOUR':
            exe_id[5] += 1
            tos = exe_stack.pop()
            tos1 = exe_stack.pop()
            tos2 = exe_stack.pop()
            tos3 = exe_stack.pop()

            exe_stack.append(tos)
            exe_stack.append(tos3)
            exe_stack.append(tos2)
            exe_stack.append(tos1)
        elif instruction[0] == 'RAISE_VARARGS':
            pass
        # 9, def
        elif instruction[0] == 'NOP':
            exe_id[9] += 1
            pass
        # Unary instructions:
        # 10, def
        elif instruction[0] == 'UNARY_POSITIVE':
            exe_id[10] += 1
            var = exe_stack.pop()
            if contains_symbolized([var]):
                exe_stack.append('+' + var)
            else:
                exe_stack.append(+var)
        # 11, def
        elif instruction[0] == 'UNARY_NEGATIVE':
            exe_id[11] += 1
            var = exe_stack.pop()
            if contains_symbolized([var]):
                exe_stack.append('-' + var)
            else:
                exe_stack.append(-var)
        # 12, def
        elif instruction[0] == 'UNARY_NOT':
            exe_id[12] += 1
            var = exe_stack.pop()
            if contains_symbolized([var]):
                exe_stack.append('not(%s)' % var)
            else:
                exe_stack.append(not var)
        # 13, def
        elif instruction[0] == 'UNARY_CONVERT':
            exe_id[13] += 1
            var = exe_stack.pop()
            if contains_symbolized([var]):
                exe_stack.append('`%s`' % var)
            else:
                exe_stack.append(var)
        # 15, def
        elif instruction[0] == 'UNARY_INVERT':
            exe_id[15] += 1
            var = exe_stack.pop()
            if contains_symbolized([var]):
                exe_stack.append('~%s' % var)
            else:
                exe_stack.append(~var)
        # Binary instructions:
        # 19, def
        elif instruction[0] == 'BINARY_POWER':
            exe_id[19] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('%s**%s' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 ** var1)
        # 20, def
        elif instruction[0] == 'BINARY_MULTIPLY':
            exe_id[20] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            # print('%s*%s' % (str(var2), str(var1)))
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and var1 < 0:
                    var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and var2 < 0:
                    var2 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(* %s %s)' % (str(var2), str(var1)))
            else:
                try:
                    exe_stack.append(var2 * var1)
                except:
                    exe_stack.append('%s*%s' % (str(var2), str(var1)))
        # 21, def
        elif instruction[0] == 'BINARY_DIVIDE':
            exe_id[21] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and var1 < 0:
                    var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and var2 < 0:
                    var2 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(/ %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 / var1)
        # 22, def
        elif instruction[0] == 'BINARY_MODULO':
            exe_id[22] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if isinstance(var1, int):
                if contains_symbolized([var1, var2]):
                    if not contains_symbolized([var1]) and var1 < 0:
                        var1 = '(- 0 %d)' % (var1 * -1)
                    if not contains_symbolized([var2]) and var2 < 0:
                        var2 = '(- 0 %d)' % (var2 * -1)
                    exe_stack.append('(% %s %s)' % (str(var2), str(var1)))
                else:
                    exe_stack.append(var1 % var2)
            else:
                if isinstance(var1, tuple):
                    result = '(str.++ '
                    for item in var1:
                        pos = var2.index('%'+'s')
                        if contains_symbolized(item):
                            pre_var2 = var2[:pos]
                            next_var2 = var2[pos+2:]
                            result += '(+ "%s" %s)' % (pre_var2, item)
                            var2 = next_var2
                        else:
                            var2 = var2 % item
                    result += '"%s"' % var2
                    exe_stack.append(result)
                else:
                    exe_stack.append(var2 + ' % ' + str(var1))

        # 23, def
        elif instruction[0] == 'BINARY_ADD':
            exe_id[23] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and isinstance(var1, int) and var1 < 0:
                    var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and isinstance(var2, int) and var2 < 0:
                    var2 = '(- 0 %d)' % (var2 * -1)
                var1 = str(var1)
                var2 = str(var2)
                if not contains_symbolized(var1):
                    var1 = "'" + var1 + "'"
                if not contains_symbolized(var2):
                    var2 = "'" + var2 + "'"
                exe_stack.append("(str.++ %s %s)" % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 + var1)
        # 24, de
        elif instruction[0] == 'BINARY_SUBTRACT':
            exe_id[24] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and var1 < 0:
                    var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and var2 < 0:
                    var2 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(- %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 - var1)
        # 25, def
        elif instruction[0] == 'BINARY_SUBSCR':
            exe_id[25] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if isinstance(var1, int):
                    var1 = int(self.bool_str) + var1
                exe_stack.append('%s[%s]' % (str(var2), str(var1)))
            else:
                try:
                    val = var2[var1]
                except:
                    pass
                # if isinstance(val, str):
                #     val = '"' + val + '"'
                # if isinstance(val, str):
                #     val = '"' + val + '"'
                exe_stack.append(val)
        # 26, def
        elif instruction[0] == 'BINARY_FLOOR_DIVIDE':
            exe_id[26] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and var1 < 0:
                    var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and var2 < 0:
                    var2 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(// %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 // var1)
        # 27, def
        elif instruction[0] == 'BINARY_TRUE_DIVIDE':
            exe_id[27] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and var1 < 0:
                    var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and var2 < 0:
                    var2 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(/ %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 / var1)
        # 28, def
        elif instruction[0] == 'INPLACE_FLOOR_DIVIDE':
            exe_id[28] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and var1 < 0:
                    var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and var2 < 0:
                    var2 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(// %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 // var1)
        # 29, def
        elif instruction[0] == 'INPLACE_TRUE_DIVIDE':
            exe_id[29] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and var1 < 0:
                    var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and var2 < 0:
                    var2 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(/ %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 / var1)
        # 30, def
        elif instruction[0] == 'SLICE+0':
            exe_id[30] += 1
            var1 = exe_stack.pop()
            if contains_symbolized([var1]):
                exe_stack.append('%s' % str(var1))
            else:
                exe_stack.append(var1[:])
        # 31, deff
        elif instruction[0] == 'SLICE+1':
            exe_id[31] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if var1 < 0 and contains_symbolized([var2]):
                    exe_stack.append('(str.substr %s (- (str.len %s) %s) (str.len %s) )' % (str(var2), str(var2), str(var1 * -1), (str(var2))))
                else:
                    exe_stack.append('(str.substr %s %s (str.len %s) )' % (str(var2), str(var1), (str(var2))))
            else:
                exe_stack.append(var2[var1:])
        # 32, def
        elif instruction[0] == 'SLICE+2':
            exe_id[32] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and contains_symbolized([var2]) and var1 < 0:
                    exe_stack.append('(str.substr %s 0 (- (str.len %s) %s))' % (str(var2), str(var2), str(var1 * -1)))
                else:
                    exe_stack.append('(str.substr %s 0 %s )' % (str(var2), str(var1)))

            else:
                exe_stack.append(var2[:var1])
        # 33, def
        elif instruction[0] == 'SLICE+3':
            exe_id[33] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            var3 = exe_stack.pop()
            if contains_symbolized([var1, var2, var3]):
                if not contains_symbolized([var3]) and isinstance(var3, str):
                    var3 = "\"" + var3 +"\""
                if not contains_symbolized([var2]) and var2 < 0:
                    var2 = '(- (str.len %s) %s)' % (var3, var2 * -1)
                if not contains_symbolized([var1]) and var1 < 0:
                    var1 = '(- (str.len %s) %s)' % (var3, var1 * -1)
                s = '(str.substr %s %s %s )' % (str(var3), str(var2), str(var1))
                if var1 > 0 and contains_symbolized([var3]):
                    exe_pc.append('(>= (str.len %s) %s)' % (str(var3), str(var1)))                
                exe_stack.append(s)
            else:
                exe_stack.append(var3[var2:var1])
        # 40, def
        elif instruction[0] == 'STORE_SLICE+0':
            exe_id[40] += 1
            tos = exe_stack.pop()
            tos1 = exe_stack.pop()
            if contains_symbolized([tos, tos1]):
                exe_var_value[tos] = tos1
            else:
                tos[:] = tos1
                exe_var_value[tos] = tos1
        # 41, def
        elif instruction[0] == 'STORE_SLICE+1':
            exe_id[41] += 1
            var1 = exe_stack.pop()
            if contains_symbolized([var1]):
                exe_stack.append('%s' % str(var1))
            else:
                exe_stack.append(var1)
        elif instruction[0] == 'LIST_APPEND':
            pass
        # 42, def
        elif instruction[0] == 'STORE_SLICE+2':
            exe_id[42] += 1
            var1 = exe_stack.pop()
            if contains_symbolized([var1]):
                exe_stack.append('%s' % str(var1))
            else:
                exe_stack.append(var1[:])
        # 43, def
        elif instruction[0] == 'STORE_SLICE+3':
            exe_id[40] += 1
            var1 = exe_stack.pop()
            if contains_symbolized([var1]):
                exe_stack.append('%s' % str(var1))
            else:
                exe_stack.append(var1[:])
        # 43, def
        
        # 55, def
        elif instruction[0] == 'INPLACE_ADD':
            exe_id[55] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if isinstance(var1, str) and not contains_symbolized([var1]):
                    var2 = "\"" + var2 + "\""
                    exe_stack.append('(str.++ %s %s)' % (str(var2), str(var1)))
                elif isinstance(var2, str) and not contains_symbolized([var2]):
                    var1 = "\"" + var1 + "\""
                    exe_stack.append('(str.++ %s %s)' % (str(var2), str(var1)))
                elif isinstance(var1, int) or isinstance(var2, int):
                    if not contains_symbolized([var1]) and isinstance(var1, int) and var1 < 0:
                        var1 = '(- 0 %d)' % (var1 * -1)
                    if not contains_symbolized([var2]) and isinstance(var2, int) and var2 < 0:
                        var1 = '(- 0 %d)' % (var2 * -1)
                    exe_stack.append('(+ %s %s)' % (str(var2), str(var1)))
                else:
                    exe_stack.append('(+ %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 + var1)
        # 56, def
        elif instruction[0] == 'INPLACE_SUBTRACT':
            exe_id[56] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and isinstance(var1, int) and var1 < 0:
                        var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and isinstance(var2, int) and var2 < 0:
                    var1 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(- %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 - var1)
        # 57, def
        elif instruction[0] == 'INPLACE_MULTIPLY':
            exe_id[57] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and isinstance(var1, int) and var1 < 0:
                        var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and isinstance(var2, int) and var2 < 0:
                    var1 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(* %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 * var1)
        # 58, def
        elif instruction[0] == 'INPLACE_DIVIDE':
            exe_id[58] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and isinstance(var1, int) and var1 < 0:
                        var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and isinstance(var2, int) and var2 < 0:
                    var1 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(/ %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 / var1)
        # 59, def
        elif instruction[0] == 'INPLACE_MODULO':
            exe_id[59] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                if not contains_symbolized([var1]) and isinstance(var1, int) and var1 < 0:
                        var1 = '(- 0 %d)' % (var1 * -1)
                if not contains_symbolized([var2]) and isinstance(var2, int) and var2 < 0:
                    var1 = '(- 0 %d)' % (var2 * -1)
                exe_stack.append('(\% %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 % var1)
        # 60, def
        elif instruction[0] == 'STORE_SUBSCR':
            exe_id[60] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            var3 = exe_stack.pop()

            name = ''
            for key in exe_var_value:
                if exe_var_value.get(key) == var2:
                    name = key
            # if contains_symbolized([var1,var2, var3]):
            #     exe_var_value['%s[%s]' %(name, var1)] = var3
            #     print('[WARN]: STORE_SUBSCR on Symbolic Vari')
            # else:
            #     var2[var1] = var3
            #     exe_var_value[name] = var2
            if not contains_symbolized([var3]) and isinstance(var3, str):
                var3 = '\"%s\"' % var3
            if contains_symbolized([var1,var2]):
                if not contains_symbolized([var1]):
                    exe_pc.append('(= (str.at %s %d) %s)' % (var2, var1, var3))
                else:
                    exe_pc.append('(= (str.at %s %s) %s)' % (var2, var1, var3))
            else:
                var2[var1] = var3
                exe_var_value[name] = var2
        # 62, def
        elif instruction[0] == 'BINARY_LSHIFT':
            exe_id[62] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(<< %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 << var1)
        # 63, def
        elif instruction[0] == 'BINARY_RSHIFT':
            exe_id[63] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(>> %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 << var1)
        # 64, def
        elif instruction[0] == 'BINARY_AND':
            exe_id[64] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(& %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 & var1)
        # 65, def
        elif instruction[0] == 'BINARY_XOR':
            exe_id[65] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(^ %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 ^ var1)
        # 66, def
        elif instruction[0] == 'BINARY_OR':
            exe_id[66] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(| %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 | var1)
        # 67, def
        elif instruction[0] == 'INPLACE_POWER':
            exe_id[67] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(** %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 ** var1)
        # 68, def
        elif instruction[0] == 'GET_ITER':
            exe_id[68] += 1
            var = exe_stack.pop()
            if contains_symbolized([var]) and not isinstance(var, list):
                exe_stack.append('iter(%s)' % var)
            else:
                exe_stack.append(iter(var))
        # 71, def
        elif instruction[0] == 'PRINT_ITEM':
            exe_id[71] += 1
            tos = exe_stack.pop()

            print(tos)
        # 72, def
        elif instruction[0] == 'PRINT_NEWLINE':
            exe_id[72] += 1
            print()
        # 75, def
        elif instruction[0] == 'INPLACE_LSHIFT':
            exe_id[75] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(<< %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 << var1)
        # 76, def
        elif instruction[0] == 'INPLACE_RSHIFT':
            exe_id[76] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(>> %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 << var1)
        # 77, def
        elif instruction[0] == 'INPLACE_AND':
            exe_id[77] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(& %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 & var1)
        # 78, def
        elif instruction[0] == 'INPLACE_XOR':
            exe_id[78] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(^ %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 ^ var1)
        # 79, def
        elif instruction[0] == 'INPLACE_OR':
            exe_id[79] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            if contains_symbolized([var1, var2]):
                exe_stack.append('(| %s %s)' % (str(var2), str(var1)))
            else:
                exe_stack.append(var2 | var1)
        # 80, def
        elif instruction[0] == 'BREAK_LOOP':
            exe_id[80] += 1
            # while exe_stack[-1] != "*BLOCK":
            #     exe_stack.pop()
            exe_stack.append('BREAK_LOOP')
            # jump_addr.append(44)
            pass
            
        elif instruction[0] == 'LOAD_LOCALS':
            exe_id[82] += 1
            exe_stack.append("")
            
        # 83, def
        elif instruction[0] == 'RETURN_VALUE':
            exe_id[83] += 1
            # print('[INFO]: Return statement is detected, TOS is: %s; PC is: %s' % (
            # str(exe_stack[-1]), ps.path_condition))
            # print("ins_dist",  ps.global_value) 
            self.add_results((exe_stack[-1], ps.path_condition, ps.ins_counter, ps.ins_dist, ps.global_value))
            # write_file_stack.pop()[0].close()
        # 85, def
        elif instruction[0] == 'EXEC_STMT':
            exe_id[85] += 1
            tos = exe_stack.pop()
            tos1 = exe_stack.pop()
            tos2 = exe_stack.pop()
            if contains_symbolized([tos2, tos1, tos]):
                exe_stack.append('exec(%s, %s, %s)' % (tos2, tos1, tos))
            else:
                exec(tos2, tos1, tos)
        # 87, def
        elif instruction[0] == 'POP_BLOCK':
            exe_id[87] += 1
            pass
            # try:
            #     while "*BLOCK" not in exe_stack[-1] :
            #         exe_stack.pop()
            #     exe_stack.pop()
            #     jump_addr.append(exe_stack.pop())
            # except:
            #     pass
            # wait_util_pop_block = False
        # 89, def
        elif instruction[0] == 'BUILD_CLASS':
            exe_id[89] += 1
            # print exe_stack

            var1 = exe_stack.pop()
            # function = exe_stack.pop()
            var2 = exe_stack.pop()
            var3 = exe_stack.pop()
            bases = tuple(var2)
            cls = type(var3, bases, {})
            # print(cls('a','b'))
            exe_stack.append(cls)
            # exe_stack.append(function)
        # TODO: instruction with args >90
        # 90, name
        elif instruction[0] == 'STORE_NAME':
            exe_id[90] += 1
            global_name = exe_global[instruction[1]]
            try:
                val = exe_stack.pop()
                # val2 = exe_stack.pop()
                # if val != val2:
                #     exe_stack.push(val2)
            except:
                val = ""
            # print(global_name, val)

            exe_global_value[global_name] = val
        # 92, def
        elif instruction[0] == 'UNPACK_SEQUENCE':
            exe_id[92] += 1
            number = instruction[1]
            # exe_stack.pop()
            tos = exe_stack.pop()
            if contains_symbolized([tos]) and 'split' in tos:
                s = ''
                lst = []
                for n in range(number):
                    ran1 = random.randint(0, 9)
                    ran2 = random.randint(0, 9)
                    ran3 = random.randint(0, 9)
                    ran = str(ran1) + str(ran2) + str(ran3)
                    lst.append('*@sp%s' % (ran))
                    if n + 1 == number:
                        s += ' *@sp%s' % (ran)
                    else:
                        s += ' *@sp%s' % (ran) + ' %s ' % (tos[2])
                exe_pc.append('(= %s (str.++ %s))' % (tos[0], s))
                lst.reverse()
                for item in lst:
                    exe_stack.append(item)

            else:
                for n in range(number-1, -1, -1):
                    exe_stack.append(tos[n])
            
            
        # 93, jrel
        elif instruction[0] == 'FOR_ITER':
            exe_id[93] += 1
            try:
                iterator = exe_stack.pop()
                if contains_symbolized([iterator]):
                    print('[INFO]: For-loop iterator depends on symbolized expression %s' % str(iterator))
                    # bool_str = raw_input('Please input designated iterable (eg. range(3)) or designated iteration: ')
                    # self.bool_str = '3'
                    try:
                        iterable = eval(str(self.bool_str))

                        if isinstance(iterable, int):
                            stripped_iterable = iterator[5:-1]
                            if contains_symbolized([stripped_iterable]):
                                if 'range' in str(iterator):
                                    it = str(iterator)
                                    range_index = it.find('range')
                                    start_index = range_index + 6
                                    it = it[start_index: -2]
                                    args = it.split(",")
                                    if len(args) == 1:
                                        iterator = iter([i for i in range(iterable)])
                                    elif len(args) == 2:
                                        pass
                                    elif len(args) == 3:
                                        pass
                                else:
                                    iterator = iter(['(str.at %s %d )' % (stripped_iterable, i) for i in range(iterable)])
                            else:
                                iterator = iter(['%s[%d]' % (stripped_iterable, i) for i in range(iterable)])
                        else:
                            iterator = iter(iterable)
                    except [NameError, TypeError]:
                        print('[ERROR]: Designated iterable %s is illegal' % bool_str)
                        raise Exception('IllegalDesignatedIterableException')

            except:
                pass

            try:
                next_val = iterator.next()
                exe_stack.append(iterator)
                exe_stack.append(next_val)
            except:
                jump_addr.append(instruction[1])
        # 97, name
        elif instruction[0] == 'STORE_GLOBAL':
            exe_id[97] += 1
            exe_global[instruction[1]] = exe_stack.pop()
        # 100, def
        elif instruction[0] == 'LOAD_CONST':
            exe_id[100] += 1
            var1 = exe_const[instruction[1]]
            
            if isinstance(var1, str):
                var1 = var1.replace('"', '')
            exe_stack.append(var1)
        # 101, name
        elif instruction[0] == 'LOAD_NAME':
            exe_id[101] += 1
            val = exe_global_value[exe_global[instruction[1]]]
            if val is not None:
                exe_stack.append(val)
            # in case of builtin type
            else:
                # print '=========================='
                # print exe_global[instruction[1]]
                obj = eval(exe_global[instruction[1]])
                exe_stack.append(obj)
        # 102, def
        elif instruction[0] == 'BUILD_TUPLE':
            exe_id[102] += 1
            lst = []
            for n in range(instruction[1]):
                try:
                    lst.append(exe_stack.pop())
                except:
                    pass

            lst.reverse()
            exe_stack.append(tuple(lst))
        # 103, def
        elif instruction[0] == 'BUILD_LIST':
            exe_id[103] += 1
            lst = []
            for n in range(instruction[1]):
                tos = exe_stack.pop()
                if isinstance(tos, str):
                    tos = tos.strip('\"')
                lst.append(tos)

            lst.reverse()
            exe_stack.append(lst)
        elif instruction[0] == 'BUILD_MAP':
            exe_id[104] += 1
            exe_stack.append({})
        # 106, name
        elif instruction[0] == 'LOAD_ATTR':
            exe_id[106] += 1
            var = exe_stack.pop()
            attr_name = exe_global[instruction[1]]
            try:
                if isinstance(var, str):
                    exe_stack.append('%s.%s' % (var, attr_name))
                elif contains_symbolized([var]):
                    exe_stack.append('%s.%s' % (var, attr_name))
                else:
                    print(var, attr_name)
                    att = getattr(var, attr_name)
                    print(att)
                    exe_stack.append(att)
            except Exception as e:
                # import traceback
                # traceback.print_exc()
                exe_stack.append("")
                # return None 
        # 107, def
        elif instruction[0] == 'COMPARE_OP':
            exe_id[107] += 1
            op = dis.cmp_op[instruction[1]]
            rhs = exe_stack.pop()
            lhs = exe_stack.pop()
            call_str = '%s %s %s' % (lhs, op, rhs)
            if contains_symbolized([rhs, lhs]):
                if op == 'in':
                    if isinstance(rhs, dict):
                        smt_str = ''
                        for index, key in enumerate(rhs):
                            if index == (len(rhs) - 1):
                                smt_str += '(= %s %s)' % (lhs, key)
                            else:
                                smt_str += '(or (= %s %s)' % (lhs, key)
                        if len(rhs) >= 2:
                            smt_str += ')' * (len(rhs)-1)
                        exe_stack.append(smt_str)
                    elif isinstance(rhs, str):
                        if not contains_symbolized([rhs]):
                            rhs = '\"' + rhs + '\"'
                        if not contains_symbolized([lhs]):
                            lhs = '\"' + lhs + '\"'
                        exe_stack.append('(str.contains %s %s)' % (rhs, lhs))
                    elif isinstance(rhs, list):
                        smt_str = ''
                        for index, item in enumerate(rhs):
                            if isinstance(item, str):
                                item = "\"%s\"" % item

                            if index == (len(rhs) - 1):
                                smt_str += '(= %s %s)' % (lhs, item)
                            else:
                                smt_str += '(or (= %s %s)' % (lhs, item)
                        if len(rhs) >= 2:
                            smt_str += ')' * (len(rhs)-1)
                        exe_stack.append(smt_str)
                elif op == 'not in':
                    if isinstance(rhs, dict):
                        smt_str = ''
                        for index, key in enumerate(rhs):
                            if index == (len(rhs) - 1):
                                smt_str += '(not (= %s %s))' % (lhs, key)
                            else:
                                smt_str += '(not (or (= %s %s))' % (lhs, key)
                        if len(rhs) >= 2:
                            smt_str += ')' * (len(rhs)-1)
                        exe_stack.append(smt_str)
                    elif isinstance(rhs, str):
                        if not contains_symbolized([rhs]):
                            rhs = '\"' + rhs + '\"'
                        if not contains_symbolized([lhs]):
                            lhs = '\"' + lhs + '\"'
                        exe_stack.append('(not (str.contains %s %s))' % (rhs, lhs))
                    elif isinstance(rhs, list):
                        smt_str = ''
                        for index, item in enumerate(rhs):
                            if isinstance(item, str):
                                item = "\"%s\"" % item

                            if index == (len(rhs) - 1):
                                smt_str += '(not (= %s %s))' % (lhs, item)
                            else:
                                smt_str += '(not (or (= %s %s))' % (lhs, item)
                        if len(rhs) >= 2:
                            smt_str += ')' * (len(rhs)-1)
                        exe_stack.append(smt_str)
                elif op == '!=':
                    if not contains_symbolized([rhs]) and isinstance(rhs, str):
                            rhs = '\"' + rhs + '\"'
                    if not contains_symbolized([lhs]) and isinstance(rhs, str):
                        lhs = '\"' + lhs + '\"'
                    if not contains_symbolized([rhs]) and isinstance(rhs, int) and rhs < 0:
                            rhs = '(- 0 %d)' % (rhs * -1)
                    if not contains_symbolized([lhs]) and isinstance(lhs, int) and lhs < 0:
                        lhs = '(- 0 %d)' % (lhs * -1)

                    exe_stack.append('(not (%s %s %s))' % ('=', lhs, rhs))
                else:

                    if op == '==':
                        op = '='
                    if not contains_symbolized([rhs]) and isinstance(rhs, str):
                            rhs = '\"' + rhs + '\"'
                    if not contains_symbolized([lhs]) and isinstance(rhs, str):
                        lhs = '\"' + lhs + '\"'
                    if not contains_symbolized([rhs]) and isinstance(rhs, int) and rhs < 0:
                            rhs = '(- 0 %d)' % (rhs * -1)
                    if not contains_symbolized([lhs]) and isinstance(lhs, int) and lhs < 0:
                        lhs = '(- 0 %d)' % (lhs * -1)
                    exe_stack.append('(%s %s %s)' % (op, lhs, rhs))
            else:
                try:
                    exe_stack.append(eval(call_str))
                except Exception as e:
                    # import traceback
                    # traceback.print_exc() 
                    print('[WARN]: User Defined Function Is Detected: %s' % call_str)
                    exe_stack.append('(%s %s %s)' % (op, lhs, rhs))
                    # print exe_stack[-1]
        # 108, name
        elif instruction[0] == 'IMPORT_NAME':
            exe_id[108] += 1
            var1 = exe_stack.pop()
            var2 = exe_stack.pop()
            # lst = exe_global[instruction[1]].split(".")
            # key = sys.path[0]+'/test/'
            # for a in range(len(lst) - 1):
            #     if(a == len(lst) - 2):
            #         key += lst[a]
            #     else:
            #         key += lst[a] + "/"
            # val = lst[len(lst)-1]

            # print(key, val)
            # sys.path.append(key)

            mod = __import__(exe_global[instruction[1]], {}, {}, var1, var2)
            
            exe_stack.append(mod)

        # 109, name
        elif instruction[0] == 'IMPORT_FROM':
            exe_id[109] += 1
            mod = exe_stack.pop()
            attr = getattr(mod, exe_global[instruction[1]])

            exe_stack.append(mod)
            exe_stack.append(attr)

            

        # 110, jrel
        elif instruction[0] == 'SETUP_EXCEPT':
            exe_stack.append(instruction[1])
            exe_stack.append("*BLOCK_Try")

        # 110, jrel
        elif instruction[0] == 'JUMP_FORWARD':
            exe_id[110] += 1
            if instruction[1] % 2 == 1:
                instruction[1] += 1
            jump_addr.append(instruction[1])

        # 111, jabs
        elif instruction[0] == 'JUMP_IF_FALSE_OR_POP':
            exe_id[111] += 1
            flag = exe_stack[-1]

            if contains_symbolized(flag):
                if ps.first_bbl_in_loop:
                    print('[INFO]: While-loop condition depends on symbolized expression %s' % str(flag))
                    bool_str = raw_input('Please input designated boolean value (eg. True): ')
                    try:
                        bool = eval(str(bool_str))
                    except [NameError, TypeError]:
                        print('[ERROR]: Designated iterable %s is illegal' % bool_str)
                        raise Exception('IllegalDesignatedIterableException')

                    if not bool:
                        jump_addr.append(instruction[1])
                    else:
                        exe_stack.pop()
                else:
                    jump_addr.append(-1)
                    bc = BranchCondition(flag)
                    bc.false_address = instruction[1]
            else:
                if not flag:
                    jump_addr.append(instruction[1])
                else:
                    exe_stack.pop()
        # 112, jabs
        elif instruction[0] == 'DELETE_SUBSCR':
            exe_stack.pop()
            exe_stack.pop()
            pass
        elif instruction[0] == 'JUMP_IF_TRUE_OR_POP':
            exe_id[112] += 1
            flag = exe_stack[-1]
            if contains_symbolized(flag):
                if ps.first_bbl_in_loop:
                    print('[INFO]: While-loop condition depends on symbolized expression %s' % str(flag))
                    bool_str = raw_input('Please input designated boolean value (eg. True): ')
                    try:
                        bool = eval(str(bool_str))
                    except [NameError, TypeError]:
                        print('[ERROR]: Designated iterable %s is illegal' % bool_str)
                        raise Exception('IllegalDesignatedIterableException')

                    if bool:
                        jump_addr.append(instruction[1])
                    else:
                        exe_stack.pop()
                else:
                    jump_addr.append(-1)
                    bc = BranchCondition(flag)
                    bc.true_address = instruction[1]
            else:
                if flag:
                    jump_addr.append(instruction[1])
                else:
                    exe_stack.pop()
        # 113, jabs
        elif instruction[0] == 'JUMP_ABSOLUTE':
            exe_id[113] += 1
            jump_addr.append(instruction[1])
        # 114, jabs
        elif instruction[0] == 'POP_JUMP_IF_FALSE':
            exe_id[114] += 1
            flag = exe_stack.pop()
            if contains_symbolized([flag]):
                if ps.first_bbl_in_loop:
                    print('[INFO]: While-loop condition depends on symbolized expression %s' % str(flag))
                    bool_str = raw_input('Please input designated boolean value (eg. True): ')
                    try:
                        bool = eval(str(bool_str))
                    except [NameError, TypeError]:
                        print('[ERROR]: Designated iterable %s is illegal' % bool_str)
                        raise Exception('IllegalDesignatedIterableException')

                    if not bool:
                        jump_addr.append(instruction[1])
                else:
                    jump_addr.append(-1)
                    bc = BranchCondition(flag)
                    bc.false_address = instruction[1]
            else:
                if not flag:
                    jump_addr.append(instruction[1])
        # 115, jabs
        elif instruction[0] == 'POP_JUMP_IF_TRUE':
            exe_id[115] += 1
            flag = exe_stack.pop()
            
            if contains_symbolized(flag):
                if ps.first_bbl_in_loop:
                    print('[INFO]: While-loop condition depends on symbolized expression %s' % str(flag))
                    bool_str = raw_input('Please input designated boolean value (eg. True): ')
                    try:
                        bool = eval(str(bool_str))
                    except [NameError, TypeError]:
                        print('[ERROR]: Designated iterable %s is illegal' % bool_str)
                        raise Exception('IllegalDesignatedIterableException')

                    if bool:
                        jump_addr.append(instruction[1])
                else:
                    jump_addr.append(-1)
                    bc = BranchCondition(flag)
                    bc.true_address = instruction[1]
            else:
                if flag:
                    jump_addr.append(instruction[1])

        # 116, name
        elif instruction[0] == 'LOAD_GLOBAL':
            exe_id[116] += 1
            val = exe_global_value[exe_global[instruction[1]]]
            
            if val is not None:
                exe_stack.append(val)
            else:
                try:
                    obj = eval(exe_global[instruction[1]])
                    exe_stack.append(obj)
                except:
                    instance = exe_var_value['self']
                    classes = instance.__class__.__mro__
                    for c in classes:
                        try:
                            # path = inspect.getfile(instance.__class__)
                            import inspect
                            path = inspect.getfile(c)
                            from importlib.machinery import SourceFileLoader
                            foo = SourceFileLoader("module.name", path).load_module()
                            val = eval('foo.' + exe_global[instruction[1]])
                            exe_global_value[exe_global[instruction[1]]] = val
                            exe_stack.append(val)
                            break
                        except Exception as e:
                            pass
        elif instruction[0] == 'STORE_MAP':
            exe_id[123] += 1
            if(len(exe_stack) != 0):
                key = exe_stack.pop()
                value = exe_stack.pop()
                a = exe_stack.pop()
                a[key] = value
            exe_stack.append(a)
        # 124, def
        elif instruction[0] == 'LOAD_FAST':
            exe_id[124] += 1
            var_name = exe_vars[instruction[1]]
            # global_stack.append(exe_var_value[var_name])
            # print(exe_var_value)
            result = exe_var_value[var_name]
            
            exe_stack.append(result)
        elif instruction[0] == 'STORE_ATTR':
            exe_id[124] += 1
            # print(exe_stack)
            # print(exe_vars)
            # print(exe_global)
            var_name = exe_global[instruction[1]]
            x = exe_stack.pop()
            y = exe_stack.pop()
            setattr(x, var_name, y)
        elif instruction[0] == 'STORE_FAST':
            exe_id[125] += 1
            var_name = exe_vars[instruction[1]]

            if len(exe_stack) == 0:
                val = 0.1
            else:
                val = exe_stack.pop()
                # if isinstance(val, str):
                #     val = '"'+val+'"'
            
            exe_var_value[var_name] = val
            # print var_name, exe_var_value[var_name]
        # 120, jrel
        elif instruction[0] == 'SETUP_LOOP':
            exe_id[120] += 1
            exe_stack.append(instruction[1])
            exe_stack.append("*BLOCK")

            # print(instruction[1])
        # 131, def
        elif instruction[0] == 'CALL_METHOD':
            global is_call
            import traceback 
            import copy
            args = []
            fnc_call = FunctionCall()
            arg_list = FunctionArgs()
            for _ in range(instruction[1]):
                x = exe_stack.pop()
                args.append(x)
                arg_list.push(x)

            method = exe_stack.pop()
            attr = exe_stack.pop()
            if isinstance(attr, tuple):
                a = attr[1]
            else:
                a = attr
            try:
                att = getattr(a, method)
            except:
                import traceback
                traceback.print_exc()
            

            import inspect
            # path = inspect.getfile(a.__class__)
            # print(path)
            # path = inspect.getfile(c)
            # from importlib.machinery import SourceFileLoader
            # foo = SourceFileLoader("module.name", path).load_module()
            # val = eval('foo.' + exe_global[instruction[1]])
            # exe_global_value[exe_global[instruction[1]]] = val
            # exe_stack.append(val)
            # break
            import types
            # print(isinstance(att, types.BuiltinFunctionType))
            # if isinstance(att, types.BuiltinFunctionType):
            #     print(dir(att))
            # print(method)
            try:
                if  method != 'docserver' and method != 'service_actions' and not isinstance(att, types.BuiltinFunctionType) and (contains_symbolized(args)) or method == 'serve_forever' or method == '_handle_request_noblock'  or method == 'process_request' or method == 'finish_request' or method == 'handle' or method == 'handle_one_request' or method == 'method' or method == 'RequestHandlerClass' or method == '_marshaled_dispatch' or method == 'generate_html_documentation':
                    
                    
                    
                    # or method == 'RequestHandlerClass'
                    # or method == 'serve_forever')
                    # or method == '_handle_request_noblock'  or method == 'process_request' or method == 'finish_request' or method == 'handle' or method == 'handle_one_request' or method == 'method'
                    # import inspect
                    # print(inspect.getsource(att))
                    # print(type(att))
                    type_obj = False
                    try:
                        co = att.__code__
                    except:
                        copy_args = []
                        for arg in args:
                            copy_args.append('')
                        init = att.__init__
                        def __init__(self):
                            pass
                        att.__init__ = __init__
                        c = att()
                        type_obj = True
                        c.__init__ = init
                        co = c.__init__.__code__
                    dis.dis(co)
                    fnc_call.set_top_item(att)
                    fnc_call.set_args(arg_list)
                    var_sets = ps.parent_const.copy()
                    var_sets.update(ps.var_value)
                    if isinstance(fnc_call.top_item, str):
                        fnc_name = fnc_call.top_item
                    else:
                        fnc_name = fnc_call.top_item.__name__
                    # print('[WARN]: Import Function On Symbolic Variable Is Detected: %s' % fnc_call.__str__())
                    print('[WARN]: Import Function On Symbolic Variable Is Detected: %s' % fnc_name)

                    # co = att.__code__
                    rps = ProgramStatus([], list(co.co_names), co.co_varnames,
                                        list(co.co_consts), ps.parent_const, co.co_argcount)

                    # modify the original var names to actual inputs
                    fnc_args = fnc_call.args.__copy__()
                    fnc_args.append(a)
                    fnc_args.reverse()
                    for i, element in enumerate(co.co_varnames):
                        if type_obj and i == 0:
                            rps.adjust_var_value(co.co_varnames[i], c)
                        elif i >= len(fnc_args):
                            rps.adjust_var_value(co.co_varnames[i], None)
                        else:
                            rps.adjust_var_value(co.co_varnames[i], fnc_args[i])

                    rps.set_ins_dist(ps.get_copy_ins_dist())
                    rps.set_input_count(exe_input_count)

                    nodes, edges = generate_cfg(co, fnc_name)
                    se = SymbolicExecution((nodes, edges), rps)
                    ff = open(fnc_name+'.txt', "w")
                    ff.write("\\begin{table} \\begin{center} \\caption{Results of Stack(%s)} \\label{tab:Results of Stack} \\begin{tabular}{m{4cm} | m{12cm} |} \\hline " % fnc_name)
                    write_file_stack.append([ff, fnc_name, 0])
                    se.run()
                    ff.write("\\end{tabular} \\end{center} \\end{table}")
                    ff.close()
                    write_file_stack.pop()
                    se_results = se.get_results()

                    nps_list = []
                    for se_result in se_results:
                        try:
                            copied_stack = copy.deepcopy(exe_stack)
                            copied_stack.append(se_result[0])

                            copied_pc = copy.deepcopy(exe_pc)
                            copied_pc += se_result[1]

                            nps = ProgramStatus(copied_stack, exe_global, exe_vars, exe_const,
                                                ps.parent_const, ps.arg_count)
                            nps.first_bbl_in_loop = ps.first_bbl_in_loop
                            nps.set_global_value(exe_global_value)
                            nps.set_var_value(exe_var_value)
                            nps.set_path_condition(copied_pc)
                            nps.set_ins_counter(exe_ic+se_result[2])
                            nps.set_ins_dist(se_result[3])
                            # [WARN]: this should be fixed quickly
                            nps.set_input_count(exe_input_count)

                            nps_list.append((nps, jump_addr, bc))
                        except:
                            pass
                    
                    return nps_list
                else:
                    args.reverse()
                    # print(args)
                    c = att(*args)
                    
                    exe_stack.append(c)
            except Exception as e:
                traceback.print_exc() 
                args.reverse()
                c = att(*args)
                exe_stack.append(c)
            # exe_stack.append()
            # print(type(method), type(attr))
        elif instruction[0] == 'EXTENDED_ARG':
            # print(exe_global[instruction[1]])
            pass
        elif instruction[0] == 'LOAD_METHOD':
            exe_stack.append(exe_global[instruction[1]])
        elif instruction[0] == 'SETUP_FINALLY':
            pass
        elif instruction[0] == 'LOAD_BUILD_CLASS':
            import builtins
            exe_stack.append(builtins.__build_class__)
        elif instruction[0] == '<0>':
            pass
        elif instruction[0] == 'CALL_FUNCTION_KW':
            fnc_call = FunctionCall()
            arg_list = FunctionArgs()
            instance = 0
            has_dic = False
            kw = exe_stack.pop()
            n_v = {}
            for i in range(len(kw)):
                x = exe_stack.pop()
                y = kw[i - len(kw) + 1]
                has_dic = True
                # arg_list.push((y, x))
                n_v[y] = x
            others = instruction[1] - len(kw)
            for _ in range(others):
                x = exe_stack.pop()
                arg_list.push(x)
            # if has_dic:
            #     arg_list.push(n_v)
            fnc_call.set_args(arg_list)
            inses = exe_stack.pop()
            if isinstance(inses, tuple):
                ins = inses[1]
            else:
                ins = inses
            fnc_call.set_top_item(ins)
            var_sets = ps.parent_const.copy()
            var_sets.update(ps.var_value)
            if hasattr(fnc_call.top_item, '__call__'):
                if instruction[1] == 0:
                    try:
                        exe_stack.append(fnc_call.top_item)
                    except Exception as e:
                        exe_stack.append(instance)
                else:
                    # try:
                    # lines = inspect.getsource(fnc_call.top_item)
                    # indexA = lines.index("(")
                    # indexB = lines.index(")")
                    # lines = lines[indexA+1:indexB]
                    # print(lines)
                    # arr = lines.split(",")
                    # t = {}
                    # alist = arg_list.to_list()
                    # for a in range(len(alist)):
                    #     if(type(alist[a]) == list):
                    #         t[alist[a][0]] = alist[a][1]
                    #     else:
                    #         t[arr[a].split('=')[0].replace(' ', '')] = alist[a]
                    # print(t)
                    # var_sets[fnc_call.top_item.__name__] = fnc_call.top_item

                    # ret_val = fnc_call.top_item(lines[indexA:indexB+1])
                    # exe_stack.append(ret_val)
                    # except Exception as e:
                    #     print(e)
                    #     try:
                    tu = (tuple)(fnc_call.get_args().to_list())
                    ret_val = fnc_call.top_item(*tu, **n_v);
                    exe_stack.append(ret_val)
                    #     except:
                    #         exe_stack.append("")
                    

            else:                 
                try:
                    args = arg_list.to_tuple()
                    b = fnc_call.top_item(*args, **n_v)
                    exe_stack.append(b)
                except Exception as a:
                    exe_stack.append(fnc_call.__str__())
        # elif instruction[0] == 'CALL_FUNCTION_EX':
        #     args = exe_stack.pop()
        #     func = exe_stack.pop()
        #     exe_stack.append(func(*args))
        elif instruction[0] == 'CALL_FUNCTION' or instruction[0] == 'CALL_FUNCTION_EX':
            exe_id[131] += 1
            fnc_call = FunctionCall()
            arg_list = FunctionArgs()
            args = []
            instance = 0
            # high = int(instruction[1] / 256 * 2)
            if instruction[0] == 'CALL_FUNCTION':
                low = int(instruction[1] % 256)
                total = low
                # for i in range(0, high, 2):
                #     x = exe_stack.pop()
                #     y = exe_stack.pop()
                    
                    # arg_list.push([y.replace('"', ''), x])
                for i in range(low):
                    x = exe_stack.pop()
                    arg_list.push(x)
                    args.append(x)
            else:
                tu = exe_stack.pop()
                for t in tu:
                    args.append(t)
                    arg_list.push(t)
                

            fnc_call.set_args(arg_list)
            


            inses = exe_stack.pop()
            if isinstance(inses, tuple):
                ins = inses[1]
            else:
                ins = inses
            # print(arg_list.to_list(), ins.__code__.co_consts)
            fnc_call.set_top_item(ins)
            var_sets = ps.parent_const.copy()
            var_sets.update(ps.var_value)
            # print(type(ins))
            # print 'copy', type(arg_list)
            # for a in arg_list:
            if  ins.__name__ == 'do_POST':
                    
                type_obj = False
                att = ins
                try:
                    co = att.__code__
                except:
                    copy_args = []
                    for arg in args:
                        copy_args.append('')
                    init = att.__init__
                    def __init__(self):
                        pass
                    att.__init__ = __init__
                    c = att()
                    type_obj = True
                    c.__init__ = init
                    co = c.__init__.__code__
                dis.dis(co)

                fnc_call.set_top_item(att)
                fnc_call.set_args(arg_list)
                var_sets = ps.parent_const.copy()
                var_sets.update(ps.var_value)
                if isinstance(fnc_call.top_item, str):
                    fnc_name = fnc_call.top_item
                else:
                    fnc_name = fnc_call.top_item.__name__
                # print('[WARN]: Import Function On Symbolic Variable Is Detected: %s' % fnc_call.__str__())
                print('[WARN]: Import Function On Symbolic Variable Is Detected: %s' % fnc_name)

                # co = att.__code__
                rps = ProgramStatus([], list(co.co_names), co.co_varnames,
                                    list(co.co_consts), ps.parent_const, co.co_argcount)

                # modify the original var names to actual inputs
                fnc_args = fnc_call.args.__copy__()
                fnc_args.append(att.__self__)
                fnc_args.reverse()
                for i, element in enumerate(co.co_varnames):
                    if type_obj and i == 0:
                        rps.adjust_var_value(co.co_varnames[i], c)
                    elif i >= len(fnc_args):
                        rps.adjust_var_value(co.co_varnames[i], None)
                    else:
                        rps.adjust_var_value(co.co_varnames[i], fnc_args[i])

                rps.set_ins_dist(ps.get_copy_ins_dist())
                rps.set_input_count(exe_input_count)

                nodes, edges = generate_cfg(co, fnc_name)
                se = SymbolicExecution((nodes, edges), rps)
                ff = open(fnc_name+'.txt', "w")
                ff.write("\\begin{table} \\begin{center} \\caption{Results of Stack(%s)} \\label{tab:Results of Stack} \\begin{tabular}{m{4cm} | m{12cm} |} \\hline " % fnc_name)
                write_file_stack.append([ff, fnc_name, 0])
                se.run()
                ff.write("\\end{tabular} \\end{center} \\end{table}")
                ff.close()
                write_file_stack.pop()
                se_results = se.get_results()

                nps_list = []
                for se_result in se_results:
                    try:
                        copied_stack = copy.deepcopy(exe_stack)
                        copied_stack.append(se_result[0])

                        copied_pc = copy.deepcopy(exe_pc)
                        copied_pc += se_result[1]

                        nps = ProgramStatus(copied_stack, exe_global, exe_vars, exe_const,
                                            ps.parent_const, ps.arg_count)
                        nps.first_bbl_in_loop = ps.first_bbl_in_loop
                        nps.set_global_value(exe_global_value)
                        nps.set_var_value(exe_var_value)
                        nps.set_path_condition(copied_pc)
                        nps.set_ins_counter(exe_ic+se_result[2])
                        nps.set_ins_dist(se_result[3])
                        # [WARN]: this should be fixed quickly
                        nps.set_input_count(exe_input_count)

                        nps_list.append((nps, jump_addr, bc))
                    except:
                        pass
                
                return nps_list
            if contains_symbolized(arg_list.__copy__() + [fnc_call.top_item]):
                if isinstance(fnc_call.top_item, str):
                    fnc_name = fnc_call.top_item
                else:
                    fnc_name = fnc_call.top_item.__name__
                    
                # user defined functions: symbolically execute it

                if fnc_name in var_sets:
                    print('[WARN]: User Defined Function On Symbolic Variable Is Detected: %s' % fnc_call.__str__())
                    
                    # try:
                    # print(var_sets[fnc_name])
                    # try:
                    # print(var_sets[fnc_name].__init__)
                    # print(exe_global_value[fnc_name])
                    # print(type(ins))
                    try:
                        co = ps.parent_const.get(fnc_name).__code__
                        # dis.dis(co)
                        # co.co_consts = 0
                        rps = ProgramStatus([], list(co.co_names), co.co_varnames,
                                            list(co.co_consts), ps.parent_const, co.co_argcount)

                        # modify the original var names to actual inputs
                        fnc_args = fnc_call.args.__copy__()
                        fnc_args.reverse()
                        for i, element in enumerate(fnc_args):
                            rps.adjust_var_value(co.co_varnames[i], fnc_args[i])

                        rps.set_ins_dist(ps.get_copy_ins_dist())
                        rps.set_input_count(exe_input_count)

                        nodes, edges = generate_cfg(co, fnc_name)
                        se = SymbolicExecution((nodes, edges), rps)
                        ff = open(fnc_call.__str__()+'.txt', "w")
                        fnc_name = fnc_call.__str__()
                        ff.write("\\begin{table} \\begin{center} \\caption{Results of Stack(%s)} \\label{tab:Results of Stack} \\begin{tabular}{m{4cm}| m{12cm} |} \\hline " % fnc_name)
                        write_file_stack.append([ff, fnc_name, 0])
                        se.run()
                        ff.write("\\end{tabular} \\end{center} \\end{table}")
                        ff.close()
                        write_file_stack.pop()
                        se_results = se.get_results()

                        nps_list = []
                        for se_result in se_results:
                            # print(se_result[1])
                            try:
                                try:
                                    copied_stack = copy.deepcopy(exe_stack)
                                except:
                                    copied_stack = exe_stack
                                copied_stack.append(se_result[0])

                                copied_pc = copy.deepcopy(exe_pc)
                                copied_pc += se_result[1]

                                nps = ProgramStatus(copied_stack, exe_global, exe_vars, exe_const,
                                                    ps.parent_const, ps.arg_count)
                                nps.first_bbl_in_loop = ps.first_bbl_in_loop
                                nps.set_global_value(exe_global_value)
                                nps.set_var_value(exe_var_value)
                                nps.set_path_condition(copied_pc)
                                nps.set_ins_counter(exe_ic+se_result[2])
                                nps.set_ins_dist(se_result[3])
                                # [WARN]: this should be fixed quickly
                                nps.set_input_count(exe_input_count)

                                nps_list.append((nps, jump_addr, bc))
                            except Exception as e:
                                import traceback
                                error_class = e.__class__.__name__ 
                                detail = e.args[0] 
                                cl, exc, tb = sys.exc_info() 
                                print(traceback.format_exc())
                                lastCallStack = traceback.extract_tb(tb)[-1] 
                                fileName = lastCallStack[0] 
                                lineNum = lastCallStack[1] 
                                funcName = lastCallStack[2] 
                                errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
                                print(errMsg)
                        
                        return nps_list
                    except Exception as e:
                        import traceback
                        error_class = e.__class__.__name__ 
                        detail = e.args[0] 
                        cl, exc, tb = sys.exc_info() 
                        lastCallStack = traceback.extract_tb(tb)[-1] 
                        fileName = lastCallStack[0] 
                        lineNum = lastCallStack[1] 
                        funcName = lastCallStack[2] 
                        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
                        print(errMsg)
                        exe_stack.append(fnc_call.__str__())
                # built in functions
                else:

                    f = str(fnc_call.top_item)

                    if not hasattr(fnc_call.top_item, '__name__'):
                        if '.find' == f[-1 * len('.find'):]:
                            wd = f[:-1 * len('.find')]
                            if not contains_symbolized(wd):
                                wd = "\"" + wd + "\""
                            if not contains_symbolized(fnc_call.args.to_list()[0]):
                                arg1 = "\"" + fnc_call.args.to_list()[0] + "\""
                            else:
                                arg1 = fnc_call.args.to_list()[0]
                            smt_str = '(str.indexof '+ wd + ' ' + arg1 + ' 0)'
                            exe_stack.append(smt_str)
                        elif '.endswith' == f[-1 * len('.endswith'):]:
                            wd = f[:-1 * len('.endswith')]
                            if not contains_symbolized(wd):
                                wd = "\"" + wd + "\""
                            if not contains_symbolized(fnc_call.args.to_list()[0]):
                                arg1 = "\"" + fnc_call.args.to_list()[0] + "\""
                            else:
                                arg1 = fnc_call.args.to_list()[0]
                            smt_str = '(str.suffixof '+ arg1 + ' ' + wd + ' )'
                            exe_stack.append(smt_str)
                        elif '.replace' == f[-1 * len('.replace'):]:
                            wd = f[:-1 * len('.replace')]
                            if not contains_symbolized(wd):
                                wd = "\"" + wd + "\""
                            if not contains_symbolized(fnc_call.args.to_list()[0]):
                                arg1 = "\"" + fnc_call.args.to_list()[0] + "\""
                            else:
                                arg1 = fnc_call.args.to_list()[0]
                            if not contains_symbolized(fnc_call.args.to_list()[1]):
                                arg2 = "\"" + fnc_call.args.to_list()[1] + "\""
                            else:
                                arg2 = fnc_call.args.to_list()[1]
                            smt_str = '(str.replace '+ wd + ' ' + arg1 + ' ' + ' ' + arg2 + ' )'
                            if len(fnc_call.args.to_list()) > 2:
                                count = int(fnc_call.args.to_list()[2])
                                for _ in range(count - 1):
                                    smt_str = '(str.replace ' + smt_str + ' ' + arg1 + ' ' + arg2 + ')'
                            
                            exe_stack.append(smt_str)
                        elif '.startswith' == f[-1 * len('.startswith'):]:
                            wd = f[:-1 * len('.startswith')]
                            if not contains_symbolized(wd):
                                wd = "\"" + wd + "\""
                            if not contains_symbolized(fnc_call.args.to_list()[0]):
                                arg1 = "\"" + fnc_call.args.to_list()[0] + "\""
                            else:
                                arg1 = fnc_call.args.to_list()[0]
                            smt_str = '(str.prefixof '+ arg1 + ' ' + wd + ' )'
                            exe_stack.append(smt_str)
                        elif '.split' == f[-1 * len('.split'):]:
                            wd = f[:-1 * len('.split')]
                            if not contains_symbolized(wd):
                                wd = "\"" + wd + "\""
                            
                            if len(fnc_call.args.to_list()) == 1:
                                arg1 = fnc_call.args.to_list()[0]
                                exe_stack.append('('+wd+'.split(\"%s\"))' % arg1)
                            # if len(fnc_call.args.to_list()) == 1:
                            #     exe_stack.append('('+wd+'.split(\"%s\"))'%fnc_call.args.to_list()[0])
                            elif len(fnc_call.args.to_list()) == 0:
                                arg1 = "\" \""
                            else:
                                if not contains_symbolized(fnc_call.args.to_list()[0]):
                                    arg1 = "\"" + fnc_call.args.to_list()[0] + "\""
                                else:
                                    arg1 = fnc_call.args.to_list()[0]
                                exe_stack.append((wd, '.split', arg1))
                            exe_stack.append('('+wd+'.split(\"%s\"))' % arg1)
                        elif '.isdigit' == f[-1 * len('.isdigit'):]:
                            wd = f[:-1 * len('.isdigit')]
                            if not contains_symbolized(wd):
                                wd = "\"" + wd + "\""
                            exe_stack.append('(isdigit %s)' % wd)
                            
                            
                        else:
                            exe_stack.append(fnc_call.__str__())
                    else:
                        try:
                            val = getattr(f, fnc_call.args.to_list()[0])
                            # val = eval(f + "(\""+ fnc_call.args.to_list()[0]+"\")")
                            exe_stack.append(val)
                        except:
                            if fnc_call.top_item.__name__ == 'index':
                                smt = ''
                                arg = fnc_call.args.to_list()[0]
                                for index, item in enumerate(inses[0]):
                                    smt += '(ite (= %s %s) %d ' % (item, arg, index)
                                smt += ')' * len(inses[0])
                                exe_stack.append(smt)
                            elif fnc_call.top_item.__name__ == 'sum':
                                arg_list = fnc_call.args.to_list()[0]
                                smt_str = ''
                                for index, arg in enumerate(arg_list):
                                    if index == len(arg_list)-1:
                                        smt_str += str(arg) + ')' * (len(arg_list) - 1)
                                    else:
                                        smt_str += '(+ ' + str(arg) + ' '
                                exe_stack.append(smt_str)
                            elif fnc_call.top_item.__name__ == 'max':
                                arg_list = fnc_call.args.to_list()
                                exe_stack.append('(max ' + str(arg_list[0]) + ' ' + str(arg_list[1]) + ')')
                            elif fnc_call.top_item.__name__ == 'min':
                                arg_list = fnc_call.args.to_list()
                                exe_stack.append('(min ' + str(arg_list[0]) + ' ' + str(arg_list[1]) + ')')
                            elif fnc_call.top_item.__name__ == 'abs':
                                arg_list = fnc_call.args.to_list()
                                exe_stack.append('(do_abs ' + str(arg_list[0]) + ')')
                            elif fnc_call.top_item.__name__ == 'len':
                                arg_list = fnc_call.args.to_list()
                                exe_stack.append('(str.len ' + str(arg_list[0]) + ')')
                            elif fnc_call.top_item.__name__ == 'int':
                                arg_list = fnc_call.args.to_list()
                                # smt = '(str.is_digit %s)' % str(arg_list[0])
                                # exe_pc.append(smt)
                                exe_stack.append('(str.to_int ' + str(arg_list[0]) + ')')
                            elif fnc_call.top_item.__name__ == 'range':
                                exe_stack.append(fnc_call.__str__())
                            else:
                                print('[WARN]: Import Function On Symbolic Variable Is Detected: %s' % fnc_call.__str__())
                                
                                
                                # try:
                                co = fnc_call.top_item.__code__
                                dis.dis(co)
                                rps = ProgramStatus([], list(co.co_names), co.co_varnames,
                                                    list(co.co_consts), ps.parent_const, co.co_argcount)

                                # modify the original var names to actual inputs
                                
                                fnc_args = args
                                if co.co_varnames[0]=='self':
                                    fnc_args.append(fnc_call.top_item.__self__)

                                fnc_args.reverse()
                                # for i, element in enumerate(co.co_varnames):
                                #     rps.adjust_var_value(co.co_varnames[i], fnc_args[i])
                                for i, element in enumerate(co.co_varnames):
                                    if i >= len(fnc_args):
                                        rps.adjust_var_value(co.co_varnames[i], None)
                                    else:
                                        rps.adjust_var_value(co.co_varnames[i], fnc_args[i])
                                
                                rps.set_ins_dist(ps.get_copy_ins_dist())
                                rps.set_input_count(exe_input_count)

                                nodes, edges = generate_cfg(co, fnc_name)
                                se = SymbolicExecution((nodes, edges), rps)

                                ff = open(fnc_call.__str__()+'.txt', "w")
                                fnc_name = fnc_call.__str__()
                                ff.write("\\begin{table} \\begin{center} \\caption{Results of Stack(%s)} \\label{tab:Results of Stack} \\begin{tabular}{m{4cm} | m{12cm} |} \\hline " % fnc_name)
                                write_file_stack.append([ff, fnc_name, 0])
                                se.run()
                                ff.write("\\end{tabular} \\end{center} \\end{table}")
                                ff.close()
                                write_file_stack.pop()
                                se_results = se.get_results()
                                # print(se_results)
                                # print('se_results')
                                exe_stack.append(se_results[0][0])
                                nps_list = []
                                # for se_result in se_results:
                                #     try:
                                #         copied_stack = copy.deepcopy(exe_stack)
                                #         copied_stack.append(se_result[0])

                                #         copied_pc = copy.deepcopy(exe_pc)
                                #         copied_pc += se_result[1]

                                #         nps = ProgramStatus(copied_stack, exe_global, exe_vars, exe_const,
                                #                             ps.parent_const, ps.arg_count)
                                #         nps.first_bbl_in_loop = ps.first_bbl_in_loop
                                #         nps.set_global_value(exe_global_value)
                                #         nps.set_var_value(exe_var_value)
                                #         nps.set_path_condition(copied_pc)
                                #         nps.set_ins_counter(exe_ic+se_result[2])
                                #         nps.set_ins_dist(se_result[3])
                                #         # [WARN]: this should be fixed quickly
                                #         nps.set_input_count(exe_input_count)

                                #         nps_list.append((nps, jump_addr, bc))
                                #     except:
                                #         pass

                                # return nps_list


                                # print(fnc_call.__str__())
                                # exe_stack.append(fnc_call.__str__())

            # exit related function is called
            elif str(type(fnc_call.top_item)) == "<class 'site.Quitter'>":
                print('[INFO]: Exit related function is called, PC is: %s' % ps.path_condition)
                self.add_results((None, ps.path_condition, ps.ins_counter, ps.ins_dist, ps.global_value))

            # input() function is called
            elif hasattr(fnc_call.top_item, '__name__') and fnc_call.top_item.__name__ == 'input':
                print('[WARN]: User Input Is Required: %s' % fnc_call.__str__())
                exe_stack.append('*input%d' % exe_input_count)
                exe_input_count += 1

            else:
                # try:
                    # The TOS is callable
                        

                if hasattr(fnc_call.top_item, '__call__'):
                    # This function call does not have any argument
                    
                    if instruction[1] == 0:
                        try:
                            b = fnc_call.top_item()
                            exe_stack.append(b)

                        except Exception as e:
                            # import traceback
                            # traceback.print_exc() 
                            exe_stack.append(instance)
                    else:
                        # Add the TOS to varsets
                        # try:

                        #     import inspect
                        #     lines = inspect.getsource(fnc_call.top_item)
                        #     indexA = lines.index("(")
                        #     indexB = lines.index(")")
                        #     lines = lines[indexA+1:indexB]
                        #     arr = lines.split(",")
                        #     t = {}
                        #     alist = arg_list.to_list()
                        #     for a in range(len(alist)):
                        #         if(type(alist[a]) == list):
                        #             t[alist[a][0]] = alist[a][1]
                        #         else:
                        #             t[arr[a].split('=')[0].replace(' ', '')] = alist[a]
                        #     var_sets[fnc_call.top_item.__name__] = fnc_call.top_item
                        #     ret_val = fnc_call.top_item(lines[indexA:indexB+1])
                        #     exe_stack.append(ret_val)
                        # except Exception as e:
                            
                        try:
                            tu = arg_list.to_tuple();
                            if fnc_call.top_item.__name__ == '__build_class__':
                                import inspect
                                path = inspect.getfile(tu[0])
                                from importlib.machinery import SourceFileLoader
                                foo = SourceFileLoader("module.name", path).load_module()
                                val = eval('foo.' + tu[1])
                                exe_stack.append(val)
                            else:
                                args.reverse()
                                tu = tuple(args)
                                
                                ret_val = fnc_call.top_item(*tu);
                                # if fnc_call.top_item.__name__ == 'resolve_dotted_attribute':
                                #     print(ret_val('title'))
                                exe_stack.append(ret_val)
                        except Exception as e:
                            # import traceback
                            # traceback.print_exc() 
                            exe_stack.append("")
                        

                else:                 
                    try:
                        args = arg_list.to_tuple()

                        b = fnc_call.top_item(*args)
                        exe_stack.append(b)
                    except Exception as a:
                        import traceback
                        traceback.print_exc() 
                        exe_stack.append(fnc_call.__str__())
            
        elif instruction[0] == 'SETUP_WITH':
            pass
        elif instruction[0] == 'WITH_CLEANUP':
            pass
        elif instruction[0] == 'END_FINALLY':
            pass
        # 132, def

        elif instruction[0] == 'MAKE_FUNCTION':
            # raise Exception('Not Finished Instruction: %s' % instruction[0])
            exe_id[132] += 1
            exe_stack.pop()
            code_obj = exe_stack.pop()

            # print(type(code_obj))
            default_args = []
            for i in range(instruction[1]):
                default_args.append(exe_stack.pop())

            # print(code_obj)
            func = FunctionType(code_obj, {}, argdefs= tuple(default_args))
            # print(func.__code__)
            # dis.dis(func)

            exe_stack.append(func)

        # 142, def
        elif instruction[0] == 'CALL_FUNCTION_VAR_KW':
            raise Exception('Not Finished Instruction: %s' % instruction[0])
        else:
            raise Exception('Not Handled Instruction: %s' % instruction[0])
    

        
        nps = ProgramStatus(exe_stack, exe_global, exe_vars, exe_const,
                            ps.parent_const, ps.arg_count)
        nps.first_bbl_in_loop = ps.first_bbl_in_loop
        nps.set_global_value(exe_global_value)
        nps.set_var_value(exe_var_value)
        nps.set_path_condition(exe_pc)
        nps.set_ins_counter(exe_ic)
        nps.set_ins_dist(exe_id)
        nps.set_input_count(exe_input_count)
        return [(nps, jump_addr, bc)]


def contains_symbolized(args):
    if isinstance(args, bool):
        return False
    flag = 0
    for arg in args:
        if str(arg).__contains__('*') and not str(arg).__contains__('xml'):
            flag = 1
    return flag
# def test4(a, b, const = 0, kk = False):
#     if(a > b):
#         return a
#     else:
#         return b

