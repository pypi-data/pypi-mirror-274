import cv2
from cv_smart_house_camera.modules.modules_processing import modules_processing

def cam_capture():
    cap = cv2.VideoCapture(0)  # 0 for default webcam, change if necessary
    frame_number = 0
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                break
            frame_number += 1

            modules_processing(frame, frame_number)
            # cv2.imshow('Webcam', frame)

            # if cv2.waitKey(1) & 0xFF == ord('q'):
                # break

        except Exception as e:
            print(f"Error processing frame {frame_number}: {e}")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cam_capture()