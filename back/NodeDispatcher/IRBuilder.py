from .dispatcher import NodeDispatcher

@NodeDispatcher.register("ROTATE_LEFT")
def handle_rotate_left(parser, n):
    return parser.cyclic_left_shift(n.inputs, n.params["amount"])

@NodeDispatcher.register("ADD_MOD")
def handle_add_mod(parser, n):
    return parser.modulo_addition(n.inputs[0], n.inputs[1], n.outputs)

@NodeDispatcher.register("XOR")
def handle_xor(parser, n):
    return parser.bitwise_xor(n.inputs, n.outputs)