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


def print_matrix(matrix):
    clear()
    print("Para retroceder presione S\nPara avanzar D\nPara verificar que este correcto V\nPara salir E\nPara ir a las casillas vacías X\nPara subir U\nPara bajar O")
    sq = np.sqrt(len(matrix))
    for i in range(len(matrix)):
        if i % sq == 0:
            print("")
        print("||", end = "")    
        for j in range(len(matrix)):
            if j==len(matrix)-1:
                if matrix[i,j] == 0:
                    print("_",end = "||") 
                else:    
                     print(matrix[i,j],end = "||") 
            if j > 0 and j %sq == 0:    
                print(end = "|")
            if j!=len(matrix)-1:
                if matrix[i,j] == 0:
                    print("_",end = " ") 
                else:    
                    print(matrix[i,j],end = " ")
        print("")    

def validate_value(i,j,matrix,val_op):
    for k in range(len(matrix)):
        if val_op == matrix[i,k] or val_op == matrix[k,j]:
            return False
    return True

def zero_matrix(matrix):
    for i in range(len(matrix)):            
        for j in range(len(matrix)):
            if  matrix[i,j] == 0:
                return i,j
    return False            

def validate_matrix(matrix):
    a = np.zeros((3, 2))
    for i in range(len(matrix)):            
        for j in range(len(matrix)):
            plus = 0
            for k in range(len(matrix)):
                if  matrix[i,j] == matrix[i,k] or  matrix[i,j] == matrix[k,j]:
                    plus += 1
                    if plus > 2:
                        return False
    return True

def grid(matrix):
    plus = 0
    sq = int(np.sqrt(len(matrix)))
    for i in range(sq):
        for j in range(sq):
            for ii in range(sq*i, sq*(i+1)):
                for jj in range(sq*j, sq*(j+1)):
                    for ix in range(sq*i, sq*(i+1)):
                        for jy in range(sq*j, sq*(j+1)):
                            if jj != jy and matrix[ii,jj] == matrix[ix,jy]:
                                #print(matrix[ii,jj], matrix[ix,jy],"     ",ii,jj, ix, jy)
                                plus += 1
                            if ii != ix and matrix[ii,jj] == matrix[ix,jy]:
                                plus += 1
                            if plus > 1:
                                return False
    return True

def game(matrix):
    print_matrix(matrix)
    o = "continue"
    while o != "exit":
        for i in range(len(matrix)):
            j = 0
            if o == "exit":
                break
            while j < len(matrix):
                if matrix[i,j] == 0:
                    print("Inserte un valor para la casilla (%d, %d): "% (i,j), end= " ")
                    op = input()
                    if op == "e":
                        o = "exit"
                        break
                    elif op == "u":
                        if i == 0:
                            i = len(matrix)-1
                        else:
                            i -= 1
                    elif op == "o":
                        if i == len(matrix)-1:
                            i = 0
                        else:
                            i += 1
                    elif op == "s":
                        if j == 0:
                            i -= 1
                            j = len(matrix)-1
                            if matrix[i,j] != 0:
                                j -= 1
                                if matrix[i,j] != 0:
                                    j -= 1
                        else:
                            j -= 1
                            if matrix[i,j] != 0:
                                if j == 0:
                                    i -= 1
                                    j = len(matrix)-1
                                    if matrix[i,j] != 0:
                                        j -= 1
                        print_matrix(matrix, len(matrix))
                    elif op == "x":
                        if zero_matrix(matrix, len(matrix)) != False:
                            i,j = zero_matrix(matrix, len(matrix))
                        else:
                            print("Ya esta completa")    
                    elif op == "d":
                        if j == len(matrix)-1:
                            i += 1
                            j = 0
                        else:    
                            j += 1
                    elif op == "v":
                        val_mat = validate_matrix(matrix,len(matrix))    
                        val_grid = grid(matrix, len(matrix))        
                        if val_mat == False or val_grid == False:
                            print("No esta bien :(")
                        else:
                            print("Felicidades, lo lograste")
                    elif op in ["1","2","3","4","5","6","7","8","9"]:        
                        val_op = int(op)
                        if 1 <= val_op <=9:        
                            value = validate_value(i,j,matrix,len(matrix),val_op)
                            if value == False:
                                print_matrix(matrix, len(matrix))
                                print("No es un número válido, Inserta otro número")
                            else:    
                                matrix[i,j] = int(op)
                                j += 1
                                print_matrix(matrix, len(matrix))
                    else:
                        print_matrix(matrix, len(matrix))
                        print("No es una entrada válida")
                else:
                    j += 1

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
    # print(np.array(grid))
    for row in range(0,len(grid)):
        for col in range(0,len(grid)):
            if grid[row][col]==0:
                # print('in')
                return False
    # print(grid)
    # print('return check ok')
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

    game(np.array(ready_grid))
    

if __name__ == "__main__":
    run()