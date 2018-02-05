# 1正则表达式re模块

## 为什么要学正则表达式

实际上爬虫一共就4个主要步骤 ：

```wiki
1.明确目标（要知道你准备在哪个范围或者网站去搜索）
2.爬（将所有的网站内容全部爬下来）
3.取（去掉对我们没用户的数据）
4.处理数据（按照我们想要的方式存储和使用）
```

我们在昨天的案例里实际上省略了第3步，也就是“取” 的步骤。因为我们down下了的数据是全部的网页，这些数据很庞大并且很混乱，大部分的东西是我们不关心的，因此我们需要将之按照我们的需求来过滤和匹配来。

那么对于文本的过滤或者规则的匹配，最强大的就是正则表达式，是Python爬虫世界里必不可少的神兵利器。

## 什么是正则表达式

正则表达式，又称规则表达式，通常被用来检索、替换那些符合某个模式(规则)的文本。

正则表达式是对字符串操作的一种逻辑公式，就是用事先定义好的一些特定字符、及这些特定字符的组合，组成一个“规则字符串”，这个“规则字符串”用来表达对字符串的一种过滤逻辑。

给定一个正则表达式和另一个字符串，我们可以达到如下的目的：

> - 给定的字符串是否符合正则表达式的过滤逻辑（“匹配”）；
> - 通过正则表达式，从文本字符串中获取我们想要的特定部分（“过滤”）。



![2018-02-01 12-24-56](/home/python/Documents/笔记/python/img/2018-02-01 12-24-56.png)

### 正则表达式匹配规则：

![5.2](/home/python/Documents/笔记/python/img/5.2.png)

# python的re模块

在Python中，我们可以使用内置的re模块来使用正则表达式。

有一点需要特别注意的是，正则表达式使用特殊字符进行转义，所以如果我们要使用原始字符串只需要加一个r前缀：

```python
r'baidu\t\.\tpython'
```

## re模块的一般使用步骤如下：

1.使用compile()函数将正则表达式的字符串编译为一个Pattern对象

2.通过Pattern对象提供的一系列方法对文本进行匹配查找，获得匹配结果，一个Match对象。

3.最后使用Match对象提供的属性和方法获得信息，根据需要进行其他的操作



## compile函数

compile函数用于编译正则表达式，生成一个Pattern对象，他的一般使用形式如下：

```python
import re

#将正则表达式编译成Pattern对象
pattern = re.compile(r'\d+')
```

在上面，我们已经将一个正则表达式编译成Pattern对象，接下来，我们就可以利用pattern的一系列方法对文本进行匹配和查找了。

Pattern对象的一些常用方法主要有：

```wiki
match方法：从起始位置开始查找，一次匹配
search方法：从任何位置开始查找，一次匹配
findall方法：全部匹配，返回列表
finditer方法：全部匹配，返回迭代器
split方法：分割字符串，返回列表
sub方法：替换
```

### match方法：

match方法用于查找字符串的头部（也可以指定起始位置），它是一次匹配，只要找到了一个匹配的结果就返回，而不是查找所以匹配的结果。他的一般使用形式如下：

match(string[,post[,endpos]])

其中,string是待匹配的字符串，pos和endpos是可选参数，指定字符串的起始和终点位置，默认值分别是0和len(字符串长度。)因此，当你不指定pos和endpos时，match方法默认匹配字符串的头部。

当匹配成功时，返回一个match对象，如果没有匹配上，则返回None

```python
In [3]: pattern = re.compile(r'\d+') #用于匹配至少一个数字

In [4]: m = pattern.match('one12twotheree34four') #查找头部，没有匹配

In [5]: print(m)
None

In [6]: m = pattern.match('one12twothree34four',2,10)#从'e'的位置开始匹配，没有匹配

In [7]: print(m)
None

In [8]: m = pattern.match('one12twothree34four',3,10) #从'1'的位置开始匹配。正好匹配

In [9]: print(m)	#返回一个match对象
<_sre.SRE_Match object; span=(3, 5), match='12'>

In [10]: m.group(0) #可以省略0
Out[10]: '12'

In [11]: m.start(0)
Out[11]: 3

In [12]: m.end(0)
Out[12]: 5

In [13]: m.span(0)
Out[13]: (3, 5)
```

在上面，当匹配成功时返回一个Match对象，其中：

- group([grouup1,....]) 方法用于获得一个或多个分组匹配的字符串，当要获得整个匹配的子串时，可直接使用group()或group(0)
- start([group]) 方法用于获取分组匹配的子串在整个字符串中的起始位置(子串第一个字符的索引)，参数默认值为0;
- end([group]) 方法用于获取分组匹配的子串在整个字符串中的结束位置(子串最后一个字符串的索引+1),参数默认值为0'；
- span([group]) 方法返回(start(group),end(group))

