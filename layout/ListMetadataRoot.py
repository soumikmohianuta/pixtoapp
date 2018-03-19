
from RectUtils import Rect
from RectUtils import RectView
from RectUtils import RectUtil
from Utils import Constants
from layout import ListViewData
from layout import FieldMetadata
from layout import ListInfoData
from layout import ListInfoItemMetadata
from layout import ListViewGenerator



class ListItemType:
    def __init__(self):
        self.view = RectView()
        self._type = 0

class ListItemMetadata:
    def __init__(self):
        self.bound = Rect()
        self.baseViews = []
        self.additionalViews = []

#		@Override
    def bound(self):
        return self.bound
    

class ResourceInfo:
    def __init__(self):
        self.view = RectView()
        self._id = ""
        self._type = 0

class ListMetadataRoot:

#	private RectView mParent
#	private List<ListItemMetadata> mListItemMetadatas
#	private int mAlignmentType

    def __init__(self,parent,listItemMetadatas,alignmentType):
        self.mParent = parent
        self.mListItemMetadatas = listItemMetadatas
        self.mAlignmentType = alignmentType

    def bound(self):
        allChildViews = []
        for itemMetadata in  self.mListItemMetadatas:
            allChildViews.extend(itemMetadata.baseViews)
            allChildViews.extend(itemMetadata.additionalViews)
        return RectUtil.findBoundRectangle(allChildViews)


    def generateCode(self,index, listViewId, projectFolder, packageName, aditionalListViewItemData, viewIdMap, resourceInfoMap):
        name = "ListView" + index
        _id = listViewId
        infoClassName = "ListInfo" + index
        adapterClassName = "ListArrayAdapter" + index
        layoutName = Constants.DEFAULT_LAYOUT_LIST_PREFIX + index
        infos = []

        info = ListViewData(name, _id, infoClassName, adapterClassName, layoutName)

        itemTypes = self.getMetadataListItemType(aditionalListViewItemData)
        fieldMetadatas = []
        for metadataListItemType in itemTypes:
#			 Meta data info
            _type = FieldMetadata(info, metadataListItemType.type, viewIdMap[metadataListItemType.view])
            fieldMetadatas.append(_type)
            
        
        info.setListFieldMetatata(fieldMetadatas)
		
        infoDatas = []
		
        for i in range(len(self.mListItemMetadatas)):
            infoData = ListInfoData()
            infoItemMetadatas = []
            listItemMetadata = self.mListItemMetadatas[i]

            for j in range(len(listItemMetadata.baseViews)):
                baseView = listItemMetadata.baseViews[j]
                resourceInfo = resourceInfoMap.get(baseView)
                infoItemMetadatas.append(ListInfoItemMetadata(infoData, fieldMetadatas[j], resourceInfo.id))

#			// For additionView
            startFieldMetadataIndex = len(listItemMetadata.baseViews)

            for j in len(aditionalListViewItemData):
                relativeViewWrapper = aditionalListViewItemData[j].relativeViews[i]
                resourceInfo = resourceInfoMap[relativeViewWrapper.view]
                infoItemMetadatas.append(ListInfoItemMetadata(infoData, fieldMetadatas[j + startFieldMetadataIndex],resourceInfo._id))

            infoData.setMetadatas(infoItemMetadatas)
            infoDatas.append(infoData)

        info.setListInfos(infoDatas)
        infos.append(info)

        generator = ListViewGenerator(projectFolder,packageName)
        generator.generateCode(infos)
        generator.createListViewCodeAndUpdateMainActivity()


    def getMetadataListItemType(self, aditionalListViewItemData):
        itemTypes = []
        if len(self.mListItemMetadatas) > 0 :
            baseViews = self.mListItemMetadatas[0].baseViews
            for rectView in baseViews:
                itemTypes.append(self.getItemType(rectView))

            for rectViewWrapper in aditionalListViewItemData:
                itemTypes.append(self.getItemType(rectViewWrapper.view))
        return itemTypes
	

    def getItemType(self,rectView):
        itemType = ListItemType()
        if rectView.mType== RectView.VIEW_TYPE_IMAGE:
            itemType.type = FieldMetadata.IMAGE
        elif rectView.mType ==  RectView.VIEW_TYPE_TEXT:
            itemType.type = FieldMetadata.TEXT
        else:
            itemType.type = FieldMetadata.VIEW
			
        itemType.view = rectView
        return itemType
