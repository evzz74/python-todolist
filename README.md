# Todo List - Google 风格待办事项应用

一个使用 Python 和 CustomTkinter 构建的现代化待办事项管理应用，采用 Google Material Design 风格。

## 功能特性

- 添加、删除待办事项
- 标记任务为已完成/未完成
- 自动保存数据到本地 JSON 文件
- 浅色/深色主题切换
- 清除所有已完成任务
- 实时统计任务数量
- 现代化的 Google Material Design UI

## 安装

1. 确保已安装 Python 3.7 或更高版本

2. 安装依赖包：
```bash
pip install -r requirements.txt
```

## 使用

### 方式一：直接运行 Python 脚本

运行应用程序：
```bash
python todolist.py
```

### 方式二：使用打包的 exe 文件

如果你已经有打包好的 `TodoList.exe` 文件，直接双击运行即可。

## 打包成 exe 文件

如果你想自己打包应用为独立的可执行文件：

### 方法一：使用自动化脚本（推荐）

直接运行打包脚本：
```bash
build.bat
```

脚本会自动完成以下步骤：
1. 安装所需依赖
2. 清理旧的构建文件
3. 使用 PyInstaller 打包应用

打包完成后，exe 文件位于 `dist\TodoList.exe`

### 方法二：手动打包

1. 安装 PyInstaller：
```bash
pip install pyinstaller
```

2. 执行打包命令：
```bash
pyinstaller --name="TodoList" --onefile --windowed --noconsole todolist.py
```

3. 打包完成后，在 `dist` 目录下找到 `TodoList.exe`

### 打包参数说明

- `--name="TodoList"` - 设置应用名称
- `--onefile` - 打包成单个 exe 文件
- `--windowed` - 不显示命令行窗口（GUI 应用）
- `--noconsole` - 隐藏控制台窗口
- `--clean` - 清理临时文件

## 操作说明

- **添加任务**：在输入框中输入任务内容，点击"添加"按钮或按 Enter 键
- **完成任务**：点击任务前的复选框来标记任务完成/未完成
- **删除任务**：点击任务右侧的 "✕" 按钮删除该任务
- **清除已完成**：点击底部的"清除已完成"按钮删除所有已完成的任务
- **切换主题**：点击"切换主题"按钮在浅色和深色模式之间切换

## 数据存储

应用程序会自动将待办事项保存到 `todos.json` 文件中，每次启动时会自动加载之前的数据。

## 技术栈

- Python 3.7+
- CustomTkinter (现代化 UI 框架)
- JSON (数据持久化)

## 截图

应用界面采用 Google Material Design 风格，包含：
- 蓝色主题色 (#1a73e8)
- 圆角设计
- 简洁的卡片式布局
- 流畅的交互体验
