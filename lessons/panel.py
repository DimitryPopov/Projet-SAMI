import tkinter as tk
import socket
class TCPClient():
    def __init__(self):
        self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
    def connect(self, host, port):
        self.sock.connect((host, port))
    def send(self, msg):
        self.sock.send(msg.encode())

    def receive(self):
        msg_recu = self.sock.recv(1024)
        print(msg_recu.decode())
        return msg_recu
    def close(self):
        self.sock.close()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.client = TCPClient()

    def create_widgets(self):
        rowConnect = tk.Frame(self)
        self.connect = tk.Button(rowConnect)
        self.connect["text"] = "Connect"
        self.connect["command"] = self.connect_robot

        self.robot = tk.Entry(rowConnect)
        rowConnect.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.connect.pack(side="left")
        self.robot.pack(side="left",expand=tk.YES, fill=tk.X)

        # Make motors
        rowA = tk.Frame(self)
        lab_motorA = tk.Label(rowA,text="Motor A speed",anchor='w')
        self.speed_motorA = tk.Entry(rowA)
        rowA.pack(side=tk.TOP,fill=tk.X, padx=5, pady=5)
        lab_motorA.pack(side=tk.LEFT)
        self.speed_motorA.pack(side=tk.RIGHT,expand=tk.YES, fill=tk.X)

        rowB = tk.Frame(self)
        lab_motorB = tk.Label(rowB,text="Motor B speed",anchor='w')
        self.speed_motorB = tk.Entry(rowB)
        rowB.pack(side=tk.TOP,fill=tk.X, padx=5, pady=5)
        lab_motorB.pack(side=tk.LEFT)
        self.speed_motorB.pack(side=tk.RIGHT,expand=tk.YES, fill=tk.X)
        #Make move and stop buttons
        self.move = tk.Button(self.master, text="MOVE", fg="green")
        self.move["command"] = self.move_robot
        self.move.pack(side="left")

        self.stop = tk.Button(self.master, text="STOP", fg="red")
        self.stop["command"] = self.stop_robot
        self.stop.pack(side="left")

        self.quit = tk.Button(self.master, text="QUIT",
                              command=self.quit_app)
        self.quit.pack(side="left")
    def connect_robot(self):
        robot_addr = self.robot.get()
        print(robot_addr)
        self.client.connect(robot_addr,9999)
    def move_robot(self):
        speedA = self.speed_motorA.get()
        speedB = self.speed_motorB.get()
        msg = "MOVE "+speedA+" "+speedB
        self.client.send(msg)
    def stop_robot(self):
        msg= 'STOP'
        self.client.send(msg)
    def quit_app(self):
        self.client.fermer()
        self.master.destroy()

# Entry point
root = tk.Tk()
app = Application(master=root)
app.mainloop()