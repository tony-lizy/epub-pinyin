"""Tests for pdf_converter module."""

import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from epub_pinyin.pdf_converter import PdfConverter, convert_epub_to_pdf, convert_epub_with_pinyin_to_pdf
from epub_pinyin.epub_parser import EpubParser


@pytest.fixture
def sample_epub_with_structure(sample_epub):
    """Create a sample EPUB with extracted structure for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        parser = EpubParser(tmpdir)
        parser.extract_epub(sample_epub)
        yield parser


@pytest.mark.skipif(not PdfConverter.is_available(), reason="WeasyPrint not available")
def test_pdf_converter_initialization(sample_epub_with_structure):
    """Test PdfConverter initialization."""
    converter = PdfConverter(sample_epub_with_structure)
    assert converter.epub_parser == sample_epub_with_structure
    assert converter.structure == sample_epub_with_structure.structure


def test_pdf_converter_initialization_no_weasyprint():
    """Test PdfConverter initialization without WeasyPrint."""
    with patch('epub_pinyin.pdf_converter.WEASYPRINT_AVAILABLE', False):
        with tempfile.TemporaryDirectory() as tmpdir:
            parser = EpubParser(tmpdir)
            
            with pytest.raises(ImportError, match="WeasyPrint is required"):
                PdfConverter(parser)


def test_pdf_converter_initialization_no_structure():
    """Test PdfConverter initialization without extracted structure."""
    if not PdfConverter.is_available():
        pytest.skip("WeasyPrint not available")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        parser = EpubParser(tmpdir)  # No extraction done
        
        with pytest.raises(ValueError, match="EPUB parser must have extracted content"):
            PdfConverter(parser)


@pytest.mark.skipif(not PdfConverter.is_available(), reason="WeasyPrint not available")
def test_get_combined_css(sample_epub_with_structure):
    """Test CSS combination functionality."""
    converter = PdfConverter(sample_epub_with_structure)
    css = converter._get_combined_css()
    
    # Check that default CSS is included
    assert "@page" in css
    assert "font-family" in css
    assert "ruby" in css
    
    # Check that EPUB CSS is included (if any)
    assert isinstance(css, str)
    assert len(css) > 0


@pytest.mark.skipif(not PdfConverter.is_available(), reason="WeasyPrint not available")
def test_prepare_html_content(sample_epub_with_structure):
    """Test HTML content preparation."""
    converter = PdfConverter(sample_epub_with_structure)
    html_files = sample_epub_with_structure.get_html_files()
    
    html_content = converter._prepare_html_content(html_files)
    
    # Check basic HTML structure
    assert "<!DOCTYPE html>" in html_content
    assert "<html lang=\"zh-CN\">" in html_content
    assert "<head>" in html_content
    assert "<body>" in html_content
    assert "</html>" in html_content
    
    # Check metadata inclusion
    assert sample_epub_with_structure.structure.metadata.title in html_content
    assert sample_epub_with_structure.structure.metadata.creator in html_content
    
    # Check that Chinese content is included
    assert "你好，世界" in html_content


@pytest.mark.skipif(not PdfConverter.is_available(), reason="WeasyPrint not available")
def test_convert_to_pdf(sample_epub_with_structure):
    """Test PDF conversion."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "test_output.pdf")
        
        converter = PdfConverter(sample_epub_with_structure)
        
        # Mock WeasyPrint to avoid actual PDF generation in tests
        with patch('epub_pinyin.pdf_converter.HTML') as mock_html:
            mock_doc = MagicMock()
            mock_html.return_value = mock_doc
            
            converter.convert_to_pdf(output_path)
            
            # Verify WeasyPrint was called
            mock_html.assert_called_once()
            mock_doc.write_pdf.assert_called_once_with(output_path)


def test_is_available():
    """Test availability check."""
    # This will return the actual availability of WeasyPrint
    available = PdfConverter.is_available()
    assert isinstance(available, bool)


@pytest.mark.skipif(not PdfConverter.is_available(), reason="WeasyPrint not available")
def test_convert_epub_to_pdf(sample_epub):
    """Test standalone EPUB to PDF conversion."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "converted.pdf")
        
        # Mock the PDF generation part
        with patch('epub_pinyin.pdf_converter.PdfConverter') as mock_converter_class:
            mock_converter = MagicMock()
            mock_converter_class.return_value = mock_converter
            
            convert_epub_to_pdf(sample_epub, pdf_path)
            
            # Verify converter was created and convert_to_pdf was called
            mock_converter_class.assert_called_once()
            mock_converter.convert_to_pdf.assert_called_once_with(pdf_path)


@pytest.mark.skipif(not PdfConverter.is_available(), reason="WeasyPrint not available")
def test_convert_epub_with_pinyin_to_pdf(sample_epub):
    """Test EPUB to PDF conversion with pinyin."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "converted_pinyin.pdf")
        
        # Mock both the text processor and PDF converter
        with patch('epub_pinyin.pdf_converter.annotate_file_with_pinyin') as mock_annotate, \
             patch('epub_pinyin.pdf_converter.PdfConverter') as mock_converter_class:
            
            mock_converter = MagicMock()
            mock_converter_class.return_value = mock_converter
            
            convert_epub_with_pinyin_to_pdf(sample_epub, pdf_path)
            
            # Verify pinyin annotation was called
            mock_annotate.assert_called()
            
            # Verify converter was created and convert_to_pdf was called
            mock_converter_class.assert_called_once()
            mock_converter.convert_to_pdf.assert_called_once_with(pdf_path)


def test_convert_epub_to_pdf_no_weasyprint():
    """Test PDF conversion without WeasyPrint available."""
    with patch('epub_pinyin.pdf_converter.PdfConverter.is_available', return_value=False):
        with tempfile.TemporaryDirectory() as tmpdir:
            epub_path = os.path.join(tmpdir, "test.epub")
            pdf_path = os.path.join(tmpdir, "test.pdf")
            
            # Create a dummy epub file
            Path(epub_path).touch()
            
            with pytest.raises(ImportError, match="WeasyPrint is required"):
                convert_epub_to_pdf(epub_path, pdf_path)


def test_convert_epub_with_pinyin_to_pdf_no_weasyprint():
    """Test PDF conversion with pinyin without WeasyPrint available."""
    with patch('epub_pinyin.pdf_converter.PdfConverter.is_available', return_value=False):
        with tempfile.TemporaryDirectory() as tmpdir:
            epub_path = os.path.join(tmpdir, "test.epub")
            pdf_path = os.path.join(tmpdir, "test.pdf")
            
            # Create a dummy epub file
            Path(epub_path).touch()
            
            with pytest.raises(ImportError, match="WeasyPrint is required"):
                convert_epub_with_pinyin_to_pdf(epub_path, pdf_path)