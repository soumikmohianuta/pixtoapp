from RectUtils import RectUtil
from Utils import ImageUtil
from Utils import Constants
from Utils import XmlUtil,TextUtils
from Utils import ColorUtil
from Utils.ColorUtil import ColorWrapper, CColor
from RectUtils.RectView import RectView
import sys
from layout import ListMetadataRoot
from Utils import GroupUtil, Environment
from resource.StyleWriter import StyleWriter
from resource.ColorWriter import ColorWriter
from resource.AndroidManifestWriter import AndroidManifestWriter
from resource.StringWriter import StringWriter
from ocr import TesseractOCR
from layout import ClosestDistanceInfo
#from resource import Color
from functools import cmp_to_key
from RectUtils.RectViewUtil import ListInfo, ListItemInfo, ListItemMetadata, ListItemType, ListMetadataRoot, IconInfo, ImageInfo
import RectUtils.RectViewUtil as RectViewTypes
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from layout import AlignGroups
import layout.LayoutHelper as LayoutHelper
#from .AlignGroups import AlignBottomGroup, AlignLeftGroup, AlignRightGroup, AlignTopGroup
from RectUtils.Rect import Rect



class ElementInfo :
    def __init__(self, element,  _id) :
        self.element = element
        self._id = _id
        
class ListWrapper :

    def __init__(self, _list):
        self._list = _list
        self.alignmentType = -1
        
    def size(self) :
        return len(self._list)
        
#@Override
    def __eq__(self,obj) :
        if obj is None:
            return self.size() == 0
        elif type(obj) != type(self):
            return False
        else:
            return self._list != obj._list
            
    def __hash__(self):
        return self._list
        
class LayoutCreator :

    
    def __init__(self, rootView,   appName, ocr,  drawableWriter, image, outProjectFolder,dipCalculator):
#        self.mScreenshotProcessor = screenshotProcessor
        self.mRootView = rootView
        self.mOcr = ocr
        self.mDrawableWriter = drawableWriter
        self.mImage = image
        self.mOutProjectFolder = outProjectFolder
        self.mDipCalculator = dipCalculator
        self.mWriter = StringWriter(appName)
        self.mStyleWriter =  StyleWriter()
        self.mColorWriter =  ColorWriter()
        self.mAndroidManifestWriter = AndroidManifestWriter(outProjectFolder)
        self.mIdMap = {}
        self.interestedIcons = {}
        self.mDrawableMap = {}
        self.mListViews = []

        self.mDefaultAlignThreshold = self.mDipCalculator.dipToWidthPx(Constants.DEFAULT_ALIGN_THRESHOLD)
        self.mDefaultEqualTheshold = self.mDipCalculator.dipToWidthPx(Constants.DEFAULT_EQUAL_THRESHOLD)
        self.mGroupDistanceVerticalTheshold = self.mDipCalculator.dipToHeightPx(Constants.GROUP_DISTANCE_VERTICAL_THRESHOLD)
 

#        @Override
    def sameGroup(self, element1,element2) :
        return RectUtil.equal_wthres(element1, element2, self.mDefaultEqualTheshold)
        
    
    
    

    def createDocument(self):
#        self.writeHierarchyLog("Un Categorized")
        self.pruneBasic(self.mRootView)
#        self.writeHierarchyLog("Categorized")
                
#        self.pruneToCreateGroupText(self.mRootView)

#        self.pruneToCreateListItemsHasDrawable(self.mRootView, self.mDrawableMap.values(), 0)

#        self.pruneToCreateListItemsHasViewsSameSize(self.mRootView, self.mDrawableMap.values(), self.mDefaultAlignThreshold)

        for i in range(len(self.mListViews)):
            listMetadata = self.mListViews[i]
            self.updateListContent(listMetadata, i)
        
        _map = {}
        
#        self.updateColorBackground(self.mRootView)

        rootElement = XmlUtil.createRoot(self.mDipCalculator, LayoutHelper.FRAMELAYOUT_ELEMENT, self.mRootView, self.mColorWriter)
        self.addChildrenLayout(rootElement, self.mRootView, 0, 0, _map)
        
        return rootElement
    
    
    def writeHierarchyLog(self,_id, clearContent= False):
        colListmap = {}


        self.logHierarchy(self.mRootView,colListmap)
        ImageUtil.logDrawViewColor(colListmap,_id,self.mImage, clearContent)

   
    def  logHierarchy(self,rootView, colListmap):
        if(rootView.mType == RectViewTypes.VIEW_TYPE_TEXT):
            colListmap[rootView]= ColorUtil.cColortoInt(CColor.Red) 
        elif(rootView.mType == RectViewTypes.VIEW_TYPE_IMAGE):
            colListmap[rootView]= ColorUtil.cColortoInt(CColor.Blue) 
        else:
            colListmap[rootView]= ColorUtil.cColortoInt(CColor.Black) 
            

        for child in rootView.mChildren:
            self.logHierarchy(child,colListmap)

    def logListOverlay(self) :
        isdebugMode = False

        if(isdebugMode):
            ImageUtil.log(RectUtil.toMapRects(self.mRootView),"pruneToCreateGroupTextWithList", self.mImage, True)
            ImageUtil.log(RectUtil.toMapRects(self.mRootView), self.mOutLogFolder, self.mFileName,"WithListOverlay", self.mImage, False)
    

    def updateColorBackground(self, root) :
        self.updateColorBackgroundInternal(root)
    

    def updateColorBackgroundInternal(self, rectViewParent) :

        if(rectViewParent.mType == RectViewTypes.VIEW_TYPE_TEXT):
            color = ColorUtil.findDominateColorForTextView(rectViewParent, self.mImage)
            rectViewParent.mColor = color[0]
            rectViewParent.textColor = color[1]
        else:
            color = ColorUtil.findDominateColor(rectViewParent, self.mImage)
            rectViewParent.mColor = color
        children = rectViewParent.mChildren
        for rectView in children:
