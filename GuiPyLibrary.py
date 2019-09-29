class Button:                                        #colourList must contain 6 colours
    def __init__(self, xPos, yPos, buttonWidth, buttonHeight, colourList, edgeWidth=1):
        self.xPos              = xPos
        self.yPos              = yPos
        self.buttonWidth       = buttonWidth
        self.buttonHeight      = buttonHeight
        self.colourList        = colourList
        self.colour            = colourList[0]
        self.edgeColour        = colourList[1]
        self.colourHovered     = colourList[2]
        self.edgeColourHovered = colourList[3]
        self.colourPressed     = colourList[4]
        self.edgeColourPressed = colourList[5]
        self.edgeWidth         = edgeWidth
        self.isPressed         = False
        self.isHovered         = False
        self.justReleased      = False
        self.justPressed       = False
        self.isDisabled        = False


        
    def handle(self): # must be called once per frame
        self._update()

        rectMode(CENTER)
        strokeWeight(self.edgeWidth)
        
        if self.isPressed:
            stroke(self.edgeColourPressed)
            fill(self.colourPressed)
            
        elif self.isHovered:
            stroke(self.edgeColourHovered)
            fill(self.colourHovered)
            
        else:
            stroke(self.edgeColour)
            fill(self.colour)

        rect(self.xPos, self.yPos, self.buttonWidth, self.buttonHeight)

        self._extraHandle()

        if self.isDisabled:
            noStroke()  
            fill(100, 100)
            rect(self.xPos, self.yPos, self.buttonWidth, self.buttonHeight)

            strokeWeight(5)
            stroke(255, 0, 0)
            line(self.xPos - (self.buttonWidth / 2), self.yPos - (self.buttonHeight / 2), self.xPos + (self.buttonWidth / 2), self.yPos + (self.buttonHeight / 2))



    def _extraHandle(self):
        pass



    def _update(self):
        left   = self.xPos - (self.buttonWidth  / 2.0)
        right  = self.xPos + (self.buttonWidth  / 2.0)
        top    = self.yPos - (self.buttonHeight / 2.0)
        bottom = self.yPos + (self.buttonHeight / 2.0)

        if self.isDisabled:
            self.isPressed         = False
            self.isHovered         = False
            self.justReleased      = False
            self.justPressed       = False
        else:
            if mouseX > left and mouseX < right and mouseY > top and mouseY < bottom:
                if mousePressed and mouseButton == LEFT:
                    if self.isPressed:
                        self.justPressed = False
                        
                    elif self.isHovered:
                        self.isHovered = False
                        self.isPressed = True
                        self.justPressed = True
                        
                else:
                    if self.isPressed:
                        self.isHovered = True
                        self.isPressed = False
                        self.justReleased = True
                        
                    else:
                        self.isHovered = True
                        self.justReleased = False
                        
            else:
                self.isHovered = False
                self.isPressed = False




class TextButton(Button):                                               #colourList must contain 9 colours
    def __init__(self, xPos, yPos, buttonWidth, buttonHeight, colourList, label, offset=0, labelSize=30, edgeWidth=1):
        Button.__init__(self, xPos, yPos, buttonWidth, buttonHeight, colourList, edgeWidth)

        self.label              = label
        self.offset             = offset
        self.labelSize          = labelSize
        self.colour             = colourList[0]
        self.labelColour        = colourList[1]
        self.edgeColour         = colourList[2]
        self.colourHovered      = colourList[3]
        self.labelColourHovered = colourList[4]
        self.edgeColourHovered  = colourList[5]
        self.colourPressed      = colourList[6]
        self.labelColourPressed = colourList[7]
        self.edgeColourPressed  = colourList[8]



    def _extraHandle(self):
        textAlign(CENTER, CENTER)
        textSize(self.labelSize)
        
        if self.isPressed:
            fill(self.labelColourPressed)

        elif self.isHovered:
            fill(self.labelColourHovered)

        else:
            fill(self.labelColour)

        text(self.label, self.xPos, self.yPos + self.offset, self.buttonWidth, self.buttonHeight)



                         #iconFunc is a function for drawing         #colourList must contain 6 colours
class IconButton(Button):#the icon on 0, 0
    def __init__(self, xPos, yPos, buttonWidth, buttonHeight, colourList, iconFunc, edgeWidth=1):
        Button.__init__(self, xPos, yPos, buttonWidth, buttonHeight, colourList, edgeWidth)

        self.iconFunc = iconFunc



    def _extraHandle(self):
        translate(self.xPos, self.yPos)
        self.iconFunc()
        resetMatrix()





