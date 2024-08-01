import tkinter as tk
from tkinter import scrolledtext

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Action Interface")

        self.create_main_interface()

    def create_main_interface(self):
        # Frame for action buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=10)

        # Creating buttons in a single row
        self.create_action_button("Search", self.open_action1_interface, button_frame)
        self.create_action_button("Update", self.open_action2_interface, button_frame)
        self.create_action_button("Action 3", self.open_action3_interface, button_frame)
        self.create_action_button("Action 4", self.open_action4_interface, button_frame)

        # Frame for chat interface
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Chat interface components
        self.chat_window = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, height=15)
        self.chat_window.pack(expand=True, fill="both", pady=10)

        self.entry = tk.Entry(self.chat_frame)
        self.entry.pack(fill="x", pady=10)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack()

    def create_action_button(self, title, command, parent_frame):
        button = tk.Button(parent_frame, text=title, command=command, width=20)
        button.pack(side="left", padx=10)

    def open_action1_interface(self):
        self.current_action = "Search"
        self.chat_window.insert(tk.END, "\n--- Search Interface Opened ---\n")

    def open_action2_interface(self):
        self.current_action = "Update"
        self.chat_window.insert(tk.END, "\n--- Update Interface Opened ---\n")

    def open_action3_interface(self):
        self.current_action = "Action 3"
        self.chat_window.insert(tk.END, "\n--- Action 3 Interface Opened ---\n")

    def open_action4_interface(self):
        self.current_action = "Action 4"
        self.chat_window.insert(tk.END, "\n--- Action 4 Interface Opened ---\n")

    def send_message(self, event=None):
        message = self.entry.get()
        self.chat_window.insert(tk.END, f"You: {message}\n")
        self.entry.delete(0, tk.END)

        # Execute action based on current action
        if hasattr(self, 'current_action'):
            if self.current_action == "Search":
                self.execute_action1(message)
            elif self.current_action == "Update":
                self.execute_action2(message)
            elif self.current_action == "Action 3":
                self.execute_action3(message)
            elif self.current_action == "Action 4":
                self.execute_action4(message)

    def execute_action1(self, message):
        result = f"Search executed: {message}"
        self.chat_window.insert(tk.END, f"Chatbot: {result}\n")

    def execute_action2(self, message):
        result = f"Update executed: {message}"
        self.chat_window.insert(tk.END, f"Chatbot: {result}\n")

    def execute_action3(self, message):
        result = f"Action 3 executed: {message}"
        self.chat_window.insert(tk.END, f"Chatbot: {result}\n")

    def execute_action4(self, message):
        result = f"Action 4 executed: {message}"
        self.chat_window.insert(tk.END, f"Chatbot: {result}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
