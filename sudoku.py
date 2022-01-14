import numpy as np 
import os 

def clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system("cls")

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

def run():
    clear()
    sudoku_size = int(input('• para sudoku 2x2 ingrese 1\n• para sudoku 3x3 ingrese 2\n\n  Ingrese el tamaño del sudoku: '))
    if sudoku_size not in [1,2]:
        while True:
            clear()
            print("La entrada no es válida, por favor ingresar una opcion valida")
            sudoku_size = int(input('• para sudoku 2x2 ingrese 1\n• para sudoku 3x3 ingrese 2\n\n  Ingrese el tamaño del sudoku: '))
            if sudoku_size in [1,2]:
                break

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
    if sudoku_size == 1:
        if difficulty_level == 1:
            matrix = np.matrix([
                        [4,0,  0,0], 
                        [0,0,  0,3],
                        [1,0,  0,0],
                        [0,0,  0,2]
                        ])
            

        elif difficulty_level == 2:
            pass
        elif difficulty_level == 3:
            pass

    elif sudoku_size == 2:
        if difficulty_level == 1:
            pass
        elif difficulty_level == 2:
            matrix = np.matrix([
                        [9,0,7,  8,0,0,  0,6,0], 
                        [0,0,6,  7,0,0,  1,8,0],
                        [0,1,0,  0,0,0,  0,0,0],
                        [0,0,8,  0,0,4,  0,0,0],
                        [1,0,0,  0,5,0,  0,0,3],
                        [0,0,0,  0,9,0,  0,7,8],
                        [0,0,0,  0,1,0,  0,0,0],
                        [6,0,0,  4,0,0,  0,0,5],
                        [5,0,0,  0,0,9,  0,0,1]
                        ])

        elif difficulty_level == 3:
            pass

    game(matrix)


if __name__ == "__main__":
    run()