再看看一个例子：

```python
In [1]: import re

In [2]: pattern = re.compile(r'([a-z]+) ([a-z]+)',re.I) #re.I表示忽略大小写

In [3]: m = pattern.match('Hello World Wide Web')

In [4]: print(m)	#匹配成功，返回一个Match对象
<_sre.SRE_Match object; span=(0, 11), match='Hello World'>

In [5]: m.group(0)	#返回匹配成功的整个子串
Out[5]: 'Hello World'

In [6]: m.span(0)	#返回匹配成功的整个子串的索引
Out[6]: (0, 11)

In [7]: m.group(1)	#返回第一个分组匹配成功的子串
Out[7]: 'Hello'

In [8]: m.span(1)	#返回第一个分组匹配成功的子串的索引
Out[8]: (0, 5)

In [9]: m.group(2)	#返回第二个分组匹配成功的子串
Out[9]: 'World'

In [10]: m.span(2)# 返回第二个分组匹配成功的子串的索引
Out[10]: (6, 11)

In [11]: m.groups()#等价与(m.group(1),m.group(2),...)
Out[11]: ('Hello', 'World')
    
In [16]: m.group(3) #不存在第三个分组
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
<ipython-input-16-71a2c7935517> in <module>()
----> 1 m.group(3)

IndexError: no such group

```

### search方法

search方法用于查找字符串的任何位置，他也是一次匹配，只要找到了一个匹配的结果就返回，而不是查找所有匹配的结果，他的一般使用形式如下：

```wiki
search(string[,pos[,endpos]])
```

其中，string是待匹配的字符串，pos和endpos是可选参数，指定字符串的起始和终点位置，默认值分别是0和len(字符串长度)

当匹配成功时，返回一个Match对象，如果没有匹配上，则返回None

例子：

```python
In [1]: import re

In [2]: pattern = re.compile('\d+')

In [3]: m = pattern.search('one12twothree34four') #这里如果使用match方法则不匹配

In [4]: m
Out[4]: <_sre.SRE_Match object; span=(3, 5), match='12'>

In [5]: m.group()
Out[5]: '12'

In [6]: m = pattern.search('one12twothree34four',10,30) #指定字符串区间

In [7]: m
Out[7]: <_sre.SRE_Match object; span=(13, 15), match='34'>

In [8]: m.group()
Out[8]: '34'

In [9]: m.span()
Out[9]: (13, 15)
```

再来看一个例子：

```python
# _*_ coding:utf-8 _*_
#__author__ :choupiMao
import re

#将正则表达式编译成Pattern对象
pattern = re.compile(r'\d+')
#使用search()查找匹配的子串，不存在匹配的子串时将返回None
#这里使用match()无法成功匹配
m = pattern.search('hello 123456 789')
if m:
    #使用match获得分组信息
    print('matching string:',m.group())
    #起始位置和结束位置
    print('position:',m.span())

    #结果：
('matching string:', '123456')
('position:', (6, 12))
```

### findall方法

上面的match和search方法都是一次匹配，只要找到了一个匹配的结果就返回，然而，在大多数时候，我们需要搜索整个字符串，获得匹配的结果。

findall()使用形式如下

```wiki
findall(string[,pos[,endpos]])
```

其中，string是待匹配的字符串，pos 和 endpos 是可选参数，指定字符串的起始和终点位置，默认值分别是 0 和 len (字符串长度)。

findall 以列表形式返回全部能匹配的子串，如果没有匹配，则返回一个空列表。

```python
import re
pattern = re.compile(r'\d+') #查找数字

result1 = pattern.findall('hello 123456 789')

result2 = pattern.findall('one1two2three3four4', 0, 10)

print(result1)
print(result2)

结果为：
['123456', '789']
['1', '2']
```

例子2：

```python
import re

#re模块提供一个方法叫compile模块，提供我们输入一个匹配的规则
#然后然后一个pattern实例，我们根据这个规则去匹配字符串
pattern = re.compile(r'\d+\.\d*')

#通过pattern.findall()能够全部匹配我们得到的字符串
result = pattern.findall("123.14574,'bigcat',327197, 2.14")

#findall以列表形式 返回全部能匹配的子串给result
for item in result:
    print(item)
   #结果
123.14574
2.14
```

### finditer方法

finditer方法的行为跟findall的行为类似，也是搜索整个字符串，获得所以匹配的结果，但他返回一个序列，访问每一个匹配结果（Match对象）的迭代器。

