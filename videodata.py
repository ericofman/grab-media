from urllib.parse import urlparse 
from urllib.parse import parse_qs 
from urllib.parse import urlencode 
from urllib.request import urlopen 
import sys

class VideoData:
    def __init__(self, video_url):
        self._video_url = video_url
        
        url_base = 'https://www.youtube.com'
        request_url = url_base + '/get_video_info?video_id'
        watch_url =  url_base + '/watch?v'
        vevo_postfix = '&el=vevo&el=embedded'
        
        if('https://' not in self._video_url):
            self._video_url = 'https://' + self._video_url
         
        parse = parse_qs(self._video_url)  
        
        if(request_url in parse.keys()):
            request_url = request_url + '=' + parse[request_url][0]
        elif(watch_url in parse.keys()):
            request_url = request_url + '=' + parse[watch_url][0]
        else:
            sys.exit("Invalid or unsupported YouTube URL: %s" % self._video_url)
        
        request = urlopen(request_url) 
        self._video_info = parse_qs(request.read())
        
        for key in self._video_info.keys():
            self._video_info[key.decode('utf-8')] = self._video_info.pop(key) 
    
    def get_title(self): 
        return self._video_info['title'][0].decode('utf-8')
    
    def get_thumbnail_url(self, quality):
        ''' 
        Thumbnail quality: default, hq, mq, sd, max
        '''
        thumbnail = self._video_info['thumbnail_url'][0].decode('utf-8') \
            .split('/')
        if(quality == "default"):
            thumbnail[-1] = thumbnail[-1]
        elif(quality in ['hq', 'mq', 'sd', 'max']):
            thumbnail[-1] = quality + thumbnail[-1]
        else:
            sys.exit("Invalid thumbnail quality prefix: %s" % quality)
        thumbnail = '/'.join(thumbnail)
        return thumbnail
    
    def get_streams(self):
        streams = {}
        fmt_stream_map = self._video_info['url_encoded_fmt_stream_map'][0].decode('utf-8').split(',')
        # parse again because youtube encodes twice
        entries = [parse_qs(entry) for entry in fmt_stream_map]  
        for i in range(len(entries)): 
            streams[((entries[i])['url'][0])] = ((entries[i])['itag'][0])
        return streams
        
if __name__ == '__main__':
    vinfo = VideoData('https://www.youtube.com/watch?v=ObiqJzfyACM')
    print(vinfo.get_title())
    print(vinfo.get_thumbnail_url('hq'))
    print(vinfo.get_streams()) 