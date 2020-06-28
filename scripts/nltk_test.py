import nltk

text = "Backgammon is one of the oldest known board games. Its history can be traced back nearly 5,000 years to archeological discoveries in the Middle East. It is a two player game where each player has fifteen checkers which move between twenty-four points according to the roll of two dice."
sentences = nltk.sent_tokenize(text)
for sentence in sentences:
    print(sentence)
    words = nltk.word_tokenize(sentence)

    for word in words:
        print(word)




# purpose : use nltk to split text collection into sentences, and sentences into words