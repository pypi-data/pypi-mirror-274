# mdtopptx

`mdtopptx` is a Python library that makes it easy to convert markdown text into compelling PowerPoint presentations. It allows you to create slides with rich formatting, bullet points, images, and hyperlinks directly from your markdown code.

## Features

- Convert markdown to PowerPoint slides with ease.
- Support for text formatting (bold, italic, underline, color).
- Add bullet points for clarity and organization.
- Insert images from URLs to enhance presentations.
- Embed hyperlinks to provide context and further references.


## Installation

You can install the `mdtopptx` package from PyPI using pip:

```bash
pip install mdtopptx
```

## Usage Examples

Here's a simple example of how you can use the `mdtopptx` library to convert markdown text into a PowerPoint presentation:

```
from mdtopptx import parse_markdown, create_ppt

# Example Markdown input
markdown_text = """
## Slide 1 (title box)

This is the first slide of my presentation.

* Bullet point 1
* Bullet point 2

---

## Slide 2 (title box)

This is the second slide.

**Bold text** and *italic text*.

Inline code: `code snippet`

<color:#FF0000>Red text</color>

---

## Slide 3 (title box)

![Image name](https://www.example.com/image.png)

[google](https://www.google.com)
"""

# Parse the markdown text and create the PowerPoint presentation
parsed_slides = parse_markdown(markdown_text)
create_ppt(parsed_slides, 'output_presentation.pptx')

```

Slides must be delimited by a blank line followed by `---` followed by a blank
line.  When rendered as markdown `---` will be a horizontal rule.  If you need
a horizontal rule in your slides, use `***` or `___` instead.