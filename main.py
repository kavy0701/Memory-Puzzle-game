import pygame
import sys

class Option:

    hovered = False
    
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()
            
    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)
        
    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (255, 255, 255)
        else:
            return (100, 100, 100)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

pygame.init()
screen = pygame.display.set_mode((640,480))

font_color = (255, 255, 250)
font_obj = pygame.font.Font("C:\Windows\Fonts\segoeprb.ttf",30)

# # Render the objects
text_obj=font_obj.render("Welcome to Memory Puzzle",True,font_color)

menu_font = pygame.font.Font("C:\Windows\Fonts\segoeprb.ttf", 25)
options = [Option("NEW GAME", (245,185)), Option("HIGH SCORE", (235,265)),
           Option("QUIT", (285,340))]
while True:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 285 <= mouse[0] and 340 <= mouse[1]: 
                pygame.quit() 
                sys.exit() 
            elif 235 <= mouse[0] and 265 <= mouse[1]:
                screen1 = pygame.display.set_mode((640,480))
                while True:
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    screen1.fill((0,0,0))
                    pygame.display.update()



            elif 245 <= mouse[0] and 185 <= mouse[1]:
                import random, pygame, sys
                import pygame.freetype
                from pygame.locals import *


                FPS = 30 # frames per second, the general speed of the program
                WINDOW_WIDTH = 640 # size of window's width in pixels
                WINDOW_HEIGHT = 480 # size of windows' height in pixels
                REVEAL_SPEED = 8 # speed boxes' sliding reveals and covers
                BOX_SIZE = 40 # size of box height & width in pixels
                GAP_SIZE = 10 # size of gap between boxes in pixels
                BOARD_WIDTH = 10 # number of columns of icons
                BOARD_HEIGHT = 7 # number of rows of icons
                assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
                XMARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
                YMARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)


                #            R    G    B
                GRAY     = (100, 100, 100)
                NAVYBLUE = ( 60,  60, 100)
                WHITE    = (255, 255, 255)
                RED      = (255,   0,   0)
                GREEN    = (  0, 255,   0)
                BLUE     = (  0,   0, 255)
                YELLOW   = (255, 255,   0)
                ORANGE   = (255, 128,   0)
                PURPLE   = (255,   0, 255)
                CYAN     = (  0, 255, 255)


                ICON = pygame.image.load('icon.png')
                BACKGROUND_IMAGE = pygame.image.load('BGG.png')


                BGCOLOR = NAVYBLUE
                LIGHTBGCOLOR = GRAY
                BOXCOLOR = WHITE
                HIGHLIGHTCOLOR = BLUE


                DONUT = 'donut'
                SQUARE = 'square'
                DIAMOND = 'diamond'
                LINES = 'lines'
                OVAL = 'oval'


                ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
                ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
                assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT, "Board is too big for the number of shapes/colors defined."


                def main():
                    global FPSCLOCK, DISPLAY_SURFACE
                    pygame.init()
                    FPSCLOCK = pygame.time.Clock()
                    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

                    clock = pygame.time.Clock()
                    font = pygame.freetype.SysFont(None, 25)
                    font.origin = True
                    
                    score_value = 0
                    
                    font_obj = pygame.font.Font("C:\Windows\Fonts\ARLRDBD.ttf", 25) 
                    
                    mousex = 0 # used to store x coordinate of mouse event
                    mousey = 0 # used to store y coordinate of mouse event
                    pygame.display.set_caption('Memory Game')
                    pygame.display.set_icon(ICON)

                    mainBoard = getRandomizedBoard()
                    revealedBoxes = generateRevealedBoxesData(False)

                    firstSelection = None # stores the (x, y) of the first box clicked.

                    DISPLAY_SURFACE.blit(BACKGROUND_IMAGE, [0, 0])
                    startGameAnimation(mainBoard)
    

                    while True: # main game loop
                        mouseClicked = False
                        DISPLAY_SURFACE.blit(BACKGROUND_IMAGE, [0, 0])
                        
                        drawBoard(mainBoard, revealedBoxes)

                        text_obj = font_obj.render("Score: "+ str(score_value), True, (255, 255, 255))
                        DISPLAY_SURFACE.blit(text_obj, (70, 12))

                        ticks = pygame.time.get_ticks()
                        seconds = int(ticks/1000 % 60)
                        minutes = int(ticks/60000 % 24)
                        out = '{minutes:02d}:{seconds:02d}'.format(minutes = minutes, seconds = seconds)
                        font.render_to(DISPLAY_SURFACE, (500, 35), out, pygame.Color('white'))
                        pygame.display.flip()
                        clock.tick(60)


                        for event in pygame.event.get(): # event handling loop
                            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                                pygame.quit()
                                sys.exit()
                            elif event.type == MOUSEMOTION:
                                mousex, mousey = event.pos
                            elif event.type == MOUSEBUTTONUP:
                                mousex, mousey = event.pos
                                mouseClicked = True

                        boxx, boxy = getBoxAtPixel(mousex, mousey)
                        if boxx != None and boxy != None:
                            # The mouse is currently over a box.
                            if not revealedBoxes[boxx][boxy]:
                                drawHighlightBox(boxx, boxy)
                            if not revealedBoxes[boxx][boxy] and mouseClicked:
                                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                                revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                                if firstSelection == None: # the current box was the first box clicked
                                    firstSelection = (boxx, boxy)
                                    score_value += 1
                                else: # the current box was the second box clicked
                                    # Check if there is a match between the two icons.
                                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                                    if icon1shape != icon2shape or icon1color != icon2color:
                                        # Icons don't match. Re-cover up both selections.
                                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                                        revealedBoxes[boxx][boxy] = False
                                        score_value -=1
                                    elif hasWon(revealedBoxes): # check if all pairs found
                                        gameWonAnimation(mainBoard)
                                        pygame.time.wait(2000)

                                        # Reset the board
                                        mainBoard = getRandomizedBoard()
                                        revealedBoxes = generateRevealedBoxesData(False)

                                        # Show the fully unrevealed board for a second.
                                        drawBoard(mainBoard, revealedBoxes)
                                        pygame.display.update()
                                        pygame.time.wait(1000)

                                        # Replay the start game animation.
                                        startGameAnimation(mainBoard)
                                    firstSelection = None # reset firstSelection variable

                        # Redraw the screen and wait a clock tick.
                        pygame.display.update()
                        FPSCLOCK.tick(FPS)


                def generateRevealedBoxesData(val):
                    revealedBoxes = []
                    for i in range(BOARD_WIDTH):
                        revealedBoxes.append([val] * BOARD_HEIGHT)
                    return revealedBoxes


                def getRandomizedBoard():
                    # Get a list of every possible shape in every possible color.
                    icons = []
                    for color in ALLCOLORS:
                        for shape in ALLSHAPES:
                            icons.append( (shape, color) )

                    random.shuffle(icons) # randomize the order of the icons list
                    numIconsUsed = int(BOARD_WIDTH * BOARD_HEIGHT / 2) # calculate how many icons are needed
                    icons = icons[:numIconsUsed] * 2 # make two of each
                    random.shuffle(icons)

                    # Create the board data structure, with randomly placed icons.
                    board = []
                    for x in range(BOARD_WIDTH):
                        column = []
                        for y in range(BOARD_HEIGHT):
                            column.append(icons[0])
                            del icons[0] # remove the icons as we assign them
                        board.append(column)
                    return board


                def splitIntoGroupsOf(groupSize, theList):
                    # splits a list into a list of lists, where the inner lists have at
                    # most groupSize number of items.
                    result = []
                    for i in range(0, len(theList), groupSize):
                        result.append(theList[i:i + groupSize])
                    return result


                def leftTopCoordsOfBox(boxx, boxy):
                    # Convert board coordinates to pixel coordinates
                    left = boxx * (BOX_SIZE + GAP_SIZE) + XMARGIN
                    top = boxy * (BOX_SIZE + GAP_SIZE) + YMARGIN
                    return (left, top)


                def getBoxAtPixel(x, y):
                    for boxx in range(BOARD_WIDTH):
                        for boxy in range(BOARD_HEIGHT):
                            left, top = leftTopCoordsOfBox(boxx, boxy)
                            boxRect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
                            if boxRect.collidepoint(x, y):
                                return (boxx, boxy)
                    return (None, None)


                def drawIcon(shape, color, boxx, boxy):
                    quarter = int(BOX_SIZE * 0.25) # syntactic sugar
                    half =    int(BOX_SIZE * 0.5)  # syntactic sugar

                    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
                    # Draw the shapes
                    if shape == DONUT:
                        pygame.draw.circle(DISPLAY_SURFACE, color, (left + half, top + half), half - 5)
                        pygame.draw.circle(DISPLAY_SURFACE, BGCOLOR, (left + half, top + half), quarter - 5)
                    elif shape == SQUARE:
                        pygame.draw.rect(DISPLAY_SURFACE, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
                    elif shape == DIAMOND:
                        pygame.draw.polygon(DISPLAY_SURFACE, color, ((left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), (left, top + half)))
                    elif shape == LINES:
                        for i in range(0, BOX_SIZE, 4):
                            pygame.draw.line(DISPLAY_SURFACE, color, (left, top + i), (left + i, top))
                            pygame.draw.line(DISPLAY_SURFACE, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))
                    elif shape == OVAL:
                        pygame.draw.ellipse(DISPLAY_SURFACE, color, (left, top + quarter, BOX_SIZE, half))


                def getShapeAndColor(board, boxx, boxy):
                    # shape value for x, y spot is stored in board[x][y][0]
                    # color value for x, y spot is stored in board[x][y][1]
                    return board[boxx][boxy][0], board[boxx][boxy][1]


                def drawBoxCovers(board, boxes, coverage):
                    # Draws boxes being covered/revealed. "boxes" is a list
                    # of two-item lists, which have the x & y spot of the box.
                    for box in boxes:
                        left, top = leftTopCoordsOfBox(box[0], box[1])
                        pygame.draw.rect(DISPLAY_SURFACE,BGCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
                        shape, color = getShapeAndColor(board, box[0], box[1])
                        drawIcon(shape, color, box[0], box[1])
                        if coverage > 0: # only draw the cover if there is an coverage
                            pygame.draw.rect(DISPLAY_SURFACE, BOXCOLOR, (left, top, coverage, BOX_SIZE))
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)


                def revealBoxesAnimation(board, boxesToReveal):
                    # Do the "box reveal" animation.
                    for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, -REVEAL_SPEED):
                        drawBoxCovers(board, boxesToReveal, coverage)
                        

                def coverBoxesAnimation(board, boxesToCover):
                    # Do the "box cover" animation.
                    for coverage in range(0, BOX_SIZE + REVEAL_SPEED, REVEAL_SPEED):
                        drawBoxCovers(board, boxesToCover, coverage)


                def drawBoard(board, revealed):
                    # Draws all of the boxes in their covered or revealed state.
                    for boxx in range(BOARD_WIDTH):
                        for boxy in range(BOARD_HEIGHT):
                            left, top = leftTopCoordsOfBox(boxx, boxy)
                            if not revealed[boxx][boxy]:
                                # Draw a covered box.
                                pygame.draw.rect(DISPLAY_SURFACE, BOXCOLOR, (left, top, BOX_SIZE, BOX_SIZE))
                            else:
                                # Draw the (revealed) icon.
                                shape, color = getShapeAndColor(board, boxx, boxy)
                                drawIcon(shape, color, boxx, boxy)


                def drawHighlightBox(boxx, boxy):
                    left, top = leftTopCoordsOfBox(boxx, boxy)
                    pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHTCOLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 4)


                def startGameAnimation(board):
                    # Randomly reveal the boxes 8 at a time.
                    coveredBoxes = generateRevealedBoxesData(False)
                    boxes = []
                    for x in range(BOARD_WIDTH):
                        for y in range(BOARD_HEIGHT):
                            boxes.append( (x, y) )
                    random.shuffle(boxes)
                    boxGroups = splitIntoGroupsOf(8, boxes)

                    drawBoard(board, coveredBoxes)
                    for boxGroup in boxGroups:
                        revealBoxesAnimation(board, boxGroup)
                        coverBoxesAnimation(board, boxGroup)


                def gameWonAnimation(board):
                    # flash the background color when the player has won
                    coveredBoxes = generateRevealedBoxesData(True)
                    color1 = LIGHTBGCOLOR
                    color2 = BGCOLOR

                    for i in range(13):
                        color1, color2 = color2, color1 # swap colors
                        DISPLAY_SURFACE.fill(color1)
                        drawBoard(board, coveredBoxes)
                        pygame.display.update()
                        pygame.time.wait(300)


                def hasWon(revealedBoxes):
                    # Returns True if all the boxes have been revealed, otherwise False
                    for i in revealedBoxes:
                        if False in i:
                            return False # return False if any boxes are covered.
                    return True


                if __name__ == '__main__':
                    main()



    pygame.event.pump()
    screen.fill((0, 0, 0))
    screen .blit(text_obj,(120, 40))
    
    for option in options:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
        else:
            option.hovered = False
        option.draw()



    pygame.display.update()
