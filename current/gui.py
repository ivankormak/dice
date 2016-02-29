from Tkinter import *

class App:
    def __init__(self):
      self.root = Tk()
      self.conf = {}
      Button(self.root, text = "Run", command = self.execute).pack(["top", "nw"])


      self.root.mainloop()

    def execute(self):
      quit()

r = App()
