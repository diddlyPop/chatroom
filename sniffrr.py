"""
facecrook.py
Kyle Guss & Jesse Mazzella

proof of concept
packet sniffing for pictures
"""

from scapy.all import *
import zlib
import scipy
import numpy
import os
import re
import cv2


class Sniffrr():

    def __init__(self, seconds=15):
        self.images_found = 0
        self.faces_found = 0
        self.sniff_time = seconds
        self.packets = None
        self.sniff_log = []
        self.credentials = []
        # pic output path
        self.directory = f"{os.environ['USERPROFILE']}/Desktop/SniffOutput"

    def __str__(self):
        return f"Images: {self.images_found}, Seconds: {self.sniff_time}, Credentials: {self.credentials}, Faces: {self.faces_found}"

    def AddSniff(self):
        '''
        adds 'sniff_time'
        uses sniff time queue helps prevent extra sniffing
        '''
        self.sniff_time += 15

    def TakeSniff(self):
        '''
        checks if 'sniff_time' > 0
        sniffs on default interface
        sets 'sniff_time' to 0
        '''
        if self.sniff_time == 0:
            if self.packets is None:
                print("No sniff time queued. No Packets stored yet.")
            else:
                print("No sniff time queued. Packets already stored though.")
        else:
            self.packets = sniff(timeout=self.sniff_time)
            self.sniff_time = 0

    def CheckSniff(self):
        '''
        loads packets from 'self.packets'
        appends byte payloads from each packet to 'http_payload'
        checks 'http_payload' for http headers
        if 'headers' are found, attempts to pull out images from 'http_payload'
        if 'image' found, store the image
        '''
        try:
            sessions = self.packets.sessions()
        except Exception as e:
            print(e)

        for session in sessions:
            http_payload = b''
            for packet in sessions[session]:
                try:
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80 or packet[TCP].dport == 43 or packet[TCP].sport == 43:
                        http_payload += bytes(packet[TCP].payload)
                except:
                    pass
                headers = self.__get_http_headers(http_payload)
                if headers is None:
                    continue
                user, password = self.__extract_creds(headers, http_payload)
                if user is not None and password is not None:
                    pass
                image, image_type = self.__extract_image(headers, http_payload)
                if image is not None and image_type is not None:
                    if self.images_found % 10 == 0:
                        file_name = '{0}-pic-{1}.{2}'.format(
                            "packets", self.images_found, image_type)
                        file = open('%s/%s' % (self.directory, file_name), 'wb')
                        file.write(image)
                        file.close()
                    self.images_found += 1
                    try:
                        result = self.__face_detect(file_name)

                        if result is True:
                            self.faces_found += 1
                    except Exception as e:
                        print(e)

    def ClassifySniff(self):
        '''
        instructs classifier to analyze 'self.directory'
        takes image classifications and appends them to 'self.sniff_log'
        '''
        filelist = [file for file in os.listdir(self.directory) if file.endswith('.png')]
        for image in filelist:
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt.xml")
            faces = face_cascade.detectMultiScale(image_gray)
            for x, y, width, height in faces:
                cv2.rectangle(image, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
                # save the image with rectangles
            file_name = '{0}-pic-{1}.{2}'.format("faces", self.faces_found, "jpg")
            cv2.imwrite(file_name, image)
            self.faces_found += 1

    def __get_http_headers(self, payload_bytes):
        '''
        finds and puts http headers into dictionary
        :param payload_bytes: bytes
        :return: dictionary of headers
        '''
        try:
            headers_bytes_raw = payload_bytes[payload_bytes.index(
                b"HTTP/1.1"):payload_bytes.index(b"\r\n\r\n") + 2]
            headers_bytes_parsed = dict(
                re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers_bytes_raw.decode("utf8")))
        except Exception as e:
            return None
        if 'Content-Type' not in headers_bytes_parsed.keys():
            return None
        return headers_bytes_parsed

    def __extract_image(self, headers, payload_bytes):
        '''
        :param headers: dictionary of headers
        :param payload_bytes: corresponding bytes for these headers
        :return: tuple of image and the image type
        '''
        image = None
        image_type = None
        try:
            if 'image' in headers['Content-Type']:
                image_type = headers['Content-Type'].split('/')[1]
                image = payload_bytes[payload_bytes.index(b"\r\n\r\n") + 4:]
                try:
                    if 'Content-Encoding' in headers.keys():
                        if headers['Content-Encoding'] == 'gzip':
                            image = zlib.decompress(image, 16 + zlib.MAX_WBITS)
                        elif headers['Content-Encoding'] == 'deflate':
                            image = zlib.decompress(image)
                except:
                    pass
        except:
            pass
            return None, None
        return image, image_type

    def __extract_creds(self, headers, payload_bytes):
        user = None
        password = None
        return user, password

    def __face_detect(self, file_name):
        print("Attempted face detect")
        img = cv2.imread("{}/{}".format(self.directory, file_name))
        cascade = cv2.CascadeClassifier("C:\\Users\\kyleg\\Desktop\\facecrook\\cascades\\haarcascade_frontalface_default.xml")
        rects = cascade.detectMultiScale(img, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, (20, 20))

        if len(rects) == 0:
            return False

        print("True")
        rects[:, 2:] += rects[:, :2]

        # highlight the faces in the image
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)

        cv2.imwrite("{}/{}-{}".format(self.directory, "faces", file_name), img)

        return True


if __name__ == "__main__":
    S = Sniffrr()
    S.TakeSniff()
    S.CheckSniff()
    S.ClassifySniff()
    print(S)