class Selector:                    #screenWidth must be < selectorWidth
    def __init__(self, xPos, yPos, selectorWidth, selectorHeight, screenWidth, screenHeight, arrowWidth, arrowHeight, edgeWidth=1, colourList=(color(150), color(0), color(0), color(100), color(0), color(50), color(0), color(0), color(100))):
        self.xPos                   = xPos
        self.yPos                   = yPos
        self.selectorWidth          = selectorWidth
        self.selectorHeight         = selectorHeight
        self.screenWidth            = screenWidth
        self.screenHeight           = screenHeight
        self.arrowWidth             = arrowWidth
        self.arrowHeight            = arrowHeight
        self.colour                 = colourList[0]
        self.edgeColour             = colourList[1]
        self.screenEdgeColour       = colourList[2]
        self.arrowColour            = colourList[3]
        self.arrowEdgeColour        = colourList[4]
        self.arrowColourHovered     = colourList[5]
        self.arrowEdgeColourHovered = colourList[6]
        self.arrowColourPressed     = colourList[7]
        self.arrowEdgeColourPressed = colourList[8]
        self.edgeWidth              = edgeWidth
        self.currentSelectionNum    = 0
        self.numOfOptions           = 0
        self.isDisabled             = False
        self._isMouseOverLeft       = False
        self._isMouseOverRight      = False
        self._isLeftPressed         = False
        self._isLeftHovered         = False
        self._hasLeftJustReleased   = False
        self._hasLeftJustPressed    = False
        self._isRightPressed        = False
        self._isRightHovered        = False
        self._hasRightJustReleased  = False
        self._hasRightJustPressed   = False
        self._arrowAreaWidth        = ((self.selectorWidth - self.screenWidth) / 2)
        self._arrowAreaHeight       = self.selectorHeight
        self._rightArrowLeft        = self.xPos + (self.screenWidth / 2.0) + (self._arrowAreaWidth / 2.0) - (self.arrowWidth / 2.0)
        self._rightArrowRight       = self._rightArrowLeft + self.arrowWidth
        self._rightArrowTop         = self.yPos - (self.arrowHeight / 2.0)
        self._rightArrowBottom      = self._rightArrowTop + self.arrowHeight
        self._leftArrowRight        = self.xPos - (self.screenWidth / 2.0) - (self._arrowAreaWidth / 2.0) + (self.arrowWidth / 2.0)
        self._leftArrowLeft         = self._leftArrowRight - self.arrowWidth
        self._leftArrowBottom       = self.yPos + (self.arrowHeight / 2.0)
        self._leftArrowTop          = self._leftArrowBottom - self.arrowHeight
        self._leftTopLineGrad       = -(self.arrowHeight / 2.0) / float(self.arrowWidth)
        self._leftBottomLineGrad    = -self._leftTopLineGrad
        self._rightTopLineGrad      = self._leftBottomLineGrad
        self._rightBottomLineGrad   = self._leftTopLineGrad
        self._leftTopLineInter      = self._leftArrowTop     - (self._leftArrowRight * self._leftTopLineGrad    )
        self._leftBottomLineInter   = self._leftArrowBottom  - (self._leftArrowRight * self._leftBottomLineGrad )
        self._rightTopLineInter     = self._rightArrowTop    - (self._rightArrowLeft * self._rightTopLineGrad   )
        self._rightBottomLineInter  = self._rightArrowBottom - (self._rightArrowLeft * self._rightBottomLineGrad)



    def handle(self): #must be called once per frame
        self._update()

        rectMode(CENTER)
        strokeWeight(self.edgeWidth)

        stroke(self.edgeColour)
        fill(self.colour)
        rect(self.xPos, self.yPos, self.selectorWidth, self.selectorHeight)


        stroke(self.screenEdgeColour)
        self._handleSelection()


        if self._isRightPressed:
            stroke(self.arrowEdgeColourPressed)
            fill(self.arrowColourPressed)
        elif self._isRightHovered:
            stroke(self.arrowEdgeColourHovered)
            fill(self.arrowColourHovered)
        else:
            stroke(self.arrowEdgeColour)
            fill(self.arrowColour)
            
        triangle(self._rightArrowLeft, self._rightArrowTop, self._rightArrowLeft, self._rightArrowBottom, self._rightArrowRight, self.yPos)

        if self._isLeftPressed:
            stroke(self.arrowEdgeColourPressed)
            fill(self.arrowColourPressed)
        elif self._isLeftHovered:
            stroke(self.arrowEdgeColourHovered)
            fill(self.arrowColourHovered)
        else:
            stroke(self.arrowEdgeColour)
            fill(self.arrowColour)

        triangle(self._leftArrowRight, self._leftArrowTop, self._leftArrowRight, self._leftArrowBottom, self._leftArrowLeft, self.yPos)


        if self.isDisabled:
            noStroke()
            fill(100, 100)
            rect(self.xPos, self.yPos, self.selectorWidth, self.selectorHeight)

            strokeWeight(5)
            stroke(255, 0, 0)
            line(self.xPos - (self.selectorWidth / 2), self.yPos - (self.selectorHeight / 2), self.xPos + (self.selectorWidth / 2), self.yPos + (self.selectorHeight / 2))



    def _handleSelection(self):
        fill(0, 0, 0)
        rect(self.xPos, self.yPos, self.screenWidth, self.screenHeight)



    def _update(self):
        self._isMouseOverLeft  = False
        self._isMouseOverRight = False

        if self.isDisabled:
            self._isLeftPressed         = False
            self._isLeftHovered         = False
            self._hasLeftJustReleased   = False
            self._hasLeftJustPressed    = False
            self._isRightPressed        = False
            self._isRightHovered        = False
            self._hasRightJustReleased  = False
            self._hasRightJustPressed   = False


        else:
            if mouseX > self._leftArrowLeft and mouseX < self._leftArrowRight and mouseY > self._leftArrowTop and mouseY < self._leftArrowBottom:
                if mouseY < self.yPos:
                    if mouseY > ((self._leftTopLineGrad * mouseX) + self._leftTopLineInter): #hovering
                        self._isMouseOverLeft = True
                else:
                    if mouseY < ((self._leftBottomLineGrad * mouseX) + self._leftBottomLineInter): #hovering
                        self._isMouseOverLeft = True
                        
            elif mouseX > self._rightArrowLeft and mouseX < self._rightArrowRight and mouseY > self._rightArrowTop and mouseY < self._rightArrowBottom:
                if mouseY < self.yPos:
                    if mouseY > ((self._rightTopLineGrad * mouseX) + self._rightTopLineInter): #hovering
                        self._isMouseOverRight = True
                else:
                    if mouseY < ((self._rightBottomLineGrad * mouseX) + self._rightBottomLineInter): #hovering
                        self._isMouseOverRight = True

            
            if self._isMouseOverLeft:
                if mousePressed and mouseButton == LEFT:
                    if self._isLeftPressed:
                        self._hasLeftJustPressed = False
                    elif self._isLeftHovered:
                        self._isLeftHovered = False
                        self._isLeftPressed = True
                        self._hasLeftJustPressed = True
                else:
                    if self._isLeftPressed:
                        self._isLeftHovered = True
                        self._isLeftPressed = False
                        self._hasLeftJustReleased = True
                    else:
                        self._isLeftHovered = True
                        self._hasLeftJustReleased = False
                            
            elif self._isMouseOverRight:
                if mousePressed and mouseButton == LEFT:
                    if self._isRightPressed:
                        self._hasRightJustPressed = False
                    elif self._isRightHovered:
                        self._isRightHovered = False
                        self._isRightPressed = True
                        self._hasRightJustPressed = True
                else:
                    if self._isRightPressed:
                        self._isRightHovered = True
                        self._isRightPressed = False
                        self._hasRightJustReleased = True
                    else:
                        self._isRightHovered = True
                        self._hasRightJustReleased = False

            else:
                self._isLeftHovered  = False
                self._isRightHovered = False
                self._isLeftPressed  = False
                self._isRightPressed = False
                self._hasLeftJustPressed = False
                self._hasRightJustPressed = False


            if self._hasRightJustReleased:
                if self.currentSelectionNum < (self.numOfOptions - 1):
                    self.currentSelectionNum += 1
                else:
                    self.currentSelectionNum = 0

                self._updateCurrentSelection()


            if self._hasLeftJustReleased:
                if self.currentSelectionNum > 0:
                    self.currentSelectionNum -= 1
                else:
                    self.currentSelectionNum = self.numOfOptions - 1

                self._updateCurrentSelection()



    def _updateCurrentSelection(self):
        pass




