from afinn import Afinn
from abc import ABCMeta, abstractmethod

class SentimentAnalyzer(object):

	__metaclass__ = ABCMeta

	SENTIMENT_POSITIVE = 'Positive'
	SENTIMENT_NEGATIVE = 'Negative'
	SENTIMENT_NEUTRAL = 'Neutral'

	def __init__(self, logger):
		self.logger = logger

	def analyzeTopic(self, topic, sampling):
		afinn = Afinn(emoticons=True)
		samplingSentiments = self.analyzeSampling(afinn, sampling)
		topicSentiment = self.suggestSentiment(topic, samplingSentiments)
		self.logger.info(topic + ': ' + topicSentiment)
		return topicSentiment

	@abstractmethod
	def analyzeSampling(self, analyzer, sampling): pass

	@abstractmethod
	def suggestSentiment(self, samplingSentiments): pass
	