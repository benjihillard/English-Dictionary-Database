from bs4 import BeautifulSoup
import requests
import logging
import os

logger = logging.getLogger(__name__)

def crawl(alph):
    for letter in alph:
        # this can run a long time its helpfull to know which letter its on
        logger.info(f"processing letter {letter}...")
        url = "http://www.mso.anu.edu.au/~ralph/OPTED/v003/wb1913_" + letter + ".html" #there is a page for each letter
        req = requests.get(url) #grab page
        soup = BeautifulSoup(req.text, "html.parser") #get parser
        dictionary = soup.find_all('p') # find all the dictionary entries
        for entries in dictionary:
            word = entries.find('b').getText() # get the word itself
            pos = entries.find('i').getText() # get the part of speech
            cut = len(word) + len(pos) + 4 # calulate how much word and pos take up
            definition = entries.getText()[cut:] # cut that from the total sting to get definition
            yield word, pos, definition

#            DO what you need here
# this loop will run through all the words in the
# english dictionary, seperating them by word, pos and definition
#
# example to print out CSV to stdout
# use DEV=true to test small amount of words
if __name__ == '__main__':
    alph = "abcdefghijklmnopqrstuvwxyz"
    if os.environ.get('DEV'):
        alph = "x"
    print("word,pos,definition")
    for word, pos, definition in crawl(alph):
        print(f"{word},{pos},\"{definition}\"")
