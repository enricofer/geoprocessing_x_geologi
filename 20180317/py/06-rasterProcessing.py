##dtm=raster
##input=vector
##output=output vector

from qgis.core import *
from processing.tools.vector import VectorWriter

vectorLayer = processing.getObject(input)
dtmLayer = processing.getObject(dtm)

fields=QgsFields()
fields.append(QgsField('elevation', QVariant.Double))
fields.append(QgsField('id_polyline', QVariant.Int))

pointSamplewriter = VectorWriter(output, None, fields,
                      QgsWkbTypes.PointGeometry, vectorLayer.crs())

features = processing.features(vectorLayer)
for feat in features:
    for point in feat.geometry().asPolyline():
        elevFeat = QgsFeature(fields)
        elevValue = dtmLayer.dataProvider().identify(point, QgsRaster.IdentifyFormatValue).results()[1]
        elevFeat['elevation'] = elevValue
        elevFeat['id_polyline'] = feat.id()
        elevGeom = QgsGeometry.fromPointXY(point)
        elevFeat.setGeometry(elevGeom)
        pointSamplewriter.addFeature(elevFeat)

del writer