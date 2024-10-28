import numpy as np
import cv2
import mediapipe as mp
import os
import shutil

print("Current Working Directory:", os.getcwd())

def filter_hands_exposure_time(hands_exposure_time, directory, output_directory,number_of_hands,show):
    '''
    This function saves in the output directory inly videos that exceed the exposure time given.
    number of hands indicate on how many hands is enough for saving the video.

    :param hands_exposure_time: the minimal required exposure time of the hands
    :param directory: input directory if unfilltered videos
    :param output_directory: output directory of filltered videos
    :param number_of_hands: how many hands is enough for saving the video
    :return: --
    '''

    # make media pipe objects
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                           min_tracking_confidence=0.5)

    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            video_path = os.path.join(directory, filename)

            #for drawing
            mp_drawing = mp.solutions.drawing_utils

            # Open the video file
            cap = cv2.VideoCapture(video_path) #takes the video file
            frame_rate = cap.get(cv2.CAP_PROP_FPS) #Retrieves the frame rate of the video for total time visibility
            hands_visible_frames = 0
            total_frames = 0

            while cap.isOpened(): #reading the frames
                success, frame = cap.read()
                if not success:
                    break

                ## frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converting to rgb format readable by mediapipe
                results = hands.process(frame)

                #find hand landmarks
                if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == number_of_hands:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    hands_visible_frames += 1  # adding if hands are detected
                total_frames += 1  #total frames

                # Show the frame - can be removed during all videos processing
                if show == True:
                    cv2.imshow('Hands', frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break


            # calculations
            hand_visible_time = hands_visible_frames / frame_rate
            print(f'{filename} total hand visible time: {hand_visible_time:.2f} seconds')
            if hand_visible_time >= hands_exposure_time:
                dest_path = os.path.join(output_directory, filename)
                shutil.copy(video_path, dest_path)

            #release current video
            cap.release()

    hands.close()
    cv2.destroyAllWindows()


filter_hands_exposure_time(60,r".\exampels", r".\filterd",2 ,True)