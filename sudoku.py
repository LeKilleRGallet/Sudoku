import pygame
import os
import random
from datetime import datetime
from math import e
import time


class Found(Exception):
    pass

def clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system("cls")

def exit_game():
    clear()
    pygame.quit()
    raise SystemExit('Gracias por jugar')

def saving():##
    for i in range(30):##
        if i%4==0:##
            r='/'##
        elif i%4==1:##
            r='—'##
        elif i%4==2:##
            r='\\'##
        elif i%4==3:##
            r='|'##
        print('\t\tGuardando...' + r,end='\r')##
        time.sleep(0.1)##

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
def draw(screen, dif, grid, font1):
    # Draw the lines
        
    for i in range (len(grid)):
        for j in range (len(grid)):
            if grid[i][j]!= 0:

                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (51, 153, 255), (i * dif, j * dif, dif + 1, dif + 1))
                #(0, 153, 153)
                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    # Draw lines horizontally and verticallyto form grid        
    for i in range(10):
        if (i % (len(grid))**(1/2)) == 0:
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
def valid(grid, q, p, val):
    for k in range(len(grid)):
        if grid[q][k]== val:
            return False
        if grid[k][p]== val:
            return False
    sq = int((len(grid))**(1/2))        
    it = q//sq
    jt = p//sq
    for i in range(it * sq, it * sq + sq):
        for j in range (jt * sq, jt * sq + sq):
            if grid[i][j]== val:
                return False
    return True

# Solves the sudoku board using Backtracking Algorithm
def solve(grid, screen, dif, font1, i=0, j=0):
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
        if valid(grid, i, j, it)== True:
            grid[i][j]= it
            global x, y
            x = i
            y = j
            # white color background\
            screen.fill((255, 255, 255))
            draw(screen, dif, grid, font1)
            draw_box(screen, x, y, dif)
            pygame.display.update()
            pygame.time.delay(20)
            if solve(grid, screen, dif, font1, i, j)== 1:
                return True
            else:
                grid[i][j]= 0
            # white color background\
            screen.fill((255, 255, 255))
        
            draw(screen, dif, grid, font1)
            draw_box(screen, x, y, dif)
            pygame.display.update()
            pygame.time.delay(50)
    return False

# Display instruction for the game
def instruction(name, font2, screen):
    text0 = font2.render("Hola %s, espero que te diviertas jugando"%(name), 1, (0, 0, 0))
    text1 = font2.render("Presiona D para reiniciar el tablero, R para limpiarlo, S para ", 1, (0, 0, 0))
    text2 = font2.render("que sea resuelto, E para salir y para validarlo presiona ENTER", 1, (0, 0, 0))

    screen.blit(text0, (10, 520))
    screen.blit(text1, (10, 540))    
    screen.blit(text2, (10, 560))
# Display options when solved
def result(font1, screen):
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
def sudokuPlay(grid, name, copy_grid):
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
    dif = 500 / len(grid)
    val = 0

    # Load test fonts for future use
    font1 = pygame.font.SysFont("comicsans", 30)
    font2 = pygame.font.SysFont("comicsans", 17)

    flag1 = 0
    flag2 = 0
    rs = 0
    error = 0
    good = 0
    errors=0
    kirito = False
    # The loop thats keep the window running
    while True:
        
        # White color background
        screen.fill((255, 255, 255))
        # Loop through the events stored in event.get()
        for event in pygame.event.get():
            # Quit the game window
            if event.type == pygame.QUIT:
                exit_game()
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
                    grid =[[0]*len(grid) for i in range(len(grid))]
                # If D is pressed reset the board to default
                if event.key == pygame.K_d:
                    rs = 0
                    error = 0
                    flag2 = 0
                    grid = copy_grid
                 # IF E is pressed exit the game
                if event.key == pygame.K_e:
                        exit_game()
        if flag2 == 1:
            kirito = True
            if solve(grid, screen, dif, font1)== False:
                error = 1
            else:
                rs = 1
            flag2 = 0
        if val != 0 and val <= len(grid):
            draw_val(screen, val, dif, font1, x, y)
            # print(x)
            # print(y)
            if copy_grid[int(x)][int(y)] == 0:##avoid to insert a number in a base cell
                if valid(grid, int(x), int(y), val)== True:
                    grid[int(x)][int(y)]= val
                    flag1 = 0
                else:
                    grid[int(x)][int(y)]= 0
                    errors +=1
                    error2(screen, font1)
                val = 0
            else:
                val = 0
        
        if error == 1:
            error1(screen, font1)
        if good == 1:
            congratulations(screen, font1)
            end_time = datetime.now()
            break
        if rs == 1:
            result(font1, screen)
        draw(screen, dif, grid, font1)
        if flag1 == 1:
            draw_box(screen, x, y, dif)
        instruction(name, font2, screen)

        # Update window
        pygame.display.update()

    # Quit pygame window
    pygame.quit()

    return (end_time, errors, kirito)
    
