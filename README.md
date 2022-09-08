# GRAD-DIRECT-PROJECT-I-02-GROUP-5
> A project for demonstrating the team collaboration.

## Team Members and Roles

- Zabheen Shaik - Web Application Developer.
- Jessica Salome - Developer
- Sai Malayaja Varada - Quality Assurance Tester
- Bhavishya Yarapathineni - Cloud Developer
- Prasanna - Android Application Developer

## Abstract

> Identifying and spotting a criminal is a time-consuming and difficult process.Criminals are becoming smarter by not leaving biological evidence or fingerprint impressions at crime scenes. 
using cutting-edge face recognition systems is a simple and quicksolution.Cameras are being installed at most building structures as well as traffic lights for military surveillance since safety technology evolves.The sensor video footage can be used to identify suspects, criminals, runaways, and missing people,among other things. 


## Overview of Face Recognition Methodology

1. Face Detection: The task of detection images surrounding it using bounding boxes an d cropping out uncessary parts of the image. The detection process is the foundtion for further  tasks as the face cannot be identified before it is recognised. An image can contain more than one phase. This step is acheived using various detection techniques.MTCNN was directly implemented MTCNN library. All images are loaded as numpy array and converted to RGB files.Face

2. Face Embedding: Face embeddings need to be created so comparisions with different vectors acn be done.This is the step where the FaceNet model was used for creating embeddings. After loading the compressed file of detected faces the  pixel  values need to be standardized as it is required for FaceNet.

3. Face Classification: In this part of the process, embeddings are classified  using machine learning models to be identified as one of the criminals. Before applying a classification, model vector normalization is applied so values are scaled. The  scikit  learn normalization library is used for this  purpose. Next,  the names of the criminals are converted from string to integer format. This is done using LabelEncoder of scikit learn. The classification model used is Linear  Support  Vector Machine as it is effective for differentiating between the face embeddings. The linear SVM model is fit on the training data.

4.Plotting Face: To visualize the working of this entire model a face from the compressed test set is picked. Then embeddings for this image are created. This face embedding is  used as input to  fit in the model and get predictions.

## APP DEVELOPMENT (FACE DETECTION AND RECOGNISION USING ANDROID STUDIO)

### Overview
In older days to identify a man, there needs to check his/her id proof and match his/her face with the attached picture on that id card of that person. There were some problems in this process sometimes the person may not keep the face with him then we cannot identify the man then. Another problem is that if the face is too old then the picture that on the face detection may not be clear so we cannot identify it. There is a possibility of the changing of the face with the increasing of age. If the face recognition will made a long time ago then the present time face is not matched with the id card photo then we cannot identify the man who is he. Nowadays we can easily identify a man by using a face detection app. only need an android device that contains a camera no need of keeping face always with him/her.
### Required steps
For face recognition, we should use an image with dimensions of at least 480x360 pixels. For ML Kit to accurately detect faces, input images must contain faces represented by sufficient pixel data. Generally, each face we want to detect in an image should be at least 100x100 pixels. If we want to detect the contours of faces, ML Kit requires higher resolution input: each face should be at least 200x200 pixels.
If we detect faces in a real-time application, you might also want to consider the overall dimensions of the input images. Smaller images can be processed faster, so to reduce latency, capture images at lower resolutions, but keep in mind the above accuracy requirements and ensure that the subject's face occupies as much of the image as possible. In this project, we can implement an android studio application with the help of Android studio using java language.






