<!-- document\python-basic.md -->

# 基础类型
## 字符串
### Immutable
字符串一旦创建，内容不可修改，改变后实际上是创建了一个新的字符串

### 字符串的 3 种定义方式
1. `' '` 单引号
2. `" "` 双引号
3. `""" """` 三引号

### 转义字符
使用`\`来输入特殊字符
- `\n` 换行
- `\t` 制表符

### 向字符串中插入值
#### f-string
- 评价：最推荐、最流程、可读性最好、性能最高
- 版本：Python 3.6+
- 基本使用方式：在字符串前加一个`f`
- Example：
```
name = "jojo"
episode = 7
message = f"This is {name} episode {episode}."
```
#### `.format` 函数
- 评价：
  - **f-string**前的主流做法。
  - 适合模版复用，对于定义好的含有若干`{}`的字符串模板，在调用时使用原生方法`format()`，按顺序输入参数插入到`{}`中
- Example：
```
template = "User {} has logged on, IP address is {}"
print(template.format("admin", "127.0.0.1"))
```
#### `%` 占位符
- 忽略

