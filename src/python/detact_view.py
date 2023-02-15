import cv2
import mediapipe as mp
from collections import deque
import sys

# 움직이는지 판단 기준
criteria = 0.75 # 이전 프레임과 차이
criteria_frame = 21 # 판단을 위한 이전 프레임
criteria_count = 12 # criteria_frame 에서 criteria_count개 보다 많은 'O' 요구 

# 행동 분리 기준
x_count = 8 # 중간에 x 값이 몇개까지 있어도 되는가
scean_count = 45 # 안움직이는 프레임이 몇개 지속되야 행동인가

# 테스트 영상
video_name='testclip6'
video_file='C:/Users/cksdn/Desktop/vue-project/src/python/testclip6.mp4'

# 메모장에 결과값 기록하기
memo = False

def decide(x, y, z, i):
    b_x = before_x.popleft()
    b_y = before_y.popleft()

    gap_x = round(b_x / x, 4)
    gap_y = round(b_y / y, 4)
 
    if(gap_x >= 1) : gap_x = round((gap_x - 1) * 100, 4)
    else : gap_x = round((1 - gap_x) * 100, 4)
    if(gap_y >= 1) : gap_y = round((gap_y - 1) * 100, 4)
    else : gap_y = round((1 - gap_y) * 100, 4)

    gap_z = round(z, 4)

# 이전 프레임보다 (criteria)% 차이가 난다면 움직이는 것으로 판정
    if gap_x > criteria - gap_z :
        return False
    elif gap_y > criteria - gap_z :
        return False
    else : 
        return True

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(video_file)

now_frame = 0
first_flag = True

before_x = deque()
before_y = deque()

# 움직이는지 판단하는 것에 이전 (criteria_frame) 프레임을 이용
result_s = deque()
for _ in range(criteria_frame) : 
    result_s.append(1)

result_list = []

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose :
    while cap.isOpened() :
        success, image = cap.read()
        if not success :
            break

        image.flags.writeable = False
        results = pose.process(image)

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        no_move = True
        if results.pose_landmarks :
            for i in range(33) :
                before_x.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x)
                before_y.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y)
                if first_flag :
                    if i == 32 : first_flag = False
                    continue
                if no_move :
                    if results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].visibility > 0.7 :
                        no_move = decide(results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x, results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y, results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].z, i)
                    else :
                        before_x.popleft()
                        before_y.popleft()
                else :
                    before_x.popleft()
                    before_y.popleft()
        
        if no_move :
            result_s.popleft()
            result_s.append(1)
        else :
            result_s.popleft()
            result_s.append(0)
        
        if sum(result_s) > criteria_count : # 최종 판단
            result = 'O'
        else :
            result = 'X'

        result_list.append(result)

        cv2.putText(image, str(now_frame), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        cv2.putText(image, str(result), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(3) & 0xFF == 27:
            break
        now_frame = now_frame + 1
 
cap.release()

before = result_list[0]
scean = []
scean_result = []
start = 0
for i in range(1, len(result_list)) :
    if(result_list[i]) == 'O' :
        if before == 'X' :
            start = i
    else :
        if before == 'O' :
            end = i-1
            scean.append([start, end])
    before = result_list[i]

if result_list[-1] == 'O' and before == 'O' :
    end = len(result_list)-1
    scean.append([start, end])

for j in range(len(scean)-1) :
    if(scean[j+1][0] - scean[j][1]) < x_count :
        scean[j+1][0] = scean[j][0]
        scean[j][0] = -1

for k in range(len(scean)) :
    if scean[k][0] != -1 and scean[k][1] - scean[k][0] > scean_count :
        scean_result.append(scean[k])

if memo :
    sys.stdout = open(video_name+'.txt', 'w')

for l in range(len(scean_result)) :
    if memo :
        print(f'{l}:{scean_result[l][0]}:{scean_result[l][1]}')
    else :
        print(f'{l}:{scean_result[l][0]}:{scean_result[l][1]}')

if memo :
    sys.stdout.close()