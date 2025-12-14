import pygame


def draw_():
    screen.blit(bigtactoe, (0, 0))
    for i in range(0, 720, 241):
        for j in range(0, 600, 207):
            screen.blit(smalltactoe, (i, j))


def draw():
    screen.blit(bigtactoe, (0, 0))

    screen.blit(smalltactoe, (0, 0))
    screen.blit(smalltactoe, (241, 0))
    screen.blit(smalltactoe, (482, 0))

    screen.blit(smalltactoe, (0, 206))
    screen.blit(smalltactoe, (240, 206))
    screen.blit(smalltactoe, (480, 206))

    screen.blit(smalltactoe, (0, 410))
    screen.blit(smalltactoe, (240, 410))
    screen.blit(smalltactoe, (480, 410))

    screen.blit(small_x, (10, 0))       # top left, top left
    screen.blit(small_o, (160, 126))    # top left, bottom right
    screen.blit(small_x, (480, 410))    # bottom right, top left
    screen.blit(small_o, (10, 126))     # top right, bottom left
    screen.blit(small_x, (10, 540))     # bottom left, bottom left
    screen.blit(small_o, (10, 410))     # bottom left, top left
    screen.blit(small_x, (80, 0))       # top left, top middle
    screen.blit(small_o, (250, 0))      # top middle, top left
    screen.blit(small_x, (150, 0))      # top left, top right

    screen.blit(line_hor, (0, 0))

    screen.blit(small_o, (490, 60))         # top right, middle left
    screen.blit(small_x, (80, 210))         # middle left, top middle
    screen.blit(small_o, (250, 0+60))       # top middle, middle left
    screen.blit(small_x, (80, 210+60))      # middle left, middle middle
    screen.blit(small_o, (240, 270))        # middle middle, middle left
    screen.blit(small_x, (80, 210 + 120))  # middle left, top middle

    screen.blit(line_ver, (70, 210))
    
    # screen.blit(small_x, (320, 270))    # middle middle, middle middle
    # screen.blit(small_o, (319, 208))    # middle middle, top middle
    # screen.blit(small_x, (319, 60))     # top middle, middle middle

    # screen.blit(small_x, (160, 126))  # top left, bottom right
    # screen.blit(small_o, (480, 410))  # bottom right, top left



# Initialization
pygame.init()
icon = pygame.image.load("pics/icon.png")
bigtactoe = pygame.image.load("pics/big_tic_tac.jpg")
smalltactoe = pygame.image.load("pics/small_tic_tac.jpg")
small_x = pygame.image.load("pics/small_red_x.png")
small_o = pygame.image.load("pics/small_blue_o.png")
line_dia_l = pygame.image.load("pics/line_diagonal_l.png")
line_dia_r = pygame.image.load("pics/line_diagonal_r.png")
line_hor = pygame.image.load("pics/line_horizontal.png")
line_ver = pygame.image.load("pics/line_vertical.png")
smalltactoe.set_colorkey((255, 255, 255))
small_x.set_colorkey((255, 255, 255))
small_o.set_colorkey((255, 255, 255))
line_hor.set_colorkey((255, 255, 255))
line_ver.set_colorkey((255, 255, 255))
line_dia_l.set_colorkey((255, 255, 255))
line_dia_r.set_colorkey((255, 255, 255))


# Open screen
dimensionY = 600
dimensionX = 900
screen = pygame.display.set_mode((dimensionX, dimensionY))
pygame.display.set_caption("Ulitmate Tic Tac Toe - X")
pygame.display.set_icon(icon)

running = True
while running:
    for event in pygame.event.get():
        show_score = False
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_m]:
                show_score = True

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)


        screen.fill((255, 255, 255))
        draw_()
        # big_board.draw(screen, show_score)
        pygame.display.update()




