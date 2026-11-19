from src.indexing.markdown_chunker import chunk_markdown


def test_small_document_creates_one_chunk():
    content = "# Title\n\nShort paragraph."

    chunks = chunk_markdown(content, "test.md", char_limit=100)

    assert len(chunks) == 1
    assert chunks[0].text == content
    assert chunks[0].start == 0
    assert chunks[0].end == len(content)


def test_blocks_are_grouped_when_they_fit():
    content = "# Title\n\nParagraph one.\n\nParagraph two."

    chunks = chunk_markdown(content, "test.md", char_limit=100)

    assert len(chunks) == 1
    assert chunks[0].text == content


def test_blocks_are_split_when_limit_is_exceeded():
    content = (
        "# Title\n\n"
        "First paragraph.\n\n"
        "Second paragraph.\n\n"
        "Third paragraph."
    )

    chunks = chunk_markdown(content, "test.md", char_limit=25)

    assert len(chunks) > 1
    assert all(len(chunk.text) <= 25 for chunk in chunks)


def test_long_block_is_split():
    content = "A" * 50

    chunks = chunk_markdown(content, "test.md", char_limit=10)

    assert len(chunks) == 5
    assert all(len(chunk.text) <= 10 for chunk in chunks)
    assert "".join(chunk.text for chunk in chunks) == content


def test_last_chunk_is_saved():
    content = "# Title\n\nParagraph."

    chunks = chunk_markdown(content, "test.md", char_limit=100)

    assert chunks
    assert chunks[-1].text == content


def test_chunk_offsets_match_text():
    content = "# Title\n\nParagraph one.\n\nParagraph two."

    chunks = chunk_markdown(content, "test.md", char_limit=20)

    for chunk in chunks:
        assert chunk.text == content[chunk.start:chunk.end]
        assert chunk.end - chunk.start == len(chunk.text)


def test_content_is_not_lost():
    content = (
        "# Title\n\n"
        "Paragraph one.\n\n"
        "Paragraph two.\n\n"
        "Paragraph three."
    )

    chunks = chunk_markdown(content, "test.md", char_limit=20)

    reconstructed = "".join(chunk.text for chunk in chunks)

    assert reconstructed == content