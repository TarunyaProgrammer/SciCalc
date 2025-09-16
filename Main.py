import math
import tkinter as tk
from tkinter import ttk


# -----------------------------
# Color and Style Configuration
# -----------------------------
GRADIENT_TOP = "#8EC5FC"  # gradient top
GRADIENT_BOTTOM = "#E0C3FC"  # gradient bottom

# Glass + Neon theme
MAIN_BG = "#000000"  # not visible; gradient canvas used
GLASS_BG = "#EDEFF8"  # simulated frosted white (#FFFFFF20 approx)
GLASS_BORDER = "#D9DAEE"  # simulated #FFFFFF40
GLASS_RADIUS = 20
GLASS_SHADOW = "#333333"  # simulated #00000040

BTN_BG = "#EEF1FA"        # simulated semi-transparent white (#FFFFFF25)
BTN_BORDER = "#D0D5E6"    # simulated #FFFFFF50
BTN_FG = "#FFFFFF"
BTN_TEXT_NORMAL = "#FFFFFF"
BTN_TEXT_FUNC = "#00FFD1"  # neon cyan for functions
BTN_HOVER_BG = "#FFFFFF"   # simulated lighten to #FFFFFF40
BTN_NEON_GLOW = "#00FFD1"

FUNC_BG = BTN_BG  # keep frosted look; use text color to distinguish
EQUALS_BG = "#FF6B6B"     # modern coral red
ACCENT_BG = "#FFB347"     # amber/orange accent (clear/backspace)

DISPLAY_BG = "#222222"    # simulated semi-transparent black (#00000050)
DISPLAY_BORDER = "#AEB2C8"  # subtle border (#FFFFFF20 approx)
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
        fg_color: str = BTN_TEXT_NORMAL,
        hover_lighten: float = 0.12,
        font=("SFMono", 14, "bold"),
        border_color: str = BTN_BORDER,
        show_neon_glow: bool = True,
        glow_color: str = BTN_NEON_GLOW,
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
        self.border_color = border_color
        self.show_neon_glow = show_neon_glow
        self.glow_color = glow_color
        self.is_pressed = False
        self._draw()
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Key-Return>", self._on_click)
        self.bind("<Key-space>", self._on_click)
        self.focusable = True

    def _draw(self):
        self.delete("all")
        w = int(self["width"]) if isinstance(self["width"], str) else self["width"]
        h = int(self["height"]) if isinstance(self["height"], str) else self["height"]
        r = min(self.radius, w // 2, h // 2)
        x1, y1, x2, y2 = 2, 2, w - 2, h - 2
        # Shadow/glow layer
        if self.show_neon_glow and self.is_pressed:
            shadow_parts = [
                self.create_rectangle(x1 + r - 1, y1 - 1, x2 - r + 1, y2 + 1, outline=self.glow_color, fill=""),
                self.create_rectangle(x1 - 1, y1 + r - 1, x2 + 1, y2 - r + 1, outline=self.glow_color, fill=""),
            ]
            for sp in shadow_parts:
                self.itemconfig(sp, width=2)

        # Rounded rectangle using rectangles and arcs
        self.shape_parts = [
            self.create_rectangle(x1 + r, y1, x2 - r, y2, outline=self.base_bg, fill=self.base_bg),
            self.create_rectangle(x1, y1 + r, x2, y2 - r, outline=self.base_bg, fill=self.base_bg),
            self.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, outline=self.base_bg, fill=self.base_bg),
            self.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, outline=self.base_bg, fill=self.base_bg),
            self.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, outline=self.base_bg, fill=self.base_bg),
            self.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, outline=self.base_bg, fill=self.base_bg),
        ]
        # Border
        self.border_parts = [
            self.create_rectangle(x1 + r, y1, x2 - r, y2, outline=self.border_color, fill=""),
            self.create_rectangle(x1, y1 + r, x2, y2 - r, outline=self.border_color, fill=""),
            self.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, outline=self.border_color, fill=""),
            self.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, outline=self.border_color, fill=""),
            self.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, outline=self.border_color, fill=""),
            self.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, outline=self.border_color, fill=""),
        ]
        for item in self.border_parts:
            self.itemconfig(item, width=1)

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
        self.is_pressed = True
        self._draw()

    def _on_release(self, _):
        self.is_pressed = False
        self._draw()


