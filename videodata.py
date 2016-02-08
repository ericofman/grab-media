from urllib.parse import urlparse 
from urllib.parse import parse_qs 
from urllib.request import urlopen 
import sys

class VideoData:
    def __init__(self, video_url):
        self._video_url = video_url
        
        url_base = 'https://www.youtube.com'
        request_url = url_base + '/get_video_info?video_id'
        watch_url =  url_base + '/watch?v'
        
        if('https://' not in self._video_url):
            self._video_url = 'https://' + self._video_url
         
        parse = parse_qs(self._video_url)  
        
        if(request_url in parse.keys()):
            request_url = request_url + '=' + parse[request_url][0]
        elif(watch_url in parse.keys()):
            request_url = request_url + '=' +parse[watch_url][0]
        else:
            sys.exit("Invalid or unsupported YouTube URL: %s" % self._video_url)
        
        request = urlopen(request_url) 
        self._video_info = request.read()
        
vinfo = VideoData('https://www.youtube.com/get_video_info?video_id=oThh3_Srxtc')
