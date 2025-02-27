from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def word_feats(words):
	return dict( [ (word, True) for word in words ] )

def get_classifier():
	negids = movie_reviews.fileids('neg')
	posids = movie_reviews.fileids('pos')

	negfeats = [ (word_feats(movie_reviews.words(fileids = [f])), 'neg') for f in negids ]
	posfeats = [ (word_feats(movie_reviews.words(fileids = [f])), 'pos') for f in posids ]

	trainfeats = negfeats + posfeats

	classifier = NaiveBayesClassifier.train(trainfeats)

	return classifier