#            if rectView.mType != RectViewTypes.VIEW_TYPE_IMAGE:
                self.updateColorBackgroundInternal(rectView)
        
    
    def resetIdMap(self) :
        self.mIdMap = {}
    
    def logList(self, _id) :

        # http:#www.color-hex.com/color/472300
        colorWrapper = ColorWrapper(ColorUtil.to(71,35, 0, 0), 1)
        additionColor = ColorWrapper(ColorUtil.to(CColor.Blue), 1)
        iRectBaseViews = []
        iRectAddtionalViews = []
        for listMetadata in self.mListViews:
            for itemMetadata in listMetadata.mListItemMetadatas:
                iRectBaseViews.extend(itemMetadata.baseViews)
                iRectAddtionalViews.extend(itemMetadata.additionalViews)
            
        
        _map = {}
        _map[colorWrapper] = iRectBaseViews
        ImageUtil.log(_map, _id + "_base", self.mImage, True)
        _map[additionColor] = iRectAddtionalViews
        ImageUtil.log(_map, _id, self.mImage, True)
    

    def pruneToCreateListItemsHasViewsSameSize(self, rectView, drawbleListCollections, defaultThresholdAlignment) :
        drawableLists = self.getDrawbleList(drawbleListCollections)

        self.pruneToCreateListItemsHasViewsSameSizeInternal(rectView, drawableLists, defaultThresholdAlignment)
    

    def pruneToCreateListItemsHasViewsSameSizeInternal(self, rectView,  baseLists, defaultThresholdAlignment) :
        
        if (rectView.mType == RectViewTypes.VIEW_TYPE_LIST_ITEM) :
            return
        
        _list = []
        _list.extend(baseLists)

        for childRectView in rectView.mChildren :
            self.pruneToCreateListItemsHasViewsSameSizeernal(childRectView, _list, defaultThresholdAlignment)
        
        groups = GroupUtil.group(rectView.mChildren, self.sameGroup)

        for viewList in groups :
            if (self.isValidList(viewList)) :
                _list.append(viewList)
            
        

        self.createListItemForView(rectView, _list, defaultThresholdAlignment)
    

    def pruneToCreateListItemsHasDrawable(self, rootView, drawbleListCollections, defaultThresholdAlignment) :

        drawbleLists = self.getDrawbleList(drawbleListCollections)
        self.pruneToCreateListItemsHasDrawableernal(rootView, drawbleLists, defaultThresholdAlignment)
        return drawbleLists
    

    def pruneToCreateListItemsHasDrawableernal(self,rectView, drawableLists, defaultThresholdAlignment) :
        if (rectView.mType == RectViewTypes.VIEW_TYPE_LIST_ITEM) :
            return
        
        for childRectView in rectView.mChildren:
            self.pruneToCreateListItemsHasDrawableernal(childRectView, drawableLists, defaultThresholdAlignment)
        
        self.createListItemForView(rectView, drawableLists, defaultThresholdAlignment)
    


    def createListItemForView(self, rectView, baseLists, defaultThresholdAlignment) :
        # Check to see if there is a list of drawable belong to one view
        # then we remove this list
        # We only find one for now
        matchedBaseLists = []
        removedList = []
        for drawableList in baseLists:
            if (RectUtil.containAll(rectView, drawableList)) :
                matchedBaseLists.append(ListWrapper(drawableList))
                removedList.append(ListWrapper(drawableList))
            
        

        # First remove approval list
        baseLists= [ x for x in baseLists if x not in removedList]
        removedList = []
        if len(matchedBaseLists) > 0:
            for matchedBaseList in matchedBaseLists:
                # System.out.prln("Found a list of: " + rectView.bound()
                # + ", list: " + matchedBaseList.size() + ", "
                # + matchedBaseList)
                # First make sure these are repeated icons of list items
                # Make sure they align either LEFT-RIGHT or TOP-BOTTOM
                checkValidList = False
                alignmentType = RectUtil.getAlignmentType(matchedBaseList._list, defaultThresholdAlignment)
                matchedBaseList.alignmentType = alignmentType
                if(alignmentType == RectUtil.ALIGNMENT_RIGHT):
                    # System.out.prln("Align LEFT and RIGHT")
                    # We sort them vertically
                    matchedBaseList._list.sort(key=cmp_to_key(RectUtil.getTopBottomComparator()))
                    if len(matchedBaseList) >= Constants.LAYOUT_MIN_ACCEPTABLE_LIST_SIZE :
                        distances = set()
                        for i in range(len(matchedBaseList)):
                            distances.add(RectUtil.verticalDistance(matchedBaseList._list[i + 1],matchedBaseList._list[i]))
                                
                            if len(distances) == 1 :
                            # Perfect
                                checkValidList = True
                            elif len(distances) >= 2 :
                            # it is okay to have more than 2 distance, but the
                            # different cannot too much
                            # we set here is <= half of the biggest distance
                                satisfy = True
                                lDistances = []
                                for  i in range(len(lDistances)-1) :
                                    first = lDistances[i]
                                    second = lDistances[i + 1]
                                    difference = abs(first - second)
                                    if (difference >= max(first, second) / 2) :
                                        satisfy = False
                                        break
                                checkValidList = satisfy
                        
                    else :
                        checkValidList = False
                
                if(alignmentType ==  RectUtil.ALIGNMENT_BOTTOM):
                    # System.out.prln("Align TOP and BOTTOM")
                    # We sort them horizontally
                    matchedBaseList._list.sort(key=cmp_to_key(RectUtil.getLeftRightComparator()))
                    if len(matchedBaseList) >= Constants.LAYOUT_MIN_ACCEPTABLE_LIST_SIZE :
                        distances = set()
                        for i in range(len(matchedBaseList)- 1):
                            distances.add(RectUtil.horizontalDistance(matchedBaseList._list[i + 1],matchedBaseList._list[i]))
                        
                        if len(distances)== 1 :
                            # Perfect
                            checkValidList = True
                        elif len(distances) >= 2 :
                            # it is okay to have more than 2 distance, but the
                            # different cannot too much
                            # we set here is <= half of the biggest distance
                            satisfy = True
                            lDistances = []
                            for i in range(lDistances)-1 :
                                first = lDistances[i]
                                second = lDistances[i + 1]
                                difference = abs(first - second)
                                if (difference >= max(first, second) / 2) :
                                    satisfy = False
                                    break
                                
                            
                        checkValidList = satisfy
                        
                    else :
                        checkValidList = False
                    
                # Now put them in a groups
                if (not checkValidList) :
                    removedList.append(matchedBaseList)                            

            # We only support one list for now, and only allow has the same
            # size
            #   maxSize = RectUtil
            # .maxSizeListWrapper(matchedBaseLists)
            #
            # for ( ListWrapper list : matchedBaseLists) :
            # if (list.size() != maxSize) :
            # removedList.add(list)
            # 
            # 
        matchedBaseLists= [ x for x in matchedBaseLists if x not in removedList]
        
            # Split list to multiple with different alignment type
        mapTypeList = {}
        for listWrapper in matchedBaseLists:
            ls = mapTypeList[listWrapper.alignmentType]
            if (ls == None) :
                ls = []
                mapTypeList[listWrapper.alignmentType] =  ls
            ls.append(listWrapper)
                        
