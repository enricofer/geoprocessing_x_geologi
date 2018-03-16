from qgis.core import  QgsWkbTypes, QgsPoint
layer = iface.activeLayer() #caricamento
if not layer or not layer.isValid():
  print ("Layer non valido!")
QgsProject.instance().addMapLayer(layer) #registrazione
informazioni=[]
for feature in layer.getFeatures(): #accesso alle features
    info = [feature.id()]
    geom = feature.geometry()
    if geom.type() ==  QgsWkbTypes.Point:
        info.append("distanza")
        info.append(geom.distance(QgsPoint(0,0)))
    elif geom.type() ==  QgsWkbTypes.LineString:
        info.append("Lunghezza")
        info.append(geom.length())
    elif geom.type() ==  QgsWkbTypes.Polygon:
        info.append("Area")
        info.append(geom.area)
    info += feature.attributes()
    informazioni.append(info)
print (informazioni)