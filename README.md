# Opencv_drone
*This repository is for small Python programs. The programs are written using the Opencv library. Software Profiling - Autonomous Drones with RPi*

# Brief summary of each program (краткая аннотация программ в репозитории):
1. **RecognizeColour.py:** 

Program for recognition of colored objects on the surface. It is necessary to modify the program to recognize not only colors, but also shapes. For example, along the contour.

(Программа для распознавания цветных объектов на поверхности. Необходимо модифицировать программу для распознавания не только цвета, но и формы. Например, по контуру).

2. **DronePlatforma.py:**

A program for recognizing a moving Aruco-tag, which is located on a vacuum cleaner. The quadcopter takes off, scans the area, detects the vacuum cleaner, then makes a gradual landing.
You need to modify the code so that it detects the vacuum cleaner by contour or by color 

(программа для распознавания движущейся Aruco-метки, которая находится на пылесосе. Квадрокоптер взлетает, сканирует территорию, обнаруживает пылесос, затем производит постепенную посадку.
Необходимо модифицировать код, чтобы он обнаруживал пылесос по контуру или по цвету).

3. **CountCoin.py:**

A program for counting the number of objects (coins) from a photo test.jpg. Check the path to the photo. My program assumes that the photo is in the same directory as the script program itself.

(Программа по подсчету количества объектов (монет) по фотографии test.jpg. Проверьте путь до фотографии. У меня в программе предполагается, что фото находится в той же директории, 
что и сам скриптпрограммы).

4. **CountHSV.py:**

A program for recognizing the number of objects from a quadrocopter. Before starting, you need to set the minimum and maximum borders by HSV color: hsv_min, hsv_max. To configure these settings, use the PreferenceHSV.py program.

(Программа по распознаванию количества объектов с квадрокоптера. Перед запуском необходимо настроить минимальное и максимальные границы по цвету HSV: hsv_min, hsv_max. Для натройки этих параметров используйте программу PreferenceHSV.py).

5. **PreferenceHSV.py:**

Program for setting the minimum and maximum border values by HSV color: hsv_min, hsv_max. To do this, you need to take a photo (screenshot) of those objects that need to be recognized. Insert a link to the path to this photo in the code. Run and adjust the sliders until the subject in the photo is white. Write hsv_min, hsv_max values to CountHSV.py program.

(Программа для настройки минимального и максимальнго значений границы по цвету HSV: hsv_min, hsv_max. Для этого необходимо сделать фото (скриншот) тех объектов ,которые необходимо будет распознавать. Ссылку на путь до этой фотографии вставьте в код. Запускайте и регулируйте ползунки до тех пор, пока объект на фото не станет белым. Запишите значения hsv_min, hsv_max в программу CountHSV.py).

6. **CountRect.py:**

A program for recognizing the number of objects from a quadrocopter. A different method is used to recognize

(Программа по распознаванию количества объектов с квадрокоптера. Используется иной способ по распознаванию).