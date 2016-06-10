import tweepy
from tweepy import OAuthHandler

class TwitterCorpus(object):

	EUA_WOEID = 23424977
	SEARCH_LIMIT = 100

	def __init__(self, logger):
		self.logger = logger
		self.logger.info('Init Twitter API')
		consumer_key = 'EDITAR AQUI'
		consumer_secret = 'EDITAR AQUI'
		access_token = 'EDITAR AQUI'
		access_secret = 'EDITAR AQUI'
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_secret)
		self.twitterAPI = tweepy.API(auth)

	def getTopicsSampling(self, number=150):
		result = {}
		self.logger.info('Get the twitter trends')
		topics = self.selectTwitterTrends()
		for topic in topics:
			self.logger.info('Get sampling of the topic: ' + topic['name'])
			sampling = self.getTrendSampling(topic, number)
			result[topic['name']] = sampling.values()
		return result

	def selectTwitterTrends(self):
		return self.twitterAPI.trends_place(TwitterCorpus.EUA_WOEID)[0]['trends'][:10]

	def getTrendSampling(self, topic, number):
		sampling = {}
		count = TwitterCorpus.SEARCH_LIMIT if number >= TwitterCorpus.SEARCH_LIMIT else number
		result = self.twitterAPI.search(q=topic['query'], count=count, result_type='recent', lang='en')
		sampling = self.normalizeTweepySearchResult(result)
		number -= count
		while number > 0:
			maxId = min(k for k in sampling) - 1
			count = TwitterCorpus.SEARCH_LIMIT if number > TwitterCorpus.SEARCH_LIMIT else number
			result = self.twitterAPI.search(q=topic['query'], count=count, result_type='recent', lang='en', max_id=maxId)
			normalizedResult = self.normalizeTweepySearchResult(result)
			sampling.update(normalizedResult)
			number -= TwitterCorpus.SEARCH_LIMIT
		return sampling

	def normalizeTweepySearchResult(self, result):
		data = {}
		for item in result:
			data[item.id] = item.text
		return data
