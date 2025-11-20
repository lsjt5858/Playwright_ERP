#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/9/28
# @Description: 角色管理功能测试

import pytest
import allure
from playwright.sync_api import Page, expect  # 修正：使用sync_api
import re
import datetime
import logging
import os

logger = logging.getLogger(__name__)


@allure.epic("用户管理系统")
@allure.feature("角色管理")
@allure.story("角色创建")
@allure.title("创建新角色")
@allure.description("测试创建新角色的完整流程")
@allure.tag("role", "create", "management")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_role(logged_in_page: Page):
    """测试创建角色功能 - 复用登录状态"""
    logger.info("🎯 开始执行角色创建测试")
    
    with allure.step("导航到角色管理页面"):
        logged_in_page.goto("http://localhost:8080/role")
        logged_in_page.wait_for_load_state("networkidle")
        
    with allure.step("点击创建角色按钮"):
        # 使用最稳定的定位方法
        create_button = logged_in_page.get_by_text("新增角色")
        expect(create_button).to_be_visible()
        create_button.click()
        
        # 等待弹窗出现
        modal = logged_in_page.locator('.ant-modal')
        expect(modal).to_be_visible()

    with allure.step("输入角色信息"):
        role_name = f"auto_{datetime.datetime.now().strftime('%H%M%S')}"  # 修正：使用datetime.datetime
        logger.info(f"创建角色名称: {role_name}")
        
        # 使用最稳定的定位方法
        name_input = logged_in_page.locator('.ant-form-item').filter(has_text="名称").locator('input[type="text"]')
        expect(name_input).to_be_visible()
        name_input.fill(role_name)  # 修正：使用fill()而不是filter()
        
        # 验证输入值
        expect(name_input).to_have_value(role_name)

    with allure.step("点击确认按钮"):
        confirm_button = logged_in_page.get_by_role("button", name="确 定")  # 修正：通常是"确定"而不是"确认"
        expect(confirm_button).to_be_visible()
        confirm_button.click()
        
        # 等待弹窗关闭
        expect(modal).not_to_be_visible()

    with allure.step("验证创建的角色是否在列表中"):
        # 等待页面刷新
        logged_in_page.wait_for_load_state("networkidle")
        
        # 使用搜索功能验证角色是否创建成功
        search_input = logged_in_page.get_by_placeholder("名称, 备注")
        expect(search_input).to_be_visible()
        search_input.fill(role_name)
        search_input.press("Enter")
        
        # 等待搜索结果
        logged_in_page.wait_for_timeout(1000)

    with allure.step("验证搜索结果"):
        # 检查是否有搜索结果
        table_rows = logged_in_page.locator('.ant-table-tbody tr')
        rows_count = table_rows.count()
        
        if rows_count > 0:
            # 获取第一行的角色名称
            first_row_name_cell = table_rows.first.locator('td').nth(1)
            expect(first_row_name_cell).to_be_visible()
            first_row_text = first_row_name_cell.text_content().strip()
            
            # 修正：正确比较字符串
            if role_name == first_row_text:
                logger.info(f"✅ 角色创建成功：找到角色 '{role_name}'")
            else:
                logger.error(f"❌ 角色验证失败：期望 '{role_name}'，实际 '{first_row_text}'")
                screenshot_path = f"screenshots/create_role_failed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                os.makedirs("screenshots", exist_ok=True)
                logged_in_page.screenshot(path=screenshot_path)
                allure.attach.file(screenshot_path, name="角色创建失败", attachment_type=allure.attachment_type.PNG)
                assert False, f"角色创建验证失败：期望 '{role_name}'，实际 '{first_row_text}'"
        else:
            logger.error(f"❌ 角色创建失败：没有找到角色 '{role_name}'")
            screenshot_path = f"screenshots/no_role_found_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs("screenshots", exist_ok=True)
            logged_in_page.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="未找到创建的角色", attachment_type=allure.attachment_type.PNG)
            assert False, f"角色创建失败：没有找到角色 '{role_name}'"
            
    with allure.step("截图记录"):
        screenshot_path = f"screenshots/role_created_{role_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs("screenshots", exist_ok=True)
        logged_in_page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="角色创建成功", attachment_type=allure.attachment_type.PNG)
        
    logger.info("🎯 角色创建测试执行完成")
    return role_name

@allure.epic("用户管理系统")
@allure.feature("角色管理")
@allure.story("角色列表")
@allure.title("查看角色列表")
@allure.description("测试角色列表页面的加载和数据显示")
@allure.tag("role", "list", "management")
@allure.severity(allure.severity_level.NORMAL)
def test_role_list(logged_in_page: Page):
    """测试查看角色列表功能 - 复用登录状态"""
    logger.info("🎯 开始执行角色列表查看测试")
    page = logged_in_page
    
    with allure.step("导航到角色管理页面"):
        page.goto("http://localhost:8080/role")
        page.wait_for_load_state("networkidle")

    with allure.step("验证页面加载"):
        # 验证页面URL
        expect(page).to_have_url(re.compile(".*role.*"))
        
        # 验证关键元素存在
        page_title = page.locator('h1, .page-title, [class*="title"]')
        if page_title.count() > 0:
            expect(page_title.first).to_be_visible()

    with allure.step("验证角色列表表格"):
        # 定位角色列表表格
        role_table = page.locator(".ant-table-tbody")
        expect(role_table).to_be_visible()
        # 验证表格有数据（修正：应该检查不为空）
        table_rows = role_table.locator('tr')
        rows_count = table_rows.count()
        
        if rows_count > 0:
            logger.info(f"✅ 角色列表加载成功，共 {rows_count} 条数据")
            
            # 验证第一行数据
            first_row = table_rows.first
            expect(first_row).to_be_visible()
            
            # 验证表头和数据结构
            table_headers = page.locator('.ant-table-thead th')
            headers_count = table_headers.count()
            logger.info(f"表格列数: {headers_count}")
            
        else:
            logger.warning("⚠️ 角色列表为空")
            
    with allure.step("验证搜索功能"):
        # 验证搜索框存在
        search_input = page.get_by_placeholder("名称, 备注")
        expect(search_input).to_be_visible()
        
        # 验证新增按钮存在
        create_button = page.get_by_text("新增角色")
        expect(create_button).to_be_visible()
        
    with allure.step("截图记录"):
        screenshot_path = f"screenshots/role_list_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=screenshot_path)
        
    logger.info("🎯 角色列表查看测试执行完成")


