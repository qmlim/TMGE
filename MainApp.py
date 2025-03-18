import tkinter as tk
import tkinter.messagebox as messagebox
import Player
from Tetris.TetrisGame import TetrisGame
from CandyCrush.CandyCrushGame import CandyCrushGame


root = tk.Tk()
root.title("TGME")
# root.geometry("700x700")
root.resizable(False, False)

container = tk.Frame(root)
container.pack(fill="both", expand=True)

mainMenuFrame = tk.Frame(container)
signUpFrame= tk.Frame(container)
gameSelectFrame = tk.Frame(container)
playerSelectFrame = tk.Frame(container)
playerProfileFrame = tk.Frame(container)
frames = [mainMenuFrame, signUpFrame, gameSelectFrame, playerSelectFrame, playerProfileFrame]

for frame in frames:
    frame.grid(row=0, column=0, sticky="nsew")

players = []


def main():
    tk.Label(
        mainMenuFrame, 
        text="Welcome to the Tile Game Matching Environment!", 
        font=("Font", 27),
        anchor="center").pack(pady=10, padx=20)
    tk.Label(
        mainMenuFrame, 
        text="Please sign up before selecting a game.", 
        font=("Font", 15)).pack(pady=(30, 0), padx=5, fill="x")
    tk.Button(
        mainMenuFrame,
        text="Sign Up",
        command=lambda: showFrame(signUpFrame),
        width=15).pack(pady=(20, 5))
    tk.Button(
        mainMenuFrame,
        text="View Player Profile",
        command=lambda: [playerSelect(), showFrame(playerSelectFrame)],
        width=15).pack(pady=5)
    tk.Button(
        mainMenuFrame,
        text="Select Game",
        command=lambda: showFrame(gameSelectFrame),
        width=15).pack(pady=5)


def signUp():
    tk.Label(
        signUpFrame, 
        text="Sign Up", 
        font=("Font", 30)).pack(ipady=10, ipadx=5, fill="x")
    tk.Label(
        signUpFrame,
        text="Username",
        font=("Font", 15)).pack(pady=(20, 0))

    usernameEntry = tk.Entry(signUpFrame)
    usernameEntry.pack(pady=3)

    tk.Button(
        signUpFrame,
        text="Submit",
        command=lambda: createPlayerAccount(usernameEntry),
        width=12).pack(pady=10)
    tk.Button(
        signUpFrame,
        text="Back",
        command=lambda: showFrame(mainMenuFrame),
        width=12).pack(pady=30)


def gameSelect():
    tk.Label(
        gameSelectFrame, 
        text="Game Select", 
        font=("Font", 30)).pack(ipady=10, ipadx=5, fill="x")
    tk.Label(
        gameSelectFrame,
        text="Select the game to play",
        font=("Font", 15)).pack(pady=(20, 0))
    tk.Button(
        gameSelectFrame,
        text="Tetris",
        command=startTetrisGame,
        width=12).pack(pady=(10, 5))

    tk.Button(
        gameSelectFrame,
        text="CandyCrush",
        command=lambda: startCandyGame(),
        width=12).pack(pady=5)

    tk.Button(
        gameSelectFrame,
        text="Back",
        command=lambda: showFrame(mainMenuFrame),
        width=12).pack(pady=30)

def startTetrisGame():
    global tetrisGame
    tetrisGame = TetrisGame(players, container)
    tetrisGame.bind_keys(root)
    showFrame(tetrisGame.gameSetUp())
    # tetrisGame.gamePlay()

def startCandyGame():
    pass

def playerSelect():
    for widget in playerSelectFrame.winfo_children():
        widget.destroy()

    tk.Label(
        playerSelectFrame, 
        text="View Player Profile", 
        font=("Font", 30)).pack(ipady=10, ipadx=5, fill="x")
    tk.Label(
        playerSelectFrame,
        text="Select a player profile to view",
        font=("Font", 15)).pack(pady=(20, 10))

    for player in players:
        tk.Button(
            playerSelectFrame,
            text=player.getUsername(),
            command=lambda p=player: [p.displayPlayerProfile(showFrame, playerSelectFrame, playerProfileFrame), showFrame(playerProfileFrame)],
            width=12).pack(pady=5)
        
    tk.Button(
        playerSelectFrame,
        text="Back",
        command=lambda: showFrame(mainMenuFrame),
        width=12).pack(pady=30)


def createPlayerAccount(usernameEntry):
    username = usernameEntry.get().strip()

    if not username:
        messagebox.showerror("ERROR", "Username cannot be empty.")
    
    elif len(username) > 12:
        messagebox.showerror("ERROR", "Username must be less than 12 characters.")

    elif findPlayer(username):
        messagebox.showerror("ERROR", "Username taken. Please enter a unique username.")
        return
    
    else: 
        newPlayer = Player.Player(username, 0)
        players.append(newPlayer)
        messagebox.showinfo("SUCCESS", f"{username} account created")
        usernameEntry.delete(0, tk.END)
        showFrame(mainMenuFrame)


def findPlayer(username):
    for player in players:
        if player.getUsername() == username:
            return player
    return False


def showFrame(frame):
    if frame:
        frame.tkraise()
    else:
        messagebox.showerror("ERROR", "Received None instead of a frame.")



if __name__ == "__main__":
    main()
    signUp()
    gameSelect()
    playerSelect()
    showFrame(mainMenuFrame)
    root.mainloop()