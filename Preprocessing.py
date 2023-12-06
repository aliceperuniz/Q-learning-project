import shutil
import os
import yaml

from imagededup.methods import PHash, DHash, WHash, AHash, CNN

dataset_names = ['Pictor ppe.v1-pictor-ppe.yolov8','CHV.v1i.yolov8', 'PPE Detection.v5-omitshoeclasses-accurate-model.yolov8',
                 'Safetyhelmet-detection.v3-bounding-box-noise.yolov8.v1i.yolov8', 'Safety vest - v4.v3i.yolov8',
                 'Hardhat.v1i.yolov8', 'Hardhat.v1-hard-hat-workers-v1.yolov8',
                 'DatasetAehon-V22.v3-originals_classesinenglish.yolov8']
dataset_paterns = {'PPE Detection.v5-omitshoeclasses-accurate-model.yolov8': ['luva', 'oculos', 'com_capacete',
                                                                              'mascara', 'sem_luva', 'sem_oculos',
                                                                              'sem_capacete', 'sem_mascara']
                   , 'Safetyhelmet-detection.v3-bounding-box-noise.yolov8.v1i.yolov8': ['capacete']
                   , 'Safety vest - v4.v3i.yolov8': ['com_capacete', 'sem_capacete', 'sem_veste', 'veste']
                   , 'Pictor ppe.v1-pictor-ppe.yolov8':['capacete', 'veste', 'trabalhador']
                   , 'Hardhat.v1i.yolov8':['sem_capacete','com_capacete','nao_importante','trabalhador']
                   , 'Hardhat.v1-hard-hat-workers-v1.yolov8':['sem_capacete','com_capacete','trabalhador']
                   , 'DatasetAehon-V22.v3-originals_classesinenglish.yolov8':['nao_importante', 'com_capacete',
                                                                              'trabalhador','sem_capacete',
                                                                              'nao_importante','nao_importante']
                   , 'CHV.v1i.yolov8':['trabalhador','veste', 'capacete', 'capacete', 'capacete', 'capacete' ]
}

dataset_numeric_paterns = {'veste':'0', 'oculos':'1', 'luva':'2','mascara':'3','sem_veste':'4', 'sem_oculos':'5',
                           'sem_luva':'6', 'sem_mascara':'7','trabalhador':'8', 'com_capacete':'9', 'sem_capacete':'10',
                           'capacete':'11', 'nao_importante':'12'}

dataset_string_paterns = {'0':'veste', '1':'oculos', '2':'luva','3':'mascara','4':'sem_veste', '5':'sem_oculos',
                           '6':'sem_luva', '7':'sem_mascara','8':'trabalhador', '9':'com_capacete', '10':'sem_capacete',
                           '11':'capacete', '12':'nao_importante'}

labels = ['train','test', 'valid']

def copy_dir(origin, target):
    # Create a copy from original dataset
    if not os.path.exists(origin):
        print(f"Folder {origin} does not exist!")
        return
    if os.path.exists(target):
        print(f"Folder {target} already exists!")
        return

    try:
        shutil.copytree(origin, target)
        print("Folder successfully copied!")
    except shutil.Error as e:
        print(f"Error copying folder: {e}")


def delete_dir(target):
    # Delete a folder
    d = os.path.basename(target)
    if not os.path.exists(target):
        print(f"Folder {d} does not exist!")
        return
    else:
        try:
            shutil.rmtree(target)
            print(f"Folder {d} successfully deleted!")
        except shutil.Error as e:
            print(f"Error deleting folder: {e}")




class Dataset:


    def __init__(self, name, path):
        self.renamed = False
        self.changed_atributes = False
        self.name = name
        self.path = path
    def get_atributes(self):
        numbers = set()
        lst_digits = [str(i) for i in range(13)]  # Lista de dígitos permitidos
        for label in labels:
            for root, dirs, files in os.walk(os.path.join(self.path, label)):
                for file in files:
                    if file.endswith('.txt'):
                        with open(os.path.join(root, file), 'r+') as arquivo_txt:
                            lines = arquivo_txt.readlines()
                            arquivo_txt.seek(0)
                            for line in lines:
                                #pega o primeiro e o segundo digits
                                first_digits = str(line.strip()[0:2]).strip()
                                if first_digits in lst_digits:
                                    numbers.add(int(first_digits))
        return list(numbers)

    def delete(self):
        delete_dir(self.path)

    def copy(self,origin):
        if os.path.exists(self.path):
            delete_dir(self.path)
        copy_dir(origin, self.path)

