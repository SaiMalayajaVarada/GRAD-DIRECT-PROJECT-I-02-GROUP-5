from sklearn.cluster import DBSCAN
import numpy as np
import cv2
import pickle
import os


def do_cluster(src_dir: str, jobs: int = -1):
    f = open(f'{src_dir}/face_encodings.p', 'rb')
    data = pickle.load(f)
    f.close()

    # you can modify the eps value to fine tune your model
    # in my case 0.41 is working fine.
    clt = DBSCAN(eps=0.41, metric="euclidean", n_jobs=jobs)
    encodings = [d["encoding"] for d in data]
    clt.fit(encodings)
    labels_id = np.unique(clt.labels_)
    num_unique_faces = len(np.where(labels_id > -1)[0])
    print('unique faces found: ', num_unique_faces)
    res_dir = f'result_{src_dir}'
    for labelID in labels_id:
        # print("[INFO] faces for face ID: {}".format(labelID))
        idxs = np.where(clt.labels_ == labelID)[0]
        os.makedirs(f'result_{src_dir}/{labelID}')
        ctr = 0
        for i in idxs:
            image = cv2.imread(data[i]["img_path"])
            cv2.imwrite(f'result_{src_dir}/{labelID}/{ctr}.jpg', image)
            ctr += 1
    print(f'Cluster has been stored in "{res_dir}" directory')
    return num_unique_faces, res_dir


def get_best_pics(num_unique_faces: int, res_dir: str):
 
    fine_images = []
    for i in range(num_unique_faces):
        files = next(os.walk(f'{res_dir}/{i}'))[-1].copy()
        best_score = 0
        best_img = None
        for file in files:
            img = cv2.imread(f'{res_dir}/{i}/{file}')
            bluriness = cv2.Laplacian(img, cv2.CV_64F).var()
            if bluriness > best_score:
                best_score = bluriness
        fine_images.append(best_img)
    return fine_images
