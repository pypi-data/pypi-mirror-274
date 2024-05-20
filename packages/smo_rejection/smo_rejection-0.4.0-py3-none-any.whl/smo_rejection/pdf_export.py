from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from .utils import calculate_mean_served_requests

def export_to_pdf(results, filename):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    for i, result in enumerate(results, start=1):
        header = f"---------------------------- Cимуляция номер: {i} ----------------------------"
        elements.append(header)

        table_data = [["index", "rand_value", "iba", "app_time", "server_1", "server_2", "server_3", "Обслужено", "Отказов"]]
        for entry in result.request_times:
            row = [entry["index"], entry["rand_value"], entry["iba"], entry["app_time"]]
            for j in range(1, 4):
                row.append(entry[f"server_{j}"])
            row.extend([entry["Обслужено"], entry["Отказов"]])
            table_data.append(row)

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        elements.append(table)

        served_count = f"Количество исполненных заявок: {result.served_requests}"
        rejected_count = f"Количество отказов: {result.rejected_requests}"
        elements.append(served_count)
        elements.append(rejected_count)
        elements.append(Spacer(1, 0.5 * inch))

    mean_served = f"В качестве оценки искомого математического ожидания a – числа обслуженных заявок примем выборочную среднюю: a = {calculate_mean_served_requests(results)}"
    elements.append(mean_served)

    doc.build(elements)