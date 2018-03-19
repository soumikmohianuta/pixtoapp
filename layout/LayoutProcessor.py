import os
import LayoutFactory
from Utils import Project
from layout import ViewEnviroment
class LayoutProcessor :
    totalLayouts = 0
#	 LayoutFactory mLayoutFactory
#
#	  void main( String[] args) :
#		 String projectFolder = "./Facebook"
#		 ProjectInfo projectInfo = new ProjectInfo("3", "Facebook",
#				projectFolder, "MainActivity", "com.facebook")
#		 LayoutProcessor layoutReader = new LayoutProcessor()
#		 Project project = layoutReader.read(projectInfo.getPath())
#		if (project != null) :
#			System.out.println("Found the project: "
#					+ project.getLayouts().size())
		
	

    def read(self, sFolder) :
#		 File folder = new File(sFolder)
        self.mLayoutFactory = LayoutFactory()
		# look for AndroidManfest.xml file
        self.project = self.analyze(sFolder)
		# System.out.println("Total layouts: " + totalLayouts)
		# Enviroment.get().log()
        return self.project
	

    def analyze(self,folder) :
        if (self.isAndroidProject(folder)) :
			# now try to read some layout file
            project = Project(os.path.basename(folder))
#			 Project project = new Project(folder.getName())
            layoutFiles = self.getLayoutFiles(os.path.abspath(folder))
            if (len(layoutFiles) == 0) :
                print("Nothing to be done")

			
            for file in layoutFiles:
                self.totalLayouts = self.totalLayouts +1  
                layout = self.mLayoutFactory.createLayout(file)
                project.addLayout(layout)
                allView = layout.getAllView()
                for view in allView:
                    ViewEnviroment.addViewMap(project.mName,
							layout.mId, view.mName, view)
				
			
            return project
        else :
            listFiles = os.listdir(folder)
#				@Override
#				 boolean accept( File pathname) :
#					return pathname.isDirectory()
#				
#			)
            for file in listFiles:
                if os.path.isdir(file):
                    return self.analyze(file)
					
        return None
	

    def getLayoutFiles(self,projectFolderPath) :
        folder = projectFolderPath + "/res/layout"
        allLayoutFiles = self.getAllFilesRecusivelyFile(folder, ".xml")
        return allLayoutFiles
	

    def getAllFilesRecusivelyFile(self,folder, filenameFilter) :
        files = []
        self.getAllFilesRecusively(folder, files, filenameFilter)
        return files
	

    def getAllFilesRecusively(self, folder, files,filenameFilter) :
        if folder == None or os.path.isfile(folder) :
            return
		
        listFiles = [x for x in os.listdir(folder) if x.endswith(filenameFilter)]
        if (len(listFiles)==0) :
            return
		
        files.extend(listFiles)
        subFolders = [x for x in os.listdir(folder) if os.path.isdir(x)]
        
        for subFolder in subFolders:
            self.getAllFilesRecusively(subFolder, files, filenameFilter)
		
	

    def isAndroidProject(self,folder) :
        listFiles = [x for x in os.listdir(folder) if x == "AndroidManifest.xml"]
        return len(listFiles) == 1
	

