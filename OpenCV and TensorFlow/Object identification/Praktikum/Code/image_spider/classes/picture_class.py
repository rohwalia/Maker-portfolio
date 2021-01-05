from Code.image_spider.classes.File_IO import FileIO
import os
desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

class Mange_Pictures:
    __myFileIO = FileIO()
    __path = desktop + "/darkflow-master/saved-data/info.txt"
    __path = os.path.abspath(__path)


    def __init__(self, list_of_pictures:list = None) :
        if list_of_pictures is None:
            self._list_of_pictures = []
        else:
            self._list_of_pictures = list_of_pictures


    def append_Picture(self, pic):
        if isinstance(pic, Picture):
            self._list_of_pictures.append(pic)
        else:
            print("something went wrong - in Mange_picture Class")


    def __str__(self):
        return (str(self._list_of_pictures))

    def __repr__(self):
        return self.__str__()

    def load_info(self):
        objects = []
        objects = self.__myFileIO.read(self.__path)
        #print( "Objects: in Mange " + str(objects))



        for dict_obj in objects:
           path = dict_obj["path"]
           source = dict_obj["source"]
           dimension = dict_obj["dimension"]
           height, width = dimension.split("x")
           desc = dict_obj["description"]

           pic = Picture(path=path, source=source, height=height, width=width, desc=desc )

           #print ("Picture in while" + str(pic))

           self._list_of_pictures.append(pic)
           #print(str(self._list_of_pictures))

    def get_all(self):
        return str(self._list_of_pictures)



class Picture:
    __path = desktop + "/darkflow-master/saved-data/info.txt"
    __path = os.path.abspath(__path)
    __myFileIO = FileIO()

    def __init__(self, path:str = None, source:str = None,  height:int = 0, width:int = 0, desc="None"):
        self._img_source = source
        self._img_desc = desc
        self._img_height = height
        self._img_width = width
        self._img_dimension = str(width) + "x" + str(height)
        self._img_path = path


    def save_info(self):
        value_list = []
        value_list.append(str(self._img_path)+"|")
        value_list.append(str(self._img_source) + "|" )
        size = self._img_dimension
        value_list.append(str(size) + "|")
        value_list.append(str(self._img_desc))


        self.__myFileIO.append(items_list=value_list, filename=self.__path)



    def __str__(self):
        return (str(self._img_desc + " at: " + self._img_path))

    def __repr__(self):
        return self.__str__()
