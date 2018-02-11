import pygame

#author Ryan Bailey

class App():
    def __init__(self, title, width, height, standardWidth, standardHeight, iconLocation=None):
        pygame.init()
        pygame.font.init()
        
        self.__title = title
        self.__width = width    #window width
        self.__height = height  #window height
        self.__standardWidth = standardWidth
        self.__standardHeight = standardHeight

        '''
        Standard width and standard height are the values for the width and
        height of the window when calling a function in the drawer class.
        Everything drawn is then scaled to the actual width and height of the
        window before being drawn to the window. This allows for the width and
        height of the window to be changed without having to change all of the
        values used when drawing provided the width-height ratio remains the
        same. The values used for the standard width and standard height must
        also have that same width-height ratio.
        '''

        if not width/height == standardWidth/standardHeight:
            raise RatioException("The window width-height ratio doesn't equal the standard width-height ratio")

        #multiplying a length in standard units by the ratio gives you the length in pixels
        self.__ratio = width/standardWidth

        pygame.display.set_caption(title)
        self.__window = pygame.display.set_mode((width, height))
        
        if iconLocation != None:
            icon = loadImage(iconLocation)
            pygame.display.set_icon(icon)

        self.__closeRequested = False
        self.__clock = pygame.time.Clock()

        '''
        In this framework, input is monostable. For example this means that
        even if a key is held down, the framework should only show the key being
        pressed in the tick when the key is first pressed, and never after, unless
        the key is pressed again. To do this, I use three variables for each type
        of input: input, lastInput and lastRealInput. In the example of a key being
        pressed, the variables being used would be keyInput, lastKeyInput and
        lastRealKeyInput. Similar names are used for mouse click input and mouse
        motion input.

        The input variable is the input as the framework intends for it to be
        seen in the current tick. Because of this, it is set to NONE if the framework
        sees that the input in the current tick is equal to the input in the last tick,
        giving the input its monostable nature. This is the variable returned by the
        inputReturned function for the type of input.

        The lastInput variable is the input as the framework intended it to be sen last
        tick. It is literally just set to whatever the input variable was last tick. This
        variable is used to monostable the input as described above.

        The lastRealInput is the last non-NONE input value, kept by the framework just
        in case it turns out to be useful in a future update, which I suspect it might but
        admittedly I have no idea why.
        '''
        
        self.__keyInput = "NONE"
        self.__lastKeyInput = self.__keyInput
        self.__lastRealKeyInput = self.__keyInput

        self.__mouseClickInput = "NONE"
        self.__lastMouseClickInput = self.__mouseClickInput
        self.__lastRealMouseClickInput = self.__mouseClickInput

        self.__mouseMotionInput = "NONE"
        self.__lastMouseMotionInput = self.__mouseMotionInput
        self.__lastRealMouseMotionInput = self.__mouseMotionInput

    def update(self): #all the runtime pygame stuff goes here
        
        #handle input
        self.__keyInput = "NONE"
        self.__mouseClickInput = "NONE"
        self.__mouseMotionInput = "NONE"
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__closeRequested = True
            
            if event.type == pygame.KEYDOWN:
                self.__keyInput = pygame.key.name(event.key)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.__mouseClickInput = []
                for value in pygame.mouse.get_pos():
                    self.__mouseClickInput += [self.__reverseScale(value)]
            
            if event.type == pygame.MOUSEMOTION:
                self.__mouseMotionInput = []
                for value in event.pos:
                    self.__mouseMotionInput += [self.__reverseScale(value)]

        #update display
        pygame.display.flip()
        self.__clock.tick(60)

    def __monostable(self, _input, lastInput, lastRealInput):
        if _input == "NONE" and lastInput != "NONE":
            lastRealInput = lastInput

        if lastInput == _input:
            _input = "NONE"
        else:
            lastInput = _input
        return _input, lastInput, lastRealInput

    def keyInputReturned(self): #returns an string detailing any keys pressed in the current tick
        (self.__keyInput,
         self.__lastKeyInput,
         self.__lastRealKeyInput) = self.__monostable(self.__keyInput,
                                                      self.__lastKeyInput,
                                                      self.__lastRealKeyInput)
        return self.__keyInput

    def mouseClickInputReturned(self):
        (self.__mouseClickInput,
         self.__lastMouseClickInput,
         self.__lastRealMouseClickInput) = self.__monostable(self.__mouseClickInput,
                                                             self.__lastMouseClickInput,
                                                             self.__lastRealMouseClickInput)
        return self.__mouseClickInput

    def mouseMotionInputReturned(self):
        (self.__mouseMotionInput,
         self.__lastMouseMotionInput,
         self.__lastRealMouseMotionInput) = self.__monostable(self.__mouseMotionInput,
                                                              self.__lastMouseMotionInput,
                                                              self.__lastRealMouseMotionInput)
        return self.__mouseMotionInput

    def drawImage(self, image, x, y, width, height):
        x = self.__scale(x)
        y = self.__scale(y)
        width = self.__scale(width)
        height = self.__scale(height)
        image = pygame.transform.scale(image, (width, height))
        rect = image.get_rect()
        rect = rect.move(x, y)
        self.__window.blit(image, rect)
    
    def drawRect(self, color, x, y, width, height):
        x = self.__scale(x)
        y = self.__scale(y)
        width = self.__scale(width)
        height = self.__scale(height)
        pygame.draw.rect(self.__window, color, pygame.Rect(x, y, width, height))
        
    def drawText(self, text, color, x, y, size, font="monospace"):
        x = self.__scale(x)
        y = self.__scale(y)
        size = self.__scale(size)
        font = pygame.font.SysFont(font, size)
        textSurface = font.render(text, True, color)
        self.__window.blit(textSurface, (x, y))

    def drawLine(self, color, x1, y1, x2, y2, width):
        x1 = self.__scale(x1)
        y1 = self.__scale(y1)
        x2 = self.__scale(x2)
        y2 = self.__scale(y2)
        width = self.__scale(width)
        pygame.draw.line(self.__window, color, (x1, y1), (x2, y2), width)

    def __scale(self, k): #scales standard units to pixels
        return int(round(k*self.__ratio, 0))

    def __reverseScale(self, k): #scales pixels to standard units
        return int(round(k/self.__ratio, 0)) #030500

    def title(self):
        return self.__title

    def standardWidth(self):
        return self.__standardWidth

    def standardHeight(self):
        return self.__standardHeight
    
    def closeRequested(self): #returns true only if exit window button pressed
        return self.__closeRequested

    def close(self):
        pygame.quit()

class RatioException(Exception):
    pass

class Screen():
    def __init__(self, app, name):
        self.app = app
        self.__name = name
        
    def draw(self):
        raise NotImplementedError("The screen you are using hasn't overriden the draw method.")

    def clear(self):
        self.app.drawRect((0, 0, 0), 0, 0, self.app.standardWidth(), self.app.standardHeight())

    def name(self):
        return self.__name

class Widget():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def mousedOver(self, x, y):
        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
            return True
        return False

    def draw(self):
        raise NotImplementedError("The Widget you are using hasn't overridden the draw method")

'''
these functions are outside of the App class as they should
be able to be accessedwithout needing an instance of app.
'''

def loadImage(path):
    return pygame.image.load(path)

def textDimensions(text, size, font="monospace"):
        font = pygame.font.SysFont(font, size)
        return font.size(text)
