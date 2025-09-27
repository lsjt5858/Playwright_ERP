#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/9/26
# @Description: [对文件功能等的简要描述（可自行添加）]

import pytest,requests
from playwright.sync_api import Page, expect
import time,allure


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@allure.title("登录测试")
def test_login(page: Page):
    page.goto("http://localhost:8080/user/login")
    page.wait_for_load_state("networkidle")
    
    with allure.step('输入公司编号'):
        # 根据截图，公司编号是第一个输入框
        page.locator(".ant-form-item").first.locator("input").fill("001")
    
    with allure.step('输入用户名'):
        # 用户名是第二个输入框
        page.locator(".ant-form-item").nth(1).locator("input").fill("admin")
    
    with allure.step('输入密码'):
        # 密码框使用type=password定位
        page.locator("input[type='password']").fill("Lx123456")
    
    with allure.step('点击登录按钮'):
        # 登录按钮
        page.get_by_text("登 录").click()
    print("你是最棒的!")
    print("    # 通过文本内容定位登录按钮  login_button = page.get_by_text(\"登录\")")
    print("#按钮的 class 属性进行定位。 使用 CSS 选择器定位 login_button = page.locator('button.ant-btn-primary')")
    print("更精确地匹配所有类名 login_button = page.locator('button.ant-btn.ant-btn-primary.ant-btn-lg')   ")
    print("# 通过角色和名称定位 login_button = page.get_by_role(\"button\", name=\"登录\"):Playwright 支持通过 ARIA 角色和名称来定位元素，这通常比直接使用 CSS 选择器更健壮。")
    print("# 使用 XPath 定位 login_button = page.locator('//button[contains(text(), \"登录\")]')")




