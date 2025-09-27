# 🎭 Playwright 自动化测试学习项目

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.49.0-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-8.3.4-orange.svg)](https://pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.13.5-red.svg)](https://docs.qameta.io/allure/)

一个专注于 Playwright 自动化测试学习与实践的项目，包含完整的测试框架、详细的学习文档和丰富的示例代码。

## 📋 目录

- [✨ 项目特性](#-项目特性)
- [📁 项目结构](#-项目结构)
- [🚀 快速开始](#-快速开始)
- [🔧 环境配置](#-环境配置)
- [📖 使用指南](#-使用指南)
- [🧪 测试功能](#-测试功能)
- [📊 测试报告](#-测试报告)
- [📚 学习资源](#-学习资源)
- [🤝 贡献指南](#-贡献指南)

## ✨ 项目特性

### 🎯 核心功能
- **完整的测试框架**：基于 Playwright + Pytest 构建
- **自动化测试**：支持多浏览器、多平台的 UI 自动化测试
- **详细的测试报告**：集成 Allure 生成美观的测试报告
- **截图和录屏**：自动截图、失败截图、测试过程录屏
- **日志记录**：完整的测试执行日志，支持文件和控制台输出

### 🛠️ 技术栈
- **测试框架**：Playwright (跨浏览器自动化)
- **测试运行器**：Pytest (Python 测试框架)
- **报告工具**：Allure (测试报告生成)
- **日志系统**：Python logging (详细日志记录)
- **CI/CD**：支持持续集成和持续部署

### 🎨 测试增强功能
- **Setup/Teardown 管理**：自动化的资源创建和清理
- **元素高亮**：测试过程中高亮显示操作元素
- **多种定位策略**：CSS选择器、XPath、文本内容等
- **异常处理**：完善的错误处理和恢复机制
- **参数化测试**：支持数据驱动测试

## 📁 项目结构

```
Playwright_Study/
├── 📁 Playwright_Study_week1/          # 主要测试项目
│   ├── 📄 pytest.ini                   # Pytest 配置文件
│   ├── 📄 requirements.txt             # Python 依赖包列表
│   ├── 🚀 run.sh                       # 基础测试运行脚本
│   ├── 🚀 run_all_tests.sh            # 完整测试运行脚本（推荐）
│   ├── 📁 tests/                       # 测试用例目录
│   │   ├── 📁 login/                   # 登录功能测试
│   │   │   ├── 📄 test_login.py        # 主要登录测试（增强版）
│   │   │   └── 📄 test_login_1.py      # 基础登录测试
│   │   ├── 📁 role/                    # 角色管理测试
│   │   └── 📁 user/                    # 用户管理测试
│   ├── 📁 screenshots/                 # 测试截图目录
│   ├── 📁 test_recordings/             # 测试录屏目录
│   ├── 📁 test_log/                    # 测试日志目录
│   ├── 📁 allure-results/              # Allure 原始结果
│   └── 📁 allure-report/               # Allure 生成的报告
├── 📁 playwright文档/                   # 学习文档和示例
│   ├── 📄 第一篇 Playwright 控件查找及定位.md
│   ├── 📄 第二篇 Playwright操作元素.md
│   ├── 📄 第三篇 处理对话框和弹窗.md
│   ├── 📄 第四篇 等待机制与元素状态检查.md
│   ├── 📄 第五篇 表单处理与文件上传下载.md
│   ├── 📄 第六篇 鼠标与键盘操作.md
│   ├── 📄 第七篇 截图与录屏功能.md
│   ├── 📄 第八篇 网络请求拦截与监控.md
│   ├── 📄 第九篇 调试技巧与最佳实践.md
│   └── 📁 源码/                        # 示例源码
├── 📄 README.md                        # 项目说明文档
├── 📄 .gitignore                       # Git 忽略规则
└── 📁 venv/                            # Python 虚拟环境（已忽略）
```

## 🚀 快速开始

### 1️⃣ 克隆项目
```bash
git clone <repository-url>
cd Playwright_Study
```

### 2️⃣ 一键安装和运行
```bash
# 进入项目目录
cd Playwright_Study_week1

# 给脚本执行权限
chmod +x run_all_tests.sh

# 一键运行所有测试（推荐）
./run_all_tests.sh
```

脚本会自动完成：
- ✅ 检查依赖环境
- ✅ 清理旧的测试结果
- ✅ 运行所有测试用例
- ✅ 生成 Allure 测试报告
- ✅ 自动打开报告页面

## 🔧 环境配置

### 📋 系统要求
- **Python**: 3.9+ 
- **操作系统**: macOS, Windows, Linux
- **浏览器**: Chrome, Firefox, Safari, Edge

### 🔨 手动安装步骤

#### 1. 创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

#### 2. 安装 Python 依赖
```bash
cd Playwright_Study_week1
pip install -r requirements.txt
```

#### 3. 安装 Playwright 浏览器
```bash
# 安装所有浏览器
python -m playwright install

# 或只安装 Chrome
python -m playwright install chromium
```

#### 4. 安装 Allure 命令行工具
```bash
# macOS (使用 Homebrew)
brew install allure

# Windows (使用 Scoop)
scoop install allure

# 或从官网下载: https://docs.qameta.io/allure/#_installing_a_commandline
```

### 📦 主要依赖包

| 包名 | 版本 | 用途 |
|------|------|------|
| playwright | 1.49.0 | 浏览器自动化核心库 |
| pytest | 8.3.4 | 测试框架 |
| pytest-playwright | 0.6.2 | Playwright 的 Pytest 插件 |
| allure-pytest | 2.13.5 | Allure 报告生成 |
| requests | 2.32.3 | HTTP 请求库 |

完整依赖列表请查看 [`requirements.txt`](Playwright_Study_week1/requirements.txt)

## 📖 使用指南

### 🎯 运行测试的多种方式

#### 方式一：一键运行（推荐）
```bash
cd Playwright_Study_week1
./run_all_tests.sh
```

#### 方式二：基础运行
```bash
cd Playwright_Study_week1
./run.sh
```

#### 方式三：直接使用 Pytest
```bash
cd Playwright_Study_week1

# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/login/test_login.py

# 运行特定测试函数
pytest tests/login/test_login.py::test_login

# 有头模式运行（显示浏览器）
pytest --headed

# 无头模式运行（后台运行）
pytest --headless
```

#### 方式四：生成 Allure 报告
```bash
# 运行测试并生成 Allure 数据
pytest --alluredir=allure-results

# 生成 HTML 报告
allure generate allure-results -o allure-report --clean

# 启动 Allure 服务查看报告
allure serve allure-results
```

### 🎛️ 测试配置选项

#### Pytest 配置 (pytest.ini)
```ini
[tool:pytest]
testpaths = tests
addopts = 
    --strict-markers
    --strict-config
    --alluredir=allure-results
    --clean-alluredir
markers =
    smoke: 冒烟测试
    regression: 回归测试
    login: 登录相关测试
```

#### 浏览器配置选项
```bash
# 指定浏览器
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# 设置浏览器选项
pytest --headed --slowmo 1000  # 有头模式，每步延迟1秒
```

## 🧪 测试功能

### 🔐 登录功能测试

#### 主要测试用例
- **test_login.py**: 增强版登录测试
  - ✅ 完整的 Setup/Teardown 流程
  - ✅ 自动截图和录屏
  - ✅ 详细的日志记录
  - ✅ Allure 报告集成
  - ✅ 元素高亮显示
  - ✅ 异常处理和恢复

#### 测试步骤
1. **环境准备**: 启动浏览器，创建测试上下文
2. **页面导航**: 打开登录页面
3. **数据输入**: 输入公司编号、用户名、密码
4. **操作执行**: 点击登录按钮
5. **结果验证**: 验证页面跳转和元素显示
6. **资源清理**: 关闭页面和浏览器

#### Setup 和 Teardown 流程

```python
# Setup 执行顺序 (测试前准备)
1. 🚀 Session Setup: browser()     - 启动浏览器
2. 🚀 Function Setup: context()    - 创建上下文和录制配置  
3. 🚀 Function Setup: page()       - 创建页面对象
4. 🎯 测试执行: test_login()       - 执行实际测试逻辑

# Teardown 执行顺序 (测试后清理)
5. 🧹 Function Teardown: page()    - 关闭页面
6. 🧹 Function Teardown: context() - 关闭上下文，保存录制
7. 🧹 Session Teardown: browser()  - 关闭浏览器
```

### 📸 截图和录屏功能

#### 自动截图
- **关键步骤截图**: 每个测试步骤自动截图
- **失败截图**: 测试失败时自动截图
- **成功截图**: 测试成功时截图
- **文件命名**: 带时间戳的有意义文件名

#### 视频录制
- **全程录制**: 整个测试过程录制为 WebM 格式
- **自动保存**: 测试结束后自动保存到 `test_recordings/` 目录
- **高质量**: 1280x800 分辨率录制

### 📝 日志系统

#### 日志级别和输出
- **INFO**: 一般信息记录
- **ERROR**: 错误信息记录
- **双重输出**: 同时输出到文件和控制台
- **中文支持**: 完整的中文日志支持

#### 日志文件位置
- **文件路径**: `test_log/test_login.log`
- **格式**: 时间戳 - 模块名 - 级别 - 消息内容

## 📊 测试报告

### 🎨 Allure 报告功能

#### 报告内容
- **测试概览**: 测试执行统计和趋势
- **测试套件**: 按功能模块分组的测试结果
- **测试用例**: 详细的测试步骤和结果
- **附件**: 截图、日志、视频等附件
- **历史趋势**: 测试执行历史和趋势分析

#### 报告特性
- **实时生成**: 测试执行完成后立即生成
- **交互式**: 可点击查看详细信息
- **多媒体**: 支持图片、视频、文本附件
- **分类标签**: 按 Epic、Feature、Story 分类

#### 查看报告
```bash
# 方式一：自动打开（推荐）
./run_all_tests.sh  # 脚本会自动打开报告

# 方式二：手动启动服务
allure serve allure-results

# 方式三：生成静态报告
allure generate allure-results -o allure-report --clean
# 然后打开 allure-report/index.html
```

### 📈 报告示例

#### 测试用例标签
```python
@allure.epic("用户管理系统")
@allure.feature("用户认证") 
@allure.story("用户登录")
@allure.title("登录功能测试")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("login", "authentication", "smoke")
```

#### 测试步骤
```python
with allure.step('打开登录页面'):
    # 测试步骤代码
    
with allure.step('输入用户凭据'):
    # 测试步骤代码
```

## 📚 学习资源

### 📖 文档目录

项目包含完整的 Playwright 学习文档：

1. **[第一篇 Playwright 控件查找及定位](playwright文档/第一篇%20Playwright%20控件查找及定位.md)**
   - CSS 选择器、XPath、文本定位
   - 元素定位最佳实践

2. **[第二篇 Playwright操作元素](playwright文档/第二篇%20Playwright操作元素.md)**
   - 点击、输入、选择操作
   - 元素状态检查

3. **[第三篇 处理对话框和弹窗](playwright文档/第三篇%20处理对话框和弹窗.md)**
   - Alert、Confirm、Prompt 处理
   - 模态框操作

4. **[第四篇 等待机制与元素状态检查](playwright文档/第四篇%20等待机制与元素状态检查.md)**
   - 智能等待策略
   - 元素可见性检查

5. **[第五篇 表单处理与文件上传下载](playwright文档/第五篇%20表单处理与文件上传下载.md)**
   - 表单填写和提交
   - 文件操作

6. **[第六篇 鼠标与键盘操作](playwright文档/第六篇%20鼠标与键盘操作.md)**
   - 复杂交互操作
   - 快捷键操作

7. **[第七篇 截图与录屏功能](playwright文档/第七篇%20截图与录屏功能.md)**
   - 截图策略和配置
   - 视频录制设置

8. **[第八篇 网络请求拦截与监控](playwright文档/第八篇%20网络请求拦截与监控.md)**
   - API 拦截和模拟
   - 网络监控

9. **[第九篇 调试技巧与最佳实践](playwright文档/第九篇%20调试技巧与最佳实践.md)**
   - 调试方法和工具
   - 最佳实践总结

### 🔗 官方资源

- **[Playwright 官方文档](https://playwright.dev/)**
- **[Pytest 官方文档](https://docs.pytest.org/)**
- **[Allure 官方文档](https://docs.qameta.io/allure/)**

## 🤝 贡献指南

### 🌟 如何贡献

1. **Fork 项目**
2. **创建功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **创建 Pull Request**

### 📝 代码规范

- **Python 代码**: 遵循 PEP 8 规范
- **测试命名**: 使用描述性的测试函数名
- **注释**: 添加必要的中文注释
- **文档**: 更新相关文档

### 🐛 问题报告

如果发现问题，请创建 Issue 并包含：
- **问题描述**: 详细描述遇到的问题
- **复现步骤**: 提供复现问题的步骤
- **环境信息**: Python 版本、操作系统等
- **错误日志**: 相关的错误信息

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👨‍💻 作者

**熊🐻来个🥬**

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
