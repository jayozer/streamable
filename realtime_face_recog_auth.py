import streamlit as st
import cv2
import face_recognition

# Define a list of authorized users
authorized_users = [
    {
        "name": "Jay",
        "image_path": "/Users/jozer/Documents/GitHub/dialectify/images/jay.jpeg"
    },
    {
        "name": "Jay_two",
        "image_path": "/Users/jozer/Documents/GitHub/dialectify/images/jay_two.png"
    }
]

# Define the Streamlit app
def app():
    # Set the app title
    st.title("Real-Time Facial Recognition Authentication")

    # Create the video capture object
    cap = cv2.VideoCapture(0)

    # Load the authorized user's images
    authorized_face_encodings = []
    for user in authorized_users:
        authorized_image = face_recognition.load_image_file(user["image_path"])
        authorized_face_encoding = face_recognition.face_encodings(authorized_image)[0]
        authorized_face_encodings.append(authorized_face_encoding)

    # Start the video capture loop
    while True:
        # Read a frame from the video capture object
        ret, frame = cap.read()

        # Convert the frame to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all the faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Check if any of the faces match an authorized user
        authorized = False
        for face_encoding in face_encodings:
            results = face_recognition.compare_faces(authorized_face_encodings, face_encoding)
            if True in results:
                authorized = True
                break

        # Display the frame with face locations and the authentication result
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        if authorized:
            cv2.putText(frame, "Authorized", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Unauthorized", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Real-Time Facial Recognition Authentication", frame)

        # Check if the user has pressed the 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the window
    cap.release()
    cv2.destroyAllWindows()