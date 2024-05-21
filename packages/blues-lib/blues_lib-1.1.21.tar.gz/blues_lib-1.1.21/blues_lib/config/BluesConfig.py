import sys,os,re

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesURL import BluesURL   

class BluesConfig():

  DOWNLOAD_ROOT = 'c:/blues_lib/download/'  
  DOWNLOAD_MODULES = {
    'http':'http',
  }

  @classmethod
  def get_download_dir(cls,module=''):

    module_dir = cls.DOWNLOAD_MODULES.get(module) 
    if module_dir:
      return '%s%s/' % (cls.DOWNLOAD_ROOT,module_dir)
      
    return cls.DOWNLOAD_ROOT

  @classmethod
  def get_download_file(cls,module,filename):
    return '%s%s' % (cls.get_download_dir(module),filename)

  @classmethod
  def get_download_http_file(cls,filename):
    return cls.get_download_file('http',filename)
  
  @classmethod
  def get_download_http_domain_file(cls,url,extension='txt'):
    domain = BluesURL.get_main_domain(url)
    filename = '%s.%s' % (domain,extension)
    return cls.get_download_http_file(filename)