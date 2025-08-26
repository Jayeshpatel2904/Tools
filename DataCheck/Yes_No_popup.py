import tkinter as tk
from tkinter.simpledialog import Dialog

class MyDialog(Dialog):
    # override body() to build your input form
    def body(self, master):
        tk.Label(master, text="Enter sentences:", anchor="w").pack(fill="x")
        self.text = tk.Text(master, width=40, height=10)
        self.text.pack()
        # need to return the widget to have first focus
        return self.text

    # override buttonbox() to create your action buttons
    def buttonbox(self):
        box = tk.Frame(self)
        # note that self.ok() and self.cancel() are defined inside `Dialog` class
        tk.Button(box, text="Yes", width=10, command=self.ok, default=tk.ACTIVE)\
            .pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(box, text="No", width=10, command=self.cancel)\
            .pack(side=tk.LEFT, padx=5, pady=5)
        box.pack()

    # override apply() to return data you want
    def apply(self):
        self.result = self.text.get("1.0", "end-1c")

root = tk.Tk()
root.withdraw()
dlg = MyDialog(root, title="Test")
print(dlg.result)
root.destroy()