#            We have enough base item here already
                # Now we try to get as much as ImageView base, as possible            

        for entry in mapTypeList:
            entryKey = [x for x in entry]
            entryValue = [entry(x) for x in entry]
            maxSize = RectUtil.maxSizeListWrapper(mapTypeList[entry])
            newLists = []
            for listWrapper in entryValue:
                if len(listWrapper) == maxSize:
                    newLists.append(listWrapper)
                    
            if len(newLists) <= 1:
                    # System.out
                    # .prln("*We need more list here let get the list = size - 1")
                    # We need more list here let get the list = size - 1
                for listWrapper in entryValue :
                        if len(listWrapper) == maxSize - 1:
                            newLists.append(listWrapper)
                        
            self.prepareCreateListView(rectView, newLists, entryKey)
                        

    def prepareCreateListView(self, rectView, matchedBaseLists, alignmentType) :
        largestSublists = set()

        # Remove lists which are subset of other lists
        for list1 in matchedBaseLists:
            # Remove sublists of list1 first
            subLists = set()
            for list2 in largestSublists:
                if all(x in list1._list for x in list2._list):
                    subLists.add(list2)
                
            
        largestSublists.remove(subLists)

            # Will add list 1 to largestSublists if there is no list which
            # contains list1
        shouldAddList1 = True

        for list2 in largestSublists:
            if all(x in list1._list for x in list2._list):
                shouldAddList1 = False
                
            
        if (shouldAddList1) :
            largestSublists.add(list1)
            
        

        matchedBaseLists =  []
        matchedBaseLists.extend(largestSublists)

        # for ( ListWrapper matchedDrawableList : matchedBaseLists) :
        # System.out.prln("After still: " + rectView.bound() + ", list: "
        # + matchedDrawableList.size() + ", " + matchedDrawableList)
        # 

        notDrwableRectViews = []
        for _list in matchedBaseLists:
            notDrwableRectViews = [x for x in notDrwableRectViews if x not in _list._list]        

        minSize = RectUtil.minSizeListWrapper(matchedBaseLists)

        # Now take min size as the base then group them
        groups = []
        for i in range(len(minSize)) :
            listItem = ListItemMetadata()
            for matchedDrawableList in matchedBaseLists:
                listItem.baseViews.append(matchedDrawableList_list[i])
            
            # listItem.baseViews.size > 0
            listItem.bound = RectUtil.findBoundRectangle(listItem.baseViews)
            groups.append(listItem)
        
        # Find views overlap these bound of each list add put them o
        # the group
        processedView = []
        for listItem in groups:
            for notDrawableView in notDrwableRectViews:
                if (not processedView.contains(notDrawableView)and RectUtil.ersectsNotInclude(listItem.bound,notDrawableView.bound())) :
                    listItem.additionalViews.add(notDrawableView)
                    processedView.add(notDrawableView)                            
        
        for listItem in groups:
            # We got a new bound here, this time more aggressive => we
            # only include view belong to
            # to the new bound
            if len(listItem.additionalViews)> 0:
                listItem.bound = RectUtil.union(listItem.bound,RectUtil.findBoundRectangle(listItem.additionalViews))
            
            for notDrawableView in notDrwableRectViews:
                if (not processedView.contains(notDrawableView) and RectUtil.contains(listItem.bound,notDrawableView.bound())) :
                    listItem.additionalViews.add(notDrawableView)
                    processedView.add(notDrawableView)    

        # check if this list is the expand version of the previous list
        # find the first list which have same size
        expandingList = None
        for i in len(self.mListViews) :
            listItemMetadatas = self.mListViews[i].mListItemMetadatas
            if len(listItemMetadatas) == len(groups) :
                includeMetada = True
                for j in range(len(groups)) :
                    if (not (groups[j].baseViews.containsAll(listItemMetadatas[j].baseViews) and groups[j].baseViews.size() > listItemMetadatas[j].baseViews.size())) :
                        includeMetada = False
                if (includeMetada) :
                    expandingList = self.mListViews[i]
                    break
                
            
        

        if (expandingList != None) :
            # System.out.prln("Expanding: " + rectView)
            self.mListViews[self.mListViews.index(expandingList)]= ListMetadataRoot(rectView, groups, alignmentType)
        else :
            validList = True
            for listItem in groups:
                allViews = []
                allViews.extend(listItem.additionalViews)
                bound = RectUtil.findBoundRectangle(allViews)
                countListView = 0
                for listMetadata in self.mListViews:
                    # contain entire a list is okay but only one list item
                    # is not okay
                    if (RectUtil.ersects(listMetadata.bound(), bound) or RectUtil.contains(listMetadata.bound(), bound)) :
                        countListView += countListView
                if (countListView >= 1) :
                    validList = False
                    break
                
            
            if (validList) :
                if len(groups) > 0 :
                    self.mListViews.append(ListMetadataRoot(rectView, groups,alignmentType))
        invalidLists = []

        for listMetadataRoot in self.mListViews:
            if (not self.validateList(listMetadataRoot)) :
                invalidLists.append(listMetadataRoot)
        
        self.mListViews = [x for x in self.mListViews if x not in invalidLists]
        

    def validateList(self, listMetadataRoot) :
        alignmentType = listMetadataRoot.mAlignmentType
        groups = listMetadataRoot.mListItemMetadatas

        # We only support more than one base view
        for listItem in groups:
            if len(listItem.baseViews) <= 1 :
                return False    
        # and all base views of each list item should have same size
        currentSize = -sys.maxint - 1
        
        for listItem in groups:
            if (currentSize == -sys.maxint - 1) :
                currentSize = len(listItem.baseViews)
            elif (currentSize != listItem.baseViews.size()) :
                return False

        # They have to be align
        if alignmentType == RectUtil.ALIGNMENT_RIGHT:
            for i in range(len(groups) - 1):
                current = groups[i]
                _next = groups[i + 1]
                for currentBase in current.baseViews:
                    for nextBase in _next.baseViews:
                        if (not RectUtil.above(currentBase, nextBase)) :
                            return False
        if alignmentType == RectUtil.ALIGNMENT_BOTTOM:
            for i in range(len(groups) - 1):
                current = groups[i]
                _next = groups[i + 1]
                for currentBase in current.baseViews:
                    for nextBase in _next.baseViews:
                        if (not RectUtil.onTheLeft(currentBase, nextBase)) :
                            return False
                        
        return True
    

    def updateListContent(self, listMetadata, index):
        if len(listMetadata.mListItemMetadatas) == 0:
            return None
        
        listItemViews = []
        for listItem in listMetadata.mListItemMetadatas :
            allViews = []
            allViews.extend(listItem.additionalViews)
            listItemView = self.groupViews(listMetadata.mParent,allViews, RectViewTypes.VIEW_TYPE_LIST_ITEM, 1)
            listItemViews.append(listItemView)
            # System.out.prln("Valid List: " + listItem.bound)
        
        listView = self.groupViews(listMetadata.mParent,listItemViews, RectViewTypes.VIEW_TYPE_LIST, 1)
        listView.mListInfo.xmlId = self.getListViewXmlId(index)
        listView.mListInfo.listItems = listItemViews
        listView.mListInfo.listItemMetadatas = listMetadata.mListItemMetadatas
        for listItemView in listItemViews:
            listItemView.mListItemInfo.parent = listView
        

        # Create list layout code
        self.createListLayoutCode(listMetadata, index, listView)
        return listView
    

    def createListLayoutCode(self, listMetadata, index, listView):
        baseListItemMetadata = listMetadata.mListItemMetadatas[0]
