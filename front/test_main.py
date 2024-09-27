import flet as ft 
from time import sleep

def main(page: ft.Page):
    i=1
    sex = ft.Text(value=" 👉👌", size = 90)
    
    page.controls.append(sex)
    page.update
    while True:
        sleep(0.1)
        if i == 1:
            page.controls[0].value = " 👉 👌"
            i = 0
        else:
            page.controls[0].value = " 👉👌"
            i=1
        page.update()
        
ft.app(main)