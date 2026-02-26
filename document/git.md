<!-- document\git.md -->

# 使用方式
## 更新`.gitignore`后应用
- 现象:更新`.gitignore`后不会立即生效,仍会追踪被"ignored"的文件
- 原因:`.gitignore`只能忽略未被追踪(Untracked)(仍在Git的缓存(index)中)的文件
### 解决方法:
1. 保存并提交当前已有代码,避免误删
2. 清理缓存`git rm -r --cached .`
3. 重新添加文件`git add .`
4. 提交更改`git commit -m "update .gitignore and refresh cache"`