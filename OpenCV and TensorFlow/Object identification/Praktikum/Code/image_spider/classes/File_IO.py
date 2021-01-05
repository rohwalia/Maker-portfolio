import os
desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
class FileIO:

    def append(self, items_list: list, filename: str=""):

        if filename == None or filename == "":
            filename =  desktop + "/darkflow-master/saved-data/file.txt"
            filename = os.path.abspath(filename)

        file_Name = filename

        try:

            # opens the text file 'images' and appends the path, dimesnsion and description in it.

            with open(file_Name, 'a') as f:

                for item in items_list:
                    f.write(str(item) + " ")
                f.write("\n")
                f.close()

        except FileNotFoundError:
            # raise File_exeption('File not found!')
            print('File not found!')
        except IOError:
            # raise File_exeption('Error reading file!')
            print('Error reading file!')



    def read (self, filename: str=""):

        if filename == None or filename == "":
            filename = "./image_spider/saved_images/file.txt"

        file_Name = filename



        value_list = []

        with open(file_Name, 'r') as f:
            line = f.readline()
            while len(line) != 0:
                infos = line.split("|")
                #print("info: " + str(infos))
                value_dict = {}
                value_dict['path'] = infos[0]
                value_dict['source'] = infos[1]
                value_dict['dimension'] = infos[2]
                value_dict['description'] = infos[3]
                #print(str(value_dict) + "Valu dict ")

                value_list.append(value_dict)
                #print ("Value List : " + str(value_list))

                line = f.readline()
            f.close()

        return value_list





