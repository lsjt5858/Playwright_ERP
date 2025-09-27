#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/9/26
# @Description: Login test with enhanced features including screenshots, recording, logging and allure tags

import pytest
import requests
import logging
import os
from datetime import datetime
from playwright.sync_api import Page, expect
import time
import allure

from Playwright_Study_week1.tests.login.test_login_1 import test_login

# ==================== 全局Setup：测试环境初始化 ====================
# 这部分代码在模块加载时执行，属于全局Setup
test_logdir = "test_log"
os.makedirs(test_logdir, exist_ok=True)  # Setup：创建日志目录

# Setup：配置日志系统 - 为整个测试会话准备日志记录功能
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(test_logdir, 'test_login.log'), encoding='utf-8'),  # 文件日志 - 修复路径
        logging.StreamHandler()  # 控制台日志
    ]
)
logger = logging.getLogger(__name__)


# ==================== Session级别的Setup和Teardown ====================
# scope="session" 表示整个测试会话只执行一次Setup和Teardown
@pytest.fixture(scope="session")
def browser(playwright):
    """
    Session级别的浏览器fixture
    Setup: 启动浏览器 -> yield -> Teardown: 关闭浏览器
    执行顺序: 第1个执行Setup，最后1个执行Teardown
    """
    # ========== Session Setup 开始 ==========
    logger.info("🚀 Session Setup: Starting Chrome browser session")
    browser = playwright.chromium.launch(
        channel="chrome", 
        headless=False,
        slow_mo=500  # 添加操作延迟，便于观察
    )
    logger.info("✅ Session Setup完成: 浏览器已启动")
    # ========== Session Setup 结束 ==========
    
    # yield 是分界线：yield前是Setup，yield后是Teardown
    yield browser  # 将浏览器对象传递给依赖的fixture和测试函数
    
    # ========== Session Teardown 开始 ==========
    logger.info("🧹 Session Teardown: Closing browser session")
    browser.close()  # 关闭浏览器，释放系统资源
    logger.info("✅ Session Teardown完成: 浏览器已关闭")
    # ========== Session Teardown 结束 ==========


# ==================== Function级别的Setup和Teardown ====================
# scope="function" 表示每个测试函数都会执行一次Setup和Teardown
@pytest.fixture(scope="function")
def context(browser):
    """
    Function级别的浏览器上下文fixture
    Setup: 创建上下文和录制配置 -> yield -> Teardown: 关闭上下文
    执行顺序: 第2个执行Setup，倒数第2个执行Teardown
    """
    # ========== Function Setup 开始 ==========
    logger.info("🚀 Function Setup: Creating browser context with recording enabled")
    
    # Setup步骤1: 创建录制目录
    record_dir = "test_recordings"
    os.makedirs(record_dir, exist_ok=True)
    
    # Setup步骤2: 生成录制文件名（带时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = f"{record_dir}/login_test_{timestamp}.webm"
    
    # Setup步骤3: 创建浏览器上下文，配置录制参数
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},  # 设置视窗大小
        record_video_dir=record_dir,              # 录制目录
        record_video_size={"width": 1280, "height": 800}  # 录制尺寸
    )
    
    logger.info(f"✅ Function Setup完成: Video recording will be saved to: {video_path}")
    # ========== Function Setup 结束 ==========
    
    # yield 分界线：传递上下文对象给依赖的fixture
    yield context
    
    # ========== Function Teardown 开始 ==========
    logger.info("🧹 Function Teardown: 关闭上下文并保存录制")
    context.close()  # 关闭上下文，自动保存录制的视频文件
    logger.info("✅ Function Teardown完成: Browser context closed, video saved")
    # ========== Function Teardown 结束 ==========


# ==================== Function级别的页面Setup和Teardown ====================
@pytest.fixture(scope="function")
def page(context):
    """
    Function级别的页面fixture
    Setup: 创建页面对象 -> yield -> Teardown: 关闭页面
    执行顺序: 第3个执行Setup，第1个执行Teardown
    """
    # ========== Function Setup 开始 ==========
    logger.info("🚀 Function Setup: Creating new page")
    page = context.new_page()  # 在上下文中创建新页面
    logger.info("✅ Function Setup完成: 页面对象已创建")
    # ========== Function Setup 结束 ==========
    
    # yield 分界线：传递页面对象给测试函数
    yield page
    
    # ========== Function Teardown 开始 ==========
    logger.info("🧹 Function Teardown: 关闭页面")
    page.close()  # 关闭页面，释放页面资源
    logger.info("✅ Function Teardown完成: Page closed")
    # ========== Function Teardown 结束 ==========


"""
==================== Setup和Teardown执行流程说明 ====================

当执行 test_login() 函数时，pytest会按以下顺序执行Setup和Teardown：

📋 完整执行顺序：
1. 🚀 Session Setup:    browser()     - 启动浏览器（整个会话只执行一次）
2. 🚀 Function Setup:   context()     - 创建上下文和录制配置
3. 🚀 Function Setup:   page()        - 创建页面对象
4. 🎯 测试执行:         test_login()  - 执行实际测试逻辑
5. 🧹 Function Teardown: page()       - 关闭页面（最先创建的最后清理）
6. 🧹 Function Teardown: context()    - 关闭上下文，保存录制
7. 🧹 Session Teardown:  browser()    - 关闭浏览器（最后执行）

💡 关键概念：
- Setup: 测试前的准备工作（创建资源、初始化环境）
- Teardown: 测试后的清理工作（释放资源、清理环境）
- yield: pytest fixture的分界线，yield前是Setup，yield后是Teardown
- scope: 控制fixture的生命周期（session > module > class > function）

🔄 依赖关系：
page 依赖 context，context 依赖 browser
所以Setup顺序：browser -> context -> page
Teardown顺序相反：page -> context -> browser
"""

