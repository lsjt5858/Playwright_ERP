#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/10/11
# @Description: [对文件功能等的简要描述（可自行添加）]

import pytest
import allure
from playwright.sync_api import Page, expect  # 修正：使用sync_api
import re
import datetime
import logging
import os
logger = logging.getLogger(__name__)

@allure.epic("产品管理系统")
@allure.feature("产品分类")
@allure.story("产品创建")
@allure.title("创建产品")
@allure.description("测试创建新产品的完整流程")
@allure.tag("categories", "create", "management")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_categories_class(logged_in_page_class: Page):
    """创建一个产品分类"""
    logger.info("创建一个产品分类")

    with allure.step("导航到产品管理页"):
        logged_in_page_class.goto("http://localhost:8080/goods/classification")
        logged_in_page_class.wait_for_load_state("networkidle")

    with allure.step("点击新增分类按钮"):
        create_button = logged_in_page_class.get_by_role("button",name = "新增分类")
        expect(create_button).to_be_visible()
        create_button.click()

        # locator('.ant-modal')：通过 CSS 选择器 .ant-modal 定位页面中的弹窗元素
        # （.ant-modal 是 Ant Design 组件库中模态框的默认类名）。
        modal = logged_in_page_class.locator('.ant-modal')
        expect(modal).to_be_visible()

    with allure.step("输入产品分类名称"):
        categories_name = f"auto_{datetime.datetime.now().strftime('%H%M%S')}"
        logger.info(f"创建产品分类名称为: {categories_name}")

        name_input = logged_in_page_class.locator('.ant-row.ant-form-item').filter(has_text="分类名称").locator('input[type="text"]')
        # name_input = logged_in_page_class.locator('.ant-form-item').filter(has_text="分类").locator('input[type="text"]')
        # name_input = logged_in_page_class.locator('.ant-form-item').filter(has_text="分类名称").locator('input[type="text"]')
        # name_input = logged_in_page_class.locator('input[type="text"][placeholder="请输入分类名称"]')
        expect(name_input).to_be_visible()
        name_input.fill(categories_name)

    with allure.step("点击确定按钮"):
        ok_button = logged_in_page_class.get_by_role("button",name='确 定')
        expect(ok_button).to_be_visible()
        ok_button.click()

        # 等待弹窗关闭
        expect(modal).not_to_be_visible()

    with allure.step("验证创建的产品是否在列表中"):
        # 等待页面刷新
        logged_in_page_class.wait_for_load_state("networkidle")

        # 搜索
        search_input = logged_in_page_class.get_by_placeholder("名称, 备注")
        expect(search_input).to_be_visible()
        search_input.fill(categories_name)
        search_input.press("Enter")
        
        # 等待搜索结果加载
        logged_in_page_class.wait_for_timeout(2000)  # 等待2秒让搜索结果加载
        logged_in_page_class.wait_for_load_state("networkidle")
        
        # search_input.press("Tab")  # 模拟 Tab 键
        # search_input.press("Escape")  # 模拟 Esc 键
        # search_input.press("Backspace")  # 模拟退格键
        # search_input.press("ArrowDown")  # 模拟下方向键
        # search_input.press("Control+A")    # 模拟 Ctrl+A（全选）

    with allure.step("验证搜索结果"):
        table_rows = logged_in_page_class.locator(".ant-table-tbody tr")
        rows_count = table_rows.count()

        if rows_count > 0:
            # table_rows：假设这是一个已定位的 “表格行” 集合（比如通过 locator('tbody tr') 获取的所有 <tr> 元素）。
            # .first：从 table_rows 集合中取第一个元素（即表格的第一行）。
            # .locator('td')：在第一行内，定位所有单元格元素 <td>（表格的数据单元格）。
            # .nth(1)：从定位到的 <td> 集合中，取索引为 1 的单元格（注意：Playwright 中索引从 0 开始，所以 nth(1) 表示第二个单元格）。
            # 最终 first_row_name_cell 就是 “表格第一行的第二个单元格” 的元素对象。
            first_row_name_cell = table_rows.first.locator('td').nth(1)
            expect(first_row_name_cell).to_be_visible()
            # .text_content()：获取该单元格内的所有文本内容（包括嵌套元素中的文本）。
            # .strip()：去除文本前后的空白字符（如空格、换行符），用于后续精准比对。
            first_row_text = first_row_name_cell.text_content().strip()

            if categories_name == first_row_text:
                logger.info(f"✅ 创建产品分类成功: 找到分类 '{categories_name}'")
            else:
                logger.error(f"❌ 验证失败: 期望 '{categories_name}' 实际 '{first_row_text}'")
                screenshot_path = f"screenshots/create_role_failed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                os.makedirs("screenshots", exist_ok=True)
                logged_in_page_class.screenshot(path=screenshot_path)
                allure.attach.file(screenshot_path, name="角色创建失败", attachment_type=allure.attachment_type.PNG)
                assert False, f"角色创建验证失败：期望 '{categories_name}'，实际 '{first_row_text}'"

        else:
            logger.error(f"❌ 角色创建失败：没有找到角色 '{categories_name}'")
            screenshot_path = f"screenshots/no_role_found_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs("screenshots", exist_ok=True)
            logged_in_page_class.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="未找到创建的角色", attachment_type=allure.attachment_type.PNG)
            assert False, f"角色创建失败：没有找到角色 '{categories_name}'"

    with allure.step("截图记录"):
        screenshot_path = f"screenshots/categories_created_{categories_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs("screenshots", exist_ok=True)
        logged_in_page_class.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="产品分类创建成功", attachment_type=allure.attachment_type.PNG)

    logger.info("🎯 产品分类创建测试执行完成")
    return categories_name

@allure.epic("产品管理系统")
@allure.feature("产品分类")
@allure.story("产品编辑")
@allure.title("编辑产品")
@allure.description("测试编辑新产品的完整流程")
@allure.tag("categories", "create", "management")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_categories_class(logged_in_page_class: Page,):
    pass




