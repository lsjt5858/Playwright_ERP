import re
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
from jinja2 import Template
import os


def generate_playwright_locator(element):
    """
    根据页面元素生成 Playwright 定位代码
    :param element: 单个控件信息字典
    :return: 定位代码字符串
    """
    if element.get("role"):
        return f"self.page.get_by_role('{element['role']}', name='{element.get('text', '')}')"
    elif element.get("text"):
        return f"self.page.get_by_text('{element['text']}')"
    elif element.get("placeholder"):
        return f"self.page.get_by_placeholder('{element['placeholder']}')"
    elif element.get("id"):
        return f"self.page.locator('#{element['id']}')"
    elif element.get("name"):
        return f"self.page.locator('[name=\"{element['name']}\"]')"
    elif element.get("class"):
        class_selector = "." + ".".join(element["class"]) if isinstance(element["class"],
                                                                        list) else f".{element['class']}"
        return f"self.page.locator('{class_selector}')"
    else:
        # 兜底方案：生成 CSS 选择器
        return f"self.page.locator('//{element['tag']}')"


def convert_to_pytest(recorded_script, page_objects):
    """
    将录制脚本转换为 pytest 测试代码
    :param recorded_script: 录制脚本代码
    :param page_objects: 页面对象类名
    :return: pytest 测试代码字符串
    """
    test_code = f"""
import pytest
from page_objects import {', '.join(page_objects)}

@pytest.mark.parametrize("username, password", [("test_user", "test_password")])
def test_login(page, username, password):
    login_page = LoginPage(page)
    page.goto("https://example.com/login")
    login_page.get_username_input().fill(username)
    login_page.get_password_input().fill(password)
    login_page.get_login_button().click()
    """
    return test_code


def generate_page_object_class(page_name, elements):
    """
    根据页面元素生成 PO 类代码
    :param page_name: 页面名称
    :param elements: 页面控件信息
    :return: PO 类代码字符串
    """
    template_str = """
class {{ page_name }}Page:
    def __init__(self, page):
        self.page = page
    {% for element in elements %}
    def {{ element.method_name }}(self):
        return {{ element.locator }}
    {% endfor %}
    """
    template = Template(template_str)

    # 为每个元素生成唯一方法名
    for element in elements:
        base_method_name = element.get("id") or element.get("name") or element.get("text", "element").replace(" ",
                                                                                                              "_").lower()
        element["method_name"] = f"get_{base_method_name}"
        element["locator"] = generate_playwright_locator(element)

    # 渲染模板
    return template.render(page_name=page_name, elements=elements)


def save_to_file(directory, file_name, content):
    """
    保存代码到文件
    :param directory: 文件夹路径
    :param file_name: 文件名
    :param content: 文件内容
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file_name), "w", encoding="utf-8") as f:
        f.write(content)


# 如果本地安装的chromium需要指定路径，则如下配置
custom_browser_path = r"C:\Users\Python_测试之道\AppData\Local\ms-playwright\chromium-1140\chrome-win\chrome.exe"
with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False, args=["--start-maximized"])  # 如果不指定路径，则执行这条语句，注释下面的那条
    browser = p.chromium.launch(executable_path=custom_browser_path, headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    # todo ------------------------------------------------------------------
    # todo 此处需调整为自己想获取的网页源码的步骤
    # todo 通过playwright codegen录制部分脚本
    # todo 通过playwright获取html源码更加靠谱稳定一点
    page.goto('http://xxx/login')
    # page.get_by_placeholder("登录账户").click()
    # page.get_by_placeholder("登录账户").fill("xxx")
    # page.get_by_placeholder("密码").click()
    # page.get_by_placeholder("密码").fill("xxx")
    # page.get_by_role("button", name="登 录").click()

    # todo ------------------------------------------------------------------

    time.sleep(3)  # 等待一下页面完成加载
    content = page.content()  # 根据上面的步骤就可以获取到登录页面的源码
    soup = BeautifulSoup(content, "html.parser")
    elements = []

    # 提取常见控件
    for tag in ["button", "input", "select", "textarea"]:
        for element in soup.find_all(tag):
            elements.append({
                "tag": tag,
                "id": element.get("id"),
                "name": element.get("name"),
                "class": element.get("class"),
                "text": element.get_text(strip=True),
                "placeholder": element.get("placeholder"),
                "role": element.get("role")
            })

    # 示例：为提取的元素生成定位代码
    for element in elements:
        locator = generate_playwright_locator(element)
        print(f"元素定位代码：{locator}")

    # 示例：生成登录页面的 PO 类
    page_object_code = generate_page_object_class("AppCenter", elements)  # todo此处的Login需修改
    print(page_object_code)
    save_to_file("tests/page_objects", "appCenterHomePage.py", page_object_code)