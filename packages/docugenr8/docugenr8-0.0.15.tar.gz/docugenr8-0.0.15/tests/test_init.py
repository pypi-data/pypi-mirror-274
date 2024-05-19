from docugenr8.document import Document

def test__check_document_settings():
    def test_page_number_presentation(page_number: int) -> str:
        return "TEST"
    doc = Document()
    doc.add_font("calibri", "./tests/calibri.ttf")
    assert doc.settings.font_current == "calibri"
    doc.settings.font_size = 15
    assert doc.settings.font_size == 15
    doc.settings.font_color = (100,100,100)
    assert doc.settings.font_color == (100,100,100)
    doc.settings.text_tab_size = 10
    assert doc.settings.text_tab_size == 10
    doc.settings.text_v_align = "right"
    assert doc.settings.text_v_align == "right"
    doc.settings.text_split_words = False
    assert doc.settings.text_split_words == False
    doc.settings.text_line_height_ratio = 2
    assert doc.settings.text_line_height_ratio == 2
    doc.settings.paragraph_first_line_indent = 20
    assert doc.settings.paragraph_first_line_indent == 20
    doc.settings.paragraph_hanging_indent = 20
    assert doc.settings.paragraph_hanging_indent == 20
    doc.settings.paragraph_left_indent = 20
    assert doc.settings.paragraph_left_indent == 20
    doc.settings.paragraph_right_indent = 20
    assert doc.settings.paragraph_right_indent == 20
    doc.settings.paragraph_space_after = 20
    assert doc.settings.paragraph_space_after == 20
    doc.settings.paragraph_space_before = 20
    assert doc.settings.paragraph_space_before == 20
    doc.settings.page_num_current_page_dummy = "TEST"
    assert doc.settings.page_num_current_page_dummy == "TEST"
    doc.settings.page_num_total_pages_dummy = "TEST"
    assert doc.settings.page_num_total_pages_dummy == "TEST"
    doc.settings.page_num_dummy_length = 10
    assert doc.settings.page_num_dummy_length == 10
    doc.settings.page_num_presentation = test_page_number_presentation
    assert doc.settings.page_num_presentation(1) == "TEST"
