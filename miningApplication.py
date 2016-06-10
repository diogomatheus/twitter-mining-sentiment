import logging
import ConfigParser
from sentimentAnalyzer import SentimentAnalyzer
from sentimentFrequencyAnalyzer import SentimentFrequencyAnalyzer
from sentimentAverageAnalyzer import SentimentAverageAnalyzer
from sentimentWeightAnalyzer import SentimentWeightAnalyzer
from sentimentEvaluation import SentimentEvaluation
from trendTopicsFilter import TrendTopicsFilter

class MiningApplication(object):

	def __init__(self, arguments):
		self.logger = self.initLogger()
		self.sentiment = None
		self.analyzer = None
		self.normalizeInitArguments(arguments)

	def execute(self):
		self.logger.info('Init trend topic mining application')
		cfg = self.readConfigurationFile('config/APP.cfg')
		calibrationFlag = self.getCalibrationFlag(cfg)
		if calibrationFlag:
			evaluation = SentimentEvaluation(self.logger)
			evaluation.execute(self.analyzer)
		else:
			if self.sentiment and self.analyzer:
				topicFilter = TrendTopicsFilter(self.logger)
				topicFilter.execute(self.analyzer, self.sentiment)
			else:
				self.logger.error('Please inform the method type and sentiment')

	def initLogger(self):
		logger = logging.getLogger('miningApplication')
		hdlr = logging.FileHandler('logging.log')
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr) 
		logger.setLevel(logging.INFO)
		return logger

	def readConfigurationFile(self, file):
		self.logger.info('Reading configuration file: ' + file)
		cfg = ConfigParser.RawConfigParser()
		cfg.read(file)
		return cfg

	def getCalibrationFlag(self, cfg):
		result = False
		calibrationFlag = cfg.get('configuration', 'CALIBRATION')
		if calibrationFlag and calibrationFlag.upper() == 'TRUE':
			result = True
		return result

	def normalizeInitArguments(self, arguments):
		analyzerTypeArgument = None
		if len(arguments) > 1:
			self.analyzer = self.getInitAnalyzerArgument(arguments[1])

		self.sentiment = None
		if len(arguments) > 2:
			self.sentiment = self.getInitSentimentArgument(arguments[2])

	def getInitAnalyzerArgument(self, argument):
		value = argument.upper()
		return {
			'FREQUENCY': SentimentFrequencyAnalyzer(self.logger),
			'AVERAGE': SentimentAverageAnalyzer(self.logger),
			'WEIGHT': SentimentWeightAnalyzer(self.logger)
		}.get(value, None)

	def getInitSentimentArgument(self, argument):
		value = argument.upper()
		return {
			'POSITIVE': SentimentAnalyzer.SENTIMENT_POSITIVE,
			'NEGATIVE': SentimentAnalyzer.SENTIMENT_NEGATIVE,
			'NEUTRAL': SentimentAnalyzer.SENTIMENT_NEUTRAL
		}.get(value, None)
