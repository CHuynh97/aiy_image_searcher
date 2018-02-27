FROM resin/rpi-raspbian

RUN apt-get update
RUN apt-get install -y \
    gcc \
    python-pip \
    cython \
    git \
    wget \
    libsm6 \
    libxrender-dev \
    python-opencv \
    python-numpy \
    portaudio19-dev \
    python-pyaudio \
    python-picamera

RUN apt-get install -t jessie python-dev

RUN pip install --upgrade pip

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN pip install https://www.piwheels.hostedpi.com/simple/tensorflow/tensorflow-1.1.0-cp27-none-linux_armv7l.whl

RUN cd "/" && \
    git clone https://github.com/thtrieu/darkflow.git && \
    cd darkflow && \
    pip install -e .

WORKDIR /darkflow

RUN mkdir weights
# RUN wget https://pjreddie.com/media/files/yolo.weights -P weights
RUN wget https://pjreddie.com/media/files/tiny-yolo.weights -P weights

ADD image_predict.py image_predict.py
ADD cat.jpg cat.jpg

RUN usermod -G videos ${USER}

CMD python image_predict.py cfg/tiny-yolo.cfg weights/tiny-yolo.weights 0.1