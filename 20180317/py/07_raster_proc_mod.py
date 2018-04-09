##dtm=raster
##input=vector
##measure=number 50
##output=output vector

from PyQt4.QtCore import QVariant
from qgis.core import *
from processing.tools.vector import VectorWriter

vectorLayer = processing.getObject(input)
dtmLayer = processing.getObject(dtm)
measureStep = measure

fields=QgsFields()
fields.append(QgsField('id_poly', QVariant.Int))
fields.append(QgsField('elevation', QVariant.Double))
fields.append(QgsField('step', QVariant.Double))

pointSamplewriter = VectorWriter(output, None, fields,
                      QgsWKBTypes.Point, vectorLayer.crs())

features = processing.features(vectorLayer)
for feat in features:
    currentLen = 0
    while currentLen < feat.geometry().length():
        point = feat.geometry().interpolate(currentLen).asPoint()
        elevFeat = QgsFeature(fields)
        elevValue = dtmLayer.dataProvider().identify(point, QgsRaster.IdentifyFormatValue).results()[1]
        elevFeat['elevation'] = elevValue
        elevFeat['step'] = currentLen
        elevFeat['id_poly'] = feat.id()
        elevGeom = QgsGeometry.fromPoint(point)
        elevFeat.setGeometry(elevGeom)
        pointSamplewriter.addFeature(elevFeat)
        currentLen += measureStep

del pointSamplewriter