class ColourSelector(Selector):                    #screenWidth must be < selectorWidth
    def __init__(self, xPos, yPos, selectorWidth, selectorHeight, screenWidth, screenHeight, arrowWidth, arrowHeight, colourOptionList, edgeWidth=1, colourList=(color(150), color(0), color(0), color(100), color(0), color(50), color(0), color(0), color(100))):
        Selector.__init__(self, xPos, yPos, selectorWidth, selectorHeight, screenWidth, screenHeight, arrowWidth, arrowHeight, edgeWidth, colourList)

        self.colourOptionList = colourOptionList
        self.currentColour    = colourOptionList[0]
        self.numOfOptions     = len(colourOptionList)



    def _handleSelection(self): #must be called once per second
        fill(self.currentColour)
        rect(self.xPos, self.yPos, self.screenWidth, self.screenHeight)
        


    def _updateCurrentSelection(self):
        self.currentColour = self.colourOptionList[self.currentSelectionNum]




class TextSelector(Selector):
    def __init__(self, xPos, yPos, selectorWidth, selectorHeight, screenWidth, screenHeight, arrowWidth, arrowHeight, textOptionList, textSizeList=None, textOffsetList=None, edgeWidth=1, colourList=(color(150), color(0), color(0), color(100), color(0), color(50), color(0), color(0), color(100))):
        Selector.__init__(self, xPos, yPos, selectorWidth, selectorHeight, screenWidth, screenHeight, arrowWidth, arrowHeight, edgeWidth, colourList)

        self.textOptionList = textOptionList
        self.textOffsetList = textOffsetList
        self.textSizeList   = textSizeList
        self.currentText    = self.textOptionList[0]
        self.numOfOptions   = len(textOptionList)



    def _handleSelection(self):
        textAlign(CENTER, CENTER)
        
        fill(255)
        rect(self.xPos, self.yPos, self.screenWidth, self.screenHeight)

        fill(0)
        
        if self.textSizeList == None:
            textSize(30)
        else:
            textSize(self.textSizeList[self.currentSelectionNum])
            
        if self.textOffsetList == None:
            text(self.currentText, self.xPos, self.yPos, self.screenWidth, self.screenHeight)
        else:
            text(self.currentText, self.xPos, self.yPos + self.textOffsetList[self.currentSelectionNum], self.screenWidth, self.screenHeight)



    def _updateCurrentSelection(self):
        self.currentText = self.textOptionList[self.currentSelectionNum]




