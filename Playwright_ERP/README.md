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

Playwright_ERP/
├── 📁 Playwright_ERP/                   # 主要测试项目
│   ├── 📄 conftest.py                  # 全局测试配置和fixture
│   ├── 📄 pytest.ini                   # Pytest 配置文件
│   ├── 📄 requirements.txt             # Python 依赖包列表
│   ├── 🚀 run.sh                       # 基础测试运行脚本
│   ├── 🚀 run_all_tests.sh             # 完整测试运行脚本（推荐）
│   ├── 📁 tests/                       # 测试用例目录
│   │   ├── 📁 login/                   # 登录功能测试模块
│   │   ├── 📁 role/                    # 角色管理测试模块
│   │   └── 📁 user/                    # 用户管理测试模块
│   ├── 📁 playwright文档/              # 学习文档和示例
│   ├── 📁 screenshots/                 # 自动生成
│   ├── 📁 test_recordings/             # 自动生成
│   ├── 📁 test_log/                    # 自动生成
│   ├── 📁 allure-results/              # 自动生成
│   └── 📁 allure-report/               # 自动生成
├── 📁 playwright文档/                   # 学习文档和示例
│   ├── 📄 UI自动化这么玩简直绝了~香迷糊了.md
│   ├── 📄 第一篇 Playwright 控件查找及定位.md
│   ├── 📄 第二篇 Playwright操作元素.md
│   ├── 📄 第三篇 处理对话框和弹窗.md
│   ├── 📄 第四篇 等待机制与元素状态检查.md
│   ├── 📄 第五篇 表单处理与文件上传下载.md
│   ├── 📄 第六篇 鼠标与键盘操作.md
│   ├── 📄 第七篇 截图与录屏功能.md
│   ├── 📄 第八篇 网络请求拦截与监控.md
│   ├── 📄 第九篇 调试技巧与最佳实践.md
│   └── 📁 源码/                        # 示例源码和工具
│       ├── 📄 play_with_fun.py        # 实用工具脚本
│       └── 📁 测试工程师必备：智能清理需求文档/
├── 📄 README.md                        # 项目说明文档（本文件）
├── 📄 .gitignore                       # Git 忽略规则
└── 📁 venv/                            # Python 虚拟环境（已忽略）
```

### 📋 重要文件说明

| 文件/目录 | 作用 | 重要性 |
|-----------|------|--------|
| `conftest.py` | 全局测试配置，包含浏览器、登录等fixture | ⭐⭐⭐⭐⭐ |
| `pytest.ini` | Pytest运行配置，测试路径、标记等 | ⭐⭐⭐⭐ |
| `requirements.txt` | Python依赖包列表 | ⭐⭐⭐⭐⭐ |
| `run_all_tests.sh` | 一键运行脚本，推荐使用 | ⭐⭐⭐⭐ |
| `tests/` | 所有测试用例的根目录 | ⭐⭐⭐⭐⭐ |
| `screenshots/` | 自动截图保存目录 | ⭐⭐⭐ |
| `test_log/` | 测试执行日志目录 | ⭐⭐⭐ |
| `allure-results/` | Allure测试结果原始数据 | ⭐⭐⭐⭐ |

## 🚀 快速开始

### 1️⃣ 克隆项目
```bash
git clone <repository-url>
```
```bash
cd Playwright_Study
```

### 2️⃣ 从克隆到运行（Mac M2 / Python 3.9）
- 建议使用虚拟环境，避免系统环境依赖冲突。
- 如果尚未安装 Homebrew（用于安装 Allure CLI），请根据需要自行安装。

步骤：
1. 进入测试项目目录：
```bash
cd Playwright_Study_week1
```
2. 创建并激活虚拟环境（推荐使用 .venv 目录）：
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
3. 升级 pip（可选，但推荐）：
```bash
pip install -U pip
```
4. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```
5. 安装 Playwright 浏览器（确保使用同一解释器执行）：
```bash
python3 -m playwright install
```
6. 安装 Allure 命令行工具（用于生成/查看报告，若不安装则仅跳过报告生成）：
```bash
brew install allure
```
7. 运行一键测试脚本：
```bash
bash run_all_tests.sh
```

