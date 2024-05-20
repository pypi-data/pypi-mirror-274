__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import json
from numpyencoder import NumpyEncoder
from ragfmk.interfaces.IEmbeddings import IEmbeddings
import ragfmk.utils.CONST as C
from ragfmk.elements.embeddings.embedding import embedding

"""
        Embeddings and data are stored in Python list/JSON and used with the following format :
        {"0": {
                'text': 'The prompt or text', 
                'embedding': array([-6.65125623e-02,  
                                    ..., 
                                    -1.22626998e-01]) 
              },
        "1": {
                'text': '...',  
                'embedding': array([...]) 
              },
        ...,
        "x" : { ... }
        }
"""

class embeddings(IEmbeddings):
    def __init__(self):
        self.__embeddings = {}
    
    @property
    def jsonContent(self) -> str: 
        return json.dumps(self.content, cls=NumpyEncoder)
    @jsonContent.setter
    def jsonContent(self, jsondata):
        embsLoaded = json.loads(jsondata)
        for key, value in embsLoaded.items():
            emb = embedding()
            emb.init(value[C.JST_TEXT], value[C.JST_EMBEDDINGS])
            self.__embeddings[key] = emb

    @property
    def content(self): 
        myJsonList = {}
        for key, value in self.__embeddings.items():
            myJsonList[key] = value.content
        return myJsonList
    
    @property
    def items(self):
        return self.__embeddings
    @items.setter
    def items(self, it):
        self.__embeddings = it
        
    def __getitem__(self, item):
        """ Makes the Data column accessible via [] array
            example: df['colName']
        Args:
            item (str): attribute/column name
        Returns:
            object: data
        """
        return self.__embeddings.__getitem__(item)
    
    @property
    def size(self):
        return len(self.__embeddings)

    def create(self, cks) -> bool:
        return False

    def save(self, filename) -> bool:
        """ Save the chunks in a file.
        Args:
            filename (_type_): JSON chunks file
        Returns:
            bool: True if ok
        """
        try:
            with open(filename, "w", encoding=C.ENCODING) as f:
                f.write(self.jsonContent)
            return True
        except Exception as e:
            return False

    def load(self, filename = "", content = "") -> bool:
        """ Load and build a chunk file (can be loaded from a json file or a json content). 
            Format required : Content = {"chunks": [..., ...] }
        Args:
            filename (str, optional): JSON embeddings file. Defaults to "".
            content (str, optional): JSON embeddings content. Defaults to "".
        Returns:
            bool: True if ok
        """
        try:
            if (len(filename) > 0):
                with open(filename, "r", encoding=C.ENCODING) as f:
                    self.jsonContent = f.read()
            elif (len(content) >0):
                self.jsonContent = content
            else:
                return False
            return True
        except Exception as e:
            return False