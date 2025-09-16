import math
import tkinter as tk


# Simple colors and sizes
MAIN_BG = "#1E1E2E"
BTN_BG = "#2D2D3A"
FUNC_BG = "#4C4C6D"
EQUALS_BG = "#FF6B6B"
ACCENT_BG = "#FFB347"
BTN_FG = "#FFFFFF"
DISPLAY_BG = "#121212"
DISPLAY_FG = "#00FFAB"

STANDARD_MIN_W, STANDARD_MIN_H = 360, 560
SCIENTIFIC_MIN_W, SCIENTIFIC_MIN_H = 520, 560


# Global state
root = tk.Tk()
root.title("Scientific Calculator")
root.configure(bg=MAIN_BG)
root.geometry("560x640")

is_scientific = True
angle_mode = tk.StringVar(value="DEG")
memory_value = 0.0
expression = tk.StringVar(value="")


def ensure_cursor_end():
    try:
        display.icursor("end")
        display.xview_moveto(1.0)
    except Exception:
        pass


def build_menu():
    menubar = tk.Menu(root)
    view_menu = tk.Menu(menubar, tearoff=0)
    view_menu.add_command(label="Standard", command=lambda: set_scientific(False))
    view_menu.add_command(label="Scientific", command=lambda: set_scientific(True))
    menubar.add_cascade(label="View", menu=view_menu)
    root.config(menu=menubar)


def build_display():
    global display
    frame = tk.Frame(root, bg=MAIN_BG)
    frame.grid(row=0, column=0, sticky="nsew", padx=16, pady=(16, 8))
    display = tk.Entry(
        frame,
        textvariable=expression,
        font=("SFMono", 28, "bold"),
        bg=DISPLAY_BG,
        fg=DISPLAY_FG,
        insertbackground=DISPLAY_FG,
        relief="flat",
        borderwidth=0,
        justify="right",
        takefocus=0,
    )
    display.pack(fill="both", expand=True)
    display.bind("<Key>", lambda e: "break")
    display.bind("<Button-1>", lambda e: "break")
    display.bind("<FocusIn>", lambda e: root.focus_set())


def build_toggles():
    global mode_btn, deg_btn
    frame = tk.Frame(root, bg=MAIN_BG)
    frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
    mode_btn = tk.Button(frame, text="Scientific" if is_scientific else "Standard", command=toggle_mode,
                         bg=FUNC_BG, fg=BTN_FG, relief="flat", padx=12, pady=8)
    mode_btn.pack(side="left")
    spacer = tk.Frame(frame, bg=MAIN_BG)
    spacer.pack(side="left", expand=True)
    deg_btn = tk.Button(frame, text="DEG", command=toggle_angle_mode,
                        bg=FUNC_BG, fg=BTN_FG, relief="flat", padx=12, pady=8)
    deg_btn.pack(side="right")


def btn(parent, text, cmd, kind="normal"):
    bg = BTN_BG
    fg = BTN_FG
    if kind == "func":
        bg = FUNC_BG
    elif kind == "equals":
        bg = EQUALS_BG
    elif kind == "accent":
        bg = ACCENT_BG
        fg = "#2D1B00"
    return tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg, relief="flat", padx=8, pady=8, font=("SFMono", 14, "bold"))


def populate_standard_keys(parent):
    grid = tk.Frame(parent, bg=MAIN_BG)
    grid.pack(fill="both", expand=True)
    for r in range(6):
        grid.grid_rowconfigure(r, weight=1, uniform="std")
    for c in range(4):
        grid.grid_columnconfigure(c, weight=1, uniform="std")

    btn(grid, "MC", lambda: memory("MC"), kind="func").grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "MR", lambda: memory("MR"), kind="func").grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "M+", lambda: memory("M+"), kind="func").grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "M-", lambda: memory("M-"), kind="func").grid(row=0, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "C", clear, kind="accent").grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "⌫", backspace, kind="accent").grid(row=1, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "(", lambda: append("("), kind="func").grid(row=1, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, ")", lambda: append(")"), kind="func").grid(row=1, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "7", lambda: append("7")).grid(row=2, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "8", lambda: append("8")).grid(row=2, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "9", lambda: append("9")).grid(row=2, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "÷", lambda: append(" ÷ "), kind="func").grid(row=2, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "4", lambda: append("4")).grid(row=3, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "5", lambda: append("5")).grid(row=3, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "6", lambda: append("6")).grid(row=3, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "×", lambda: append(" × "), kind="func").grid(row=3, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "1", lambda: append("1")).grid(row=4, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "2", lambda: append("2")).grid(row=4, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "3", lambda: append("3")).grid(row=4, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "-", lambda: append(" - "), kind="func").grid(row=4, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "0", lambda: append("0")).grid(row=5, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, ".", lambda: append(".")).grid(row=5, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "+", lambda: append(" + "), kind="func").grid(row=5, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "=", evaluate, kind="equals").grid(row=5, column=3, sticky="nsew", padx=6, pady=6)


