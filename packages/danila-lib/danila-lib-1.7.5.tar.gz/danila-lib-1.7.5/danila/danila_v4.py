import os

import cv2

from data.neuro.Letters_recognize import Letters_recognize
from data.neuro.Rama_detect_class import Rama_detect_class
from data.neuro.Rama_prod_classify_class import Rama_prod_classify_class
from data.neuro.Text_detect_class import Text_detect_class
from data.neuro.models import *
from data.result.Class_im import Class_im
from data.result.Class_text import Class_text
from data.result.Rama_prod import Rama_Prod
from data.result.Rect import Rect

"""main module for user"""
from data.neuro.Rama_classify_class import Rama_classify_class
from data.neuro.text_recognize_yolo import Text_Recognize_yolo

class Danila_v4:
    """main class for user"""
    def __init__(self, yolov5_dir):

        yolo_path = yolov5_dir
        rama_prod_classify_model_path = RAMA_PROD_CLASSIFY_MODEL_ADDRESS
        self.rama_prod_classify_model = Rama_prod_classify_class(rama_prod_classify_model_path, yolo_path)
        rama_no_spring_detect_model_path = RAMA_BEGICKAYA_DETECT_MODEL_ADDRESS
        self.rama_no_spring_detect_model = Rama_detect_class(rama_no_spring_detect_model_path,
                                                             'rama_no_spring_detect', yolo_path)
        rama_spring_detect_model_path = RAMA_RUZHIMMASH_DETECT_MODEL_ADDRESS
        self.rama_spring_detect_model = Rama_detect_class(rama_spring_detect_model_path, 'rama_spring_detect',
                                                             yolo_path)
        rama_spring_ruzhimmash_text_detect_model_path = RAMA_RUZHIMMASH_TEXT_DETECT_MODEL_ADDRESS
        self.rama_spring_ruzhimmash_text_detect_model = Text_detect_class(rama_spring_ruzhimmash_text_detect_model_path,
                                                                          'rama_text_ruzhimmash_detect', yolo_path)
        rama_no_spring_bejickaya_text_detect_model_path = RAMA_BEJICKAYA_TEXT_DETECT_MODEL_ADDRESS
        self.rama_no_spring_bejickaya_text_detect_model = Text_detect_class(rama_no_spring_bejickaya_text_detect_model_path,
                                                                            'rama_text_begickaya_detect', yolo_path)
        text_recognize_yolo_ruzhimmash_model_path = TEXT_RECOGNIZE_RUZHIMMASH_MODEL_ADDRESS
        self.text_recognize_ruzhimmash_model = Text_Recognize_yolo(text_recognize_yolo_ruzhimmash_model_path, yolo_path)
        text_recognize_yolo_begickaya_model_path = TEXT_RECOGNIZE_BEGICKAYA_MODEL_ADDRESS
        self.text_recognize_begickaya_model = Text_Recognize_yolo(text_recognize_yolo_begickaya_model_path, yolo_path)
    # returns string - class of rama using CNN network
    # img - openCV frame

    def rama_classify(self, img, size = 256):
        """rama_classify(Img : openCv frame): String - returns class of rama using CNN network"""
        """rama_classify uses Rama_classify_class method - classify(Img)"""
        # img = cv2.imread(img_path)
        rama_prod = self.rama_prod_classify_model.classify(img, size)
        return rama_prod.name

    # returns openCV frame with rama from openCV frame\
    def rama_detect(self, img, size = 256):
        """rama_detect(img : openCV img) -> openCV image with drawn rama rectangle"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        rama_prod = self.rama_prod_classify_model.classify(img, size)
        if rama_prod == Rama_Prod.no_rama:
            return img
        rect = Rect()
        if (rama_prod == Rama_Prod.ruzhimmash):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
        new_img = img.copy()
        os.remove('initial_image.jpg')
        if rect is None:
            return img
        cv2.rectangle(new_img, (rect.xmin, rect.ymin), (rect.xmax, rect.ymax), (0, 0, 255), 2)
        cv2.putText(new_img, rama_prod.name, (rect.xmin, rect.ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        return new_img

    # returns openCV image with cut_rama
    def rama_cut(self, img, size = 256):
        """rama_cut(img : openCV img) -> openCV image of rama rectangle"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img, size)
        rama_prod = self.rama_prod_classify_model.classify(img)
        if rama_prod == Rama_Prod.no_rama:
            return img
        rect = Rect()
        if (rama_prod == Rama_Prod.ruzhimmash):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
        if rect is None:
            return img
        img_res = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
        os.remove('initial_image.jpg')
        return img_res
    #
    # returns openCV cut rama with drawn text areas
    def text_detect_cut(self, img, size = 256):
        """returns openCV cut rama with drawn text areas"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        rama_prod = self.rama_prod_classify_model.classify(img, size)
        if rama_prod == Rama_Prod.no_rama:
            return {'result': 'no_rama'}
        rect = Rect()
        if (rama_prod == Rama_Prod.ruzhimmash):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_spring_ruzhimmash_text_detect_model.text_detect(img_cut_path)
            image_drawn_text_areas = self.rama_spring_ruzhimmash_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img_cut)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_no_spring_bejickaya_text_detect_model.text_detect(img_cut_path)
            image_drawn_text_areas = self.rama_no_spring_bejickaya_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img_cut)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas

    # returns openCV img with drawn text areas
    def text_detect(self, img, size = 256):
        """returns openCV img with drawn text areas"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        rama_prod = self.rama_prod_classify_model.classify(img, size)
        if rama_prod == Rama_Prod.no_rama:
            return img
        rect = Rect()
        if (rama_prod == Rama_Prod.ruzhimmash):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_spring_ruzhimmash_text_detect_model.text_detect(img_cut_path)
            image_text_areas.explore_to_whole_image(rect)
            image_drawn_text_areas = self.rama_spring_ruzhimmash_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return img
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_no_spring_bejickaya_text_detect_model.text_detect(img_cut_path)
            image_text_areas.explore_to_whole_image(rect)
            image_drawn_text_areas = self.rama_no_spring_bejickaya_text_detect_model.draw_text_areas_in_opencv(image_text_areas, img)
            os.remove(initial_image_path)
            os.remove(img_cut_path)
            return image_drawn_text_areas

    # returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'
    def text_recognize(self, img, size = 256):
        """returns dict {'number', 'prod', 'year'} for openCV rama img or 'no_rama'"""
        initial_image_path = 'initial_image.jpg'
        cv2.imwrite(initial_image_path, img)
        rama_prod = self.rama_prod_classify_model.classify(img, size)
        if rama_prod == Rama_Prod.no_rama:
            return {'result': 'no_rama'}
        rect = Rect()
        if (rama_prod == Rama_Prod.ruzhimmash):
            rect = self.rama_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return {'result': 'no_rama'}
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_spring_ruzhimmash_text_detect_model.text_detect(img_cut_path)

            label_area = self.text_recognize_ruzhimmash_model.work_image_cut(image_text_areas, img_cut, 5, 64,128,
                                                                  4, 64,128, 2, 64,64)
            res_labels = {}
            if len(label_area.labels[Class_text.number]) == 5:
                res_labels['number'] = label_area.labels[Class_text.number]
            else:
                number_image_text_areas = image_text_areas.areas[Class_text.number]
                image_text_areas_min = []
                image_text_areas_max = []
                for number_image_text_area in number_image_text_areas:
                    w = number_image_text_area.xmax - number_image_text_area.xmin
                    if (number_image_text_area.xmin - (w//2)) < 0:
                        new_xmin = 0
                    else:
                        new_xmin = number_image_text_area.xmin - (w//2)
                    rect_min = Rect(xmin=new_xmin, xmax=number_image_text_area.xmax, ymin=number_image_text_area.ymin, ymax=number_image_text_area.ymax)
                    image_text_areas_min.append(rect_min)
                    new_xmax = number_image_text_area.xmax + w//2
                    rect_max = Rect(xmin=number_image_text_area.xmin, xmax=new_xmax, ymin=number_image_text_area.ymin, ymax=number_image_text_area.ymax)
                    image_text_areas_max.append(rect_max)
                image_text_areas.areas[Class_text.number] = image_text_areas_min
                label_area_min = self.text_recognize_ruzhimmash_model.work_image_cut(image_text_areas, img_cut, 5, 64,128,
                                                                  4, 64,128, 2, 64,64)
                if len(label_area_min.labels[Class_text.number]) == 5:
                    res_labels['number'] = label_area_min.labels[Class_text.number]
                else:
                    image_text_areas.areas[Class_text.number] = image_text_areas_max
                    label_area_max = self.text_recognize_ruzhimmash_model.work_image_cut(image_text_areas, img_cut, 5, 64, 128,
                                                                              4, 64, 128, 2, 64, 64)
                    if len(label_area_max.labels[Class_text.number]) == 5:
                        res_labels['number'] = label_area_max.labels[Class_text.number]
                    else:
                        res_labels['number'] = label_area.labels[Class_text.number]
            res_labels['prod'] = '1275'
            if (len(label_area.labels[Class_text.year]) == 2) and (int(label_area.labels[Class_text.year]) < 25):
                res_labels['year'] = label_area.labels[Class_text.year]
            else:
                res_labels['year'] = '23'
            return res_labels
        else:
            rect = self.rama_no_spring_detect_model.rama_detect(initial_image_path)
            if rect is None:
                return {"result" : "no_rama"}
            img_cut = img[rect.ymin:rect.ymax, rect.xmin:rect.xmax]
            img_cut_path = 'cut_img.jpg'
            cv2.imwrite(img_cut_path, img_cut)
            image_text_areas = self.rama_no_spring_bejickaya_text_detect_model.text_detect(img_cut_path)
            label_area = self.text_recognize_begickaya_model.work_image_cut(image_text_areas, img_cut, 6, 64, 192,
                                                                  2, 64, 64, 2, 64,64)
            res_labels = {}
            if len(label_area.labels[Class_text.number]) == 6:
                res_labels['number'] = label_area.labels[Class_text.number]
            else:
                number_image_text_areas = image_text_areas.areas[Class_text.number]
                image_text_areas_min = []
                image_text_areas_max = []
                for number_image_text_area in number_image_text_areas:
                    w = number_image_text_area.xmax - number_image_text_area.xmin
                    if (number_image_text_area.xmin - (w//2)) < 0:
                        new_xmin = 0
                    else:
                        new_xmin = number_image_text_area.xmin - (w//2)
                    rect_min = Rect(xmin=new_xmin, xmax=number_image_text_area.xmax, ymin=number_image_text_area.ymin, ymax=number_image_text_area.ymax)
                    image_text_areas_min.append(rect_min)
                    new_xmax = number_image_text_area.xmax + w//2
                    rect_max = Rect(xmin=number_image_text_area.xmin, xmax=new_xmax, ymin=number_image_text_area.ymin, ymax=number_image_text_area.ymax)
                    image_text_areas_max.append(rect_max)
                image_text_areas.areas[Class_text.number] = image_text_areas_min
                label_area_min = self.text_recognize_begickaya_model.work_image_cut(image_text_areas, img_cut, 5, 64,128,
                                                                  4, 64,128, 2, 64,64)
                if len(label_area_min.labels[Class_text.number]) == 6:
                    res_labels['number'] = label_area_min.labels[Class_text.number]
                else:
                    image_text_areas.areas[Class_text.number] = image_text_areas_max
                    label_area_max = self.text_recognize_begickaya_model.work_image_cut(image_text_areas, img_cut, 5, 64, 128,
                                                                              4, 64, 128, 2, 64, 64)
                    if len(label_area_max.labels[Class_text.number]) == 6:
                        res_labels['number'] = label_area_max.labels[Class_text.number]
                    else:
                        res_labels['number'] = label_area.labels[Class_text.number]
            res_labels['prod'] = '12'
            if (len(label_area.labels[Class_text.year]) == 2) and (int(label_area.labels[Class_text.year]) < 25):
                res_labels['year'] = label_area.labels[Class_text.year]
            else:
                res_labels['year'] = '23'
            return res_labels
