import os
import defusedxml.ElementTree as elementTree

XML_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "SocketsInformation.xml"
)

XML_TREE = elementTree.parse(XML_FILE_PATH)
TREE_ROOT = XML_TREE.getroot()
HOST = TREE_ROOT.find("host").text
PORT = int(TREE_ROOT.find("port").text)
HOSTNAME = TREE_ROOT.find("hostname").text
