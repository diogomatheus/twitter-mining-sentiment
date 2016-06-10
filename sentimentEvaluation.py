import csv
import xml.dom.minidom
from sentimentAnalyzer import SentimentAnalyzer

class SentimentEvaluation(object):

	def __init__(self, logger):
		self.logger = logger
		self.analyzerType = None

	def execute(self, analyzer):
		self.analyzerType = analyzer.__class__.__name__
		self.logger.info('Init Evaluation Module for: ' + self.analyzerType)
		database = self.getTwitterDatabase()
		analyzerResults = self.analyzeDatabaseTopics(analyzer, database)
		evaluationResults = self.evaluate(database, analyzerResults)
		self.writeResults(evaluationResults)

	def getTwitterDatabase(self):
		database = {}
		filename = 'data/mapping.xml'
		self.logger.info('Reading file: ' + filename)

		DOMTree = xml.dom.minidom.parse(filename)
		topics = DOMTree.getElementsByTagName("topic")

		for topic in topics:
			topicNameNode = topic.getElementsByTagName('name')[0]
			topicName = str(topicNameNode.firstChild.data)

			topicSentimentNode = topic.getElementsByTagName('sentiment')[0]
			topicSentiment = str(topicSentimentNode.firstChild.data)
			topicTuple = (topicName, topicSentiment)

			sampling = topic.getElementsByTagName('sampling')[0]
			samples = sampling.getElementsByTagName('sample')

			messages = {}
			for sample in samples:
				sampleMessage = sample.firstChild.data
				sampleAttributesKeys = sample.attributes.keys()
				sampleSentiment = sample.attributes['sentiment'].value
				messages[sampleMessage] = sampleSentiment

			database[topicTuple] = messages

		return database
	
	def analyzeDatabaseTopics(self, analyzer, database):
		results = {}
		if database:
			for row in database:
				topic, topicSentiment = row
				topicSampling = database[row].keys()
				results[topic] = analyzer.analyzeTopic(topic, topicSampling)
		return results
	
	def evaluate(self, correctMap, predictedMap):
		total = len(correctMap)
		basicMeasures = self.getBasicEvaluationMeasures(correctMap, predictedMap)
		precisionRecallMeasures = self.getPrecisionRecallMeasuresPerClass(basicMeasures)
		f1Measures = self.getF1MeasurePerClass(precisionRecallMeasures)
		macroF1Measure = self.getMacroF1Measure(f1Measures)
		coverageMeasure = self.getCoverageMeasure(basicMeasures, total)
		accuracyMeasure = self.getAccuracyMeasure(basicMeasures, total)

		measuresMap = {}
		measuresMap['basicMeasures'] = basicMeasures
		measuresMap['precisionRecallMeasures'] = precisionRecallMeasures
		measuresMap['macroF1'] = macroF1Measure
		measuresMap['coverage'] = coverageMeasure
		measuresMap['accuracy'] = accuracyMeasure
		return measuresMap

	def getBasicEvaluationMeasures(self, correctMap, predictedMap):
		a, b, c, d, e, f, g, h, i = 0, 0, 0, 0, 0, 0, 0, 0, 0
		for topic, topicSentiment in correctMap:
			predictedSentiment = predictedMap[topic]
			if topicSentiment == SentimentAnalyzer.SENTIMENT_POSITIVE:
				if predictedSentiment == SentimentAnalyzer.SENTIMENT_POSITIVE:
					a += 1
				elif predictedSentiment == SentimentAnalyzer.SENTIMENT_NEUTRAL:
					b += 1
				elif predictedSentiment == SentimentAnalyzer.SENTIMENT_NEGATIVE:
					c += 1
			elif topicSentiment == SentimentAnalyzer.SENTIMENT_NEUTRAL:
				if predictedSentiment == SentimentAnalyzer.SENTIMENT_POSITIVE:
					d += 1
				elif predictedSentiment == SentimentAnalyzer.SENTIMENT_NEUTRAL:
					e += 1
				elif predictedSentiment == SentimentAnalyzer.SENTIMENT_NEGATIVE:
					f += 1
			elif topicSentiment == SentimentAnalyzer.SENTIMENT_NEGATIVE:
				if predictedSentiment == SentimentAnalyzer.SENTIMENT_POSITIVE:
					g += 1
				elif predictedSentiment == SentimentAnalyzer.SENTIMENT_NEUTRAL:
					h += 1
				elif predictedSentiment == SentimentAnalyzer.SENTIMENT_NEGATIVE:
					i += 1

		return {'a':a, 'b':b, 'c':c, 'd':d, 'e':e, 'f':f, 'g':g, 'h':h, 'i':i}

	def getPrecisionRecallMeasuresPerClass(self, bms):
		precisionPositive = bms['a']
		precisionPositiveExpression = (bms['a'] + bms['d'] + bms['g'])
		if precisionPositiveExpression:
			precisionPositive /= float(precisionPositiveExpression)

		precisionNeutral = bms['e']
		precisionNeutralExpression = (bms['b'] + bms['e'] + bms['h'])
		if precisionNeutralExpression:
			precisionNeutral /= float(precisionNeutralExpression)

		precisionNegative = bms['i']
		precisionNegativeExpression = (bms['c'] + bms['f'] + bms['i'])
		if precisionNegativeExpression:
			precisionNegative /= float(precisionNegativeExpression)
		
		recallPositive = bms['a']
		recallPositiveExpression = (bms['a'] + bms['b'] + bms['c'])
		if recallPositiveExpression:
			recallPositive /= float(recallPositiveExpression)

		recallNeutral = bms['e']
		recallNeutralExpression = (bms['d'] + bms['e'] + bms['f'])
		if recallNeutralExpression:
			recallNeutral /= float(recallNeutralExpression)

		recallNegative =  bms['i']
		recallNegativeExpression = (bms['g'] + bms['h'] + bms['i'])
		if recallNegativeExpression:
			recallNegative /= float(recallNegativeExpression)
		
		return {
			'p': {'p':precisionPositive, 'n':precisionNegative, 'u':precisionNeutral},
			'r': {'p':recallPositive, 'n':recallNegative, 'u':recallNeutral}
		}

	def getF1MeasurePerClass(self, prms):
		f1Positive = 0
		f1PositiveFirstExpression = (2 * prms['p']['p'] * prms['r']['p'])
		f1PositiveSecondExpression =  (prms['p']['p'] + prms['r']['p'])
		if f1PositiveFirstExpression and f1PositiveSecondExpression:
			f1Positive = f1PositiveFirstExpression / float(f1PositiveSecondExpression)

		f1Negative = 0
		f1NegativeFirstExpression = (2 * prms['p']['n'] * prms['r']['n'])
		f1NegativeSecondExpression =  (prms['p']['n'] + prms['r']['n'])
		if f1NegativeFirstExpression and f1NegativeSecondExpression:
			f1Negative = f1NegativeFirstExpression / float(f1NegativeSecondExpression)

		f1Neutral = 0
		f1NeutralFirstExpression = (2 * prms['p']['u'] * prms['r']['u'])
		f1NeutralSecondExpression =  (prms['p']['u'] + prms['r']['u'])
		if f1NeutralFirstExpression and f1NeutralSecondExpression:
			f1Neutral = f1NeutralFirstExpression / float(f1NeutralSecondExpression)

		return {'F1Positive':f1Positive, 'F1Negative':f1Negative, 'F1Neutral':f1Neutral}

	def getMacroF1Measure(self, f1ms):
		f1sum = 0
		for f1 in f1ms:
			f1sum += f1ms[f1]
		return f1sum / float(3)

	def getAccuracyMeasure(self, bms, total):
		return (bms['a']+bms['e']+bms['i']) / float(total)

	def getCoverageMeasure(self, bms, total):
		return (total - (bms['b'] + bms['e'] + bms['h'])) / float(total)
	
	def writeResults(self, measuresMap):
		outputFile = 'evaluation/' + self.analyzerType + '-measures.csv'
		with open(outputFile, 'w+') as csvfile:
			headers = ['measure', 'value']
			writer = csv.DictWriter(csvfile, delimiter=';', lineterminator='\n', fieldnames=headers)
			for measure in measuresMap:
				writer.writerow({'measure': measure, 'value' : measuresMap[measure]})
