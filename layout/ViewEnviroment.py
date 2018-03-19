#class ViewEnviroment:
#    static ViewEnviroment sEnviroment;
#    private final HashMap<String, List<View>> viewTypeMap;


viewMap = {}
viewTypeMap = {}

#    public static synchronized ViewEnviroment get() {
#        if (sEnviroment == null) {
#            sEnviroment = new ViewEnviroment();
#        }
#        return sEnviroment;
#    }

#    Map<String, View> viewMap;

def addViewMap(projectName, layoutId, viewName, view):
        viewMap[projectName + "_" + layoutId + "_" + viewName] = view
        if (viewTypeMap[viewName] == None):
            views = []
            views.append(view);
            viewTypeMap[viewName] = views
        else:
            views = viewTypeMap[viewName]
            views.append(view)
