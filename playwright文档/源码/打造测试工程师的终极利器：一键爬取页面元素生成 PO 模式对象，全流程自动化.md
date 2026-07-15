## **前言**

测试工程师在自动化测试中常常遇到以下难题：  
1. **页面复杂，元素难以定位**：面对复杂的页面结构，手动编写元素定位代码既耗时又容易出错。  
2. **重复劳动**：每次新增页面或调整页面布局时，都需要重新手动创建 Page Object，对测试效率造成极大影响。  
3. **适配复杂场景**：面对需要鉴权的页面（如登录后才能访问的页面），如何高效获取页面元素成为一大挑战。  

**如果有一个工具，能够一键爬取页面所有元素，自动生成符合 Page Object 设计模式的 Python 文件，并支持复杂场景（如鉴权）和自定义扩展，是不是可以彻底解放测试工程师？**

本文将为你展示如何构建这样的工具，利用 **Python 爬虫** 提取页面元素，并结合 **Ollama 本地部署的 DeepSeek 模型** 提高元素定位的准确性，自动生成符合 PO 模式的代码文件。无论页面结构有多复杂，这个工具都能轻松胜任，同时保证代码清晰、易扩展，适合 Python 基础较弱的测试工程师使用。

---

## **工具功能概述**

1. **页面元素提取**  
   - 爬取 HTML 页面，提取所有常见控件（如按钮、输入框、下拉列表等）。
   - 根据属性优先级（如 `id`、`name`、`class`）生成准确的定位代码。

2. **支持鉴权处理**  
   - 对于需要登录的页面，支持通过请求头添加鉴权信息（如 `Authorization` Token）完成页面爬取。

3. **自动生成 PO 对象**  
   - 按照 Page Object 设计模式，生成 Python 文件，分层管理页面对象及其操作方法。

4. **接入 DeepSeek 提高定位准确性**  
   - 利用 DeepSeek 模型对提取的元素进行分类和优化，确保生成的代码更智能、更准确。

5. **支持复杂页面与扩展**  
   - 针对复杂页面结构（如动态加载元素），提供可扩展的通用解决方案。

---

## **工具实现**

### **1. 依赖安装**

在编写代码前，请确保安装以下依赖库：
```bash
pip install requests beautifulsoup4 playwright jinja2
```

---

### **2. 页面元素提取代码**

以下代码演示如何爬取页面 HTML 并提取所有常见控件（如按钮、输入框等），支持基于属性优先级生成准确的定位代码。

```python
from bs4 import BeautifulSoup
import requests

def extract_page_elements(url, headers=None):
    """
    爬取页面并提取常见控件信息
    :param url: 页面 URL
    :param headers: 请求头（支持鉴权）
    :return: 页面控件信息字典
    """
    # 发起 HTTP 请求
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {response.status_code}")
    
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    elements = []

    # 提取按钮
    for button in soup.find_all("button"):
        elements.append({
            "tag": "button",
            "id": button.get("id"),
            "name": button.get("name"),
            "class": button.get("class"),
            "text": button.get_text(strip=True)
        })

    # 提取输入框
    for input_field in soup.find_all("input"):
        elements.append({
            "tag": "input",
            "id": input_field.get("id"),
            "name": input_field.get("name"),
            "type": input_field.get("type"),
            "placeholder": input_field.get("placeholder")
        })

    # 提取下拉列表
    for select in soup.find_all("select"):
        elements.append({
            "tag": "select",
            "id": select.get("id"),
            "name": select.get("name"),
            "options": [option.get_text(strip=True) for option in select.find_all("option")]
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

### **3. 元素优先级定位规则**

根据提取的元素属性，按以下优先级生成定位代码：
- **第一优先级**：`id`
- **第二优先级**：`name`
- **第三优先级**：`class`
- **兜底方案**：XPath（自动生成）

以下代码展示如何根据优先级生成准确的定位代码：

```python
def generate_locator(element):
    """
    根据元素属性生成定位代码
    :param element: 单个控件信息字典
    :return: 定位代码字符串
    """
    if element.get("id"):
        return f"self.page.locator('#{element['id']}')"
    elif element.get("name"):
        return f"self.page.locator('[name=\"{element['name']}\"]')"
    elif element.get("class"):
        class_name = " ".join(element["class"]) if isinstance(element["class"], list) else element["class"]
        return f"self.page.locator('.{class_name}')"
    else:
        # 兜底方案：生成 XPath
        return f"self.page.locator('//{element['tag']}[text()=\"{element.get('text', '')}\"]')"

# 示例：为提取的元素生成定位代码
for element in elements:
    locator = generate_locator(element)
    print(f"元素定位代码：{locator}")
```

---

### **4. 自动生成 PO 对象**

结合提取到的控件信息，自动生成符合 Page Object 设计模式的 Python 文件。

#### **生成 PO 类**

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

    # 生成方法名和定位代码
    for element in elements:
        element["method_name"] = f"get_{element['id'] or element['name'] or 'element'}"
        element["locator"] = generate_locator(element)

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

    def get_username(self):
        return self.page.locator('#username')

    def get_password(self):
        return self.page.locator('#password')

    def get_login_button(self):
        return self.page.locator('#login')
```

---

### **5. 项目结构与文件输出**

按照 Page Object 模式的层级结构生成文件：
```plaintext
tests/
├── page_objects/
│   ├── login_page.py  # 自动生成的 PO 类文件
├── test_login.py      # 示例测试代码
```

生成文件的代码：
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

# 保存生成的 PO 类
save_to_file("tests/page_objects", "login_page.py", page_object_code)
```

---

### **6. DeepSeek 接入优化**

通过调用 DeepSeek 模型，根据元素上下文优化定位代码，提高准确性。例如：
- 输入：“生成更准确的 XPath 定位代码”
- DeepSeek 输出优化后的定位规则。

调用 DeepSeek 接口：
```python
def optimize_with_deepseek(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {"model": "deepseek-r1:1.5b", "prompt": prompt}
    response = requests.post(url, json=payload)
    return response.json()["response"]

# 示例：优化定位规则
prompt = "如何为以下元素生成更准确的 XPath 定位代码：<input id='username' class='form-control'>"
optimized_code = optimize_with_deepseek(prompt)
print("DeepSeek 优化后的定位代码：", optimized_code)
```

---

## **总结**

通过这套工具，测试工程师可以实现以下目标：
1. **爬取页面所有控件，快速生成 PO 对象**：支持常见控件（如按钮、输入框等）及复杂页面。
2. **支持鉴权场景**：通过请求头添加 Token，轻松爬取需登录页面。
3. **提升定位准确性**：结合 DeepSeek 模型优化元素定位代码。
4. **自动化输出符合 PO 模式的代码结构**：减少重复劳动，提高测试效率。

这套工具不仅让测试工程师从繁琐的手工操作中解放出来，更能帮助团队构建可维护的测试代码库。如果你正在寻找一款高效的自动化测试工具，不妨试试这套方案！