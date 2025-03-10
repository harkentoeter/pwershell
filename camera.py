import cv2
import os

def take_picture(save_dir="C:/Path/To/Save", initial_file_name="picture"):
    os.makedirs(save_dir, exist_ok=True)
    file_count = 1
    full_path = None

    while True:
        file_name = f"{initial_file_name}{file_count}.png"
        full_path = os.path.join(save_dir, file_name)
        
        if not os.path.exists(full_path):
            break
        
        file_count += 1
    
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        return None, "Error: Could not access the camera."

    retval, img = camera.read()
    
    camera.release()
    cv2.destroyAllWindows()

    if not retval:
        return None, "Error: Failed to capture image."

    cv2.imwrite(full_path, img)
    return full_path, "Image saved successfully."

