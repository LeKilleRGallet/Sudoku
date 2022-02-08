import pygame
import math 
import numpy as np 
import os
import random


class Found(Exception):
    pass

def clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system("cls")

def validator(grid, num, row, col, l_col, subgrid_size):
    if not num in grid[row]:
        if not num in l_col:
            subgrid=[]
            try:
                for subrow in range(1,subgrid_size+1):
                    for subcol in range(1,subgrid_size+1):
                        if row<(subgrid_size*subrow) and col<(subgrid_size*subcol):
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
                return False
    return True

def filler(grid,subgrid_size):

    number_list=[*range(1,len(grid)+1)]

    for i in range(len(grid)**2):
        row, col = i//len(grid), i%len(grid)
        if grid[row][col]==0:
            random.shuffle(number_list)
            l_col = [l_row[col] for l_row in grid] #list of column values
            for num in number_list:
                if validator(grid, num, row, col, l_col, subgrid_size):
                    grid[row][col] = num
                    if check(grid):
                        return grid
                    else:
                        if filler(grid,subgrid_size):
                            return grid
            break #if no number is found in the row, break the loop and try again with a new number_list
    grid[row][col] = 0

def solver(grid,subgrid_size):
    global counter

    number_list=[*range(1,len(grid)+1)]

    for i in range(len(grid)**2):
        row, col = i//len(grid), i%len(grid)
        if grid[row][col]==0:
            random.shuffle(number_list)
            l_col = [l_row[col] for l_row in grid] #list of column values
            for num in number_list:
                if validator(grid, num, row, col, l_col, subgrid_size):
                    grid[row][col] = num
                    if check(grid):
                        counter += 1
                        break
                    else:
                        if solver(grid,subgrid_size):
                            return grid
            break
    grid[row][col] = 0

def remove(grid, subgrid_size, difficulty_level):
    global counter
    attempts = difficulty_level*(len(grid)//subgrid_size)
    counter = 1
    while attempts > 0:
        row, col = random.randint(0,len(grid)-1), random.randint(0,len(grid)-1)
        while grid[row][col]==0:
            row, col = random.randint(0,len(grid)-1), random.randint(0,len(grid)-1)
        backup, grid[row][col] = grid[row][col], 0
        counter=0
        solver(grid,subgrid_size)

        if counter != 1:
            grid[row][col] = backup
            attempts -= 1

    return grid

#########################################################################
#########################################################################
#########################FUNCTIONS PYGAME################################
#########################################################################

def get_cord(pos, x, y, dif):
    x = pos[0]//dif
    y = pos[1]//dif

    return (x, y)

# Highlight the cell selected
def draw_box(screen, x, y, dif):
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)

# Function to draw required lines for making Sudoku grid        
def draw(screen, dif, grid, grid_size, font1):
    # Draw the lines
        
    for i in range (grid_size):
        for j in range (grid_size):
            if grid[i][j]!= 0:

                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (51, 153, 255), (i * dif, j * dif, dif + 1, dif + 1))
                #(0, 153, 153)
                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    # Draw lines horizontally and verticallyto form grid        
    for i in range(10):
        if (i % (grid_size)**(1/2)) == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)    

# Fill value entered in cell    
def draw_val(screen, val, dif, font1, x, y):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))

# Raise error when wrong value entered
def error1(screen, font1):
    text1 = font1.render("!Aun no has completado el tablero!", 1, (0, 0, 0))
    screen.blit(text1, (20, 600))

def error2(screen, font1):
    text1 = font1.render("No es una entrada válida", 1, (0, 0, 0))
    screen.blit(text1, (20, 600))
# Congratulations
def congratulations(screen, font1):
    vacio = font1.render(" ", 1, (0, 0, 0))
    screen.blit(vacio, (20, 600))
    text = font1.render("Felicidades, lo lograste!!", 1, (0, 0, 0))
    screen.blit(text, (20, 600))    

