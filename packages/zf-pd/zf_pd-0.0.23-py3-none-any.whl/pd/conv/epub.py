from loguru import logger


def epub(src: str, dst: str) -> None:
    dst_format = dst.split(".")[-1]

    if dst_format == 'pdf':
        epub_to_pdf(src, dst)
    else:
        logger.error(f"Unsupported format {dst_format}")
    return


def epub_to_pdf(src: str, dst: str) -> None:
    converter = EpubToPDF(
        src_path=src,
        dst_path=dst,
    )
    converter.convert()
    return


"""
Code for converting the EPUB to PDF.
"""

import os
import zipfile
import io
import img2pdf
from PIL import Image
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from lxml import etree


class EpubToPDF:
    def __init__(self, src_path, dst_path):
        self.src_path = src_path
        self.dst_path = dst_path

    def convert(self):
        with zipfile.ZipFile(self.src_path, 'r') as epub:
            # Extract the contents of the EPUB file
            epub.extractall(os.path.splitext(self.src_path)[0])

            # Find the OPF file
            opf_file = self.find_opf_file(epub)

            # Parse the OPF file
            opf_path = os.path.join(os.path.splitext(self.src_path)[0], opf_file)
            tree = etree.parse(opf_path)
            root = tree.getroot()

            # Namespace dictionary
            ns = {'opf': 'http://www.idpf.org/2007/opf', 'xhtml': 'http://www.w3.org/1999/xhtml'}

            # Find the manifest items
            manifest_items = root.findall('.//opf:manifest/opf:item', namespaces=ns)

            # Create a PDF writer
            pdf_writer = PdfWriter()

            # Iterate over the manifest items
            for item in manifest_items:
                # Check if the item is an XHTML file
                if item.attrib['media-type'] == 'application/xhtml+xml':
                    xhtml_path = os.path.join(os.path.dirname(opf_path), item.attrib['href'])
                    self.add_xhtml_to_pdf(xhtml_path, pdf_writer)
                # Check if the item is an image
                elif item.attrib['media-type'].startswith('image/'):
                    image_path = os.path.join(os.path.dirname(opf_path), item.attrib['href'])
                    self.add_image_to_pdf(image_path, pdf_writer)

            # Write the PDF to the destination path
            with open(self.dst_path, 'wb') as pdf_file:
                pdf_writer.write(pdf_file)

    def find_opf_file(self, epub):
        # Find the OPF file in the EPUB
        for file in epub.namelist():
            if file.endswith('.opf'):
                return file
        raise Exception('OPF file not found in the EPUB.')

    def add_xhtml_to_pdf(self, xhtml_path, pdf_writer):
        # Parse the XHTML file
        tree = etree.parse(xhtml_path)
        root = tree.getroot()

        # Create a BytesIO object to write the PDF content
        packet = io.BytesIO()

        # Create a canvas object
        c = canvas.Canvas(packet, pagesize=letter)

        # Render the XHTML content on the canvas
        for element in root.iter():
            if element.text:
                c.drawString(100, 700, element.text)

        # Save the canvas to the BytesIO object
        c.showPage()
        c.save()

        # Get the PDF content from the BytesIO object
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # Add the new page to the PDF writer
        pdf_writer.add_page(new_pdf.pages[0])

    def add_image_to_pdf(self, image_path, pdf_writer):
        # Open the image file
        with open(image_path, 'rb') as image_file:
            # Create an image object
            image = Image.open(image_file)

            # Convert the image to bytes
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')

            # Create a new PDF page with the image
            pdf_bytes = img2pdf.convert(image_bytes.getvalue())
            pdf_page = PdfReader(io.BytesIO(pdf_bytes)).pages[0]

            # Add the new page to the PDF writer
            pdf_writer.add_page(pdf_page)
