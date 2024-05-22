from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from .utils import calculate_mean_served_requests
import io

def export_to_pdf(results):
    """
    Экспортирует результаты симуляции в PDF-файл.

    ### Параметры:
    * `results (list)` - Список результатов симуляции.

    ### Возвращает:
    * `pdf_content (bytes)` - Содержимое PDF-файла в виде байтового объекта.
    """
    # Регистрация шрифта Arial для поддержки кириллицы
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

    # Получение стандартных стилей и добавление стилей для кириллицы
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Cyrillic', fontName='Arial', fontSize=10))
    styles.add(ParagraphStyle(name='CyrillicHeading3', fontName='Arial', fontSize=12, spaceAfter=6))

    # Создание байтового объекта для записи PDF
    pdf_bytes = io.BytesIO()

    # Создание документа PDF с указанным размером страницы и кодировкой
    doc = SimpleDocTemplate(pdf_bytes, pagesize=letter, encoding='UTF-8')
    elements = []

    for i, result in enumerate(results, start=1):
        # Добавление заголовка для каждой симуляции
        header = Paragraph(f"----------------------------------------- Симуляция номер: {i} -----------------------------------------", styles["CyrillicHeading3"])
        elements.append(header)

        # Подготовка данных для таблицы
        table_data = [["Индекс", "Случайное число", "МЕЖ", "Время в очереди", "Сервер 1", "Сервер 2", "Сервер 3", "Обслужено", "Отказов"]]
        for entry in result.request_times:
            row = [entry["index"], entry["rand_value"], entry["iba"], entry["app_time"]]
            for j in range(1, 4):
                row.append(entry[f"server_{j}"])
            row.extend([entry["Обслужено"], entry["Отказов"]])
            table_data.append(row)

        # Создание таблицы и установка стилей
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        elements.append(table)

        # Добавление итогов для каждой симуляции
        served_count = Paragraph(f"Количество исполненных заявок: {result.served_requests}", styles["Cyrillic"])
        rejected_count = Paragraph(f"Количество отказов: {result.rejected_requests}", styles["Cyrillic"])
        elements.append(served_count)
        elements.append(rejected_count)
        elements.append(Spacer(1, 0.5 * inch))  # Добавление отступа между симуляциями

    # Добавление среднего количества обслуженных заявок в конце документа
    mean_served = Paragraph(f"В качестве оценки искомого математического ожидания a – числа обслуженных заявок примем выборочную среднюю: a = {calculate_mean_served_requests(results)}", styles["Cyrillic"])
    elements.append(mean_served)

    # Построение и сохранение PDF документа
    doc.build(elements)

    # Получение содержимого PDF в виде байтов
    pdf_bytes.seek(0)  # Перематываем объект BytesIO в начало
    pdf_content = pdf_bytes.getvalue()

    return pdf_content
