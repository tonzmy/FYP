from flask import Flask, send_file
from flask import jsonify
from flask import request
import requests
from io import BytesIO
from PIL import Image
import base64
import time
import numpy as np
# yolov3
from yolov3.yolo_image import detect_img
# yolov2
from yolov2.darkflow.net.build import TFNet

# yolov2
tinyv2_options = {"model": "yolov2/cfg/tiny-yolo-voc-4c.cfg", "load": 6000, "threshold": 0.1}
fullv2_options = {"model": "yolov2/cfg/yolo-voc-4c.cfg", "load": 10900, "threshold": 0.1}
tinyv2 = TFNet(tinyv2_options)
print("tiny v2 is loaded")
fullv2 = TFNet(fullv2_options)
print("full v2 is loaded")

app = Flask(__name__, static_url_path='/static')

def countNum(bus, car, motorbike, truck, results):
    totalNum = len(results)
    if totalNum < 12:
        level = 'Light'
    elif totalNum < 24:
        level = 'Moderate'
    else:
        level ='Heavy'

    for i in range(len(results)):
        name = results[i]['label']
        if name == 'bus':
            bus = bus + 1
        elif name == 'motorbike':
            motorbike = motorbike + 1
        elif name == 'truck':
            truck = truck + 1
        elif name == 'car':
            car = car + 1
        else:
            continue
    return bus, car, motorbike, truck, level

@app.route('/', methods=['GET'])
def showImage():
    return app.send_static_file('index.html')


@app.route('/image', methods=['POST'])
def getImage():
    ts = str(int(time.time()))
    message = request.get_json(force=True)
    cameraId = str(message['cameraId'])
    url = 'http://www.dsat.gov.mo/cams/cam' + cameraId + '/AxisPic-Cam' + cameraId + '.jpg?' + ts;

    with requests.get(url) as response:
        if response.status_code == 200 and response.headers['Content-type'] == 'image/jpeg':
            tinyv2_bus = tinyv2_car = tinyv2_motorbike = tinyv2_truck = tinyv2_num = 0
            fullv2_bus = fullv2_car = fullv2_motorbike = fullv2_truck = fullv2_num = 0
            v3_bus = v3_car = v3_motorbike = v3_truck = v3_num = 0
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            np_img = np.asarray(img)

            # tiny v2
            tinyv2_results = tinyv2.return_predict(np_img)
            tinyv2_bus, tinyv2_car, tinyv2_motorbike, tinyv2_truck, tinyv2_level = countNum(tinyv2_bus, tinyv2_car, tinyv2_motorbike, tinyv2_truck, tinyv2_results)

            # yolov2
            fullv2_results = fullv2.return_predict(np_img)
            fullv2_bus, fullv2_car, fullv2_motorbike, fullv2_truck, fullv2_level = countNum(fullv2_bus, fullv2_car, fullv2_motorbike, fullv2_truck, fullv2_results)

            # yolov3
            v3_results = detect_img(img)
            # print(v3_results)
            v3_bus, v3_car, v3_motorbike, v3_truck, v3_level = countNum(v3_bus, v3_car, v3_motorbike, v3_truck, v3_results)

            #tasks: return json format content and results; test
            content = base64.b64encode(img_data)
            data = {
                'numbers': [
                    {
                        'tinyv2_bus': tinyv2_bus,
                        'tinyv2_car': tinyv2_car,
                        'tinyv2_truck': tinyv2_truck,
                        'tinyv2_motorbike': tinyv2_motorbike,
                        'tinyv2_level': tinyv2_level
                    },
                    {
                        'fullv2_bus': fullv2_bus,
                        'fullv2_car': fullv2_car,
                        'fullv2_truck': fullv2_truck,
                        'fullv2_motorbike': fullv2_motorbike,
                        'fullv2_level': fullv2_level
                    },
                    {
                        'v3_bus': v3_bus,
                        'v3_car': v3_car,
                        'v3_motorbike': v3_motorbike,
                        'v3_truck': v3_truck,
                        'v3_level': v3_level
                    }
                ],
                'content': content
            }

            return jsonify(data)
            # return response.text
        else:
            return 'error'
