from layout.LayoutCreator import LayoutCreator
from RectUtils.RectView import RectView
from RectUtils import RectUtil
from Utils import XmlUtil
from . import RelativeLayoutFilter
from Utils import Constants
from functools import cmp_to_key
import sys
from layout import LayoutFilter
from Utils import TextUtils
from layout import RectViewWrapper
from RectUtils.Rect import Rect
from RectUtils.RectViewUtil import ListInfo, ListItemInfo, ListItemMetadata, ListItemType, ListMetadataRoot, IconInfo, ImageInfo
from layout import ListMetadataRoot 




class LayoutCreatorForList(LayoutCreator):

    LIST_VIEW_ELEMENT = "ListView"
    MAX_DISTANCE_RATIO_OF_LIST = 1/3

    def LayoutCreatorForList(self,rootView, appName, ocr, drawableWriter, image,fileName,  outLogFolder,  outProjectFolder, dipCalculator):
        super.__init__(rootView, appName, ocr, drawableWriter, image, fileName,
                outLogFolder, outProjectFolder, dipCalculator)
    

    #@Override
    def updateListContent(self, listMetadataRoot, index):
        groups = listMetadataRoot.getListItemMetadatas()
        aditionalListViewItemData = self.canGenerateListAndGetAdditionListInfo(listMetadataRoot)
        if (aditionalListViewItemData == None) :
            listView = self.updateListContent(listMetadataRoot, index)
            listView.getListInfo().valid = False
            return listView
        

        allViews = []
        for listItem in groups :
            allViews.extend(listItem.baseViews)
            allViews.extend(listItem.additionalViews)
            
        listView = self.groupViewsForList(listMetadataRoot.getParent(),
                allViews, RectView.VIEW_TYPE_LIST, 1)
        listView.getListInfo().xmlId = self.getListViewXmlId(index)
        listView.getListInfo().listItems = []
        listView.getListInfo().listItemMetadatas = groups

        self.createListLayoutCode(listView, listMetadataRoot,
                aditionalListViewItemData, index)

        listView.getListInfo().valid = True
        return listView
    

#    @Override
    def logListOverlay(self) :
        mapRects = RectUtil.toMapRects(self.mRootView)
        for metadataRoot in self.mListViews:
            for listItemMetadata in metadataRoot.getListItemMetadatas():
                mapRects.update(RectUtil.toMapRects(listItemMetadata.baseViews))
                mapRects.update(RectUtil.toMapRects(listItemMetadata.additionalViews))
                # Add List item color
                color = RectUtil.getColorWrapperBaseOnType(RectView.VIEW_TYPE_LIST_ITEM)
                iRects = mapRects[color]
                if (iRects == None) :
                    iRects = []
                    mapRects[color]  = iRects
                
                iRects.append(RectUtil.toIRect(listItemMetadata.bound))
                mapRects[color] =  iRects
            
        

#        imageUtil.log(mapRects, mOutLogFolder, mFileName,
#                "pruneToCreateGroupTextWithList", mImage, true, mScreenshotProcessor.getImageChangeListener() )
#
#        imageUtil.log(mapRects, mOutLogFolder, mFileName,
#                "pruneToCreateGroupTextWithListOverlay", mImage, false, mScreenshotProcessor.getImageChangeListener())
#    

    def groupViewsForList(self, parentView, newChildren, viewTypeRect, minChidren) :
        if len(newChildren) >= minChidren :
            bound = RectUtil.findBoundRectangle(newChildren)
            newParent = RectView(bound, None)
            newParent.mType = viewTypeRect
            # replace the parent at the location of the first child
            indexOf = parentView.mChildren.index(
                    newChildren[0])
            if indexOf > 0 and indexOf < len(parentView.mChildren) :
                parentView.mChildren[indexOf] = newParent
            else :
                parentView.mChildren.append(newParent)
            
            # Now remove the rest
            
            parentView.mChildren = [x for x in parentView.mChildren if x not in newChildren]

            # Make sure there is no view is hidden under the new parent
            insideViews = RectUtil.contain(newParent, parentView.mChildren)
            parentView.mChildren = [x for x in parentView.mChildren if x not in insideViews]
            indexOfNewParent = parentView.mChildren.index(newParent)
            if (indexOfNewParent == len(parentView.mChildren) - 1) :
                parentView.mChildren.extend(insideViews)
            else :
                parentView.mChildren.extend(indexOfNewParent + 1,
                        insideViews)
            

            return newParent
        
        return None
    

    def createListLayoutCode(self, listView, listMetadata, aditionalListViewItemData, index):

        if len(listMetadata.getListItemMetadatas()) == 0 :
            return
        

        baseListItemMetadata = listMetadata.getListItemMetadatas()[0]
