import io

import onnxruntime as ort
from PIL import Image, ImageDraw
import numpy as np

from PIL import ImageFont
from ultralytics import YOLO
from pathlib import Path

# from roboflow import Roboflow
#
#
# rf = Roboflow(api_key="z1B73yP5LSQJhcOeuKL9")
# project = rf.workspace().project("detect-money")
# model = project.version(2).model
class CVModel:

    model_detector_M = ort.InferenceSession(Path('cv_models\\cv_processing\\NewDetector.onnx').resolve())
    model_detector_N = ort.InferenceSession(Path('cv_models\\cv_processing\\DetectN.onnx').resolve())
    model_detector_S = ort.InferenceSession(Path('cv_models\\cv_processing\\DetectorS.onnx').resolve())
    model_classifier = YOLO(Path('cv_models\\cv_processing\\classifier.pt').resolve())

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
    @staticmethod
    def __classify_item(item_path: str):
        result = CVModel.model_classifier(item_path)
        probs = result[0].probs  # Class probabilities for classification outputs
        money_class = CVModel.__yolo_classes[probs.top1]
        probability = probs.top1conf.item()
        return money_class, probability

    @staticmethod
    def __detect_objects_on_image(buf, num: int):

        input, img_width, img_height = CVModel.__prepare_input(buf)
        output = CVModel.__run_model(input, num)
        return CVModel.__process_output(output,img_width,img_height)

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
            outputs = CVModel.model_detector_M.run(["output0"], {"images":input})
        elif(num == 2):
            outputs = CVModel.model_detector_N.run(["output0"], {"images": input})
        else:
            outputs = CVModel.model_detector_S.run(["output0"], {"images": input})
        return outputs[0]

    @staticmethod
    def __iou(box1,box2):
        return CVModel.__intersection(box1,box2)/CVModel.__union(box1,box2)

    @staticmethod
    def __union(box1,box2):
        box1_x1,box1_y1,box1_x2,box1_y2 = box1[:4]
        box2_x1,box2_y1,box2_x2,box2_y2 = box2[:4]
        box1_area = (box1_x2-box1_x1)*(box1_y2-box1_y1)
        box2_area = (box2_x2-box2_x1)*(box2_y2-box2_y1)
        return box1_area + box2_area - CVModel.__intersection(box1,box2)

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
            label = CVModel.__yolo_classes[class_id]
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
            boxes = [box for box in boxes if CVModel.__iou(box, boxes[0]) < 0.7]
        return result

    @staticmethod
    def __work_with_items(task_id: int, img: bytes, coordinates_list: list): # drawing and classifiyng

        image = Image.open(io.BytesIO(img))
        font = ImageFont.truetype(Path(f'cv_models\\cv_processing\\Karla-VariableFont_wght.ttf').resolve(), 60)
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
            money_class, prob = CVModel.__classify_item(item_path)
            sum += CVModel.__yolo_classes_sum[money_class]

            text = f"{money_class}\n{round(prob, 3)}"
            draw.rectangle((x, y, width, height), outline=CVModel.__colors[money_class], width=5)
            draw.text((x, y, width, height), text=text, fill=None, font=font, anchor=None, spacing=0, align="left")

            money_classes.append(money_class)
            i += 1
        # Сохранение главной картинки. Потом убрать
        # //
        image.save(Path(f'database\\images\\processed\\{task_id}Result.jpeg'))
        # //
        img_byte_main = io.BytesIO()            
        image.save(img_byte_main, format="JPEG")
        img_byte_main = img_byte_main.getvalue()

        return sum, img_byte_main, img_byte_array

    @staticmethod
    def Yolo8M_Work(task_id: int, img: bytes):
        coordinates_list = CVModel.__detect_objects_on_image(img, 1)
        message_sum, img_byte_main, img_byte_array = CVModel.__work_with_items(task_id, img, coordinates_list)
        return message_sum, img_byte_main, img_byte_array

    @staticmethod
    def Yolo8N_Work(task_id: int, img: bytes):
        coordinates_list = CVModel.__detect_objects_on_image(img, 2)
        message_sum, img_byte_main, img_byte_array = CVModel.__work_with_items(task_id, img, coordinates_list)
        return message_sum, img_byte_main, img_byte_array

    @staticmethod
    def Yolo8S_Work(task_id: int, img: bytes):
        coordinates_list = CVModel.__detect_objects_on_image(img, 3)
        message_sum, img_byte_main, img_byte_array = CVModel.__work_with_items(task_id, img, coordinates_list)
        return message_sum, img_byte_main, img_byte_array

# Тестовый код. Конвертирует картинку в байтовый формат для передачи в метод
# //
# file_name = f"neuro_processing/0ЫЫЫЫЫЫ.jpeg"

# img = Image.open(file_name)
# img_byte = io.BytesIO()
# img.save(img_byte, format="JPEG")
# img_byte = img_byte.getvalue()
# # //

# # МЕТОД, КОТОРЫЙ ДЕЛАЕТ ВСЮ МАГИЮ
# message_sum, img_byte_main, img_byte_array = Model.Yolo8M_Work(img_byte)

# print(message_sum)
# print(img_byte_main)