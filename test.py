import cv2
import os

def take_picture():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(downloads_path, exist_ok=True)

    file_count = 1
    while True:
        file_name = f"picture{file_count}.png"
        full_path = os.path.join(downloads_path, file_name)
        
        if not os.path.exists(full_path):
            break
        
        file_count += 1

    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("Error: Could not access the camera.")
        return

    retval, img = camera.read()
    
    camera.release()
    cv2.destroyAllWindows()

    if not retval:
        print("Error: Failed to capture image.")
        return

    cv2.imwrite(full_path, img)
    print(f"Image saved successfully at {full_path}")

if __name__ == "__main__":
    take_picture()

