from yolo import YOLOv5
from decoder import QR_Decoder
import cv2

def main():

    cap = cv2.VideoCapture(0)
    yolo = YOLOv5()
    decoder = QR_Decoder()
    while True:
        ret, frame = cap.read()

        if ret:
            objects, out = yolo.detect(frame)
            if len(objects) > 0:
                for x1, y1, x2, y2  in objects: # x1 = x, y1 = y,  x2 = x + w, y2 = y + h

                    cropped = out[y1:y2, x1:x2]

                    decoder.decode_w_pyzbar(cropped)
                    #decoder.decode_w_cv2(cropped)
                    #decoder.decode_w_dbr(frame) # or you can entire image(frame)
                    #decoder.decode_w_pyboof(cropped)
                    
            cv2.imshow("frame", out)
            
        if cv2.waitKey(5) & 0xFF == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()