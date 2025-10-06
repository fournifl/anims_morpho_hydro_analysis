import datetime

import cv2


def read_img(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    split_name = path.name.split("_")
    img_date_str = (
        split_name[-3] + "_" + split_name[-2] + "_" + split_name[-1].split(".")[0]
    )
    img_date = datetime.datetime.strptime(img_date_str, "%Y%m%d_%H_%M")
    return img, img_date
