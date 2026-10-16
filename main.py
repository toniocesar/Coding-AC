import tkinter as tk
from tkinter import messagebox


def longest_common_substring(strings):
    strings = list(strings)
    if not strings:
        return ""

    base = min(strings, key=len)
    common = list(range(1, len(base) + 1))

    for text in strings:
        if text == base:
            continue

        best = [0] * len(base)
        dp = [0] * (len(base) + 1)

        for char in text:
            for i in range(len(base), 0, -1):
                dp[i] = dp[i - 1] + 1 if base[i - 1] == char else 0
                best[i - 1] = max(best[i - 1], dp[i])

        common = [min(a, b) for a, b in zip(common, best)]

    length = max(common, default=0)
    if length == 0:
        return ""

    end = common.index(length) + 1
    return base[end - length:end]


class LongestCommonSubstringApp:
    """Tkinter GUI that lets the user add any number of text fields,
    then computes the longest common substring shared by all of them."""

    def __init__(self, root):
        self.root = root
        self.root.title("Longest Common Substring")
        self.root.geometry("640x520")

        self.field_frames = []  # keeps track of each (row_frame, text_widget)

        self._build_layout()
        # Start with two fields so there is something to compare right away.
        self.add_field()
        self.add_field()

    def _build_layout(self):
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        top_bar = tk.Frame(container)
        top_bar.pack(fill="x")
        tk.Label(top_bar, text="Strings to compare:", font=("TkDefaultFont", 11, "bold")).pack(side="left")
        tk.Button(top_bar, text="+ Add field", command=self.add_field).pack(side="right")

        # Scrollable area for the dynamic list of text fields.
        canvas_frame = tk.Frame(container)
        canvas_frame.pack(fill="both", expand=True, pady=(8, 8))

        self.canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.fields_container = tk.Frame(self.canvas)
        self.fields_window = self.canvas.create_window((0, 0), window=self.fields_container, anchor="nw")

        self.fields_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.fields_window, width=e.width),
        )

        run_bar = tk.Frame(container)
        run_bar.pack(fill="x")
        tk.Button(run_bar, text="Run", command=self.run_algorithm, bg="#4CAF50", fg="white").pack(side="left")
        tk.Button(run_bar, text="Clear result", command=self.clear_result).pack(side="left", padx=(8, 0))

        tk.Label(container, text="Result:", font=("TkDefaultFont", 11, "bold")).pack(anchor="w", pady=(8, 0))
        self.result_text = tk.Text(container, height=4, wrap="word")
        self.result_text.pack(fill="x")
        self.result_text.configure(state="disabled")

    def add_field(self):
        row = tk.Frame(self.fields_container)
        row.pack(fill="x", expand=True, pady=4)

        index_label = tk.Label(row, text=f"{len(self.field_frames) + 1}.", width=3, anchor="n")
        index_label.pack(side="left")

        text_widget = tk.Text(row, height=4, wrap="word")
        text_widget.pack(side="left", fill="x", expand=True)

        remove_button = tk.Button(row, text="Remove", command=lambda: self.remove_field(row))
        remove_button.pack(side="left", padx=(6, 0))

        self.field_frames.append((row, text_widget))
        self._renumber_fields()

    def remove_field(self, row):
        self.field_frames = [(r, t) for (r, t) in self.field_frames if r is not row]
        row.destroy()
        self._renumber_fields()

    def _renumber_fields(self):
        for i, (row, _) in enumerate(self.field_frames, start=1):
            row.winfo_children()[0].configure(text=f"{i}.")

    def clear_result(self):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.configure(state="disabled")

    def run_algorithm(self):
        strings = [t.get("1.0", "end-1c") for _, t in self.field_frames]
        strings = [s for s in strings if s.strip() != ""]

        if len(strings) < 2:
            messagebox.showwarning(
                "Not enough input",
                "Please fill in at least two text fields before running.",
            )
            return

        result = longest_common_substring(strings)

        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        if result:
            self.result_text.insert("1.0", result)
        else:
            self.result_text.insert("1.0", "(no common substring found)")
        self.result_text.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = LongestCommonSubstringApp(root)
    root.mainloop()