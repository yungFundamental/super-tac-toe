import pygame
import cell
import board
import socket
import threading
import bot


mode_dict = {"exit": -1, "host": 0, "connect": 1, "friend": 2, "bot": 3}
running = False
user_turn = True
first_turn = True
next_big_index = 10     # index of the board that the player must pick a cell from, insignificant until second turn


def index_to_coords(index):
    if int(index/3) == 0:
        coordinates = "top "
    elif int(index / 3) == 1:
        coordinates = "middle "
    elif int(index / 3) == 2:
        coordinates = "bottom "
    else:
        coordinates = "\"unknown height\", "

    if index % 3 == 0:
        coordinates += "left"
    elif index % 3 == 1:
        coordinates += "middle"
    elif index % 3 == 2:
        coordinates += "right"
    else:
        coordinates += "\"unknown side\""

    return coordinates


def get_mode():
    print("Please enter the corresponding number of the mode you want to play.")
    while True:
        option = input("Options:\nhost a game : 1 | connect to a host : 2 | play against"
                       " a bot : 3 | offline multiplayer : 4 | exit : 5\n")

        if option == "1":
            return mode_dict["host"]
        if option == "2":
            return mode_dict["connect"]
        if option == "3":
            return mode_dict["bot"]
        if option == "4":
            return mode_dict["friend"]
        if option == "5":
            return mode_dict["exit"]

        print("Undefined option, please try again.")


def local_turn(main_board, x, y):
    if main_board.find(x, y) is not None:
        big_i, small_i = main_board.find(x, y)
        if main_board.cells[big_i].cells[small_i].id == cell.XO.blank:
            return big_i, small_i
    return None, None


def turn_recv(sock):
    big_i, small_i = tuple(filter(None, sock.recv(1024).decode("utf-8").split(';')))
    return int(big_i), int(small_i)


def turn_send(main_board, x, y, sock):
    big_i, small_i = local_turn(main_board, x, y)
    if big_i is not None and small_i is not None:
        sock.send(bytes(f"{big_i};{small_i}", "utf-8"))
    return big_i, small_i


def online_manager(main_board, sock, opponent_shape):
    global first_turn
    global running
    global next_big_index
    global user_turn
    while running:
        while user_turn and running:
            pass
        if not user_turn:
            big_i, small_i = turn_recv(sock)
            if first_turn or main_board.cells[next_big_index].full() or big_i is next_big_index:
                user_turn = main_board.choose(big_i, small_i, opponent_shape)
                next_big_index = small_i
                first_turn = False
                print(f"Waiting for your move, "
                      f"board {index_to_coords(next_big_index)}")

    sock.close()


