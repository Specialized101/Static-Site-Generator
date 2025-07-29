from enum import Enum

class TextType(Enum):
	PLAIN_TEXT = "plain"
	BOLD_TEXT = "bold"
	ITALIC_TEXT = "italic"
	CODE_TEXT = "code"
	LINK_TEXT = "link"
	IMAGE_TEXT = "image"

class TextNode:
	def __init__(self, text, text_type: TextType, url=None):
		if not isinstance(text_type, TextType):
			raise TypeError(f"text_type must be an instance of TextType, got {type(text_type)}")
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		if self.text == other.text and \
			self.text_type == other.text_type and \
			self.url == other.url:
			return True
		return False
	
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
	