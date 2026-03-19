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

### 1.4 推荐：使用GitHub CLI（现代替代方案）
```cmd
# 安装GitHub CLI
winget install --id GitHub.cli

# 登录认证
gh auth login
# 或使用Token登录
gh auth login --with-token <your-token>
```

## 2. 本地仓库操作流程
### 2.1 检查当前状态
```cmd
git status
```
- `On branch main`：当前分支为main（推荐使用main而非master）
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
git push -u origin main   # 推荐使用main分支
```
- 当提示输入密码时 → **粘贴Personal Access Token**
- `-u origin main` 会设置默认跟踪分支

#### 后续推送（已设置跟踪关系后）
```cmd
git push   # 简化命令
# 或使用GitHub CLI
gh repo sync
```

## 3. 项目特定上传建议（AI小说生成项目）
### 3.1 .gitignore文件配置建议
由于本项目包含图片、日志等文件，建议创建`.gitignore`文件：
```
# 忽略日志文件
*.log
nohup.out

# 忽略Python缓存
__pycache__/
*.pyc

# 忽略大型数据文件（如模型文件）
*.bin
*.pth
*.ckpt
*.safetensors

# 忽略临时文件
*.tmp
*.swp

# 忽略IDE配置
.vscode/
.idea/

# 忽略用户配置文件（避免提交敏感信息）
config.json
api_keys.json
.env
```

### 3.2 大文件处理
GitHub单个文件限制为100MB，项目中的图片文件（jpg/目录）通常较小，但如需上传大型文件：
- 使用Git LFS（Large File Storage）
- 或将大型文件上传到其他存储服务（如阿里云OSS、腾讯云COS），在README中提供下载链接

### 3.3 敏感信息保护
- **绝对不要**提交API密钥、Token等敏感信息
- 使用环境变量或配置文件（已添加到.gitignore）
- 项目中涉及的模型API密钥应在本地配置，不在版本控制中

## 4. 常见问题解决
### 4.1 错误：src refspec main does not match any
**原因**：本地没有main分支
**解决**：
1. 先执行 `git commit -m "Initial commit"` 创建提交
2. 使用 `git branch` 查看实际分支名
3. 推送对应分支：`git push -u origin main`

### 4.2 认证失败
**原因**：密码错误或权限不足
**解决**：
- 确认使用Personal Access Token而非密码
- 检查Token是否有`repo`权限
- 重新生成Token并重试
- 尝试使用GitHub CLI：`gh auth login`

### 4.3 分支名称不匹配
**检查当前分支**：
```cmd
git branch
```
- `* main` 表示当前分支是main（推荐）
- `* master` 表示当前分支是master

**强制使用main分支**：
```cmd
git branch -M main    # 将当前分支重命名为main
git push -u origin main
```

## 5. 实际操作示例
```cmd
# 1. 创建.gitignore文件（如果不存在）
echo "# AI小说生成项目忽略文件" > .gitignore
echo "*.log" >> .gitignore
echo "nohup.out" >> .gitignore
echo "__pycache__/" >> .gitignore

# 2. 修改文件后检查状态
git status

# 3. 添加所有更改
git add .

# 4. 提交更改
git commit -m "更新app.py功能，添加.gitignore配置"

# 5. 推送至GitHub
git push

# 6. 验证推送成功
# 访问 https://github.com/guominwen/AI-automatically-generates-novels-main
```

## 6. 注意事项
- 不要将敏感信息（如Token、API密钥）提交到仓库
- 推送前确保已提交所有更改
- Windows系统中路径分隔符为`\`，但Git命令中建议使用`/`
- 中文文件名可能需要特殊处理，建议使用英文命名
- 项目特定：AI模型相关文件（如app各大模型/目录）应避免提交大型模型文件
- 图片文件（jpg/目录）可以正常提交，但注意文件大小

## 7. 从GitHub拉取最新代码
### 7.1 基本拉取操作
```cmd
# 拉取远程仓库的最新更改（当前分支）
git pull origin main

# 或简写形式
git pull
```

### 7.2 处理拉取冲突
当本地有未提交的更改时，可能会出现冲突：
```cmd
# 方案1：先提交本地更改再拉取
git commit -m "保存本地更改"
git pull origin main

# 方案2：暂存本地更改再拉取
git stash
git pull origin main
git stash pop

# 方案3：强制覆盖本地更改（谨慎使用！）
git fetch origin
git reset --hard origin/main
```

### 7.3 使用GitHub CLI拉取
```cmd
# 同步本地仓库与远程仓库
gh repo sync

# 或使用标准Git命令
gh auth login  # 确保已登录
git pull origin main
```

### 7.4 项目特定拉取建议
- **AI小说生成项目**：拉取后建议检查以下文件是否更新：
  - `app.py` 和 `app各大模型/` 目录下的模型配置文件
  - `static/` 目录下的前端脚本
  - `templates/` 目录下的HTML模板
- 如果拉取后出现依赖问题，运行：
  ```cmd
  pip install -r requirements.txt
  ```

### 7.5 理解拉取结果信息
当执行 `git pull origin master` 后看到：
```
From https://github.com/guominwen/AI-automatically-generates-novels-main
 * branch            master     -> FETCH_HEAD
Already up to date.
```
**这表示成功！** 不是错误信息：
- `* branch master -> FETCH_HEAD`：成功拉取了远程的master分支
- `Already up to date.`：本地已经是最新版本，没有需要合并的新提交
- 这是正常的成功消息，说明您的代码已经是最新的

如果看到类似信息，请放心，您的代码已同步到最新版本。

> 本手册基于Windows环境编写，适用于AI-automatically-generates-novels-main项目
> 更新日期：2026年3月15日
