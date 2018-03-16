##Vector=group
##input=vector
##output=output vector

from qgis.core import *
from processing.tools.vector import VectorWriter

vectorLayer = processing.getObject(input)

provider = vectorLayer.dataProvider()

writer = VectorWriter(output, None, vectorLayer.pendingFields(),
                      provider.geometryType(), vectorLayer.crs())

features = processing.features(vectorLayer)
for feat in features:
    writer.addFeature(feat)

del writer