class Preprocessing:
    def __init__(self, dataset):
        self.dataset = dataset
        self.rename_files()
        self.change_atribute_names()

    def rename_files(self):
        if self.dataset.renamed:
            print('Files already renamed!')
            return
        print('Renaming files from ' + self.dataset.name)
        # Lista para armazenar os caminhos dos arquivos TXT
        txt_files = []
        images_files = []
        # Percorre os arquivos TXT nas subpastas de labels

        for label in labels:
            for root, dirs, files in os.walk(os.path.join(self.dataset.path, label)):
                for file in files:
                    if file.endswith('.txt'):
                        txt_files.append(os.path.join(root, file))
                    if file.endswith('.jpg'):
                        images_files.append(os.path.join(root, file))
            count = 0
        for image in images_files:
            if not image.replace('.jpg', '.txt').replace('images', 'labels') in txt_files:
                print('não possui arquivo txt correspondente ' + image)
            else:
                txt_path, txt_name = image.replace('.jpg', '.txt').replace('images', 'labels').rsplit('\\', 1)
                image_path, image_name = image.rsplit('\\', 1)
                os.rename(image_path + '\\' + image_name,
                          image_path + '\\' + self.dataset.name + '-' + str(count) + '.jpg')
                os.rename(txt_path + '\\' + txt_name, txt_path + '\\' + self.dataset.name + '-' + str(count) + '.txt')
                count += 1
        self.dataset.renamed = True
        print('Renaming files from ' + self.dataset.name + ' finished!')

    def change_atribute_names(self):
        if self.dataset.changed_atributes:
            print('Atributes already changed!')
            return
        for label in labels:
            for root, dirs, files in os.walk(os.path.join(self.dataset.path, label)):
                for file in files:
                    if file.endswith('.txt'):
                        with open(os.path.join(root, file), 'r+') as arquivo_txt:
                            lines = arquivo_txt.readlines()
                            arquivo_txt.seek(0)
                            for line in lines:
                                id = (int)(line[0])
                                line_processada = dataset_numeric_paterns[dataset_paterns[self.dataset.name][id]] + line[1:]
                                arquivo_txt.write(line_processada)
                            arquivo_txt.truncate()
        self.dataset.changed_atributes = True

    def ajust_atributes(self):
        atributes = self.dataset.get_atributes()
        for label in labels:
            for root, dirs, files in os.walk(os.path.join(self.dataset.path, label)):
                for file in files:
                    if file.endswith('.txt'):
                        arquivo_entrada = os.path.join(root, file)
                        with open(arquivo_entrada, 'r') as arquivo:
                            linhas = arquivo.readlines()

                        for i in range(len(linhas)):
                            for atributo in atributes:
                                if linhas[i].startswith(str(atributo)):
                                    linhas[i] = linhas[i].replace(str(atributo), str(atributes.index(atributo)))

                        # Escreve as linhas modificadas no arquivo
                        with open(arquivo_entrada, 'w') as arquivo:
                            arquivo.writelines(linhas)