def populate_scientific_keys(parent):
    grid = tk.Frame(parent, bg=MAIN_BG)
    grid.pack(fill="both", expand=True)
    for r in range(6):
        grid.grid_rowconfigure(r, weight=1, uniform="sci")
    for c in range(4):
        grid.grid_columnconfigure(c, weight=1, uniform="sci")

    btn(grid, "sin", lambda: append("sin("), kind="func").grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "cos", lambda: append("cos("), kind="func").grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "tan", lambda: append("tan("), kind="func").grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "^", lambda: append(" ^ "), kind="func").grid(row=0, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "asin", lambda: append("asin("), kind="func").grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "acos", lambda: append("acos("), kind="func").grid(row=1, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "atan", lambda: append("atan("), kind="func").grid(row=1, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "√", lambda: append("sqrt("), kind="func").grid(row=1, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "sinh", lambda: append("sinh("), kind="func").grid(row=2, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "cosh", lambda: append("cosh("), kind="func").grid(row=2, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "tanh", lambda: append("tanh("), kind="func").grid(row=2, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "x²", lambda: append("square("), kind="func").grid(row=2, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "log", lambda: append("log10("), kind="func").grid(row=3, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "ln", lambda: append("ln("), kind="func").grid(row=3, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "exp", lambda: append("exp("), kind="func").grid(row=3, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "x³", lambda: append("cube("), kind="func").grid(row=3, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "x!", lambda: append("factorial("), kind="func").grid(row=4, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "|x|", lambda: append("abs("), kind="func").grid(row=4, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "π", lambda: append("pi"), kind="func").grid(row=4, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "e", lambda: append("e"), kind="func").grid(row=4, column=3, sticky="nsew", padx=6, pady=6)

    btn(grid, "%", lambda: append("%"), kind="func").grid(row=5, column=0, sticky="nsew", padx=6, pady=6)
    btn(grid, "÷", lambda: append(" ÷ "), kind="func").grid(row=5, column=1, sticky="nsew", padx=6, pady=6)
    btn(grid, "×", lambda: append(" × "), kind="func").grid(row=5, column=2, sticky="nsew", padx=6, pady=6)
    btn(grid, "+/-", toggle_sign, kind="func").grid(row=5, column=3, sticky="nsew", padx=6, pady=6)


def build_keypads():
    global main_frame, science_frame, standard_frame
    main_frame = tk.Frame(root, bg=MAIN_BG)
    main_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
    science_frame = tk.Frame(main_frame, bg=MAIN_BG)
    standard_frame = tk.Frame(main_frame, bg=MAIN_BG)
    science_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
    standard_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    populate_scientific_keys(science_frame)
    populate_standard_keys(standard_frame)
    set_scientific(is_scientific)


def configure_grid():
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)


def toggle_mode():
    set_scientific(not get_is_scientific())


def get_is_scientific():
    return science_frame.winfo_ismapped()


def set_scientific(is_sci):
    global is_scientific
    is_scientific = is_sci
    mode_btn.configure(text="Scientific" if is_sci else "Standard")
    if is_sci:
        science_frame.grid()
    else:
        science_frame.grid_remove()
    apply_min_size()


def toggle_angle_mode():
    angle_mode.set("RAD" if angle_mode.get() == "DEG" else "DEG")
    deg_btn.configure(text=angle_mode.get())


def append(value):
    expression.set(expression.get() + value)
    ensure_cursor_end()


def clear():
    expression.set("")
    ensure_cursor_end()


def backspace():
    expression.set(expression.get()[:-1])
    ensure_cursor_end()


def toggle_sign():
    expr = expression.get()
    if not expr:
        return
    i = len(expr) - 1
    while i >= 0 and (expr[i].isdigit() or expr[i] == '.'):
        i -= 1
    if i >= 0 and expr[i] == '-':
        expression.set(expr[:i] + expr[i+1:])
    else:
        expression.set(expr[:i+1] + '-' + expr[i+1:])
    ensure_cursor_end()


