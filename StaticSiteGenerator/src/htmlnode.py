link_tag = "a"
bold_tag = "b"
italic_tag = "i"
quote_tag = "q"
code_tag = "code"
href_tag = "href"
paragraph_tag = "p"
header1_tag = "hl"
normal_tag = None

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        assert NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"\nHtmlNode: \ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("[!] Invalid HTML: missing value")
        if self.tag == None:
            return f'{self.value}'
        if self.tag == "a":
                return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"\nLeafNode: \ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("[!] Invalid HTML: missing tag")
        if not self.children:
            raise ValueError("[!] Invalid HTML: no children attached")
        children_html = "".join(child.to_html() for child in self.children)
        return f'<{self.tag}>{children_html}</{self.tag}>'

    def __repr__(self):
        return f"\nParentNode: \ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"
    