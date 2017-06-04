#!/usr/bin/python
import os
import Tkinter as Tk
import atexit
from socket import error as socket_error
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR

default_server = "raspberrypi.local"
default_port = 9123

sock = None
def create_socket():
    global sock
    sock = socket(AF_INET, SOCK_STREAM)

Connected = False;
def connect_to_server(client, port = default_port):
    create_socket()
    try:
        sock.connect((client, port))
        os.system('xset r off')
        return "Connected"
    except socket_error as exc:
        os.system('xset r on')
        return "%s" % exc

def disconnect_from_server():
    global sock
    sock.close()

def SendKeys():
    global Connected
    data = str(keys['w'][0]) + str(keys['a'][0]) + str(keys['s'][0]) + str(keys['d'][0])
    if Connected:
        try:
            sock.send(data)
        except socket_error as e:
            Connected = False
            b.config(text = "Connect")
            state.config(text = "Disconnected", fg = 'red')
            ipBox.config(state='normal')
            portBox.config(state='normal')

            disconnect_from_server()
    else:
        return "Error"

def on_exit():
    global Connected
    if Connected:
        disconnect_from_server()
    os.system('xset r on')
    root.quit()

atexit.register(on_exit)

root = Tk.Tk()
canvas = Tk.Canvas(root, width = 195, height = 125)

W_png = Tk.PhotoImage(data = "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")

A_png = Tk.PhotoImage(data = "iVBORw0KGgoAAAANSUhEUgAAADgAAAA1CAQAAAC+EeBLAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAAEgAAABIAEbJaz4AAAAHdElNRQfhBgMGJQ/w+IkNAAAEbElEQVRYw72YzW9UVRTAf/e+NzPtTGkJlErTsgBJSAgJlgqhMS5F48LEECsb48IYE0lc8BewM8adccFGV8YAf4ERjCHaabGtVKSK1LSFUFNsoV9jOzN9714X73veDO28duZMZt6d++be3z3n3HPumSdO8wtfd+1/PTeYPiX3INh90Wq1PF64tvD9h4sGQvPN4YMfd1xo6TaMRtAANLZdnFv+dv7Kew+Nnq7eS/s/ynYa0rstIj9NIiI22pCpjvRJyc0Js/PN9sFMm0YDAomBiCBFjWt8UTqG0ShslNuX2dNxoes3M/duS7dzU5BColAIcLHSbwWf3tVZpA5dg0+vJTHYxHIX2tKTGzTT/cJQgCCFwHI19aZWGEgEyu3Xvpba1UFHwF5bhZAptDevmXrZFO3OYAOJ7ZvDM1yZByzRwjH21TBosIzKb05LITBcIMi9JsLzno5tEcEsnzFDlou8jZFoA4HCQKAciwjpGUFU2ZE2w0wwzzQ3WU6IC4zvGFlqtOuhSpEs8DNFACaY3GFO8Cgy7PhKucufbv8Ct1jfASx4yVo4yRp5FgETicUIM8j6WTGo1DU0FEwzjkWWfrqBWUawdkHHmhqWGeUh0Ml5TgAFhphPrGNAqeFDwROGWUdwlFfoIwtM8rubhRqgoeYek0Cafg7yEl3AE4ZY2x0gMWSBn3gGdHGGNMc4jkBxm5mEJvXikOpxKJhmDAXs5Skj/EU7JjBLns1EMOW/zWoalskzB8AMnyKBAjawwS3eojch0nGGiX8+eCKZJ0/JNW0hMvAPfqUnsR+pHoeKO0wBgjSttNJKliytGMAKP7KaABhQzMrtIlkizzLQwRscQbsnY5EfuIPNOPcZqLP0cFDOkW2Gs7kjD7iLAo7zAS+iEAgkFjmmKDDHEH201F3teIpJFTGooMgoc0CWAXp9/SDDGQ4DRfI8rjvjhOIwmmkE/zBMCehlgHSkQjnCaVLAfcaw6vRjlUzjAG3u8YgMOc5yNGI2RY5X6SHDBrdZTgCk2qbRvMD7aEzOkkVXTNvHJywA3dRbsQYqmdGhkn763W0SH7SP8zgxayQAOldTV+xSw/VltUEC6del9eGCWIglb73F2re6/7xRvg/1Dguk7QFdH1aatHFAR8xGo6JA3SwNvflVPHk3Sj+vtq+SvBuHBN0cDcM+rFFENQaooVlxGCCb4kNdLSyaoZ8PFA31oSCSacIx0kgNlQs2vcPDaiDSxobKONzArvtY3a4UKcfjsMAKtQ7WrU7I5/ULLJbYDMWhdpAWixi0++e58AtEGfkWtAIJ7wAdqggEmjKLrAXVnzbVqj7g/HSdOQq0kYpA8dtEpgp00DXfNkVWKbjPaADUsmmPqXPCfeZT4l+eIasYNv58cDt3vUd7vvaWPWpaV60T5qGgM8n/v+2K9di6Lkvfla/ZhWacidZq+WrxhvH5f39PAYdoC1fhu/1SlvWo/FXpysl5cZEv+eJA5pzxjjxFewNSjkCzosbt66Ubrz29zP+DN4t2m7de8wAAADt0RVh0Y29tbWVudABFZGl0ZWQgYnkgUGF1bCBTaGVybWFuIGZvciBXUENsaXBhcnQsIFB1YmxpYyBEb21haW40zfqqAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDE3LTA2LTAzVDA4OjM2OjU4KzAyOjAwtE2TzQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxNy0wNi0wM1QwODozNjo1OCswMjowMMUQK3EAAAAASUVORK5CYII=")

