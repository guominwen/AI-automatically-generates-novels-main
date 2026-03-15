# GitHub上传操作手册

## 1. 前置准备
### 1.1 检查Git安装
```cmd
git --version
```
确保已安装Git（Windows系统通常已预装）

### 1.2 配置Git用户名和邮箱（首次使用必须设置）
```cmd
git config --global user.name "您的GitHub用户名"
git config --global user.email "您的注册邮箱"
```

### 1.3 生成Personal Access Token（替代密码）
- 访问 [GitHub Token设置页](https://github.com/settings/tokens)
- 点击 `Generate new token` → 选择 `repo` 权限 → 生成并**立即复制**
- **重要**：Token仅显示一次，请妥善保存

## 2. 本地仓库操作流程
### 2.1 检查当前状态
```cmd
git status
```
- `On branch master`：当前分支为master
- `working tree clean`：无未提交更改
- `Untracked files`：有新文件需要添加

### 2.2 添加文件到暂存区
```cmd
git add .          # 添加所有修改的文件
git add 文件名     # 添加指定文件
```

### 2.3 提交更改
```cmd
git commit -m "描述本次修改内容"
```
- 必须先提交才能创建分支
- 提交信息应简明扼要

### 2.4 推送到GitHub
#### 首次推送（设置跟踪关系）
```cmd
git push -u origin master   # 如果本地是master分支
# 或
git push -u origin main     # 如果本地是main分支
```
- 当提示输入密码时 → **粘贴Personal Access Token**
- `-u origin master` 会设置默认跟踪分支

#### 后续推送（已设置跟踪关系后）
```cmd
git push   # 简化命令
```

## 3. 常见问题解决
### 3.1 错误：src refspec main does not match any
**原因**：本地没有main分支
**解决**：
1. 先执行 `git commit -m "Initial commit"` 创建提交
2. 使用 `git branch` 查看实际分支名
3. 推送对应分支：`git push -u origin master`

### 3.2 认证失败
**原因**：密码错误或权限不足
**解决**：
- 确认使用Personal Access Token而非密码
- 检查Token是否有`repo`权限
- 重新生成Token并重试

### 3.3 分支名称不匹配
**检查当前分支**：
```cmd
git branch
```
- `* master` 表示当前分支是master
- `* main` 表示当前分支是main

**强制使用main分支**：
```cmd
git branch -M main    # 将当前分支重命名为main
git push -u origin main
```

## 4. 实际操作示例
```cmd
# 1. 修改文件后检查状态
git status

# 2. 添加所有更改
git add .

# 3. 提交更改
git commit -m "更新app.py功能"

# 4. 推送至GitHub
git push

# 5. 验证推送成功
# 访问 https://github.com/guominwen/AI-automatically-generates-novels-main
```

## 5. 注意事项
- 不要将敏感信息（如Token）提交到仓库
- 推送前确保已提交所有更改
- Windows系统中路径分隔符为`\`，但Git命令中建议使用`/`
- 中文文件名可能需要特殊处理，建议使用英文命名

> 本手册基于Windows环境编写，适用于AI-automatically-generates-novels-main项目