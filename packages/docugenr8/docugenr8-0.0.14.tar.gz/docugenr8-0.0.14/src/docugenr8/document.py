"""_summary_.

.
"""

from __future__ import annotations

from collections.abc import Callable

from docugenr8_core import Document as CoreDocument
from docugenr8_core.page import Page as CorePage
from docugenr8_core.settings import Settings as CoreSettings
from docugenr8_core.text_area import TextArea as CoreTextArea
from docugenr8_pdf.pdf import Pdf


class Document:
    """_summary_.

    .
    """

    def __init__(
        self,
        core_document: CoreDocument | None = None,
    ) -> None:
        """_summary_.

        .
        """
        if core_document is None:
            self.__core_document = CoreDocument()
        self.settings = Settings(self.__core_document.settings)
        self.pages: list[Page] = []
        self.doc_attributes: DocAttributes

    def add_font(
        self,
        font_name: str,
        path: str,
    ) -> None:
        self.__core_document.add_font(font_name, path)

    def add_page(
        self,
        width: float,
        height: float,
    ) -> None:
        page = Page(self.__core_document.add_page(width, height))
        self.pages.append(page)

    def create_textarea(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> TextArea:
        text_area = TextArea(x, y, width, height, self.__core_document)
        return text_area

    def output_to_bytes(
        self,
        file_format: str,
    ) -> bytes:
        match file_format:
            case "pdf":
                dto = self.__core_document._build_dto()
                return Pdf(dto).output_to_bytes()
            case _:
                raise NotImplementedError("Not supported file format.")

    def output_to_file(
        self,
        file_format: str,
        file_name: str,
    ) -> None:
        match file_format:
            case "pdf":
                b = self.output_to_bytes(file_format)
                with open(file_name, "wb") as f:
                    f.write(b)
            case _:
                raise NotImplementedError("Not supported file format.")


class Settings:
    def __init__(
        self,
        core_settings: CoreSettings,
    ) -> None:
        self.__core_settings = core_settings

    @property
    def font_current(self):
        return self.__core_settings.font_current

    @font_current.setter
    def font_current(self, font_name: str):
        self.__core_settings.font_current = font_name

    @property
    def font_size(self):
        return self.__core_settings.font_size

    @font_size.setter
    def font_size(self, font_size: float):
        self.__core_settings.font_size = font_size

    @property
    def font_color(self):
        return self.__core_settings.font_color

    @font_color.setter
    def font_color(self, font_color: tuple[int, int, int]):
        self.__core_settings.font_color = font_color

    @property
    def text_tab_size(self):
        return self.__core_settings.text_tab_size

    @text_tab_size.setter
    def text_tab_size(self, tab_size: float):
        self.__core_settings.text_tab_size = tab_size

    @property
    def text_h_align(self):
        return self.__core_settings.text_h_align

    @text_h_align.setter
    def text_h_align(self, h_align: str):
        self.__core_settings.text_h_align = h_align

    @property
    def text_v_align(self):
        return self.__core_settings.text_v_align

    @text_v_align.setter
    def text_v_align(self, v_align: str):
        self.__core_settings.text_v_align = v_align

    @property
    def text_line_height_ratio(self):
        return self.__core_settings.textline_height_ratio

    @text_line_height_ratio.setter
    def text_line_height_ratio(self, height_ratio: float):
        self.__core_settings.textline_height_ratio = height_ratio

    @property
    def text_split_words(self):
        return self.__core_settings.text_split_words

    @text_split_words.setter
    def text_split_words(self, split_words: bool):
        self.__core_settings.text_split_words = split_words

    @property
    def paragraph_first_line_indent(self):
        return self.__core_settings.paragraph_first_line_indent

    @paragraph_first_line_indent.setter
    def paragraph_first_line_indent(self, indent: float):
        self.__core_settings.paragraph_first_line_indent = indent

    @property
    def paragraph_hanging_indent(self):
        return self.__core_settings.paragraph_hanging_indent

    @paragraph_hanging_indent.setter
    def paragraph_hanging_indent(self, indent: float):
        self.__core_settings.paragraph_hanging_indent = indent

    @property
    def paragraph_left_indent(self):
        return self.__core_settings.paragraph_left_indent

    @paragraph_left_indent.setter
    def paragraph_left_indent(self, indent: float):
        self.__core_settings.paragraph_left_indent = indent

    @property
    def paragraph_right_indent(self):
        return self.__core_settings.paragraph_right_indent

    @paragraph_right_indent.setter
    def paragraph_right_indent(self, indent: float):
        self.__core_settings.paragraph_right_indent = indent

    @property
    def paragraph_space_before(self):
        return self.__core_settings.paragraph_space_before

    @paragraph_space_before.setter
    def paragraph_space_before(self, space: float):
        self.__core_settings.paragraph_space_before = space

    @property
    def paragraph_space_after(self):
        return self.__core_settings.paragraph_space_after

    @paragraph_space_after.setter
    def paragraph_space_after(self, space: float):
        self.__core_settings.paragraph_space_after = space

    @property
    def page_num_current_page_dummy(self):
        return self.__core_settings.page_num_current_page_dummy

    @page_num_current_page_dummy.setter
    def page_num_current_page_dummy(self, page_dummy: str):
        self.__core_settings.page_num_current_page_dummy = page_dummy

    @property
    def page_num_total_pages_dummy(self):
        return self.__core_settings.page_num_total_pages_dummy

    @page_num_total_pages_dummy.setter
    def page_num_total_pages_dummy(self, page_dummy: str):
        self.__core_settings.page_num_total_pages_dummy = page_dummy

    @property
    def page_num_dummy_length(self):
        return self.__core_settings.page_num_dummy_length

    @page_num_dummy_length.setter
    def page_num_dummy_length(self, length: int):
        self.__core_settings.page_num_dummy_length = length

    @property
    def page_num_presentation(self):
        return self.__core_settings.page_num_presentation

    @page_num_presentation.setter
    def page_num_presentation(self, presentation: Callable[[int], str]):
        self.__core_settings.page_num_presentation = presentation


class Page:
    def __init__(
        self,
        core_page: CorePage,
    ) -> None:
        self.__core_page = core_page

    @property
    def width(self):
        return self.__core_page._width

    @width.setter
    def width(self, width: float):
        self.__core_page._width = width

    @property
    def height(self):
        return self.__core_page._height

    @height.setter
    def height(self, height: float):
        self.__core_page._height = height

    def add_content(
        self,
        content: object,
    ) -> None:
        if isinstance(content, TextArea):
            self.__core_page.add_content(content._get_core())


class DocAttributes:
    def __init__(
        self,
    ) -> None:
        pass


class TextArea:
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        core_document: CoreDocument,
    ) -> None:
        self.__core_text_area = core_document.create_textarea(x, y, width, height)

    def _get_core(self) -> CoreTextArea:
        return self.__core_text_area

    def add_text(
        self,
        unicode_text: str,
    ) -> None:
        self.__core_text_area.add_text(unicode_text)

    def link_textarea(
        self,
        next_textarea: TextArea,
    ) -> None:
        self.__core_text_area.link_textarea(next_textarea.__core_text_area)

    def set_width(
        self,
        new_width: float,
    ) -> None:
        self.__core_text_area.set_width(new_width)
