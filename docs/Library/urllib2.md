# 1.urllib2库的基本使用

所谓网页抓取，就是把url地址中指定的网络资源从网络中读取出来，保存到本地，在Python中有很多库用来抓取网页，我们先学习urllib2

```python
urllib2是Python2.7自带的模块，（不需要下载，直接导入）
urllib2官方文档：https://docs.python.org/2/library/urllib2.html
urllib2源码：https://hg.python.org/cpython/file/2.7/Lib/urllib2.py
    urllib2在Python3.x中被改为urllib.request
```

## urlopen

```python
import urllib2
#向指定url发送请求，并返回服务器响应的类文件对象
response = urllib2.urlopen("http://www.baidu.com")

#类文件对象支持 文件对象的操作方法，如read()方法读取文件全部内容，返回字符串
html = response.read()
print(html)
```

## Request	

​	在我们第一个例子里，urlopen()的参数就是一个url地址；

但是如果需要执行更复杂的操作，比如增加HTTP报头，必须创建一个Request实例来作为urlopen()的参数，而需要访问的url地址则作为Request实例的参数

```python
import urllib2
#url作为Request()方法的参数，构造并返回一个Request对象
request = urllib2.Request("http://www.baidu.com")

#Request对象作为urlopen()方法的参数，发送给服务器并接收响应
response = urllib2.urlopen(request)
html = response.read()
print(html)
```

运行结果完全一样的：

```wiki
新建Request实例，除了必须要有url参数之外，还可以设置另外两个参数：
1.data（默认为空）：是伴随url提交的数据，（比如要post的数据），同时HTTP请求将从GET改为
POST方式。
2.headers（默认为空）：是一个字典，包含了需要发送的HTTP报头的键值对。
这两个参数下面会说到。
```

## User-Agent

但是这样直接用urllib2给一个网站发送请求的话，确实有点唐突了，

但是如果我们用一个合法的身份去请求别人网站，显然人家就是欢迎的，所以我们应该给我们的这个代码加上一个身份，就是所谓的User-Agent头

```wi
浏览器就是互联网世界上公认被允许的身份，如果我们希望我们的爬虫程序更像一个真实用户，那我们第一步，就是需要伪装成一个被公认的浏览器
```

```python
import urllib2
url = "http://www.baidu.com"

ua_header = {
	'User-Agent':'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0;'
}

#url返回headers，一起构造Request请求，这个请求将附带IE浏览器的User-Agent
request = urllib2.Request(url,headers=ua_header)

#向这个服务器发送请求
response = urllib2.urlopen(request)
html = response.read()
print(html)
```

### 添加更多的Header信息

在HTTP Request中加入特定的Header，来构造一个完整的HTTP请求信息。

```wiki
可以通过调用Request.add_header()添加/修改一个特定的header
也可以通过调用Request.get_header()来查看已有的header
```

添加一个特定的header

```python
import urllib2

url = "http://www.baidu.com"
header = {"User-Agent":"Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0"}
request = urllib2.Request(url,headers = header)

#也可以通过调用Request.add_header()添加/修改一个特定的header
request.add_header("Connection","keep-alive")

#也可以通过调用Request.get_header()来查看header信息
#request.get_header(header_name="Connection")

response = urllob2.urlopen(request)
print(response.code) #可以查看响应状态码
html = response.read()
print(html)

```

随机添加/修改/User-Agent

```python
import urllib2
import random

url = "http://www.baidu.com"

ua_list=[
    "Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS... "
]
user_agent = random.choice(ua_list)

request = urllib2.Request(url)

request.add_header("User-Agent",user_agent)

#第一个字母大写，后面的全部小写
request.get_header("User-agent")
response = urllib2.urlopen(request)
html = response.read()
print(html)
```

# 2.GET请求和POST请求

urllib2默认只支持HTTP/HTTPS的GET和POST方法

## urllib.urlencode()

urllib和urllib2都是接收url请求的相关模块，但是提供了不同的功能，两个最显著的不同如下：

```wiki
urllib仅可以接收URL，不能创建设置了headers的Request类实例；
但是urllib提供了urlencode()方法用来GET查询字符串的产生，而urllib2则没有。（这是urllib和urllib2经常一起使用的主要原因）

编码工作使用urllib的urlencode()函数，帮我们将key:value这样的键值对转换成"key=value"这样的字符串，解码工作可以使用urllib的unquote()函数。（注意，不是urllib2.urlencode())
```

```python
>>> import urllib
>>> world = {"wd":"百度一下"}

#通过urllib.urlencode()方法，将字典键值对按URL编码转换，从而被web服务器接受
>>> urllib.urlencode(world)
'wd=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B'

#通过urllib.unquote()方法，把url编码字符串，转换回原先字符串。
>>> print(urllib.unquote("wd=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B"))
wd=百度一下

```

**一般的HTTP请求提交数据，需要编码成URL编码格式，然后作为URL的一部分，或者作为参数传到Request对象中。**

## GET方式

get请求一般用于我们向服务器获取数据，比如说，我们用百度搜索 臭屁猫：<https://www.baidu.com/s?wd=臭屁猫

