#!/usr/bin/python3
import tkinter, tkinter.messagebox, customtkinter, random, os, sys, psutil, logging, random, time
from paho.mqtt import client as mqtt_client
from mosquitto import *

# TODO 1. creating the subscribe function & testing it
# TODO 2. creating the publish function & testing it
# TODO 3. implementing those to the textbox for the subscribing function & to the text entry + publish button for the publish function
# TODO 4. making the helpage window & making the restart + quit buttons working

"""
inspiration:
https://www.youtube.com/watch?v=aRJXC8hJvrc
https://www.youtube.com/watch?v=XcrEumS9T9M

documentation:
https://github.com/TomSchimansky/CustomTkinter/wiki
https://customtkinter.tomschimansky.com/documentation/
https://www.simplilearn.com/tutorials/python-tutorial/global-variable-in-python
"""

# appearance global variables
customtkinter.set_appearance_mode("System")  # modes: "System", "Dark" or "Light"
customtkinter.set_default_color_theme("dark-blue")  # themes: "blue", "green" or "dark-blue"

# mqtt default global variables
broker_default_port = "1883"
random_client_id = f'python-mqtt-{random.randint(0, 100)}'

# helping page window
class helpWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Helping Page")
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Settings tab\n\npresents the simple way to subscribe\nto a Topic on an according Broker\n\nAdvanced tab\n\nto add more infos to connect to a broker\nif it has a different access port than 1883 or\nif you need a custom/recognizable ID\n\nPublish button\n\nsend the message in the Type a message\nentry box")
        self.label.pack(padx=20, pady=20)

