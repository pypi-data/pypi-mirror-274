import json
from pathlib import Path

from .drawing import Drawing

class Images:
    _images = {}
    
    @staticmethod
    def _register_images(filepath: str) -> None:
        filename = Path(filepath).stem
        
        with open(filepath) as f:
            temp_images = json.load(f)
            print("Reading images from " + filepath)
            for key in temp_images.keys():
                Images.__images[key] = temp_images[key]
                print("Loaded image \"{}\" from {}".format(key, filepath))