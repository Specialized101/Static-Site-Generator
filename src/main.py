from textnode import TextNode, TextType

def main():
    some_textnode = TextNode("Hello World", TextType.BOLD_TEXT, "https://www.boot.dev")
    print(some_textnode)

if __name__ == "__main__":
    main()