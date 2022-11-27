import mongoengine
from mongoengine import Document, fields
from dictionaryScript import crawl
import logging
import os

logger = logging.getLogger(__name__)

class Word(Document):
    word = fields.StringField(primary=True)
    definition = fields.ListField(default=[])

    @classmethod
    def find_or_create(cls, word, pos, definition):
        w = cls.objects(word=word).first()
        if w is None:
            w = Word(
                word = word,
                definition = [
                    { "pos": pos, "meaning": definition }
                ]
            )
        else:
            w.definition.append({ "pos": pos, "meaning": definition })
        w.save()
        logger.info(f"Added word {word}")
        return w


def mongo_import(host, db, username, password):
    mongoengine.connect(db=db, host=host, username=username, password=password)
    previous = None
    for word, pos, definition in crawl():
        if not previous:
            previous = Word()
            previous.word = word
            previous.definition.append({ "pos": pos, "meaning": definition })
        elif previous.word != word:
            previous.save()
            previous = Word()
            previous.word = word
            previous.definition.append({ "pos": pos, "meaning": definition })
        else:
            previous.definition.append({ "pos": pos, "meaning": definition })
    if previous:
        previous.save()

if __name__ == '__main__':
    mongo_import('192.168.1.51', 'wordsquad', 'wordsquad', os.environ.get('MONGO_PASS'))
