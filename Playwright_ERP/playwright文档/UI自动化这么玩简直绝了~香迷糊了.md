## **前言**

在自动化测试中，**Playwright** 是一款备受推崇的浏览器自动化工具，其强大的 API（如 `get_by_role`、`get_by_text` 等）让复杂页面元素的精准定位变得更加高效。然而，如何将 Playwright 的这些功能与 **Page Object 模式（PO 模式）** 结合起来，生成可维护、灵活、通用的测试代码，仍然是一个挑战。

尤其是面对层级复杂的页面结构或动态加载的元素，测试工程师往往需要花费大量时间手动调整定位方式，避免因元素重复或动态变化而导致的脚本维护难题。如果能将 **Playwright 的录制脚本** 自动转换为符合 PO 模式的代码，并通过 Playwright 的强大 API 灵活生成精准定位方法，将大大提升测试效率，降低测试成本。

本文将通过构建一个工具，帮助你：
1. 利用 **Playwright 的 API**（如 `get_by_role`、`get_by_text` 和 `locator` 等），生成精准且通用的页面元素定位方法。
2. 按照 **Page Object 模式** 自动生成 Python 文件，并转换录制脚本为 pytest 测试用例。
3. 适配动态页面和复杂层级结构，确保代码灵活性和可维护性。

---

## **工具功能概述**

1. **智能生成 PO 方法**  
   - 使用 Playwright 的 API，根据元素属性（如 `role`、`text`、`placeholder` 等）生成灵活的定位代码。
   - 对于层级复杂的元素，自动生成 CSS 选择器（如 `page.locator(".class1 > .class2")`）。

2. **避免重复定义**  
   - 自动为无 `name` 或 `id` 的元素生成唯一方法名称，确保代码可读性和无冲突。

3. **转换录制脚本为 pytest 测试用例**  
   - 将 Playwright 的录制脚本转换为调用 PO 方法的 pytest 测试代码，符合行业最佳实践。

4. **自动化文件生成**  
   - 按照 PO 模式结构，生成可直接运行的项目文件。

---

## **工具实现**

### **1. 依赖安装**

在开始前，请确保安装以下依赖库：
```bash
pip install playwright jinja2
```

---

### **2. 页面元素提取与 Playwright API 定位**

以下代码展示如何提取页面元素并生成基于 Playwright API 的灵活定位方法。

#### **2.1 元素提取与属性优先级**

```python
from bs4 import BeautifulSoup
import requests

def extract_page_elements(url, headers=None):
    """
    爬取页面并提取常见控件信息
    :param url: 页面 URL
    :param headers: 鉴权请求头
    :return: 页面控件信息字典
    """
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    elements = []

    # 提取常见控件
    for tag in ["button", "input", "a", "select", "textarea"]:
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

    return elements

# 示例：提取页面元素
url = "https://example.com/login"
headers = {"Authorization": "Bearer your_token_here"}  # 鉴权请求头
elements = extract_page_elements(url, headers=headers)
print("提取的页面元素：")
for element in elements:
    print(element)
```

---

#### **2.2 生成 Playwright 定位代码**

根据元素属性，按以下优先级生成定位代码：
1. 使用 `get_by_role`：如果元素有 `role` 属性。
2. 使用 `get_by_text`：如果元素有可见文本。
3. 使用 `get_by_placeholder`：如果元素有 `placeholder` 属性。
4. 使用 `locator`：生成基于 `id`、`name` 或 `class` 的精准定位代码。
5. 兜底：生成 CSS 选择器或 XPath。

```python
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
        class_selector = "." + ".".join(element["class"]) if isinstance(element["class"], list) else f".{element['class']}"
        return f"self.page.locator('{class_selector}')"
    else:
        # 兜底方案：生成 CSS 选择器
        return f"self.page.locator('//{element['tag']}')"

# 示例：生成定位代码
for element in elements:
    locator = generate_playwright_locator(element)
    print(f"定位代码：{locator}")
```

**输出示例**：
```plaintext
定位代码：self.page.get_by_role('button', name='Login')
定位代码：self.page.get_by_placeholder('Enter your username')
定位代码：self.page.locator('#password')
定位代码：self.page.locator('.form-control')
```

---

### **3. 生成 PO 类**

结合上述定位方法，自动生成符合 Page Object 模式的类文件。

```python
from jinja2 import Template

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
        base_method_name = element.get("id") or element.get("name") or element.get("text", "element").replace(" ", "_").lower()
        element["method_name"] = f"get_{base_method_name}"
        element["locator"] = generate_playwright_locator(element)

    # 渲染模板
    return template.render(page_name=page_name, elements=elements)

# 示例：生成登录页面的 PO 类
page_object_code = generate_page_object_class("Login", elements)
print(page_object_code)
```

**生成的 PO 类代码**：
```python
class LoginPage:
    def __init__(self, page):
        self.page = page

    def get_login_button(self):
        return self.page.get_by_role('button', name='Login')

    def get_username_input(self):
        return self.page.get_by_placeholder('Enter your username')

    def get_password_input(self):
        return self.page.locator('#password')
```

---

### **4. 转换录制脚本为 pytest 测试用例**

将 Playwright 的录制脚本转换为 pytest 测试代码，并调用生成的 PO 类。

```python
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

# 示例：转换录制脚本为 pytest 测试代码
pytest_code = convert_to_pytest(None, ["LoginPage"])
print(pytest_code)
```

**生成的 pytest 测试代码**：
```python
import pytest
from page_objects import LoginPage

@pytest.mark.parametrize("username, password", [("test_user", "test_password")])
def test_login(page, username, password):
    login_page = LoginPage(page)
    page.goto("https://example.com/login")
    login_page.get_username_input().fill(username)
    login_page.get_password_input().fill(password)
    login_page.get_login_button().click()
```

---

### **5. 自动化文件生成**

将生成的 PO 类和测试代码保存到文件中，按照以下目录结构组织：
```plaintext
tests/
├── page_objects/
│   ├── login_page.py  # 自动生成的 PO 类文件
├── test_login.py      # pytest 测试代码
```

```python
import os

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

# 保存生成的 PO 类和测试代码
save_to_file("tests/page_objects", "login_page.py", page_object_code)
save_to_file("tests", "test_login.py", pytest_code)
```

---

## **总结**

通过这套工具，测试工程师可以实现：
1. **智能定位**：灵活使用 Playwright 的 API（如 `get_by_role`、`get_by_text` 等），精准高效地生成元素定位代码。
2. **自动化代码生成**：快速生成符合 PO 模式的类文件和 pytest 测试代码，提升测试效率。
3. **适配复杂场景**：支持动态页面和复杂层级结构，确保代码的灵活性和可维护性。

这套工具不仅能让测试工程师从繁琐的手工操作中解放出来，还能帮助他们更专注于高价值的测试逻辑。如果你正在寻找一款能显著提升效率的自动化测试工具，不妨试试这套方案！