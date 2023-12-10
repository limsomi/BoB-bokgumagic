import os
from PyQt5 import QtWidgets
from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from PIL import Image, UnidentifiedImageError
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import pandas as pd
from modules.ui.view_dialog import InputDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfFileReader
class WriteReport(QThread):
    progress_signal=pyqtSignal(int)
    result_signal = pyqtSignal()
    finished_signal=pyqtSignal()
    def __init__(self,date,name):
        super().__init__()
        self.date=date
        self.name=name
    def set_background(self,slide, background_path, prs):
        """ 슬라이드의 배경으로 이미지를 설정하는 함수 """
        left = top = Inches(0)
        pic = slide.shapes.add_picture(background_path, left, top, width=prs.slide_width, height=prs.slide_height)
        # 이미지를 슬라이드의 가장 뒤로 이동
        slide.shapes._spTree.remove(pic._element)
        slide.shapes._spTree.insert(2, pic._element)

    def add_table_from_csv(self,prs, file_name, background_path):
        data = pd.read_csv(file_name)
        rows, cols = data.shape
        slides = []

        for start_row in range(0, rows, 14):
            end_row = min(start_row + 14, rows)
            slide_layout = prs.slide_layouts[5]
            slide = prs.slides.add_slide(slide_layout)
            self.set_background(slide, background_path, prs)
            slides.append(slide)
            title = slide.shapes.title
            title.text = os.path.basename(file_name)

            table_width = cols * Inches(1)
            table_height = min(end_row - start_row, 14) * Inches(0.5)
            x_position = (prs.slide_width - table_width) / 2
            y_position = (prs.slide_height - table_height) / 2 - Cm(2)

            table = slide.shapes.add_table(min(end_row - start_row, 14) + 1, cols, x_position, y_position, table_width, table_height).table

            for col_index, col_name in enumerate(data.columns):
                cell = table.cell(0, col_index)
                cell.text = col_name
                for paragraph in cell.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(8)

            for row_index in range(start_row, end_row):
                for col_index, item in enumerate(data.iloc[row_index]):
                    cell = table.cell(row_index - start_row + 1, col_index)
                    cell.text = str(item)
                    for paragraph in cell.text_frame.paragraphs:
                        for run in paragraph.runs:
                            run.font.size = Pt(8)

        return slides

    def add_text_from_file(self,prs, file_path, slide_title, background_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            start = 0
            max_lines = 30

            while start < len(text):
                slide_layout = prs.slide_layouts[5]
                slide = prs.slides.add_slide(slide_layout)
                self.set_background(slide, background_path, prs)
                title = slide.shapes.title
                title.text = slide_title

                textbox = slide.shapes.add_textbox(Cm(1), Cm(4), Inches(7), Inches(5))
                text_frame = textbox.text_frame
                text_frame.word_wrap = True

                paragraph = text_frame.add_paragraph()
                paragraph.font.size = Pt(15)

                for _ in range(max_lines):
                    if start < len(text):
                        end = text.find('\n', start) + 1 if text.find('\n', start) != -1 else len(text)
                        paragraph.text += text[start:end]
                        start = end
                    else:
                        break

    def add_text_from_files(self,prs, folder_path, slide_title, background_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    start = 0
                    max_lines = 30

                    while start < len(text):
                        slide_layout = prs.slide_layouts[5]
                        slide = prs.slides.add_slide(slide_layout)
                        self.set_background(slide, background_path, prs)
                        title = slide.shapes.title
                        title.text = slide_title

                        textbox = slide.shapes.add_textbox(Cm(1), Cm(4), Inches(7), Inches(5))
                        text_frame = textbox.text_frame
                        text_frame.word_wrap = True

                        paragraph = text_frame.add_paragraph()
                        paragraph.font.size = Pt(15)

                        for _ in range(max_lines):
                            if start < len(text):
                                end = text.find('\n', start) + 1 if text.find('\n', start) != -1 else len(text)
                                paragraph.text += text[start:end]
                                start = end
                            else:
                                break

    def add_images_with_names(self,prs, folder_path, title_text, background_path):
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        for i in range(0, len(image_files), 9):
            slide_layout = prs.slide_layouts[5]
            slide = prs.slides.add_slide(slide_layout)
            self.set_background(slide, background_path, prs)
            title = slide.shapes.title
            title.text = title_text

            image_size = Inches(2)
            gap = Inches(0.7)  # 이미지 간 간격

            for j in range(9):
                if i + j < len(image_files):
                    file_path = os.path.join(folder_path, image_files[i + j])
                    try:
                        img = Image.open(file_path)
                    except UnidentifiedImageError:
                        continue

                    width, height = img.size
                    aspect_ratio = width / height
                    resized_height = image_size
                    resized_width = resized_height * aspect_ratio

                    col = j % 3
                    row = j // 3

                    total_width = 3 * resized_width + 2 * gap
                    total_height = 3 * resized_height + 2 * gap
                    start_x = (prs.slide_width - total_width) / 2
                    start_y = (prs.slide_height - total_height) / 2

                    x_position = start_x + (resized_width + gap) * col
                    y_position = start_y + (resized_height + gap) * row

                    if x_position < 0:
                        x_position += Cm(2)
                    elif x_position + resized_width > prs.slide_width:
                        x_position -= Cm(2)

                    slide.shapes.add_picture(file_path, x_position, y_position, width=resized_width, height=resized_height)

                    text_box = slide.shapes.add_textbox(x_position, y_position + resized_height, resized_width, Inches(0.5))
                    tf = text_box.text_frame
                    tf.text = image_files[i + j]
                    tf.paragraphs[0].font.size = Pt(10)
                    tf.word_wrap = True
    
    # def save_as_pdf(self, pptx_path, pdf_path):
    #     prs = Presentation(pptx_path)

    #     pdf_writer = PdfWriter()

    #     for i, slide in enumerate(prs.slides):
    #         # Slide를 이미지로 저장
    #         slide_image_path = f"temp_slide_{i}.png"
    #         self.save_slide_as_image(slide, slide_image_path)

    #         # 이미지를 PDF에 추가
    #         pdf_writer.add_page(self.image_to_pdf_page(slide_image_path))

    #         # 이미지 파일 삭제
    #         os.remove(slide_image_path)

    #     # PDF 파일 저장
    #     with open(pdf_path, "wb") as pdf_file:
    #         pdf_writer.write(pdf_file)

    # def save_slide_as_image(self, slide, image_path):
    #     image = slide.shapes._spTree[2].get_or_add_image_part().blob
    #     with open(image_path, 'wb') as img_file:
    #         img_file.write(image)

    # def image_to_pdf_page(self, image_path):
    #     pdf_page = canvas.Canvas("temp.pdf", pagesize=letter)
    #     pdf_page.drawImage(image_path, 0, 0, width=letter[0], height=letter[1])
    #     pdf_page.showPage()
    #     pdf_page.save()

    #     # 생성된 PDF 파일을 읽어온 후 반환
    #     pdf_reader = PdfFileReader("temp.pdf")
    #     return pdf_reader.getPage(0)
    
    
    def run(self):
        signal=0

        prs = Presentation()
        prs.slide_width = Cm(21)
        prs.slide_height = Cm(29.7)
        signal+=10
        self.progress_signal.emit(signal)
        # 표지 슬라이드 추가
        slide_layout = prs.slide_layouts[5]
        cover_slide = prs.slides.add_slide(slide_layout)
        cover_slide.shapes.add_picture('./report_cover.png', 0, 0, prs.slide_width, prs.slide_height)
        signal+=10
        self.progress_signal.emit(signal)
        # 제목 추가 (원래 위치에서 3인치 아래로 이동)
        original_title_y = Inches(2)
        title_shape = cover_slide.shapes.add_textbox(Inches(1), original_title_y + Inches(3), prs.slide_width - Inches(2), Inches(1))
        title_text_frame = title_shape.text_frame
        title_text_frame.text = "분석 결과 보고서"
        title_text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
        title_paragraph = title_text_frame.paragraphs[0]
        title_paragraph.font.size = Pt(44)
        title_paragraph.font.bold = True
        title_paragraph.font.color.rgb = RGBColor(0, 0, 100)
        signal+=10
        self.progress_signal.emit(signal)
        # 부제목 추가 (원래 위치에서 3인치 아래로 이동)
        original_subtitle_y = Inches(3)
        subtitle_shape = cover_slide.shapes.add_textbox(Inches(1), original_subtitle_y + Inches(3), prs.slide_width - Inches(2), Inches(1))
        subtitle_text_frame = subtitle_shape.text_frame
        subtitle_text_frame.text = f"Date: {self.date}   Name: {self.name}"
        subtitle_text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT
        signal+=10
        self.progress_signal.emit(signal)
        # 데이터 테이블 슬라이드 추가
        files = ["./result/Package.csv", "./result/EventLog.csv", "./result/contacts.csv", "./result/clipboard/clipboard.csv"]
        for file_name in files:
            table_slides = self.add_table_from_csv(prs, file_name, './report_background.png')
        
        self.add_text_from_files(prs, './result/clipboard/html', 'clipboard/html', './report_background.png')
        self.add_text_from_file(prs, './result/shared_prefs/com.projectstar.ishredder.android.standard.txt', 'ishredder.txt', './report_background.png')
        signal+=10
        self.progress_signal.emit(signal)
        # ... 기타 콘텐츠 추가 코드 ...
        
        #add_images_from_folder(prs, './result/clipboard/image')

        #add_shreddit_images(prs, './result/com.palmtronix.shreddit.v1/')

        # 'result/clipboard/image' 폴더의 이미지 처리
        self.add_images_with_names(prs, "./result/clipboard/image", "clipboard image", './report_background.png')
        signal+=10
        self.progress_signal.emit(signal)
        # 'result/com.palmtronix.shreddit.v1' 폴더의 이미지 처리
        self.add_images_with_names(prs, "./result/cache/com.palmtronix.shreddit.v1", "shreddit cache image", './report_background.png')
        signal+=10
        self.progress_signal.emit(signal)
        # 'result/com.shredder.fileshredder.securewipe' 폴더의 이미지 처리
        self.add_images_with_names(prs, "./result/cache/com.shredder.fileshredder.securewipe", "secure wipe out \n  cache image", './report_background.png')
        signal+=10
        self.progress_signal.emit(signal)
        # 'result/com.shredder.fileshredder.securewipe' 폴더의 이미지 처리
        self.add_images_with_names(prs, "./result/gallery3d_cache", "gallery cache image", './report_background.png')
        signal+=10
        self.progress_signal.emit(signal)
        pptx_path=os.path.join(os.getcwd(), 'Analysis_Report.pptx')
        prs.save(pptx_path)

        # pdf_path = os.path.join(os.getcwd(), 'Analysis_Report.pdf')
        # self.save_as_pdf(pptx_path, pdf_path)
        signal+=10
        self.progress_signal.emit(signal)
        self.result_signal.emit()
        self.finished_signal.emit()

