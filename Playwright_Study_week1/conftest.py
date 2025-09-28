#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/9/26
# @Description: 全局测试配置和fixture

import pytest
import logging
import os
from datetime import datetime
from playwright.sync_api import Page, expect
import allure

# 全局日志配置
test_logdir = "test_log"
os.makedirs(test_logdir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(test_logdir, 'test_global.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Session级别的浏览器fixture
@pytest.fixture(scope="session")
def browser(playwright):
    """Session级别的浏览器，整个测试会话共享"""
    logger.info("🚀 Session Setup: Starting Chrome browser session")
    browser = playwright.chromium.launch(
        channel="chrome", 
        headless=False,
        slow_mo=300
    )
    yield browser
    logger.info("🧹 Session Teardown: Closing browser session")
    browser.close()

# Session级别的已登录上下文
@pytest.fixture(scope="session")
def logged_in_context(browser):
    """Session级别的已登录上下文，登录一次后所有测试共享"""
    logger.info("🚀 Session Setup: Creating logged-in context")
    
    # 创建上下文
    context = browser.new_context(
        viewport={"width": 1280, "height": 800}
    )
    
    # 创建临时页面进行登录
    page = context.new_page()
    
    # 执行登录流程
    logger.info("执行登录流程...")
    page.goto("http://localhost:8080/user/login")
    page.wait_for_load_state("networkidle")
    
    # 输入登录信息
    page.locator(".ant-form-item").first.locator("input").fill("001")
    page.locator(".ant-form-item").nth(1).locator("input").fill("admin")
    page.locator("input[type='password']").fill("Lx123456")
    page.get_by_text("登 录").click()
    page.wait_for_load_state("networkidle")
    
    # 验证登录成功
    expect(page).to_have_url("http://localhost:8080/home")
    logger.info("✅ 登录成功，上下文已准备就绪")
    
    # 关闭临时页面，保留已登录的上下文
    page.close()
    
    yield context
    
    logger.info("🧹 Session Teardown: Closing logged-in context")
    context.close()

# Function级别的页面fixture
@pytest.fixture(scope="function")
def logged_in_page(logged_in_context):
    """Function级别的已登录页面，每个测试函数都会获得一个新的已登录页面"""
    logger.info("🚀 Function Setup: Creating new page from logged-in context")
    page = logged_in_context.new_page()
    
    # 导航到首页确保处于登录状态
    page.goto("http://localhost:8080/home")
    page.wait_for_load_state("networkidle")
    
    yield page
    
    logger.info("🧹 Function Teardown: Closing page")
    page.close()

# 可选：未登录的页面fixture（用于登录测试）
@pytest.fixture(scope="function")
def fresh_page(browser):
    """Function级别的全新页面，用于登录测试等需要未登录状态的场景"""
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    yield page
    page.close()
    context.close()