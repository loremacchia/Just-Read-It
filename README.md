# Eyes For Blind
## To read the unreadable 
We know that technology is increasing its support to our society day by day. This project is thought to be a part of this innovation process by providing a support to *blind people in going grocery shopping*.

### Recognize text in supermarket items
The task is to help blind people to read what they can not. Often supermarket items don't have a braille translation of their name and descriptions. We provide an app that can spot text in images, transcript it and read it with the phone's text-to-speech.

######## Todo put demo gif









[![Luz Vision | Web RTC](https://img.youtube.com/vi/JLI_p2d0C-s/maxresdefault.jpg)](https://youtu.be/JLI_p2d0C-s)
[Watch the DEMO](https://youtu.be/JLI_p2d0C-s)


##### Option 2: Using hardware (Rasberry Pi + AI) ([DEMO](https://youtu.be/H8Pw1uwH2YU))


[![Luz Vision | Web RTC](https://img.youtube.com/vi/H8Pw1uwH2YU/maxresdefault.jpg)](https://youtu.be/H8Pw1uwH2YU)
[Watch the DEMO](https://youtu.be/H8Pw1uwH2YU)


##### Option 3: (work in progress): Using embedded hardwares + AI


![alt text](resources/part3.jpg)


=============================================
##### Deploy (Using Docker Compose)
`cd docker`

`docker-compose up -d`

##### Deploy (Native)
`cd docker`

`pip install -r requirements.txt `

`cd ../scripts`

`python web-server.py`

Visit http://localhost:5002.

##### THIS IS WORK IN PROGRESS.

#### TO DO
- Integrate OCR to read text from camera. 
- More accuracte object level detection using custom training.
- .... huge list.

##### My other work related to AI [Content-AI](https://github.com/nycdidar/Content-AI)


> FULL CREDIT GOES TO EVERYONE INVOLVED IN ML/AI FIELD. WE WOULD BE IN STONE AGE WITHOUT THEIR DEDICATION AND HARD WORK.
