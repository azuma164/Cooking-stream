import cv2
import mediapipe as mp
from control import Control

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

landmarks_global = None
category_global = None
actioned = -1


def print_result(
    result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int
):
    # ジェスチャーが認識されたときの処理をここに追加
    if len(result.gestures) > 0:
        for idx in range(len(result.gestures[0])):
            gesture = result.gestures[0][idx]
            if gesture.category_name == "None":
                return
            print("gesture recognition result: {}".format(gesture))
            global actioned
            if gesture.category_name == "Pointing_Up":
                if actioned == -1:
                    Control.unmute_microphone()
                    actioned = 0
            elif gesture.category_name == "Thumb_Up":
                if actioned == -1:
                    Control.mute_microphone()
                    actioned = 0
            if gesture.category_name != "None":
                # 手のランドマークの座標を取得
                landmarks = result.hand_landmarks
                global landmarks_global, category_global
                landmarks_global, category_global = landmarks[0], gesture.category_name
                return


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    model_path = "./models/gesture_recognizer.task"
    base_options = BaseOptions(model_asset_path=model_path)

    options = GestureRecognizerOptions(
        base_options=base_options,
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result,
    )

    with GestureRecognizer.create_from_options(options) as recognizer:
        timestamp = 0
        while cap.isOpened():
            if actioned != -1:
                actioned += 1
            if actioned >= 20:
                actioned = -1

            timestamp += 1
            ret, frame = cap.read()
            if not ret:
                break

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            recognizer.recognize_async(mp_image, timestamp)

            image_height, image_width, _ = frame.shape
            if landmarks_global is not None:
                x_min, y_min = int(landmarks_global[0].x * image_width), int(
                    landmarks_global[0].y * image_height
                )
                x_max, y_max = int(landmarks_global[9].x * image_width), int(
                    landmarks_global[9].y * image_height
                )

                # cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                cv2.putText(
                    frame,
                    f"Category: {category_global}",
                    (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )
            cv2.imshow("Gesture Recognition", frame)

            # キーイベントを待機し、Escキーで終了
            if cv2.waitKey(1) & 0xFF == 27:
                break

    # 後処理
    cap.release()
    cv2.destroyAllWindows()
