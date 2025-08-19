import io
from collections import namedtuple
from abc import ABC, abstractmethod
from pathlib import Path

import onnxruntime as ort
from PIL import (
    
    Image, 
    ImageDraw, 
    ImageFont
)
import numpy as np
from ultralytics import YOLO

from ..enums import CVModel


ModelResult = namedtuple('ModelResult', ['message_sum', 'img_byte_main', 'img_byte_array'])


class YOLO8Model(ABC):

    name: str = None

    nums_of_processed_images = 0

    model_detector_M = ort.InferenceSession(Path('src/cv_models/core/NewDetector.onnx').resolve())
    model_detector_N = ort.InferenceSession(Path('src/cv_models/core/DetectN.onnx').resolve())
    model_detector_S = ort.InferenceSession(Path('src/cv_models/core/DetectorS.onnx').resolve())
    model_classifier = YOLO(Path('src/cv_models/core/classifier.pt').resolve())

    __yolo_classes = [
        "1000rub_note",
        "100rub_note",
        "10kop",
        "10rub_coin",
        "1rub_coin",
        "2000rub_note",
        "200rub_note",
        "2rub_coin",
        "5000rub_note",
        "500rub_note",
        "50kop",
        "50rub_note",
        "5rub_coin",
        "5rub_note",
        "backsite", "not_money",
        "1 kopeck",
        "1 ruble",
        "10 kopecks",
        "10 rubles",
        "100 rubles",
        "1000 rubles",
        "2 rubles",
        "200 rubles",
        "2000 rubles",
        "5 kopecks",
        "5 rubles",
        "50 kopecks",
        "50 rubles",
        "500 rubles",
        "5000 rubles"

    ]

    __yolo_classes_sum = {
        "5-kopecks": 0.05,
        "10kop": 0.1, "50kop": 0.5, "1rub_coin": 1, "2rub_coin": 2, "5rub_coin": 5,
        "5rub_note": 5, "10rub_coin": 10, "50rub_note": 50, "100rub_note": 100, "200rub_note": 200,
        "500rub_note": 500, "1000rub_note": 1000, "2000rub_note": 2000, "5000rub_note": 5000,
        "backsite": 0, "not_money": 0,"1 kopeck": 0.01,
        "1 ruble": 1,
        "10 kopecks": 0.1,
        "10 rubles": 10,
        "100 rubles": 100,
        "1000 rubles": 1000,
        "2 rubles": 2,
        "200 rubles": 200,
        "2000 rubles": 2000,
        "5 kopecks": 0.05,
        "5 rubles": 5,
        "50 kopecks": 0.5,
        "50 rubles": 50,
        "500 rubles": 500,
        "5000 rubles": 5000
    }
    __colors = {
        "1000rub_note": (255, 0, 0),
        "100rub_note": (0, 255, 0),
        "10kop": (0, 0, 255),
        "10rub_coin": (255, 255, 0),
        "1rub_coin": (0, 255, 255),
        "2000rub_note": (255, 0, 255),
        "200rub_note": (192, 192, 192),
        "2rub_coin":(128, 128, 128),
        "5000rub_note":(128, 0, 0),
        "500rub_note": (128, 128, 0),
        "50kop": (0, 128, 0),
        "50rub_note": (128, 0, 128),
        "5rub_coin": (0, 128, 128),
        "5rub_note": (0, 0, 128),
        "backsite": (47, 79, 47), "not_money": (0, 206, 209),
        "1 kopeck":(72, 61, 139),
        "1 ruble": (0, 255, 255),
        "10 kopecks": (0, 0, 255),
        "10 rubles": (255, 255, 0),
        "100 rubles": (0, 255, 0),
        "1000 rubles": (255, 0, 0),
        "2 rubles":(128, 128, 128),
        "200 rubles": (192, 192, 192),
        "2000 rubles": (255, 0, 255),
        "5 kopecks": (0, 0, 128),
        "5 rubles": (0, 128, 128),
        "50 kopecks": (0, 128, 0),
        "50 rubles": (128, 0, 128),
        "500 rubles": (128, 128, 0),
        "5000 rubles": (128, 0, 0)

    }

    @abstractmethod
    def use(self, image: bytes) -> ModelResult:
        ...
        

    @staticmethod
    def __classify_item(item_path: str):
        result = YOLO8Model.model_classifier(item_path)
        probs = result[0].probs  # Class probabilities for classification outputs
        money_class = result[0].names[probs.top1]
        probability = probs.top1conf.item()
        return money_class, probability

    @staticmethod
    def __detect_objects_on_image(buf, num: int):

        input, img_width, img_height = YOLO8Model.__prepare_input(buf)
        output = YOLO8Model.__run_model(input, num)
        return YOLO8Model.__process_output(output,img_width,img_height)

    @staticmethod
    def __prepare_input(buf):
        img = Image.open(io.BytesIO(buf))
        img_width, img_height = img.size
        img = img.resize((640, 640))
        img = img.convert("RGB")
        input = np.array(img)
        input = input.transpose(2, 0, 1)
        input = input.reshape(1, 3, 640, 640) / 255.0
        return input.astype(np.float32), img_width, img_height

    @staticmethod
    def __run_model(input, num: int):
        # Это модель детекции
        if(num == 1):
            outputs = YOLO8Model.model_detector_M.run(["output0"], {"images":input})
        elif(num == 2):
            outputs = YOLO8Model.model_detector_N.run(["output0"], {"images": input})
        else:
            outputs = YOLO8Model.model_detector_S.run(["output0"], {"images": input})
        return outputs[0]

    @staticmethod
    def __iou(box1,box2):
        return YOLO8Model.__intersection(box1,box2)/YOLO8Model.__union(box1,box2)

    @staticmethod
    def __union(box1,box2):
        box1_x1,box1_y1,box1_x2,box1_y2 = box1[:4]
        box2_x1,box2_y1,box2_x2,box2_y2 = box2[:4]
        box1_area = (box1_x2-box1_x1)*(box1_y2-box1_y1)
        box2_area = (box2_x2-box2_x1)*(box2_y2-box2_y1)
        return box1_area + box2_area - YOLO8Model.__intersection(box1,box2)

    @staticmethod
    def __intersection(box1,box2):
        box1_x1,box1_y1,box1_x2,box1_y2 = box1[:4]
        box2_x1,box2_y1,box2_x2,box2_y2 = box2[:4]
        x1 = max(box1_x1,box2_x1)
        y1 = max(box1_y1,box2_y1)
        x2 = min(box1_x2,box2_x2)
        y2 = min(box1_y2,box2_y2)
        return (x2-x1)*(y2-y1)

    @staticmethod
    def __process_output(output, img_width, img_height):
        output = output[0].astype(float)
        output = output.transpose()

        boxes = []
        for row in output:
            prob = row[4:].max()
            if prob < 0.5:
                continue
            class_id = row[4:].argmax()
            label = YOLO8Model.__yolo_classes[class_id]
            xc, yc, w, h = row[:4]
            x1 = (xc - w/2) / 640 * img_width
            y1 = (yc - h/2) / 640 * img_height
            x2 = (xc + w/2) / 640 * img_width
            y2 = (yc + h/2) / 640 * img_height
            boxes.append([x1, y1, x2, y2, label, prob])

        boxes.sort(key=lambda x: x[5], reverse=True)
        result = []
        while len(boxes) > 0:
            result.append(boxes[0])
            boxes = [box for box in boxes if YOLO8Model.__iou(box, boxes[0]) < 0.7]
        return result


    @classmethod
    def __work_with_items(cls, img: bytes, coordinates_list: list): # drawing and classifiyng

        image = Image.open(io.BytesIO(img))
        font = ImageFont.truetype(Path('src/cv_models/core/Karla-VariableFont_wght.ttf').resolve(), 60)
        i = 0
        sum = 0
        money_classes = []
        img_byte_array = []
        for coords in coordinates_list:
            image_copy = image.copy()
            x, y, width, height, value, precision = coords
            draw = ImageDraw.Draw(image)
            cropped = image_copy.crop((x, y, width, height))
            # Сохранение нарезок. Потом убрать
            # //
            item_path = f"{i}Result.jpeg"
            cropped.save(item_path)
            # //
            img_byte= io.BytesIO()
            cropped.save(img_byte, format="JPEG")
            img_byte_array.append(img_byte.getvalue())
            money_class, prob = YOLO8Model.__classify_item(item_path)
            sum += YOLO8Model.__yolo_classes_sum[money_class]

            text = f"{money_class}\n{round(prob, 3)}"
            draw.rectangle((x, y, width, height), outline=YOLO8Model.__colors[money_class], width=5)
            draw.text((x, y, width, height), text=text, fill=None, font=font, anchor=None, spacing=0, align="left")

            money_classes.append(money_class)
            i += 1
        # Сохранение главной картинки. Потом убрать
        # //

        cls.nums_of_processed_images += 1

        # Create a byte buffer in memory
        img_byte_main_buffer = io.BytesIO()
        # Save the image with drawn boxes to the buffer
        image.save(img_byte_main_buffer, format="JPEG")
        # Get the bytes from the buffer
        processed_image_bytes = img_byte_main_buffer.getvalue()

        return sum, processed_image_bytes, img_byte_array


    @staticmethod
    def _Yolo8M_Work(img: bytes):
        coordinates_list = YOLO8Model.__detect_objects_on_image(img, 1)
        message_sum, img_byte_main, img_byte_array = YOLO8Model.__work_with_items(img, coordinates_list)

        return ModelResult(message_sum, img_byte_main, img_byte_array)


    @staticmethod
    def _Yolo8N_Work(img: bytes):
        coordinates_list = YOLO8Model.__detect_objects_on_image(img, 2)
        message_sum, img_byte_main, img_byte_array = YOLO8Model.__work_with_items(img, coordinates_list)

        return ModelResult(message_sum, img_byte_main, img_byte_array)


    @staticmethod
    def _Yolo8S_Work(img: bytes):
        coordinates_list = YOLO8Model.__detect_objects_on_image(img, 3)
        message_sum, img_byte_main, img_byte_array = YOLO8Model.__work_with_items(img, coordinates_list)

        return ModelResult(message_sum, img_byte_main, img_byte_array)
    

class YOLO8N(YOLO8Model):

    name = CVModel.YOLO8N

    def __init__(self) -> None:
        super().__init__()

    def use(self, image: bytes):
        return self._Yolo8N_Work(image)


class YOLO8S(YOLO8Model):

    name = CVModel.YOLO8S

    def __init__(self) -> None:
        super().__init__()

    def use(self, image: bytes):
        return self._Yolo8S_Work(image)


class YOLO8M(YOLO8Model):

    name = CVModel.YOLO8M

    def __init__(self) -> None:
        super().__init__()

    def use(self, image: bytes):
        return self._Yolo8M_Work(image)