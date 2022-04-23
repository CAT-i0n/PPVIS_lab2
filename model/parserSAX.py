import xml.sax
from datetime import date
from xml.sax import make_parser, handler


class DataHandler(handler.ContentHandler):
    def __init__(self, contentList: list):
        super().__init__()
        self.__contentList = contentList
        self.__currentRecord = dict()
        self.__name = False
        self.__year = False
        self.__group = False
        self.__total = False
        self.__done = False
        self.__language = False

    def startElement(self, tag, attrs):
        if tag == "Record":
            self.__currentRecord = dict()
        if tag == "name":
            self.__name = True
        if tag == "year":
            self.__year = True
        if tag == "group":
            self.__group = True
        if tag == "total":
            self.__total = True
        if tag == "done":
            self.__done = True
        if tag == "language":
            self.__language = True

    def endElement(self, tag):
        if tag == "Record":
            self.__contentList.append(self.__currentRecord)
        if tag == "name":
            self.__name = False
        if tag == "year":
            self.__year = False
        if tag == "group":
            self.__group = False
        if tag == "total":
            self.__total = False
        if tag == "done":
            self.__done = False
        if tag == "language":
            self.__language = False

    def characters(self, content):
        if self.__name:
            self.__currentRecord.update({"name": content})
        if self.__year:
            self.__currentRecord.update({"year": content})
        if self.__group:
            self.__currentRecord.update({"group": content})
        if self.__total:
            self.__currentRecord.update({"total": content})
        if self.__done:
            self.__currentRecord.update({"done": content})
        if self.__language:
            self.__currentRecord.update({"language": content})


def parse(filepath: str) -> list:
    out: list = list()
    parser = make_parser()
    parser.setContentHandler(DataHandler(out))
    parser.parse(filepath)
    return out


if __name__ == "__main__":
    data: list = list()
    xml.sax.parse("../data/database.xml", DataHandler(data))
    print(data)
