class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        atts = []
        for k, v in self.props.items():
            atts.append(f'{k}="{v}"')
        return " " + " ".join(atts)

    def __eq__(self, other):
        if self.tag != other.tag or self.value != other.value or self.props != other.props:
            return False
        if self.children is not None:
            for i in range(len(self.children)):
                if self.children[i] != other.children[i]:
                    return False
        return True

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

