from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input
from keras.applications.mobilenet_v2 import decode_predictions
import numpy as np
from PIL import Image


class CatClassifier:
    def __init__(self):
        self.model = MobileNetV2(weights='imagenet')
        self.data = np.empty((1, 224, 224, 3))
        self.cats = ['tabby', 'tiger_cat', 'Persian_cat', 'Siamese_cat', 'Egyptian_cat', 'cougar',
                     'lynx', 'leopard', 'snow_leopard', 'jaguar', 'lion', 'tiger', 'cheetah']

    def is_cat(self, image: Image) -> bool:
        self.data[0] = image.resize((224, 224))
        self.data = preprocess_input(self.data)
        predictions = self.model.predict(self.data)
        if decode_predictions(predictions)[0][0][1] in self.cats:
            return True
        return False