#        document = XmlUtil.createDocument()
        rootView = RectView(baseListItemMetadata.bound, None)
        for rectView in baseListItemMetadata.baseViews:
            rootView.addChild(rectView)
        
        for rectView in baseListItemMetadata.additionalViews:
            rootView.addChild(rectView)
        
        rootView.mChildren.sort(key=cmp_to_key(RectUtil.getTopBottomComparator()))
        rootView.mChildren.sort(key=cmp_to_key(RectUtil.getLeftRightComparator()))
        
        rootElement = XmlUtil.createRoot(self.mDipCalculator, FRAMELAYOUT_ELEMENT, rootView, self.mColorWriter)
        _map = {}
        self.addChildrenLayout(rootElement, rootView, listView.x,listView.y, _map)
        
        rectViews = RectUtil.toRects(rootView)
        rectViews.remove(rootView)
        XmlUtil.writeDocument(rootView, self.mOutProjectFolder+ Constants.DEFAULT_LAYOUT_PATH + "/"+ Constants.DEFAULT_LAYOUT_LIST_PREFIX + index + ".xml")

    def getListViewXmlId(self,index):
        return "ListView_" + index    

    def getDrawbleList(self, drawableLists) :
        # Find lists more than two views
        viewLists = []
        for viewList in drawableLists:
            if (self.isValidList(viewList)) :
                viewLists.append(viewList)
                    
        return viewLists
    

    def isValidList(self, viewList) :
        if len(viewList) < Constants.LAYOUT_MIN_ACCEPTABLE_LIST_SIZE :
            return False
        
        bound = RectUtil.findBoundRectangle(viewList)
        heightDip = self.mDipCalculator.pxToHeightDip(bound.height)
        widthDip = self.mDipCalculator.pxToWidthDip(bound.width)
        area = heightDip * widthDip
        return area >= Constants.MIN_SINGLE_LIST_AREA
    

    def pruneToCreateGroupText(self,view) :
        self.pruneToCreateGroupInternal(view)
    

    def pruneToCreateGroupInternal(self,rectView) :
        for childRectView in rectView.mChildren:
            self.pruneToCreateGroupInternal(childRectView)
        
        processedViews = []
        newViews = []
        ###CHECK MOHIAN
        alignLeftGroup = AlignGroups.AlignLeftGroup(self.mDefaultAlignThreshold, self.mGroupDistanceVerticalTheshold)
        alignRightGroup = AlignGroups.AlignRightGroup(self.mDefaultAlignThreshold, self.mGroupDistanceVerticalTheshold)
        self.groupChildrenTextViews(alignLeftGroup, rectView, processedViews,newViews)
        self.groupChildrenTextViews(alignRightGroup, rectView, processedViews,newViews)

        # groupChildrenViews(alignTopGroup, rectView, processedViews)
        # groupChildrenViews(alignBottomGroup, rectView, processedViews)
    

    def groupChildrenTextViews(self, alignGroup, rectView, processedViews, newViews) :
        currentChildren = []
        currentChildren.extend(rectView.mChildren)
        processedViews = [x for x in processedViews if x not in processedViews]
        
        alignViews = GroupUtil.group(currentChildren,alignGroup.sameGroup)
        for _list in alignViews:
            # Sort the item vertically
            _list.sort(key = alignGroup.sortComparator())
            if len(_list) > 0 :
                newChildren = []
                curent = _list[0]                
                newChildren.append(curent)
                for i in  range(len(_list)):
                    _next = _list[i]
                    # we only merge text box
                    if (self.isTextViewOrTextViewContainer(curent) and self.isTextViewOrTextViewContainer(_next) and alignGroup.apply(ClosestDistanceInfo.ClosestDistanceInfo(curent,_next, rectView.mChildren))) :
                        newChildren.append(_next)
                    else :
                        # we store the old group
                        newView = self.groupViews(rectView,newChildren, RectViewTypes.VIEW_TYPE_DEFAULT, 2)
                        if (newView != None) :
                            newViews.append(newView)
                        
                        processedViews.extend(newChildren)
                        # this may be a new group
                        newChildren = []
                        newChildren.append(_next)
                    
                    curent = _next
                
                    newView = self.groupViews(rectView, newChildren, RectViewTypes.VIEW_TYPE_DEFAULT, 2)
                    if (newView != None) :
                        newViews.append(newView)
                    processedViews.extend(newChildren)
            
        
    

    def isTextViewOrTextViewContainer(self, rectView) :
        if (rectView.mType == RectViewTypes.VIEW_TYPE_TEXT) :
            return True
        
        if len(rectView.mChildren) == 1 and rectView.mChildren[0].mType == RectViewTypes.VIEW_TYPE_TEXT:
            return RectUtil.same(rectView, rectView.mChildren[0], 0.1)
        
        return False
    
    def useTransparentBackground(self,rectView) :
        return rectView.mType == RectViewTypes.VIEW_TYPE_LIST or rectView.mType == RectViewTypes.VIEW_TYPE_IMAGE
    

    def pruneBasic( self,rootView) :
        self.pruneBasicInternal(None, rootView)

        # TODO: carefully test this logic
        # If this view only have one children it the text view
        # And it size almost the same as the textview, so why we need
        # this container then, just replace it with the text view
        self.pruneRemoveRedundantViewsInternal(None, rootView)
    

    def pruneRemoveRedundantViewsInternal(self, parent,view) :
        if (parent != None) :
            # TODO: carefully test this logic
            # (1) If this view only have one children it the text view
            # And it size almost the same as the textview, so why we need
            # this container then, just replace it with the text view
            if len(view.mChildren) == 1 :
                child = view.mChildren[0]
                if child.mType == RectViewTypes.VIEW_TYPE_TEXT and RectUtil.same(view, child, 0.5) :
                    return (view, child)
                elif child.mType == RectViewTypes.VIEW_TYPE_IMAGE and RectUtil.same(view, child, 0.5) :
                    return (view, child)

        # recursive to children

