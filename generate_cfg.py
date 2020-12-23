#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    generate_cfg.py - Generate the CFG of a Python method.
#    Copyright (C) 2013 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import opcode
import copy
import pygraphviz as pgv
from struct import unpack
from collections import defaultdict


class Instruction(object):
    def __init__(self, address, op, symbol=None, symbol_str=None, arg=None):
        self.address = address
        self.opcode = op
        self.mnemonic = opcode.opname[self.opcode]
        self.symbol_str = symbol
        self.symbol = symbol
        self.arg = arg
        if isinstance(self.symbol, str):
            self.symbol = self.__html_escape(self.symbol)
    # Address: 3 Opcode: 100 Mnemonic: LOAD_CONST Symbol_str: 123 Symbol: 123 Arg: 1
    # Address: 6 Opcode: 100 Mnemonic: LOAD_CONST Symbol_str: 1234 Symbol: 1234 Arg: 2
    # Address: 9 Opcode: 131 Mnemonic: CALL_FUNCTION Symbol_str: 2 Symbol: 2 Arg: 2
    def get(self):
        return self.mnemonic 
    def __html_escape(self, text):
        """Produce entities within text."""
        html_escape_table = {
            '&' : '&amp;',
            '"' : '&quot;',
            "'" : '&apos;',
            '>' : '&gt;',
            '<' : '&lt;',
            '%' : ''
        }
        return ''.join(html_escape_table.get(c, c) for c in text)

    def demo(self):
        return " Address: " + str(self.address) + " Opcode: " + str(self.opcode) + " Mnemonic: " + str(self.mnemonic) + " Symbol_str: " + str(self.symbol_str) + " Symbol: " + str(self.symbol) + " Arg: " + str(self.arg)
    def __str__(self):
        s = '<TR><TD align="left"><FONT color="white">%-20s</FONT>' % self.mnemonic
        
        if self.opcode >= opcode.HAVE_ARGUMENT:
            s += '<FONT color="#73ADAD">%s</FONT>' % self.arg
            # s += '<FONT color="#73ADAD">%s</FONT>' % str(self.arg).ljust(5)
        s += '</TD></TR>'
        return s


class BasicBlock(object):
    def __init__(self):
        self.instructions = []
        self.start_address = None
        self.end_address = None
        self.next_bbl = None
        self.is_loop_condition = False

    def get_instructions(self):
        lst = []
        for item in self.instructions:
            lst.append(item)
        return lst

    def append(self, instr):
        if len(self.instructions) == 0:
            # print(instr.address)
            self.start_address = instr.address

        self.instructions.append(instr)
        self.end_address = instr.address
    def demo(self):
        return "instructions:" + str(self.instructions) + "start_address:" + str(self.start_address) + "end_address:" + str(self.end_address) + "next_bbl:" + str(self.next_bbl) + "is_loop_condition:" + str(self.is_loop_condition)
    def demoInstructions(self):
        for ins in self.instructions:
            print(ins.demo())
    def __str__(self):
        # print(self.start_address)
        s = '<TABLE><TR><TD align="left"><FONT color="#9DD600">off_%.8d:</FONT></TD></TR>' % self.start_address
        s += ''.join(map(str, self.instructions))
        s += '</TABLE>'
        return s


def findlabels(code):
    """
    Detect all offsets in a byte code which are jump targets.
    Return the list of offsets.
    """
    labels = []
    n = len(code)
    i = 0
    while i < n:
        c = code[i]
        
        # op = ord(c)
        op = c
        # print(op)
        i = i+1
        if op >= opcode.HAVE_ARGUMENT:
            # oparg = ord(code[i]) + ord(code[i+1])*256
            # print(code[i])
            oparg = code[i]
            # print(oparg)
            # oparg = code[i]
            # print(oparg)
            # print(code[i], code[i+1])
            # print(oparg)
            # print('hi')
            i = i+1
            label = -1
            if op in opcode.hasjrel:
                label = i+oparg
            elif op in opcode.hasjabs:
                label = oparg
            if label >= 0:
                if label not in labels:
                    labels.append(label)
    return labels


def next_branch_distance(i, branches):
    diff_addr = []
    for abs_addr in branches:
        if abs_addr != None and abs_addr > i:
            diff_addr.append(abs_addr-i)

    if len(diff_addr) == 0:
        return None

    return min(diff_addr)