S_png = Tk.PhotoImage(data = "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")

D_png = Tk.PhotoImage(data = "iVBORw0KGgoAAAANSUhEUgAAADgAAAA1CAQAAAC+EeBLAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAKqNIzIAAAAJcEhZcwAAAEgAAABIAEbJaz4AAAAHdElNRQfhBgMGJS0lmMjpAAAEJUlEQVRYw72Yy2tcVRjAf+cxM0mTJjGZxpQYJRBiA2IgNiiULlzYgpuCYOxGuyoFBRf+Be67E6Hd1IWKtMWli2LdCYqxhbaLEHxQLUZjEmMymdrMzL3nuLivMzO5k+nNTL/hzrn3nDvzO993zve4V8yzyCejI6f7FvJz8jCCzos1pert8rX1r89vKITl88mxdwfP9hxVqhs0AIvv765sfbF6+e3f1fjoMx+MXDhUVDIaFnW3ZhHR9Gslc4P5Wck3d3Tx9YGFQr/FAgKJQtQhRUrbPCnbhLEYfEzYVzg8eHb0ru57q+doMCjIITEYBIRYGZ8l31EbTNI6bfIdnUkUNbxwoj3jfQs6/5JQBhDkEHihptFfGwdikeHsRayHrQMm58ZB5rDR/+rccSkGgiGJxI/NIRo+xNNIX7HGq+DMYFAJfkgjotWzIa5GGT8EKfIUyKMP4C8GFdoKrNAWiwgPAMlvXOFPFCDQ9FFkkhmmKSIzASPjB6uuA7u7hihzj/vOtSBHkXne4BV6M+sZ2U+7M0i7scIKf7HEec5wKCMsomjL3s6teZEZqpRY4QE7GH7iEkOcRh3IsDph10uOVzkH1NjkFl9yF4/7fMoMkwcwaAsNBTl6kQiGmWSai/yA5Q7f8lyGzZNQpOu8e1neYpDM8Q5PA2W+YzuDiyRhQabh6kUyzyxg+ZXVjBo6QPZBCixDzKCBLdYfGxcgg0MGRts/DWlGyAM1HmaAmfjQ7WiYzDGr2DAHxY6//zaosU4VyNOfGdrSD+tvlWyyhAcMUcwE29cPXRH4fM89QDLFWBj5Hw8XB29SNYxyoaTKIp+xAfRzgsHUuNuOjjpth1oq7GDZ5W8W+YolLII5TmZKUo5J0zSscoNlapRYY41HWGCKc4xnwO25ho1An2WWnX7FMS5wEpnZoE4CbhysbyU9jPEyZzhOIRPOzYi6UTfLU5xgKiwQFb0MM8E0zzMMGXEtTWp4lvcx8R7V5Cmgw7onK64hAQtcwyoG4gI4KntNapHYvoYpRVQyp0QO/pDjrGE7oe3gklhQdxtVD2wzeHcGCST5sPv6RbV9i+DdeWTb6akzwKBtq4jqFNBCmh92D/lE1rCth5lu6JcSSzstgrpI4/pINzU0IVhHycPrItLHp6kufYSP6hJ0l2qzH5bZhtTH7tbmatUv8PiXmuOHNkB6bKAYiBNtkn4bk7FoyvzuDrBOqhZYqmywk7yfstqU7JHg1v9YoUw/uToo4Fzj9LgevPfhs0uJslOpmy3t3zKnRPieoMIam8g9DNv8frCd0ejVXqy95/+ovaveC3oi6ay1uRGyiPeHd11WblSv+eUnkRO9UvXq7k118eEvPwMT9CfP+53/GM97UL1SuTy7Kt7jYz46Ujil3pRzDHQh5Ags2+a2f71y87V/PuR/vGpC4OUbiJUAAAA7dEVYdGNvbW1lbnQARWRpdGVkIGJ5IFBhdWwgU2hlcm1hbiBmb3IgV1BDbGlwYXJ0LCBQdWJsaWMgRG9tYWluNM36qgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxNy0wNi0wM1QwODozNjo1MCswMjowMIei3aoAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTctMDYtMDNUMDg6MzY6NTArMDI6MDD2/2UWAAAAAElFTkSuQmCC")