#         Document document = XmlUtil.createDocument()
        rootView = RectView(baseListItemMetadata.bound, None)
        for rectView in baseListItemMetadata.baseViews:
            rootView.addChild(rectView)
        

        for rectView in baseListItemMetadata.additionalViews:
            rootView.addChild(rectView)
        
        rootView.mChildren.sort(key=cmp_to_key(RectUtil.getTopBottomComparator()))
        rootView.mChildren.sort(key=cmp_to_key(RectUtil.getLeftRightComparator()))

        rootElement = XmlUtil.createRoot(self.mDipCalculator, self.FRAMELAYOUT_ELEMENT, rootView, self.mColorWriter)
        _map = {}
        self.addChildrenLayout(rootElement, rootView, listView.getX(),
                listView.getY(), _map)

        rectViews = RectUtil.toRects(rootView)
        rectViews.remove(rootView)

        viewIdMap = {}
        # For baseview
        for rectView in baseListItemMetadata.baseViews:
            elementInfo = _map[rectView]
            viewIdMap[rectView]=  elementInfo._id
        

        # For additionview
        for rectViewWrapper in aditionalListViewItemData:
            elementInfo = _map[rectViewWrapper.view]
            viewIdMap[rectViewWrapper.view]  = elementInfo.id
        

        # TODO: since we checked already (#getAditionalListViewItemData), all
        # base view should only image views
        resourceInfoMap = {}

        listItemMetadatas = listMetadata.getListItemMetadatas()
        
        for listItemMetadata in listItemMetadatas:
            for baseView in listItemMetadata.baseViews:
                resourceInfoMap[baseView] = self.getInfoResource(baseView)
                   

        for rectViewWrapper in aditionalListViewItemData :
            for viewWrapper in rectViewWrapper.relativeViews :
                resourceInfoMap[viewWrapper.view]= self.getInfoResource(viewWrapper.view)            
        

        listMetadata.generateCode(index, listView.getListInfo().xmlId,
                self.mOutProjectFolder, aditionalListViewItemData, viewIdMap, resourceInfoMap)

        # We need to store current x, y, w, h of element before we loss
        # them
        anotateMap = LayoutFilter.anotate(rootView)

        layoutFilter = RelativeLayoutFilter()
        layoutFilter.doFilter(rootView, anotateMap)

        XmlUtil.writeDocument(rootView, self.mOutProjectFolder
                + Constants.DEFAULT_LAYOUT_PATH + "/"
                + Constants.DEFAULT_LAYOUT_LIST_PREFIX + index + ".xml")
    

    def getInfoResource(self,view) :
        info = ListMetadataRoot.ResourceInfo()
        info.view = view
        info.type = view.mType
        info.id = self.getOriginalIdFromRectView(view)
        return info
    

    def getOriginalIdFromRectView(self,baseView) :
        if(baseView.mType == RectView.VIEW_TYPE_IMAGE):
            return baseView.getImageInfo().drawableId
        elif baseView.mType == RectView.VIEW_TYPE_TEXT:
            if (TextUtils.isEmpty(baseView.getTextInfo().id)) :
                return self.mWriter.addResource(baseView.getTextInfo().textWrapper.text)
            else :
                return baseView.getTextInfo().id            
        else:
            return None
        
    

