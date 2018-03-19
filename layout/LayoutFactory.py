from Utils.Layout import Layout
class LayoutFactory:

    def createLayout(layoutFile):
        return Layout.fromFile(layoutFile)
    