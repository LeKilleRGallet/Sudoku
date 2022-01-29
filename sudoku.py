import numpy as np 
import os
import random

def clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system("cls")

class Found(Exception):
    pass

def random_matrix():
    matrix = np.zeros((9,9))
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i,j] = np.random.randint(1,10)
    return matrix


def print_matrix(grid, subgrid_size):
    clear()
    print("\n\tPara retroceder presione S\n\tPara avanzar presione D\n\tPara salir presione E\n\tPara ir a las casillas vacías presione X\n\tPara subir presione U\n\tPara bajar presione O\n")

    print('\t      ', end='')
    for i in range(len(grid)):
        if i > 0 and i % subgrid_size == 0:
            print('   ', end='')
        print(i+1, end=' ')
    
    print("")

    print('\t     ', end='')
    print('='*(((len(grid)+1)*2)+(3*(subgrid_size-1))), end='')

    for i in range(len(grid)):
        if i % subgrid_size == 0:
            print("")
        print('\t%d'% (i+1), end="  ")
        print("|| ", end = "")
        for j in range(len(grid)):
            if (j != 0) and (j%subgrid_size == 0):
                print(end = " | ")

            if (j==(len(grid)-1)) and grid[i,j] == 0:
                print("_",end = " ||") 
            elif (j==(len(grid)-1)) and grid[i,j] != 0:
                print(grid[i,j],end = " ||") 
            elif (j!=(len(grid)-1)) and grid[i,j] == 0:
                print("_",end = " ")
            elif (j!=(len(grid)-1)) and grid[i,j] != 0:
                print(grid[i,j],end = " ")
        print("")
    print('\n')

def zero_matrix(matrix):
    for i in range(len(matrix)):            
        for j in range(len(matrix)):
            if  matrix[i,j] == 0:
                return i,j
    return False            

def validator(grid, num, row, col, l_col, subgrid_size):
    if not num in grid[row]:
        if not num in l_col:
            subgrid=[] ##try
            try:
                for subrow in range(1,subgrid_size+1):
                    for subcol in range(1,subgrid_size+1):
                        if row<(subgrid_size*subrow) and col<(subgrid_size*subcol):
                            # print('i={}'.format(i), 'row={}'.format(row), 'col={}'.format(col), 'subrow={}'.format(subrow), 'subcol={}'.format(subcol), 'subgrid_size={}'.format(subgrid_size))
                            subgrid=[grid[j][subgrid_size*(subcol-1):subgrid_size*subcol] for j in range(subgrid_size*(subrow-1),subgrid_size*subrow)]
                            raise Found
            except Found:
                if not (any(num in _ for _ in subgrid)): ##validate if num is in 'subgrid' unnesting 'subgrid'
                    return True
    return False

def check(grid):
    for row in range(0,len(grid)):
        for col in range(0,len(grid)):
            if grid[row][col]==0:
                # print('in')
                return False
    return True


def filler(grid,subgrid_size):

    number_list=[*range(1,len(grid)+1)]

    for i in range(len(grid)**2):
        row, col = i//len(grid), i%len(grid)
        if grid[row][col]==0:
            random.shuffle(number_list)
            # number_list = random.sample([*range(1,len(grid)+1)], counts = len_list, k = len(grid)*2)
            l_col = [l_row[col] for l_row in grid] #list of column values
            for num in number_list:
                if validator(grid, num, row, col, l_col, subgrid_size):
                    grid[row][col] = num
                    if check(grid):
                        # print('return check')
                        return grid
                    else:
                        if filler(grid,subgrid_size):
                            # print('return filler interno')
                            return grid
            break #if no number is found in the row, break the loop and try again with a new number_list
    grid[row][col] = 0

def solver(grid,subgrid_size):
    # print('in solver')
    global counter

    number_list=[*range(1,len(grid)+1)]

    for i in range(len(grid)**2):
        row, col = i//len(grid), i%len(grid)
        if grid[row][col]==0:
            random.shuffle(number_list)
            # number_list = random.sample([*range(1,len(grid)+1)], counts = len_list, k = len(grid)*2)
            l_col = [l_row[col] for l_row in grid] #list of column values
            for num in number_list:
                if validator(grid, num, row, col, l_col, subgrid_size):
                    grid[row][col] = num
                    if check(grid):
                        # print('in check return')
                        counter += 1
                        break
                    else:
                        if solver(grid,subgrid_size):
                            # print('return filler interno')
                            return grid ## or True???
            break
    grid[row][col] = 0