class Group:
    def __init__(self, datasets, group_path, name):
        self.datasets = datasets
        self.group_path = group_path
        self.group_name = name


    def get_comun_atributes(self):
        atributes = set(self.datasets[0].get_atributes())
        for dataset in self.datasets[1:]:
            atributes = atributes.intersection(dataset.get_atributes())
        return sorted(list(atributes))

    def get_all_atributes(self):
        atributes = set()
        for dataset in self.datasets:
            for atribute in dataset.get_atributes():
                atributes.add(atribute)
        return list(atributes)

    def get_atributes_names(self, atributes):
        return [dataset_string_paterns[str(atribute)] for atribute in atributes]

    def group_datasets_all(self):

        if not os.path.exists(self.group_path):
            os.makedirs(self.group_path)

        for dataset in self.datasets:
            for label in labels:
                if not os.path.exists(os.path.join(self.group_path, label)):
                    os.makedirs(os.path.join(self.group_path, label))

                for root, dirs, files in os.walk(os.path.join(dataset.path, label)):
                    for file in files:

                        if not os.path.exists(os.path.join(self.group_path, label, 'labels')):
                            os.makedirs(os.path.join(self.group_path, label, 'labels'))
                        if file.endswith('.txt'):
                            shutil.copy(os.path.join(root, file), os.path.join(self.group_path, label, 'labels', file))

                        if not os.path.exists(os.path.join(self.group_path, label, 'images')):
                            os.makedirs(os.path.join(self.group_path, label, 'images'))

                        if file.endswith('.jpg'):
                            shutil.copy(os.path.join(root, file), os.path.join(self.group_path, label, 'images', file))

        self.dataset = Dataset(self.group_name,self.group_path)
        self.atributes = self.dataset.get_atributes()

    def group_datasets_separated(self):

        if not os.path.exists(self.group_path):
            os.makedirs(self.group_path)

        for label in labels:

            if label == 'test':
                data = self.datasets[1]
            else:
                data = self.datasets[0]

            if not os.path.exists(os.path.join(self.group_path, label)):
                os.makedirs(os.path.join(self.group_path, label))

            for root, dirs, files in os.walk(os.path.join(data.path, label)):
                for file in files:


                    if not os.path.exists(os.path.join(self.group_path, label, 'labels')):
                        os.makedirs(os.path.join(self.group_path, label, 'labels'))

                    if file.endswith('.txt'):
                        shutil.copy(os.path.join(root, file), os.path.join(self.group_path, label, 'labels', file))

                    if not os.path.exists(os.path.join(self.group_path, label, 'images')):
                        os.makedirs(os.path.join(self.group_path, label, 'images'))

                    if file.endswith('.jpg'):
                        shutil.copy(os.path.join(root, file), os.path.join(self.group_path, label, 'images', file))

        self.dataset = Dataset(self.group_name,self.group_path)
        self.atributes = self.dataset.get_atributes()

    def create_yamls(self):
        data = {
            'train': '../train/images',
            'test': '../test/images',
            'val': '../valid/images',
            'nc': len(self.atributes),
            'names': [str(i) for i in self.atributes]
        }
        yaml_file = os.path.join(self.group_path, 'data.yaml')
        with open(yaml_file, 'w') as arquivo:
            yaml.dump(data, arquivo)


    def filter_atributes(self, atributes):
        self.atributes = atributes
        if not os.path.exists(self.group_path):
            print('Group path does not exist!')
            return
        empty_files = []

        print('Filtering atributes from ' + self.group_path)
        for label in labels:
            for root, dirs, files in os.walk(os.path.join(self.group_path, label)):
                for file in files:
                    if file.endswith('.txt'):
                        with open(os.path.join(root, file), 'r+') as f:
                            linhas = f.readlines()
                            f.seek(0)  # Volta ao início do arquivo
                            for linha in linhas:
                                for atribute in atributes:
                                    if linha.startswith(str(atribute)) and atribute != '12':
                                        f.write(linha)
                            f.truncate()  # Remove o conteúdo restante (se houver) após as linhas processadas
                            f.seek(0)  # Volta ao início do arquivo para verificar se está vazio
                            if len(f.readlines()) == 0:
                                empty_files.append(os.path.join(root, file))
        if len(empty_files) > 0:
            print('Removing empty files from ' + self.group_path)
            empty_files_images = [e.replace('labels', 'images').replace('.txt', '.jpg') for e in empty_files]
            for file in empty_files:
                os.remove(file)
            for file in empty_files_images:
                os.remove(file)

    def ajust_atributes(self):

        for label in labels:
            for root, dirs, files in os.walk(os.path.join(self.group_path, label)):
                for file in files:
                    if file.endswith('.txt'):
                        arquivo_entrada = os.path.join(root, file)
                        with open(arquivo_entrada, 'r') as arquivo:
                            linhas = arquivo.readlines()

                        for i in range(len(linhas)):
                            for atributo in self.atributes:
                                if linhas[i].startswith(str(atributo)):
                                    linhas[i] = linhas[i].replace(str(atributo), str(self.atributes.index(atributo)))

                        # Escreve as linhas modificadas no arquivo
                        with open(arquivo_entrada, 'w') as arquivo:
                            arquivo.writelines(linhas)

    def delete(self):
        for d in self.datasets:
            d.delete()
        self.dataset.delete()

    def is_empty(self):
        return any([not os.listdir(os.path.join(self.group_path, label,'labels')) for label in labels])


