import requests
import os

request_headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
                   'Range': 'bytes=0-'}

def download_file(url):
    #TODO: Check it the file to download already exist. If yes rename the actual downloaded 
    #      file to avoid overide because of the file resume.

    retry = 0
    max_retry = 3
    chunk_size = 0

    local_filename = url.split('/')[-1]
    if os.path.isfile(local_filename):
        os.remove(local_filename)
        
    while retry < max_retry:
        try:
            r = requests.get(url, verify=False, stream=True, headers=request_headers)
            r.raise_for_status()
            file_size = int(r.headers.get('content-length'))
            with open(local_filename, 'ab') as f:
                for chunk in r.iter_content(chunk_size=102400): 
                    print(f'Downloading: {chunk_size} bytes of {file_size} bytes. {file_size - chunk_size} missing.')
                    chunk_size = chunk_size + len(chunk)
                    f.write(chunk)
        except requests.exceptions.ChunkedEncodingError as e:
            print(f'Download Error: {e}')
            request_headers['Range'] = f'bytes={chunk_size}-'
            retry = retry + 1

    return local_filename

#Main
url = 'https://www.archimatetool.com/downloads/archi5.php?/5.1.0/Archi-Win64-5.1.0.zip'
print(download_file(url))