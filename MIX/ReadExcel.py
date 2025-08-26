import pandas as pd
data = pd.read_excel('C:\\Users\\jayeshkumar.patel\\Documents\\Personal\\Insurance\\Question Answer_Final_New.xlsx')
data = data.reset_index()

for index, row in data.iterrows():
    
    print(index, row['Question'], row['A'],row['B'], row['C'], row['D'])


import PySimpleGUI as sg

sg.theme('Dark Grey 13')

layout = [[sg.Text('Filename')],
          [sg.Input(), sg.FileBrowse()],
          [sg.OK(), sg.Cancel()]]

window = sg.Window('Get filename example', layout)

event, values = window.read()
window.close()