def remove(grid, subgrid_size, difficulty_level):
    # print('in remove')
    global counter
    attempts = difficulty_level*(len(grid)//subgrid_size)
    counter = 1
    while attempts > 0:
        # print('in while1')
        row, col = random.randint(0,len(grid)-1), random.randint(0,len(grid)-1)
        while grid[row][col]==0:
            # print('in while2')
            row, col = random.randint(0,len(grid)-1), random.randint(0,len(grid)-1)
        backup, grid[row][col] = grid[row][col], 0
        # copyGrid = grid[:]###????
        counter=0
        solver(grid,subgrid_size)

        if counter != 1:
            # print('in counter != 1')
            grid[row][col] = backup
            # print(np.array(grid))
            attempts -= 1
    
    return grid
            


def game(grid, subgrid_size):
    #agregar que el usuario pueda ir a una celda de su eleccion de inmediato
    #agregar que el usuario pueda identificar cuales son las celdas que vienen por defecto y que no se pueden modificar
    base_grid=[_[:] for _ in grid]#do a deepcopy of the grid
    grid=np.array(grid)
    print_matrix(grid, subgrid_size)
    while True:
        for col in range(len(grid)):
            row = 0
            while row < len(grid):
                if base_grid[col][row] == 0:
                    try:
                        op= input("\tInserte un valor para la casilla (%d, %d): "% (row+1,col+1))
                        op= int(op)
                        if op in [*range(1,len(grid)+1)]:
                            l_col = [l_row[row] for l_row in grid]
                            if validator(grid, op, col, row, l_col, subgrid_size):
                                grid[col,row]=op
                                row+=1
                                print_matrix(grid, subgrid_size)
                            else:
                                print('\teste valor ya se encuentra en la fila, columna o caja')
                        else:
                            print_matrix(grid, subgrid_size)
                            print('\tel numero debe estar entre 1 y %d vuelve a intentarlo'% (len(grid)+1))

                    except ValueError: #if user entered a string

                        op= op.lower()

                        if op == "e":
                            aborted=input('\testas seguro que quieres salir? (s/n)')
                            if aborted.lower() == 's':
                                raise SystemExit('\n\tel juego ha finalizado con exito')
                        elif op == "u":
                            if col == 0:
                                col = len(grid)-1
                            else:
                                col -= 1
                        elif op == "o":
                            if col == len(grid)-1:
                                col = 0
                            else:
                                col += 1
                        elif op == "s":
                            if row == 0:
                                col -= 1
                                row = len(grid)-1
                                if grid[col,row] != 0:
                                    row -= 1
                                    if grid[col,row] != 0:
                                        row -= 1
                            else:
                                row -= 1
                                if grid[col,row] != 0:
                                    if row == 0:
                                        col -= 1
                                        row = len(grid)-1
                                        if grid[col,row] != 0:
                                            row -= 1
                            print_matrix(grid, subgrid_size)
                        elif op == "x":
                            if zero_matrix(grid) != False:
                                col,row = zero_matrix(grid)
                            else:
                                print("Ya esta completa")    
                        elif op == "d":
                            if row == len(grid)-1:
                                col += 1
                                row = 0
                            else:
                                row += 1
                        else:
                            print_matrix(grid, subgrid_size)
                            print("No es una entrada válida")
                else:
                    if check(grid):
                        raise SystemExit('\n\tEnhorabuena! lograste resolver el sudoku\n\tGracias por jugar\n')
                    row += 1


def run():
    clear()
    grid_size = int(input('• para sudoku 4x4 con subcuadriculas 2x2 ingrese 4\n• para sudoku 9x9 con subcuadriculas 3x3 ingrese 9\n  Ingrese el tamaño de las celdas del sudoku: '))
    if grid_size not in [4,9]:
        while True:
            clear()
            print("La entrada no es válida, por favor ingresar una opcion valida")
            grid_size = int(input('• para sudoku 4x4 con subcuadriculas 2x2 ingrese 4\n• para sudoku 9x9 con subcuadriculas 3x3 ingrese 9\n  Ingrese el tamaño de las celdas del sudoku: '))
            if grid_size in [4,9]:
                break
    
    subgrid_size = None
    if grid_size == 4:
        subgrid_size = 2
    elif grid_size == 9:
        subgrid_size = 3


    clear()
    difficulty_level = int(input('• para dificultad fácil ingrese 1\n• para dificultad media ingrese 2\n• para dificultad dificil ingrese 3\n\n  Ingrese el grado de dificultad: '))
    if difficulty_level not in [1,2,3]:
        while True:
            clear()
            print("La entrada no es válida, por favor ingresar una opcion valida")
            difficulty_level = int(input('• para dificultad fácil ingrese 1\n• para dificultad media ingrese 2\n• para dificultad dificil ingrese 3\n\n  Ingrese el grado de dificultad: '))
            if difficulty_level in [1,2,3]:
                break
    
    clear()
    zero_grid=[[0]*grid_size for i in range(grid_size)]

    fully_grid=filler(zero_grid,subgrid_size)

    ready_grid=remove(fully_grid,subgrid_size,difficulty_level)

    game(ready_grid, subgrid_size)
    

if __name__ == "__main__":
    run()