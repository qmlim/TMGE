import tkinter as tk

class Player:
    def __init__(self, username, wins):
        self.username = username
        self.wins = wins

    def displayPlayerProfile(self, showFrame, playerSelectFrame, playerProfileFrame):        
        for widget in playerProfileFrame.winfo_children():
            widget.destroy()
        
        tk.Label(
            playerProfileFrame,
            text="Player Profile",
            font=("Font", 30)).pack(pady=5)
        tk.Label(
            playerProfileFrame,
            text=f"Username: {self.username}",
            font=("Font", 15),
            anchor="w",
            justify="left").pack(pady=5, padx=10, fill="x")
        tk.Label(
            playerProfileFrame,
            text=f"Wins: {self.wins}",
            font=("Font", 15),
            anchor="w",
            justify="left").pack(pady=5, padx=10, fill="x")
        tk.Button(
            playerProfileFrame,
            text="Back",
            command=lambda: showFrame(playerSelectFrame),
            width=12).pack(pady=30)

    def getUsername(self):
        return self.username