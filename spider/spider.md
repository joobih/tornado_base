## Python爬虫框架分享

这篇文章主要介绍一下这周学习的一个总结，包括各种爬虫库和第三方爬虫框架等的实例使用。用例的代码都可以直接运行的，(只要你有环境)
也为这段时间的辛苦技术寻知路做一个记录吧！以后方便查阅！

#一，爬虫的定义？
	爬虫：是一种按照一定的规则，自动地抓取万维网信息的程序或者脚本。
	我理解的爬虫的分类：
		1，搜索引擎类：例如Google，百度等他们每天都会万维网去抓取数以亿记的网页保存在自己的搜索引擎里，各种网页都
		会是他们感兴趣的；
		2，批量定时抓取指定网站中的感兴趣的东西。比如抓取携程网站上的机票价格，抓取某个租房网上的租房信息等，抓取股票
		实时数据，抓取某个论坛的游客评论信息。这类的爬虫在很多小公司里面需求还是蛮大的。
		3，获取指定网站某个用户的信息：比如运营商，淘宝，京东，学信网，邮件等。
		4，其他...你所关心的数据。

比较常见的用来做爬虫的语言Python，Java，NodeJS，C#，C++等。接下来就针对Python这门语言说一下能够用来做爬虫的一些框架
	

#二，爬虫进阶路线
做了这么久的爬虫给我的感受有以下两点：不断模仿浏览器、和目标站点的互相伤害。

- 不断模仿浏览器：

	有一类第三方库可以做模拟登陆可以自己维护Cookie信息，但是做得不够好！！但是不能全部实现浏览器的功能，
	比如不能执行JS代码，不能自动管理证书等问题
- 和目标站点的互相伤害：

	爬虫的一方：想方设法抓取数据，不用考虑网站的性能和压力，批量跑数据，即使把网站爬挂了也不关我的事。即使某些数据需要加密传输，
	查看源码或则自动执行JS代码也要搞定。遇到需要验证码的就自己写程序识别或则去购买第三方的软件识别。遇到封IP的就用代理。如果再遇到困难，
	干脆直接完全模拟一个无界面的浏览器算了。

	反爬虫：像12306，携程这些网站都经历过网站被爬挂导致不能访问的痛苦，最后12306才设计出了那么变态的验证码。而携程的做法要更
	变态猥琐一些：1，使用minify工具把变量变成abcd还不够，他会变成阿拉伯语（因为阿拉伯语有的时候是从左向右写，有的时候是从右向左写，
	还有的时候是从下向上写）2，抓到你是爬虫了，他们不会直接封你的IP，他会给你一部分真数据给你一部分假数据。
		
	

#三，Python自带的http请求库：
	Python自带的urllib,urllib2,urllib3...

###urllib:

主要是用来处理一些URL格式化，URL参数编码等功能，用来辅助其他模块的，不能增加头部User Agent 等信息。
主要的一些函数有urlopen、quote、unquote。
该模块是最基本的发送http请求的模块，打开一些简单的网页，发送一些简单的post请求。
这些模块都是最基本的能够满足一些简单的网站的爬虫需求，也能够实现Cookies的自我管理等。
但是当遇到一些反爬虫技术做得比较好的网站的话就会很恼火！比如说使用了https请求的网站：像广东移动；

#####用例1：

	import urllib
	
	url = "https://uac.10010.com/portal/mallLogin.jsp?redirectURL=http://iservice.10010.com/e3/"
	f = urllib.urlopen(url)
	html = f.read()
	coding = getcode()
	info = f.info()
	print info
	print coding
	print html


###urllib2:

	优点：
		比urllib更好一些，可以自己定义头部去发送请求，可以增加cookie管理模块实现模拟登陆，也是很多爬虫库的底层支撑库。比如mechanize等。
	缺点：
		功能太少。

