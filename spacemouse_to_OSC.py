from tkinter import *
import time
from threading import *
import pyspacemouse
import time
from pythonosc import udp_client
import argparse

# define if we are using XYZ or AED or YRP
profile = "XYZ"
# define name of the param to send over OSC
actualParam = ""
# define data of the param to send over OSC
actualParamData = 0

# Definition de la fenetre
window = Tk()
window.title("Spacemouse to OSC")
window.geometry('800x200')
window.configure(bg='black')
window.grid_columnconfigure(1, minsize=100)


def threading_start():
    # Call work function
    t1 = Thread(target=spacemouse_callback)
    t1.start()


def threading_stop():
    Thread(target=spacemouse_callback).terminate


def button_0(state, buttons, pressed_buttons):
    print("Button:", pressed_buttons)


def button_0_1(state, buttons, pressed_buttons):
    print("Buttons:", pressed_buttons)


def someButton(state, buttons):
    print("Some button")


callback_life = True


def spacemouse_callback():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=32764,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

    button_arr = [pyspacemouse.ButtonCallback(0, button_0),
                  pyspacemouse.ButtonCallback(
                      [1], lambda state, buttons, pressed_buttons: print("Button: 1")),
                  pyspacemouse.ButtonCallback([0, 1], button_0_1), ]

    def someButton(state, buttons):
        global profile
        print("Some button")
        if (buttons[1] == 1):
            if (profile == "XYZ") :
                profile = "AED"
            elif (profile == "AED") :
                profile = "YRP"
            else :
                profile = "XYZ"

    def sendOSC(state):
        global profile
        global actualParam
        global actualParamData
        if (profile == "XYZ"):
            if (state.x == state.y == state.z == 0):
                client.send_message("/spacemouse/x", 0)
                client.send_message("/spacemouse/y", 0)
                client.send_message("/spacemouse/z", 0)
                text_value_dictionary["text_value_X"].set("000")
                text_value_dictionary["text_value_Y"].set("000")
                text_value_dictionary["text_value_Z"].set("000")
            else:
                if (abs(state.x) > abs(state.y) and abs(state.x) > abs(state.z)):
                    actualParam = "x"
                    actualParamData = state.x
                elif (abs(state.y) > abs(state.x) and abs(state.y) > abs(state.z)):
                    actualParam = "y"
                    actualParamData = state.y
                else:
                    actualParam = "z"
                    actualParamData = state.z
        else:
            if (state.roll == state.pitch == state.yaw == 0):
                client.send_message("/spacemouse/roll", 0)
                client.send_message("/spacemouse/pitch", 0)
                client.send_message("/spacemouse/yaw", 0)
                text_value_dictionary["text_value_ROLL"].set("000")
                text_value_dictionary["text_value_PITCH"].set("000")
                text_value_dictionary["text_value_YAW"].set("000")
                client.send_message("/spacemouse/a", 0)
                client.send_message("/spacemouse/e", 0)
                client.send_message("/spacemouse/d", 0)
                text_value_dictionary["text_value_A"].set("000")
                text_value_dictionary["text_value_E"].set("000")
                text_value_dictionary["text_value_D"].set("000")
            else:
                if (abs(state.roll) > abs(state.pitch) and abs(state.roll) > abs(state.yaw) and abs(state.roll) > abs(state.z) and profile == "YRP"):

                    actualParam = "roll"
                    actualParamData = state.roll
                elif (abs(state.pitch) > abs(state.roll) and abs(state.pitch) > abs(state.yaw) and abs(state.pitch) > abs(state.z)):
                    if (profile == "AED"):
                        actualParam = "d"
                    else :
                        actualParam = "pitch"
                    actualParamData = state.pitch
                elif (abs(state.z) > abs(state.roll) and abs(state.z) > abs(state.yaw) and abs(state.z) > abs(state.pitch) and profile == "AED"):
                    actualParam = "e"
                    actualParamData = state.z
                else:
                    if (profile == "AED"):
                        actualParam = "a"
                    else :
                        actualParam = "yaw"
                    actualParamData = state.yaw
        actualParamData = int(float(actualParamData)*10000)
        if (actualParamData > 10000 or actualParamData < -10000):
            actualParamData = 0
        if (actualParamData != 0):
            text_value_dictionary["text_value_"+actualParam.upper()].set(actualParamData)
        client.send_message("/spacemouse/"+actualParam, actualParamData)

    success = pyspacemouse.open(dof_callback=sendOSC, button_callback=someButton,
                                button_callback_arr=button_arr)
    if success:
        global callback_life
        while callback_life:
            pyspacemouse.read()
            time.sleep(0.01)


