import csv
import os
import shutil

Root_Dir = '../'
# Root_Dir = '/backup/openimage/v4/'
ClassName_2_ID_File = Root_Dir + 'class-descriptions-boxable.csv'
# Annot
Train_Annot_File = Root_Dir + 'train-annotations-bbox.csv'
Valid_Annot_File = Root_Dir + 'validation-annotations-bbox.csv'
Test_Annot_File = Root_Dir + 'test-annotations-bbox.csv'


'''
recrete directory by dir_name
if dir_name exist, remove it  
'''
def recreate_dir(dir_name):
    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)

    os.mkdir(dir_name)


'''
input: class name  
output: all ImageID
'''
def get_imageID_by_class_name(csv_name, class_name):
    class_id = class_name_2_id(class_name)
    imageID_list = []
    with open(csv_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if class_id==row[2]: #row[2] == labelName == class id
                if not row[0] in imageID_list:
                    imageID_list.append(row[0])

    return imageID_list
    
'''
input: class name  
output: class id   (same as annotation LabelName)
'''
def class_name_2_id(check_name):
    check_name = check_name.lower()
    with open(ClassName_2_ID_File, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            class_name = row[1]
            if len(row)>2:
                class_name = ' '.join(row[1:])
            if class_name.lower()==check_name:
                return row[0]
    return 0
'''
input: check name
output: all class name contains the check name
'''
def include_check_name(check_name):
    include_list = []
    check_name = check_name.lower()
    with open(ClassName_2_ID_File, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            class_name = row[1]
            if len(row)>2:
                class_name = ' '.join(row[1:])
            if check_name in class_name.lower():
                include_list.append(class_name)

    return include_list

'''
input: csv file path, check name
output: image ID list
'''
def include_check_name_imageID(csv_file, check_name):
    imgID_list = []
    include_list = include_check_name(check_name)
    for class_name in include_list:
        # class_id = class_name_2_id(class_name)
        tmp_imgID_list = get_imageID_by_class_name(csv_file, class_name)
        imgID_list = imgID_list + tmp_imgID_list

    return imgID_list

'''
input: src_dir, dst_dir, csv_file, include_name
result: copy all src_dir/[include name].jpg to [include_name]/*.jpg
'''
def copy_images_by_include_name(src_dir, dst_dir, csv_file, include_name):
    
    recreate_dir(dst_dir)
    imgID_list = include_check_name_imageID(csv_file, include_name)

    print(imgID_list)

    for imgID in imgID_list:
        src = src_dir+'/' + imgID +'.jpg'
        dst = dst_dir+'/' + imgID +'.jpg'
        print('COPY '+ src +' -> '+ dst)

        try:
            shutil.copyfile(src, dst)
        except Exception as e :
            print(e)

'''
input: src_csv_file, dst_csv_file, include_name
result: copy [src_csv_file] to [dst_csv_file] which LabelName name include [include_name]
'''
def copy_csv_by_include_name(src_csv_file, dst_csv_file, include_name):
    include_list = include_check_name(include_name)

    class_id_list = []
    for class_name in include_list:
        class_id_list.append(class_name_2_id(class_name))

    print('include_list -> ' + str(include_list))
    print('class_id_list -> ' + str(class_id_list))
    
    with open(src_csv_file, newline='') as rFile, open(dst_csv_file, 'w') as wFile:
        reader = csv.reader(rFile, delimiter=',', quotechar='|')
        writer = csv.writer(wFile)
        for row_ind, row in enumerate(reader):
            if row_ind==0:
                writer.writerow(row)
            elif row[2] in class_id_list: #row[2] == labelName == class id
                writer.writerow(row)

        print('CREATE ' + dst_csv_file)




'''
input: src_dir, dst_dir, csv_file, include_name
result: copy all src_dir/[include name].jpg to [include_name]/*.jpg
'''
def copy_images_by_classes_path(classes_path, src_dir, dst_dir, annot_file, for_train=False):
    classes=[]
    with open(classes_path) as f:
        classes = f.readlines()

    classes = [x.strip() for x in classes] 
    print("CLASSES: " + str(classes))

    imgID_list=[]

    print("GET Image ID from " + annot_file)
    for class_name in classes:
        tmp_imgID_list = get_imageID_by_class_name(annot_file,class_name)
        imgID_list = imgID_list + tmp_imgID_list

    if len(imgID_list) > 0:
        recreate_dir(dst_dir)


    # copy from src_dir to  dst_dir
    for imgID in imgID_list:
        src = src_dir+'/' + imgID +'.jpg'
        dst = dst_dir+'/' + imgID +'.jpg'
        print('COPY '+ src +' -> '+ dst)

        try:
            shutil.copyfile(src, dst)
        except Exception as e :
            print(e)


'''
input: src_dir, dst_dir, csv_file, include_name
result: copy all src_dir/[include name].jpg to [include_name]/*.jpg
'''
def copy_images_by_classes_path_for_train(classes_path, dst_dir, annot_file):
    TRAIN_DIR_MAX_ID = 8  # train_00~train_08
    classes=[]
    with open(classes_path) as f:
        classes = f.readlines()

    classes = [x.strip() for x in classes] 
    print("CLASSES: " + str(classes))

    imgID_list=[]

    print("GET Image ID from " + annot_file)
    for class_name in classes:
        tmp_imgID_list = get_imageID_by_class_name(annot_file,class_name)
        imgID_list = imgID_list + tmp_imgID_list

    if len(imgID_list) > 0:
        recreate_dir(dst_dir)

    img_unfind_list =[]
    # copy from train_00~train_08 to  dst_dir
    for imgID in imgID_list:
        dst = dst_dir+'/' + imgID +'.jpg'
        img_find = False
        for dir_ind in range(0, TRAIN_DIR_MAX_ID+1):
            traind_ind_dir = Root_Dir  + 'train_0' + str(dir_ind) +'/'
            src = traind_ind_dir + imgID +'.jpg'
            # print('Find '+ src)

            if os.path.isfile(src):
                try:
                    print('COPY '+ src +' -> '+ dst)
                    shutil.copyfile(src, dst)
                    img_find = True
                except Exception as e :
                    img_find = False
                    print(e)
                break
            
        if not img_find:
            img_unfind_list.append(imgID)
            print("NOT FIND " + imgID +'.jpg')

    print('NOT FIND List->' )
    print(img_unfind_list)


'''
input: src_csv_file, dst_csv_file, include_name
result: copy [src_csv_file] to [dst_csv_file] which LabelName name include [include_name]
'''
def copy_csv_by_class_path(classes_path, src_csv_file, dst_csv_file, check_file_dir = ''):
    # get classes name
    classes=[]
    with open(classes_path) as f:
        classes = f.readlines()

    classes = [x.strip() for x in classes]   # trip for deleting '\'...etc.
    print("CLASSES: " + str(classes))
   
    # get class id
    class_id_list = []
    for class_name in classes:
        class_id_list.append(class_name_2_id(class_name))
    print('class_id_list -> ' + str(class_id_list))
    
    with open(src_csv_file, newline='') as rFile, open(dst_csv_file, 'w') as wFile:
        reader = csv.reader(rFile, delimiter=',', quotechar='|')
        writer = csv.writer(wFile)
        for row_ind, row in enumerate(reader):
            if row_ind==0:
                writer.writerow(row)
            elif row[2] in class_id_list: #row[2] == labelName == class id
                if check_file_dir=='':
                    writer.writerow(row)
                else:
                    img_path = check_file_dir + row[0] + '.jpg'
                    if os.path.isfile(img_path):
                        writer.writerow(row)
                    else:
                        print('ImageID NOT EXIST at' + img_path)

        print('CREATE ' + dst_csv_file)

# print(name_2_id('Sea turtle')
# print('Gun List -> ' + str(  include_check_name('gun')) )
# print('Knife List -> ' + str(  include_check_name('Knife')) )
# Gun List -> ['Shotgun', 'Handgun']
# Knife List -> ['Knife', 'Kitchen knife']

# imgID_list = get_imageID_by_class_name(Valid_Annot_File,'Fruit')
# print(len(imgID_list))

# validation
# copy_images_by_include_name(Root_Dir + 'validation', Root_Dir + 'valid_gun', Valid_Annot_File, 'gun')
# copy_csv_by_include_name(Valid_Annot_File, Root_Dir + 'valid_gun/gun.csv', 'gun')

# train
# copy_images_by_include_name(Root_Dir + 'train_00', Root_Dir + 'train_00_gun', Train_Annot_File, 'gun')
# copy_images_by_include_name(Root_Dir + 'train_01', Root_Dir + 'train_01_gun', Train_Annot_File, 'gun')
# copy_images_by_include_name(Root_Dir + 'train_02', Root_Dir + 'train_02_danger', Train_Annot_File, 'gun')
# copy_images_by_include_name(Root_Dir + 'train_03', Root_Dir + 'train_03_gun', Train_Annot_File, 'gun')
# copy_images_by_include_name(Root_Dir + 'train_04', Root_Dir + 'train_04_gun', Train_Annot_File, 'gun')
# copy_images_by_include_name(Root_Dir + 'train_05', Root_Dir + 'train_05_gun', Train_Annot_File, 'gun')


############################### copy_images_by_classes_path ###############################
# train
# copy_images_by_classes_path_for_train('danger_classes.txt',Root_Dir +'train_danger', Train_Annot_File) # 'train_tmp_annot.csv'
# copy_images_by_classes_path_for_train('danger_classes.txt',Root_Dir +'train_danger', 'train_tmp_annot.csv')

# copy_csv_by_class_path('danger_classes.txt',Train_Annot_File, Root_Dir + 'train_danger/annot.csv', check_file_dir=Root_Dir +'train_danger/')

#valid 
# copy_images_by_classes_path('danger_classes.txt', Root_Dir + 'validation',Root_Dir + 'validation_danger',Valid_Annot_File)
# copy_csv_by_class_path('danger_classes.txt',Valid_Annot_File, Root_Dir + 'validation_danger/annot.csv')

# test 
copy_images_by_classes_path('danger_classes.txt', Root_Dir + 'test',Root_Dir + 'test_danger',Test_Annot_File)
copy_csv_by_class_path('danger_classes.txt',Test_Annot_File, Root_Dir + 'test_danger/annot.csv')
