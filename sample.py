import customtkinter as ctk
from scrollable_frame import ScrollableFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x400")
app.title("ScrollableFrame サンプル")

# スクロールフレームを作成（縦スクロール有効・スクロールバー表示）
scrollable = ScrollableFrame(app, scroll_vertical=True, show_scrollbar=True)
scrollable.pack(fill="both", expand=True, padx=10, pady=10)

# 中にウィジェットを配置（例：ボタンをたくさん）
for i in range(30):
    btn = ctk.CTkButton(scrollable.scrollable_frame, text=f"ボタン {i+1}")
    btn.pack(pady=5, padx=10, anchor="w")

app.mainloop()
