## "I, a universe of atoms, an atom in the universe" Richard Feynman

When I was young, I sometimes look into the sky and ask myself. As a speck of dust in this vast universe, will my existence have any meaning? Will my action can make any change in this world? After a long time of self-exploring, self-explanation, reading, and listening, I think I have found some answers to those questions. Throughout history, humans have changed the course of nature by using 2 things: the ability to work together and the ability to use tools. By working together with other people as a Company and with the right tool, which is Data in our era, I will be on the right path to change myself and change a small part of this world. And that is what I believe.

# Project: [YOLO_face_mask_detection](https://github.com/TranPhu1999/YOLO_face_mask_detection)
In this project:
- Train a Yolov3 model to detect Face mask wearing with Kaggle Face Mask Dataset (Tensorflow, OpenCV, Numpy)
- Build a Flask API that receive image send it to one of the two Yolov3 models (first one is pretrained model on COCO dataset, the second one is the model that I just train above) as input and send image result to a web interface (flask)
- Build a simple web interface that Upload image from user then send it to Flask API, receive and display the output (HTML, CSS, JavaSript)

|![Input](images/maksssksksss0.png) | ![Output](images/download.png)|

![Interface](/images/image.png)


# Project: [Explore and predict Vietnam weather](https://github.com/TranPhu1999/Explore_Predict_Vietnam-weather)
In this project:
- Write code to call API and request data about Vietnam weather from openweathermap.org (request, pandas, numpy)
- Explore and preprocess data: check null, check duplicate, check data distribution, reformat data for modeling (pandas, numpy, matplotlib, seaborn)
- Build LogisticRegression Classifier and Naive Bayes Classifier to try to predict the weather after 12h from the current time (pandas, Sklearn)

![img](images/Explore_Predict_Vietnam%20weather.png)


# Project: [Sentiment_analysis](https://github.com/TranPhu1999/Sentiment_analysis)
In this project:
- Crawl Airpod review data from Amazon (Selenium)
- Manualy label review sentence as Positive and Negative, remove spelling mistake, typos,... (pandas)
- Using TF-IDF, BERT and fastText to create embeddings for each sentences
- Store data on MongoDB cloud
- Connect to MongoDB, extract data and use logistic regression and Support Vector Machine to build classification model

![img](/images/Sentiment_analysis_project.png)