看看例子：

```python
import re

pattern = re.compile(r'\d+')

result_iter1 = pattern.finditer('hello 123456 789')
result_iter2 = pattern.finditer('one1two2three3four4',0,10)

print(type(result_iter1))
print(type(result_iter2))

print('result1')

for m1 in result_iter1: #m1是Match对象
    print('matching string: {}, position: {}'.format(m1.group(), m1.span()))

print 'result2...'
for m2 in result_iter2:
    print('matching string: {}, position: {}'.format(m2.group(), m2.span()))

```

执行结果：

```python
<type 'callable-iterator'>
<type 'callable-iterator'>
result1
matching string: 123456, position: (6, 12)
matching string: 789, position: (13, 16)
result2...
matching string: 1, position: (3, 4)
matching string: 2, position: (7, 8)
```

### split方法

split方法按照能够匹配的子串将字符串分割后返回列表，他的使用形式如下：

```wiki
split(string[,maxsplit])
```

其中，maxsplit用于指定最大分割次数，不指定将全部分割。

例子：

```python
import re

p = re.compile(r'[\s\,\;]+')

print(p.split('a,b;; c  d'))

#结果
['a', 'b', 'c', 'd']

```

### sub方法

sub方法用于替换。他的使用形式如下：

```wiki
sub(repl,string[,count])
```

其中，repl可以是字符串也可以是一个函数：

- 如果repl是字符串，则会使用repl去替换字符串每一个匹配的子串，并返回替换后的字符串，另外，repl还可以使用id的形式来引用分组，但不能使用编号0;
- 如果repl是函数，这个方法应当只接受一个参数(Match对象)，并返回一个字符串用于替换（返回的字符串中不能再引用分组）
- count用于指定最多替换次数，不指定时全部替换。

例子：

```python
import re

p = re.compile(r'(\w+) (\w+)') # \w = [a-zA-Z 0-9]
s = 'hello 123, hello 456'

print(p.sub(r'hello world',s)) #使用'hello world 替换hello 123 和hello 456
print(p.sub(r'\2 \1',s))#引用分组

def func(m):
    return 'h1'+' '+ m.group(2)

print(p.sub(func,s))
print(p.sub(func,s,1)) #最多替换一次
```

执行结果：

```wiki
hello world, hello world
123 hello, 456 hello
h1 123, h1 456
h1 123, hello 456
```

### 匹配中文

在某些情况下，我们想要匹配文本中的汉字，有一点需要注意的是，中问的unicode编码范围主要在[u4e00-u9fa5]，这里说主要是因为这个范围并不完整，比如没有包括全角（中文）标点，不过在大部分情况下应该是够用的。

假设现在想把字符串title = u'你好,hello,世界'中的中文提取出来，可以这么做：

```python
import re
title = u'你好，hello，世界'
pattern = re.compile(ur'[\u4e00-\u9fa5]+')
result = pattern.findall(title)
print(result)
```

注意到，我们在正则表达式前面加上了两个前缀ur,其中r表示使用原始字符，u表示unicode字符串

执行结果：

```python
[u'\u4f60\u597d', u'\u4e16\u754c']
```

#### 注意：贪婪模式与非贪婪模式

1.贪婪模式：在整个表达式匹配成功的前提下，尽可能多的匹配(*);

2.非贪婪模式:在整个表达式匹配成功的前提下，尽可能少的匹配(?);

3.**Python里数量词默认是贪婪的**



示例一：源字符串：abbbc

- 使用贪婪的数量词的正则表达式ab*,匹配结果：abbb。
  - 决定了尽可能多匹配b,所以a后面的所以b都出现了。
- 使用非贪婪的数量词的正则表达式ab*?，匹配结果是：a
  - 即使前面有*,但是?决定了尽可能少匹配b，所以没有b



实例二：源字符串：`aa<div>test1</div>bb<div>test2</div>cc`

- 使用贪婪的数量词的正则表达式：<div>.*</div>
- 匹配结果：<div>test1</div>bb<div>test2</div>

这里采用的是贪婪模式，在匹配到第一个“</div>”时已经可以使整个表达式匹配成功，但是由于采用的是贪婪模式，所以仍然要向右尝试匹配，查看是否还有更长的可以成功匹配的子串，匹配到第二个"</div>" 后，向右在没有可以成功匹配的子串，匹配结束，匹配结果为"<div>test1</div>bb<div>test2</div>"

- 使用非贪婪的数量词的正则表达式：<div>.*?</div>
- 匹配结果：<div>test1</div>

 













