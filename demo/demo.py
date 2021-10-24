import pytesseract
import cv2
import matplotlib.pyplot as plt
import os
import shutil
from zipfile import ZipFile

import numpy as np

try:
    from PIL import Image
except ImportError:
    import Image

from typing import Union, Tuple
from pdf2image import convert_from_path
from deskew import determine_skew

from natasha import (Segmenter,
                     MorphVocab,

                     NewsEmbedding,
                     NewsMorphTagger,
                     NewsSyntaxParser,
                     NewsNERTagger,

                     PER,
                     ORG,
                     NamesExtractor,
                     Doc, )

abs_path = os.path.abspath(os.getcwd())

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)


def bluring_the_all_files():
    for file_page, filename in enumerate(os.listdir(abs_path + "/tmp/")):
        image = cv2.imread(abs_path + "/tmp/" + filename)
        print("---------------------------------------\n------------------------------------" * 3)
        string = pytesseract.image_to_string(image, lang="rus", config='--psm 6 --oem 3')

        doc = Doc(string.replace("\n", " ").
                  replace("Государственного", " ").
                  replace("негосударственного", " ").
                  replace("акционерного", ""))
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)
        doc.tag_ner(ner_tagger)
        names = []

        for span in doc.spans:
            if span.type == PER:
                if len(span.text) > 1:
                    for i in span.text.split():
                        names.append(i)
                else:
                    names.append(span.text)
        image_copy = image.copy()
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT,
                                         lang='rus', config='--psm 6 --oem 3')
        data_y = [e for e in data["text"]]
        word_occurences = [i for i, word in enumerate(data_y) if word in names]
        for occ in word_occurences:
            # extract the width, height, top and left position for that detected word
            w = data["width"][occ]
            h = data["height"][occ]
            l = data["left"][occ]
            t = data["top"][occ]
            # define all the surrounding box points
            p1 = (l, t)
            p2 = (l + w, t)
            p3 = (l + w, t + h)
            p4 = (l, t + h)
            # draw the 4 lines (rectangular)
            # image_copy = cv2.rectangle(image_copy, (p1, p3), (p2, p4), (255,0,0), 2)
            image_copy = cv2.line(image_copy, p1, p2, color=(255, 0, 0), thickness=2)
            image_copy = cv2.line(image_copy, p2, p3, color=(255, 0, 0), thickness=2)
            image_copy = cv2.line(image_copy, p3, p4, color=(255, 0, 0), thickness=2)
            image_copy = cv2.line(image_copy, p4, p1, color=(255, 0, 0), thickness=2)
        plt.imsave(f"{abs_path}/output/output-{file_page + 1}.png", image_copy)
        plt.imshow(image_copy)


def bluring_the_text(filepath):
    file_input, tip = filepath.split("/")[-1].split(".")
    if tip == 'pdf':
        if os.path.isdir(abs_path + "/tmp"):
            shutil.rmtree(abs_path + "/tmp")
            os.mkdir(abs_path + "/tmp")
        else:
            os.mkdir(abs_path + "/tmp")
        folder = abs_path + "/output"


        pages = convert_from_path(filepath, dpi=100)
        for idx, page in enumerate(pages):
            page.save('tmp/page-' + str(idx + 1) + '.png', 'PNG')


        ###### Если будем работать с изображениями отправленные с телефонов ######
        # def rotate(
        #         image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
        # ) -> np.ndarray:
        #     old_width, old_height = image.shape[:2]
        #     angle_radian = math.radians(angle)
        #     width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
        #     height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

        #     image_center = tuple(np.array(image.shape[1::-1]) / 2)
        #     rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        #     rot_mat[1, 2] += (width - old_width) / 2
        #     rot_mat[0, 2] += (height - old_height) / 2
        #     return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    os.mkdir(file_path)
            except Exception as e:
                print("Ошибка при удалении папки %s. Ошибка: %s" % (file_path, e))
        bluring_the_all_files()
    else:
        try:
            bluring_the_all_files()
        except Exception as e:
            print(f"Непредвиденная ошибка при распознании файла. Ошибка {e}")


    with ZipFile(f'bluring_zip_files/{file_input}.zip', 'w') as zipObj2:
        for filename in os.listdir(abs_path + "/output/"):
            # Add multiple files to the zip
            zipObj2.write(abs_path + "/output/" + filename)
    return "bluring_zip_files/" + f"{file_input}.zip"
