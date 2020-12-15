import dis
import marshal
import py_compile
import sys
# sys.path.insert(0, '/home/soslab-l1/PycharmProjects/BytecodeAnalyzer/exp_src/pw_chk')
# import pw_chk
import os
import collections
import json
from generate_cfg import generate_cfg
from symbolic_execution import SymbolicExecution
from ProgramStatus import ProgramStatus
from PathConstraints import PathConstraints

def do_symbolic(srcipt_path, bytecode_path, target_const):

    generate_bytecode(srcipt_path, bytecode_path)
    # dissemble bytecode & initialize ProgramStatus
    init_ps = disassemble(bytecode_path, const=target_const)

    nodes, edges = cfg_generator(bytecode_path, 'const_%d' % target_const, const=target_const)

    se = SymbolicExecution((nodes, edges), init_ps)
    se.run()

    print('[INFO]: ============= RESULTS =============')
    res = se.get_results()
    return res
def generate_bytecode(input_path, output_path):
    """
    Generating a compiled .pyc file.
    :param input_path: path of the source .py file.
    :param output_path: path of the output .pyc file.
    :return: None.
    """
    py_compile.compile(input_path, output_path)


def disassemble(input_path, const=None):
    """
    Disassembling a .pyc file and generating its initial ProgramStatus instance.
    :param input_path: path of the source .pyc file.
    :param const: the designed code object to be disassembled
    :return: an initialized ProgramStatus instance.
    """
    # Header size changed in 3.3. It might change again, but as of this writing, it hasn't.
    
    header_size = 16 if sys.version_info >= (3, 3) else 8
    # header_size = 16

    with open(input_path, "rb") as f:
        # first 8 or 12 bytes are metadata
        magic_and_timestamp = f.read(header_size)
        # rest is a marshalled code object
        co = marshal.load(f)

    parent_const = {}
    # target code object is assigned, symbolically execute its parent code object
    if const is not None:
        ps = ProgramStatus([], list(co.co_names), list(co.co_varnames),
                           list(co.co_consts), parent_const, co.co_argcount)


        nodes, edges = cfg_generator(input_path, 'parent_const_%s.pyc' % str(const), const=None)
        
        se = SymbolicExecution((nodes, edges), ps, 0)
        # print nodes
        # die here : no Instrution named function call
        # for ins in nodes[0].get_instructions():
        #     print('ins', ins.get())
        # print('se', nodes[0].get_instructions()[5].get())
        # print('ps', ps.get_copy_global_val())
        # no function input
        print('[INFO]: Conducting Symbolic Execution on Parent Code Object of The Target')
        se.run()
        
        res = se.get_results()
        # fetch local variable of the parent code object as the global variable of the target code object
        parent_const = res[0][4]
        co = co.co_consts[const]
    # string adjustment
    modified_const = list(co.co_consts)
    for i, it in enumerate(modified_const[:]):
        if isinstance(it, str):
            modified_const[i] = '"'+it+'"'

    ps = ProgramStatus([], list(co.co_names), list(co.co_varnames),
                       list(modified_const), parent_const, co.co_argcount)
    # print("co", co.co_names, list(co.co_varnames), list(modified_const), parent_const, co.co_argcount)
    # parent_const indicate the function code
    # print("test4", co)
    # print('global', ps.stack) # ('global', ('test4',))
    dis.dis(co) #prints the instructions of the function
    return ps


def cfg_generator(input_path, graph_name, const=None):
    # Header size changed in 3.3. It might change again, but as of this writing, it hasn't.
    # print(sys.version_info)
    header_size = 16 if sys.version_info >= (3, 3) else 8
    # header_size = 16
    with open(input_path, "rb") as f:
        # first 8 or 12 bytes are metadata
        magic_and_timestamp = f.read(header_size)
        # print magic_and_timestamp

        # rest is a marshalled code object
        code = marshal.load(f)
    if const is not None:
        code = code.co_consts[const]
    # print(code, graph_name)
    return generate_cfg(code, graph_name)