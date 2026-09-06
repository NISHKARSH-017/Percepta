import cv2


def load_chart(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not load the image.")

    return image


def get_image_info(image):
    height, width, channels = image.shape

    return {
        "width": width,
        "height": height,
        "channels": channels
    }


def resize_image(image, max_width=1500):
    height, width = image.shape[:2]

    if width <= max_width:
        return image

    scale = max_width / width

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized = cv2.resize(image, (new_width, new_height))

    return resized


# Testing
if __name__ == "__main__":
    image = load_chart("test_chart.png")

    print("Image loaded successfully!")

    info = get_image_info(image)
    print("Original image information:", info)

    resized_image = resize_image(image)

    success = cv2.imwrite("processed_chart.png", resized_image)
    print("Processed image saved:", success)

    resized_info = get_image_info(resized_image)
    print("Resized image information:", resized_info)
