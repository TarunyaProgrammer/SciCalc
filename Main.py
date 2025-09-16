import math
import tkinter as tk
from tkinter import ttk


# -----------------------------
# Color and Style Configuration
# -----------------------------
MAIN_BG = "#1E1E2E"       # deep dark gray
BTN_BG = "#2D2D3A"        # dark slate
FUNC_BG = "#4C4C6D"       # muted blue-gray
EQUALS_BG = "#FF6B6B"     # modern coral red
ACCENT_BG = "#FFB347"     # amber/orange accent (clear/backspace)
BTN_FG = "#FFFFFF"         # white
DISPLAY_BG = "#121212"    # near black
DISPLAY_FG = "#00FFAB"    # neon teal/green

# Minimum sizes for each mode
STANDARD_MIN_W, STANDARD_MIN_H = 360, 560
SCIENTIFIC_MIN_W, SCIENTIFIC_MIN_H = 520, 560


def lighten_color(hex_color: str, factor: float = 0.12) -> str:
    """Return a lighter shade of the given hex color by the factor (0-1)."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02X}{g:02X}{b:02X}"


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        master,
        text: str = "",
        command=None,
        width: int = 80,
        height: int = 56,
        radius: int = 12,
        bg_color: str = BTN_BG,
        fg_color: str = BTN_FG,
        hover_lighten: float = 0.12,
        font=("SFMono", 14, "bold"),
        **kwargs,
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            highlightthickness=0,
            bd=0,
            bg=MAIN_BG,
            **kwargs,
        )
        self.command = command
        self.text = text
        self.radius = radius
        self.base_bg = bg_color
        self.hover_bg = lighten_color(bg_color, hover_lighten)
        self.fg = fg_color
        self.font = font
        self._draw()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Key-Return>", self._on_click)
        self.bind("<Key-space>", self._on_click)
        self.focusable = True

    def _draw(self):
        self.delete("all")
        w = int(self["width"]) if isinstance(self["width"], str) else self["width"]
        h = int(self["height"]) if isinstance(self["height"], str) else self["height"]
        r = min(self.radius, w // 2, h // 2)
        x1, y1, x2, y2 = 2, 2, w - 2, h - 2
        # Rounded rectangle using rectangles and arcs
        self.shape_parts = [
            self.create_rectangle(x1 + r, y1, x2 - r, y2, outline=self.base_bg, fill=self.base_bg),
            self.create_rectangle(x1, y1 + r, x2, y2 - r, outline=self.base_bg, fill=self.base_bg),
            self.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, outline=self.base_bg, fill=self.base_bg),
            self.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, outline=self.base_bg, fill=self.base_bg),
            self.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, outline=self.base_bg, fill=self.base_bg),
            self.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, outline=self.base_bg, fill=self.base_bg),
        ]
        self.text_item = self.create_text((w // 2, h // 2), text=self.text, fill=self.fg, font=self.font)

    def _paint(self, color: str):
        for item in self.shape_parts:
            self.itemconfig(item, fill=color, outline=color)

    def _on_enter(self, _):
        self._paint(self.hover_bg)

    def _on_leave(self, _):
        self._paint(self.base_bg)

    def _on_click(self, _):
        if callable(self.command):
            self.command()

    def _on_press(self, _):
        pass

    def _on_release(self, _):
        pass


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.configure(bg=MAIN_BG)
        self.geometry("560x640")

        # Modes
        self.is_scientific = True
        self.angle_mode = tk.StringVar(value="DEG")  # or "RAD"

        # Memory
        self.memory_value = 0.0

        # Expression state
        self.expression = tk.StringVar(value="")

        self._build_menu()
        self._build_display()
        self._build_toggles()
        self._build_keypads()
        self._configure_grid()
        self._apply_min_size()

        self.bind("<Key>", self._handle_keypress)

    # ---------- UI Construction ----------
    def _build_menu(self):
        menubar = tk.Menu(self)
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Standard", command=lambda: self._set_scientific(False))
        view_menu.add_command(label="Scientific", command=lambda: self._set_scientific(True))
        menubar.add_cascade(label="View", menu=view_menu)
        self.config(menu=menubar)

    def _build_display(self):
        display_frame = tk.Frame(self, bg=MAIN_BG)
        display_frame.grid(row=0, column=0, sticky="nsew", padx=16, pady=(16, 8))

        self.display = tk.Entry(
            display_frame,
            textvariable=self.expression,
            font=("SFMono", 28, "bold"),
            bg=DISPLAY_BG,
            fg=DISPLAY_FG,
            insertbackground=DISPLAY_FG,
            relief="flat",
            borderwidth=0,
            justify="right",
            takefocus=0,
        )
        self.display.pack(fill="both", expand=True)
        # Prevent direct typing/cursor edits in the entry
        self.display.bind("<Key>", lambda e: "break")
        self.display.bind("<Button-1>", lambda e: "break")
        self.display.bind("<FocusIn>", lambda e: self.focus_set())

    def _build_toggles(self):
        toggle_frame = tk.Frame(self, bg=MAIN_BG)
        toggle_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))

        self.mode_btn = RoundedButton(
            toggle_frame,
            text="Scientific" if self.is_scientific else "Standard",
            command=self._toggle_mode,
            width=130,
            height=38,
            radius=10,
            bg_color=FUNC_BG,
            font=("SFMono", 12, "bold"),
        )
        self.mode_btn.pack(side="left")

        spacer = tk.Frame(toggle_frame, bg=MAIN_BG)
        spacer.pack(side="left", expand=True)

        self.deg_btn = RoundedButton(
            toggle_frame,
            text="DEG",
            command=self._toggle_angle_mode,
            width=90,
            height=38,
            radius=10,
            bg_color=FUNC_BG,
            font=("SFMono", 12, "bold"),
        )
        self.deg_btn.pack(side="right")

    def _build_keypads(self):
        self.main_frame = tk.Frame(self, bg=MAIN_BG)
        self.main_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))

        # Scientific panel (left/top)
        self.science_frame = tk.Frame(self.main_frame, bg=MAIN_BG)
        # Standard panel (always shown on right/bottom)
        self.standard_frame = tk.Frame(self.main_frame, bg=MAIN_BG)

        self.science_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.standard_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self._populate_scientific_keys()
        self._populate_standard_keys()
        self._set_scientific(self.is_scientific)

    def _btn(self, parent, text, cmd, kind="normal"):
        color = BTN_BG
        if kind == "func":
            color = FUNC_BG
        elif kind == "equals":
            color = EQUALS_BG
        elif kind == "accent":
            color = ACCENT_BG
        return RoundedButton(parent, text=text, command=cmd, bg_color=color)

    def _populate_standard_keys(self):
        grid = tk.Frame(self.standard_frame, bg=MAIN_BG)
        grid.pack(fill="both", expand=True)

        for r in range(6):
            grid.grid_rowconfigure(r, weight=1, uniform="std")
        for c in range(4):
            grid.grid_columnconfigure(c, weight=1, uniform="std")

        # Row 0: MC, MR, M+, M-
        self._btn(grid, "MC", lambda: self._memory("MC"), kind="func").grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "MR", lambda: self._memory("MR"), kind="func").grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "M+", lambda: self._memory("M+"), kind="func").grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "M-", lambda: self._memory("M-"), kind="func").grid(row=0, column=3, sticky="nsew", padx=6, pady=6)

        # Row 1: C, ⌫, (, )
        self._btn(grid, "C", self._clear, kind="accent").grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "⌫", self._backspace, kind="accent").grid(row=1, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "(", lambda: self._append("("), kind="func").grid(row=1, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, ")", lambda: self._append(")"), kind="func").grid(row=1, column=3, sticky="nsew", padx=6, pady=6)

        # Row 2: 7 8 9 ÷
        self._btn(grid, "7", lambda: self._append("7")).grid(row=2, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "8", lambda: self._append("8")).grid(row=2, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "9", lambda: self._append("9")).grid(row=2, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "÷", lambda: self._append(" ÷ "), kind="func").grid(row=2, column=3, sticky="nsew", padx=6, pady=6)

        # Row 3: 4 5 6 ×
        self._btn(grid, "4", lambda: self._append("4")).grid(row=3, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "5", lambda: self._append("5")).grid(row=3, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "6", lambda: self._append("6")).grid(row=3, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "×", lambda: self._append(" × "), kind="func").grid(row=3, column=3, sticky="nsew", padx=6, pady=6)

        # Row 4: 1 2 3 −
        self._btn(grid, "1", lambda: self._append("1")).grid(row=4, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "2", lambda: self._append("2")).grid(row=4, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "3", lambda: self._append("3")).grid(row=4, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "-", lambda: self._append(" - "), kind="func").grid(row=4, column=3, sticky="nsew", padx=6, pady=6)

        # Row 5: 0 . + =
        self._btn(grid, "0", lambda: self._append("0")).grid(row=5, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, ".", lambda: self._append(".")).grid(row=5, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "+", lambda: self._append(" + "), kind="func").grid(row=5, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "=", self._evaluate, kind="equals").grid(row=5, column=3, sticky="nsew", padx=6, pady=6)

    def _populate_scientific_keys(self):
        grid = tk.Frame(self.science_frame, bg=MAIN_BG)
        grid.pack(fill="both", expand=True)

        for r in range(6):
            grid.grid_rowconfigure(r, weight=1, uniform="sci")
        for c in range(4):
            grid.grid_columnconfigure(c, weight=1, uniform="sci")

        # Row 0
        self._btn(grid, "sin", lambda: self._append("sin("), kind="func").grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "cos", lambda: self._append("cos("), kind="func").grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "tan", lambda: self._append("tan("), kind="func").grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "^", lambda: self._append(" ^ "), kind="func").grid(row=0, column=3, sticky="nsew", padx=6, pady=6)

        # Row 1
        self._btn(grid, "asin", lambda: self._append("asin("), kind="func").grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "acos", lambda: self._append("acos("), kind="func").grid(row=1, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "atan", lambda: self._append("atan("), kind="func").grid(row=1, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "√", lambda: self._append("sqrt("), kind="func").grid(row=1, column=3, sticky="nsew", padx=6, pady=6)

        # Row 2
        self._btn(grid, "sinh", lambda: self._append("sinh("), kind="func").grid(row=2, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "cosh", lambda: self._append("cosh("), kind="func").grid(row=2, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "tanh", lambda: self._append("tanh("), kind="func").grid(row=2, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "x²", lambda: self._append("square("), kind="func").grid(row=2, column=3, sticky="nsew", padx=6, pady=6)

        # Row 3
        self._btn(grid, "log", lambda: self._append("log10("), kind="func").grid(row=3, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "ln", lambda: self._append("ln("), kind="func").grid(row=3, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "exp", lambda: self._append("exp("), kind="func").grid(row=3, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "x³", lambda: self._append("cube("), kind="func").grid(row=3, column=3, sticky="nsew", padx=6, pady=6)

        # Row 4
        self._btn(grid, "x!", lambda: self._append("factorial("), kind="func").grid(row=4, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "|x|", lambda: self._append("abs("), kind="func").grid(row=4, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "π", lambda: self._append("pi"), kind="func").grid(row=4, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "e", lambda: self._append("e"), kind="func").grid(row=4, column=3, sticky="nsew", padx=6, pady=6)

        # Row 5
        self._btn(grid, "%", lambda: self._append("%"), kind="func").grid(row=5, column=0, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "÷", lambda: self._append(" ÷ "), kind="func").grid(row=5, column=1, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "×", lambda: self._append(" × "), kind="func").grid(row=5, column=2, sticky="nsew", padx=6, pady=6)
        self._btn(grid, "+/-", self._toggle_sign, kind="func").grid(row=5, column=3, sticky="nsew", padx=6, pady=6)

    def _configure_grid(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # ---------- Event Handlers ----------
    def _toggle_mode(self):
        self._set_scientific(not self.is_scientific)

    def _set_scientific(self, is_sci: bool):
        self.is_scientific = is_sci
        self.mode_btn.text = "Scientific" if is_sci else "Standard"
        self.mode_btn._draw()
        if is_sci:
            self.science_frame.grid()
        else:
            self.science_frame.grid_remove()
        self._apply_min_size()

    def _apply_min_size(self):
        if self.is_scientific:
            self.minsize(SCIENTIFIC_MIN_W, SCIENTIFIC_MIN_H)
        else:
            self.minsize(STANDARD_MIN_W, STANDARD_MIN_H)

    def _toggle_angle_mode(self):
        self.angle_mode.set("RAD" if self.angle_mode.get() == "DEG" else "DEG")
        self.deg_btn.text = self.angle_mode.get()
        self.deg_btn._draw()

    def _append(self, value: str):
        self.expression.set(self.expression.get() + value)
        self._ensure_cursor_end()

    def _clear(self):
        self.expression.set("")
        self._ensure_cursor_end()

    def _backspace(self):
        self.expression.set(self.expression.get()[:-1])
        self._ensure_cursor_end()

    def _toggle_sign(self):
        expr = self.expression.get()
        if not expr:
            return
        # Toggle sign of the last number token
        i = len(expr) - 1
        while i >= 0 and (expr[i].isdigit() or expr[i] == '.'):  # last numeric span
            i -= 1
        # Insert or remove unary minus
        if i >= 0 and expr[i] == '-':
            self.expression.set(expr[:i] + expr[i+1:])
        else:
            self.expression.set(expr[:i+1] + '-' + expr[i+1:])
        self._ensure_cursor_end()

    def _handle_keypress(self, event):
        char = event.char
        keysym = event.keysym
        # Handle control keys
        if keysym in ("Return", "KP_Enter"):
            self._evaluate()
            return "break"
        if keysym == "BackSpace":
            self._backspace()
            return "break"
        if keysym == "Escape":
            self._clear()
            return "break"

        # Block all alphabetic input from keyboard
        if char and char.isalpha():
            return "break"

        # Allow only specific printable characters
        allowed = set("0123456789.+-*/()^%")
        if char in allowed:
            mapping = {'*': ' × ', '/': ' ÷ ', '^': ' ^ '}
            self._append(mapping.get(char, char))
            return "break"

        # Ignore other keys (arrows, modifiers) to avoid cursor issues
        return "break"

    def _ensure_cursor_end(self):
        try:
            self.display.icursor("end")
            self.display.xview_moveto(1.0)
        except Exception:
            pass

    # ---------- Evaluation ----------
    def _evaluate(self):
        expr = self.expression.get().strip()
        if not expr:
            return
        try:
            result = self._safe_eval(expr)
            if result is None or isinstance(result, complex) or (isinstance(result, float) and (math.isnan(result) or math.isinf(result))):
                raise ValueError
            # Trim trailing .0 where appropriate
            if isinstance(result, float) and abs(result - int(result)) < 1e-12:
                result = int(result)
            self.expression.set(str(result))
            self._ensure_cursor_end()
        except Exception:
            self.expression.set("Math Error")
            self._ensure_cursor_end()

    # Percent transform: converts tokens like 50% -> (50/100)
    def _transform_percent(self, s: str) -> str:
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

    def _preprocess(self, expr: str) -> str:
        expr = expr.replace('×', '*').replace('÷', '/')
        expr = expr.replace('^', '**')
        expr = self._transform_percent(expr)
        return expr

    # Math functions with angle mode consideration
    def _build_env(self):
        def to_rad(x):
            return math.radians(x) if self.angle_mode.get() == "DEG" else x
        def to_deg(x):
            return math.degrees(x) if self.angle_mode.get() == "DEG" else x

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

        env = {
            'sin': sin_,
            'cos': cos_,
            'tan': tan_,
            'asin': asin_,
            'acos': acos_,
            'atan': atan_,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'log10': math.log10,
            'ln': ln_,
            'exp': math.exp,
            'pow': math.pow,
            'sqrt': math.sqrt,
            'factorial': math.factorial,
            'abs': abs,
            'square': square,
            'cube': cube,
            'pi': math.pi,
            'e': math.e,
        }
        return env

    def _safe_eval(self, expr: str):
        import ast

        expr = self._preprocess(expr)

        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Load,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd,
            ast.Call, ast.Name, ast.Constant, ast.Mod, ast.FloorDiv, ast.LShift, ast.RShift
        )

        def _check(node):
            if not isinstance(node, allowed_nodes):
                raise ValueError("Disallowed expression")
            for child in ast.iter_child_nodes(node):
                _check(child)

        tree = ast.parse(expr, mode='eval')
        _check(tree)

        env = self._build_env()

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

    # ---------- Memory ----------
    def _memory(self, op: str):
        try:
            current = self._safe_eval(self.expression.get()) if self.expression.get() else 0.0
        except Exception:
            current = 0.0
        if op == "MC":
            self.memory_value = 0.0
        elif op == "MR":
            # Replace expression with memory value
            self.expression.set(str(self._format_number(self.memory_value)))
            return
        elif op == "M+":
            self.memory_value += float(current)
        elif op == "M-":
            self.memory_value -= float(current)

    def _format_number(self, val):
        if isinstance(val, float) and abs(val - int(val)) < 1e-12:
            return int(val)
        return val


def main():
    app = CalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()


