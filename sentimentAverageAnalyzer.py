from sentimentAnalyzer import SentimentAnalyzer

class SentimentAverageAnalyzer(SentimentAnalyzer):

	def analyzeSampling(self, analyzer, sampling):
		result = {}
		for sample in sampling:
			result[sample] = analyzer.score(sample)
		return result

	def suggestSentiment(self, topic, sentimentMap):
		sentiment = SentimentAnalyzer.SENTIMENT_NEUTRAL
		sentimentSum = 0
		for sample in sentimentMap:
			sentimentSum += sentimentMap[sample]
		average = sentimentSum / len(sentimentMap)
		if average >= 1:
			sentiment = SentimentAnalyzer.SENTIMENT_POSITIVE
		elif average >= -1:
			sentiment = SentimentAnalyzer.SENTIMENT_NEGATIVE
		return sentiment
