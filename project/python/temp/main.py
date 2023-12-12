import os
import customtkinter as ctk # pip install customtkinter
# pip3 install packaging

root = ctk.CTk()
root.geometry("750x550")
root.title("xeylou's mqtt explorer")

ctk.set_appearance_mode("dark")

title_label = ctk.CTkLabel(root, text="xeylou's mqtt explorer",
                            font=ctk.CTkFont(size=30, weight="bold"))
title_label.pack(padx=10, pady=(40,20))

frame = ctk.CTkFrame(root)
frame.pack(fill="x", padx=100)

server_info_frame = ctk.CTkFrame(frame)
server_info_frame.pack(padx=100, pady=(20, 5), fill="both")
server_info_label = ctk.CTkLabel(
    server_info_frame, text="Server Info", font=ctk.CTkFont(weight="bold"))
server_info_label.pack()
server_dropdown = ctk.CTkComboBox(server_info_frame, values=["1", "2", "3"])
server_dropdown.pack(pady=10)

test_frame = ctk.CTkFrame(frame)
test_frame.pack(padx=100, pady=5, fill="both")
server_info_label = ctk.CTkLabel(
    test_frame, text="Test Frame", font=ctk.CTkFont(weight="bold"))

root.mainloop()
