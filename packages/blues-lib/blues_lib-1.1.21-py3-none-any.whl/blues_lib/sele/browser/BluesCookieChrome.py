
import sys,os,re,time
from .BluesChrome import BluesChrome

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesFiler import BluesFiler  
from util.BluesURL import BluesURL   
from config.BluesConfig import BluesConfig    

class BluesCookieChrome(BluesChrome):

  def __init__(self,config={},arguments={},experimental_options={}):
    super().__init__(config,arguments,experimental_options)

  '''
  @description : support to login by default cookie
  '''
  def get_with_cookie(self,url,cookies=''):
    '''
    @description : get a page afater add cookies
    @param {dict|str} cookies
    '''
    if cookies:
      self.action.cookie.add_cookies(cookies) 
    self.driver.get(url)

  def get_with_cookie_file(self,url,file=''):
    default_file = BluesConfig.get_download_http_domain_file(self.driver.current_url,'txt')
    file_path = file if file else default_file
    if file_path:
      cookies = BluesFiler.read(file_path)
    else:
      cookies = ''
    self.get_with_cookie(url,cookies)
