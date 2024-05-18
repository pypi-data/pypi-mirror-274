# PY92
快速确定学校是否是
* 985
* 211
* 双一流
* 本科
* 民办

# 数据来源
[大学生必备网](https://www.dxsbb.com/news/list_88.html) -> [cn_schools.csv](./data/cn_schools.csv)

如果学校类型有误、遗漏学校，欢迎提交issue。

# 安装

```shell
pip install py92
```
本库仅依赖pandas。

# 示例
前言：
* 如果是，返回1；
* 如果不是，返回0；
* 如果不在清单返回-1。（例如海外院校或者遗漏情况）

先引用库
```python
import py92
```
1. `is_in(name)`
返回学校是否在清单中。
```python
print(py92.is_in("北京大学")) # 1
print(py92.is_in("上海海事大学")) # 1
print(py92.is_in("纽约大学")) # 0
```

2. `is_985`
返回学校是否属于**985**。
```python
print(py92.is_985("北京大学"))  # 1
print(py92.is_985("上海海事大学"))  # 0
print(py92.is_985("纽约大学")) # -1
```

3. `is_211`
返回学校是否属于**211**。

```python
print(py92.is_211("北京大学"))  # 1
print(py92.is_211("上海大学")) # 1
print(py92.is_211("上海海事大学"))  # 0
```

4. `is_db1`
返回学校是否属于**双一流**。

```python
print(py92.is_db1("北京大学"))  # 1
print(py92.is_db1("上海海洋大学")) # 1
print(py92.is_db1("上海海事大学"))  # 0
```

5. `is_university`
返回学校是否属于**本科**。

```python
print(py92.is_university("上海海事大学"))  # 1
print(py92.is_university("上海海事职业技术学院"))  # 0
```


6. `is_public`
返回学校是否属于**公办**。

```python
print(py92.is_public("上海建桥学院"))  # 0
print(py92.is_public("上海海事大学"))  # 1
```

7. `get_highest_label`
获取学校最高的标签。
规则：985>211>双一流>本科>专科

```python
print(py92.get_highest_label("上海交通大学"))  # 985
print(py92.get_highest_label("上海大学"))  # 211
print(py92.get_highest_label("上海海洋大学"))  # 双一流
print(py92.get_highest_label("上海海事大学"))  # 本科
print(py92.get_highest_label("上海海事职业技术学院"))  # 专科
```

8. `get_label`
返回学校所有标签。

```python
print(py92.get_label("上海海事大学"))
# {'name': '上海海事大学', '985': 0, '211': 0, '双一流': 0, '本科': 1, '公办': 1}
```

9. `is_[xxx]s`
返回学校组是否属于**xxx**。
输入：`[name1, name2, name3]`
```python
schools = ["北京大学","上海海事大学","纽约大学"]
print(py92.is_ins(schools)) # [1, 1, 0]
```