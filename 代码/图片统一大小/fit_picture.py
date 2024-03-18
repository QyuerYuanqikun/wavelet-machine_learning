from PIL import Image
import os

def resize_images_in_folder(source_folder, dest_folder, size=(512, 512)):
    """
    Resize all images in the specified folder to the given size and save them
    to the destination folder.

    :param source_folder: Folder containing the original images.
    :param dest_folder: Folder where resized images will be saved.
    :param size: Tuple specifying the new size (width, height).
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for file_name in os.listdir(source_folder):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(source_folder, file_name)
            img = Image.open(file_path)
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            save_path = os.path.join(dest_folder, file_name)
            resized_img.save(save_path)

source_folder = 'E:\wavelet\Image\Flickr1024 Dataset\Validation'
dest_folder = 'E:\wavelet\Image\Flickr1024 Dataset\Validation_same_size'
resize_images_in_folder(source_folder, dest_folder, size=(128, 128))
