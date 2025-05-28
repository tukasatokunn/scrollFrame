#scrollable_frame.py
import customtkinter as ctk
import tkinter as tk

class ScrollableFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        scroll_vertical=True,
        show_scrollbar=False,
        bg_color=None,
        scrollbar_color=None,
        **kwargs
    ):
        super().__init__(master, **kwargs)

        # grid全体の行・列設定（可変サイズ対応）
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        canvas_bg = bg_color if bg_color is not None else None
        self.canvas = tk.Canvas(self, bg=canvas_bg, borderwidth=0, highlightthickness=0)

        frame_bg = bg_color if bg_color is not None else None
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=frame_bg)

        scrollbar_bg = scrollbar_color if scrollbar_color is not None else "transparent"
        scrollbar_fg = scrollbar_color if scrollbar_color is not None else "transparent"

        self.scroll_vertical = scroll_vertical
        self.show_scrollbar = show_scrollbar
        self._pending_update = None
        self._last_size = (0, 0)

        if self.show_scrollbar:
            if self.scroll_vertical:
                self.v_scrollbar = ctk.CTkScrollbar(
                    self,
                    orientation="vertical",
                    command=self.canvas.yview,
                    bg_color=scrollbar_bg,
                    fg_color=scrollbar_fg
                )
                self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
                self.v_scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                self.h_scrollbar = ctk.CTkScrollbar(
                    self,
                    orientation="horizontal",
                    command=self.canvas.xview,
                    bg_color=scrollbar_bg,
                    fg_color=scrollbar_fg
                )
                self.canvas.configure(xscrollcommand=self.h_scrollbar.set)
                self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_frame_configure(self, event):
        current_size = (event.width, event.height)
        if current_size == self._last_size:
            return
        self._last_size = current_size

        if self._pending_update is not None:
            self.after_cancel(self._pending_update)
        self._pending_update = self.after(10, self._delayed_update)

    def _delayed_update(self):
        self._pending_update = None

        bbox = self.canvas.bbox("all")
        if bbox is not None:
            self.canvas.configure(scrollregion=bbox)
        else:
            self.canvas.configure(scrollregion=(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height()))

        max_width = self.winfo_width()
        max_height = self.winfo_height()

        if self.scroll_vertical:
            # 縦スクロール時は幅を最大幅に、高さはscrollable_frameの必要高さに
            self.canvas.itemconfig(self.window_id, width=max_width, height=self.scrollable_frame.winfo_reqheight())
        else:
            # 横スクロール時は高さを最大高さに、幅はscrollable_frameの必要幅に
            self.canvas.itemconfig(self.window_id, width=self.scrollable_frame.winfo_reqwidth(), height=max_height)

    def _on_mousewheel(self, event):
        if self.scroll_vertical:
            if event.num == 5 or event.delta == -120:
                self.canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta == 120:
                self.canvas.yview_scroll(-1, "units")
        else:
            if event.num == 5 or event.delta == -120:
                self.canvas.xview_scroll(1, "units")
            elif event.num == 4 or event.delta == 120:
                self.canvas.xview_scroll(-1, "units")


    def set_scroll_direction(self, vertical: bool):
        """スクロール方向を縦（True）/横（False）に切り替える"""
        if self.scroll_vertical == vertical:
            return  # 変更なしなら何もしない

        self.scroll_vertical = vertical

        # スクロールバーの再設定
        # 既存のスクロールバーを破棄
        if hasattr(self, 'v_scrollbar'):
            self.v_scrollbar.grid_forget()
            del self.v_scrollbar
        if hasattr(self, 'h_scrollbar'):
            self.h_scrollbar.grid_forget()
            del self.h_scrollbar

        if self.show_scrollbar:
            scrollbar_bg = "transparent"  # 必要に応じて元の色を保持できるよう改良も
            scrollbar_fg = "transparent"

            if self.scroll_vertical:
                self.v_scrollbar = ctk.CTkScrollbar(
                    self,
                    orientation="vertical",
                    command=self.canvas.yview,
                    bg_color=scrollbar_bg,
                    fg_color=scrollbar_fg
                )
                self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand="")
                self.v_scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                self.h_scrollbar = ctk.CTkScrollbar(
                    self,
                    orientation="horizontal",
                    command=self.canvas.xview,
                    bg_color=scrollbar_bg,
                    fg_color=scrollbar_fg
                )
                self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand="")
                self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        # canvasのスクロール方向に合わせてウィンドウ幅/高さを調整
        self._delayed_update()