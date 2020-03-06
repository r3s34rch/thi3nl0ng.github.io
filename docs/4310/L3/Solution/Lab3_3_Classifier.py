from collections import defaultdict
class Model(object):
	def __init__(self):
		self.counts = defaultdict(float)
		self.counts['total'] = 0.0
		self.wordcounts = defaultdict(float)
		self.wordcounts['total'] = 0.0
		self.words = defaultdict(float)
		self.allwords = defaultdict(float)
	
	def train(self, type, examples):
		if not type in self.counts:
			self.counts[type] = 0.0
		if not type in self.wordcounts:
			self.wordcounts[type] = 0.0
		for example in examples:
			self.counts['total'] += 1.0
			self.counts[type] += 1.0
			if not type in self.words:
				self.words[type] = defaultdict(float)
			for word in example.split(' '):
				self.wordcounts['total'] += 1.0
				self.wordcounts[type] += 1.0
				self.allwords[word] = True
				if not word in self.words[type]:
					self.words[type][word] = 1.0
				else:
					self.words[type][word] += 1.0

	def prior(self, type):
		return self.implementation.prior(type)

	def probability(self, word, type):
		return self.implementation.probability(word, type)

	def classify(self, type, data):
		return self.implementation.classify(type, data)
      
class Smoothing(Model):
	def __init__(self, k = 1):
		Model.__init__(self)
		self.k = k

	def prior(self, type):
		return (self.counts[type] + self.k) / (self.counts['total'] + (self.k * len(self.words.keys())))

	def probability(self, word, type):
		a = self.words[type][word] + self.k
		b = self.wordcounts[type] + (self.k * len(self.allwords))
		
		return a / b

	def classify(self, type, data):
		if not isinstance(data, list):
			a = self.probability(data, type) * self.prior(type)
			b = 0.0
			for _type in self.words:
				b += self.probability(data, _type) * self.prior(_type)
			if b == 0.0:
				return 0;
			else
				return a / b
		else:
			a = self.prior(type)
			for word in data:
				a *= self.probability(word, type)
			b = 0.0
			for _type in self.words:
				bb = self.prior(_type)
				for word in data:
					bb *= self.probability(word, _type)
				b += bb
			if b == 0.0:
				return 0;
			else
				return a / b
		    
class MaximumLikelihood(Smoothing):
    def __init__(self, k = 0):
        Smoothing.__init__(self,k)

#####################################################################################################################################
# Read me: The classifier model:																									#
#	functions:																														#
#	1- initialization(k) of the model																								#
#       - k == 0: no-smooth mode 																									#
#       - k != 0: smooth mode																										#
#	2- prior(label) : get prior probability of label in the model																	#
#	3- probability(feature, label) :  the probability that input values with that label will have that feature						#
#	4- classify(label, data) :  the probability that input data is classified as label						 						#
#####################################################################################################################################
        
def Lab3_3a():
    print ('Lab3_3a')
    MOVIE = ['a perfect world', 'my perfect woman', 'pretty woman']
    SONG = ['a perfect day', 'electric storm', 'another rainy day']

    model = MaximumLikelihood(1)    
    model.train('movie', MOVIE)
    model.train('song', SONG)
    """
        YOUR CODE HERE!

        Returns the values.
        1. Prior probability of labels used in training. (movie, song)
        2. Probability of word under given prior label (i.e., P(word|label)) according to this NB model.
                a. P(perfect|movie)
                b. P(storm|movie)
                c. P(perfect|song)
                d. P(storm|song)
        3. Probability of the title 'perfect storm' is labeled as 'movie' and 'song' with no-smooth mode and smooth mode (k=1)
    """
    print ('P(movie)', model.prior('movie'))
    print ('P(song)', model.prior('song'))
    
    print ('P(perfect|movie) =', model.probability('perfect', 'movie'))
    print ('P(perfect|song) =', model.probability('perfect', 'song'))
    
    print ('P(storm|movie) =', model.probability('storm', 'movie'))
    print ('P(storm|song) =', model.probability('storm', 'song'))

    print ('P(movie|perfect storm) =', model.classify('movie', ['perfect', 'storm']))

    print ('\nNo-Smooth Mode')
    model = MaximumLikelihood()
    model.train('movie', MOVIE)
    model.train('song', SONG)

    # Here's a hint for Homework 3 Problem 1: the size of the vocabulary is 11.
    #print (len(model.allwords) == 11)
    print ('P(movie|perfect storm) =', model.classify('movie', ['perfect', 'storm']))
def Lab3_3b():
    print ('\nLab3_3b')

    HAM = ["play sport today", "went play sport", "secret sport event", "sport is today", "sport costs money"]
    SPAM = ["offer is secret", "click secret link", "secret sport link"]

    model = MaximumLikelihood()
    model.train('S', SPAM)
    model.train('H', HAM)
    """
        YOUR CODE HERE!

        Returns the values.
        1. Prior probability of labels for SPAM, HAM data.
        2. Probability of word 'secret', 'sport' under given prior label (SPAM, HAM)
        3. Probabilities of: The word 'today is secret' is labeled as SPAM, HAM with no-smooth mode and smooth mode (k=1)
             
    """
    print ('P(spam) =', model.prior('S'))
    print ('P(secret|spam) =', model.probability('secret', 'S'))
    print ('P(secret|ham) =', model.probability('secret', 'H'))
    print ('P(spam|secret) =', model.classify('S', 'sport'))
    print ('P(spam|secret is secret) =', model.classify('S', ['secret', 'is', 'secret']))
    print ('P(spam|today is secret) =', model.classify('S', ['today', 'is', 'secret']))

    print ('\nSmooth Mode')
    model = MaximumLikelihood(1)
    model.train('S', SPAM)
    model.train('H', HAM)
    print ('P(spam) =', model.prior('S'))
    print ('P(ham) =', model.prior('H'))
    print ('P(today|spam) =', model.probability('today', 'S'))
    print ('P(today|ham) =', model.probability('today', 'H'))
    print ('P(spam|today is secret) =', model.classify('S', ['today', 'is', 'secret']))
if __name__ == '__main__':
    Lab3_3a()
    Lab3_3b()