#        children = view.mChildren
        swapLists = []
        
        for childView in view.mChildren:
            swapList = self.pruneRemoveRedundantViewsInternal(view, childView)
            swapLists.append(swapList)
        

        for pair in swapLists:
            view.mChildren = [x for x in view.mChildren if x is not pair[0]]
            if pair[1] is not None:
                view.mChildren.append(pair[1])
        
        return (None , None)
    
    def isFullImage(self, view):
        if view.hasTextRecusive():
            return False
        if len(view.mChildren)==0: 
            return True
        
        
        if(ColorUtil.isAContainer(view, self.mImage)):
            return False
        else:
            return True
        
        
#        if len(view.mChildren)==1:
#            # check if center aligned
#           centerAlign= 2 * view.mChildren[0].x + view.mChildren[0].width + 2 * view.mChildren[0].y + view.mChildren[0].height - view.width - view.height
#           if(centerAlign == 0):
#               return False
#           else:
#               return True
#        
#        childrens = []
#        childrens.extend(view.mChildren)
#        RectUtil.sortLeftRightTopBottom(childrens)
#        curChild = childrens[0]
#        countAligned = 1
#        for i in range(1,len(childrens)):
#            _next = childrens[i]
#            if RectUtil.alignLeft(curChild, _next, self.mDefaultAlignThreshold):
#                countAligned = countAligned + 1 
#            else:
#                if RectUtil.alignBottom(childrens[0], _next, self.mDefaultAlignThreshold):
#                    countAligned = countAligned + 1 
#            curChild = _next
#            
#           
#        if(countAligned == len(childrens)):
#            
#            return False
#        else:
#            return True
            
            
    

    def pruneBasicInternal(self,parent,view) :
        # TODO: if this view is too small and it has no children,so we don't
        # need them
        if self.mDipCalculator.isViewToBeIgnore(view.width, view.height) :
            if (parent != None) :
                parent.mChildren.remove(view)
            return
