import tkinter as tk
import tkinter.messagebox as messagebox
from Player import Player
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
currentplayers = []


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
        command=lambda: startTetrisGame(),
        width=12).pack(pady=(10, 5))
    tk.Button(
        gameSelectFrame,
        text="CandyCrush",
        command=lambda: startCandyCrushGame(),
        width=12).pack(pady=5)
    tk.Button(
        gameSelectFrame,
        text="Back",
        command=lambda: showFrame(mainMenuFrame),
        width=12).pack(pady=30)

def startCandyCrushGame():
    pickTwoPlayers()
    if (len(currentplayers) == 2):
        candyCrushGame = CandyCrushGame(currentplayers, container, mainMenuFrame, showFrame)
        candyCrushFrame = candyCrushGame.gamePlay()
        frames.append(candyCrushFrame)
        showFrame(candyCrushFrame)

def startTetrisGame():
    pickTwoPlayers()
    if (len(currentplayers) == 2):
        tetrisGame = TetrisGame(currentplayers, container, mainMenuFrame, showFrame)
        tetrisFrame = tetrisGame.gameSetUp()
        frames.append(tetrisFrame)
        showFrame(tetrisFrame)

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
        newPlayer = Player(username, 0)
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

def pickTwoPlayers():
    currentplayers.clear()
    selectWindow = tk.Toplevel(container)
    selectWindow.title("Player Select")
    label = tk.Label(selectWindow, text="Please Select Two Players")
    label.pack(pady=10)
    playerBtns = []

    #Centers New Window Somewhat Over Main Window
    selectWindow.geometry(f"+{root.winfo_x() + (root.winfo_width())//4}+{root.winfo_y() +(root.winfo_height())//4}")

    def addPlayer(player, playerInd):
        print(playerInd)
        if len(currentplayers) < 2:
            currentplayers.append(player)
        if len(currentplayers) == 2:
            selectWindow.destroy()
        playerBtns[playerInd].config(state="disabled")

    for playerInd in range(len(players)):
        player = players[playerInd]
        playerBtn = tk.Button(
            selectWindow,
            text=player.getUsername(),
            command=lambda p=player, ind = playerInd: addPlayer(p, ind),
            width=12)
        playerBtn.pack(pady=5)
        playerBtns.append(playerBtn)

    #Opens Over Main Window
    selectWindow.transient(container)
    #Stops Main Window Buttons
    selectWindow.grab_set()
    #Stops Main Window From Moving On Until Closed
    container.wait_window(selectWindow)


if __name__ == "__main__":
    main()
    signUp()
    gameSelect()
    playerSelect()
    showFrame(mainMenuFrame)
    root.mainloop()