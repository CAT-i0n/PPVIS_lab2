import xml.dom.minidom as minidom

from datetime import date


def writeXML(filepath, dataList: list):
    doc = minidom.Document()
    rootNode = doc.createElement("Table")
    doc.appendChild(rootNode)

    for record in dataList:
        recordNode = doc.createElement("Record")
        rootNode.appendChild(recordNode)

        for tagName in record.keys():
            node = doc.createElement(tagName)
            if type(record[tagName]) is date:
                nodeText = doc.createTextNode(record[tagName].isoformat())
            else:
                nodeText = doc.createTextNode(record[tagName])
            node.appendChild(nodeText)
            recordNode.appendChild(node)

    with open(filepath, "w", encoding="UTF-8") as file:
        doc.writexml(file, addindent='    ', newl='\n', encoding='UTF-8')