class Duplicate_finder:
    def __init__(self, origin, destiny):
        if not os.path.exists(destiny):
            os.makedirs(destiny)

        self.move_duplicates(origin, destiny)

    def find_duplicates(self, listas):
        if len(listas) != 5:
            return []

        duplicates = set(listas[0])

        for lista in listas[1:]:
            duplicates.intersection_update(lista)

        return list(duplicates)

    def getPHash(self,img_dir):
        ## PHash
        phasher = PHash()
        encodings_p = phasher.encode_images(image_dir=img_dir)
        return phasher.find_duplicates(encoding_map=encodings_p)

    def getDHash(self,img_dir):
        ## DHash
        dhasher = DHash()
        encodings_d = dhasher.encode_images(image_dir=img_dir)
        return dhasher.find_duplicates(encoding_map=encodings_d)

    def getWHash(self,img_dir):
        ## WHash
        whasher = WHash()
        encodings_w = whasher.encode_images(image_dir=img_dir)
        return whasher.find_duplicates(encoding_map=encodings_w)

    def getAHash(self,img_dir):
        ## AHash
        ahasher = AHash()
        encodings_a = ahasher.encode_images(image_dir=img_dir)
        return ahasher.find_duplicates(encoding_map=encodings_a)

    def getCNNHAsh(self,img_dir):
        ## CNN
        cnn = CNN()
        encodings_c = cnn.encode_images(image_dir=img_dir)
        return cnn.find_duplicates(encoding_map=encodings_c, min_similarity_threshold=0.99)

    def move_duplicates(self,origin, destiny):


        labels = ['train', 'test', 'valid']

        for label in labels:

            duplicate_dir = os.path.join(destiny, label)
            origin_dir = os.path.join(origin, label)

            if not os.path.exists(duplicate_dir):
                os.mkdir(duplicate_dir)
                os.mkdir(os.path.join(duplicate_dir, 'images'))
                os.mkdir(os.path.join(duplicate_dir, 'labels'))

            img_dir = os.path.join(origin_dir, 'images')
            txt_dir = os.path.join(origin_dir, 'labels')

            copy_img_dir = os.path.join(duplicate_dir, 'images')
            copy_txt_dir = os.path.join(duplicate_dir, 'labels')

            # verifica se o caminho é valido

            ## PHash
            phasher = PHash()
            encodings_p = phasher.encode_images(image_dir=img_dir)
            print(img_dir)
            duplicates_p = phasher.find_duplicates(encoding_map=encodings_p)

            print("PHash duplicates loaded")

            ## DHash
            dhasher = DHash()
            encodings_d = dhasher.encode_images(image_dir=img_dir)
            duplicates_d = dhasher.find_duplicates(encoding_map=encodings_d)

            print("DHash duplicates loaded")

            ## WHash
            whasher = WHash()
            encodings_w = whasher.encode_images(image_dir=img_dir)
            duplicates_w = whasher.find_duplicates(encoding_map=encodings_w)

            print("WHash duplicates loaded")

            ## AHash
            ahasher = AHash()
            encodings_a = ahasher.encode_images(image_dir=img_dir)
            duplicates_a = ahasher.find_duplicates(encoding_map=encodings_a)

            print("AHash duplicates loaded")

            ## CNN
            cnn = CNN()
            encodings_c = cnn.encode_images(image_dir=img_dir)
            duplicates_c = cnn.find_duplicates(encoding_map=encodings_c, min_similarity_threshold=0.99)

            print("CNNHash duplicates loaded")

            # ___________________________________________________________________________________
            img_duplicates = dict()
            for img in duplicates_p:
                methods = [duplicates_p[img], duplicates_d[img], duplicates_w[img], duplicates_a[img],
                           duplicates_c[img]]
                img_duplicates[img] = self.find_duplicates(methods)

            duplicates = [[i, img_duplicates[i]] for i in img_duplicates if len(img_duplicates[i]) > 0]
            # _____________________________________________________________________________________________

            for original, copies in duplicates:
                # create a dict in destiny with the same name as the origin
                if not os.path.exists(os.path.join(copy_img_dir, original)):
                    os.mkdir(os.path.join(copy_img_dir, original))

                if not os.path.exists(os.path.join(copy_txt_dir, original)):
                    os.mkdir(os.path.join(copy_txt_dir, original))

                for copy in copies:
                    if os.path.exists(os.path.join(img_dir, copy)):
                        txt_copy = copy.replace('.jpg', '.txt')
                        # move the txt file to the new folder
                        os.rename(os.path.join(txt_dir, txt_copy), os.path.join(copy_txt_dir, original, txt_copy))

                        # move the file to the new folder
                        os.rename(os.path.join(img_dir, copy), os.path.join(copy_img_dir, original, txt_copy))