#        
#
        allChildrenAreTooSmall = self.isAllChildrenTooSmall(view)

        if not allChildrenAreTooSmall and len(view.mChildren) != 0 :
            removedChildren = []
            for childView in view.mChildren:
                if self.mDipCalculator.isViewToBeIgnore(childView.width,childView.height) :
                    removedChildren.append(childView)
                
            
            view.mChildren = [x for x in view.mChildren if x not in removedChildren]
            for childView in view.mChildren:
                self.pruneBasicInternal(view, childView)
#                        # add this drawable if we did not want to show any children
#        # here
#          
        isAImageView = self.isFullImage(view)
        if isAImageView:      
#        if not view.hasText() and allChildrenAreTooSmall and len(view.mChildren) == 0 :
            currentMat = ImageUtil.getImageFromRect(self.mImage, view.bound())
            iconInfo =  IconInfo(currentMat)
            drawableId = ""
            if iconInfo in self.interestedIcons:
                drawableId = self.interestedIcons[iconInfo]
            viewsSameDrawable = None
            if (TextUtils.isEmpty(drawableId)) :
                drawableId = self.mDrawableWriter.addResourceDirectly(currentMat,view)
                self.interestedIcons[iconInfo] = drawableId
                viewsSameDrawable = []
                self.mDrawableMap[drawableId] =  viewsSameDrawable
            else :
                viewsSameDrawable = self.mDrawableMap[drawableId]
            
            view.mType = RectViewTypes.VIEW_TYPE_IMAGE
            view.mImageInfo.iconInfo = iconInfo
            view.mImageInfo.drawableId = drawableId
            view.mChildren = []
            viewsSameDrawable.append(view)
        elif view.hasTextRecusive() :
            # process text view
            textWithLocations = view.mTextWithLocations
            view.mColor = ColorUtil.findDominateColor(view,self.mImage)
            for textWrapper in textWithLocations:
                newHeight = TesseractOCR.increaseHeight(textWrapper.height)
                textView = textWrapper.boundRectView
                newY = textView.y - (newHeight - textView.height )/ 2.0
                textView.y = newY
                textView.x = textWrapper.x
                textView.width = textWrapper.width
                textView.height =  newHeight
                textView.mType = RectViewTypes.VIEW_TYPE_TEXT
                textView.mTextInfo.textWrapper = textWrapper
                textView.rect = Rect(textView.x, textView.y, textWrapper.width, textView.height)
                color = ColorUtil.findDominateColorForTextView(textView, self.mImage)
                textView.mColor = color[0]
                textView.textColor = color[1]