#    @Override
    def  getElementTypeForRect(self, rectView) :
        if (rectView.mType == RectView.VIEW_TYPE_LIST and rectView.getListInfo().valid) :
            return self.LIST_VIEW_ELEMENT
        else :
            return self.getElementTypeForRect(rectView)
        
    

    def canGenerateListAndGetAdditionListInfo(self,listMetadataRoot) :
        groups = listMetadataRoot.getListItemMetadatas()

        if len(groups)<= 1:
            return None
        

        newGroups = []
        ratio = 0
        # only allow list not too much different from each other in size
        alignmentType = listMetadataRoot.getAlignmentType()
        if alignmentType == RectUtil.ALIGNMENT_RIGHT:
            newGroups = []
            newGroups.extend(groups)
            newGroups.sort(key=cmp_to_key(RectUtil.getTopBottomComparator()))

            ratio = groups[0].bound.height * self.MAX_DISTANCE_RATIO_OF_LIST
            for i in range(len(groups)- 1):
                current = groups[i]
                _next = groups[i + 1]
                if (RectUtil.verticalDistance(current.bound, _next.bound) > ratio) :
                    return None
        if alignmentType ==  RectUtil.ALIGNMENT_BOTTOM:
            newGroups = []
            newGroups.extend(groups)
            newGroups.sort(key=cmp_to_key(RectUtil.getLeftRightComparator()))
            ratio = groups[0].bound.width * self.MAX_DISTANCE_RATIO_OF_LIST
            for i in range(len(groups)-1) :
                current = groups[i]
                _next = groups[i + 1]
                if (RectUtil.horizontalDistance(current.bound, _next.bound) > ratio) :
                    return None
                       

        # and all base views of each list item should have same size
        currentSize = -sys.maxint-1 
        for listItem in groups:
            if (currentSize == -sys.maxint-1) :
                currentSize = len(listItem.baseViews)
            elif (currentSize != len(listItem.baseViews)) :
                return None
        
        # same addition size
        currentSize = -sys.maxint-1
        for listItem in groups:
            if (currentSize == -sys.maxint-1) :
                currentSize = len(listItem.additionalViews)
            elif currentSize != len(listItem.additionalViews) :
                return None
            
        # We only support more than one base view
        for listItem in groups:
            if len(listItem.baseViews) <= 1 :
                return None
        # They have to be align
        if alignmentType == RectUtil.ALIGNMENT_RIGHT:
            for i in range(len(groups)-1) :
                current = groups[i]
                _next = groups[i + 1]
                for currentBase in current.baseViews:
                    for nextBase in _next.baseViews:
                        if (not RectUtil.above(currentBase, nextBase)) :
                            return None
        if alignmentType == RectUtil.ALIGNMENT_BOTTOM:
            for i in range(len(groups)-1) :
                current = groups[i]
                _next = groups[i + 1]
                for currentBase in current.baseViews:
                    for nextBase in _next.baseViews:
                        if (not RectUtil.onTheLeft(currentBase, nextBase)) :
                            return None

        # We only support base view is image view for now
        for listItem in groups:
            for baseView in listItem.baseViews:
                if (baseView.mType != RectView.VIEW_TYPE_IMAGE) :
                    return None

        # We already check that all additional view has same size
        sameLevelViews = []

        for listItemMetadata in groups:
            additionalViewRecusive = []
            for rectView in listItemMetadata.additionalViews:
                self.getAllLeaveViewRecusively(additionalViewRecusive, rectView, listItemMetadata.bound.x, listItemMetadata.bound.y)            
            sameLevelViews.add(additionalViewRecusive)        

        # make sure it all overlap and have same type
        if len(sameLevelViews) <= 1:
            return None
        
        # same recursive addition size
        currentSize = -sys.maxint-1
        for listItem in sameLevelViews:
            if (currentSize == -sys.maxint-1) :
                currentSize = len(listItem)
            elif currentSize != len(listItem) :
                return None
                    
        firstList = sameLevelViews[0]
        for t in firstList:
            t.overlapFlag = True
            t.relativeViews.append(t)
        
        for i in range(len(sameLevelViews)):
            for t in firstList:
                for o in sameLevelViews[i] :
                    if (not o.overlapFlag and RectUtil.intersects(t, o) and o.mType == t.mType) :
                        o.overlapFlag = True
                        t.relativeViews.append(o)
                        break
        

        # Make sure all items is marked
        for listItem in sameLevelViews:
            for r in listItem:
                if (not r.overlapFlag) :
                    return None

        # Make sure we get all relative view
        for t in firstList:
            if len(t.relativeViews) != len(groups) :
                return None

        return firstList    

    def getAllLeaveViewRecusively(self, additionalViewRecusive, rectView, x, y) :

        if len(rectView.mChildren) == 0:
            b = rectView.bound()
            additionalViewRecusive.append(RectViewWrapper(rectView, Rect(b.x - x, b.y - y, b.width, b.height)))
        else :
            for child in rectView.mChildren :
                self.getAllLeaveViewRecusively(additionalViewRecusive, child, x, y)
            
        