#####用例2：

	'
	import urllib
	import urllib2

	url = 'http://www.pythontab.com' 
	headers = {"User-Agent":'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
	values = {'name' : 'Michael Foord', 
          'location' : 'pythontab', 
          'language' : 'Python' }  
	data = urllib.urlencode(values)
	req = urllib2.Request(url,data,headers = headers)
	response = urllib2.urlopen(req)
	html = response.read()
	print html
	'
#四，mechanize和requests
这两个爬虫模块比urllib2功能要等多一些，他们可以基本实现模拟浏览器功能，也可以自动管理cookies去访问状态的保存。下面就简单说一下这两个模块的优缺点：

###[mechanize](https://pypi.python.org/pypi/mechanize)

		优点：可以实现自动地管理cookies信息。在urllib2基础上封装的一套http请求，所以urllib2能做的基本都可以做。由于是自己手动执行http请
	求,所以速度还是比较快。

		缺点：不能运行JS代码，不能完全实现浏览器的基本功能。文档少，最新版本是2011年发布的0.2.5版，作者也已经停止更新了，所以很多新功能和
	bug也没有维护。比较大型的爬虫需求不建议使用该模块。

###[requests](https://pypi.python.org/pypi/requests)

		优点和mechanize基本上差不多，都可以实现cookies的管理，但requests是基于urllib3上进行的封装，使用到了一个叫做HTTP连接池的东西。

		缺点是同一个站点如果是使用了多个服务器，某些页面跳转时从一个域名跳转到另一个域名时就会出现问题。和mechanize一样，他也不可以运行JS
	代码。如果需要执行JS代码都需要安装其他模块结合起来使用，很麻烦。

#####用例3：mechanize
	

	'
	import mechanize
	import cookielib
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)#
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)	
	br.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"),]
	url = "https://uac.10010.com/portal/mallLogin.jsp?redirectURL=http://iservice.10010.com/e3/"
	br.open(url)
	t = str(int(1000*time.time()))
    redirectURL = "http%3A%2F%2Fwww.10010.com"
    url = "https://uac.10010.com/portal/Service/MallLogin?"+\
              "req_time=%s&redirectURL=%s&userName=%s&password=%s&" +\
              "pwdType=01&productType=01&redirectType=01&rememberMe=1&_=%s"
    url = url % (t,redirectURL,username,password,t)
	r = br.open(url)
	print r.code
	html = br.response().read()
	coding = br.encoding()
	print html

	'

#####用例4：requests

	'
	#encoding=utf-8
	import requests
	import httplib
	import json
	
	httplib.HTTPConnection.debuglevel = 1
	
	def login():
	    s = requests.Session()
	    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"}
	    username = "17721495426"
	    password = "KtQQA9l74zP6TRIhNwAiQw=="	#433142
	    url = "http://login.189.cn/login"
	    s.get(url,headers = headers)
	    url1 = "http://login.189.cn/login/ajax"
	    param1 = {
	        "m":"checkphone",
	        "phone":username
	    }
	    r = s.post(url1,data=param1,headers = headers)
	    html1 = r.content
	    print html1
	    html1 = json.loads(html1)
	    ProvinceID = html1["ProvinceID"]
	    param2 = {
	        "Account":username,
	        "AreaCode":"",
	        "CityNo":"",
	        "ProvinceID":ProvinceID,
	        "UType":"201",
	        "m":"loadlogincaptcha"
	    }  
	    s.post(url,data=param2,headers = headers)
	    login_url = "http://login.189.cn/login"
	    param_login = {
	        "Account":username,
	        "Password":password,
	        "UType":"201",
	        "ProvinceID":ProvinceID,
	        "AreaCode":"",
	        "CityNo":"",
	        "RandomFlag":"",
	        "Captcha":"",
	     }   
	    r = s.post(login_url,data=param_login,headers = headers)

	'

#五，spynner

###spynner :
	这是一个使用了PYQt4图形框架的库，自己实现了一个浏览器界面，基于WebKit浏览器引擎之上进行的开发。可以模拟用户在浏览器中的各种点击，移动鼠标，定位等功能。要使用该库需要安装以下的依赖库：
	sudo apt-get install libx11-dev mesa-common-dev libglu1-mesa-dev libxrandr-dev libxi-dev libxetx-dev libxtst.dev libpng-dev 
	优点：不用像requests和mechanize那样去操心后台发送的get/post请求，这就像是让告诉机器应该在哪里输入数据，哪里点击提交按钮，点击链接。完全的实现机器浏览网页数据。不用手动点击。还可以执行JS代码
	缺点：由于涉及到图形库的加载，并且自己实现的浏览器，运行速度很慢。有时候界面还会卡死。所以并不建议用在实际生产环境中去。适合用来做研究，测试。