#                textView.mColor = ColorUtil.findDominateColor(textView,self.mImage)
                view.addChild(textView)
                
                
#                currentMat = ImageUtil.getImageFromRect(self.mImage, textView.bound())
#                iconInfo =  IconInfo(currentMat)
#                drawableId = ""
#                if iconInfo in self.interestedIcons:
#                    drawableId = self.interestedIcons[iconInfo]
#                    viewsSameDrawable = None
#                if (TextUtils.isEmpty(drawableId)) :
#                    drawableId = self.mDrawableWriter.addResourceDirectly(currentMat,view)
#                    self.interestedIcons[iconInfo] = drawableId
#                    viewsSameDrawable = []
#                    self.mDrawableMap[drawableId] =  viewsSameDrawable
#                else :
#                    viewsSameDrawable = self.mDrawableMap[drawableId]
#            
#                textView.mType = RectViewTypes.VIEW_TYPE_IMAGE
#                textView.mImageInfo.iconInfo = iconInfo
#                textView.mImageInfo.drawableId = drawableId
#                textView.mChildren = []
#                viewsSameDrawable.append(textView)

                
                
            
            # Update Bound of parent text view
            if len(view.mChildren) > 0 :
                allViews = []
                allViews.extend(view.mChildren)
                allViews.append(view)
                view.bound = RectUtil.findBoundRectangle(allViews)
            
        
    

    def isAllChildrenTooSmall(self,rectView) :
        children = rectView.mChildren
        for childView in children:
            if not self.mDipCalculator.isViewToBeIgnore(childView.width,childView.height) :
                return False                    
        return True
           

    def getId(self,  elementName,  rawView) :
        index= 0
        if elementName in self.mIdMap:
            currentIndex = self.mIdMap[elementName]
            index = currentIndex + 1
        
        self.mIdMap[elementName] =  index
        return elementName + "_" + str(index)
    

    def addChildrenLayout(self, element, rectView,   parentLeft,   parentTop, rectViewElementInfoMap) :
        # Setting background
        if (self.useTransparentBackground(rectView)) :
            XmlUtil.addBackgroundColor(element, ColorUtil.toInt(0, 255, 255, 255), self.mColorWriter)
#        elif (RectViewTypes.isContanerView(rectView)) :
        # We always want to genenate background regard less of the respect
        # ratioand Environment.get().getValue(Environment.KEY_KEEP_ASPECT_RATIO) == Boolean.TRUE
        # We will not do this if ratio is between input image and output is the same