http://www.baidu.com/s?wd=%E8%87%AD%E5%B1%81%E7%8C%AB

在其中我们可以看到在请求部分里，http://www.baidu.com/s?之后出现一个长长的字符串，其中就包含我们要查询的关键词臭屁猫，于是我们可以尝试用默认的GET方式来发送请求。

```python
import urllib	#负责url编码处理
import urllib2

url = "http://www.baidu.com/s"

word = {"wd":"臭屁猫"}
#转换url编码格式（字符串）
word = urllib.urlencode(word)
fullurl = url +"?"+word #url首个分隔符就是?

headers = {
	"User-Agent":"Mozilla/5.0 (Macintosh; U; PPC Mac OS X"
}

request = urllib2.Request(url,headers = headers)
response = urllib2.urlopen(request)
html = response.read()
print(html)
```

#### 批量爬取贴吧页面数据

```wiki
首先我们创建一个python文件, tiebaSpider.py，我们要完成的是，输入一个百度贴吧的地址，比如：

百度贴吧LOL吧第一页：http://tieba.baidu.com/f?kw=lol&ie=utf-8&pn=0

第二页： http://tieba.baidu.com/f?kw=lol&ie=utf-8&pn=50

第三页： http://tieba.baidu.com/f?kw=lol&ie=utf-8&pn=100
```

发现规律了吧，贴吧中每个页面不同之处，就是url最后的pn的值，其余的都是一样的，我们可以抓住这个规律。

- 先写一个main，提示用户输入要爬取的贴吧名，并用urllib.urlencode()进行转码，然后组合url,假设全是LoL吧，那么组合后的url就是："http://tieba.baidu.com/f?kw=lol"

```python
#模拟main函数
import urllib
import urllib2

if __name__ == "__main__":

	kw = raw_input("请输入要爬取的贴吧：")
	#输入起始页和终止页，str转成int类型
	beginPage = int(raw_input("请输入起始页："))
	endPage = int(raw_input("请输入终止页："))

	url = "http://tieba.baidu.com/f?"
	key = urllib.urlencode({"kw":kw})

	#组合后的url示例：http://tieba.baidu.com/f?kw=lol
	url = url + key
	tiebaSpider(url,beginPage,endPage)
```

- 接下来，我们写一个百度贴吧爬虫接口，我们需要传递3个参数给这个接口，一个是main里组合的url地址，以及起始页和终止页码，表示要爬取页码的范围。

```python
def tiebaSpider(url,beginPage,endPage):
	"""
		作用：负责处理url，分配每个url去发送请求
		url:需要处理的第一个url
		beginPage:爬虫执行的起始页面
		endPage:爬虫执行的结束页面
	"""
	for page in range(beginPage,endPage + 1):
		pn = (page - 1) * 50

		filename = "第" + str(page)+"页.html"
		#组合为完整的url,并且pn值每次增加50
		fullurl = url + "&pn" + str(pn)
		# print(fullurl)

		#调用loadPage()发送请求获取HTML页面
		html = loadPage(fullurl,filename)
		#将获取到的HTML页面写入本地磁盘文件
		writeFile(html,filename)
```

- 我们之前已经写出一个爬取一个网页的代码，现在，我们可以将他封装成一个小函数loadPage（）供我们使用

```python
def loadPage(url,filename):
	"""
		作用：根据url发送请求，获取服务器响应文件
		url:需要爬取的url地址
		filename:文件名
	"""
	print("正在下载" + filename)
	headers={"User-Agent":"Baiduspider"}
	request = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(request)
	return response.read()
```

- 最后我们希望将爬取到的每个页面的信息存储在本地磁盘上，我们可以简单写一个存储文件的接口。

```python
def writeFile(html,filename):
	"""
		作用：保存服务器响应文件到本地磁盘文件里
		html:服务器响应文件
		filename:本地磁盘文件名
	"""
	print("正在存储."+filename)

	with open(filename,'w') as f:
		f.write(html)
	print("*"*20)
```

## POST方式：

上面我们说了Request请求对象的里面有data参数，他就是用在POST里的，我们要传送的数据就是这个参数data，data是一个字典，里面要匹配键值对

于是，我们可以尝试用POST方式发送请求。

```python
import urllib
import urllib2

#post请求的目标url
url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"

headers = {'User-Agent':'Baiduspider'}

formdata = {
	"type":"AUTO",
    "i":"i love python",
    "doctype":"json",
    "xmlVersion":"1.8",
    "keyfrom":"fanyi.web",
    "ue":"UTF-8",
    "action":"FY_BY_ENTER",
    "typoResult":"true"
}

data = urllib.urlencode(formdata)

request = urllib2.Request(url,data=data,headers=headers)
response = urllib2.urlopen(request)
print(response.read())
```

发送POST请求时，需要特别注意headers的一些属性：

```wiki
Content-Length:144:是指发送的表单数据长度为144，也就是字符个数是144个

X-Requested-With: XMLHttpRequest ：表示Ajax异步请求。

Content-Type: application/x-www-form-urlencoded ： 表示浏览器提交 Web 表单时使用，表单数据会按照 name1=value1&name2=value2 键值对形式进行编码。
```

## 获取AJAX加载的内容

