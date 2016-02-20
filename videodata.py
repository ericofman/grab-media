from urllib.parse import urlparse 
from urllib.parse import parse_qs 
from urllib.parse import urlencode 
from urllib.request import urlopen 
from urllib.request import urlretrieve
import sys

class VideoData:
    fmt_types = {
            5:  "FLV,320x240",         13: "3GP,176x144", 
            17: "3GP,176x144",         18: "MP4,480x360", 
            22: "MP4,1280x720",        34: "FLV,480x360",
            35: "FLV,640x480",         36: "3GP,320x240", 
            37: "MP4,1920x1080",       38: "MP4,2048x1080", 
            44: "WEBM,640x480",        46: "WEBM,1920x1080",
            59: "MP4,640x480",         78: "MP4,640x480", 
            82: "MP4,480x360,3",       17: "3GP,176x144", 
            18: "MP4,480x360",         22: "MP4,1280x720",
            34: "FLV,480x360",         35: "FLV,640x480", 
            36: "3GP,320x240",         37: "MP4,1920x1080", 
            38: "MP4,2048x1080",       43: "WEBM,480x360",
            44: "WEBM,640x480",        45: "WEBM,1280x720", 
            46: "WEBM,1920x1080",      59: "MP4,640x480", 
            78: "MP4,640x480",         82: "MP4,480x360,3",
            83: "MP4,640x480,3",       84: "MP4,1280x720,3", 
            85: "MP4,1920x1080,3",     100: "WEBM,480x360,3", 
            101: "WEBM,640x480,3",     102: "WEBM,1280x720,3",
           133: "MP4,320x240,V",       134: "MP4,480x360,V", 
           135: "MP4,640x480,V",       136: "MP4,1280x720,V", 
           137: "MP4,1920x1080,V",     139: "MP4,Low bitrate,A", 
           140: "MP4,Med bitrate,A",   141: "MP4,Hi  bitrate,A",
           160: "MP4,256x144,V",       171: "WEBM,Med bitrate,A", 
           172: "WEBM,Hi  bitrate,A",  242: "WEBM,320x240,VO",
           243: "WEBM,480x360,VO",     244: "WEBM,640x480,VO", 
           245: "WEBM,640x480,VO",     246: "WEBM,640x480,VO",
           247: "WEBM,1280x720,VO",    248: "WEBM,1920x1080,VO",
           249: "WEBM,Low bitrate,AO", 250: "WEBM,Med bitrate,AO",
           251: "WEBM,High bitrate,AO",264: "MP4,2560x1440,V",
           266: "MP4,3840x2160,V",     271: "WEBM,2560x1440,VO",
           272: "WEBM,3840x2160,VO",   278: "WEBM,256x144,VO",
           298: "MP4,1280x720,V",      302: "WEBM,1280x720,VO",
           313: "WEBM,3840x2160,VO",
    }    
    
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
        fmt_stream_map = self._video_info['url_encoded_fmt_stream_map'][0] \
            .decode('utf-8').split(',')
        # parse again because youtube encodes twice
        entries = [parse_qs(entry) for entry in fmt_stream_map]  
        for i in range(len(entries)): 
            streams[((entries[i])['itag'][0])] = ((entries[i])['url'][0])
        return streams
    
    def _available_itags(self, streams):
        return [int(value) for value in list(streams.keys())]
    
    def get_available_streams(self, streams):
        itags = self._available_itags(streams) 
        for itag in itags:
            print("{0}: {1}".format(itag, self.fmt_types[itag])) 
    
    def download_stream(self, streams, itag, filename):
        if not streams:
            sys.exit("No streams available for this video")
        
        if itag not in self._available_itags(streams):
            sys.exit("itag not found") 
         
        request = urlopen(streams[str(itag)])  
        meta = request.info() 
        file_size = int(meta.get_all("Content-Length")[0])      

        file = open(filename + '.' + 
                    self.fmt_types[itag].split(',')[0].lower(), "wb") 
        blocksize = 8192
        file_dl_size = 0               
        while True:
            chunk = request.read(blocksize)
            if not chunk: break
            file.write(chunk)
            file_dl_size += len(chunk)  
            print("Downloading: {0}/{1} Bytes".format(file_dl_size, file_size))
        file.close() 
        
        if(file_dl_size == file_size):
            print("Video successfully downloaded.")
        else:
            sys.exit("Video failed to properly download.")
        
if __name__ == '__main__':
    vinfo = VideoData('https://www.youtube.com/watch?v=GQQMLE4FuIQ')
    print(vinfo.get_title())
    print(vinfo.get_thumbnail_url('hq'))
    streams = vinfo.get_streams()  
    vinfo.get_available_streams(streams)
    vinfo.download_stream(streams, 22, "video_test")