@allure.epic("用户管理系统")
@allure.feature("角色管理")
@allure.story("角色列表")
@allure.title("查看角色列表")
@allure.description("测试角色列表页面的加载和数据显示")
@allure.tag("role", "list", "management")
@allure.severity(allure.severity_level.NORMAL)
def test_role_list_session(logged_in_page_session: Page):
    """测试查看角色列表功能 - 复用登录状态"""
    logger.info("🎯 开始执行角色列表查看测试")
    page = logged_in_page_session

    with allure.step("导航到角色管理页面"):
        page.goto("http://localhost:8080/role")
        page.wait_for_load_state("networkidle")

    with allure.step("验证页面加载"):
        # 验证页面URL
        expect(page).to_have_url(re.compile(".*role.*"))

        # 验证关键元素存在
        page_title = page.locator('h1, .page-title, [class*="title"]')
        if page_title.count() > 0:
            expect(page_title.first).to_be_visible()

    with allure.step("验证角色列表表格"):
        # 定位角色列表表格
        role_table = page.locator(".ant-table-tbody")
        expect(role_table).to_be_visible()
        # 验证表格有数据（修正：应该检查不为空）
        table_rows = role_table.locator('tr')
        rows_count = table_rows.count()

        if rows_count > 0:
            logger.info(f"✅ 角色列表加载成功，共 {rows_count} 条数据")

            # 验证第一行数据
            first_row = table_rows.first
            expect(first_row).to_be_visible()

            # 验证表头和数据结构
            table_headers = page.locator('.ant-table-thead th')
            headers_count = table_headers.count()
            logger.info(f"表格列数: {headers_count}")

        else:
            logger.warning("⚠️ 角色列表为空")

    with allure.step("验证搜索功能"):
        # 验证搜索框存在
        search_input = page.get_by_placeholder("名称, 备注")
        expect(search_input).to_be_visible()

        # 验证新增按钮存在
        create_button = page.get_by_text("新增角色")
        expect(create_button).to_be_visible()

    with allure.step("截图记录"):
        screenshot_path = f"screenshots/role_list_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        page.screenshot(path=screenshot_path)

    logger.info("🎯 角色列表查看测试执行完成")


@allure.epic("用户管理系统")
@allure.feature("角色管理")
@allure.story("角色列表")
@allure.title("删除角色")
@allure.description("测试角色列表页面的加载和数据显示")
@allure.tag("role", "delete", "management")
def test_delete_role_session(logged_in_page_session: Page):
    """测试删除角色功能 - 复用登录状态"""
    logger.info("🎯 开始执行删除角色测试")
    page = logged_in_page_session

    with allure.step("创建一个角色并获取名称"):
        role_name = test_create_role(page)
        logger.info(f"待删除的角色：{role_name}")

    with allure.step("导航到角色管理页面并搜索该角色"):
        page.goto("http://localhost:8080/role")
        page.wait_for_load_state("networkidle")

        search_input = page.get_by_placeholder("名称, 备注")
        expect(search_input).to_be_visible()
        search_input.fill(role_name)
        search_input.press("Enter")

        table_rows = page.locator('.ant-table-tbody tr')
        target_row = table_rows.filter(has_text=role_name).first
        expect(target_row).to_be_visible()

    with allure.step("点击该行的删除按钮"):
        delete_button = target_row.get_by_role("button", name=re.compile("删除"))
        expect(delete_button).to_be_visible()
        delete_button.click()

        confirm_button = page.get_by_role("button", name=re.compile("确 定"))
        # confirm_button = page.click('role=button[name="确 定"]')
        # confirm_button = page.get_by_role("button", has_text="确 定")
        # confirm_button = page.locator("body > div:nth-child(7) > div > div > div > div.ant-popover-inner > div > div.ant-popover-buttons > button.ant-btn.ant-btn-primary.ant-btn-sm > span")
        expect(confirm_button).to_be_visible()
        confirm_button.click()


    with allure.step("验证该角色已被删除"):
        # 重新搜索确保该记录不存在
        search_input = page.get_by_placeholder("名称, 备注")
        expect(search_input).to_be_visible()
        search_input.fill(role_name)
        search_input.press("Enter")
        page.wait_for_timeout(800)

        remaining = page.locator('.ant-table-tbody tr').filter(has_text=role_name).count()
        if remaining == 0:
            logger.info(f"✅ 角色删除成功：'{role_name}' 不在列表中")
        else:
            logger.error(f"❌ 角色删除失败：仍发现角色 '{role_name}'")
            screenshot_path = f"screenshots/delete_role_failed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="角色删除失败", attachment_type=allure.attachment_type.PNG)
            assert False, f"角色删除失败：仍然存在 '{role_name}'"
    with allure.step("截图记录删除结果"):
        screenshot_path = f"screenshots/role_deleted_{role_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs("screenshots", exist_ok=True)
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="角色删除成功", attachment_type=allure.attachment_type.PNG)


    logger.info("🎯 删除角色测试执行完成")