# Check if the value entered in board is valid
def valid(m, i, j, val,grid_size):
    for it in range(grid_size):
        if m[i][it]== val:
            return False
        if m[it][j]== val:
            return False
    sq = int((grid_size)**(1/2))        
    it = i//sq
    jt = j//sq
    for i in range(it * sq, it * sq + sq):
        for j in range (jt * sq, jt * sq + sq):
            if m[i][j]== val:
                return False
    return True

# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
    min = len(grid) -1
    
    while grid[i][j]!= 0:
        if i<min:
            i+= 1
        elif i == min and j<min:
            i = 0
            j+= 1
        elif i == min and j == min:
            return True
    pygame.event.pump()
    for it in range(1, 10):
        if valid(grid, i, j, it,grid_size)== True:
            grid[i][j]= it
            global x, y #####################################################################################################
            x = i
            y = j
            # white color background\
            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(20)
            if solve(grid, i, j)== 1:
                return True
            else:
                grid[i][j]= 0
            # white color background\
            screen.fill((255, 255, 255))
        
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)
    return False

# Display instruction for the game
def instruction(myname):
    text0 = font2.render("Hola %s, espero que te diviertas jugando"%(myname), 1, (0, 0, 0))
    text1 = font2.render("Presiona D para reiniciar el tablero, R para limpiarlo, S para ", 1, (0, 0, 0))
    text2 = font2.render("que sea resuelto y para validarlo presiona ENTER", 1, (0, 0, 0))
    text3 = font2.render("Recuerda ingresar números en el intervalo [1,9]", 1, (0, 0, 0))

    screen.blit(text0, (10, 520))
    screen.blit(text1, (10, 540))    
    screen.blit(text2, (10, 560))
    screen.blit(text3, (10, 580))
# Display options when solved
def result(myname, grid_size, copy_grid):
    text = font1.render("Esta resuelto!! Presiona R o D", 1, (0, 0, 0))
    screen.blit(text, (20, 600))



#########################################################################
#########################################################################
#########################################################################
#########################################################################



def get_name():

    clear()
    while True:
        name = input('Ingrese su nombre: ')
        if name == '':
            clear()
            print("La entrada no es válida, por favor ingresar una opcion valida")
            continue

        return name

def get_GridSize():

    clear()
    while True:
        try:
            grid_size = int(input('• para sudoku 4x4 con subcuadriculas 2x2 ingrese 4\n• para sudoku 9x9 con subcuadriculas 3x3 ingrese 9\n  Ingrese el tamaño de las celdas del sudoku: '))
            if grid_size not in [4,9]:
                    clear()
                    print("La entrada no es válida, por favor ingresar una opcion valida")
                    continue

        except ValueError:
            clear()
            print("La entrada unicamente puede ser un numero entero, por favor vuelve a intentarlo")
            continue
        
        if grid_size in [4,9]:
            if grid_size == 4:
                return (grid_size,2)
            elif grid_size == 9:
                return (grid_size,3)

def get_difficulty():

    clear()
    while True:
        try:
            difficulty = int(input('Ingrese la dificultad del juego: \n• 1 para facil \n• 2 para medio \n• 3 para dificil \n• 4 para Leyenda\n'))
            if difficulty not in [1,2,3,4]:
                    clear()
                    print("La entrada no es válida, por favor ingresar una opcion valida")
                    continue

        except ValueError:
            clear()
            print("La entrada unicamente puede ser un numero entero, por favor vuelve a intentarlo")
            continue
        
        if difficulty in [1,2,3,4]:
            return difficulty

def get_confirmation(Name, grid_size, difficulty):
    
    clear()

    if difficulty == 1:
        str_difficulty = "Fácil"
    elif difficulty == 2:
        str_difficulty = "Medio"
    elif difficulty == 3:
        str_difficulty = "Dificil"
    elif difficulty == 4:
        str_difficulty = "Leyenda"

    while True:
        try:
            confirmation = int(input('Hola %s \nhas elegido un tablero de %sx%s con dificultad %s\n¿Deseas confirmar tu seleccion?\n• 1 para confirmarla\n• 2 para cambiar tu seleccion\n'%(Name, grid_size, grid_size, str_difficulty)))
            if confirmation not in [1,2]:
                    clear()
                    print("La entrada no es válida, por favor ingresar una opcion valida")
                    continue

        except ValueError:
            clear()
            print("La entrada unicamente puede ser un numero entero, por favor vuelve a intentarlo")
            continue
        
        if confirmation in [1,2]:
            return confirmation


