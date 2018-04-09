# -*- coding: utf-8 -*-

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink,
                       QgsFields,QgsField,QgsFeature,QgsGeometry, QgsWkbTypes, QgsRaster)


class DTMProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT_LAYER = 'OUTPUT_LAYER'
    INPUT_LAYER = 'INPUT_LAYER'
    DTM_LAYER = 'DTM_LAYER'
    MEASURE_VALUE = 'MEASURE'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DTMProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'measure_elev_on_dtm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Measure elevation on dtm')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Example scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'examplescripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Example algorithm short description")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(QgsProcessingParameterRasterLayer(
            self.DTM_LAYER,
            self.tr("DTM layer")))
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT_LAYER,
            self.tr("Input layer"),[QgsProcessing.TypeVectorLine]))
        self.addParameter(QgsProcessingParameterNumber(
            self.MEASURE_VALUE,
            self.tr("Measure step size"),
            QgsProcessingParameterNumber.Integer,50))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT_LAYER,
            self.tr("Output point layer"),
            QgsProcessing.TypeVectorPoint))

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        
        
        vectorLayer = self.parameterAsSource(parameters, self.INPUT_LAYER, context)
        dtmLayer = self.parameterAsRasterLayer(parameters, self.DTM_LAYER, context)
        measureStep = self.parameterAsInt (parameters, self.MEASURE_VALUE, context)

        
        fields=QgsFields()
        fields.append(QgsField('id_poly', QVariant.Int))
        fields.append(QgsField('elevation', QVariant.Double))
        fields.append(QgsField('step', QVariant.Double))


        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT_LAYER, context, fields, QgsWkbTypes.Point, vectorLayer.sourceCrs())
        
        
        features = vectorLayer.getFeatures() #QgsProcessingUtils.getFeatures(vectorLayer, context)
        for feat in features:
            currentLen = 0
            while currentLen < feat.geometry().length():
                point = feat.geometry().interpolate(currentLen).asPoint()
                elevFeat = QgsFeature(fields)
                elevValue = dtmLayer.dataProvider().identify(point, QgsRaster.IdentifyFormatValue).results()[1]
                elevFeat['elevation'] = elevValue
                elevFeat['step'] = currentLen
                elevFeat['id_poly'] = feat.id()
                elevGeom = QgsGeometry.fromPointXY(point)
                elevFeat.setGeometry(elevGeom)
                sink.addFeature(elevFeat, QgsFeatureSink.FastInsert)
                currentLen += measureStep
        
        return {self.OUTPUT_LAYER: dest_id}
        