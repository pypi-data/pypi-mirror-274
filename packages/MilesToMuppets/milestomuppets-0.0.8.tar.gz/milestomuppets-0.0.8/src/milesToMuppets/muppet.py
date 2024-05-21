# builtins
import sys
import time

# imports
import requests

# files
from .data import *
from .functions import *

class MilesToMuppets:
    def __init__(self, client_id: str, client_secret: str, output_mode: str= 'null') -> None:
        # set up internal 
        DATA = data
        CONSTANTS = DATA['constants']
        KEY_LIST = DATA['key_list']
        ALBUM_LIST = DATA['songs']
        self.data = DATA
        self.constants = CONSTANTS
        self.key_list = KEY_LIST
        self.album_list = ALBUM_LIST

        # get token, auth_header
        self.TOKEN = get_token(client_id, client_secret)
        self.AUTH_HEADER = get_auth_header(self.TOKEN)

        # set up vals
        self.mph_speed = CONSTANTS['defMphSpeed']
        self.min_per_mile = CONSTANTS['defMinPerMile']

        # print DATA
        if output_mode == 'print':
            print('-----------------------------')
            print("SESSION DATA:")
            print("Token:", self.TOKEN)
            print("Auth header:", self.AUTH_HEADER)
            print('-----------------------------')

    def get_session_data(self) -> dict:
        return {
            'token': self.TOKEN,
            'auth header': self.AUTH_HEADER
        }
    def set_mile_distance(self, distance: float) -> None:
        '''set the distance you intend to travel, in miles'''
        self.mile_distance = distance
        self.minute_distance = self.min_per_mile * self.mile_distance
        self.ms_distance = minuteToMs(self.minute_distance)

    def set_speed(self, speed: float) -> None:
        '''sets the speed at which you are traveling, in mph'''
        self.constants['defMphSpeed'] = speed
        self.constants['defMinPerMile'] = 60 / speed

    def choose_album(self, song_choice: int) -> dict:
        '''chooses a song from the "key_list" dictionary'''
        album_id = self.album_list[self.key_list[song_choice]]
        self.ALBUM_DATA = requests.get(f'https://api.spotify.com/v1/albums/{album_id}', headers=self.AUTH_HEADER).json()
        self.album_name = self.ALBUM_DATA['name']
        self.song_count = self.ALBUM_DATA['total_tracks']
        self.tracks = self.ALBUM_DATA['tracks']['items']
        return {
            "album name": self.album_name,
            "total songs": self.song_count
        }
    
    def evaluate_album(self, print_cycle: bool = True) -> dict:
        '''evaluates the album'''
        total_ms = 0
        song_amount = 0
        found_max = False
        leng = "                                                                                      "
        if print_cycle:
            print('-----------------------------\n')
        for track in self.tracks:
            name = track['name']
            duration_ms = track['duration_ms']
            if print_cycle:
                sys.stdout.write("\033[F")
                sys.stdout.write(f"{leng}\n{leng}")
                sys.stdout.write("\033[F")
                sys.stdout.write(f"\rsong name: {name}\nduration: {duration_ms}ms")
                sys.stdout.flush()
                time.sleep(0.15)

            if total_ms >= self.ms_distance:
                found_max = True
                break
            else:
                total_ms += duration_ms
                song_amount += 1
            
        ms_leftover = self.ms_distance - total_ms
        minute_leftover = round(msToMinute(ms_leftover), 2)
        if print_cycle:
            print(" ")
            print('-----------------------------')
        return {
            'finished album': found_max,
            'average speed': self.mph_speed,
            'minute(s) per mile': self.min_per_mile,
            'songs listened': song_amount,
            'mile distance': self.mile_distance,
            'minute distance': self.minute_distance,
            'ms distance': self.ms_distance
        }