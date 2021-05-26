import matplotlib.pyplot as plt
import numpy as np
import random
import tkinter as tkr
from frame import ScrollableFrame

started = 0
# Domyslne parametry wzorów
pattern_count = 6
width = 4
height = 4
repetitions = 1000
random_patterns = False
patterns = np.zeros((pattern_count, width * height))

# Tutaj ustawiamy uszkodzony wzór (który będzie odzyskiwany)
damaged_pattern = np.array([-1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

def hopfield():
    # Wyświetlanie wzorów na ekran dzięki axes
    fig, ax = plt.subplots(1, pattern_count, figsize=(10, 5))

    for i in range(pattern_count):
        ax[i].matshow(patterns[i].reshape((height, width)), cmap='terrain')
        ax[i].set_xticks([])  # schowanie współrzędnych x,y na obrazkach
        ax[i].set_yticks([])

    plt.show()


    # Tworzenie sieci hopfielda
    W = np.zeros((width * height, width * height))

    for i in range(width * height):
        for j in range(width * height):
            if i == j or W[i, j] != 0.0:
                continue

            w = 0.0

            for n in range(pattern_count):
                w += patterns[n, i] * patterns[n, j]

            W[i, j] = w / patterns.shape[0]
            W[j, i] = W[i, j]

    # Wzor do odzyskania
    recovered_pattern = damaged_pattern.copy()

    for _ in range(repetitions):
        for i in range(width * height):
            if(np.dot(W[i], recovered_pattern) > 0):
                recovered_pattern[i] = 1.0
            elif(np.dot(W[i], recovered_pattern) < 0):
                recovered_pattern[i] = -1.0



    # Wyswietlenie wzorów przed i po zastosowaniu sieci
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    ax[0].matshow(damaged_pattern.reshape(height, width), cmap='terrain')
    ax[0].set_title('Uszkodzony')
    ax[0].set_xticks([])
    ax[0].set_yticks([])

    ax[1].matshow(recovered_pattern.reshape(height, width), cmap='terrain')
    ax[1].set_title('Odzyskany')
    ax[1].set_xticks([])
    ax[1].set_yticks([])

    plt.show()
# -----------------------------------------------------------------------------------------------
# Auto generowanie wzorów, jeżeli chcemy generować z dużą ilością pixeli, lub dużą ilością wzorów
def generate_patterns():
    global damaged_pattern
    damaged_pattern = np.empty(0)
    new_patterns = []
    global patterns
    for i in range(pattern_count + 1):
        current_pattern = []
        for j in range(width*height):
            rand = random.randint(0,1)
            if(rand==0):
                rand = -1
            current_pattern.append(rand)
        if(i==0):
            damaged_pattern = np.array(current_pattern)
        else:
            new_patterns.append(current_pattern)
    patterns = np.array(new_patterns)
    global main_window
    main_window.destroy()
    hopfield()
# -----------------------------------------------------------------------------------------------


def apply_new_parameters(count,wid,hei,rep,ran):
    global pattern_count
    global width
    global height
    global repetitions
    global random_patterns
    global patterns
    try:
        count=int(count)
        wid = int(wid)
        hei = int(hei)
        rep = int(rep)
        ran = ran
        pattern_count = count
        width = wid
        height = hei
        repetitions = rep
        random_patterns = ran
        patterns = np.zeros((pattern_count, width * height))
    except ValueError:
        tkr.messagebox.showerror("Złe dane","Podaj poprawne dane")
        start()


def ask_for_patterns():
    global main_window
    global main_frame
    global patterns
    if(random_patterns):
        generate_patterns()
        return
    try:
        main_frame.destroy()
    except tkr.TclError:
        return
    current_patterns = []

    scrollable = ScrollableFrame(main_window)

    image = tkr.PhotoImage(file='img.png')
    image2 = tkr.PhotoImage(file='img2.png')

    for i in range(pattern_count+1):

        main_frame = tkr.Frame(scrollable.scrollable_frame,bg="green")
        main_frame.pack(expand=True,fill=tkr.BOTH)

        if(i==0):
            announce_label = tkr.Label(main_frame, text="Narysuj wzór uszkodzony ",bd=10,bg="green",font=('Calibri', 20,'bold'))
        else:
            announce_label = tkr.Label(main_frame, text="Narysuj wzór nr " + str(i),bd=10,bg="green",font=('Calibri', 20,'bold'))
        announce_label.pack()
        board_frame = tkr.Frame(main_frame)
        board_frame.pack()
        current_pattern_bool = []
        boxes = []


        for a in range(height):
            for b in range(width):
                current_pattern_bool.append(tkr.BooleanVar())
                boxes.append(tkr.Checkbutton(board_frame,variable=current_pattern_bool[a*width+b],image=image2,selectimage=image,indicatoron=False))
                boxes[a*width+b].grid(row=a,column=b)
        current_patterns.append(current_pattern_bool)



    next = tkr.Button(main_frame,text="Dalej",command=main_window.destroy)
    next.pack()
    scrollable.pack(side="top", expand=True, fill="both")
    main_window.mainloop()


    global damaged_pattern
    for i,x in enumerate(current_patterns):
        current_pattern = []
        for y in x:
            if (y.get()):
                current_pattern.append(-1)
            else:
                current_pattern.append(1)
        if(i==0):
            damaged_pattern = np.array(current_pattern)
        else:
            patterns[i-1] = current_pattern

    hopfield()


main_window = tkr.Tk()
main_window.title("Rekreacja wzoru sieciami hopfielda")
main_window.geometry("600x440")
main_frame = tkr.Frame(main_window,bg="green")
main_frame.pack(expand=True,fill=tkr.BOTH)



def start():
    global started
    global main_window
    global main_frame
    started+=1
    if(started>1):
        main_frame.destroy()
        main_frame = tkr.Frame(main_window, bg="green")
        main_frame.pack(expand=True, fill=tkr.BOTH)
    welcome_label = tkr.Label(main_frame,text="Podaj wartości startowe",bd=10,bg="green",font=('Calibri', 20,'bold'))
    welcome_label.pack(anchor=tkr.NW)
    form_frame = tkr.Frame(main_frame,bg="green")
    form_frame.pack(anchor=tkr.NW)

    count_label = tkr.Label(form_frame,text="Podaj ilość uczonych wzorów",bd=10,bg="green",font=('Calibri', 13,'bold'))
    count_label.grid(row=0,column=0,sticky=tkr.W)
    count_text = tkr.Text(form_frame,height=1,width=3)
    count_text.grid(row=0,column=1)
    width_label = tkr.Label(form_frame,text="Podaj szerokosc wzoru",bd=10,bg="green",font=('Calibri', 13,'bold'))
    width_label.grid(row=1,column=0,sticky=tkr.W)
    width_text = tkr.Text(form_frame,height=1,width=3)
    width_text.grid(row=1,column=1)
    height_label = tkr.Label(form_frame,text="Podaj wysokosc wzoru",bd=10,bg="green",font=('Calibri', 13,'bold'))
    height_label.grid(row=2,column=0,sticky=tkr.W)
    height_text = tkr.Text(form_frame,height=1,width=3)
    height_text.grid(row=2,column=1)
    repetitions_label = tkr.Label(form_frame,text="Podaj liczbę powtorzen pętli odtwarzania wzoru",bd=10,bg="green",font=('Calibri', 13,'bold'))
    repetitions_label.grid(row=3,column=0,sticky=tkr.W)
    repetitions_text = tkr.Text(form_frame,height=1,width=10)
    repetitions_text.grid(row=3,column=1)
    random_label = tkr.Label(form_frame,text="Zaznacz jeśli chcesz wygenerowac wzory losowo",bd=10,bg="green",font=('Calibri', 13,'bold'))
    random_label.grid(row=4,column=0,sticky=tkr.W)
    var = tkr.BooleanVar()
    random_box = tkr.Checkbutton(form_frame,variable=var,bg="green")
    random_box.grid(row=4,column=1)


    button_frame = tkr.Frame(main_frame,bg="green")
    button_frame.pack(side=tkr.TOP)

    apply_button = tkr.Button(button_frame,text="Zastosuj",command=lambda:[apply_new_parameters(count_text.get("1.0",tkr.END),width_text.get("1.0",tkr.END),height_text.get("1.0",tkr.END),repetitions_text.get("1.0",tkr.END),var.get()),ask_for_patterns()],bd=5)
    apply_button.grid(row=0,column=0,sticky=tkr.N)
    default_button = tkr.Button(button_frame,text="Użyj domyślnych wartości",command=ask_for_patterns,bd=5)
    default_button.grid(row=1,column=0,sticky=tkr.S)
    foot_label = tkr.Label(main_frame, text="Grzegorz Świst, 2021", bg="green")
    foot_label.pack(anchor=tkr.SE, side=tkr.BOTTOM)
    main_window.mainloop()


start()


