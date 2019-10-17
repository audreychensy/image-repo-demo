from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from image_searcher import ColorDescriptor, Searcher
from index import extractFeatures
import cv2
import os
import numpy
from shutil import copy


## could be done in a separate create-app function for more config options
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

## index all images in dataset
extractFeatures()
INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')


@app.route('/api/clean', methods=['DELETE'])
def mvfile():
    ## remove cached images
    dir = "my-app/public"
    files = os.listdir(dir)
    for file in files:
        if file.endswith(".jpg"):
            os.remove(os.path.join(dir,file))
            print("removed ", file)
    return "success"

@app.route('/api/searchImg', methods=['POST'])
def search():
    RESULTS_ARRAY = []
    try:
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))

        # load the query image and describe it
        #read image file string data
        filestr = request.files['img'].read()
        #convert string data to numpy array
        npimg = numpy.fromstring(filestr, numpy.uint8)
        # convert numpy array to image
        query = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
        # query = cv2.imread(img)
        query = (query * 255).astype("uint8")
        (r, g, b) = cv2.split(query)
        query = cv2.merge([b, g, r])
        features = cd.describe(query)

        # perform the search
        searcher = Searcher(INDEX)
        results = searcher.search(features)

        # loop over the results, displaying the score and image name
        for (score, resultID) in results:
            RESULTS_ARRAY.append(str(resultID)
                # {"image": str(resultID), "score": str(score)}
                )
        # copy result images to react public folder for display
        r = RESULTS_ARRAY[:4]
        
        for img in r:
            dirs = [img[i:i+4] for i in range(0, 12, 4)]
            path = "dataset/" + '/'.join(dirs) + '/' + img
            copy(path, "my-app/public")
        
        #return success
        return jsonify({"results": RESULTS_ARRAY[:4]})

    except:
        # return error
        return jsonify({"sorry": "Sorry, no results! Please try again."}), 500

    

if __name__ == '__main__':
    app.run()