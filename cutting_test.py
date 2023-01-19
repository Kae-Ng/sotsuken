import cv2
import json
import csv
import os
 
#cascade=cv2.CascadeClassifier("haarcascade_fullbody.xml")
 
json_file = open('logeye_20230103_163035.json', 'r')
json_dict = json.load(json_file)


    


mv= cv2.VideoCapture('senmou1_final_20201030.mp4')#動画の読み込み





size=(5760,2880)
#get fps
fps = mv.get(cv2.CAP_PROP_FPS)
#for calculating seconds
fps_inv = 1 / fps

frame_count =int(mv.get(cv2.CAP_PROP_FRAME_COUNT))#動画を画像にした総枚数を調べる
print("frame_count ", frame_count)





#create save file path and name
os.makedirs('data/temp/result_range_mv', exist_ok=True)
#base_path = os.path.join('data/temp/result_range_sec', 'sample_video_img')
base_path = os.path.join('data/temp/result_range_sec_mv', 'sample_video')



#総フレーム数の桁数(for export frame's name)
#digit = len(str(frame_count))


# Define the codec and create VideoWriter object
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output1.avi',fourcc, fps, size)
#out = cv2.VideoWriter('output.avi',-1, 20.0, (640,480))

#fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
#out = cv2.VideoWriter('{}_{}_{}.{}'.format(base_path, "278", '327', 'mp4'), fourcc, fps, size)







#薬シーン
start_fr=round(278*fps)
stop_fr=round(327*fps)



with open('sample1.csv', 'w') as f:
    #extracting frame
    fr = start_fr

    while fr < stop_fr:
#        n = round(fps * sec)
#        print("hit  !!!")
        #set starting point (frame no.)
        mv.set(cv2.CAP_PROP_POS_FRAMES, fr)
        ret, frame = mv.read()
        if ret:
            frame=cv2.resize(frame,size)

            #contours_data = [2200, 1920, 2760, 2250]
            #2200, 1920), (2760, 2250
            contours_x_data = 2200
            contours_xw_data = 2760
            contours_y_data = 1920
            contours_yh_data = 2250
            
        
            eye_x_data = json_dict["trackingDataList"][fr]["x"]
            eye_y_data = json_dict["trackingDataList"][fr]["y"]
            eye_z_data = json_dict["trackingDataList"][fr]["z"]

            cv2.rectangle(frame, (contours_x_data, contours_y_data), (contours_xw_data, contours_yh_data), (0,0,255), 3)#赤い四角で囲む
            if eye_z_data == 1.0:
                cv2.circle(frame, (int(eye_x_data), int(eye_y_data)), 20, color=(0, 255, 0), thickness=-1)

            if contours_x_data <= eye_x_data and eye_x_data <= contours_xw_data and contours_y_data <= eye_y_data and eye_y_data <= contours_yh_data and eye_x_data != 0.0 :
                print("eye_x",eye_x_data)
                print("eye_y",eye_y_data)
                print("TRUE",fr * fps_inv) #hitの時刻（秒）
                
                writer = csv.writer(f)
                writer.writerow([fr * fps_inv])
        


            # write the frame
            out.write(frame)


#            if fr == stop_fr-1 or fr == start_fr:
#                cv2.imwrite(
#                    '{}_{}_{:.2f}.{}'.format(
#                        base_path, str(fr).zfill(digit), fr * fps_inv, 'jpg'
#                    ),
#                    frame
#                )

        else:
            break
        fr += 1
        cv2.imshow('movie', cv2.resize(frame, dsize=None, fx=0.25, fy=0.25))

    
        k=cv2.waitKey(1)#1ミリ秒wait
        if k==27:#ESCキーを押したとき
            break
    

    mv.release()
    out.release()
    cv2.destroyAllWindows()