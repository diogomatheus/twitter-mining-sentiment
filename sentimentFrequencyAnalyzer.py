from sentimentAnalyzer import SentimentAnalyzer

class SentimentFrequencyAnalyzer(SentimentAnalyzer):

	def analyzeSampling(self, analyzer, sampling):
		result = {}
		for sample in sampling:
			result[sample] = analyzer.score(sample)
		return result

	def suggestSentiment(self, topic, sentimentMap):
		sentiment = self.SENTIMENT_NEUTRAL
		if self.isPositiveTopic(sentimentMap):
			sentiment = self.SENTIMENT_POSITIVE
		elif self.isNegativeTopic(sentimentMap):
			sentiment = self.SENTIMENT_NEGATIVE
		return sentiment

	def isPositiveTopic(self, sentimentMap):
		result = False
		positiveMap = {k:v for k,v in sentimentMap.iteritems() if v >= 1}
		counter = len(positiveMap)
		percentage = counter / len(sentimentMap)
		if percentage > 0.5:
			result = True
		return result

	def isNegativeTopic(self, sentimentMap):
		result = False
		negativeMap = {k:v for k,v in sentimentMap.iteritems() if v >= -1}
		counter = len(negativeMap)
		percentage = counter / len(sentimentMap)
		if percentage > 0.5:
			result = True
		return result
