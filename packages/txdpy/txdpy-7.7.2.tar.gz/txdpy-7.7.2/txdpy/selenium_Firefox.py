from selenium.webdriver import Firefox
from selenium import webdriver
from PIL import Image
from io import BytesIO
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.service import Service

class selenium_firefox:
    def __init__(self,default_image=True):
        # 禁止一些东西加载提升速度可能也能解决一些爬去过程中的bug和反爬吧！
        fp = webdriver.FirefoxOptions()
        # 忽略证书错误
        fp.accept_untrusted_certs = True
        fp.assume_untrusted_cert_issuer = False
        if default_image:
            fp.set_preference("permissions.default.image", 2)
        fp.set_preference("thatoneguydotnet.QuickJava.curVersion", "2.0.6.1")
        fp.set_preference("thatoneguydotnet.QuickJava.startupStatus.Images", 2)
        fp.set_preference("thatoneguydotnet.QuickJava.startupStatus.AnimatedImage", 2)
        fp.set_preference("browser.cache.disk.enable", False)
        fp.set_preference("browser.cache.memory.enable", False)
        fp.set_preference("browser.cache.offline.enable", False)
        fp.set_preference("network.http.use-cache", False)
        service = Service(executable_path=r'C:\Users\86186\Desktop\pythonpro\爬虫项目\各学校专业分更新监控和采集\geckodriver.exe')
        self.driver = Firefox(service=service, options=fp)
        self.ocr_code=None

    def iivc(self,code_element):
        """
        :param code_element:验证码元素 driver.find_elements(By.ID,'img_code'):
        :return 验证码
        """
        # 截取验证码图片并读取为图像对象
        captcha_image = Image.open(BytesIO(code_element.screenshot_as_png))
        if not self.ocr_code:
            import ddddocr
            self.ocr_code = ddddocr.DdddOcr(show_ad=False)  # 实例化对象
        code = self.ocr_code.classification(captcha_image)  # 识别图片上的字符
        return code

    def select(self,select_element):
        return Select(select_element)