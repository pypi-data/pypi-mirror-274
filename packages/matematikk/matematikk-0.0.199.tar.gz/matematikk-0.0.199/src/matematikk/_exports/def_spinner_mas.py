import os

def spinner(i_spin):

    # Tøm terminal-skjerm
    os.system("clear")

    i_spin += 1
    if i_spin == 0: print("|")
    if i_spin == 1: print("/")
    if i_spin == 2: print("-")
    if i_spin == 3: print("\\")
    if i_spin == 4: print("|")
    if i_spin == 5: print("/")
    if i_spin == 6: print("-")
    if i_spin == 7: print("\\")

    if i_spin == 7: i_spin = -1

    return i_spin
