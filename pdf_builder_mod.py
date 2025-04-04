from fpdf import FPDF

class PDFReport(FPDF):
    def __init__(self, title:str, subtitle:str):
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self.set_auto_page_break(auto=True, margin=15)
    
    def add_title_page(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(200, 20, self.title, ln=True, align='C')
        self.set_font('Arial', 'I', 16)
        self.cell(200, 10, self.subtitle, ln=True, align='C')
        self.ln(20)
    
    def add_summary(self, summary_text:str):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, summary_text)
        self.ln(10)
    
    def add_table(self, table_data:list):
        self.set_font('Arial', 'B', 12)
        self.cell(40, 10, 'Column 1', 1)
        self.cell(40, 10, 'Column 2', 1)
        self.cell(40, 10, 'Column 3', 1)
        self.ln()
        
        self.set_font('Arial', '', 12)
        for row in table_data:
            for item in row:
                self.cell(40, 10, str(item), 1)
            self.ln()
        self.ln(10)

    def add_figure(self, image_path:str, caption:str):
        """Adds an image (graph/table) to the PDF."""
        self.add_page()
        self.image(image_path, x=10, y=self.get_y(), w=180)
        self.ln(85)  # Adjust spacing below the image
        self.set_font('Arial', 'I', 12)
        self.cell(0,10,"",ln=True, align='C')
        self.cell(0, 10, caption, ln=True, align='C')

    def save_pdf(self, filename):
        self.output(filename)

    def get_sanitized_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def generate_report(self, figures:list, captions:list, summary:str):
        """Generates a pdf report"""
        if len(captions) == len(figures):
            self.add_title_page()
            self.add_summary(summary)
            for i in range(len(figures)):
                self.add_figure(f"{figures[i]}", caption=captions[i])
            self.save_pdf(f"reports/{self.title}{self.get_sanitized_timestamp()}.pdf")
        else: 
            raise "Number of figures is different to captions"
