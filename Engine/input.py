import glfw

KEYS = {
    "A": glfw.KEY_A, "B": glfw.KEY_B, "C": glfw.KEY_C, "D": glfw.KEY_D,
    "E": glfw.KEY_E, "F": glfw.KEY_F, "G": glfw.KEY_G, "H": glfw.KEY_H,
    "I": glfw.KEY_I, "J": glfw.KEY_J, "K": glfw.KEY_K, "L": glfw.KEY_L,
    "M": glfw.KEY_M, "N": glfw.KEY_N, "O": glfw.KEY_O, "P": glfw.KEY_P,
    "Q": glfw.KEY_Q, "R": glfw.KEY_R, "S": glfw.KEY_S, "T": glfw.KEY_T,
    "U": glfw.KEY_U, "V": glfw.KEY_V, "W": glfw.KEY_W, "X": glfw.KEY_X,
    "Y": glfw.KEY_Y, "Z": glfw.KEY_Z,
    "0": glfw.KEY_0, "1": glfw.KEY_1, "2": glfw.KEY_2, "3": glfw.KEY_3,
    "4": glfw.KEY_4, "5": glfw.KEY_5, "6": glfw.KEY_6, "7": glfw.KEY_7,
    "8": glfw.KEY_8, "9": glfw.KEY_9,
    "UP": glfw.KEY_UP, "DOWN": glfw.KEY_DOWN,
    "LEFT": glfw.KEY_LEFT, "RIGHT": glfw.KEY_RIGHT,
    "SPACE": glfw.KEY_SPACE, "ENTER": glfw.KEY_ENTER,
    "TAB": glfw.KEY_TAB, "ESC": glfw.KEY_ESCAPE,
    "BACKSPACE": glfw.KEY_BACKSPACE,
    "SHIFT": glfw.KEY_LEFT_SHIFT, "CTRL": glfw.KEY_LEFT_CONTROL,
    "ALT": glfw.KEY_LEFT_ALT,
    "F1": glfw.KEY_F1, "F2": glfw.KEY_F2, "F3": glfw.KEY_F3, "F4": glfw.KEY_F4,
    "F5": glfw.KEY_F5, "F6": glfw.KEY_F6, "F7": glfw.KEY_F7, "F8": glfw.KEY_F8,
    "F9": glfw.KEY_F9, "F10": glfw.KEY_F10, "F11": glfw.KEY_F11, "F12": glfw.KEY_F12,
}

_prev = {}
_now = {}


def in_update():
    global _prev, _now
    _prev = _now.copy()
    _now = {}
    window = glfw.get_current_context()
    for name, key in KEYS.items():
        _now[name] = glfw.get_key(window, key)


def in_pressed(name):
    return _now.get(name, glfw.RELEASE) == glfw.PRESS and \
           _prev.get(name, glfw.RELEASE) == glfw.RELEASE


def in_down(name):
    return _now.get(name, glfw.RELEASE) in (glfw.PRESS, glfw.REPEAT)


def in_released(name):
    return _now.get(name, glfw.RELEASE) == glfw.RELEASE and \
           _prev.get(name, glfw.RELEASE) in (glfw.PRESS, glfw.REPEAT)
