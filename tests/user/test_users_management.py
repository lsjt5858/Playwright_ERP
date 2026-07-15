#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 熊🐻来个🥬
# @Date:  2025/9/28
# @Description: 用户管理功能测试

import pytest
import allure
from playwright.sync_api import Page, expect
import re
import datetime
from faker import Faker
import logging
import os
from typing import Optional
fake = Faker("zh_CN")
logger = logging.getLogger(__name__)


class UserRowScope:
    """用户列表行的作用域（Scope Model），只在目标行内执行操作"""
    def __init__(self, page: Page, row_locator):
        self.page = page
        self.row = row_locator

    def delete(self):
        delete_btn = self.row.locator('button:has-text("删除"), [role="button"]:has-text("删除")').first
        expect(delete_btn).to_be_visible()
        delete_btn.click()

        # 在当前可见的 Popconfirm 内确认
        confirm_pop = self.page.locator('.ant-popover:visible').first
        confirm_btn = confirm_pop.get_by_role("button", name=re.compile(r"确\s*定"))
        expect(confirm_btn).to_be_visible()
        confirm_btn.click()


class UserPage:
    """用户页面 Page Object：封装创建/搜索/定位/删除等操作"""
    def __init__(self, page: Page):
        self.page = page

    def goto_account(self):
        self.page.goto("http://localhost:8080/account")
        self.page.wait_for_load_state("networkidle")

    def goto_user_list(self):
        self.page.goto("http://localhost:8080/account")
        self.page.wait_for_load_state("networkidle")

    def create_user(self, name: Optional[str] = None, employee_name: Optional[str] = None, gender: str = "女") -> str:
        """创建用户，返回创建的用户名"""
        self.goto_account()

        # 打开创建弹窗
        create_btn = self.page.locator('button:has-text("新增账号"), button:has-text("新增用户")').first
        expect(create_btn).to_be_visible()
        create_btn.click()
        modal = self.page.locator('.ant-modal:visible').first
        expect(modal).to_be_visible()

        # 数据准备
        if name is None:
            name = f"auto_{datetime.datetime.now().strftime('%H%M%S')}"
        if employee_name is None:
            employee_name = fake.name()
        logger.info(f"创建用户名称: {name}")

        # 用户名
        user_name_input = self.page.locator('.ant-row.ant-form-item').filter(has_text="用户名").locator('input[type="text"]')
        expect(user_name_input).to_be_visible()
        user_name_input.fill(name)
        expect(user_name_input).to_have_value(name)

        # 员工姓名
        employee_input = self.page.locator('.ant-row.ant-form-item').filter(has_text="员工姓名").locator('input[type="text"]')
        expect(employee_input).to_be_visible()
        employee_input.fill(employee_name)

        # 性别选择（语义定位 + 浮层限定）
        gender_item = self.page.locator('.ant-form-item').filter(has_text=re.compile(r"性别"))
        gender_combobox = gender_item.get_by_role("combobox")
        expect(gender_combobox).to_be_visible()
        gender_combobox.click()

        dropdown = self.page.locator('.ant-select-dropdown:visible').first
        expect(dropdown).to_be_visible()
        # 先 hover “男”，再选择目标性别
        male_opt = dropdown.get_by_role('option', name='男')
        expect(male_opt).to_be_visible()
        male_opt.hover()

        target_opt = dropdown.get_by_role('option', name=gender)
        expect(target_opt).to_be_visible()
        target_opt.click()

        # 提交
        confirm_btn = self.page.get_by_role("button", name=re.compile(r"确\s*定"))
        expect(confirm_btn).to_be_visible()
        confirm_btn.click()
        expect(modal).not_to_be_visible()
        self.page.wait_for_load_state("networkidle")

        return name

    def _search_input(self):
        """稳健定位搜索输入框"""
        return self.page.locator(
            'input[placeholder*="名称"], input[placeholder*="备注"], '
            'input[placeholder*="搜索"], input[type="search"], '
            '.ant-input[placeholder]'
        ).first

    def search_user(self, keyword: str):
        self.goto_user_list()
        search_input = self._search_input()
        if search_input.count() > 0:
            expect(search_input).to_be_visible()
            search_input.fill(keyword)
            search_input.press("Enter")
        self.page.wait_for_load_state("networkidle")
        table_body = self.page.locator('.ant-table-tbody')
        if table_body.count() > 0:
            expect(table_body.first).to_be_visible()
        return self.page.locator('.ant-table-tbody tr')

    def row_by_name(self, name: str):
        """根据用户名返回该行 locator"""
        rows = self.search_user(name)
        target_row = rows.filter(has_text=name).first
        # 若短时间内没有行出现，不强行失败；交由调用方做业务断言
        return target_row

    def row_scope(self, name: str) -> UserRowScope:
        """返回该用户所在行的作用域对象"""
        target_row = self.row_by_name(name)
        expect(target_row).to_be_visible()
        return UserRowScope(self.page, target_row)

    def assert_user_exists(self, name: str):
        locator = self.page.locator('.ant-table-tbody tr').filter(has_text=name)
        # 非 0 断言用 not_to_have_count(0)
        expect(locator).not_to_have_count(0)

    def assert_user_not_exists(self, name: str):
        locator = self.page.locator('.ant-table-tbody tr').filter(has_text=name)
        expect(locator).to_have_count(0)


@allure.epic("用户管理系统")
@allure.feature("用户管理")
class TestUsersManagement:
    @allure.story("用户创建")
    @allure.title("创建新用户")
    @allure.description("测试创建新用户的完整流程")
    def test_create_user_class(self, logged_in_page_class: Page):
        logger.info("🎯 开始执行用户创建测试")
        page = logged_in_page_class
        user_page = UserPage(page)
        user_name = user_page.create_user()

        # 验证创建结果（作用域到目标行）
        target_row = user_page.row_by_name(user_name)
        expect(target_row).to_be_visible()

        # 记录截图
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/user_created_{user_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        logged_in_page_class.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="用户创建成功", attachment_type=allure.attachment_type.PNG)

        logger.info("🎯 用户创建测试执行完成")

    @allure.story("用户删除")
    @allure.title("删除用户（先创建再删除）")
    @allure.tag("user", "delete", "management")
    def test_delete_user_class(self, logged_in_page_class: Page):
        """企业常用删除逻辑：先创建 → 在列表中搜索 → 行作用域删除 → 验证不存在"""
        logger.info("🎯 开始执行删除用户测试")
        user_page = UserPage(logged_in_page_class)

        # 先创建一个待删用户
        user_name = user_page.create_user()
        logger.info(f"待删除的用户：{user_name}")

        # 行作用域删除
        row_scope = user_page.row_scope(user_name)
        row_scope.delete()

        # 验证不存在
        user_page.assert_user_not_exists(user_name)

        # 截图记录
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/user_deleted_{user_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        logged_in_page_class.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="用户删除成功", attachment_type=allure.attachment_type.PNG)

        logger.info("🎯 删除用户测试执行完成")




