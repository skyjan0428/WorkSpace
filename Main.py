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
from do_symbolic import do_symbolic





if __name__ == '__main__':
    target_const = 11

    debug_mode = True

    #  test : 3, gen : 10, trans: 4, zoo:20

    # file_name = 'calvin/runtime/north/calvincontrol'
    # file_name = 'test_class'
    file_name = 'pytorch'
    # pah of the target code

    # path = './test/'
    path = './test2/'
    sys.path.append(sys.path[0]+ path[1:-1])


    srcipt_path = os.path.join(path, file_name+'.py')
    bytecode_path = os.path.join(path, file_name+'.pyc')

    res = do_symbolic(srcipt_path, bytecode_path, target_const, 0)
    count = 0
    if not debug_mode:
        os.mkdir('./' + file_name);
    for item in res:
        raw_constraint = item[1]
        count += 1
        print('Path constraints %d: %s' % (count, str(raw_constraint)))

        print('SMT path constraints:')
        smt_pc = PathConstraints(raw_constraint)
        if not debug_mode:
            f = open('./' + file_name + '/' + str(count) + ".smt", "a")
            f.write(smt_pc.to_smt())
            f.close()
        print(smt_pc.to_smt())

        d = dict((k, v) for k, v in item[3].items() if v > 0)
        od = collections.OrderedDict(sorted(d.items()))
        print('Instruction set %d: %s' % (count, json.dumps(od)))
        print('==========')
    from symbolic_execution import write_file_stack

    for write_file in write_file_stack:
        ff = write_file[0]
        ff.write("\\end{tabular} \\end{center} \\end{table}")
        ff.close()


    print('[INFO]: ============= END OF THE RESULTS =============')




