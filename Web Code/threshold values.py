import requests
token2 = 'patdUkV4ikC0l5VLo'
token = 'patdUkV4ikC0l5VLo.2f761ebff9da11df77cefec5e522c664d8dbfd456cb436a7e5de5b6608cc3297'
baseid = 'appt3YptNUKHPvP9U'

cv2_image = cv2.cvtColor(np.array(cam.raw_image), cv2.COLOR_RGB2BGR)
b,g,r = cv2.split(cv2_image)
grey = cv2.cvtColor(cv2_image, cv2.COLOR_BGRA2GRAY)
cam.show(grey)  # shows any cv2 image in the same spot on the webpage (third image)
image3 = Image.fromarray(grey)
rg = r - g
rb = r - b
rg = np.clip(rg, 0, 255)
rb = np.clip(rb, 0, 255)

def change_airtable_cell(table_name, field_id, value):
    url = f'https://api.airtable.com/v0/{baseid}/{table_name}'
    auth_token = token
    headers = {'Authorization': f"Bearer {auth_token}","Content-Type":"application/json"}
    data = {
  "records": [
    {
        "id": field_id,
      "fields": {
        "Colour": value
      }
    }
  ]
}
    try:
        response = requests.patch(url, headers=headers, json=data)
        print(response.text)
        response.close()
    except Exception as e:
        print("Error:", str(e))
### DETECT RED ### 
img_hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
redmask1 = cv2.inRange(img_hsv, (0,50,20), (5,255,255))
redmask2 = cv2.inRange(img_hsv, (175,50,20), (180,255,255))
# Merge the mask and crop the red regions
redmask = cv2.bitwise_or(redmask1, redmask2)

# Threshold Image
_,redbin=cv2.threshold(redmask,50,255,cv2.THRESH_BINARY)
kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.uint8)
'''or 
erosion_size = 1
element = cv2.getStructuringElement(cv2.MORPH_RECT, (2 * erosion_size + 1, 2 * erosion_size + 1),
 (erosion_size, erosion_size))
'''
rederoded = cv2.erode(redbin, kernel)
reddilated = cv2.dilate(rederoded, kernel)
rnzcount = cv2.countNonZero(reddilated)
print(rnzcount)
#textBox.innerText=repr(np.sum(grey))
display(Image.fromarray(reddilated))

### DETECT BLUE ###
img_hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
bluemask1 = cv2.inRange(img_hsv, (100,50,20), (155,255,255))
bluemask2 = cv2.inRange(img_hsv, (175,50,20), (180,255,255))
# Merge the mask and crop the red regions
bluemask = cv2.bitwise_or(bluemask1, bluemask2)
# Threshold Image
_,bluebin=cv2.threshold(bluemask,50,255,cv2.THRESH_BINARY)
kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.uint8)
'''or 
erosion_size = 1
element = cv2.getStructuringElement(cv2.MORPH_RECT, (2 * erosion_size + 1, 2 * erosion_size + 1),
 (erosion_size, erosion_size))
'''
blueeroded = cv2.erode(bluebin, kernel)
bluedilated = cv2.dilate(blueeroded, kernel)
bnzcount = cv2.countNonZero(bluedilated)
print(bnzcount)
#textBox.innerText=repr(np.sum(grey))
display(Image.fromarray(bluedilated))

### DETECT GREEN ###
img_hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
greenmask1 = cv2.inRange(img_hsv, (36,50,20), (86,255,255))
greenmask2 = cv2.inRange(img_hsv, (175,50,20), (180,255,255))
# Merge the mask and crop the red regions
greenmask = cv2.bitwise_or(greenmask1, greenmask2)
# Threshold Image
_,greenbin=cv2.threshold(greenmask,50,255,cv2.THRESH_BINARY)
kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.uint8)
'''or 
erosion_size = 1
element = cv2.getStructuringElement(cv2.MORPH_RECT, (2 * erosion_size + 1, 2 * erosion_size + 1),
 (erosion_size, erosion_size))
'''
greeneroded = cv2.erode(greenbin, kernel)
greendilated = cv2.dilate(greeneroded, kernel)
gnzcount = cv2.countNonZero(greendilated)
print(gnzcount)
#textBox.innerText=repr(np.sum(grey))
display(Image.fromarray(greendilated))

if gnzcount > rnzcount and gnzcount > bnzcount:
    print('green')
    change_airtable_cell('tempData',"rectXe6J7oTAOytqs",'Green')
if rnzcount > bnzcount and rnzcount > gnzcount:
    print('red')
    change_airtable_cell('tempData',"rectXe6J7oTAOytqs",'Red')
if bnzcount > rnzcount and bnzcount > gnzcount:
    print('blue')
    change_airtable_cell('tempData',"rectXe6J7oTAOytqs",'Blue')
    