有些网页内容使用Ajax加载，只要记得，ajax一般返回的是json，直接对ajax地址进行post或get，就返回json数据了。

“作为一名爬虫工程师，你最需要关注的，是数据的来源”

```python
import urllib
import urllib2

#demo1
url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action'

headers = {
	"User-Agent":'Biaduspider'
}

formdata = {
	'start':'0',
	'limit':'10',
}
data = urllib.urlencode(formdata)

request = urllib2.Request(url,data=data,headers=headers)

response = urllib2.urlopen(request)

print(response.read())

#demo2

url = 'https://movie.douban.com/j/chart/top_list?'

headers = {"User-Agent":'Baiduspider'}

#处理所有参数

formdata = {
	'type':'11',
    'interval_id':'100:90',
    'action':'',
    'start':'0',
    'limit':'10'
}

data = urllib.urlencode(formdata)

request = urllib2.Reuqest(url,data=data,headers=headers)
response = urllib2.urlopen(request)
print(response.read())

```

### 问题：为什么 有时候POST也能在URL内看到数据？

- GET方式是直接以链接形式访问，链接中包含了所以的参数，服务器端用Request.QueryString获取变量的值，如果包含了密码的话是一种不安全的选择，不过你可以直观地看到自己提交了什么内容。
- POST则不会在网址上显示所有的参数，服务器端用Request.Form获取提交的数据，在Form提交的时候，但是HTML代码里如果不指定method属性，则默认为GET请求，Form中提交的数据将会附加在url之后，以 ? 分开与 url 分开
- 表单数据可以作为URL字段（method="get")或者HTTP POST(method="post")的方式来发送。比如在下面的HTML代码中，表单数据将因为（method='get'）而附加到URL上；

```html
<form action="form_action.asp" method="get">
    <p>First name: <input type="text" name="fname" /></p>
    <p>Last name: <input type="text" name="lname" /></p>
    <input type="submit" value="Submit" />
</form>
```

## 处理HTTPS请求SSL证书验证

现在随处课件https开头的网站，urllib2可以为HTTPS请求验证SSL证书，就像web浏览器一样，如果网站的ssl证书是经过CA认证的，则能够正常访问，如："https://www.baidu.com/"等

如果ssl证书验证不通过，或者操作系统不信任服务器的安全证书，比如浏览器访问12306网站。



urllib2在访问的时候则会报出SSLError

```python
import urllib2

url = 'https://www.12306.cn/mormhweb/'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
request = urllib2.Request(url,headers=headers)

response = urllib2.urlopen(request)
print(response.read())

#运行结果：
urllib2.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)>
```

所以。如果以后遇到这种网站，我们需要单独处理SSL证书，让程序忽略SSL证书验证错误，即可正常访问。

```python
import urllib
import urllib2
import ssl

#1.表示忽略未经核实的SSL证书认证
context = ssl._create_unverified_context()

url = "https://www.12306.cn/mormhweb"

headers = {"User-Agent":'Baiduspider'}

request = urllib2.Request(url,headers=headers)

#2.在urlopen()方法里 指明添加context参数
response = urllib2.urlopen(response,context = context)

print(response.read())
```

### 关于CA

