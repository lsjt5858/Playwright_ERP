# Playwright_Study

一个以 Playwright 学习与示例为主的仓库，包含少量可运行脚本与测试。

## 目录结构（关键信息）
- Playwright_Study_week1/
  - run.sh — 一键运行测试并生成/打开 Allure 报告
  - pytest.ini — Pytest 配置（`testpaths = tests`）
  - requirements.txt — Python 依赖
  - tests/
    - test_baidu_kimi.py — 有效的 Playwright UI 示例测试
    - test_baidu.py — 示例测试（当前大多被注释）
- playwright文档/ — 学习文档与源码示例

## 环境准备
1. 创建并激活虚拟环境（可选）
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows 使用 venv\Scripts\activate
   ```
2. 安装依赖
   ```bash
   pip install -r Playwright_Study_week1/requirements.txt
   ```
3. 安装 Playwright 浏览器内核
   ```bash
   python -m playwright install
   ```
4. 安装 Allure 命令行（用于生成/预览报告）
   - macOS: `brew install allure`
   - Windows: `scoop install allure` 或从官网安装包

## 运行测试
- 一键运行（推荐）
  ```bash
  cd Playwright_Study_week1
  ./run.sh
  ```
  脚本会：
  - 执行 `pytest` 发现并运行 `tests/` 下的用例
  - 生成到 `allure-report/`，并通过 `allure serve` 打开本地报告

- 仅运行 Pytest（不生成报告）：
  ```bash
  cd Playwright_Study_week1
  pytest
  ```

## 备注
- 首次运行前请确保已执行 `python -m playwright install`。
- `test_baidu_kimi.py` 使用 `pytest-playwright` 提供的 `page` fixture；如需无头或有头运行可用 `--headed/--headless` 控制。
- 如果没有安装 Allure CLI，可以注释或移除 `run.sh` 中 Allure 相关两行，仅保留 `pytest`。

# Playwright_Study
