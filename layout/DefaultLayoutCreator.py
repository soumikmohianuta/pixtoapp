
from layout import LayoutCreator

class DefaultLayoutCreator(LayoutCreator.LayoutCreator):

    def __init__(self,rootView,  appName, ocr, drawableWriter, image, outProjectFolder, dipCalculator):
        super().__init__(rootView, appName, ocr, drawableWriter, image, outProjectFolder, dipCalculator)