def handle_keypress(event):
    char = event.char
    keysym = event.keysym
    if keysym in ("Return", "KP_Enter"):
        evaluate()
        return "break"
    if keysym == "BackSpace":
        backspace()
        return "break"
    if keysym == "Escape":
        clear()
        return "break"
    if char and char.isalpha():
        return "break"
    allowed = set("0123456789.+-*/()^%")
    if char in allowed:
        mapping = {'*': ' × ', '/': ' ÷ ', '^': ' ^ '}
        append(mapping.get(char, char))
        return "break"
    return "break"


def transform_percent(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        if s[i] == '%':
            out.append("/100")
            i += 1
        else:
            out.append(s[i])
            i += 1
    return ''.join(out)


def preprocess(expr: str) -> str:
    expr = expr.replace('×', '*').replace('÷', '/')
    expr = expr.replace('^', '**')
    expr = transform_percent(expr)
    return expr


def build_env():
    def to_rad(x):
        return math.radians(x) if angle_mode.get() == "DEG" else x
    def to_deg(x):
        return math.degrees(x) if angle_mode.get() == "DEG" else x

    def sin_(x):
        return math.sin(to_rad(x))
    def cos_(x):
        return math.cos(to_rad(x))
    def tan_(x):
        return math.tan(to_rad(x))
    def asin_(x):
        return to_deg(math.asin(x))
    def acos_(x):
        return to_deg(math.acos(x))
    def atan_(x):
        return to_deg(math.atan(x))

    def ln_(x):
        return math.log(x)
    def square(x):
        return x * x
    def cube(x):
        return x * x * x

    return {
        'sin': sin_, 'cos': cos_, 'tan': tan_,
        'asin': asin_, 'acos': acos_, 'atan': atan_,
        'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
        'log10': math.log10, 'ln': ln_, 'exp': math.exp, 'pow': math.pow,
        'sqrt': math.sqrt, 'factorial': math.factorial, 'abs': abs,
        'square': square, 'cube': cube, 'pi': math.pi, 'e': math.e,
    }


def safe_eval(expr: str):
    import ast
    expr = preprocess(expr)
    allowed_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Load,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd,
        ast.Call, ast.Name, ast.Constant, ast.Mod
    )

    def _check(node):
        if not isinstance(node, allowed_nodes):
            raise ValueError("Disallowed expression")
        for child in ast.iter_child_nodes(node):
            _check(child)

    tree = ast.parse(expr, mode='eval')
    _check(tree)
    env = build_env()

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if hasattr(ast, 'Num') and isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.Name):
            if node.id in env:
                return env[node.id]
            raise ValueError("Unknown identifier")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                return left ** right
            if isinstance(node.op, ast.Mod):
                return left % right
            raise ValueError
        if isinstance(node, ast.Call):
            func = _eval(node.func)
            args = [_eval(a) for a in node.args]
            if len(node.keywords) != 0:
                raise ValueError("No keywords allowed")
            return func(*args)
        raise ValueError

    return _eval(tree)


def evaluate():
    expr = expression.get().strip()
    if not expr:
        return
    try:
        result = safe_eval(expr)
        if result is None or isinstance(result, complex) or (isinstance(result, float) and (math.isnan(result) or math.isinf(result))):
            raise ValueError
        if isinstance(result, float) and abs(result - int(result)) < 1e-12:
            result = int(result)
        expression.set(str(result))
        ensure_cursor_end()
    except Exception:
        expression.set("Math Error")
        ensure_cursor_end()


def memory(op: str):
    global memory_value
    try:
        current = safe_eval(expression.get()) if expression.get() else 0.0
    except Exception:
        current = 0.0
    if op == "MC":
        memory_value = 0.0
    elif op == "MR":
        expression.set(str(format_number(memory_value)))
        return
    elif op == "M+":
        memory_value += float(current)
    elif op == "M-":
        memory_value -= float(current)


def format_number(val):
    if isinstance(val, float) and abs(val - int(val)) < 1e-12:
        return int(val)
    return val


def apply_min_size():
    if is_scientific:
        root.minsize(SCIENTIFIC_MIN_W, SCIENTIFIC_MIN_H)
    else:
        root.minsize(STANDARD_MIN_W, STANDARD_MIN_H)


def main():
    build_menu()
    build_display()
    build_toggles()
    build_keypads()
    configure_grid()
    apply_min_size()
    root.bind("<Key>", handle_keypress)
    root.mainloop()


if __name__ == "__main__":
    main()


