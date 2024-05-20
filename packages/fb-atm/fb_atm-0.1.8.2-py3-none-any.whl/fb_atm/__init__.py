
import re,requests
from mahdix import *
import urllib.parse
from bs4 import BeautifulSoup as bs
clear()
class Page:
    def __init__(self):
            self.headers_web = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,vi;q=0.8,bn;q=0.7','cache-control': 'max-age=0','dnt': '1','dpr': '1','priority': 'u=0, i','referer': 'https://www.facebook.com/',
            'sec-ch-prefers-color-scheme': 'dark','sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"','sec-ch-ua-full-version-list': '"Chromium";v="124.0.6367.119", "Google Chrome";v="124.0.6367.119", "Not-A.Brand";v="99.0.0.0"','sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1','upgrade-insecure-requests': '1','viewport-width': '475',
            'user-agent': W_ueragnt(),}
    def fromate_cookes(self,cookes):
            r"""
                Format cookie data into a consistent format.

                Args:
                    cookies (str or set): The input cookies to format.

                Returns:
                    dict: A dictionary containing the formatted cookies.
                """
            try:  
                if isinstance(cookes, set):
                        return cookies
                elif isinstance(cookes, str):
                    cookies = dict(urllib.parse.parse_qsl(cookes, keep_blank_values=True))
                    return cookies
            except Exception as e:
                  print('parsing error',e)
    def get_page_ID(self,cookes):
            try:
                r"""
                Generate page cookies based on input cookies.
                Args:
                    cookies (str): Input cookies.

                Returns:
                    list: A list of generated page page uid as a integer.


                inputing ID cookes you can generate get all uid
                this function returning 22 fast page uid wich are admin or show on your ids..
                from https://www.facebook.com/pages/ url get all uid
                """
                cookies=self.fromate_cookes(cookes)
                params = {
                        'category': 'your_pages',
                        'ref': 'bookmarks',}
                self.html =requests.get('https://www.facebook.com/pages/',headers=self.headers_web,cookies=cookies,params=params).text
                self.page_uid=re.findall(r'"__typename":"User","id":"(\d+)"',self.html)
                return self.page_uid
            except Exception as e:
                  print('cookes error',e)
    def generate_page_cooeks(self,cooeks):
        try:

            r"""
                Generate page cookies based on input cookies.
                Args:
                    cookies (str): Input cookies.

                Returns:
                    list: A list of generated page cookies as a string.

                inputing ID cookes you can generate page cookes
                this function returning 22 fast page Cookes wich are admin or show on your ids..
                from https://www.facebook.com/pages/ url get all page cookes
            """
            self.all_page_cookes=[]
            self.geting_page_uid=self.get_page_ID(cooeks)
            for uid in  set(self.geting_page_uid):
                try:
                    invcng=f"m_page_voice={cooeks.split('m_page_voice=')[1].split(';')[0]}"
                    page_inv=f'm_page_voice={uid}'
                    cokix=str(cooeks).replace(invcng,page_inv)
                except:cokix=cooeks.replace(' ','')+f'm_page_voice={uid}'
                page_coki='i_user='+uid+';'+cokix
                result_string = ';'.join(random.sample(page_coki.split(';'), len(page_coki.split(';')))).replace(';;',';')
                self.all_page_cookes.append(result_string)
                
            return self.all_page_cookes  # Proper indentation for return statement
            
        except Exception as e:print(e)
    
    def GPR_Data(self,url='https://www.facebook.com/bk4human',headers=None, cookies=None):
        r"""
            Generate post request data from a Facebook URL using cookies.
            Args:
                url (str): The URL to fetch data from. Default is 'https://www.facebook.com/bk4human'.
                cookies (dict): Optional. A dictionary containing cookies to be used in the request. Default is None.
            Returns:
                fb_dtsg , jazoest ,lsd and Profile_ID
                this for send post request
            """
        try:
            
            if headers is None:
                headers = self.headers_web
            cookie=self.fromate_cookes(cookies)
            data_responce=requests.get(url,headers=headers,cookies=cookie).text
            if 'm.facebook' in url:
                uidx = re.search('actorId:"(.*?)"', str(data_responce)).group(1)
                try:
                    fb_dtsg=re.search('type="hidden" name="fb_dtsg" value="(.*?)"',str(data_responce)).group(1)
                except:
                    fb_dtsg=re.search('{"dtsg":{"token":"(.*?)"',str(data_responce)).group(1)
                try:
                    jazoest=re.search('type="hidden" name="jazoest" value="(.*?)"',str(data_responce)).group(1)
                except:
                    try:
                        jazoest=re.search('"jazoest", "(.*?)"',str(data_responce)).group(1)
                    except:jazoest=''
                lsd=re.search('"LSD",\[\],{"token":"(.*?)"}',str(data_responce)).group(1)
            elif  'www.facebook' in url:
                uidx = re.search('__user=(.*?)&', str(data_responce)).group(1)
                fb_dtsg = re.search('"DTSGInitialData",\[\],{"token":"(.*?)"', str(data_responce)).group(1)
                jazoest = re.search('&jazoest=(.*?)",', str(data_responce)).group(1)
                lsd = re.search('"LSD",\[\],{"token":"(.*?)"', str(data_responce)).group(1)
                
            return {
                "fb_dtsg":fb_dtsg,
                "jazoest":jazoest,
                "lsd":lsd,
                "Profile_ID":uidx
            }
        except Exception as e:print(e)
