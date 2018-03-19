from layout import ListInfoItemMetadata
from layout import ListInfoData
from layout import FieldMetadata
from layout import ListViewData
from Utils import Constants, Util
from stringtemplate3 import StringTemplateGroupLoader, StringTemplate

class ListViewGenerator:

    def __init__(self, projectFolder,packageName) :
        self.mProjectOutput = projectFolder
        self.mJavaSourceOutput = projectFolder + "/src/"+ Util.convertPageToFolderPath(packageName)
        self.templateFolder= projectFolder + "/"+ Constants.TEMPLATE_FOLDER + "/ListViewGenerator.stg"
#        self.mGroup =  StringTemplateGroupLoader(self.templateFolder, "UTF-8", '<', '>')
        self.stMain = self.mGroup.getInstanceOf("main")
        self.mPackageName = packageName
        self.stMain.setAttribute("packageName", self.mPackageName)
        self.stBaseAdapter = self.mGroup.getInstanceOf("baseadapter")
        self.stBaseAdapter.setAttribute("packageName", self.mPackageName)
	
    def process(self) :
        self.creatListViewCode(1)
        self.creatListViewCode(2)
        self.createListViewCodeAndUpdateMainActivity()
	

    def createListViewCodeAndUpdateMainActivity(self):
        Util.writeFile(self.stBaseAdapter.render(), self.mJavaSourceOutput + "/" + "BaseArrayAdapter.java")
        Util.writeFile(self.stMain.render(), self.mJavaSourceOutput + "/"+ "MainActivity.java")
	

    def creatListViewCode(self,index):
        name = "ListView" + index
        _id = "listview" + index
        infoClassName = "ListInfo" + index
        adapterClassName = "ListArrayAdapter" + index
        layoutName = Constants.DEFAULT_LAYOUT_LIST_PREFIX + index
        infos =  []
        info =  ListViewData(name, _id, infoClassName, adapterClassName, layoutName)

#		 Meta data info
        fieldMetadatas =  []
        textType =  FieldMetadata(info,FieldMetadata.TEXT)
        imageType =  FieldMetadata(info, FieldMetadata.IMAGE)
        fieldMetadatas.add(imageType)
        fieldMetadatas.add(textType)
        info.setListFieldMetatata(fieldMetadatas)
        infoDatas =  []

#		 List item 1
        infoData =  ListInfoData()
        infoItemMetadatas =  []
        infoItemMetadatas.append( ListInfoItemMetadata(infoData, imageType, "ic_launcher"))
        infoItemMetadatas.append( ListInfoItemMetadata(infoData, textType,"app_name"))

        infoData.setMetadatas(infoItemMetadatas)
        infoDatas.append(infoData)

#		 List item 2
        infoData =  ListInfoData()
        infoItemMetadatas =  []
        infoItemMetadatas.append( ListInfoItemMetadata(infoData, imageType, "ic_launcher"))
        infoItemMetadatas.append( ListInfoItemMetadata(infoData, textType,"app_name"))

        infoData.setMetadatas(infoItemMetadatas)
        infoDatas.append(infoData)
        info.setListInfos(infoDatas)
        infos.append(info)
        self.generateCode(infos)
	

    def generateCode(self,infos):
        self.stMain.setAttribute("listViews", infos)
        self.stAdapter = self.mGroup.getInstanceOf("adapter")
        self.stAdapter.setAttribute("packageName", self.mPackageName)
        
        self.stListInfo = self.mGroup.getInstanceOf("listinfo")
        self.stListInfo.setAttribute("packageName", self.mPackageName)
        
        for listViewData in infos:
            self.stAdapter.setAttribute("listView", listViewData)
            Util.writeFile(self.stAdapter.toString(), self.mJavaSourceOutput + "/" + listViewData.getAdapterClassName() + ".java")
            self.stListInfo.setAttribute("listView", listViewData)
            Util.writeFile(self.stListInfo.toString(), self.mJavaSourceOutput + "/"+ listViewData.getInfoClassName() + ".java")
		
	
#if __name__ == '__main__' :
#    generator =  ListViewGenerator(
#				"/Users/tuannguyen/Development/workspaces/workspace_screenshot/ListViewTemplate",
#				"com.example.listviewtemplate")
#    generator.process()
#	
