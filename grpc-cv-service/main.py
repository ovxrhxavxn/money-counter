import grpc
from concurrent import futures
import logging

# Import from your new shared package!
from src.money_counter_protos.generated import cv_pb2, cv_pb2_grpc 
# Import your model logic
from src.cv_models.core.yolo8model import YOLO8N, YOLO8S, YOLO8M

# Set up logging
logging.basicConfig(level=logging.INFO)

class ComputerVisionServicer(cv_pb2_grpc.ComputerVisionServicer):
    def __init__(self):
        # Create instances of your models, ready to use
        self.models = {
            cv_pb2.YOLO8N: YOLO8N(),
            cv_pb2.YOLO8S: YOLO8S(),
            cv_pb2.YOLO8M: YOLO8M(),
        }
        logging.info("YOLO models loaded.")

    def ProcessImage(self, request, context):
        logging.info(f"Received request for model type: {cv_pb2.ModelType.Name(request.model_type)}")

        # Select the correct model based on the request
        model_to_use = self.models.get(request.model_type)

        if not model_to_use:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid model type specified")
            return cv_pb2.ProcessResponse()

        try:
            # Your YOLO8Model classes have a 'use' method, but it returns a namedtuple.
            # Let's assume the processed image is in `img_byte_main`.
            # You might need to adjust this based on what `_Yolo8N_Work` etc. return.
            # Looking at your yolo8model.py, the use() method returns a ModelResult namedtuple.
            # The second item in that tuple seems to be the main image bytes.
            model_result = model_to_use.use(request.image_data)
            processed_image_bytes = model_result.img_byte_main

            logging.info("Image processed successfully.")
            return cv_pb2.ProcessResponse(image_data=processed_image_bytes)

        except Exception as e:
            logging.error(f"Error processing image: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An internal error occurred: {e}")
            return cv_pb2.ProcessResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cv_pb2_grpc.add_ComputerVisionServicer_to_server(ComputerVisionServicer(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("gRPC server starting on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
