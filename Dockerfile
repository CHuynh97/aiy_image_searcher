FROM tensorflow/tensorflow

RUN apt-get update
RUN apt-get install -y \
    python-pip \
    cython \
    git \
    wget \
    libsm6 \
    libxrender-dev

RUN pip install opencv-python

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN cd "/" && \
    git clone https://github.com/thtrieu/darkflow.git && \
    cd darkflow && \
    pip install -e .

WORKDIR /darkflow

RUN mkdir weights
RUN wget https://pjreddie.com/media/files/yolo.weights -P weights

ADD image_predict.py image_predict.py

CMD python image_predict.py cfg/yolo.cfg weights/yolo.weights 0.1