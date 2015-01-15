from copy import deepcopy

class filter(object) :

    def __init__(self, forbidden_word_list) :
	self.w_list = deepcopy(forbidden_word_list)

    def filt(self, message) :
	for word in self.w_list :
	    message = message.replace(word, '*' * len(word))
	return message