def generate_cfg(co, name):

    code = co.co_code
    branch_instruction = opcode.hasjrel + opcode.hasjabs
    
    nodes = {}
    edges = []
    branch_dest = []

    # path_conditions = defaultdict(list)
    # branch_conditions = defaultdict(list)
    
    exit_flag = 0
    exit_call_address = -1

    for label in findlabels(code):
        nodes[label] = BasicBlock()
    i = 0
    extended_arg = 0
    free = co.co_cellvars + co.co_freevars
    
    current_bbl = BasicBlock()

    
    while i < len(code):
        # op = ord(code[i])
        op = code[i]
        oparg = None
        current_instruction_addr = i
        symbol = None
        # indicates the edge will be removed
        cut_edge_flag = 0
        i += 1
        if op == 0:
            continue
        if op >= opcode.HAVE_ARGUMENT:
            # print unpack('<b', code[i : i + 1])
            # print unpack('<b', code[i+1 : i+2])
            # oparg = unpack('<H', code[i : i + 2])[0] + extended_arg
            oparg = code[i]
            extended_arg = 0
            
            if op == opcode.EXTENDED_ARG:
                extended_arg = oparg << 16
            if op in opcode.hasconst:
                symbol = co.co_consts[oparg]
            elif op in opcode.hasname:
                symbol = co.co_names[oparg]
            elif op in opcode.hasjrel:
                symbol = i + oparg
            elif op in opcode.haslocal:
                symbol = co.co_varnames[oparg]
            elif op in opcode.hascompare:
                symbol = opcode.cmp_op[oparg]
            elif op in opcode.hasfree:
                symbol = free[oparg]
            else:
                symbol = oparg
        i += 1
        # print(current_instruction_addr, op, repr(symbol), symbol, oparg)
        ins = Instruction(current_instruction_addr, op, repr(symbol), symbol, oparg)
        # print ins.demo()
        
        current_bbl.append(ins)
        # print(ins)
        # filter unreachable instructions due to RETURN_VALUE instruction
        if op == opcode.opmap['RETURN_VALUE']:
            
            nodes[current_bbl.start_address] = current_bbl

            next_valid_instruction = next_branch_distance(current_instruction_addr, branch_dest)
            if next_valid_instruction == None:
                break
            i = next_valid_instruction + current_instruction_addr

        # filter unreachable instructions due to sys.exit()/os._exit()/exit()/quit() code
        if (op == opcode.opmap['LOAD_ATTR'] or op == opcode.opmap['LOAD_GLOBAL']) and \
                (repr(symbol).__contains__('exit') or repr(symbol) == "'quit'"):
            exit_flag = 1
            exit_call_address = current_instruction_addr
            # exit_flag = is_exit_code(code, current_instruction_addr)

        if exit_flag == 1 and op == opcode.opmap['CALL_FUNCTION'] or op == opcode.opmap['CALL_METHOD']:
            exit_call_distance = current_instruction_addr-exit_call_address
            if exit_call_distance == 3 or exit_call_distance == 6:
                
                nodes[current_bbl.start_address] = current_bbl
                next_valid_instruction = next_branch_distance(current_instruction_addr, branch_dest)
                if next_valid_instruction == None:
                    break
                i = next_valid_instruction + current_instruction_addr
                cut_edge_flag = 1
            else:
                exit_flag = 0

        # Is-it a branch instruction ? Or Does it exist a future BBL ?
        if op in branch_instruction or i in nodes:
            dst = oparg

            # If it is a relative branchment, we compute the dest address
            if op in opcode.hasjrel:
                dst += i

            branch_dest.append(dst)

            # Push our current BBL into the nodes list
            
            nodes[current_bbl.start_address] = current_bbl

            color_branch_taken_if_jmp, color_branch_if_no_jmp = 'blue', 'blue'
            if op in branch_instruction:
                if opcode.opname[op].find('JUMP_IF_FALSE') != -1:
                    color_branch_taken_if_jmp = 'green'
                    color_branch_if_no_jmp = 'red'
                elif opcode.opname[op].find('JUMP_IF_TRUE') != -1:
                    color_branch_taken_if_jmp = 'green'
                    color_branch_if_no_jmp = 'red'

                # Add an edge between the current_bbl and the destination
                if opcode.opname[op] not in ['SETUP_LOOP', 'SETUP_WITH']:
                    edges.append((current_bbl.start_address, dst, color_branch_taken_if_jmp))

            # If the branchment instruction isn't a pure jump (non-conditionnal)
            if opcode.opname[op] not in ['JUMP_ABSOLUTE', 'JUMP_FORWARD', 'RETURN_VALUE'] and not cut_edge_flag:
                current_bbl.next_bbl = i
                edges.append((current_bbl.start_address, i, color_branch_if_no_jmp))

            # filter unreachable instructions due to JUMP instruction
            if opcode.opname[op] in ['JUMP_ABSOLUTE']:
                next_valid_instruction = (next_branch_distance(current_instruction_addr, branch_dest))
                i = next_valid_instruction + current_instruction_addr

            if i in nodes:
                current_bbl = nodes[i]

            else:
                current_bbl = BasicBlock()
   
    G = pgv.AGraph(directed = True)
    G.graph_attr.update({
        'splines' : 'true',
        'label' : 'Control Flow Graph of: %s' % repr(name)
    })

    G.node_attr.update({
        'style' : 'filled',
        'shape' : 'box',
        'color' : '#2D2D2D',
        'fontname' : 'Consolas Bold', # monospace font ftw!
        'fontsize' : 9,
        'nojustify' : 'true'
    })

    G.edge_attr.update({
        'color' : 'blue',
        'dir' : 'forward',
        'arrowsize' : 1
    })

    # add nodes to the graph
    # print(type(nodes))
    for bbl_id in nodes.keys():
        # print(bbl_id, nodes[bbl_id])
        nodes[bbl_id].start_address = bbl_id
        G.add_node(bbl_id, label='<%s>' % nodes[bbl_id])
    # print(current_bbl.demo())
    # exit()

    # set edge label
    for src, dst, color in edges:
        # if path_conditions[src, dst]:
        #     pc = path_conditions[src, dst]
        # else:
        #     pc = ['True']
        G.add_edge(src, dst, color = color)

    G.layout('dot')
    G.draw(name + '_cfg.svg', prog='dot', args='-Ln20 -LC2')

    print('-----Control Flow Graph of %s Has Been Generated-----' % name)
    
    return nodes, edges