@allure.epic("用户管理系统")
@allure.feature("用户认证")
@allure.story("用户登录")
@allure.title("登录功能测试")
@allure.description("测试用户使用正确的凭据登录系统的完整流程")
@allure.tag("login", "authentication", "smoke", "critical")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "熊🐻来个🥬")
@allure.label("suite", "登录测试套件")
@allure.testcase("TC001", "登录功能测试用例")
def test_login(page: Page):
    """
    登录功能测试
    
    📝 注意：当这个函数被调用时，所有的Setup已经完成：
    ✅ browser fixture已经启动了浏览器
    ✅ context fixture已经创建了上下文和录制配置  
    ✅ page fixture已经创建了页面对象
    
    测试步骤:
    1. 打开登录页面
    2. 输入公司编号
    3. 输入用户名
    4. 输入密码
    5. 点击登录按钮
    6. 验证登录成功
    
    📝 注意：当这个函数执行完毕后，所有的Teardown会自动执行：
    🧹 page fixture会关闭页面
    🧹 context fixture会关闭上下文并保存录制
    🧹 browser fixture会关闭浏览器（如果是最后一个测试）
    """
    logger.info("🎯 开始执行登录测试 - 此时所有Setup已完成")
    
    with allure.step('打开登录页面'):
        logger.info("导航到登录页面")
        page.goto("http://localhost:8080/user/login")
        page.wait_for_load_state("networkidle")
        
        # 截图：登录页面
        screenshot_path = f"screenshots/login_page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs("screenshots", exist_ok=True)
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="登录页面截图", attachment_type=allure.attachment_type.PNG)
        logger.info(f"登录页面截图已保存: {screenshot_path}")
    
    with allure.step('输入公司编号: 001'):
        logger.info("输入公司编号: 001")
        company_input = page.locator(".ant-form-item").first.locator("input")
        company_input.highlight()  # 高亮显示元素
        company_input.fill("001")
        
        # 截图：输入公司编号后
        screenshot_path = f"screenshots/company_filled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="输入公司编号后", attachment_type=allure.attachment_type.PNG)
        logger.info("公司编号输入完成")
    
    with allure.step('输入用户名: admin'):
        logger.info("输入用户名: admin")
        username_input = page.locator(".ant-form-item").nth(1).locator("input")
        username_input.highlight()
        username_input.fill("admin")
        
        # 截图：输入用户名后
        screenshot_path = f"screenshots/username_filled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="输入用户名后", attachment_type=allure.attachment_type.PNG)
        logger.info("用户名输入完成")
    
    with allure.step('输入密码: ********'):
        logger.info("输入密码")
        password_input = page.locator("input[type='password']")
        password_input.highlight()
        password_input.fill("Lx123456")
        
        # 截图：输入密码后
        screenshot_path = f"screenshots/password_filled_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="输入密码后", attachment_type=allure.attachment_type.PNG)
        logger.info("密码输入完成")
    
    with allure.step('点击登录按钮'):
        logger.info("点击登录按钮")
        login_button = page.get_by_text("登 录")
        login_button.highlight()
        
        # 截图：点击登录前
        screenshot_path = f"screenshots/before_login_click_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="点击登录前", attachment_type=allure.attachment_type.PNG)
        
        login_button.click()
        logger.info("登录按钮已点击")
        
        # 等待页面跳转
        page.wait_for_load_state("networkidle")
    
    with allure.step('验证登录成功 - 检查URL跳转'):
        logger.info("验证页面URL是否跳转到首页")
        try:
            # 修复：登录成功后实际跳转到 /home 页面，而不是根路径
            expect(page).to_have_url("http://localhost:8080/home")
            logger.info("URL验证成功：已跳转到首页(/home)")
            allure.attach(page.url, name="当前页面URL", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            logger.error(f"URL验证失败: {e}")
            logger.info(f"当前实际URL: {page.url}")  # 添加实际URL的日志记录
            # 失败时截图
            screenshot_path = f"screenshots/url_verification_failed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            page.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="URL验证失败截图", attachment_type=allure.attachment_type.PNG)
            raise
    
    with allure.step('验证登录成功 - 检查首页元素'):
        logger.info("验证首页元素是否显示")
        try:
            home_element = page.get_by_text("首页")
            expect(home_element).to_be_visible()
            logger.info("首页元素验证成功")
            
            # 成功截图
            screenshot_path = f"screenshots/login_success_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            page.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="登录成功截图", attachment_type=allure.attachment_type.PNG)
            
        except Exception as e:
            logger.error(f"首页元素验证失败: {e}")
            # 失败时截图
            screenshot_path = f"screenshots/home_element_failed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            page.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="首页元素验证失败截图", attachment_type=allure.attachment_type.PNG)
            raise
    
    logger.info("🎯 登录测试执行完成")
    logger.info("📋 接下来pytest会自动执行Teardown流程：")
    logger.info("   1. 🧹 page fixture Teardown: 关闭页面对象")
    logger.info("   2. 🧹 context fixture Teardown: 关闭上下文，保存录制视频")
    logger.info("   3. 🧹 browser fixture Teardown: 关闭浏览器（如果是最后一个测试）")
    
    # 📝 重要说明：
    # 从这里开始，pytest会自动调用各个fixture的Teardown部分
    # 我们不需要手动调用任何清理代码，pytest会按照依赖关系的逆序自动执行
    # 这就是pytest fixture机制的强大之处：自动化的资源管理！