验证（可选）：
- 确认 pytest 指向虚拟环境：
```bash
which pytest
```
- 确认已安装 Playwright 包：
```bash
python3 -m pip show playwright
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

#### 📋 系统要求
- Python: 3.9（Mac M2 建议使用 python3 与虚拟环境）
- 操作系统: macOS、Windows、Linux
- 浏览器: Chromium/Chrome、Firefox、WebKit（通过 `python3 -m playwright install` 安装）

#### 🔨 手动安装步骤（与快速开始等效）
1. 创建虚拟环境：
```bash
python3 -m venv .venv
```
2. 激活虚拟环境（macOS/Linux）：
```bash
source .venv/bin/activate
```
3. 安装依赖：
```bash
pip install -r requirements.txt
```
4. 安装 Playwright 浏览器：
```bash
python3 -m playwright install
```
5. 安装 Allure CLI（macOS）：
```bash
brew install allure
```
6. 运行测试：
```bash
bash run_all_tests.sh
```

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

### 👥 角色管理测试

#### 功能覆盖
- **角色创建**: 测试新增角色的完整流程
- **角色列表**: 验证角色列表的显示和数据
- **角色搜索**: 验证搜索功能的准确性
- **数据验证**: 确保操作结果的正确性
- **UI交互**: 测试弹窗、表单、按钮等UI元素

### 🎯 测试架构设计

#### Fixture 设计模式
- **Session 级别**: 浏览器实例，整个测试会话共享
- **Function 级别**: 页面实例，每个测试独立
- **登录状态复用**: 避免重复登录，提高测试效率
- **资源自动清理**: 确保测试环境的干净

#### 元素定位策略
- **语义化定位**: 优先使用 `get_by_role`、`get_by_text` 等语义化方法
- **CSS选择器**: 使用稳定的CSS类名和属性
- **XPath定位**: 复杂场景下的精确定位
- **组合定位**: 多种定位方法结合使用，提高稳定性

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

## 🎯 最佳实践

### 🔧 测试编写最佳实践

#### 1. 元素定位原则
```python
# ✅ 推荐：语义化定位
page.get_by_role("button", name="登录")
page.get_by_text("新增角色")
page.get_by_placeholder("请输入用户名")

# ⚠️ 谨慎使用：CSS选择器
page.locator(".ant-btn-primary")

# ❌ 避免：脆弱的定位
page.locator("body > div:nth-child(3) > div > button")
```

#### 2. 等待策略
```python
# ✅ 推荐：智能等待
expect(page.locator("#element")).to_be_visible()

# ✅ 网络等待
page.wait_for_load_state("networkidle")

# ⚠️ 谨慎使用：固定等待
page.wait_for_timeout(1000)  # 仅在必要时使用
```

#### 3. 数据管理
```python
# ✅ 推荐：动态数据
role_name = f"auto_{datetime.now().strftime('%H%M%S')}"

# ✅ 测试数据隔离
@pytest.fixture
def test_data():
    return {"username": "test_user", "password": "test_pass"}
```

### 🚀 性能优化

#### 1. 浏览器配置优化
```python
# 禁用图片加载（提高速度）
context = browser.new_context(
    viewport={"width": 1280, "height": 800},
    ignore_https_errors=True,
    # 可选：禁用图片
    # bypass_csp=True
)
```

#### 2. 并行测试
```bash
# 并行运行测试（提高效率）
pytest -n auto  # 自动检测CPU核心数
pytest -n 4     # 指定4个进程
```

#### 3. 测试分组
```bash
# 按标记运行
pytest -m smoke      # 只运行冒烟测试
pytest -m "not slow" # 排除慢速测试
```

### 🛡️ 稳定性保障

#### 1. 重试机制
```python
# pytest.ini 配置
[tool:pytest]
addopts = --reruns 2 --reruns-delay 1
```

#### 2. 异常处理
```python
try:
    element = page.wait_for_selector("#element", timeout=5000)
    element.click()
except TimeoutError:
    logger.error("元素未找到，进行截图")
    page.screenshot(path="error.png")
    raise
```

## 🔧 故障排除

### 🐛 常见问题及解决方案

#### 1. 浏览器启动失败
```bash
# 问题：浏览器无法启动
# 解决：重新安装浏览器
python -m playwright install --force

# 检查浏览器版本
python -m playwright --version
```

#### 2. 元素定位失败
```python
# 问题：元素找不到
# 解决：添加调试信息
print(f"页面URL: {page.url}")
print(f"页面标题: {page.title()}")
page.screenshot(path="debug.png")

# 检查元素是否存在
if page.locator("#element").count() > 0:
    print("元素存在")
else:
    print("元素不存在")
```

#### 3. 测试超时
```python
# 问题：测试执行超时
# 解决：调整超时设置
pytest.ini:
timeout = 300  # 5分钟超时

# 或在代码中设置
page.set_default_timeout(30000)  # 30秒
```

#### 4. 网络问题
```bash
# 问题：网络连接失败
# 解决：检查目标服务
curl http://localhost:8080/user/login

# 或在测试中添加网络检查
page.goto("http://localhost:8080", wait_until="networkidle")
```

### 📊 调试技巧

#### 1. 调试模式运行
```bash
# 有头模式 + 慢速执行
pytest --headed --slowmo 1000

