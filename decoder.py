import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import pyboof as pb
from dbr import BarcodeReader

class QR_Decoder:

    def __init__(self):
        # dbr
        self.dbr_reader = BarcodeReader()
        license_key = "LICENSE KEY" # if you have LICENSE key, write here 
        self.dbr_reader.init_license(license_key)

        #pyboof
        self.pb_detector = pb.FactoryFiducial(np.uint8).qrcode() 
        
        #cv2
        self.cv2_detector = cv2.QRCodeDetector()


    def decode_w_pyzbar(self,frame):
        datas = list()
        decoded = pyzbar.decode(frame)
        for obj in decoded:
            print("- pyzbar result: ", obj.data)
            

        
    def decode_w_dbr(self,frame):
        decoded_qrs = self.dbr_reader.decode_buffer(frame)
        if decoded_qrs != None:
            for decoded in decoded_qrs:
                print(f"- dbr result: {decoded.barcode_text}")


    def decode_w_pyboof(self,frame):
        # pyboof input must be grayscaled 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        boof_img = pb.ndarray_to_boof(gray)

        self.pb_detector.detect(boof_img)
        for qr in self.pb_detector.detections:
            print(f"- pyboof result: ", qr.message)
            

    def decode_w_cv2(self,frame):
        data, vertices_array, binary_qrcode = self.cv2_detector.detectAndDecode(frame)
        if vertices_array is not None:
            print("- OpenCV result:", data)

