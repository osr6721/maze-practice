#include <Servo.h>
Servo myservo;
char cmd;

void setup() {
  Serial.begin(9600); // 시리얼 통신 시작 (boadrate: 9600)
  myservo.attach(8);
}

void loop() {
  // 컴퓨터로부터 시리얼 통신이 전송되면, 한줄씩 읽어와서 cmd 변수에 입력
  if(Serial.available()){
    cmd = Serial.read(); 

    if(cmd=='a'){
      //Serial.println("a 수신완료");
      myservo.write(0);
      delay(500);
    }
    else if(cmd=='b'){
      //Serial.println("b 수신완료");
      myservo.write(180);
      delay(500);
    }
  }
}


###############################


import cv2
import tensorflow.keras
import numpy as np
import time
import serial
import datetime
import matplotlib.pyplot as plt


py_serial = serial.Serial(port='COM3',baudrate=9600)
                         # Window     # 보드레이트 (통신 속도)

def preprocessing(frame):
    # 이미지 뒤집기
    frame_fliped = cv2.flip(frame, 1)
    # 사이즈 조정
    size = (224, 224)
    frame_resized = cv2.resize(frame_fliped, size, interpolation=cv2.INTER_AREA)
    # 이미지 정규화
    frame_normalized = (frame_resized.astype(np.float32) /127.0) -1
    # 이미지 차원 재조정 - 예측을 위해
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    return frame_reshaped

def predict(frame):
    prediction = model.predict(frame)
    return prediction
    
print(cv2.__version__)
# 카메라를 제어할 수 있는 객체
capture = cv2.VideoCapture(0)
# 카메라 길이 너비 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
print("실행완료")
model_filename ='keras_model.h5'
model = tensorflow.keras.models.load_model(model_filename)
sleep_cnt =1

while True:
    try:
        ret, frame = capture.read() # ret : 프레임을 잘 읽었는지 여부 , frame : 받아온 프레임
        frame_fliped = cv2.flip(frame, 1)
        size = (224, 224)
        frame_resized = cv2.resize(frame_fliped, size, interpolation=cv2.INTER_AREA)
        cv2.imshow("VideoFrame",  frame_resized) # 해당 이미지 출력
        # 일정 시간(ms) 기다린 후, 사용자가 아무 키나 눌렀다면 종료
        if cv2.waitKey(1000) >0:
            break

        # 데이터 전처리
        preprocessed = preprocessing(frame)
        # 예측
        prediction = predict(preprocessed)       # 예측된 값은 2차원 배열에 담겨 각각의 확률을 나타냄.
        print("0번 클래스일 확률:", prediction[0, 0], "1번 클래스일 확률:", prediction[0, 1])
    
        if prediction[0, 0] < prediction[0, 1]:  # 클래스 0일 확률과 클래스1일 확률을 비교
            print('1번 Class 감지됨.')
            sleep_cnt +=1
            if sleep_cnt % 5 ==0:
                print('1번 클래스',sleep_cnt,'회 감지됨.')
                sleep_cnt =1
                #아두이노로 각도 변경 코드 전송
                py_serial.write("a".encode())
                #break  ## 1번만 알람이 오면 프로그램을 정지 시킴 (반복을 원한다면, 주석으로 막기!)
        else:
            #아두이노로 각도 변경 코드 전송
            py_serial.write("b".encode())
            print('0번 클래스 감지됨.')
            #sleep_cnt =1                    
    except:
        pass
capture.release() # 카메라 객체 자원 반환
cv2.destroyAllWindows() # 열려있는 모든 창 닫기
