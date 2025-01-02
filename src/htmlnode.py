class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        result = []
        for key, value in self.props.items():
            result.append(f'{key}="{value}"')
        return " ".join(result)

    def __repr__(self):
        return f"<HTMLNode {self.tag} {self.value} {self.children} {self.props}>"


class LeafNode(HTMLNode):
    def __init__(self, tag, value: str, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"<LeafNode {self.tag} {self.value} {self.props}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children: list, value=None, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("There is no tag")
        if self.children is None:
            raise ValueError("There is not children")

        result = []
        for node in self.children:
            result.append(node.to_html())
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{''.join(result)}</{self.tag}>"
        return f"<{self.tag}>{''.join(result)}</{self.tag}>"

    def __repr__(self):
        return f"<ParentNode {self.tag} {self.children} {self.props}>"
