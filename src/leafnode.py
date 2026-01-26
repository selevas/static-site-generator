from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return str(self.value)
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

