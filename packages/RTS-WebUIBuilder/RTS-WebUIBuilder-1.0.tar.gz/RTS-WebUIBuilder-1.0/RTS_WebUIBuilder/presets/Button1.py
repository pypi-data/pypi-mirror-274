from ..RLabel import RLabel
from ..RBox import RBox
from ..RAdditions import rgba, rgb

class ButtonLeftImage:
    def __init__(self,imageSource:str, text:str, height:int=30, width:int=180,borderRadius:int=15, buttonBackground:str="rgba(255,255,255,1)", buttonForeground:str="rgba(0,0,0,1)")->None:

        self.button = button = RBox()
        button.style.draw(height=height, width=width)
        button.style.colorize(background=buttonBackground, color=buttonForeground)
        button.style.roundCorners(all=borderRadius)

        button.style.margin()

        buttonImage = RBox()
        buttonImage.style.draw(height=height, width=height)
        buttonImage.style.backgroundImage(imageSource)
        buttonImage.style.roundCorners(topleft=borderRadius, bottomleft=borderRadius)
        button.buttonImage = buttonImage

        buttonText = RLabel() 
        buttonText.displaytext = text
        buttonText.style.draw(height=height, width=f"calc(100% - {height}px)",moveX=height)
        buttonText.style.roundCorners(topright=borderRadius, bottomright=borderRadius)
        buttonText.style.margin()
        buttonText.style.padding()
        buttonText.style.alignment(align="center", justify="center")
        button.buttonText = buttonText
        #buttonText.style.colorize(background="red")