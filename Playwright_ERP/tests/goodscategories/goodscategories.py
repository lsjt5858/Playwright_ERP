#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/10/11
# @Description: [对文件功能等的简要描述（可自行添加）]
import string
from linecache import clearcache

import pytest
import allure
from playwright.sync_api import Page, expect  # 修正：使用sync_api
import re
import datetime, random
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
@pytest.fixture(scope="class")
def test_create_categories_class(logged_in_page_class: Page):
    """创建一个产品分类"""
    logger.info("创建一个产品分类")

    with allure.step("导航到产品管理页"):
        logged_in_page_class.goto("http://localhost:8080/goods/classification")
        logged_in_page_class.wait_for_load_state("networkidle")

    with allure.step("点击新增分类按钮"):
        create_button = logged_in_page_class.get_by_role("button", name="新增分类")
        expect(create_button).to_be_visible()
        create_button.click()

        # locator('.ant-modal')：通过 CSS 选择器 .ant-modal 定位页面中的弹窗元素
        # （.ant-modal 是 Ant Design 组件库中模态框的默认类名）。
        modal = logged_in_page_class.locator('.ant-modal')
        expect(modal).to_be_visible()

    with allure.step("输入产品分类名称"):
        categories_name = f"auto_{datetime.datetime.now().strftime('%H%M%S')}"
        logger.info(f"创建产品分类名称为: {categories_name}")

        name_input = logged_in_page_class.locator('.ant-row.ant-form-item').filter(has_text="分类名称").locator(
            'input[type="text"]')
        # name_input = logged_in_page_class.locator('.ant-form-item').filter(has_text="分类").locator('input[type="text"]')
        # name_input = logged_in_page_class.locator('.ant-form-item').filter(has_text="分类名称").locator('input[type="text"]')
        # name_input = logged_in_page_class.locator('input[type="text"][placeholder="请输入分类名称"]')
        expect(name_input).to_be_visible()
        name_input.fill(categories_name)

    with allure.step("点击确定按钮"):
        ok_button = logged_in_page_class.get_by_role("button", name='确 定')
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
def test_update_categories_class(test_create_categories_class, logged_in_page_class: Page):
    """修改一个  产品类 """
    logger.info("定位编辑按钮用于修改")

    with allure.step("定位编辑按钮📌"):
        # 使用创建的分类名称定位对应表格行
        search_input = logged_in_page_class.get_by_placeholder("名称, 备注")
        expect(search_input).to_be_visible()
        search_input.fill(test_create_categories_class)
        search_input.press("Enter")
        logged_in_page_class.wait_for_timeout(1500)
        logged_in_page_class.wait_for_load_state("networkidle")

        row = logged_in_page_class.locator(".ant-table-tbody tr").filter(has_text=test_create_categories_class).first
        expect(row).to_be_visible()

        edit_button = row.get_by_role('button', name='编辑')
        expect(edit_button).to_be_visible()
        edit_button.click()

    with allure.step("修改分类名称"):
        modal = logged_in_page_class.locator('.ant-modal')
        expect(modal).to_be_visible()

        categories_name_new = f"auto_{''.join(random.choices(string.ascii_letters + string.digits, k=10))}"
        logger.info(f"更新分类名称为: {categories_name_new}")

        update_name_input = modal.locator('.ant-form-item').filter(has_text="分类名称").locator('input[type="text"]')
        expect(update_name_input).to_be_visible()
        update_name_input.fill(categories_name_new)

    with allure.step("确认修改"):
        ok_button = modal.get_by_role('button', name='确 定')
        expect(ok_button).to_be_visible()
        ok_button.click()

        # 等待弹窗关闭并页面稳定
        expect(modal).not_to_be_visible()
        logged_in_page_class.wait_for_load_state("networkidle")

    with allure.step("验证修改结果"):
        # 重新搜索新名称
        search_input.fill(categories_name_new)
        search_input.press("Enter")
        logged_in_page_class.wait_for_timeout(1500)
        logged_in_page_class.wait_for_load_state("networkidle")

        table_rows = logged_in_page_class.locator(".ant-table-tbody tr")
        rows_count = table_rows.count()

        if rows_count > 0:
            first_row_name_cell = table_rows.first.locator('td').nth(1)
            expect(first_row_name_cell).to_be_visible()
            first_row_text = first_row_name_cell.text_content().strip()

            if categories_name_new == first_row_text:
                logger.info(f"✅ 分类更新成功: 找到分类 '{categories_name_new}'")
            else:
                logger.error(f"❌ 验证失败: 期望 '{categories_name_new}' 实际 '{first_row_text}'")
                screenshot_path = f"screenshots/update_categories_failed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                os.makedirs("screenshots", exist_ok=True)
                logged_in_page_class.screenshot(path=screenshot_path)
                allure.attach.file(screenshot_path, name="分类更新失败", attachment_type=allure.attachment_type.PNG)
                assert False, f"分类更新验证失败：期望 '{categories_name_new}'，实际 '{first_row_text}'"
        else:
            logger.error(f"❌ 分类更新失败：没有找到分类 '{categories_name_new}'")
            screenshot_path = f"screenshots/no_categories_found_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs("screenshots", exist_ok=True)
            logged_in_page_class.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="未找到更新后的分类", attachment_type=allure.attachment_type.PNG)
            assert False, f"分类更新失败：没有找到分类 '{categories_name_new}'"

    with allure.step("截图记录"):
        screenshot_path = f"screenshots/categories_updated_{categories_name_new}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs("screenshots", exist_ok=True)
        logged_in_page_class.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="产品分类更新成功", attachment_type=allure.attachment_type.PNG)


