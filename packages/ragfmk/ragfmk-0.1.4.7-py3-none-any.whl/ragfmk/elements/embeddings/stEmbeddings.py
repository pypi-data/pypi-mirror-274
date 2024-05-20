__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from sentence_transformers import SentenceTransformer
import ragfmk.utils.CONST as C
from ragfmk.elements.embeddings.embeddings import embeddings
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

class stEmbeddings(embeddings):
    def __init__(self):
        self.__embeddingsModel = C.EMBEDDING_MODEL
        super().__init__()

    @property
    def model(self) -> str: 
        return self.__embeddingsModel
    @model.setter
    def model(self, model):
        self.__embeddingsModel = model

    def create(self, cks) -> bool:
        """ Calculate the embeddings for list of chunks
        Args:
            cks (chunks):  chunks object
        Returns:
            str: json with data and embeddings for all chunks
        """
        try: 
            encoder = SentenceTransformer(self.__embeddingsModel)
            vect = encoder.encode(cks.items)
            vectAndData = zip(cks.items, vect)
            self.items = {}
            for i, (chunk, vector) in enumerate(vectAndData):
                emb = embedding()
                emb.init(chunk, vector)
                self.items[str(i)] = emb
            return True
        except Exception as e:
            return False