#            bound = ImageUtil.getImageFromRect(self.mImage, rectView)
#            # We remove children here using 4 layer channel So we have to make sure that when we save it we will not Adding anymore layer
#            newImageBackground = ImageUtil.removeChildren(bound, rectView)
#            drawableId = self.mDrawableWriter.addResourceDirectly(newImageBackground, rectView)
#            XmlUtil.addBackroundImage(element, drawableId)

        else :
            XmlUtil.addBackgroundColor(element, rectView.mColor,self.mColorWriter)
        
        for childRectView in rectView.mChildren:
            _id = ""
            # list view has it own index
            if (childRectView.mType == RectViewTypes.VIEW_TYPE_LIST) :
                _id = childRectView.mListInfo.xmlId
            else :
                _id = self.getId(LayoutHelper.FRAMELAYOUT_ELEMENT, childRectView)
            

            marginLeft = childRectView.x - parentLeft
            marginTop = childRectView.y - parentTop
            childElement = None
            if (self.useTransparentBackground(childRectView)) :
                childElement = XmlUtil.addElement(self.mDipCalculator, element,self.getElementTypeForRect(childRectView), childRectView, marginLeft, marginTop, _id)
            else :
                childElement = XmlUtil.addElement(self.mDipCalculator, element,self.getElementTypeForRect(childRectView), childRectView,marginLeft, marginTop, _id, self.mColorWriter)
            
            rectViewElementInfoMap[childRectView] = ElementInfo( childElement, _id)
            self.addChildrenLayout(childElement, childRectView, childRectView.x, childRectView.y, rectViewElementInfoMap)
        

        # image view
        if (rectView.mType == RectViewTypes.VIEW_TYPE_IMAGE) :
              drawableId = self.interestedIcons.get(rectView.mImageInfo.iconInfo)
              element.tag = Constants.ELEMENT_IMAGE_VIEW
              XmlUtil.addImageDrawable(element, drawableId)
            # override attributes
              XmlUtil.removeAttribute(element, Constants.ATTRIBUTE_BACKGROUND)
              _id = self.getId(Constants.ELEMENT_IMAGE_VIEW, rectView)
              XmlUtil.addId(element, _id)
              XmlUtil.addScaleType(element, "fitXY")
              rectViewElementInfoMap[rectView] = ElementInfo(element, _id)
        elif (rectView.mType == RectViewTypes.VIEW_TYPE_TEXT) :

             textWrapper = rectView.mTextInfo.textWrapper
             stringId = self.mWriter.addResource(textWrapper.text)
             rectView.mTextInfo._id = stringId
             element.tag = Constants.ELEMENT_TEXT_VIEW
             if (Environment.getValue(Environment.KEY_TEXT_WIDTH_WRAP_CONTENT) == True) :
                XmlUtil.addSize(self.mDipCalculator, element,
                        Constants.ATTRIBUTE_WRAP_CONTENT, rectView.height)
             else :
                 XmlUtil.addSize(self.mDipCalculator, element, rectView.width,
                        rectView.height)

             XmlUtil.addBackgroundColor(element, rectView.mColor,self.mColorWriter)
             element.set(Constants.ATTRIBUTE_TEXT, XmlUtil.getReferenceResourceId(stringId))
             _id = self.getId(Constants.ELEMENT_TEXT_VIEW, rectView)
             XmlUtil.addId(element, _id)
             textAttributes = textWrapper.getTextAttributes(self.mOcr,rectView.height)
             XmlUtil.addTextColor(element, rectView.textColor,self.mColorWriter)
             stypeId = self.mStyleWriter.addResource(textAttributes)
             element.set(Constants.ATTRIBUTE_STYLE, XmlUtil.getReferenceStyleId(stypeId))
             rectViewElementInfoMap[rectView] = ElementInfo(element, _id)
             
        
        
    

    def getElementTypeForRect(self, rectView) :
        return LayoutHelper.FRAMELAYOUT_ELEMENT
    
    def groupViews(self,parentView, newChildren,   viewTypeRect, minChidren) :

        if len(newChildren) >= minChidren:
             newBound = RectUtil.findBoundRectangle(newChildren)
             newParent = RectView(newBound, None)
             newParent.mType =viewTypeRect
             for rectView in newChildren :
                 newParent.addChild(rectView)
            
            # replace the parent at the location of the first child
             if newChildren[0] in parentView.mChildren:
                 indexOf = parentView.mChildren.index(newChildren[0])
#             if indexOf > 0 and indexOf < len(parentView.mChildren) :
                 parentView.mChildren[indexOf]= newParent
             else :
                 parentView.mChildren.append(newParent)
            
            # Now remove the rest
             parentView.mChildren = [x for x in parentView.mChildren if x not in newChildren] 

            # Make sure there is no view is hidden under the new parent
             insideViews = RectUtil.contain(newParent,parentView.mChildren)
             parentView.mChildren = [x for x in parentView.mChildren if x not in insideViews] 
             indexOfNewParent = parentView.mChildren.index(newParent)
             if (indexOfNewParent == len(parentView.mChildren) - 1) :
                parentView.mChildren.extend(insideViews)
             else :
                indexExtension = []
                indexExtension.extend(parentView.mChildren[:indexOfNewParent])
                indexExtension.extend(insideViews)
                indexExtension.extend(parentView.mChildren[indexOfNewParent:])
                parentView.mChildren = indexExtension
             return newParent
        
        return None
