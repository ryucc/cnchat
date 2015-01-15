class my_filter(object) :

    def __init__(self, word_file) :
        self.w_list = []
        with open (word_file) as f :
            for word in f :
                self.w_list.append(word.rstrip('\n'))

    def filt(self, message) :
	for word in self.w_list :
	    message = message.replace(word, '*' * len(word))
	return message
