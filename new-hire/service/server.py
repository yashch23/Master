import flask
from flask import Flask, render_template, request, Response
import json
import spacy
import re
filename = "document.jpg"

def getDocumentDetails(data):
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
   import spacy
   import io
   try:
       from PIL import Image
   except ImportError:
       import Image
   #data1=request.data.decode('utf-8')
   data1 = data
   
   #IMG_20190726_114742.jpg
   #text = pytesseract.image_to_string(Image.open(data1))
   image = Image.open(io.BytesIO(data1))
   import random
   #filename = "filename" + str(random.randint(1, 100000)) + ".jpg";
   #try :
    #   filename = "filename" + str(random.randint(1, 100000)) + ".jpg";
   #except:
    #   filename = "filename" + str(random.randint(1, 100000)) + ".png";
   try:
       image.save(filename)
   except:
       image.save(filename)
   import numpy as np
   import cv2
   img = cv2.imread(filename, -1)
   rgb_planes = cv2.split(img)
   result_planes = []
   result_norm_planes = []
   for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255,
                          norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
   result_norm_planes.append(norm_img)
   result = cv2.merge(result_planes)
   result_norm = cv2.merge(result_norm_planes)
   cv2.imwrite(filename, result)
    # cv2.imwrite('shadows_out_norm.png', result_norm)
   document_details = pytesseract.image_to_string(filename)
   return document_details;
app = Flask(__name__)
@app.route('/document_details', methods=['GET','POST'])
def index():
   document_details = getDocumentDetails(request.data);
   doc_type = request.args.get("doc_type");
       
   if (doc_type != 'bank') :
        resp = flask.Response(document_details);
        resp.headers['Content-Type'] = 'text/html';
   else :
        data = bank_details(document_details);
        result = json.dumps(data);
        resp = flask.Response(result);
        resp.headers['Content-Type'] = 'application/json';
   
   
   resp.headers['Access-Control-Allow-Origin'] = '*';
   resp.headers['Access-Control-Allow-Methods'] = 'POST';
   resp.headers['Access-Control-Allow-Headers'] = 'Accept, Content-Type, Authorization';
   return resp;
   