image1 = canvas.create_image(100, 35, anchor = Tk.CENTER, image = W_png)
image2 = canvas.create_image(40, 90, anchor = Tk.CENTER, image = A_png)
image3 = canvas.create_image(100, 90, anchor = Tk.CENTER, image = S_png)
image4 = canvas.create_image(160, 90, anchor = Tk.CENTER, image = D_png)
rec1 = canvas.create_rectangle(74, 10, 125, 59, outline="red", state='hidden', width = 5)
rec3 = canvas.create_rectangle(74, 67, 125, 115, outline="red", state='hidden', width = 5)
rec2 = canvas.create_rectangle(15, 67, 66, 115, outline="red", state='hidden', width = 5)
rec4 = canvas.create_rectangle(135, 67, 185, 115, outline="red", state='hidden', width = 5)
canvas.grid(column = 0, rowspan = 2, pady = 30)
root.wm_geometry("500x200")
root.title('Remote Control')
root.resizable(False, False)

ip = Tk.StringVar()
ip.set(default_server)
ipBox = Tk.Entry(root, textvariable = ip, width = 15)
ipBox.grid(column = 1, row = 0)

port = Tk.StringVar()
port.set(str(default_port))
portBox = Tk.Entry(root, textvariable = port, width = 5)
portBox.grid(column = 2, row = 0)

state = Tk.Label(root, text="Disconnected", font=("Helvetica", 14), fg = 'red', justify=Tk.RIGHT)
state.grid(column = 1, columnspan = 3, row = 1)

def onButtonDown():
    global Connected
    if not Connected:
        result = connect_to_server(ip.get(), int(port.get()))
        print result

        if result == "Connected":
            Connected = True
            b.config(text = "Disconnect")
            state.config(text = "Connected to {}:{}".format(ip.get(), port.get()), fg = 'green')
            ipBox.config(state='readonly')
            portBox.config(state='readonly')
        else:
            state.config(text = result[result.index("]") + 1:])
    else:
        disconnect_from_server()
        Connected = False
        state.config(text = "Disconnected", fg = 'red')
        b.config(text = "Connect")
        ipBox.config(state='normal')
        portBox.config(state='normal')

b = Tk.Button(root, text="Connect", width=10, command = onButtonDown)
b.grid(column = 3, row = 0)

keys = {'w': [0, rec1], 'a': [0, rec2], 's': [0, rec3], 'd': [0, rec4]}

def keyPressHandler(event):
    try:
        keys[event.char][0] = 1;
        canvas.itemconfigure(keys[event.char][1], state = 'normal')
        SendKeys()
    except KeyError:
        pass

def keyReleaseHandler(event):
    try:
        keys[event.char][0] = 0;
        canvas.itemconfigure(keys[event.char][1], state = 'hidden')
        SendKeys()
    except KeyError:
        pass

root.bind_all('<KeyPress>', keyPressHandler)
root.bind_all('<KeyRelease>', keyReleaseHandler)
root.wm_protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