@allure.epic("产品管理系统")
@allure.feature("产品分类")
@allure.story("产品删除")
@allure.title("删除产品")
@allure.description("测试删除新产品的完整流程")
@allure.tag("categories", "create", "management")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_categories_class(test_create_categories_class, logged_in_page_class: Page):
    """删除 一个  产品类 """
    logger.info("定位删除按钮用于删除")

    with allure.step("定位删除按钮📌"):
        # 使用创建的分类名称定位对应表格行
        search_input = logged_in_page_class.get_by_placeholder("名称, 备注")
        expect(search_input).to_be_visible()
        search_input.fill(test_create_categories_class)
        search_input.press("Enter")
        logged_in_page_class.wait_for_timeout(1500)
        logged_in_page_class.wait_for_load_state("networkidle")

        row = logged_in_page_class.locator(".ant-table-tbody tr").filter(has_text=test_create_categories_class).first
        expect(row).to_be_visible()

        # 更稳健地定位“删除”按钮（处理“删 除”空格情况）
        delete_button = row.get_by_role('button', name=re.compile(r"删\s*除"))
        expect(delete_button).to_be_visible()
        delete_button.click()

    with allure.step("确认删除"):
        # 精确定位弹出的确认框并点击“确 定”
        popconfirm = logged_in_page_class.locator(".ant-popconfirm, .ant-popover").first
        expect(popconfirm).to_be_visible()

        confirm_button = popconfirm.get_by_role("button", name=re.compile(r"确\s*定"))
        expect(confirm_button).to_be_visible()
        confirm_button.click()

        # 等待确认框消失与页面稳定
        expect(popconfirm).not_to_be_visible()
        logged_in_page_class.wait_for_load_state("networkidle")

    with allure.step("验证删除结果"):
        search_input.fill(test_create_categories_class)
        search_input.press("Enter")
        logged_in_page_class.wait_for_timeout(800)
        logged_in_page_class.wait_for_load_state("networkidle")

        # 仅统计包含该名称的行，避免误判
        remaining = logged_in_page_class.locator(".ant-table-tbody tr").filter(has_text=test_create_categories_class).count()
        if remaining == 0:
            logger.info(f"✅ 删除验证通过: 分类 '{test_create_categories_class}' 已从列表中移除")
        else:
            logger.error(f"❌ 删除验证失败：分类 '{test_create_categories_class}' 仍在列表中")
            screenshot_path = f"screenshots/categories_not_deleted_{test_create_categories_class}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs("screenshots", exist_ok=True)
            logged_in_page_class.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="分类删除失败", attachment_type=allure.attachment_type.PNG)
            assert False, f"分类删除失败：仍然存在 '{test_create_categories_class}'"

    with allure.step("截图记录"):
        screenshot_path = f"screenshots/categories_deleted_{test_create_categories_class}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs("screenshots", exist_ok=True)
        logged_in_page_class.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="产品分类删除成功", attachment_type=allure.attachment_type.PNG)