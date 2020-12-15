def build_in(a, b):
    array = [1, 2, 3, a, b]

    summing = sum(array)
    do_max = max(a, 100)
    do_min = min(b, 0)
    summing += do_min

    if summing > do_max:
        return 0
    else:
        return 1



def do_abs(a, b):
    if abs(a) >= abs(b):
        return 0
    else:
        return 1

def do_array(a, b):
    array = [1, 2, 3, 4]

    sliced = array[2:]
    c = sliced[0]

    d = array[1:3]

    array[0] = 6
    return array[0]

def do_numbers(a, b):
    c = 100 if a > b else 0
    if c > a:
        return a
    else:
        return b


def do_range(a, b):
    cnt = 0
    for i in range(b, a):
        for j in range(1, 4):
            for k in range(1, 4):
                cnt += 1
    d = cnt
    return d

def loop(a, b):
    arr = [a, a, b, a, a, a]
    cnt = 0
    for ele in arr:
        if ele > 1:
            break
        cnt += ele
    return cnt

def while_loop(a, b):
    i = 0
    j = 0
    cnt = 0
    while i < 3:
        j = 0
        while j < 3:
            cnt += 1
            j += 1
        i += 1

    return cnt

def add_digits(num):
    if num<9:
        return num
    elif num%9==0:
        return 9
    else:
        return num%9


def multiplication_or_sum(num1, num2):
	product = num1 *num2
	if(product < 1000):
		return product
	else:
		return num1 +num2


def string_find(a, b):
    search = a.find('ggg')
    ret = 0
    if search < 5:
        ret = 1
    else:
        ret = 2
	  return ret


def string_in(a, b):
    if "abc" in a:
        return 0
    else:
        return 1


def string_slice(a, b):
    c = a[1:3]
    c += b
    return c

def string_iter(a, b):
    cnt = ""
    for ele in a:
        cnt += ele
    return cnt


class TheSubClass:
    def __init__(self, value:str):
        self.sub = sub_sub_import.TheSubSubClass(value)
        self.value = sub_sub_import.sub_sub_func(value, value)
        self.value = value

    def __str__(self):
        return self.value

def sub_func(a, b):
    a = a + 1
    return a


class TheSubSubClass:
    def __init__(self, value:str):
        self.value = value

    def __str__(self):
        return self.value

def sub_sub_func(a, b):
    return a
    

def count_emma(statement):
  count = 0
  for i in range(len(statement)-1):
    if statement[i:i+4] == 'Emma':
        count += 1
    # Cannot handle the
    # count += statement[i:i+4] == 'Emma'
  return count

  
def multiplication_or_sum(num1, num2):
  product = num1 *num2
  if(product < 1000):
    return product
  else:
    return num1 +num2


import re   # pragma: no cover

def regex(string):
    """This function returns at least one matching digit."""
    pattern = re.compile(r"^(\d+)") # For brevity, this is the same as r"\d+"
    result = pattern.match(string)
    if result:
        return  result.group()
    return None