#@app.route('/bank_details', methods=['GET','POST', 'OPTIONS'])
def bank_details(document_details):
   text = document_details;
   ifscode=str(0)
   accnum=str(0)
   fl=0
   import numpy as np
    
   text1 = text
   for word in (text1.split()):
       #print("********************************1 " + word.encode('utf-8'))
       try:
            val = int(word)
            if(len(str(val)) >= 13):
                accnum= str(val)
            #if(re.search("[A-Z|a-z]{4}[0][/d]{6}$", word)):
                #ifscode=word;
       except ValueError:
            qwerty = 0
        #if(word=='CODE' or fl==1 or word=='COE' or word=='IFS' or word=='IFS CODE'):
         #   print("********************************")
          #  fl=1
           # if(word!=" " and word!="-" ):
            #    print("********************************2")
             #   ifscode=word
              #  fl=0
   nlp = spacy.load("en_core_web_sm", disable=["parser"])
   doc = nlp(text)
   #print(doc)
   orgs= [entity.text for entity in doc.ents if entity.label_=="ORG"]
   banks = ['AXIS BANK', "UNION BANK", "AXIS BANK LTD", 'CORPORATION BANK', "ALLAHABAD BANK", "AMERICAN EXPRESS", "ANDHRA BANK", "ARAB BANGLADESH", "BANK OF BARODA", "BANK MUSCAT", "BANK OF AMERICA", "BANK OF INDIA", "BANK OF MAHARASHTRA", "BANK OF PUNJAB", "BANK OF RAJASTHAN", "BARCLAYS", "BHARAT OVERSEAS", "CANARA BANK", "CATHOLIC SYRIAN", "CENTURION", "CEYLON", "CITIBANK", "CORPORATION", "COSMOS CO-OPERATIVE BANK", "DBS", "DENA", "DEUTSCHE BANK", "DEVELOPMENT CREDIT", "DHANLAKSHMI", "EXPORT-IMPORT BANK OF INDIA", "FEDERAL BANK", "GLOBAL TRUST", "HDFC", "HONGKONG SHANGHAI BANKING", "ICICI BANK", "IDBI BANK", "IND BANK HOUSING", "INDIAN OVERSEAS", "INDUSIND BANK", "INDUSTRIAL DEVELOPMENT", "ING VYSYA", "JAMMU AND KASHMIR", "JP MORGAN CHASE", "KARNATAKA", "KARUR VYSYA", "KOTAK MAHINDRA", "LAKSHMI VILAS", "LORD KRISHNA", "MIZUHO CORPORATE", "MUDRA BANK", "THE NAINITAL BANK LTD.", "NORTH KNARA G.S.B. CO-OP.", "ORIENTAL BANK OF COMMERCE", "PUNJAB AND SIND", "PUNJAB NATIONAL", "RATNAKAR", "RESERVE BANK OF INDIA", "ROYAL BANK OF SCOTLAND", "SBI COMMERCIAL", "SHAMRAO VITHAL CO-OPERATIVE", "SHREE MAHAVIR SAHAKARI BANK LTD.", "SOUTH INDIAN", "STANDARD CHARTERED", "STATE BANK OF BIKANER & JAIPUR", "STATE BANK OF HYDERABAD", "STATE BANK OF INDIA", "STATE BANK OF INDORE", "STATE BANK OF MYSORE", "STATE BANK OF PATIALA", "STATE BANK OF TRAVANCORE", "SYNDICATE BANK", "TAMILNAD MERCANTILE", "UCO BANK", "UNITED BANK OF INDIA", "VIJAYA BANK", "YES BANK"]
   flag=0
   bankname=""
   #accnum=0
   for element1 in orgs:
       element2 = element1.upper()
       for elementb in banks:
           if(element2 == elementb):
               bankname=element1
               flag=1
               break
   if(flag==0):
       text1=text.upper()
       for elementb in banks:
           if(text1.find(elementb)!=-1):
               bankname=elementb
               break
   #numbers= [token.lemma_ for token in doc if token.pos_=="NUM"]
   #for number in numbers:
   #    if(len(number)==15):
    #       accnum=number
     #      break
   from skimage.segmentation import clear_border
   from imutils import contours
   import imutils
   import numpy as np
   import argparse
   import imutils
   import cv2
   def extract_digits_and_symbols(image, charCnts, minW=5, minH=15):
       charIter = charCnts.__iter__()
       rois = []
       locs = []
       while True:
           try:
               c = next(charIter)
               (cX, cY, cW, cH) = cv2.boundingRect(c)
               roi = None
               if cW >= minW and cH >= minH:
                   roi = image[cY:cY + cH, cX:cX + cW]
                   rois.append(roi)
                   locs.append((cX, cY, cX + cW, cY + cH))
               else:
                   parts = [c, next(charIter), next(charIter)]
                   (sXA, sYA, sXB, sYB) = (np.inf, np.inf, -np.inf,
                       -np.inf)
                   for p in parts:
                       (pX, pY, pW, pH) = cv2.boundingRect(p)
                       sXA = min(sXA, pX)
                       sYA = min(sYA, pY)
                       sXB = max(sXB, pX + pW)
                       sYB = max(sYB, pY + pH)
                   roi = image[sYA:sYB, sXA:sXB]
                   rois.append(roi)
                   locs.append((sXA, sYA, sXB, sYB))
           except StopIteration:
               break
       return (rois, locs)
   charNames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
       "T", "U", "A", "D"]
   ref = cv2.imread("micr_e13b_reference.png")
   ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
   ref = imutils.resize(ref, width=400)
   ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV |
       cv2.THRESH_OTSU)[1]
   refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,
       cv2.CHAIN_APPROX_SIMPLE)
   refCnts = imutils.grab_contours(refCnts)
   refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
   refROIs = extract_digits_and_symbols(ref, refCnts,
       minW=10, minH=20)[0]
   chars = {}
   for (name, roi) in zip(charNames, refROIs):
       roi = cv2.resize(roi, (36, 36)) 
       chars[name] = roi
   rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 7))
   output = []
   image = cv2.imread(filename)
   (h, w,) = image.shape[:2]
   delta = int(h - (h * 0.2))
   bottom = image[delta:h, 0:w]
   gray = cv2.cvtColor(bottom, cv2.COLOR_BGR2GRAY)
   blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
   gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0,
       ksize=-1)
   gradX = np.absolute(gradX)
   (minVal, maxVal) = (np.min(gradX), np.max(gradX))
   gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
   gradX = gradX.astype("uint8")
   gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
   thresh = cv2.threshold(gradX, 0, 255,
       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
   thresh = clear_border(thresh)
   groupCnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
       cv2.CHAIN_APPROX_SIMPLE)
   groupCnts = groupCnts[0] 
   groupLocs = []
   for (i, c) in enumerate(groupCnts):
       (x, y, w, h) = cv2.boundingRect(c)
       if w > 50 and h > 15:
           groupLocs.append((x, y, w, h))
   groupLocs = sorted(groupLocs, key=lambda x:x[0])
   for (gX, gY, gW, gH) in groupLocs:
       groupOutput = []
       group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
       group = cv2.threshold(group, 0, 255,
           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
       charCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,
           cv2.CHAIN_APPROX_SIMPLE)
       charCnts = imutils.grab_contours(charCnts)
       charCnts = contours.sort_contours(charCnts,
           method="left-to-right")[0]
       (rois, locs) = extract_digits_and_symbols(group, charCnts)
       for roi in rois:
           scores = []
           roi = cv2.resize(roi, (36, 36))
           for charName in charNames:
               result = cv2.matchTemplate(roi, chars[charName],
                   cv2.TM_CCOEFF)
               (_, score, _, _) = cv2.minMaxLoc(result)
               scores.append(score)
           groupOutput.append(charNames[np.argmax(scores)])
       cv2.rectangle(image, (gX - 10, gY + delta - 10),
           (gX + gW + 10, gY + gY + delta), (0, 0, 255), 2)
       cv2.putText(image, "".join(groupOutput),
           (gX - 10, gY + delta - 25), cv2.FONT_HERSHEY_SIMPLEX,
           0.95, (0, 0, 255), 3)
       #output.append(bankname)
       #output.append(accnum)
       output.append("".join(map(str, groupOutput)))
   data = {};
   data['bank_name'] = bankname;
   data['account_number'] = accnum;
   data['micr'] = "{}".format(" ".join(map(str, output)));
   #data['ifsc']=ifscode;
   return data;
   
   
if __name__ == '__main__':
   #app.run(debug=True, host='localhost', port=9773)
   #app.run(host= '0.0.0.0',ssl_context='adhoc')
   app.run(host= '0.0.0.0', port=3310,ssl_context='adhoc')
   #app.run(debug=False, host= '10.166.70.150', port=9773)
   #app.run(debug=True, host= '70.34.58.20', port=9773)
   # port = int(os.environ.get('PORT', 5000))
   # app.run(host="127.0.0.1", port=port)