class App(customtkinter.CTk):
    def __init__(self):
        self.help_window = None

        super().__init__()

        # window configuration
        self.title("xeylou's mqtt explorer")
        self.geometry(f"{750}x{425}")
        self.resizable(False,False)

        # grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # sidebar frame & widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.sidebar_clear_button = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event_help, text="Help")
        self.sidebar_clear_button.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.sidebar_help_button = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event_clear, text="Clear")
        self.sidebar_help_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.sidebar_restart_button = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event_restart, text="Restart")
        self.sidebar_restart_button.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.sidebar_quit_button = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event_quit, text="Quit")
        self.sidebar_quit_button.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                    command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                    command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20), sticky="nsew")

        # message entry & publish button
        self.message = customtkinter.CTkEntry(self, placeholder_text="Type a message")
        self.message.grid(row=1, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.publish_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
                                                    text="Publish", command=self.publish_button)
        self.publish_button.grid(row=1, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Settings")
        self.tabview.add("Advanced")
        self.tabview.tab("Settings").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Advanced").grid_columnconfigure(0, weight=1)

        # settings tab
        self.label_settings_tab = customtkinter.CTkLabel(self.tabview.tab("Settings"), text="Connection Settings")
        self.label_settings_tab.grid(row=0, column=0, padx=20, pady=20)
        self.broker_address_combobox = customtkinter.CTkComboBox(self.tabview.tab("Settings"),
                                                    values=["test.mosquito.org"])
        self.broker_address_combobox.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.topic_combobox = customtkinter.CTkComboBox(self.tabview.tab("Settings"),
                                                    values=["/adehutest"])
        self.topic_combobox.grid(row=2, column=0, padx=20, pady=(0, 10))
        self.subscribe_button = customtkinter.CTkButton(self.tabview.tab("Settings"), text="Subscribe",
                                                    command=self.confirmation_dialog_event)
        self.subscribe_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        # advanced tab
        self.label_advanced_tab = customtkinter.CTkLabel(self.tabview.tab("Advanced"), text="Advanced Connection Settings")
        self.label_advanced_tab.grid(row=0, column=0, padx=20, pady=20)
        self.broker_address_advanced_combobox = customtkinter.CTkComboBox(self.tabview.tab("Advanced"),
                                                    values=["test.mosquito.org"])
        self.broker_address_advanced_combobox.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.broker_port = customtkinter.CTkComboBox(self.tabview.tab("Advanced"),
                                                    values=["1883"])
        self.broker_port.grid(row=2, column=0, padx=20, pady=(0, 10))
        self.topic_advanced_combobox = customtkinter.CTkComboBox(self.tabview.tab("Advanced"),
                                                    values=["adehutest"])
        self.topic_advanced_combobox.grid(row=3, column=0, padx=20, pady=(0, 10))
        self.id_advanced_combobox = customtkinter.CTkComboBox(self.tabview.tab("Advanced"),
                                                    values=["30000"])
        self.id_advanced_combobox.grid(row=4, column=0, padx=20, pady=(0, 10))
        self.advanced_subscribe_button = customtkinter.CTkButton(self.tabview.tab("Advanced"), text="Subscribe",
                                                    command=self.advanced_confirmation_dialog_event)
        self.advanced_subscribe_button.grid(row=5, column=0, padx=20, pady=(10, 10))

        # set default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.broker_address_combobox.set("Broker Address")
        self.topic_combobox.set("Topic")
        self.broker_address_advanced_combobox.set("Broker Address")
        self.broker_port.set("Broker Port")
        self.topic_advanced_combobox.set("Topic")
        self.id_advanced_combobox.set("Custom ID")
        self.textbox.insert("0.0", "Welcome!\n\n" + "May you want to change the broker\nconnection settings before publishing\n\nYou can refer to the Help page for\nmore info\n\n\n")

    # callback events
    def sidebar_button_event_clear(self):
        self.textbox.delete("0.0", "end")

    def sidebar_button_event_help(self):
        if self.help_window is None or not self.help_window.winfo_exists():
            self.help_window = helpWindow(self)  # create window if its None or destroyed
        else:
            self.help_window.focus()  # if window exists focus it

    def sidebar_button_event_restart(self):
        self.destroy()
        app = App()
        app.mainloop()

    def sidebar_button_event_quit(self):
        print(f"[DEBUG] Quitting")
        self.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def confirmation_dialog_event(self):
        to_broker = self.broker_address_combobox.get()
        to_topic = self.topic_combobox.get()
        to_port = broker_default_port
        with_id = random_client_id
        advertissement_message = f'Do you want to use this infos? (Y\\n)\n{to_broker}:{to_port} on topic {to_topic}\nwith ID {with_id}'
        dialog = customtkinter.CTkInputDialog(text=advertissement_message, title="Confirm Subscription")
        confirmation_message = dialog.get_input()
        confirmation_message_lowered = confirmation_message.lower()
        if confirmation_message_lowered in ["y", "yes", ""]:
            print(f"[DEBUG] Condition to Confirm Subscription for confirmation_dialog_event is matched")
            self.subscribe_to_mqtt(to_broker, to_port, to_topic, with_id)
        else:
            print(f"[DEBUG] Condition to Confirm Subscription for confirmation_dialog_event is unmatched")

    def advanced_confirmation_dialog_event(self):
        to_broker = self.broker_address_advanced_combobox.get()
        to_topic = self.topic_advanced_combobox.get()
        to_port = self.broker_port.get()
        with_id = self.id_advanced_combobox.get()
        advertissement_message = f'Do you want to use this infos? (Y\\n)\n{to_broker}:{to_port} on topic {to_topic}\nwith ID {with_id}'
        dialog = customtkinter.CTkInputDialog(text=advertissement_message, title="Confirm Subscription")
        confirmation_message = dialog.get_input()
        confirmation_message_lowered = confirmation_message.lower()
        match confirmation_message_lowered:
            case "y":
                print(f"yes")
            case "yes":
                print(f"yes")
            case "":
                print(f"yes")
            case _:
                print(f"[DEBUG] Condition to Confirm Subscription for advanced_confirmation_dialog_event is unmatched")


    def publish_button(self):
        to_send  = self.message.get()  # catching message to send
        print(f"[DEBUG] Publishing message : {to_send}")


if __name__ == "__main__":
    print(f"[DEBUG] Creating App Agent")
    app = App()
    print(f"[DEBUG] Initializing Window")
    app.mainloop()
