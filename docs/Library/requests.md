# Requests:让HTTP服务人类

虽然Python的标准库urllib2模块已经包含了我们平常使用的大多数功能，但是他的API使用起来让人感觉不太好，而Request自称"HTTP for Humans",说明使用更简洁方便。

> Requests 唯一的一个非转基因的 Python HTTP 库，人类可以安全享用：）

Requests继承了urllib2的所有特性，Requests支持HTTP连接保持和连接池，支持使用cookie保持会话，支持文件上传，支持自动确定响应内容的编码，支持国际化的URL和ＰＯＳＴ数据自动编码

## Requests的底层实现其实就是urllib3

Requests的文档非常完备，中文文档也相当不错。Requests能完全满足当前网络的需求，支持python2.6~3.5，而且能在PyPy下完美运行。

开源地址：<https://github.com/kennethreitz/requests>

中文文档 API： <http://docs.python-requests.org/zh_CN/latest/index.html>

安装方式：

利用pip 安装或者利用easy_install都可以完成安装：

```shell
$ pip install requests
$ easy_install requests
```

## 基本GET请求（headers参数和parmas参数)

### 1.最基本的GET请求可以直接用GET方法

```python
import requests
response = requests.get("http://www.baidu.com/")

#也可以这样写
#response = requests.request("get","http://www.baidu.com/")
```

### 2.添加headers和查询参数

如果想添加headers,可以传入headers参数来增加请求头中的headers信息，如果要将参数放发在url中传递，可以利用 params 参数

```python
import requests

url = "http://www.baidu.com"
kw = {'wd':'长城'}
headers = {
    "User-Agent":"Mozialla/4.0(windows NT 10.0.0;)"
}
#params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
response = requests.get(url,params=kw,headers=headers)

#查看响应内容，response.text返回的是Unicode格式的数据
print(response.text)

#查看响应内容，response.content返回的字节流数据
print(response.content)

#查看完整的url地址
print(response.url)

#查看响应头部字符编码
print(response.encoding)

#查看响应码
print(response.status_code)

结果：
....
.....
http://www.baidu.com/?wd=%E9%95%BF%E5%9F%8E
utf-8
200
```

- 使用response.text时，Requests会基于HTTP响应的文本编码自动解码响应内容，大多数Unicode字符集都能被无缝的解码
- 使用response.content时，返回的是服务器响应数据的原始二进制节流，可以用来保存图片等二进制文件

## 基本ＰＯＳＴ请求(data参数)

### 1.最基本的GET请求可以直接用ｐｏｓｔ方法

```python
response = requests.post(url,data = data)
```

### 2.传入data数据

对于POST请求来说，我们一般需要为他增加一些参数。那么最基本的传参方法可以利用data这个参数。

```python
import requests

formdata = {
    "type": "AUTO",
    "i": "i love python",
    "doctype": "json",
    "xmlVersion": "1.8",
    "keyfrom": "fanyi.web",
    "ue": "UTF-8",
    "action": "FY_BY_ENTER",
    "typoResult": "true"
}

url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"
headers = {
    "User-Agent":"BaiduSpider"
}

response = requests.post(url,data=formdata,headers=headers)

print(response.text)
#如果是json文件可以直接显示
print(response.json())

```

### 代理(Proxies参数)

如果需要使用代理，你可以通过为任意请求方法提供proxies参数来配置单个请求：

```python
import requests

#根据协议类型，选择不同的代理
proxies = {
    "http":"http://112.95.204.193:8888",
    "https":"http://222.223.153.19:808",
}

response = requests.get("http://www.baidu.com",proxies=proxies)
print(response.text)
```

也可以通过本地环境变了HTTP_PROXY和HTTPS_PROXY来配置代理：

```python
export HTTP_PROXY="http://12.34.56.79:9527"
export HTTPS_PROXY="https://12.34.56.79:9527"
```

### 私密代理验证（特定格式）和web客户端验证(auth参数)

urllib2这里的做法比较复杂，requests只需要一步：

#### **私密代理**

```python
import requests

#如果代理需要使用HTTP Basic Auth ,可以使用下面这种格式
proxy = {
    "http":"username:passwd@IP:port"
}
response = requests.get("http://www.baidu.com",proxies = proxy)
print(response.text)
```

#### web客户端验证

```python
import requests
auth =("test",'123456')
response = requests.get('http://192.168.16.12',auth = auth)
print(response.text)
```

urllib2泪奔

### Cookie和Session

#### cookie

如果一个响应中包含了cookie，那么我们可以利用cookies参数拿到；

```python
import requests

response = requests.get("http://www.baidu.com")

#返回CookieJar对象：
cookiejar = response.cookies

#将cookiejar转为字典
cookiedict = requests.utils.dict_from_cookiejar(cookiejar)

print(cookiejar)
print(cookiedict)
```

运行结果：

```python
<RequestsCookieJar[<Cookie BDORZ=27315 for .baidu.com/>]>
{'BDORZ': '27315'}
```

#### Sission

在requests里。session对象是一个非常常用的对象，这个对象代表一次用户会话：从客户端浏览器连接服务器开始，到客户端浏览器与服务器断开。

会话能让我们在跨域请求时候保持某些参数，比如在同一个session实例发出的所以请求之间保持cookie.

#### 实现人人网登录

```python
import requests

#1.创建session对象，可以保持Cookie值
session = requests.session()

#2.处理headers
headers = {
    "User-Agent":"baiduspider"
}

#3.需要登录的用户名和密码

data = {"email":'yourmail',"password":'1234545'}

#4.发送附带用户名和密码的请求，并获取登录后的Cookie值，保持在session里
session.post("http://www.renren.com/PLogin.do",data=data)

#5.session包含用户登录后的cookie值，可以直接访问那些登录后才能访问的页面
response = session.get("http://www.renren.com/410043129/profile")

#6.打印响应内容
print(response.text)

```

### 处理HTTPS请求SSL证书验证

Requests也可以为HTTPS请求验证证书：

- 要想检查某个主机的SSL证书，你可以使用verify参数（也可以不写）

```python
import requests
response = requests.get("https://www.baidu.com",verify = True)
print(response.text)
```

- 如果SSL证书验证不通过，或者不信任服务器的安全证书，则会报出SSLError，据说 12306 证书是自己做的：

来试一下：

```python
import requests
response = requests.get("https://www.12306.cn/mormhweb/")
print response.text
```

`SSLError: ("bad handshake: Error([('SSL routines', 'ssl3_get_server_certificate', 'certificate verify failed')],)",)`

**如果我们想跳过 12306 的证书验证，把 verify 设置为 False 就可以正常请求了。**

```python
r = requests.get("https://www.12306.cn/mormhweb/", verify = False)
```











