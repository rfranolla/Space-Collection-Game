import pygame
import time
import random
import sys
import math

#### ==================================================================================================== ####
####                                         INITIALIZE                                                   ####
#### ==================================================================================================== ####

def initialize():
    ''' Central Initialize function. Calls helper functions to initialize Pygame and then the gameData dictionary.
    Input: None
    Output: gameData Dictionary
    '''
    screen = initializePyGame()
    return initializeData(screen)

####                                           HELPERS                                                    ####
#### ---------------------------------------------------------------------------------------------------- ####

def initializeData(screen):

    # Start Music
    pygame.mixer.music.load("resources/sound/music.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1) 

    # Initialize gameData Dictionary
    gameData = {'screen': screen,
                'background': pygame.transform.scale(pygame.image.load("resources/background/background.png").convert_alpha(), (800, 600)),
                'numPlayers': 0,
                'entities': [],
                'score': 0,
                'myFont': pygame.font.SysFont('impact', 50),
                'gameOver': False,
                'isOpen': True}

    # Determine number of players
    gameData['numPlayers'] = numberOfPlayers(gameData)

    for i in range(gameData['numPlayers']):
        # Generate 'Ship' Entity
        gameData['entities'].append({'type': 'ship',
                                     'number': i+1,
                                     'location': [400, 300],
                                     'velocity': 10,
                                     'size': 60,
                                     'angle': 180,
                                     'sprite': pygame.transform.scale(pygame.image.load("resources/ship/ship_{}.png".format(i+1)).convert_alpha(), (60, 60)),
                                     'currAction': 'NA'})


    # Generate 'Gem' Entity
    gameData['entities'].append({'type': 'gem',
                                 'location': [random.randint(100, 700), random.randint(100, 500)],
                                 'size': 20,
                                 'sprite': pygame.transform.scale(pygame.image.load("resources/gem/gem.png").convert_alpha(), (20,20)),
                                 'isCollected': False})

    # Generate 'Boost' Entity
    gameData['entities'].append({'type': 'boost',
                                 'location': [random.randint(50, 750), random.randint(50, 550)],
                                 'size': 40,
                                 'sprite': pygame.transform.scale(pygame.image.load("resources/boost/boost.png").convert_alpha(), (40,40)),
                                 'isCollected': False,
                                 'exists': False})

    # Generate 'Meteor' Entity
    for i in range(random.randint(2, 4)):
        gameData['entities'].append({'type': 'meteor',
                                     'size': 50,
                                     'angle': random.randint(0, 360),
                                     'sprite': pygame.transform.scale(pygame.image.load("resources/meteor/meteor_{}.png".format(random.randint(1, 4))).convert_alpha(), (50, 50)),
                                     'location': [random.randint(700, 750), random.randint(500, 550)],
                                     'velocity': [random.randint(1, 5), random.randint(1, 5)]})

    # Generate 'Line' Entity
    stop = random.randint(0, 50)
    start = stop+25
    stop = stop/100
    start = start/100
    gameData['entities'].append({'type': 'line',
	                         'origin': (800,0),                       # the location of the line segmants 
	                         'location': [[],[]], 
	                         'angle': 90,                                # the current "angle" of the line
                                 'speed': 0.25,                              # the speed at which the line moves
                                 'changeGap': False,
                                 'sprites': [[],[]],
	                         'length': [ (0.00, stop), (start, 1.00) ],  # the "length" intervals that specify the gap(s)
	                         'segments':[]})                             # the individual "segments" (i.e., non-gaps)

    return gameData

def initializePyGame():
    ''' Initializes Pygame'''
    pygame.init()
    pygame.key.set_repeat(1, 1)
    return pygame.display.set_mode((800, 600))

def numberOfPlayers(gameData):
    
    selected = False
    numPlayers = 0
    gameData["screen"].blit(gameData["background"], (0, 0))
    pygame.draw.rect(gameData['screen'], (124, 174, 255), (100, 250, 200, 100))
    text = gameData['myFont'].render(("1 Player"), 1, (0,0,0))
    gameData['screen'].blit(text, (125, 275))

    pygame.draw.rect(gameData['screen'], (124, 174, 255), (500, 250, 200, 100))
    text = gameData['myFont'].render(("2 Player"), 1, (0,0,0))
    gameData['screen'].blit(text, (525, 275))

    pygame.display.flip()

    frameRate = 40
    clock = pygame.time.Clock()
    while not selected:
        events = pygame.event.get()
        for event in events:
        # Handle Mouse Click
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                if (mousePos[0]>100 and mousePos[0]<300 and mousePos[1]>250 and mousePos[1]<350):
                    numPlayers = 1
                    selected = True
                if (mousePos[0]>500 and mousePos[0]<700 and mousePos[1]>250 and mousePos[1]<350):
                    numPlayers = 2
                    selected = True
        clock.tick(frameRate)
    return numPlayers

#### ======================================================================================================= ####
####                                           PROCESSING                                                    ####
#### ======================================================================================================= ####

def process(gameData):
    ''' Central Process function. Calls helper functions to handle various KEYDOWN events.
    Input: gameData Dictionary
    Output: None
    '''
    events = pygame.event.get()
    for event in events:
        # Handle [x] Press
        if event.type == pygame.QUIT:
            gameData['isOpen'] = False
            
        # Handle Key Presses
        if event.type == pygame.KEYDOWN:
                
            # Handle 'Escape' Key
            if event.key == pygame.K_ESCAPE:
                handleKeyEscape(gameData)

            for entity in gameData['entities']:
                if entity['type'] == 'ship' and entity['number'] == 1:
                # Handle Movement
                    if (event.key == pygame.K_a):
                        handleKeyLeft(entity)

                    elif (event.key == pygame.K_d):
                        handleKeyRight(entity)

                    elif (event.key == pygame.K_w):
                        handleKeyUp(entity)

                    elif (event.key == pygame.K_s):
                        handleKeyDown(entity)

                if entity['type'] == 'ship' and entity['number'] == 2:
                # Handle Movement
                    if (event.key == pygame.K_LEFT):
                        handleKeyLeft(entity)

                    elif (event.key == pygame.K_RIGHT):
                        handleKeyRight(entity)

                    elif (event.key == pygame.K_UP):
                        handleKeyUp(entity)

                    elif (event.key == pygame.K_DOWN):
                        handleKeyDown(entity)


####                                           HANDLERS                                                   ####
#### ---------------------------------------------------------------------------------------------------- ####
def handleKeyLeft(entity):
    entity['currAction'] = 'Left'

def handleKeyRight(entity):
    entity['currAction'] = 'Right'

def handleKeyUp(entity):
    entity['currAction'] = 'Up'

def handleKeyDown(entity):
    entity['currAction'] = 'Down'

def handleKeyEscape(gameData):
    ''' Handles the Escape KEYDOWN event. Sets a flag for 'isOpen' to 'False'.
    Input: gameData Dictionary
    Output: None
    '''
    gameData['isOpen'] = False

#### ====================================================================================================== ####
####                                            UPDATING                                                    ####
#### ====================================================================================================== ####
    
def update(gameData):
    ''' Central Update function '''

    if not gameData['gameOver']:
        for entity in gameData["entities"]:
            if entity['type'] == 'ship':
                gemEntity = None
                boostEntity = None
                for moreEntities in gameData['entities']:
                    if moreEntities['type'] == 'gem':
                        gemEntity = moreEntities
                    elif moreEntities['type'] == 'boost':
                        boostEntity = moreEntities
                    elif moreEntities['type'] == 'line':
                        lineEntity = moreEntities
                updateShip(entity, gemEntity, boostEntity)
                entity['currAction'] = 'NA'

            if entity['type'] == 'gem':
                if (entity['isCollected'] == True):
                    gameData['score'] += 1
                updateGem(entity)

            if entity['type'] == 'meteor':
                shipEntity = None
                for moreEntities in gameData['entities']:
                    if moreEntities['type'] == 'ship':
                        shipEntity = moreEntities
                updateMeteor(gameData, entity, shipEntity)

            if entity['type'] == 'boost':
                if gameData['score']>0 and gameData['score']%13 == 0:
                    entity['exists'] = True
                updateBoost(entity)

            if entity['type'] == 'line':
                shipEntity = None
                for moreEntities in gameData['entities']:
                    if moreEntities['type'] == 'ship':
                        shipEntity = moreEntities
                updateLine(gameData, entity, shipEntity)
    
            

####                                          HELPERS                                                    ####
#### --------------------------------------------------------------------------------------------------- ####

def updateShip(entity, gemEntity, boostEntity):
    # Update position if its in the bounds of the window
    if entity['currAction'] == 'NA':
        return

    if (entity['currAction'] == 'Left' and entity['location'][0]-entity['size'] >= 0):
        entity['location'][0] -= entity['velocity']
        entity['angle'] = 270

    if (entity['currAction'] == 'Right' and (entity['location'][0]+entity['size']) <= 800):
        entity['location'][0] += entity['velocity']
        entity['angle'] = 90

    if (entity['currAction'] == 'Up' and (entity['location'][1]-entity['size']) >= 0):
        entity['location'][1] -= entity['velocity']
        entity['angle'] = 180

    if (entity['currAction'] == 'Down' and (entity['location'][1]+entity['size']) <= 600):
        entity['location'][1] += entity['velocity']
        entity['angle'] = 0

    # Check to see if collided with the gem
    if (entity['location'][0]<gemEntity['location'][0]+entity['size'] and entity['location'][0]>gemEntity['location'][0] and entity['location'][1]<gemEntity['location'][1]+entity['size'] and entity['location'][1]>gemEntity['location'][1]):
        gemEntity['isCollected'] = True

    # Check to see if collided with boost
    if (entity['location'][0]<boostEntity['location'][0]+entity['size'] and entity['location'][0]>boostEntity['location'][0] and entity['location'][1]<boostEntity['location'][1]+entity['size'] and entity['location'][1]>boostEntity['location'][1] and boostEntity['exists']):
        boostEntity['isCollected'] = True
        entity['velocity'] += 0.5

def updateGem(entity):
    if entity['isCollected']:
        entity['isCollected'] = False
        entity['exists'] = False
        entity['location'] = [random.randint(100, 700), random.randint(100, 500)]

def updateBoost(entity):
    if entity['isCollected']:
        entity['isCollected'] = False
        entity['exists'] = False
        entity['location'] = [random.randint(50, 750), random.randint(50, 550)]

def updateMeteor(gameData, entity, shipEntity):
    # Update its loaction and direction if it hits the edge of the window. And increase angle to simulate spinning in space
    entity['angle'] += 1
    entity['location'][0] += entity['velocity'][0]
    entity['location'][1] += entity['velocity'][1]
    if (entity['location'][0]+entity['size'] > 800 or entity['location'][0] < 0):
        entity['velocity'][0] *= -1
    if (entity['location'][1]+entity['size'] > 600 or entity['location'][1] < 0):
        entity['velocity'][1] *= -1

    # See if meteor collides with the ship
    meteorRect = entity['sprite'].get_rect(topleft = entity['location'])
    shipRect = shipEntity['sprite'].get_rect(topleft = shipEntity['location'])
    if (meteorRect.colliderect(shipRect)):
        gameData['gameOver'] = True

def updateLine(gameData, entity, shipEntity):
    # if score is a multiple of ten, change gap location
    if gameData['score']>0 and gameData['score']%10 == 0:
        entity['changeGap'] = True

    # increase the angle of the rotating line
    entity['angle'] += entity['speed']

    # the rotating line angle ranges between 90 and 180 degrees
    if entity['angle'] > 180:

        # when it reaches an angle of 180 degrees, reset line and increase speed, see if gap needs to change
        entity['angle'] = 90
        entity['speed'] += 0.01
        if entity['changeGap']:
            stop = random.randint(0, 50)
            start = stop+25
            stop = stop/100
            start = start/100
            entity['length'] = [ (0.00, stop), (start, 1.00) ]
            entity['changeGap'] = False
        
		
    # the points associated with each line segment must be recalculated as the angle changes
    entity['segments'] = []
	
    # consider every line segment length
    i = 0
    for len in entity['length']:
	
        # compute the start of the line...
        sol_x = entity['origin'][0] + math.cos(math.radians(entity['angle'])) * 1000 * len[0]
        sol_y = entity['origin'][1] + math.sin(math.radians(entity['angle'])) * 1000 * len[0]
		
        # ...and the end of the line...
        eol_x = entity['origin'][0] + math.cos(math.radians(entity['angle'])) * 1000 * len[1]
        eol_y = entity['origin'][1] + math.sin(math.radians(entity['angle'])) * 1000 * len[1]
		
        # ...and then add that line to the list
        entity['segments'].append( ((sol_x, sol_y), (eol_x, eol_y)) )

        length = int(((sol_x - eol_x)**2 + (sol_y - eol_y)**2)**(1/2))
        entity['sprites'][i] = (pygame.transform.scale(pygame.image.load("resources/laser/laser.png").convert_alpha(), (length,10)))
        entity['location'][i] = (eol_x, eol_y)
        i+=1


    # Check to see if collided with ship
    for seg in entity["segments"]:
        # unpack u; a line is an ordered pair of points and a point is an ordered pair of co-ordinates
        (u_sol, u_eol) = seg
        (u_sol_x, u_sol_y) = seg[0]
        (u_eol_x, u_eol_y) = seg[1]  

        # the equation for all points on the line segment u can be considered u = u_sol + t * (u_eol - u_sol), for t in [0, 1]
        # the center of the circle and the nearest point on the line segment (that which we are trying to find) define a line 
        # that is is perpendicular to the line segment u (i.e., the dot product will be 0); in other words, it suffices to take
        # the equation v_ctr - (u_sol + t * (u_eol - u_sol)) · (u_evol - u_sol) and solve for t
        t = ((shipEntity['location'][0] - u_sol_x) * (u_eol_x - u_sol_x) + (shipEntity['location'][1]  - u_sol_y) * (u_eol_y - u_sol_y)) / ((u_eol_x - u_sol_x) ** 2 + (u_eol_y - u_sol_y) ** 2)

        # this t can be used to find the nearest point w on the infinite line between u_sol and u_sol, but the line is not 
        # infinite so it is necessary to restrict t to a value in [0, 1]
        t = max(min(t, 1), 0)
	
        # so the nearest point on the line segment, w, is defined as
        w_x = u_sol_x + t * (u_eol_x - u_sol_x)
        w_y = u_sol_y + t * (u_eol_y - u_sol_y)
	
        # Euclidean distance squared between w and v_ctr
        d_sqr = (w_x - shipEntity['location'][0] ) ** 2 + (w_y - shipEntity['location'][1] ) ** 2
	
        # if the Eucliean distance squared is less than the radius squared
        if (d_sqr <= (shipEntity['size']/2) ** 2):
            # the line collides
            gameData['gameOver'] = True




#### =================================================================================================== ####
####                                           RENDERING                                                 ####
#### =================================================================================================== ####

def render(gameData):
    ''' Central Render function'''

    # If player loses print the game over screen with the score they got...
    if gameData['gameOver']:
        gameData["screen"].blit(gameData["background"], (0, 0))

        text = gameData['myFont'].render(("GAME OVER"), 1, (0,255,0))
        gameData['screen'].blit(text, (300, 200))

        if gameData['score']<25:
            scoreText = gameData['myFont'].render(("You Gathered %s Gems. That Is Not Enough" % gameData['score']), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (50, 250))

            scoreText = gameData['myFont'].render(("The Local Colony Will Starve in 2 Weeks"), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (75, 300))

            scoreText = gameData['myFont'].render(("'Good Job'"), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (325, 350))

        if gameData['score']>25 and gameData['score']<50:
            scoreText = gameData['myFont'].render(("You Gathered %s Gems. I Guess That's Good" % gameData['score']), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (50, 250))

            scoreText = gameData['myFont'].render(("The Local Colony Will Survive For Now"), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (75, 300))

            scoreText = gameData['myFont'].render(("Take a 5 Minute Break"), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (300, 350))

        if gameData['score']>50 and gameData['score']<75:
            scoreText = gameData['myFont'].render(("You Gathered %s Gems. Well Done Captain" % gameData['score']), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (50, 250))

            scoreText = gameData['myFont'].render(("The Local Colony Will Prosper"), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (75, 300))

            scoreText = gameData['myFont'].render(("You Are Fantastic"), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (300, 350))

        if gameData['score']>75:
            scoreText = gameData['myFont'].render(("You Gathered %s Gems. You Are Amazing" % gameData['score']), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (75, 250))

            scoreText = gameData['myFont'].render(("The Local Colony Will Survive The Rest Of The Year"), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (50, 300))

            scoreText = gameData['myFont'].render(("You Are a God"), 1, (0,255,0))
            gameData['screen'].blit(scoreText, (300, 350))



    # ...else print the entities onto the screen
    else:
        gameData["screen"].blit(gameData["background"], (0, 0))

        for entity in gameData["entities"]:
            if entity['type'] == 'ship':
                renderShip(gameData, entity)
            if entity['type'] == 'gem':
                renderGem(gameData, entity)
            if entity['type'] == 'line':
                renderLine(gameData, entity)
            if entity['type'] == 'boost':
                renderBoost(gameData, entity)
            if entity['type'] == 'meteor':
                renderMeteor(gameData, entity)

        renderScore(gameData)
            
    pygame.display.flip()

####                                           HELPERS                                                    ####
#### ---------------------------------------------------------------------------------------------------- ####

def renderShip(gameData, entity):
    rotated_image = pygame.transform.rotate(entity['sprite'], entity['angle'])
    rotated_pos = rotated_image.get_rect(center = entity['location'])
    gameData['screen'].blit(rotated_image, rotated_pos)

def renderGem(gameData, entity):
    gameData['screen'].blit(entity['sprite'], entity['location'])

def renderMeteor(gameData, entity):
    rotated_image = pygame.transform.rotate(entity['sprite'], entity['angle'])
    rotated_pos = rotated_image.get_rect(center = entity['location'])
    gameData['screen'].blit(rotated_image, rotated_pos)

def renderBoost(gameData, entity):
    if entity['exists']:
        gameData['screen'].blit(entity['sprite'], entity['location'])

def renderScore(gameData):
    score = gameData['myFont'].render(("Score: %s" % gameData['score']), 1, (0,255,0))
    gameData['screen'].blit(score, (300, 10))

def renderLine(gameData, entity):
    i = 0
    angle = - (math.atan2(entity['origin'][1] - entity['segments'][0][1][1], entity['origin'][0] - entity['segments'][0][1][0])) * 180/math.pi 
    for seg in entity['segments']:
        #pygame.draw.aaline(gameData['screen'], (255, 255, 255), seg[0], seg[1])

        rotated_image = pygame.transform.rotate(entity['sprites'][i], angle)
        rotated_pos = rotated_image.get_rect(bottomleft = entity['location'][i])
        gameData['screen'].blit(rotated_image, rotated_pos)
        i+=1


#### ==================================================================================================== ####
####                                             MAIN                                                     ####
#### ==================================================================================================== ####

def main():
    ''' Main function of script - calls all central functions above via a Game Loop code structure.
    Input: None
    Output: None
    '''
    # Initialize Data and Pygame
    gameData = initialize()

    #Control Frame Rate
    frame_rate = 40
    delta_time = 1 / frame_rate
    clock = pygame.time.Clock()
    
    # Begin Central Game Loop
    while gameData['isOpen']:
        process(gameData)
        update(gameData)
        render(gameData)
        clock.tick(frame_rate)
        
    # Exit Pygame and Python
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
