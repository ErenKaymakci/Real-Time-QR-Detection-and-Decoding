# Real Time QR Detection & Decoding 🚀
<a href='https://www.python.org/' target="_blank"><img alt='Python' src='https://img.shields.io/badge/Made_With Python-100000?style=for-the-badge&logo=Python&logoColor=white&labelColor=3774A7&color=FFD445'/></a>
<a href='https://github.com/ErenKaymakci/Real-Time-QR-Detection-and-Decoding/blob/main/LICENSE' target="_blank"><img alt='' src='https://img.shields.io/badge/MIT_Lıcense-100000?style=for-the-badge&logo=&logoColor=white&labelColor=3774A7&color=000000'/></a>

## Contents   
- [What is QR Code](#what-is-qr-code)
- [How QR Works](#how-qr-works)
- [About Project](#about-project)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Conclusion](#conclusion)
- [License](#license)

## What is QR Code
Quick response(QR) code is 10x faster than barcodes. In history, companies used barcodes for keep track of their stocks. But barcodes only store up to 20 alphanumeric characters. So QR codes invented by Japanese company Denzo Wave in 1994. QR codes can store up to 4296 alphanumeric characters.

## How QR Works
We can basically define QR code like `2D array`. QR codes range from 11x11(called micro QR) pixels up to 177x177. White pixels represents 0, black pixels represents 1. 

The image in the below shows the constant areas in QR code:

![image](/imgs/explained.png)



## About Project
- **Dataset**: I've mixed my custom data with this dataset: 
https://www.kaggle.com/datasets/hamidl/yoloqrlabeled

- Project has 2 stage. 
   - QR Detection
   - QR Decoding 
 
- Detection being done with YOLOv5. 4 options can be used for decoding process: `pyboof`, `dbr`, `pyzbar`, `cv2` 
- **Process**: detection ➡️ decoding ➡️ print results

## Installation
```
git clone https://github.com/ErenKaymakci/Real-Time-QR-Detection-and-Decoding
cd Real-Time-QR-Detection-and-Decoding
pip install -r requirements.txt
```
## Usage
`python main.py`

Detection parameters can be changed in here: 

https://github.com/ErenKaymakci/Real-Time-QR-Detection-and-Decoding/blob/main/yolo.py#L16

Decoding options can be changed with comment/uncomment in here: 

https://github.com/ErenKaymakci/Real-Time-QR-Detection-and-Decoding/blob/main/main.py#L21

## Results


## Conclusion

## License
[MIT](https://github.com/ErenKaymakci/Real-Time-QR-Detection-and-Decoding/blob/main/LICENSE)

