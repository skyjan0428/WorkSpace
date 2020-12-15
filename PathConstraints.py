class Node:
    def __init__(self, data):
        self.left_child = None
        self.right_child = None
        self.data = data

    def __str__(self):
        if self.left_child is None:
            lc = None
        else:
            lc = self.left_child.data

        if self.right_child is None:
            rc = None
        else:
            rc = self.right_child.data
        return 'data: %s, left_child: %s, right_child: %s' % (self.data, lc, rc)

    def is_internal(self):
        if self.left_child is not None or self.right_child is not None:
            return True
        else:
            return False


class BinaryTree:
    def __init__(self, root):
        self.root = root

    def print_tree(self):
        self.print_node(self.root, 0)

    def print_node(self, node, depth):
        if node is None:
            print('  ' * depth + 'Null')
            return
        print ('  ' * depth + node.data)

        if node.is_internal():
            self.print_node(node.left_child, depth+1)
            self.print_node(node.right_child, depth+1)

    def print_smt(self):
        return '(%s)' % self.get_smt_node(self.root)

    def get_smt_node(self, node):
        if node is None:
            return ''
        s = ''
        if node.data == 'not':
            s += '(%s ' % node.data
            s += self.get_smt_node(node.left_child)
            s += ' '
            s += self.get_smt_node(node.right_child)
            s += ')'
        elif node.is_internal():
            s += '%s ' % node.data

            s += self.get_smt_node(node.left_child)
            s += ' '
            s += self.get_smt_node(node.right_child)
        else:
            return '%s ' % node.data

        s += ''
        return s


