import numpy as np
import gc
import cv2
import face_recognition
import os
import uuid
import pickle


def find_encodings(img: np.ndarray):
    encodings = None
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)[0]
    except Exception as err:
        print(err, str(type(err)))
    gc.collect()
    return encodings


def is_print_required(msg: str, req: bool = True):

    if req:
        print(msg)


def create_face_database(directory: str, rm_blur_img: bool = False, threshold: float = 100.0,
                         display: bool = True):
    encodings = []
    
    if not os.path.exists(directory):
        raise FileNotFoundError("Directory not found")

    files = next(os.walk(directory))[-1].copy()

    num_files = len(files)
    if num_files > 0:
        db_dir = str(uuid.uuid4())
        db_dir = db_dir.replace("-", "_")
        os.makedirs(db_dir)
    else:
        raise FileNotFoundError("No files found in directory")

    ctr = 1
    for i in range(num_files):
        img = cv2.imread(directory + files[i])
        blurriness = cv2.Laplacian(img, cv2.CV_64F).var()

        if rm_blur_img:
            if blurriness >= threshold:
                pass
            else:
                is_print_required(f'{i + 1} / {num_files} -- skipped due to blurriness {blurriness}',
                                  display)
                continue

        # crop face image if required
        # code can be added here
        
        face_encoding = find_encodings(img)
        if face_encoding is not None:
            cv2.imwrite(f'{db_dir}/img_{ctr}.jpg', img)
            encodings.append({'img_path': f'{db_dir}/img_{ctr}.jpg',
                              'encoding': face_encoding})
            is_print_required(f'{i+1} / {num_files} -- used for database', display)
            ctr += 1
        else:
            is_print_required(f'{i+1} / {num_files} -- skipped due to face not found', display)

    num_of_data = ctr - 1
    f = open(f'{db_dir}/face_encodings.p', 'wb')
    pickle.dump(encodings, f)
    f.close()
    gc.collect()
    return db_dir, num_of_data
