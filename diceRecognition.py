import sys
import cv2
import numpy as np


def get_dice_intensity(cap, background, dice_number, calibration):
    kernel = np.ones((7, 7), np.uint8)
    if calibration:
        frame_title = 'Kalibrace = ' + str(dice_number)
    else:
        frame_title = 'Snimek'
    while True:
        calibration_done = False
        ret, image = cap.read()
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        substracted = cv2.subtract(background, image_gray)
        ret, thresholded_image = cv2.threshold(substracted, 140, 255, cv2.THRESH_BINARY)
        morphed_image = cv2.dilate(thresholded_image, kernel, iterations=1)
        cv2.imshow(frame_title, morphed_image)
        dice_intensity_value = cv2.countNonZero(morphed_image)
        if calibration:
            if cv2.waitKey(10) & 0xFF == ord('q'):
                calibration_done = True
            if calibration_done:
                return dice_intensity_value
        else:
            return dice_intensity_value


def find_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    dice = 'neznam'
    if idx == 0:
        dice = 'jedna'
    elif idx == 1:
        dice = 'dva'
    elif idx == 2:
        dice = 'tri'
    elif idx == 3:
        dice = 'ctyri'
    elif idx == 4:
        dice = 'pet'
    elif idx == 5:
        dice = 'sest'
    return dice


def main(argv):
    dices_intensity = np.zeros(6)
    calibration_number = 1
    kernel = np.ones((7, 7), np.uint8)
    print argv
    cap = cv2.VideoCapture(0)
    # ziskani pozadi
    print 'Ziskej pozadi a stiskni q'
    while True:
        ret, image = cap.read()
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Pozadi', image_gray)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            background = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            break

    for x in np.nditer(dices_intensity, op_flags=['readwrite']):
        x[...] = get_dice_intensity(cap, background, calibration_number, True)
        calibration_number += 1

    while True:
        dice_value = get_dice_intensity(cap, background, calibration_number, False)
        print(find_nearest(dices_intensity, dice_value))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main(sys.argv)

