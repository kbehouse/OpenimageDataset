import json
import csv
# from openimaeg_util import class_name_2_id
ClassName_2_ID_File = './' + 'class-descriptions-boxable.csv'
Bbox_labels_600_hierarchy = './' + 'bbox_labels_600_hierarchy.json'
Bbox_labels_600_hierarchy_toName =  './' + 'bbox_labels_600_hierarchy_to_name.json'
'''
input:  class id  
output: class name   (same as annotation LabelName)
'''
def class_id_2_name(class_id):
    # print('class_id = ', class_id)
    with open(ClassName_2_ID_File, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if class_id==row[0]:
                # print('class_id = ', class_id,', row[0]=', row[0],', row[1]=', row[1])
                return row[1]
    return ""

# convert into JSON:
# y = json.dumps(x)
# print(y)
def parse_subcategory(subcategory, include_id = False):
    for n in subcategory:
        # print('n = ', n, ', len(n)=',len(n))
        if 'LabelName' in n: 
            if include_id:
                n['LabelName'] =  class_id_2_name(n['LabelName'] ) + ' (' + n['LabelName']  + ')'
            else:
                n['LabelName'] =  class_id_2_name(n['LabelName'] )
        if 'Subcategory' in n and 'LabelName' in n:
            # parse_subcategory(n['Subcategory'])
            parse_item(n, include_id)
            # print("in 'Subcategory' in n and 'LabelName' in n")

def parse_item(x, include_id):     
    for k, v in x.items():
        if k == 'LabelName':          
            if include_id:
                x[k] = class_id_2_name(v) + ' (' + v + ')'
            else:
                x[k] = class_id_2_name(v)
        elif k == 'Subcategory' or k== 'Part':
            parse_subcategory(x[k], include_id)

with open(Bbox_labels_600_hierarchy) as json_file:  
    j = json.load(json_file)
    parse_item(j, True)
    with open( Bbox_labels_600_hierarchy_toName, 'w') as outfile:  
        json.dump(j, outfile, indent=2)