class Checkbox:
    def __init__(self, xPos, yPos, sideLength, lineColour=color(150), tickColour=color(0, 255, 0), lineWidth=1):
        self.xPos          = xPos
        self.yPos          = yPos
        self.lineColour    = lineColour
        self.tickColour    = tickColour
        self.sideLength    = sideLength
        self.lineWidth     = lineWidth
        self.isDisabled    = False
        self.isTicked      = False
        self._justReleased = False
        self._isPressed    = False
        self._isHovered    = False
        self._sideQuarter  = sideLength / 4.0



    def handle(self):
        self._update()

        rectMode(CENTER)
        strokeWeight(self.lineWidth)

        stroke(self.lineColour)
        noFill()
        rect(self.xPos, self.yPos, self.sideLength, self.sideLength)

        if self.isTicked:
            stroke(self.tickColour)
            line(self.xPos - self._sideQuarter, self.yPos, self.xPos, self.yPos + self._sideQuarter)
            line(self.xPos, self.yPos + self._sideQuarter, self.xPos + self._sideQuarter, self.yPos - self._sideQuarter)

        if self.isDisabled:
            noStroke()
            fill(100, 100)
            rect(self.xPos, self.yPos, self.sideLength, self.sideLength)

            strokeWeight(5)
            stroke(255, 0, 0)
            line(self.xPos - (self.sideLength / 2), self.yPos - (self.sideLength / 2), self.xPos + (self.sideLength / 2), self.yPos + (self.sideLength / 2))



    def _update(self):
        left   = self.xPos - (self.sideLength / 2.0)
        right  = self.xPos + (self.sideLength / 2.0)
        top    = self.yPos - (self.sideLength / 2.0)
        bottom = self.yPos + (self.sideLength / 2.0)

        if self.isDisabled:
            self._justReleased = False
            self._isPressed    = False
            self._isHovered    = False


        else:
            if mouseX > left and mouseX < right and mouseY > top and mouseY < bottom:
                if mousePressed and mouseButton == LEFT:
                    if self._isHovered:
                        self._isHovered = False
                        self._isPressed = True
                else:
                    if self._isPressed:
                        self._isHovered = True
                        self._isPressed = False
                        self._justReleased = True
                    else:
                        self._isHovered = True
                        self._justReleased = False
            else:
                self._isHovered = False
                self._isPressed = False


            if self._justReleased:
                self.isTicked = not self.isTicked