class PathConstraints:
    def __init__(self, raw_pcs):
        self.raw_pcs = raw_pcs
        self.pcs = []

        for rpc in raw_pcs:
            c_root = self.generate_constraint(rpc)
            root = Node('assert')
            root.left_child = c_root
            self.pcs.append(BinaryTree(root))
    def findMatch(self, smt, p, dire, start, end):
        
        balance = 0
        if dire == 1:
            move = 1
            while smt[p+move] != end or balance != 0:
                if smt[p+move] == start:
                    balance -= 1
                elif smt[p+move] == end:
                    balance += 1
                move += 1
            return p+move
        else:
            move = -1
            while smt[p+move] != end or balance != 0:
                if smt[p+move] == start:
                    balance -= 1
                elif smt[p+move] == end:
                    balance += 1
                move -= 1
            return p+move

    def to_smt(self):

        var = {'*title':'String'}
        s = ''
        pre = '(set-option :produce-models true)\n (set-logic ALL)\n'
        for key in var:
            pre += '(declare-fun ' + key + ' () ' + var[key] + ')\n'
        smt = ''
        for bt in self.pcs:
            smt = bt.print_smt()
            s += smt+ '\n'

        # if 'str.at' in s:
        #     dic = {}
        #     position = s.find('str.at', 0)
        #     while position != -1:
        #         start = s[position: ]
        #         lst = start.split(" ")
        #         key = lst[1]
        #         value = lst[2]
        #         if key in dic:
        #             if dic[key] < value:
        #                 dic[key] = value
        #         else:
        #             dic[key] = value
        #         position = s.find('str.at', (position+1))
        #     for key in dic:
        #         s += '(assert (> (str.len ' + key + ') ' + dic[key] + '))\n'

        if '*@sp' in s:
            dic = {}
            position = s.find('*@sp', 0)
            while position != -1:
                var = s[position: position+7]
                if var not in dic:
                    dic[var] = 0
                    pre += '(declare-fun ' + var + ' () String )\n'
                position = s.find('*@sp', (position+3))

        if '.split' in s:
            import random
            # print(s)
            position = s.find('.split')
            dic = {}
            # print(s)
            while position != -1:
                end = position + 6
                real_end = self.findMatch(s, end, 1, '(', ')')
                split_value = s[end+1:real_end]
                end = real_end + 1
                start = self.findMatch(s, position, -1, ')', '(')
                name = s[start+1:position]
                # print('name', name)
                ran1 = random.randint(0, 9)
                ran2 = random.randint(0, 9)
                ran3 = random.randint(0, 9)
                ran = str(ran1) + str(ran2) + str(ran3)
                s = s.replace(s[start:end+1], '*@ss%s' % (ran))

                # print('*@ss%s' % (ran))
                pre += '(declare-fun ' + '*@ss%s' % (ran) + ' () String )\n'
                
                find_index = s.find('*@ss%s' % (ran))
                max_index = -1
                while find_index != -1:
                    try:
                        start_position = find_index + 7
                        # print(s[start_position:])
                        # if s[start_position] != '[':

                        end_position = self.findMatch(s, start_position, 1, '[', ']')
                        value_s = s[start_position+1: end_position]
                        temp = int(value_s)
                        vs = s[find_index: start_position] + value_s
                        s = s[: start_position] + value_s + s[end_position+1:]
                        if vs not in dic:
                            dic[vs] = 0
                            pre += '(declare-fun ' + vs + ' () String )\n'
                        if temp > max_index:
                            max_index = temp
                    except Exception as e:
                        pass
                        # import traceback
                        # import sys
                        # error_class = e.__class__.__name__ 
                        # detail = e.args[0] 
                        # cl, exc, tb = sys.exc_info() 
                        # print(traceback.format_exc())
                        # lastCallStack = traceback.extract_tb(tb)[-1] 
                        # fileName = lastCallStack[0] 
                        # lineNum = lastCallStack[1] 
                        # funcName = lastCallStack[2] 
                        # errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
                        # print(e)
                    find_index = s.find('*@ss%s' % (ran), find_index+1)
                cons = ''

                for i in range(max_index+1):
                    if '*@ss%s%d' % (ran, i) not in dic:
                        pre += '(declare-fun ' + '*@ss%s%d' % (ran, i) + ' () String )\n'
                    if i == max_index:
                        cons += ' *@ss%s%d %s' % (ran, i, '*@sstring'+ran)
                    else:
                        cons += ' *@ss%s%d %s ' % (ran, i, split_value)
                if cons != '':
                    s += '(assert (= %s (str.++ %s )))\n' % (name, cons)
                str_len = s.find('str.len')
                while str_len != -1:
                    if '*@ss' not in s[str_len + 8: str_len + 15] or s[str_len+15].isdigit():
                        str_len = s.find('str.len', str_len+1)
                        continue
                    compare_op = (s[str_len-3])
                    size = int(s[str_len+17])
                    # print(compare_op, size)

                    arg = s[str_len + 8: str_len + 15]
                    
                    move_index = 0
                    end_index = s.find('\n', str_len)
                    while s[str_len - move_index] != '\n':
                        move_index += 1
                    length = end_index - (str_len - move_index)
                    # str_len -= length
                    s = s[:str_len - move_index + 1] + s[end_index+1:]
                    # s = s[:str_len-3] + '= 1 1' + s[str_len+18:]
                    if compare_op == '=':
                        cons = ''
                        rand1 = random.randint(0, 9)
                        rand2 = random.randint(0, 9)
                        rand = str(rand1)+str(rand2)
                        for i in range(size):
                            if i == size -1:
                                cons += ' *@slen%s%d ' % (rand, i)
                            else:
                                cons += '*@slen%s%d ' % (rand, i) + " %s " % split_value
                            
                            pre += '(declare-fun ' + '*@slen%s%d' % (rand, i) + ' () String )\n'
                            # pre += '(declare-fun ' + '*@sstring%s' % (str(ran)) + ' () String )\n'
                        if cons != '':
                            s += '(assert (= %s (str.++ %s \"\")))\n' % (arg, cons)
                        s += '(assert (= %s %s)) \n' % (name, arg)
                    elif compare_op == '>':
                        cons = ''
                        rand1 = random.randint(0, 9)
                        rand2 = random.randint(0, 9)
                        rand = str(rand1)+str(rand2)
                        pre += '(declare-fun ' + '*@sstring%s' % (str(rand)) + ' () String )\n'
                        for i in range(size + 1):
                            if i == size:
                                cons += ' *@slen%s%d %s ' % (rand, i, '*@sstring'+str(rand))
                            else:
                                cons += '*@slen%s%d ' % (rand, i) + " %s " % split_value
                            pre += '(declare-fun ' + '*@slen%s%d' % (rand, i) + ' () String )\n'
                        if cons != '':
                            s += '(assert (= %s (str.++ %s )))\n' % (arg, cons)
                        s += '(assert (= %s %s)) \n' % (name, arg)
                    elif compare_op == '<':
                        cons = ''
                        rand1 = random.randint(0, 9)
                        rand2 = random.randint(0, 9)
                        rand = str(rand1)+str(rand2)
                        ct = ''
                        for i in range(size):
                            if i == 0:
                                cons += ' *@slen%s%d ' % (rand, i)
                            else:
                                cons += " %s " % split_value + '*@slen%s%d ' % (rand, i)
                            pre += '(declare-fun ' + '*@slen%s%d' % (rand, i) + ' () String )\n'
                            ct += '(or (= %s (str.++ %s \"\"))' % (arg, cons)
                            # pre += '(declare-fun ' + '*@sstring%s%s' % (str(ran), str(i)) + ' () String )\n'
                            s += '(assert (not (str.contains %s %s)))\n' % ('*@slen%s%d' % (rand, i), split_value)
                        ct += ' false ' + ')' * size
                        if size != 0:
                            s += '(assert %s)\n' % (ct)
                        s += '(assert (= %s %s)) \n' % (name, arg)
                    str_len = s.find('str.len', str_len-length+1)
                

                pre += '(declare-fun ' + '*@sstring'+ran + ' () String )\n'
                position = s.find('.split', position+1)

            
        # if '-' in smt:
        #     position = smt.find('-', 0)
        #     while position != -1:
        #         if smt[position+1] == '(' or smt[position+1] == ' ':
        #             position = smt.find('-', (position+1))
        #             continue
        #         move = 1
        #         while smt[position+move] != ')' and smt[position+move] != ' ' and smt[position+move] != '(':
        #             move += 1
        #         print(smt[position+1: position+move+1])
        #         smt = smt[0: position] + '(- 0 %s)' % (smt[position+1: position+move+1]) + smt[position+move+1:]
        #         position = smt.find('-', (position+1))
        # if 'str.substr' in smt:
        #     dic = {}
        #     position = smt.find('str.substr', 0)
        #     while position != -1:
        #         start = smt[position: ]
        #         lst = start.split(" ")
        #         key = lst[1]
        #         value = lst[3]
        #         if key in dic:
        #             if dic[key] < value:
        #                 dic[key] = value
        #         else:
        #             dic[key] = value
        #         position = smt.find('str.substr', (position+1))
        #     for key in dic:

        #         s += '(assert (>= (str.len ' + key + ') ' + dic[key] + '))\n'

        if 'max' in s:
            pre += '(define-fun max ((a Int) (b Int)) Int \n (ite (>= a b) a b))\n'
        if 'min' in s:  
            pre += '(define-fun min ((a Int) (b Int)) Int \n (ite (<= a b) a b))\n'
        if 'do_abs' in s:
            pre += '(define-fun do_abs ((a Int)) Int \n (ite (< a 0) (* (- 0 1) a) a))\n'
        if 'isdigit' in s:
            pre += '(define-fun isdigit ((a String)) Bool\n (str.in_re a (re.++ (re.* (str.to_re "0")) (re.* (str.to_re "1")) (re.* (str.to_re "2")) (re.* (str.to_re "3")) (re.* (str.to_re "4")) (re.* (str.to_re "5")) (re.* (str.to_re "6")) (re.* (str.to_re "7")) (re.* (str.to_re "8")) (re.* (str.to_re "9")))))\n'
        s = pre + s      
        s += '(check-sat)\n (get-model)\n'
        return s

    def generate_constraint(self, c):
        if c.startswith('not('):
            n = Node('not')
            lc = self.generate_constraint(c[4:-1].strip())
            # lc = Node(c[4:-1].strip())
            n.left_child = lc

        elif c.__contains__('=='):
            n = Node('=')
            splt = c.split('==')
            left = splt[0].strip()
            right = splt[1].strip()

            if self.is_variable(left):
                lc = Node(left)
            else:
                lc = self.generate_constraint(left)

            if self.is_variable(right):
                rc = Node(right)
            else:
                rc = self.generate_constraint(right)

            n.left_child = lc
            n.right_child = rc

        elif c.__contains__('not in'):
            n_down = Node('str.contains')
            splt = c.split('not in')
            left = splt[0].strip()
            right = splt[1].strip()

            if self.is_variable(right):
                lc = Node(right)
            else:
                lc = self.generate_constraint(right)

            if self.is_variable(left):
                rc = Node(left)
            else:
                rc = self.generate_constraint(left)

            n_down.left_child = lc
            n_down.right_child = rc

            n = Node('not')
            n.left_child = n_down

        elif c.startswith('*') and (not c.__contains__('.')) and (not c.__contains__('[')) and (
        not c.__contains__('(')):
            n_down = Node('isNull')
            lc = Node(c)
            n_down.left_child = lc

            n = Node('not')
            n.left_child = n_down

        # elif c.__contains__('in'):
        #     n = Node('contains')
        #     splt = c.split('in')
        #     lc = generate_constraint(splt[0].strip())
        #     rc = generate_constraint(splt[1].strip())
        #     n.left_child = lc
        #     n.right_child = rc

        # Minimal item
        else:
            # print c
            n = Node(c)

        return n

    def is_variable(self, c):
        if c.startswith('*') and (not c.__contains__('.')) and (not c.__contains__('[')) and (
        not c.__contains__('(')):
            return True
        else:
            return False