# infinite loop which manages turns (user turn, opponent turn, user turn, opponent turn...)
# user_shape is added even though it should be obvious from the fact that we are first so that it would be easy to make
# it so that o will start
# def turn_manager(main_board, user_turn_func, opponent_turn_func, user_first=True, user_shape=cell.XO.x):
#     global user_turn
#     user_turn = user_first
#     if user_first:
#         big_i, small_i = first_turn(main_board, user_turn_func, user_shape)
#     else:
#         big_i, small_i = first_turn(main_board, opponent_turn_func, cell.reverse(user_shape))
#     user_turn = not user_turn
#
#     while True:
#         if user_turn:
#             # user turn:
#             while True:
#                 big_index, small_index = user_turn_func()
#                 # check if a proper has been carried out:
#                 # if there is an open spot in the board the player is supposed to pick from, the cell chosen has to be
#                 # from that board
#                 if not main_board.cells[big_i].full():
#                     if big_index is not small_i:    # includes big_index is None
#                         continue
#                 status = main_board.choose(big_index, small_index, user_shape)
#                 if not status:   # if the cell is taken
#                     continue
#                 small_i = big_index
#                 # turn has been used
#                 user_turn = False
#         else:
#             # opponent turn:
#             # NOTE: if the opponent turn function is a recv function then the function will automatically stop the
#             # thread process until the turn is carried out, the infinite loop is insignificant. In addition, the checks
#             # are insignificant as well since it should be
#             while True:
#                 big_index, small_index = opponent_turn_func()
#                 # check if a proper turn has been carried out
#                 if big_index is not small_i:    # includes big_index is None
#                     continue
#                 status = main_board.choose(big_index, small_index, user_shape)
#                 if not status:  # if the cell is taken
#                     continue
#                 small_i = big_index
#                 # turn has been used
#                 user_turn = True
#         if main_board.full() or main_board.winner():
#             return
def game():
    global user_turn
    global next_big_index
    global running
    global first_turn
    mode = get_mode()
    if mode == mode_dict["exit"]:
        return 0

    if mode == mode_dict["host"]:
        # Create host socket
        port = 8080
        ip = socket.gethostbyname(socket.gethostname())
        server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_s.bind(('127.0.0.1', port))
        # Connect
        server_s.listen(1)
        print(f"TCP server socket on ip: {ip}, port: {port}, \nWaiting for connection...")
        (client_socket, opponent_ip) = server_s.accept()
        print(f"Connected from: {opponent_ip}")

        # The host is 'x' and goes first
        user_shape = cell.XO.x
        user_turn = True

    elif mode == mode_dict["connect"]:
        # Create client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect
        print("Please enter the information of the host:")
        ip = input("IP: ")
        port = int(input("port: "))
        print(f"Connecting to {ip}:{port}...")
        client_socket.connect((ip, port))
        print("Connected.")
        # Client is 'o' and goes second
        user_shape = cell.XO.o
        user_turn = False

    elif mode == mode_dict["friend"]:
        # The 'o' player will act as the opponent in this code so our_shape is 'x'
        user_shape = cell.XO.x
        user_turn = True

    elif mode == mode_dict["bot"]:
        # The 'o' player will be the bot so our_shape is 'x'
        user_shape = cell.XO.x
        user_turn = True
        buf = input("Please enter the maximum depth of the game tree (else write \"default\"): ")
        if buf.isnumeric():
            bot.max_depth = int(buf)
        else:
            print(f"max_depth gets the default value of {bot.max_depth}")
        buf = input("Show number of nodes created? (y/n):")
        if buf == 'y':
            bot.show_counter = True

    # Initialization
    print("\nLoading game...")
    pygame.init()
    # Images
    icon = pygame.image.load("pics/icon.png")
    big_tac_toe = pygame.image.load("pics/big_tic_tac.jpg")
    small_tac_toe = pygame.image.load("pics/small_tic_tac.jpg")
    small_x = pygame.image.load("pics/small_red_x.png")
    small_o = pygame.image.load("pics/small_blue_o.png")
    big_x = pygame.image.load("pics/big_red_x.png")
    big_o = pygame.image.load("pics/big_blue_o.png")
    small_line_dia_l = pygame.image.load("pics/line/small/diagonal_l.png")
    small_line_dia_r = pygame.image.load("pics/line/small/diagonal_r.png")
    small_line_hor = pygame.image.load("pics/line/small/horizontal.png")
    small_line_ver = pygame.image.load("pics/line/small/vertical.png")
    big_line_dia_l = pygame.image.load("pics/line/big/diagonal_l.png")
    big_line_dia_r = pygame.image.load("pics/line/big/diagonal_r.png")
    big_line_hor = pygame.image.load("pics/line/big/horizontal.png")
    big_line_ver = pygame.image.load("pics/line/big/vertical.png")

    # Transparency
    small_tac_toe.set_colorkey((255, 255, 255))
    small_x.set_colorkey((255, 255, 255))
    small_o.set_colorkey((255, 255, 255))
    big_x.set_colorkey((255, 255, 255))
    big_o.set_colorkey((255, 255, 255))
    small_line_hor.set_colorkey((255, 255, 255))
    small_line_ver.set_colorkey((255, 255, 255))
    small_line_dia_l.set_colorkey((255, 255, 255))
    small_line_dia_r.set_colorkey((255, 255, 255))
    big_line_hor.set_colorkey((255, 255, 255))
    big_line_ver.set_colorkey((255, 255, 255))
    big_line_dia_l.set_colorkey((255, 255, 255))
    big_line_dia_r.set_colorkey((255, 255, 255))

    # Open Screen
    dimension_y = 600
    dimension_x = 700
    screen = pygame.display.set_mode((dimension_x, dimension_y))
    caption = "SuperTacToe"
    if mode != mode_dict["friend"]:
        caption += f" - {user_shape.name}"
    pygame.display.set_caption(caption)
    pygame.display.set_icon(icon)

    main_board = board.BigBoard(0, 0, 241, 207, big_tac_toe, big_x, big_o, big_line_hor, big_line_ver, big_line_dia_l,
                                big_line_dia_r, small_tac_toe, small_x, small_o, small_line_hor,
                                small_line_ver, small_line_dia_l, small_line_dia_r)

    running = True
    if mode == mode_dict["host"] or mode == mode_dict["connect"]:
        # if online, create a receiving thread - receives input from socket during opponent turn
        receiving_thread = threading.Thread(target=online_manager, args=(main_board, client_socket,
                                                                      cell.reverse(user_shape)))

        if user_turn:
            buf1 = "first"
        else:
            buf1 = "second"
        print(f"You are {buf1}, your shape is {user_shape.name}")
        receiving_thread.start()

    game_over = False
    while running:
        main_board.winner()
        show_score = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                if mode == mode_dict["host"] or mode == mode_dict["connect"]:
                    receiving_thread.join()

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_m]:
                    show_score = True

            if main_board.won[0] == cell.XO.blank and not main_board.full():
                if user_turn:
                    if event.type == pygame.MOUSEBUTTONUP:
                        x, y = pygame.mouse.get_pos()
                        if mode == mode_dict["connect"] or mode == mode_dict["host"]:   # online
                            big_i, small_i = turn_send(main_board, x, y, client_socket)
                        else:
                            big_i, small_i = local_turn(main_board, x, y)
                        if big_i is not None and small_i is not None:
                            if first_turn or main_board.cells[next_big_index].full() or big_i is next_big_index:
                                user_turn = not main_board.choose(big_i, small_i, user_shape)
                                next_big_index = small_i
                                first_turn = False
                                if mode == mode_dict["friend"]:
                                    print(f"Waiting for {cell.reverse(user_shape).name}, "
                                          f"board {index_to_coords(next_big_index)}")
                                big_i = None
                                small_i = None
                else:
                    # opponent turn: if online, let the thread handle it
                    if mode is not mode_dict["connect"] and mode is not mode_dict["host"]:
                        if mode == mode_dict["bot"]:
                            big_i, small_i = bot.bot_move(main_board, cell.reverse(user_shape), next_big_index,
                                                          not first_turn)

                        elif mode == mode_dict["friend"]:
                            if event.type == pygame.MOUSEBUTTONUP:
                                x, y = pygame.mouse.get_pos()
                                big_i, small_i = local_turn(main_board, x, y)
                        if big_i is not None and small_i is not None:
                            if first_turn or main_board.cells[next_big_index].full() or big_i is next_big_index:
                                user_turn = main_board.choose(big_i, small_i, cell.reverse(user_shape))
                                next_big_index = small_i
                                first_turn = False
                                print(f"Waiting for {user_shape.name}, "
                                      f"board {index_to_coords(next_big_index)}")
                                big_i = None
                                small_i = None
            elif not game_over:
                # exit screen, keep drawing until the user wants to exit the board
                if main_board.won[0] != cell.XO.blank:
                    print(main_board.won[0].name + " wins!")
                elif main_board.full():
                    print("It's a tie!")

                game_over = True

            screen.fill((255, 255, 255))
            main_board.draw(screen, show_score)
            pygame.display.update()

    return 0