#########################

def get_score(time, difficulty, size, errors):

    time_multiplier = 1
    max_time_for_bonus = ((((size)+(e**((size**(1/2))+(size/3))))**(1/2))-(4/difficulty))*60
    if time < max_time_for_bonus:
        time_multiplier = 1.1
        excess_time = max_time_for_bonus-time
        time_multiplier += excess_time*0.0025

    score = ((100000000*difficulty*size)/time)-(errors*50)*time_multiplier
    score = int(score)
    if score > 0:
        return score
    else:
        return 0

def save_score(name, score):

    while True:
        try:
            confirmation = int(input('Tu puntuacion es %s\n¿Deseas guardarla?\n• 1 para guardarla\n• 2 para no guardarla\n'%(score)))##
            if confirmation==1:
                with open('scores.txt', 'a') as file:
                    file.write(name + ' ' + str(score) + '\n')
                    saving()##
                    break
            elif confirmation==2:
                reconfirmation = int(input('¿Estas seguro que deseas no guardar la puntuacion? \n• 1 para no confirmar no guardarla\n• 2 para guardar'))
                if reconfirmation==1:
                    break
                elif reconfirmation==2:
                    with open('scores.txt', 'a') as file:
                        file.write(name + '\t' + str(score) + '\n')
                        saving()
                        break
                else:
                    print("La entrada no es válida, por favor ingresar una opcion valida")
                    continue
            else:
                print("La entrada no es válida, por favor ingresar una opcion valida")
                continue
        except ValueError:
            print('La entrada unicamente puede ser un numero entero, por favor vuelve a intentarlo')
            continue

def play():

    clear()
    while True:

        name = get_name()
        grid_size, subgrid_size = get_GridSize()
        difficulty = get_difficulty()
        confirmation = get_confirmation(name, grid_size, difficulty)
        if confirmation == 1:
            clear()
            break
        else:
            clear()
            continue

    zero_grid=[[0]*grid_size for _ in range(grid_size)]
    fully_grid=filler(zero_grid,subgrid_size)
    ready_grid=remove(fully_grid,subgrid_size,difficulty)
    start_time=datetime.now()
    copy_grid=[_[:] for _ in ready_grid]
    end_time, errors, kirito = sudokuPlay(ready_grid,name,copy_grid)
    total_time= end_time - start_time
    score=get_score(total_time.seconds, difficulty, grid_size, errors)

    if kirito==False:
        clear()
        print('Felicitaciones %s completaste el sudoku %sx%s en %s minutos y %s segundos'%(name, grid_size, grid_size, total_time.seconds//60, total_time.seconds%60))
        save_score(name, score)

def show_highscore():

    clear()
    print('Puntuaciones:\n')
    print(f'{("Nombre".center(20))}\t\t{("Puntuacion".center(40))}')
    print('-'*70)
    with open('scores.txt', 'r') as file:
        lines = file.readlines()
        lines.sort(key=lambda x: int(x.split()[1]), reverse=True)
        file.close()
        for i, line in enumerate(lines):
            print(f'{i+1:>3}. {line.split()[0]:<30} \t\t{line.split()[1]:<10}')
    
    print('\n')
    cnt=input('Presione enter para continuar\t')
    if cnt == 'Hack_Clear_File':
        with open('scores.txt', 'w') as file:
            file.write('')
            file.close()
        print('Archivo borrado')
        cnt=input('Presione enter para continuar')


def run():

    while True:
        clear()
        print('Bienvenido al juego de Sudoku\n')
        print('1. Jugar\n')
        print('2. Ver puntuaciones\n')
        print('3. Salir\n')
        try:
            option = int(input('Ingrese una opcion: '))
            if option == 1:
                play()
            elif option == 2:
                clear()
                show_highscore()

            elif option == 3:
                clear()
                exit_game()
            else:
                print('La opcion ingresada no es valida, por favor ingrese una opcion valida')
                continue
        except ValueError:
            print('La entrada unicamente puede ser un numero entero, por favor vuelve a intentarlo')
            continue

if __name__ == "__main__":
    run()