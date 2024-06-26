# Import required libraries
import cv2
import face_recognition

# Capture video from default camera
webcam_video_stream = cv2.VideoCapture(0)

# Load samples and retrieve 128 face encodings for each
face_1 = face_recognition.load_image_file('Dataset/Arigovinthan.jpg')
face_1_encodings = face_recognition.face_encodings(face_1)[0]
face_1_name = 'Name:Arigovinthan/Reg.No:420120104003/Dept:CSE/Phone:8072099257'

face_2 = face_recognition.load_image_file('Dataset/Surendhar.jpg')
face_2_encodings = face_recognition.face_encodings(face_2)[0]
face_2_name = 'Name:Surendhar/Reg.No:420120104045/Dept:CSE/Phone:7339679520'

face_3 = face_recognition.load_image_file('Dataset/Vijayanandh.jpg')
face_3_encodings = face_recognition.face_encodings(face_3)[0]
face_3_name = 'Name:Vijayanandh/Reg.No:420120104310/Dept:CSE/Phone:7708503265'

# Save encodings and corresponding labels to separate arrays in same order
known_face_encodings = [face_1_encodings, face_2_encodings, face_3_encodings, face_4_encodings]
known_face_names = [face_1_name, face_2_name, face_3_name, face_4_name]

# Initialize arrays for face locations, encodings, and names
all_face_locations = []
all_face_encodings = []
all_face_names = []

# Loop through each video frame until user exits
while True:
    ret, current_frame = webcam_video_stream.read()

    # Let's use a smaller version (0.25x) of the image for faster processing
    scale_factor = 4
    current_frame_small = cv2.resize(
        current_frame, (0, 0), fx=1/scale_factor, fy=1/scale_factor)

    # Find total number of faces, encodings, set names to empty
    all_face_locations = face_recognition.face_locations(
        current_frame_small, number_of_times_to_upsample=2, model='hog')
    
    all_face_encodings = face_recognition.face_encodings(current_frame_small, all_face_locations)
    
    all_face_names = []
    
    # Iterate through each face location and encoding in our test image
    for current_face_location, current_face_encoding in zip(all_face_locations, all_face_encodings):
        # Splitting up tuple of face location
        top_pos, right_pos, bottom_pos, left_pos = current_face_location
        
        # Correct positions based on scale factor
        top_pos *= scale_factor
        right_pos *= scale_factor
        bottom_pos *= scale_factor
        left_pos *= scale_factor
        
        # Now we'll slice our image array to isolate the faces
        current_face_image = current_frame[top_pos: bottom_pos,
                                                left_pos:right_pos]

        # Compare to known faces to check for matches
        all_matches = face_recognition.compare_faces(
            known_face_encodings, current_face_encoding)

        # Initialize name string as unknown face
        name_of_person = 'Unknown Face'

        # Check if all_matches isn't empty
        # If yes get the index number corresponding to the face in the first index
        if True in all_matches:
            first_match_index = all_matches.index(True)
            name_of_person = known_face_names[first_match_index]

        # Draw rectangle around face
        cv2.rectangle(current_frame, (left_pos, top_pos),
                      (right_pos, bottom_pos), (255, 0, 255), 2)

        # Write corresponding name below face
        font = cv2.FONT_HERSHEY_DUPLEX
        print(f'Detected: {name_of_person}')
        cv2.putText(current_frame, name_of_person, (left_pos,
                    bottom_pos + 20), font, 0.5, (0, 0, 255), 1)

        # Display image with rectangle and text
        cv2.imshow('Footprint Detection', current_frame)
        
    # Press spacebar key to exit loop
    if cv2.waitKey(1) == ord(' '):
        break

webcam_video_stream.release()
cv2.destroyAllWindows()
