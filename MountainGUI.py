import PySimpleGUI as PyGUI
from Main import findPath
from math import log10 , floor
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def round_it(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def drawFigure():
    print("hello")

def main():
    amount = 0
    #layout of the window
    layout = [  [PyGUI.Text("Navigating Mount Saint Helens is a shortest path calculator that finds the shortest path cost",size=(100, 1), font='Lucida',justification='left')],
                [PyGUI.Text("from two points on Mount Saint Helens.",size=(100, 1), font='Lucida',justification='left')],
                [PyGUI.Text('____________________________________________________________________________________________________',size=(80, 1), font='Lucida',justification='left')],
                [PyGUI.Text('Choose a Search Algorithm: ',size=(19, 1), font='Lucida',justification='left'), 
                PyGUI.Combo(['Dijkstra','A*','Weighted A*'],size=(15, 1),default_value='Dijkstra',key='algorithm')],
                [PyGUI.Text('Start: ',size=(10, 1), font='Lucida',justification='left'), 
                PyGUI.Combo(['50','100','150','200','250','300','350','400','450','500'],size=(10, 1),default_value='250',key='startX'),
                PyGUI.Combo(['50','100','150','200','250','300','350','400','450','500'],size=(10, 1),default_value='250',key='startY')],
                [PyGUI.Text('Goal: ',size=(10, 1), font='Lucida',justification='left'), 
                PyGUI.Combo(['50','100','150','200','250','300','350','400','450','500'],size=(10, 1),default_value='400',key='goalX'),
                PyGUI.Combo(['50','100','150','200','250','300','350','400','450','500'],size=(10, 1),default_value='400',key='goalY')],
                [PyGUI.Button('Find Path',size=(10, 1))],
                [PyGUI.Text('____________________________________________________________________________________________________',size=(80, 1), font='Lucida',justification='left')],
                [PyGUI.Text('Time (s): ',size=(6, 1), font='Lucida',justification='left'),
                PyGUI.Text('',size=(18, 1), font='Lucida',justification='left', key='time')],
                [PyGUI.Text('Path Cost: ',size=(7, 1), font='Lucida',justification='left'),
                PyGUI.Text('',size=(18, 1), font='Lucida',justification='left', key='pathCost')],
                [PyGUI.Text('Nodes Explored: ',size=(11, 1), font='Lucida',justification='left'),
                PyGUI.Text('',size=(18, 1), font='Lucida',justification='left', key='nodes')],
                [PyGUI.Text('____________________________________________________________________________________________________',size=(80, 1), font='Lucida',justification='left')],
                [PyGUI.Text("Algorithms",size=(20, 1), font='Lucida',justification='left')],
                [PyGUI.Text("      - Dijkstra's Algorithm: A search algorithm used to find the shortest path between two points.",size=(80, 1), font='Lucida',justification='left')],
                [PyGUI.Text("      - A* Algorithm: A search algorithm based off of Dijkstra's, however has added hueristics to",size=(100, 1), font='Lucida',justification='left')],
                [PyGUI.Text("        find the shortest path with less work.",size=(80, 1), font='Lucida',justification='left')],
                [PyGUI.Text("      - Weighted A* Algorithm: A weighted version of A* which weights the heuristics to better",size=(80, 1), font='Lucida',justification='left')],
                [PyGUI.Text("        find the goal.",size=(80, 1), font='Lucida',justification='left')],
                [PyGUI.Button('Exit',size=(10, 1))]
            ]

    # Create the Window
    window = PyGUI.Window("Navigating Mount Saint Helens", layout = layout, size=(670, 600))


    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == PyGUI.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            break
        # Ensure the input is valid
        elif event == 'Find Path':
            algorithm = 'Dijkstra'
            if values['algorithm'] == 'Dijkstra':
                algorithm = 'Dijkstra'
            elif values['algorithm'] == 'A*':
                algorithm = 'AStarExp'
            elif values['algorithm'] == 'Weighted A*':
                algorithm = 'AStarMSH'
            else:
                PyGUI.Print(f'An error happened.  Here is the info:')
                PyGUI.Print(f'Your inputted algorithm is invalid. Please choose one of the three provided search algorithms.')
                PyGUI.popup_error(f'ERROR!')
                continue
            # Ensure the start and end coordinates are valid
            try:
                startX = int(values['startX'])
                startY = int(values['startY'])
                start = [startX, startY]
                goalX = int(values['goalX'])
                goalY = int(values['goalY'])
                goal = [goalX, goalY]
            except:
                PyGUI.Print(f'An error happened.  Here is the info:')
                PyGUI.Print(f'Your inputted start and end coordinates were not the proper type. Please enter integers between 0 and 500.')
                PyGUI.popup_error(f'ERROR!')
                continue
            # Check if the start and end coordinates are the same, throw an error if they are
            if start[0] == goal[0] and start[1] == goal[1]:
                PyGUI.Print(f'An error happened.  Here is the info:')
                PyGUI.Print(f'Your start and end points are the same. They must be different for the program to calculate the shortest path.')
                PyGUI.popup_error(f'ERROR!')

            else:
                output = findPath(algorithm, start, goal)
                
                #update the layout of the screen with the calcualted time, path cost, and number of nodes explored
                time = round_it(output[0], 4)
                path = round_it(output[1], 4)
                nodes = round_it(output[2], 4)
                window['time'].update(value=time)
                window['pathCost'].update(value=path)
                window['nodes'].update(value=nodes)

    window.close()