#########################
def sudokuPlay():
    # initialise the pygame font
    pygame.font.init()

    # Total window
    screen = pygame.display.set_mode((500, 650))

    # Title and Icon
    pygame.display.set_caption("SUDOKU")
    img = pygame.image.load('icon.png')
    pygame.display.set_icon(img)

    x = 0
    y = 0
    dif = 500 / grid_size
    val = 0

    # Load test fonts for future use
    font1 = pygame.font.SysFont("comicsans", 30)
    font2 = pygame.font.SysFont("comicsans", 17)

    run = True
    flag1 = 0
    flag2 = 0
    rs = 0
    error = 0
    good = 0
    # The loop thats keep the window running
    while run:
        
        # White color background
        screen.fill((255, 255, 255))
        # Loop through the events stored in event.get()
        for event in pygame.event.get():
            # Quit the game window
            if event.type == pygame.QUIT:
                run = False
            # Get the mouse position to insert number
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag1 = 1
                pos = pygame.mouse.get_pos()
                x, y =get_cord(pos, x, y, dif)
            # Get the number to be inserted if key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x-= 1
                    flag1 = 1
                if event.key == pygame.K_RIGHT:
                    x+= 1
                    flag1 = 1
                if event.key == pygame.K_UP:
                    y-= 1
                    flag1 = 1
                if event.key == pygame.K_DOWN:
                    y+= 1
                    flag1 = 1
                if event.key == pygame.K_1:
                    val = 1
                if event.key == pygame.K_2:
                    val = 2
                if event.key == pygame.K_3:
                    val = 3
                if event.key == pygame.K_4:
                    val = 4
                if event.key == pygame.K_5:
                    val = 5
                if event.key == pygame.K_6:
                    val = 6
                if event.key == pygame.K_7:
                    val = 7
                if event.key == pygame.K_8:
                    val = 8
                if event.key == pygame.K_9:
                    val = 9
                if event.key == pygame.K_RETURN:
                    if check(grid):
                        good = 1
                    else: 
                        error = 1    
                            
                # If S pressed solves the board    
                if event.key == pygame.K_s:
                    flag2 = 1
                # If R pressed clear the sudoku board
                if event.key == pygame.K_r:
                    rs = 0
                    error = 0
                    flag2 = 0
                    grid =[[0]*grid_size for i in range(grid_size)]
                # If D is pressed reset the board to default
                if event.key == pygame.K_d:
                    rs = 0
                    error = 0
                    flag2 = 0
                    grid = copy_grid
        if flag2 == 1:
            if solve(grid, 0, 0)== False:
                error = 1
            else:
                rs = 1
            flag2 = 0
        if val != 0:        
            draw_val(val)
            # print(x)
            # print(y)
            if valid(grid, int(x), int(y), val,grid_size)== True:
                grid[int(x)][int(y)]= val
                flag1 = 0
            else:
                grid[int(x)][int(y)]= 0
                error2()
            val = 0
        
        if error == 1:
            error1()
        if good == 1:
            congratulations()    
        if rs == 1:
            result(myname, grid_size, copy_grid)    
        draw()
        if flag1 == 1:
            draw_box()    
        instruction(myname)

        # Update window
        pygame.display.update()

    # Quit pygame window
    pygame.quit()
#########################


def run():
    
    clear()
    while True:

        name = get_name()

        grid_size, subgrid_size = get_GridSize()

        difficulty = get_difficulty()
        
        confirmation = get_confirmation()

        if confirmation == 1:
            clear()
            break
        else:
            clear()
            continue


    zero_grid=[[0]*grid_size for _ in range(grid_size)]

    fully_grid=filler(zero_grid,subgrid_size)

    ready_grid=remove(fully_grid,subgrid_size,difficulty)

    sudokuPlay(ready_grid,name,grid_size,subgrid_size)

if __name__ == "__main__":
    run()