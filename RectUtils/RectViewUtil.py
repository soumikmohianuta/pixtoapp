# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 00:36:11 2017

@author: soumi
"""
from RectUtils.Rect import Rect
from RectUtils.RectUtil import *
from Utils import FileMetadata
#from .RectView import RectView


VIEW_TYPE_DEFAULT = 0
VIEW_TYPE_TEXT = 1
VIEW_TYPE_IMAGE = 2
VIEW_TYPE_LIST_ITEM = 3
VIEW_TYPE_LIST = 4
def isContanerView(rectView):
    if (rectView != None and (rectView.mType == VIEW_TYPE_LIST or rectView.mType == VIEW_TYPE_DEFAULT or rectView.mType == VIEW_TYPE_LIST_ITEM)):
        return True
    return False

class ListInfo:
    xmlId=""			#String Xml ID
    listItems = []		#Array of RectView
    listItemMetadatas = []		#Array of ListItemMetadata
    valid = False


class ListItemInfo:
    parent = None
	
    
class IconInfo:
    def __init__(self, imageData = None):
        self.imageData = imageData
    
    def __eq__(self,newIcon):
#        if (self.imageData == None or newIcon.bwImage ==None):
#            return False

        if self.imageData.shape != newIcon.imageData.shape:
            return False
        else:
            subData = self.imageData - newIcon.imageData
            if(subData.sum() == 0):
                return True
            else:
                return False
    
    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + self.imageData.shape[0]
        result = prime * result + self.imageData.shape[1]
        result = prime * result + len(self.imageData.shape)
        return result
	
class ImageInfo:
    iconInfo = IconInfo() #Inconfo
    drawableId = ""       #String for ID



class ListItemMetadata:
    rect =  Rect()
    baseViews = []    # Array of rectview
    additionalViews = [] # Array of rectview
    
class ListItemType:
    view = None
    listItemType_type =0   #int


class ResourceInfo:
    view = None # 
    resourceInfo_id = 0 
    resourceInfo_type = 0			

class ListMetadataRoot:
#    mParent  #Rectview
#    mListItemMetadatas  #List<ListItemMetadata>
#    mAlignmentType;
    
    def __init__(self,parent, listItemMetadatas, alignmentType):
        self.mParent = parent
        self.mListItemMetadatas = listItemMetadatas
        self.mAlignmentType = alignmentType
    
    def bound(self):
        allChildViews = []
        for itemMetadata in self.mListItemMetadatas :
            allChildViews.extend(itemMetadata.baseViews)
            allChildViews.extend(itemMetadata.additionalViews)
        
        return RectUtil.findBoundRectangle(allChildViews);
    
#    def generateCode(int index, String listViewId,
#			String projectFolder, String packageName,
#			List<RectViewWrapper> aditionalListViewItemData,
#			Map<RectView, String> viewIdMap,
#			Map<RectView, ResourceInfo> resourceInfoMap) throws IOException {
#		String name = "ListView" + index;
#		String id = listViewId;
#		String infoClassName = "ListInfo" + index;
#		String adapterClassName = "ListArrayAdapter" + index;
#		String layoutName = Constants.DEFAULT_LAYOUT_LIST_PREFIX + index;
#		final List<ListViewData> infos = new ArrayList<ListViewData>();
#
#		final ListViewData info = new ListViewData(name, id, infoClassName,
#				adapterClassName, layoutName);
#
#		List<ListItemType> itemTypes = getMetadataListItemType(aditionalListViewItemData);
#		final List<FieldMetadata> fieldMetadatas = new ArrayList<FieldMetadata>();
#		for (ListItemType metadataListItemType : itemTypes) {
#			// Meta data info
#			final FieldMetadata type = new FieldMetadata(info,
#					metadataListItemType.type,
#					viewIdMap.get(metadataListItemType.view));
#			fieldMetadatas.add(type);
#		}
#		info.setListFieldMetatata(fieldMetadatas);
#		
#		final List<ListInfoData> infoDatas = new ArrayList<ListInfoData>();
#		
#		for (int i = 0; i < mListItemMetadatas.size(); i++) {
#			ListInfoData infoData = new ListInfoData();
#			List<ListInfoItemMetadata> infoItemMetadatas = new ArrayList<ListInfoItemMetadata>();
#
#			ListItemMetadata listItemMetadata = mListItemMetadatas.get(i);
#
#			for (int j = 0; j < listItemMetadata.baseViews.size(); j++) {
#				RectView baseView = listItemMetadata.baseViews.get(j);
#				ResourceInfo resourceInfo = resourceInfoMap.get(baseView);
#				infoItemMetadatas.add(new ListInfoItemMetadata(infoData,
#						fieldMetadatas.get(j), resourceInfo.id));
#			}
#
#			// For additionView
#			int startFieldMetadataIndex = listItemMetadata.baseViews.size();
#
#			for (int j = 0; j < aditionalListViewItemData.size(); j++) {
#				RectViewWrapper relativeViewWrapper = aditionalListViewItemData
#						.get(j).relativeViews.get(i);
#				ResourceInfo resourceInfo = resourceInfoMap
#						.get(relativeViewWrapper.view);
#				infoItemMetadatas.add(new ListInfoItemMetadata(infoData,
#						fieldMetadatas.get(j + startFieldMetadataIndex),
#						resourceInfo.id));
#			}
#
#			infoData.setMetadatas(infoItemMetadatas);
#			infoDatas.add(infoData);
#		}
#
#		info.setListInfos(infoDatas);
#		infos.add(info);
#
#		ListViewGenerator generator = new ListViewGenerator(projectFolder,
#				packageName);
#		generator.generateCode(infos);
#		generator.createListViewCodeAndUpdateMainActivity();
#	}
#
    def getMetadataListItemType(self,aditionalListViewItemData):
        itemTypes = []
        if (len(self.mListItemMetadatas) > 0):
            baseViews = self.mListItemMetadatas[0].baseViews;
            for rectView in baseViews:
                itemTypes.append(self.getItemType(rectView))
            
            for rectViewWrapper in aditionalListViewItemData:
                itemTypes.append(self.getItemType(rectViewWrapper.view))
                
        return itemTypes
    
    
    def getItemType(self,rectView):
        itemType = ListItemType()
        if(rectView.getType()== RectView.VIEW_TYPE_IMAGE):
            itemType.type = FileMetadata.IMAGE
            
        if(rectView.getType()== RectView.VIEW_TYPE_TEXT):
            itemType.type = FileMetadata.TEXT
            
        else:
            itemType.type = FileMetadata.VIEW
            
        itemType.view = rectView
        return itemType
    
    def getAlignmentType(self):
        self.mAlignmentType
        
    def setAlignmentType(self,alignmentType):
        self.mAlignmentType = alignmentType
	





