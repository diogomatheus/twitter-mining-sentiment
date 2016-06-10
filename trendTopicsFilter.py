import csv
import datetime
from twitterCorpus import TwitterCorpus

class TrendTopicsFilter(object):

	def __init__(self, logger):
		self.logger = logger
		self.analyzerType = None

	def execute(self, analyzer, sentiment):
		self.analyzerType = analyzer.__class__.__name__
		self.logger.info('Init Trend Topic Filter Module for: ' + self.analyzerType)
		topics = self.getTwitterTrendTopics()
		classifiedTopics = self.analyzeTrendTopics(analyzer, topics)
		relevantTopics = self.filterTrendTopics(classifiedTopics, sentiment)
		self.writeResults(relevantTopics, sentiment)
	
	def getTwitterTrendTopics(self):
		corpus = TwitterCorpus(self.logger)
		return corpus.getTopicsSampling()

	def analyzeTrendTopics(self, analyzer, topics):
		results = {}
		if topics:
			for topic in topics:
				results[topic] = analyzer.analyzeTopic(topic, topics[topic])
		return results

	def filterTrendTopics(self, topics, sentiment):
		return {k:v for k,v in topics.iteritems() if v == sentiment}

	def writeResults(self, topics, sentiment):
		executionDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		outputFile = 'relevant-topics/' + executionDate + ': ' + self.analyzerType + '-' + sentiment + '.csv'
		with open(outputFile, 'w+') as csvfile:
			headers = ['topic', 'sentiment']
			writer = csv.DictWriter(csvfile, delimiter=';', lineterminator='\n', fieldnames=headers)
			for topic in topics:
				writer.writerow({'topic': topic, 'sentiment' : topics[topic]})
