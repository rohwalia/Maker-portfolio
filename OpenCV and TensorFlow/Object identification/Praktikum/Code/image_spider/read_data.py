
from Code.image_spider.classes.picture_class import Mange_Pictures

mange = Mange_Pictures()
mange.load_info()
mange.get_all()

print(mange.get_all())

