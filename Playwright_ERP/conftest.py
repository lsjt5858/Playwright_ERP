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

# 新增：全局缓存登录后的 token（供 API 用例复用）
AUTH_TOKEN = None

# Session级别的浏览器fixture
@pytest.fixture(scope="session")
def browser(playwright):
    """Session级别的浏览器，整个测试会话共享"""
    logger.info("🚀 Session Setup: Starting Chromium browser session")
    # 注意：不使用 channel="chrome"，避免额外原生窗口
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=300
    )
    yield browser
    logger.info("🧹 Session Teardown: Closing browser session")
    browser.close()

@pytest.fixture(scope="session")
def logged_in_context(browser):
    """
    Session级别的已登录上下文：
    - 只登录一次（会话级）
    - 后续所有页面均复用该上下文，保证登录态一致
    """
    logger.info("🚀 Session Setup: Creating logged-in context")
    context = browser.new_context(viewport={"width": 1280, "height": 800})

    # 使用临时页面执行一次登录
    page = context.new_page()
    logger.info("🔐 执行登录流程...")
    page.goto("http://localhost:8080/user/login")
    page.wait_for_load_state("networkidle")

    # 输入登录信息并提交
    page.locator(".ant-form-item").first.locator("input").fill("001")
    page.locator(".ant-form-item").nth(1).locator("input").fill("admin")
    page.locator("input[type='password']").fill("Lx123456")
    page.get_by_text("登 录").click()
    page.wait_for_load_state("networkidle")

    # 验证登录成功
    expect(page).to_have_url("http://localhost:8080/home")
    logger.info("✅ 登录成功，上下文已准备就绪")

    # 提取并缓存登录后的 token（优先 localStorage，其次 cookie）
    global AUTH_TOKEN
    try:
        token = page.evaluate('window.localStorage.getItem("token")')
    except Exception:
        token = None
    if not token:
        try:
            for c in context.cookies():
                if c.get("name") in ("access","token", "auth_token", "Authorization"):
                    token = c.get("value")
                    break
        except Exception:
            token = None
    AUTH_TOKEN = token
    if AUTH_TOKEN:
        logger.info(f"🔑 已获取到认证token: {AUTH_TOKEN[:20]}...")
    else:
        logger.warning("⚠️ 未在localStorage或cookie中发现token，请确认实际存储键名")

    # 关闭临时页面，保留已登录的上下文
    # page.close()

    yield context

    logger.info("🧹 Session Teardown: Closing logged-in context")
    context.close()

# 提供一个 session 级别的 token fixture，供 API 用例直接注入使用
@pytest.fixture(scope="session")
def auth_token(logged_in_context):
    """会话级 token，API 测试直接使用"""
    return AUTH_TOKEN

# ================= 页面复用的不同粒度（按需选择） =================

@pytest.fixture(scope="function")
def logged_in_page(logged_in_context):
    """
    Function级页面（保留隔离性，推荐用于“容易脏”的用例）：
    - 每个测试函数新建一个页面
    - 复用 session 级上下文（已登录）
    """
    logger.info("🚀 Function Setup: Creating new page from logged-in context")
    page = logged_in_context.new_page()
    page.goto("http://localhost:8080/home")
    page.wait_for_load_state("networkidle")
    yield page
    logger.info("🧹 Function Teardown: Closing page")
    page.close()

@pytest.fixture(scope="class")
def logged_in_page_class(logged_in_context):
    """
    Class级页面（推荐默认使用，窗口更少）：
    - 同一个测试类共享一个页面
    - 适合导航密集、状态可控的场景
    """
    logger.info("🚀 Class Setup: Creating shared page for test class")
    page = logged_in_context.new_page()
    page.goto("http://localhost:8080/home")
    page.wait_for_load_state("networkidle")
    yield page
    logger.info("🧹 Class Teardown: Closing shared page")
    page.close()

@pytest.fixture(scope="module")
def logged_in_page_module(logged_in_context):
    """
    Module级页面（同文件共享一个页面）：
    - 适合模块内用例共享状态的折中方案
    """
    logger.info("🚀 Module Setup: Creating shared page for test module")
    page = logged_in_context.new_page()
    page.goto("http://localhost:8080/home")
    page.wait_for_load_state("networkidle")
    yield page
    logger.info("🧹 Module Teardown: Closing shared page")
    page.close()

@pytest.fixture(scope="session")
def logged_in_page_session(logged_in_context):
    """
    Session级页面（整个会话共享一个页面）：
    - 单窗口贯穿所有用例（性能最好）
    - 注意：跨用例状态需谨慎重置，适合演示或非常稳定的场景
    """
    logger.info("🚀 Session Setup: Creating one shared page for all tests")
    page = logged_in_context.new_page()
    page.goto("http://localhost:8080/home")
    page.wait_for_load_state("networkidle")
    yield page
    logger.info("🧹 Session Teardown: Closing session shared page")
    # page.close()

# 可选：未登录页面（用于专门验证登录流程）
@pytest.fixture(scope="function")
def fresh_page(browser):
    """
    Function级未登录页面：
    - 用于登录测试或需要未登录态的场景
    - 独立上下文，避免污染已登录上下文
    """
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()
    yield page
    page.close()
    context.close()