import cv2
import os

def video_to_images(video_path, output_folder, fps=1):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Capture the video from the specified path
    video_capture = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video_capture.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    # Get the total number of frames in the video
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get the frame rate of the video
    video_fps = video_capture.get(cv2.CAP_PROP_FPS)

    # Calculate the interval between frames to capture (in terms of frame number)
    frame_interval = int(video_fps / fps)

    frame_count = 0
    saved_frame_count = 0

    while True:
        # Read frame-by-frame
        ret, frame = video_capture.read()

        # If the frame was not retrieved successfully, end of video is reached
        if not ret:
            break

        # Only save the frame if it meets the interval criteria
        if frame_count % frame_interval == 0:
            # Define the output image file path
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count:04d}.jpg")

            # Save the current frame as an image file
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")

            saved_frame_count += 1

        frame_count += 1

    # Release the video capture object
    video_capture.release()
    print("Video processing complete. All frames have been saved.")

# Example usage:
video_path = 'IM0.mp4'
output_folder = 'pics'
video_to_images(video_path, output_folder)
