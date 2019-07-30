import cv2


def display(pixels, title="Camera Output"):
    """Displays the given capture in a CV2 window. Useful for debugging

    Args:
        pixels: MxNx3 array of pixels
        title: The title of the window

    """
    cv2.namedWindow(title)
    cv2.moveWindow(title, 500, 500)
    cv2.imshow(title, pixels[:, :, 0:3])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
