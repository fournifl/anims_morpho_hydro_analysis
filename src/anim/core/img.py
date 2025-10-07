import datetime

import cv2


def read_img(path, resize_factor=0.25):
    img = cv2.imread(path)
    # converting BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # resize
    # width = int(img.shape[1] * resize_factor)
    # height = int(img.shape[0] * resize_factor)
    # img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    # date
    split_name = path.name.split("_")
    if path.suffix == ".jpg":
        img_date_str = (
            split_name[-3] + "_" + split_name[-2] + "_" + split_name[-1].split(".")[0]
        )
        img_date = datetime.datetime.strptime(img_date_str, "%Y%m%d_%H_%M")
    elif path.suffix == ".jpeg":
        img_date_str = split_name[-3] + "_" + split_name[-2]
        img_date = datetime.datetime.strptime(img_date_str, "%Y%m%d_%H%M%S")

    return img, img_date


def get_list_of_imgs(path, start, end):
    ls_imgs = sorted(path.glob("*.jpeg"))
    ls_imgs_ok = []
    for f in ls_imgs:
        split_name = f.name.split("_")
        img_date_str = split_name[-3] + "_" + split_name[-2]
        img_date = datetime.datetime.strptime(img_date_str, "%Y%m%d_%H%M%S")
        if img_date >= start and img_date <= end:
            ls_imgs_ok.append(f)
    return ls_imgs_ok
