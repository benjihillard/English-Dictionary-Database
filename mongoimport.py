import mongoengine
from mongoengine import Document, fields
from dictionaryScript import crawl
import logging
import os

logger = logging.getLogger(__name__)

class Word(Document):
    word = fields.StringField(primary=True)
    definition = fields.ListField(default=[])

def mongo_import(host, db, username, password, alph):
    mongoengine.connect(db=db, host=host, username=username, password=password)
    previous = None
    for word, pos, definition in crawl(alph):
        if not previous:
            logger.info(f"Starting...")
            previous = Word()
            previous.word = word
        elif previous.word != word:
            logger.info(f"Moving on to new word {word}...")
            previous.save()
            previous = Word()
            previous.word = word
        logger.info(f"Adding definition for word {word}")
        previous.definition.append({ "pos": pos, "meaning": definition })
    if previous:
        previous.save()

# sample MongoDB connection settings.
if __name__ == '__main__':
    alph = "abcdefghijklmnopqrstuvwxyz"
    if os.environ.get('DEV'):
        alph = "x"
    mongo_import('192.168.1.51', 'wordsquad', 'wordsquad', os.environ.get('MONGO_PASS'), alph)