# 调试模式（暂停执行）
pytest --pdb
```

#### 2. 元素高亮
```python
# 高亮显示元素
element = page.locator("#button")
element.highlight()
element.click()
```

#### 3. 浏览器开发者工具
```python
# 打开开发者工具
page.pause()  # 暂停执行，手动调试
```

### 🔍 日志分析

#### 1. 日志级别配置
```python
# 详细日志
logging.basicConfig(level=logging.DEBUG)

# 只显示错误
logging.basicConfig(level=logging.ERROR)
```

#### 2. 自定义日志
```python
import logging
logger = logging.getLogger(__name__)

logger.info("测试开始执行")
logger.warning("发现潜在问题")
logger.error("测试执行失败")
```

## 🚀 CI/CD 集成

### 🔄 GitHub Actions 示例

```yaml
name: Playwright Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install
    - name: Run tests
      run: pytest --alluredir=allure-results
    - name: Generate report
      run: allure generate allure-results -o allure-report
    - name: Deploy report
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./allure-report
```

### 🐳 Docker 支持

```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.49.0-focal

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["pytest", "--alluredir=allure-results"]
```

## 📈 项目扩展

### 🔮 未来计划

- [ ] **API 测试集成**: 添加接口测试支持
- [ ] **移动端测试**: 支持移动设备测试
- [ ] **数据库验证**: 集成数据库检查
- [ ] **性能测试**: 添加性能监控
- [ ] **可视化测试**: 集成视觉回归测试

### 🛠️ 技术栈扩展

- **API 测试**: requests + pytest
- **数据库**: SQLAlchemy + pytest-postgresql
- **性能测试**: Lighthouse + pytest-benchmark
- **可视化测试**: Percy + Playwright

## ❓ 常见问题 (FAQ)

### 🤔 测试相关问题

**Q: 为什么测试运行很慢？**
A: 可以尝试以下优化：
- 使用无头模式：`pytest --headless`
- 并行运行：`pytest -n auto`
- 禁用录屏：修改 `conftest.py` 中的录屏配置

**Q: 测试失败时如何调试？**
A: 推荐的调试步骤：
1. 查看失败截图：`screenshots/` 目录
2. 检查测试日志：`test_log/` 目录
3. 使用有头模式：`pytest --headed --slowmo 1000`
4. 添加断点：`page.pause()`

**Q: 如何添加新的测试模块？**
A: 按照以下步骤：
1. 在 `tests/` 下创建新目录
2. 添加 `__init__.py` 文件
3. 创建 `test_*.py` 测试文件
4. 可选：添加模块专用的 `conftest.py`

### 🔧 环境相关问题

**Q: 浏览器安装失败怎么办？**
A: 尝试以下解决方案：
```bash
# 清理并重新安装
python -m playwright uninstall --all
python -m playwright install

# 如果网络问题，可以设置镜像
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com
```

**Q: 依赖包安装失败？**
A: 建议使用虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install -r requirements.txt
```

**Q: 测试目标服务未启动？**
A: 确保测试目标服务正在运行：
```bash
# 检查服务状态
curl http://localhost:8080/user/login
# 或在浏览器中访问 http://localhost:8080
```

### 📊 报告相关问题

**Q: Allure 报告无法生成？**
A: 检查 Allure 是否正确安装：
```bash
allure --version
# 如果未安装，参考环境配置章节
```

**Q: 报告中没有截图？**
A: 确保测试代码中包含截图逻辑：
```python
allure.attach.file(screenshot_path, name="测试截图", 
                   attachment_type=allure.attachment_type.PNG)
```

## 📝 版本历史

### v1.2.0 (2024-01-XX)
- ✅ 添加角色管理测试模块
- ✅ 完善元素定位策略
- ✅ 优化错误处理和截图功能
- ✅ 更新文档和最佳实践

### v1.1.0 (2024-01-XX)
- ✅ 集成 Allure 测试报告
- ✅ 添加自动截图和录屏
- ✅ 完善日志系统
- ✅ 优化 fixture 设计

### v1.0.0 (2024-01-XX)
- ✅ 基础测试框架搭建
- ✅ 登录功能测试实现
- ✅ Playwright + Pytest 集成
- ✅ 基础文档编写

## 🤝 贡献者

感谢所有为这个项目做出贡献的开发者！

- **熊🐻来个🥬** - 项目创建者和主要维护者

## 📞 联系方式

如果你有任何问题或建议，欢迎通过以下方式联系：

- 📧 **邮箱**: [你的邮箱]
- 💬 **微信**: [你的微信号]
- 🐙 **GitHub**: [你的GitHub链接]

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
