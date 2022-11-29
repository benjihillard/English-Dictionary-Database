import mongoengine
from mongoengine import Document, fields
from dictionaryScript import crawl
import logging
import os

logger = logging.getLogger(__name__)

class Word(Document):
    word = fields.StringField()
    definition = fields.ListField(default=[])
    meta = {
        'indexes': ['word']
    }

    @classmethod
    def find_or_create(cls, word):
        w = cls.objects(word=word).first()
        if w is None:
            w = Word(word=word)
        return w

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
            previous = Word.find_or_create(word)
        logger.info(f"Adding definition for word {word}")
        previous.definition.append({ "pos": pos, "meaning": definition })
    # save the last word before finishing
    if previous:
        previous.save()

# sample MongoDB connection settings.
if __name__ == '__main__':
    alph = "abcdefghijklmnopqrstuvwxyz"
    if os.environ.get('DEV'):
        alph = "x"
    mongo_import('192.168.1.51', 'wordsquad', 'wordsquad', os.environ.get('MONGO_PASS'), alph)
