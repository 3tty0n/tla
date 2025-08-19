from rpython.rlib import jit

# there are a couple of files:
# test_tla.py contains tests for the interpreter to pass
# targettla.py is the "Makefile" for RPython
# tla.py (this file) contains the interpreter itself
# *.tla.py small example programs
# tla_assembler.py assembles the example programs into *.tla files that can be run

OPNAMES = []
HASARG = []

def define_op(name, has_arg=False):
    globals()[name] = len(OPNAMES)
    OPNAMES.append(name)
    HASARG.append(has_arg)

# CONST_INT VALUE: push integer VALUE to stack
define_op("CONST_INT", True)

# POP: pop the top element of the stack
define_op("POP")

# ADD: pop two elements from the stack, add them and push the result
define_op("ADD")

# EXIT: stop execution and return the top stack element
define_op("EXIT")

# JUMP_IF TARGET: pop element from the stack and jump to target if it is true
define_op("JUMP_IF", True)

# DUP: duplicate the top stack element
define_op("DUP")

# SUB: pop two elements from the stack, subtract them and push the result
define_op("SUB")

# NEWSTR CHAR: make a new string of length 1 with the given character CHAR
define_op("NEWSTR", True)


def assemble(mylist):
    return ''.join([chr(x) for x in mylist])

# ____________________________________________________________


class W_Object:
    def getrepr(self):
        """
        Return an RPython string which represent the object
        """
        raise NotImplementedError

    def is_true(self):
        raise NotImplementedError

    def add(self, w_other):
        raise NotImplementedError



class W_IntObject(W_Object):
    pass # add code here...


class W_StringObject(W_Object):
    pass # add code here...



# ____________________________________________________________

def opcode_to_string(pc, bytecode):
    op = ord(bytecode[pc])
    name = OPNAMES[op]
    if HASARG[op]:
        arg = str(ord(bytecode[pc + 1]))
    else:
        arg = ''
    return "%s: %s %s" % (pc, name, arg)

jitdriver = jit.JitDriver(greens=['pc', 'bytecode'],
                          reds=['self'],
                          get_printable_location=opcode_to_string)

class Frame(object):
    # add code here

    def interp(self):
        # implement bytecode dispatch loop here
        pass


def run(bytecode, w_arg):
    frame = Frame(bytecode)
    frame.push(w_arg)
    w_result = frame.interp()
    return w_result
