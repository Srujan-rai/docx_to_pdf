from http.server import SimpleHTTPRequestHandler
import http.server
import socketserver
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import shutil

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Save the uploaded DOCX file
        with open('uploaded.docx', 'wb') as docx_file:
            docx_file.write(post_data)

        # Convert the DOCX to PDF
        self.convert_docx_to_pdf('uploaded.docx', 'converted.pdf')

        # Send the converted PDF file to the client
        self.send_response(200)
        self.send_header('Content-Disposition', 'attachment; filename=converted.pdf')
        self.send_header('Content-type', 'application/pdf')
        self.end_headers()

        with open('converted.pdf', 'rb') as pdf_file:
            shutil.copyfileobj(pdf_file, self.wfile)

    def convert_docx_to_pdf(self, input_docx, output_pdf):
        doc = Document(input_docx)

        c = canvas.Canvas(output_pdf, pagesize=letter)

        width, height = letter
        max_line_height = 12  # Adjust as needed
        left_margin = 40
        top_margin = 750  # Adjust as needed

        y = top_margin

        for paragraph in doc.paragraphs:
            c.setFont("Helvetica", 12)
            c.drawString(left_margin, y, paragraph.text)
            y -= max_line_height

            if y < 50:  # You can adjust this value based on your page size and margins
                c.showPage()
                y = top_margin

        c.save()

if __name__ == '__main__':
    port = 9600
    Handler = MyHandler

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()