#####用例5：spynner
	'
	#encoding=utf-8
	__docformat__ = 'restructuredtext en'
	
	from time import sleep
	from spynner import browser
	def login():
	    br = browser.Browser()
	    #浙江登陆页面
	    url = "http://zj.189.cn/wt_uac/auth.html?app=wt&login_goto_url=nb%2Fzhuanti%2Fsdhd%2F&module=null&auth=uam_login_auth&template=uam_login_page"
	    
	    br.load(url,load_timeout=30)
	    br.create_webview()
	    br.show()
	    br.wk_fill('input[id=u_account]', '17706516913')
	    br.wk_fill('input[id=u_password]', '905405')
		#查找id=imgbar的img标签
	    pic = br.webframe.findFirstElement("img#imgbar")
	    
	    src = str(pic.attribute("src"))
	    print src
		#下载页面的数据
	    pic_html = br.download(src)
	    print pic_html
	    f = open("zhejiang.jpg","wb")
	    f.write(pic_html)
	    f.close()
	    pic_captcha = raw_input("输入验证码")
	    br.wk_fill('input[id=product_code]', pic_captcha)           #查找id=product_code的input输入框并且填充字符串pic_captcha
	    br.wk_click("input[class=paySub]",wait_load=True)           #查找class=paySub的input输入框组件并且点击
	    # br.native_click("input[class=paySub]",wait_load=True,timeout= 50)
	    html = str(br.webframe.toHtml().toUtf8())                   #获取点击后的页面数据（不转码的话中文显示成？）
	    cookies = br.get_cookies()                                  #获取cookies信息
	    print html
	    # print br.manager.windows
	    raw_input("prompt")
	    br.close()      #关闭浏览器
	    
	if __name__ == "__main__":
		login()
		
	'

#六，Splinter,Selenium2
	因为Splinter是再Selenium基础上进行的封装。所以直接看Selenium的使用。最后再简单说一下Splinter的一些API。
	首先Selenium2(WebDriver)是一个可以调用浏览器进行各种模拟操作的框架，包括调用真实浏览器Firefox,Chrome,IE，Opera，Safar。以及无界面的浏览器
	驱动PhantomJS和HtmlUnit ，它还可以支持移动端。其中Chrome，Firefox，PhantomJS是需要安装第三方的驱动插件。
	真实的调取浏览器可以看到他操作浏览器进行的各种操作。方便你做调试，相对来说运行速度就会慢一些。

#####用例6：Selenium
	'
	#encoding=utf-8
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.common.action_chains import ActionChains
	from selenium.common.exceptions import NoSuchElementException
	import time
	import requests
	import httplib
	httplib.HTTPConnection.debuglevel = 1 
	
	def unicom():
	#     driver = webdriver.PhantomJS()
	    driver = webdriver.Firefox()
	    driver.implicitly_wait(10)
	    url = "https://uac.10010.com/portal/homeLogin"
	    url1 = "http://iservice.10010.com/e3/query/call_dan.html?menuId=000100030001"
	    driver.get(url)
	    username = driver.find_element_by_id("userName")
	    username.clear()
	    username.send_keys("15528281963")
	    password = driver.find_element_by_id("userPwd")
	    password.clear()
	    password.send_keys("554682")
	    submit = driver.find_element_by_id("login1").click()
	    time.sleep(10)
	    win = driver.current_window_handle
	    driver.switch_to_window(win)
	    print driver.page_source
	    raw_input("prompt")
	    action = ActionChains(driver)
	    print driver.page_source
	    i = 10
	    while i:
	        win = driver.current_window_handle
	        try: 
	            driver.find_element_by_xpath("//a[@href='http://iservice.10010.com/e3/']")
	            break
	        except (NoSuchElementException,Exception),e:
	            time.sleep(0.5)
	            print e,
	            i -= 1
	            continue
	    
	    driver.get(url1)
	    cookies = driver.get_cookies()
	    print cookies
	    re_cookie = {}
	    for cookie in cookies:
	        re_cookie[cookie['name']] = cookie['value']
	        print "%s = %s" % (cookie['name'], cookie['value'])
	    print re_cookie
	    url = "http://iservice.10010.com/e3/static/query/callDetail?_=1473235527125&menuid=000100030001"
	    param = {"pageNo":"1","pageSize":"100","beginDate":"2016-06-01","endDate":"2016-06-30"}
	    header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"}
	    r = requests.post(url,data = param,headers = header, cookies = re_cookie)
	    print r.content
	    driver.quit()
	    
	if __name__ == "__main__":
		unicom()
	    
	'