CA(Certificate Authority)是数字证书认证中心的简称，是指发放、管理、废除数字证书的受信任的第三方机构，如[北京数字认证股份有限公司](http://www.bjca.org.cn)、[上海市数字证书认证中心有限公司](http://www.sheca.com)等...

CA的作用是检查证书持有者身份的合法性，并签发证书，以防证书被伪造或篡改，以及对证书和密钥进行管理。

现实生活中可以用身份证来证明身份， 那么在网络世界里，数字证书就是身份证。和现实生活不同的是，并不是每个上网的用户都有数字证书的，往往只有当一个人需要证明自己的身份的时候才需要用到数字证书。

普通用户一般是不需要，因为网站并不关心是谁访问了网站，现在的网站只关心流量。但是反过来，网站就需要证明自己的身份了。

比如说现在钓鱼网站很多的，比如你想访问的是[www.baidu.com](http://www.baidu.com)，但其实你访问的是[www.daibu.com](http://www.daibu.com)”，所以在提交自己的隐私信息之前需要验证一下网站的身份，要求网站出示数字证书。

一般正常的网站都会主动出示自己的数字证书，来确保客户端和网站服务器之间的通信数据是加密安全的



# 3.Handler处理器和自定义Openr

- opener是urllib2.OpenerDirector的实例，我们之前一直都在使用的urlopen，它是一个特殊的opener（也就是模块帮我们构建好的）。
- 但是基本的urlopen()方法不支持代理，cookie等其他的HTTP/HTTPS高级功能，所以要支持这些功能
  - 1.使用相关的Handler处理器来创建特定功能的处理器对象；
  - 2.然后通过urllib2.build_opener()方法使用这些处理器对象，创建自定义opener对象；
  - 3.使用自定义的opener对象，调用open()方法发送请求。
- 如果程序里所有的请求都使用自定义的opener，可以使用urllb2.install_opener()将自定义的opener对象，定义为全局的opener，表示如果之后凡是调用urlopen，都将使用这个opener（根据自己的需求来选择）

## 简单的自定义opener()

```python
import urllib2

#构建一个HTTPHandler处理器对象，支持处理HTTP请求
http_handler = urllib2.HTTPHandler()

#构建一个HTTPHandller处理器对象，支持处理hTTPS请求
#http_handler = urllib2.HTTPSHandler()

#调用urllib2.build_opener()方法，创建支持处理HTTP请求的opener对像
opener = urllib2.build_opener(http_handler)

#构建Request请求
request = urllib2.Request('http://www.baidu.com')

#调用自定义opener对象的open()方法，发送request请求
response = opener.open(request)

#获取服务器响应内容
print(response.read())
```

这种方式发送请求得到的结果，和使用urllib2.urlopen()发送HTTP/HTTPS请求得到的结果是一样的。

如果在HTTPHandler（）增加debuglevel=1参数，还会将Debug Log打开，这样程序在执行的时候，会把收包和发包的报头在屏幕上自动打印出来，方便调试，有时可以省去抓包的工作。

```python
#仅需要修改的代码部分

#构建一个HTTPHandler处理器对象，支持处理HTTP请求，同时开启Debug Log,debuglevel值默认0

http_handler = urllib2.HTTPHandler(debuglevel = 1)

#构建一个HTTPSHandler处理器对象，支持处理HTTPS请求，同时开启debug log,debuglevel值默认为0
https_handler = urllib2.HTTPSHandler(debuglevel = 1)

```

## ProxyHandler处理器（代理设置）

使用代理IP，这是爬虫/反爬虫的第二大招，通常也是最好用的。

很多网站会检测某一段时间某个IP的访问次数。（通过流量统计。系统日志等）。如果访问次数多的不像正常人，它会禁止这个IP的访问。

所以我们可以设置一些代理服务器，每隔一段时间换一个代理，就算IP被禁止，依然可以换个IP继续爬

urllib2中通过ProxyHandler来设置使用代理服务器，下面代码说明如何使用自定义opener来使用代理；

```python
import urllib2

#构建了两个代理Handler,一个有代理IP，一个没有代理IP
httpproxy_handler = urllib2.ProxyHandler({"http":'122.114.31.177:808'})
nullproxy_handler = urllib2.ProxyHandler({})

proxySwitch = True #定义一个开关

#通过urllib2.build_opener()方法使用这些代理Handler对象，创建自定义opener对象
#根据代理开关是否打开，使用不同的代理模式

if proxySwitch:
	opener = urllib2.build_opener(httpproxy_handler)
else:
	opener = urllib2.build_opener(nullproxy_handler)

request = urllib2.Request("http://www.baidu.com/")

#1.如果这么写，只有使用opener.open()方法发送请求才使用自定义的代理，而urlopen()则不使用自定义代理
response = opener.open(request)

#2.如果这么写，就是将opener应用到全局，之后所以的，不管是opener.open()还是urlopen()发送请求都将使用自定义代理
# urllib2.install_opener(opener)
# response = urlopen(request)

print(response.read()
```

- 免费的开放代理获取基本没有成本，我们可以在一些代理网站上搜集这些免费代理，测试后如果可以用，就把他收集起来用在爬虫上面。
- 免费短期代理网站
  - [西刺免费代理IP](http://www.xicidaili.com/)
  - [快代理免费代理](http://www.kuaidaili.com/free/inha/)
  - [Proxy360代理](http://www.proxy360.cn/default.aspx)
  - [全网代理IP](http://www.goubanjia.com/free/index.shtml)

如果代理IP足够多，就可以向随机获取User-Agent一样，随机选择一个代理去访问网站

```python
import urllib2
import random

proxy_list = [
    {"http" : "124.88.67.81:80"},
    {"http" : "124.88.67.81:80"},
    {"http" : "124.88.67.81:80"},
    {"http" : "124.88.67.81:80"},
    {"http" : "124.88.67.81:80"}
    ]
#随机选择一个代理
proxy = random.choice(proxy_list)

#使用选择的代理构建代理处理器对象
httpproxy_handler = urllib2.ProxyHandler(proxy)

opener = urllib2.build_opener(httpproxy_handler)

request = urllib2.Request("http://www.baidu.com")

response = opener.open(request)
print(response.read())
```

但是，这些免费开放代理一般会有很多人都在使用，而且代理有寿命短，速度慢，匿名度不高，HTTP/HTTPS支持不稳定等缺点（免费没好货）。

所以，专业爬虫工程师或爬虫公司会使用高品质的私密代理，这些代理通常需要找专门的代理供应商购买，再通过用户名/密码授权使用（舍不得孩子套不到狼）。

## HTTPPasswordMgrWithDefaultRealm()

`HTTPPasswordMgrWithDefaultRealm()`类将创建一个密码管理对象，用来保存 HTTP 请求相关的用户名和密码，主要应用两个场景：

1. 验证代理授权的用户名和密码 (`ProxyBasicAuthHandler()`)
2. 验证Web客户端的的用户名和密码 (`HTTPBasicAuthHandler()`)

## ProxyBasicAuthHandler(代理授权验证)

如果我们使用之前的代码来使用私密代理，会报 HTTP 407 错误，表示代理没有通过身份验证：

`urllib2.HTTPError: HTTP Error 407: Proxy Authentication Required`

所以我们需要改写代码，通过：

- `HTTPPasswordMgrWithDefaultRealm()`：来保存私密代理的用户密码
- `ProxyBasicAuthHandler()`：来处理代理的身份验证。

```python
import urllib2
import urllib

#私密代理授权的账户
user = "mr_mao_hacker"

#私密代理授权的密码
passwd = 'passwd'

#私密代理IP
proxyserver = "61.158.163.130:16816"
# 1. 构建一个密码管理对象，用来保存需要处理的用户名和密码
passwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
# 2. 添加账户信息，第一个参数realm是与远程服务器相关的域信息，一般没人管它都是写None，后面三个参数分别是 代理服务器、用户名、密码
passwdmgr.add_password(None, proxyserver, user, passwd)

# 3. 构建一个代理基础用户名/密码验证的ProxyBasicAuthHandler处理器对象，参数是创建的密码管理对象
#   注意，这里不再使用普通ProxyHandler类了
proxyauth_handler = urllib2.ProxyBasicAuthHandler(passwdmgr)

# 4. 通过 build_opener()方法使用这些代理Handler对象，创建自定义opener对象，参数包括构建的 proxy_handler 和 proxyauth_handler
opener = urllib2.build_opener(proxyauth_handler)

# 5. 构造Request 请求
request = urllib2.Request("http://www.baidu.com/")

# 6. 使用自定义opener发送请求
response = opener.open(request)

# 7. 打印响应内容
print response.read()
```

## HTTPBasicAuthHandler处理器（Web客户端授权验证）

有些Web服务器（包括HTTP/FTP等）访问时，需要进行用户身份验证，爬虫直接访问会报HTTP 401 错误，表示访问身份未经授权：

`urllib2.HTTPError: HTTP Error 401: Unauthorized`

如果我们有客户端的用户名和密码，我们可以通过下面的方法去访问爬取：

```python
import urllib
import urllib2

# 用户名
user = "test"
# 密码
passwd = "123456"
# Web服务器 IP
webserver = "http://192.168.199.107"

# 1. 构建一个密码管理对象，用来保存需要处理的用户名和密码
passwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

# 2. 添加账户信息，第一个参数realm是与远程服务器相关的域信息，一般没人管它都是写None，后面三个参数分别是 Web服务器、用户名、密码
passwdmgr.add_password(None, webserver, user, passwd)

# 3. 构建一个HTTP基础用户名/密码验证的HTTPBasicAuthHandler处理器对象，参数是创建的密码管理对象
httpauth_handler = urllib2.HTTPBasicAuthHandler(passwdmgr)

# 4. 通过 build_opener()方法使用这些代理Handler对象，创建自定义opener对象，参数包括构建的 proxy_handler
opener = urllib2.build_opener(httpauth_handler)

# 5. 可以选择通过install_opener()方法定义opener为全局opener
urllib2.install_opener(opener)

# 6. 构建 Request对象
request = urllib2.Request("http://192.168.199.107")

# 7. 定义opener为全局opener后，可直接使用urlopen()发送请求
response = urllib2.urlopen(request)

# 8. 打印响应内容
print response.read()
```

## Cookie

cookie是指某些网站服务器为了辨别用户身份和进行Session跟踪，而存储在用户浏览器上的文本文件，cookie可以保持登录信息到用户下次与服务器的会话

## Cookie原理

HTTP是无状态的面向链接的协议，为了保持连接状态，引入了Cookie机制cookie是HTTP消息头中的一种属性，包括：

```python
Cookie名字（Name）
Cookie的值（Value）
Cookie的过期时间（Expires/Max-Age）
Cookie作用路径（Path）
Cookie所在域名（Domain），
使用Cookie进行安全连接（Secure）。

前两个参数是Cookie应用的必要条件，另外，还包括Cookie大小（Size，不同浏览器对Cookie个数及大小限制是有差异的）。

```

Cookie由变量名和值组成，根据Netscape公司的规定，Cookie格式如下：

`Set－Cookie: NAME=VALUE；Expires=DATE；Path=PATH；Domain=DOMAIN_NAME；SECURE`

## Cookie应用

cookies在爬虫方面最典型的应用是判断注册用户是否已经登录网站，用户可能得到提示，是否在下一次进入此网站时保留用户信息以便简化登录手续

```python
#_*_ coding:utf-8 _*_
#获取一个有登录信息的Cookie模拟登录

import urllib2

headers = {
    "Host":"www.renren.com",
    "Connection":"keep-alive",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",

    # 便于终端阅读，表示不支持压缩文件
    # Accept-Encoding: gzip, deflate, sdch,

    # 重点：这个Cookie是保存了密码无需重复登录的用户的Cookie，这个Cookie里记录了用户名，密码(通常经过RAS加密)
    "Cookie": "anonymid=ixrna3fysufnwv; depovince=GW; _r01_=1; JSESSIONID=abcmaDhEdqIlM7riy5iMv; jebe_key=f6fb270b-d06d-42e6-8b53-e67c3156aa7e%7Cc13c37f53bca9e1e7132d4b58ce00fa3%7C1484060607478%7C1%7C1484060607173; jebecookies=26fb58d1-cbe7-4fc3-a4ad-592233d1b42e|||||; ick_login=1f2b895d-34c7-4a1d-afb7-d84666fad409; _de=BF09EE3A28DED52E6B65F6A4705D973F1383380866D39FF5; p=99e54330ba9f910b02e6b08058f780479; ap=327550029; first_login_flag=1; ln_uact=mr_mao_hacker@163.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn521/20140529/1055/h_main_9A3Z_e0c300019f6a195a.jpg; t=214ca9a28f70ca6aa0801404dda4f6789; societyguester=214ca9a28f70ca6aa0801404dda4f6789; id=327550029; xnsid=745033c5; ver=7.0; loginfrom=syshome"
}

#2.通过headers里的报头信息（主要是cookie信息）构建Request对象
request = urllib2.Request("http://www.renren.com",headers = headers)

response = urllib2.urlopen(request)

print(response.read())
```

但是这样做太过复杂，我们先需要在浏览器登录账户，并且设置保存密码，并且通过抓包才能获取这个Cookie，那有么有更简单方便的方法呢？

## cookielib库和HTTPCookieProcessor处理器

在Python处理Cookie，一般是通过`cookielib`模块和 urllib2模块的`HTTPCookieProcessor`处理器类一起使用。

- cookielib模块：主要作用是提供用于存储cookie的对象
- HTTPCookieProcessor处理器：主要作用是处理这些cookie对象，并构建handler对象。

### cookilib库

该模块主要对象有CookieJar、FileCookieJar、MozillaCookieJar、LWPCookieJar。

```wiki
CookieJar:管理HTTP cookie值、存储HTTP请求生成的cookie、向传出的HTTP请求添加cookie的对象，整个cookie都存储在内存中，对CookieJar实例进行垃圾回收后cookie也将丢失。

FileCookieJar(filename,delayload=None,policy=None)：从CookieJar派生而来，用来创建FileCookieJar实例，检索cookie信息并将cookie存储到文件中。filename是存储cookie的文件名。
delayload为True时支持延迟访问文件，即只有在需要时才读取文件或在文件中存储数据。

MozillaCookieJar(filename,delayload=None,policy=None):从FileCookieJar派生而来，创建Mozilla浏览器cookies.text兼容的FileCookieJar实例。

LWPCookieJar(filename,delayload=None,policy=None):从FileCookieJar派生而来，创建与libwwww-perl标准的Set-Cookie3文件格式 兼容的FileCookieJar实例
```

**其实大多数情况下，我们只用CookieJar(),如果需要和本地文件交互，就用MozillaCookJar()或LWPCookieJar()**

我们来做几个案例：

#### (1)获取Cookie，并保存到CookieJar()对象中

```python
import urllib2
import cookielib

#构建一个CookieJar对象实例来保存cookie
cookiejar = cookielib.CookieJar()

#使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar()对象
handler = urllib2.HTTPCookieProcessor(cookiejar)

#通过build_opener()来构建opener
opener = urllib2.build_opener(handler)

#以get方法访问页面，访问之后会自动保存cookie到cookiejar中
opener.open("http://www.baidu.com/")

##可以按标准格式将保存的Cookie打印出来
cookieStr = ""
for item in cookiejar:
	cookieStr = cookieStr + item.name + "=" + item.value +";"

#舍去最后一位的分好
print(cookieStr[:-1])
```

我们使用以上方法将Cookie保存到cookiejar对象中，然后打印除了cookie中的值，也就是访问百度首页的cookie值。

运行结果如下：

```python
BAIDUID=253786CD49A616E6A07F7C634FC1078B:FG=1;BIDUPSID=253786CD49A616E6A07F7C634FC1078B;H_PS_PSSID=1439_24569_21117_20927;PSTM=1517406240;BDSVRTM=0;BD_HOME=0
```

#### (2)访问网站获得cookie，并把获得的cookie保存在cookie文件中

```python
import urllib2
import cookielib

#保存cookie的本地文件名
filename = 'cookie.txt'

#声明一个MozillaCookieJar(由save实现)对象实例来保存cookie,之后写入文件
cookiejar = cookielib.MozillaCookieJar(filename)

#使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar()对象
handler = urllib2.HTTPCookieProcessor(cookiejar)

#通过build_opener()来构建opener
opener = urllib2.build_opener(handler)

#创建一个请求，原理同urllib2的urlopen
response = opener.open("http://www.baidu.com")

#保存cookie到本地文件
cookiejar.save()

```

#### 3.从文件中获取cookies，作为请求的一部分去访问

```python
import urllib2
import cookielib

#创建MozillCookieJar(有load实现)实例对象
cookiejar = cookielib.MozillaCookieJar()

#从文件中读取cookie内容到变量
cookiejar.load('cookie.txt')

#使用HTTPCookieProcess()来创建cookie处理器对像，参数为CookieJar()对象
handler = urllib2.HTTPCookieProcessor(cookiejar)

#通过build_opener()来构建opener
opener = urllib2.build_opener(handler)

response = opener.open("http://www.baidu.com")

```

### 利用cookie和POST登录人人网

```python
import urllib
import urllib2
import cookielib

#1.构建一个CookieJar对象实例来保存cookie
cookie = cookielib.CookieJar()

#2.使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar对象
cookie_handler = urllib2.HTTPCookieProcessor(cookie)

#3.通过build_opener()来构建opener
opener = urllib2.build_opener(cookie_handler)

#4.addheaders接收一个列表，里面每个元素都是一个headers信息的元组，opener将附带headers信息
opener.addheaders=[("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36")]

#5.需要登录的账户和密码
data = {'email':'youemail','password':'passwd'}

#6.通过urlencode()转码
postdata = urllib.urlencode(data)

#7.构建Request请求对象，包含需要发送的用户名和密码
url = 'http://www.renren.com/PLogin.do'
request = urllib2.Request(url,data=postdata)

#8.通过opener发送这个请求，并获取登录后的Cookie值
opener.open(request)

#9.opener包含用户登录后的cookie值，可以直接访问那些登录后才可以访问的页面
response = opener.open("http://www.renren.com/410043129/profile")

# 10. print
print(response.read())

```

模拟登录要注意几点：

```wiki
登录一般会现有一个HTTP GET，用于拉去一些信息以及获得Cookie，然后在HTTP POST登录。

HTTP POST 登录的链接有可能是动态的，从GET返回的信息中获取

password有些是明文发送，有些是加密后发送，有些网站甚至采用动态加密的，同事包括了很多其他数据的加密信息，只能通过查询JS源码获得加密算法，再去破解加密，非常困难

大多数网站的登录整体流程是类似的，可能有些细节不一样，所以不能保证其他网站登录成功。
```

**这个测试案例中，为了想让大家快速理解知识点，我们使用的人人网登录接口是改版前的隐藏接口。登录比较方便**

**当然，我们也可以直接发送账户密码到登录界面模拟登录，但是当网页采用javaScript动态技术后，想封锁基于 HttpClient 的模拟登录就太容易了，甚至可以根据你的鼠标活动的特征准确地判断出是不是真人在操作。**

所以，想做通用的模拟登录还要选别的技术，比如用内置浏览器引擎的爬虫（关键字：Selenium,PhantomJS)后面学习到。

# urllib2的异常错误处理

在我们用`urlopen或opener.open`方法发出一个请求时，如果`urlopen或opener.open`不能处理这个response，就产生错误。

这里主要说的是URLError和HTTPError，以及对它们的错误处理。

## URLError

URLError 产生的原因主要有：

> 1. 没有网络连接
> 2. 服务器连接失败
> 3. 找不到指定的服务器

我们可以用`try except`语句来捕获相应的异常。下面的例子里我们访问了一个不存在的域名：

```python
# urllib2_urlerror.py

import urllib2

requset = urllib2.Request('http://www.ajkfhafwjqh.com')

try:
    urllib2.urlopen(request, timeout=5)
except urllib2.URLError, err:
    print err
```

运行结果如下：

```python
<urlopen error [Errno 8] nodename nor servname provided, or not known>

urlopen error，错误代码8，错误原因是没有找到指定的服务器。
```

## HTTPError

HTTPError是URLError的子类，我们发出一个请求时，服务器上都会对应一个response应答对象，其中它包含一个数字"响应状态码"。

如果`urlopen或opener.open`不能处理的，会产生一个HTTPError，对应相应的状态码，HTTP状态码表示HTTP协议所返回的响应的状态。

**注意，urllib2可以为我们处理重定向的页面（也就是3开头的响应码），100-299范围的号码表示成功，所以我们只能看到400-599的错误号码。**

```python
# urllib2_httperror.py

import urllib2

requset = urllib2.Request('http://blog.baidu.com/itcast')

try:
    urllib2.urlopen(requset)
except urllib2.HTTPError, err:
    print err.code
    print err
```

运行结果如下：

```python
404
HTTP Error 404: Not Found
```

HTTP Error，错误代号是404，错误原因是Not Found，说明服务器无法找到被请求的页面。

> 通常产生这种错误的，要么url不对，要么ip被封。

## 改进版

由于HTTPError的父类是URLError，所以父类的异常应当写到子类异常的后面，所以上述的代码可以这么改写：

```python
import urllib2

requset = urllib2.Request('http://blog.baidu.com/itcast')

try:
    urllib2.urlopen(requset)

except urllib2.HTTPError, err:
    print err.code

except urllib2.URLError, err:
    print err

else:
    print "Good Job"
```

运行结果如下：

```python
404
```

##### 这样我们就可以做到，首先捕获子类的异常，如果子类捕获不到，那么可以捕获父类的异常。



# HTTP响应状态码参考：

```wiki
1xx:信息

100 Continue
服务器仅接收到部分请求，但是一旦服务器并没有拒绝该请求，客户端应该继续发送其余的请求。
101 Switching Protocols
服务器转换协议：服务器将遵从客户的请求转换到另外一种协议。



2xx:成功

200 OK
请求成功（其后是对GET和POST请求的应答文档）
201 Created
请求被创建完成，同时新的资源被创建。
202 Accepted
供处理的请求已被接受，但是处理未完成。
203 Non-authoritative Information
文档已经正常地返回，但一些应答头可能不正确，因为使用的是文档的拷贝。
204 No Content
没有新文档。浏览器应该继续显示原来的文档。如果用户定期地刷新页面，而Servlet可以确定用户文档足够新，这个状态代码是很有用的。
205 Reset Content
没有新文档。但浏览器应该重置它所显示的内容。用来强制浏览器清除表单输入内容。
206 Partial Content
客户发送了一个带有Range头的GET请求，服务器完成了它。



3xx:重定向

300 Multiple Choices
多重选择。链接列表。用户可以选择某链接到达目的地。最多允许五个地址。
301 Moved Permanently
所请求的页面已经转移至新的url。
302 Moved Temporarily
所请求的页面已经临时转移至新的url。
303 See Other
所请求的页面可在别的url下被找到。
304 Not Modified
未按预期修改文档。客户端有缓冲的文档并发出了一个条件性的请求（一般是提供If-Modified-Since头表示客户只想比指定日期更新的文档）。服务器告诉客户，原来缓冲的文档还可以继续使用。
305 Use Proxy
客户请求的文档应该通过Location头所指明的代理服务器提取。
306 Unused
此代码被用于前一版本。目前已不再使用，但是代码依然被保留。
307 Temporary Redirect
被请求的页面已经临时移至新的url。



4xx:客户端错误

400 Bad Request
服务器未能理解请求。
401 Unauthorized
被请求的页面需要用户名和密码。
401.1
登录失败。
401.2
服务器配置导致登录失败。
401.3
由于 ACL 对资源的限制而未获得授权。
401.4
筛选器授权失败。
401.5
ISAPI/CGI 应用程序授权失败。
401.7
访问被 Web 服务器上的 URL 授权策略拒绝。这个错误代码为 IIS 6.0 所专用。
402 Payment Required
此代码尚无法使用。
403 Forbidden
对被请求页面的访问被禁止。
403.1
执行访问被禁止。
403.2
读访问被禁止。
403.3
写访问被禁止。
403.4
要求 SSL。
403.5
要求 SSL 128。
403.6
IP 地址被拒绝。
403.7
要求客户端证书。
403.8
站点访问被拒绝。
403.9
用户数过多。
403.10
配置无效。
403.11
密码更改。
403.12
拒绝访问映射表。
403.13
客户端证书被吊销。
403.14
拒绝目录列表。
403.15
超出客户端访问许可。
403.16
客户端证书不受信任或无效。
403.17
客户端证书已过期或尚未生效。
403.18
在当前的应用程序池中不能执行所请求的 URL。这个错误代码为 IIS 6.0 所专用。
403.19
不能为这个应用程序池中的客户端执行 CGI。这个错误代码为 IIS 6.0 所专用。
403.20
Passport 登录失败。这个错误代码为 IIS 6.0 所专用。
404 Not Found
服务器无法找到被请求的页面。
404.0
没有找到文件或目录。
404.1
无法在所请求的端口上访问 Web 站点。
404.2
Web 服务扩展锁定策略阻止本请求。
404.3
MIME 映射策略阻止本请求。
405 Method Not Allowed
请求中指定的方法不被允许。
406 Not Acceptable
服务器生成的响应无法被客户端所接受。
407 Proxy Authentication Required
用户必须首先使用代理服务器进行验证，这样请求才会被处理。
408 Request Timeout
请求超出了服务器的等待时间。
409 Conflict
由于冲突，请求无法被完成。
410 Gone
被请求的页面不可用。
411 Length Required
"Content-Length" 未被定义。如果无此内容，服务器不会接受请求。
412 Precondition Failed
请求中的前提条件被服务器评估为失败。
413 Request Entity Too Large
由于所请求的实体的太大，服务器不会接受请求。
414 Request-url Too Long
由于url太长，服务器不会接受请求。当post请求被转换为带有很长的查询信息的get请求时，就会发生这种情况。
415 Unsupported Media Type
由于媒介类型不被支持，服务器不会接受请求。
416 Requested Range Not Satisfiable
服务器不能满足客户在请求中指定的Range头。
417 Expectation Failed
执行失败。
423
锁定的错误。



5xx:服务器错误

500 Internal Server Error
请求未完成。服务器遇到不可预知的情况。
500.12
应用程序正忙于在 Web 服务器上重新启动。
500.13
Web 服务器太忙。
500.15
不允许直接请求 Global.asa。
500.16
UNC 授权凭据不正确。这个错误代码为 IIS 6.0 所专用。
500.18
URL 授权存储不能打开。这个错误代码为 IIS 6.0 所专用。
500.100
内部 ASP 错误。
501 Not Implemented
请求未完成。服务器不支持所请求的功能。
502 Bad Gateway
请求未完成。服务器从上游服务器收到一个无效的响应。
502.1
CGI 应用程序超时。　·
502.2
CGI 应用程序出错。
503 Service Unavailable
请求未完成。服务器临时过载或当机。
504 Gateway Timeout
网关超时。
505 HTTP Version Not Supported
服务器不支持请求中指明的HTTP协议版本
```









































