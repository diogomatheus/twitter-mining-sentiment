from sentimentAnalyzer import SentimentAnalyzer

class SentimentWeightAnalyzer(SentimentAnalyzer):

	def analyzeSampling(self, analyzer, sampling):
		result = {}
		for sample in sampling:
			score = analyzer.score(sample)
			result[sample] = (score * 2) if score <= -1 else score
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
