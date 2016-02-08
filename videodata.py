from urllib.parse import urlparse 
from urllib.parse import parse_qs 
from urllib.request import urlopen 
import sys

class VideoData:
    def __init__(self, video_url):
        self._video_url = video_url
        
        url_base = 'https://www.youtube.com'
        request_url = url_base + '/get_video_info?video_id'
        vevo_post_fix = '&el=vevo&el=embedded'
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
        self._video_info = parse_qs(request.read())
        
        if(self.is_vevo()):
            request_url += vevo_post_fix
            request = urlopen(request_url) 
            self._video_info = parse_qs(request.read())            
            
    def is_vevo(self):
        reason = self._video_info[b'reason'][0].decode('utf-8')
        if('VEVO' in reason):
            return True
        else:
            return False
    
    def get_title(self): 
        return self._video_info[b'title'][0].decode('utf-8')
    
    def get_thumbnail_url(self, hq):
        thumbnail = self._video_info[b'thumbnail_url'][0].decode('utf-8') \
            .split('/')
        if(hq):
            thumbnail[-1] = 'hq' + thumbnail[-1]
            thumbnail = '/'.join(thumbnail)
        return thumbnail

if __name__ == '__main__':
    vinfo = VideoData('https://www.youtube.com/watch?v=EgqUJOudrcM')
    print(vinfo.get_title())
    print(vinfo.get_thumbnail_url(True))