# test after() function to execute inside loop
window.after(1000, threading_start)

# Définition du titre
lbl = Label(window, font='Helvetica 16 bold', text="Spacemouse to OSC",
            bg='black', fg='white', pady=5, padx=5, anchor="w")

frame_XYZ = Frame(window, highlightbackground="white",
                  highlightthickness=2, bg='black')
frame_X = Frame(frame_XYZ)
frame_Y = Frame(frame_XYZ)
frame_Z = Frame(frame_XYZ)

frame_AED = Frame(window, highlightbackground="white",
                  highlightthickness=2, bg='black')
frame_A = Frame(frame_AED)
frame_E = Frame(frame_AED)
frame_D = Frame(frame_AED)

frame_YRP = Frame(window, highlightbackground="white",
                  highlightthickness=2, bg='black')
frame_ROLL = Frame(frame_YRP)
frame_PITCH = Frame(frame_YRP)
frame_YAW = Frame(frame_YRP)

# Declaration of text variable
text_value_dictionary = dict()
text_value_dictionary["text_value_X"] = StringVar()
text_value_dictionary["text_value_X"].set("000")
text_value_dictionary["text_value_Y"] = StringVar()
text_value_dictionary["text_value_Y"].set("000")
text_value_dictionary["text_value_Z"] = StringVar()
text_value_dictionary["text_value_Z"].set("000")

text_value_dictionary["text_value_A"] = StringVar()
text_value_dictionary["text_value_A"].set("000")
text_value_dictionary["text_value_E"] = StringVar()
text_value_dictionary["text_value_E"].set("000")
text_value_dictionary["text_value_D"] = StringVar()
text_value_dictionary["text_value_D"].set("000")

text_value_dictionary["text_value_ROLL"] = StringVar()
text_value_dictionary["text_value_ROLL"].set("000")
text_value_dictionary["text_value_PITCH"] = StringVar()
text_value_dictionary["text_value_PITCH"].set("000")
text_value_dictionary["text_value_YAW"] = StringVar()
text_value_dictionary["text_value_YAW"].set("000")

# Declaration of tkinter labels
lbl_XYZ = Label(frame_XYZ, font='Helvetica 14 bold',
                text="XYZ", bg='black', fg='white')
lbl_X = Label(frame_X, font='Helvetica 10 bold',
              text="X", bg='black', fg='white')
lbl_data_X = Label(frame_X, font='Helvetica 10',
                   textvariable=text_value_dictionary["text_value_X"], bg='white', fg='black')
lbl_Y = Label(frame_Y, font='Helvetica 10 bold',
              text="Y", bg='black', fg='white')
lbl_data_Y = Label(frame_Y, font='Helvetica 10',
                   textvariable=text_value_dictionary["text_value_Y"], text="0.0000", bg='white', fg='black')
lbl_Z = Label(frame_Z, font='Helvetica 10 bold',
              text="Z", bg='black', fg='white')
lbl_data_Z = Label(frame_Z, font='Helvetica 10',
                   textvariable=text_value_dictionary["text_value_Z"], text="0.0000", bg='white', fg='black')

lbl_AED = Label(frame_AED, font='Helvetica 14 bold',
                text="AED", bg='black', fg='white')
lbl_A = Label(frame_A, font='Helvetica 10 bold',
              text="A", bg='black', fg='white')
lbl_data_A = Label(frame_A, font='Helvetica 10',
                   textvariable=text_value_dictionary["text_value_A"], text="0.0000", bg='white', fg='black')
lbl_E = Label(frame_E, font='Helvetica 10 bold',
              text="E", bg='black', fg='white')
