#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/11/20
# @Description: [对文件功能等的简要描述（可自行添加）]
import datetime

import pytest
import allure
from playwright.sync_api import Page,expect
import logging


@allure.epic("基础数据")
@allure.feature("仓库管理")
@allure.story("仓库创建")
@allure.title("创建新仓库")
@allure.description("测试创建新仓库的完整流程")
def test_create_warehouses(logged_in_page_module: Page):
    """测试创建仓库的完整功能"""
    logging.info("🎯 开始测试创建仓库")
    page = logged_in_page_module

    with allure.step("导航到仓库页面"):
        page.goto("http://localhost:8080/basicData/warehouse")
        page.wait_for_selector("div.ant-table-content")

    with allure.step("点击新增仓库"):
        # create_button = page.get_by_role("button",name="新增仓库")
        create_button = page.get_by_text("新增仓库")
        expect(create_button).to_be_visible()
        create_button.click()

    with allure.step("输入新增仓库信息"):
        name = f"auto_{datetime.datetime.now().strftime('%H%M%S')}"
        name_input = page.locator(".ant-row").filter(has_text="仓库名称").locator("input")
        expect(name_input).to_be_visible()
        name_input.fill(name)

    with allure.step("点击确定按钮"):
        ok_button = page.get_by_role("button", name="确 定")
        expect(ok_button).to_be_visible()
        ok_button.click()

