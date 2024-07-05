import os
import pydicom
import cv2
import numpy as np
from PIL import Image
from moviepy.editor import ImageSequenceClip

def dicom_to_images(dicom_file):
    ds = pydicom.dcmread(dicom_file)
    pixel_data = ds.pixel_array
    pixel_data = cv2.normalize(pixel_data, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    if len(pixel_data.shape) == 3:
        frames = [Image.fromarray(frame) for frame in pixel_data]
    else:
        frames = [Image.fromarray(pixel_data)]
    
    return frames

def convert_to_rgb(image):
    if len(image.shape) == 2:  # Grayscale
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return image

def images_to_mp4(images, output_file, fps=24):
    if not images:
        raise ValueError("No images to convert to MP4")
    
    frames = [convert_to_rgb(np.array(image)) for image in images]
    
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_file, codec="libx264")

def main(dicom_file, output_file):
    images = dicom_to_images(dicom_file)
    print(f"Number of frames extracted: {len(images)}")
    if images:
        print(f"Shape of the first frame: {np.array(images[0]).shape}")
    images_to_mp4(images, output_file)

if __name__ == "__main__":
    dicom_file = "IM0.unknown"  # Replace with the path to your DICOM file
    output_file = os.path.join(os.getcwd(), "output.mp4")
    print(f"Saving video to: {output_file}")
    main(dicom_file, output_file)