lbl_data_E = Label(frame_E, font='Helvetica 10',
                   textvariable=text_value_dictionary["text_value_E"], text="0.0000", bg='white', fg='black')
lbl_D = Label(frame_D, font='Helvetica 10 bold',
              text="D", bg='black', fg='white')
lbl_data_D = Label(frame_D, font='Helvetica 10',
                   textvariable=text_value_dictionary["text_value_D"], text="0.0000", bg='white', fg='black')

lbl_YRP = Label(frame_YRP, font='Helvetica 14 bold',
                text="YRP", bg='black', fg='white')
lbl_ROLL = Label(frame_ROLL, font='Helvetica 10 bold',
              text="R", bg='black', fg='white')
lbl_data_ROLL = Label(frame_ROLL, font='Helvetica 10',
                   textvariable=text_value_dictionary["text_value_ROLL"], text="0.0000", bg='white', fg='black')
lbl_PITCH = Label(frame_PITCH, font='Helvetica 10 bold',
              text="P", bg='black', fg='white')
lbl_data_PITCH = Label(frame_PITCH, font='Helvetica 10',
                   textvariable=text_value_dictionary["text_value_PITCH"], text="0.0000", bg='white', fg='black')
lbl_YAW = Label(frame_YAW, font='Helvetica 10 bold',
              text="Y", bg='black', fg='white')
lbl_data_YAW = Label(frame_YAW, font='Helvetica 10',
                   textvariable=text_value_dictionary["text_value_YAW"], text="0.0000", bg='white', fg='black')

# Placement des éléments dans la fenetre
lbl.grid(column=0, row=0)

# Placement XYZ
frame_XYZ.grid(column=0, row=1, padx=2, pady=2)
lbl_XYZ.grid(column=0, row=0, columnspan=3)
frame_X.grid(column=0, row=1)
#frame_X.grid_columnconfigure(1, minsize=30)
frame_Y.grid(column=1, row=1)
frame_Z.grid(column=2, row=1)
lbl_X.grid(column=0, row=0, sticky="nesw")
lbl_data_X.grid(column=0, row=1, sticky="nesw")
lbl_Y.grid(column=0, row=0, sticky="nesw")
lbl_data_Y.grid(column=0, row=1, sticky="nesw")
lbl_Z.grid(column=0, row=0, sticky="nesw")
lbl_data_Z.grid(column=0, row=1, sticky="nesw")

# Placement AED
frame_AED.grid(column=1, row=1, padx=2, pady=2)
lbl_AED.grid(column=0, row=0, columnspan=3)
frame_A.grid(column=0, row=1)
frame_E.grid(column=1, row=1)
frame_D.grid(column=2, row=1)
lbl_A.grid(column=0, row=0, sticky="nesw")
lbl_data_A.grid(column=0, row=1, sticky="nesw")
lbl_E.grid(column=0, row=0, sticky="nesw")
lbl_data_E.grid(column=0, row=1, sticky="nesw")
lbl_D.grid(column=0, row=0, sticky="nesw")
lbl_data_D.grid(column=0, row=1, sticky="nesw")

# Placement AED
frame_YRP.grid(column=2, row=1, padx=2, pady=2)
lbl_YRP.grid(column=0, row=0, columnspan=3)
frame_ROLL.grid(column=1, row=1)
frame_PITCH.grid(column=2, row=1)
frame_YAW.grid(column=0, row=1)
lbl_ROLL.grid(column=0, row=0, sticky="nesw")
lbl_data_ROLL.grid(column=0, row=1, sticky="nesw")
lbl_PITCH.grid(column=0, row=0, sticky="nesw")
lbl_data_PITCH.grid(column=0, row=1, sticky="nesw")
lbl_YAW.grid(column=0, row=0, sticky="nesw")
lbl_data_YAW.grid(column=0, row=1, sticky="nesw")

# Sur la fermeture de la fenetre event
def window_exit():
    window.destroy()
    # threading_stop()
    global callback_life
    callback_life = False


window.protocol("WM_DELETE_WINDOW", window_exit)

# Début de la fenetre
window.mainloop()
