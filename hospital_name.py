from fuzzywuzzy import fuzz
import cv2
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

image_path = "/Users/sivagar/Documents/work_projects/general_ocr/key_value/IP1167041 CARMONA HOSPITAL & MEDICAL CENTER INC (p7) (1page)_page-0007.jpg"
image = cv2.imread(image_path)
document_height, document_width, _ = image.shape  # Get the dimensions of the input image
threshold = 0.006*document_height

def extract_hospital_name(ocr_results, threshold,key_name = 'hospital name' ,line_param='same_line', value_index=1):
    mid_height_results = []
    for coordinates, (text, _) in ocr_results:
        mid_height = (coordinates[0][1] + coordinates[3][1]) / 2
        mid_height_results.append(((coordinates[0], coordinates[3]), (text, _), mid_height))
    sorted_results = mid_height_results
    key_match = None
    for (_, _), (text, _), mid_height in sorted_results:
        if similar(key_name.lower(), text.lower()) >= 0.9:
            key_match = text
            break
    if key_match is None:
        return None
    print(key_match)
    key_mid_height = None
    for (_, _), (text, _), mid_height in sorted_results:
        if text == key_match:
            key_mid_height = mid_height
            break
    if key_mid_height is None:
        return None
    max_next_line_height = key_mid_height + 4*threshold
    threshold2 = key_mid_height + threshold
    values = []
    for (coordinates[0], coordinates[3]), (text, _), mid_height in sorted_results:
        if line_param == 'same_line' and abs(mid_height - key_mid_height) <= threshold:
            values.append(((coordinates[0], coordinates[3]),text))
        elif line_param == 'next_line' and threshold2 < mid_height <= max_next_line_height:
            values.append(((coordinates[0], coordinates[3]),text))
    #print(values)
    sorted_strings = sorted(values, key=lambda x: x[0][0][0])
    result_strings = [item[1] for item in sorted_strings]
    if key_match in result_strings:
        i = result_strings.index(key_match)
        if 0 <= value_index < len(result_strings):
            return result_strings[i+value_index]
    else:
        if 0 <= value_index < len(result_strings):
                return result_strings[value_index]
        else:
            return None




hospital_name = extract_hospital_name(ocr_results,threshold)
print(hospital_name)