class GlassPanel(tk.Canvas):
    def __init__(self, master, radius: int = GLASS_RADIUS, pad: int = 14, **kwargs):
        super().__init__(master, highlightthickness=0, bd=0, bg=MAIN_BG, **kwargs)
        self.radius = radius
        self.pad = pad
        self.bind("<Configure>", self._redraw)
        # inner content frame
        self.content = tk.Frame(self, bg=MAIN_BG)
        self.content_window = self.create_window(self.pad, self.pad, anchor="nw", window=self.content)

    def _redraw(self, _):
        self.delete("panel")
        w = self.winfo_width()
        h = self.winfo_height()
        r = min(self.radius, w // 12, h // 12)

        x1, y1, x2, y2 = 8, 8, w - 8, h - 8

        # Shadow (offset)
        self._rounded_rect(x1 + 4, y1 + 6, x2 + 4, y2 + 6, r, fill=GLASS_SHADOW, outline="", tags="panel")
        # Panel fill
        self._rounded_rect(x1, y1, x2, y2, r, fill=GLASS_BG, outline=GLASS_BORDER, width=2, tags="panel")

        # Reposition content window inside with padding
        self.coords(self.content_window, x1 + self.pad, y1 + self.pad)
        self.itemconfig(self.content_window, width=max(0, x2 - x1 - 2 * self.pad), height=max(0, y2 - y1 - 2 * self.pad))

    def _rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        parts = []
        parts.append(self.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs))
        parts.append(self.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs))
        parts.append(self.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, **kwargs))
        parts.append(self.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, **kwargs))
        parts.append(self.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, **kwargs))
        parts.append(self.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, **kwargs))
        return parts


def _hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def _rgb_to_hex(rgb):
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def draw_vertical_gradient(canvas: tk.Canvas, top_color: str, bottom_color: str):
    canvas.delete("gradient")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width <= 0 or height <= 0:
        return
    r1, g1, b1 = _hex_to_rgb(top_color)
    r2, g2, b2 = _hex_to_rgb(bottom_color)
    steps = max(2, height)
    for i in range(steps):
        t = i / (steps - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        color = _rgb_to_hex((r, g, b))
        canvas.create_line(0, i, width, i, fill=color, tags="gradient")


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.configure(bg=MAIN_BG)
        self.geometry("640x760")

        # Modes
        self.is_scientific = True
        self.angle_mode = tk.StringVar(value="DEG")  # or "RAD"

        # Memory
        self.memory_value = 0.0

        # Expression state
        self.expression = tk.StringVar(value="")

        # Background gradient
        self.background_canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.background_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.bind("<Configure>", lambda e: draw_vertical_gradient(self.background_canvas, GRADIENT_TOP, GRADIENT_BOTTOM))

        # Glass panel container
        self.panel = GlassPanel(self)
        self.panel.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)

        # Build UI into glass panel content
        self._build_menu()
        self._build_display(parent=self.panel.content)
        self._build_toggles(parent=self.panel.content)
        self._build_keypads(parent=self.panel.content)
        self._configure_grid(container=self.panel.content)
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

    def _build_display(self, parent=None):
        parent = parent or self
        display_frame = tk.Frame(parent, bg=MAIN_BG)
        display_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=(8, 6))

        # Display styled to look like rounded frosted panel
        self.display = tk.Entry(
            display_frame,
            textvariable=self.expression,
            font=("SFMono", 28, "bold"),
            bg=DISPLAY_BG,
            fg=DISPLAY_FG,
            insertbackground=DISPLAY_FG,
            relief="flat",
            borderwidth=2,
            highlightthickness=2,
            highlightbackground=DISPLAY_BORDER,
            highlightcolor=DISPLAY_BORDER,
            justify="right",
        )
        self.display.pack(fill="both", expand=True)

    def _build_toggles(self, parent=None):
        parent = parent or self
        toggle_frame = tk.Frame(parent, bg=MAIN_BG)
        toggle_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 6))

        self.mode_btn = RoundedButton(
            toggle_frame,
            text="Scientific" if self.is_scientific else "Standard",
            command=self._toggle_mode,
            width=130,
            height=38,
            radius=10,
            bg_color=BTN_BG,
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
            bg_color=BTN_BG,
            font=("SFMono", 12, "bold"),
        )
        self.deg_btn.pack(side="right")

    def _build_keypads(self, parent=None):
        parent = parent or self
        self.main_frame = tk.Frame(parent, bg=MAIN_BG)
        self.main_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

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
        bg = BTN_BG
        fg = BTN_TEXT_NORMAL
        border = BTN_BORDER
        glow = BTN_NEON_GLOW
        if kind == "func":
            fg = BTN_TEXT_FUNC
        elif kind == "equals":
            bg = EQUALS_BG
            fg = "#FFFFFF"
            border = lighten_color(EQUALS_BG, 0.25)
            glow = "#FFFFFF"
        elif kind == "accent":
            bg = ACCENT_BG
            fg = "#2D1B00"
            border = lighten_color(ACCENT_BG, 0.25)
            glow = BTN_NEON_GLOW
        return RoundedButton(parent, text=text, command=cmd, bg_color=bg, fg_color=fg, border_color=border, glow_color=glow)

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

    def _configure_grid(self, container=None):
        container = container or self
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=0)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(0, weight=1)

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

    def _clear(self):
        self.expression.set("")

    def _backspace(self):
        self.expression.set(self.expression.get()[:-1])

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

    def _handle_keypress(self, event):
        char = event.char
        if event.keysym in ("Return", "KP_Enter"):
            self._evaluate()
        elif event.keysym == "BackSpace":
            self._backspace()
        elif event.keysym == "Escape":
            self._clear()
        elif char in "0123456789.+-*/()^":
            mapping = {'*': ' × ', '/': ' ÷ ', '^': ' ^ '}
            self._append(mapping.get(char, char))

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
        except Exception:
            self.expression.set("Math Error")

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


