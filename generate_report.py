from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from main import HashTable
import os
import sys

# Устанавливаем кодировку для вывода в консоль
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def create_report(filename="hash_table_report.pdf"):
    """Создание подробного PDF отчета о реализации хеш-таблицы"""
    
    # Регистрация шрифта Arial для поддержки русского языка
    pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\arial.ttf'))
    
    # Создаем документ формата A4
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Создаем стили с Arial
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomHeading',
        fontName='Arial',
        fontSize=14,
        leading=18,
        alignment=TA_LEFT,
        spaceBefore=20,
        spaceAfter=10
    ))
    
    styles.add(ParagraphStyle(
        name='CustomBody',
        fontName='Arial',
        fontSize=12,
        leading=16,
        alignment=TA_JUSTIFY
    ))
    
    story = []
    
    # Введение
    story.append(Paragraph("1. Постановка задачи", styles['CustomHeading']))
    story.append(Paragraph("""
        Целью данной работы является реализация хеш-таблицы со следующими характеристиками:
        <br/><br/>
        • Тип ключа: строковый (вариант 1б)
        <br/>
        • Метод хеширования: метод умножения (вариант 2б)
        <br/>
        • Разрешение коллизий: метод внешних цепочек (вариант 3а)
        <br/>
        • Размер таблицы: 16 элементов (2^4)
    """, styles['CustomBody']))
    
    # Теоретическая часть
    story.append(Paragraph("2. Теоретические сведения", styles['CustomHeading']))
    story.append(Paragraph("""
        <b>2.1 Метод умножения для хеширования</b>
        <br/><br/>
        Метод умножения использует формулу: h(k) = ⌊M(kA mod 1)⌋
        где:
        <br/>
        • k - числовое представление ключа
        <br/>
        • A = (√5-1)/2 ≈ 0.6180339887498949 (золотое сечение)
        <br/>
        • M = 16 (размер таблицы)
        <br/><br/>
        <b>2.2 Преобразование строкового ключа</b>
        <br/><br/>
        Для преобразования строкового ключа в число используется полиномиальная функция:
        k = sum(ord(символ) * (31^i)) для каждого символа
        <br/><br/>
        <b>2.3 Метод внешних цепочек</b>
        <br/><br/>
        При возникновении коллизии новый элемент добавляется в связный список, 
        хранящийся в соответствующей ячейке таблицы.
    """, styles['CustomBody']))
    
    # Практическая часть
    story.append(Paragraph("3. Практическая реализация", styles['CustomHeading']))
    
    # Создаем хеш-таблицу и тестовые данные
    hash_table = HashTable(16)
    test_keys = ["test1", "test2", "test3", "test4", "test5", 
                 "test6", "test7", "test1", "test8", "test2"]
    
    # Таблица результатов вставки
    insertion_data = []
    insertion_data.append(["Ключ", "Хеш-значение", "Успех вставки", "Коллизии"])
    
    for key in test_keys:
        hash_value = hash_table.hash_function(key)
        success = hash_table.insert(key)
        _, node = hash_table.search(key)
        collisions = node.collisions if node else "Н/Д"
        insertion_data.append([key, hash_value, "Да" if success else "Нет", collisions])
    
    story.append(Paragraph("3.1 Результаты вставки ключей:", styles['CustomHeading']))
    
    # Создаем таблицу с результатами
    t = Table(insertion_data, colWidths=[100, 100, 100, 80])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 20))
    
    # Демонстрация поиска
    story.append(Paragraph("3.2 Тестирование поиска:", styles['CustomHeading']))
    search_keys = ["test1", "test2", "test9"]
    
    search_results = []
    for key in search_keys:
        index, node = hash_table.search(key)
        if node:
            result = f"Найден по индексу {index}, коллизий: {node.collisions}"
        else:
            result = "Не найден"
        search_results.append([key, result])
    
    search_table = Table([["Ключ", "Результат"]] + search_results, colWidths=[100, 280])
    search_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
    ]))
    
    story.append(search_table)
    
    # Заключение
    story.append(Paragraph("4. Заключение", styles['CustomHeading']))
    story.append(Paragraph("""
        В ходе выполнения работы была реализована хеш-таблица с использованием метода 
        умножения для хеширования и метода внешних цепочек для разрешения коллизий. 
        <br/><br/>
        Тестирование показало, что:
        <br/>
        • Реализованный алгоритм успешно обрабатывает как уникальные, так и повторяющиеся ключи
        <br/>
        • Коллизии эффективно разрешаются с помощью метода внешних цепочек
        <br/>
        • Поиск элементов работает корректно как для существующих, так и для отсутствующих ключей
        <br/><br/>
        Реализованная структура данных может быть использована для эффективного хранения 
        и поиска данных со строковыми ключами.
    """.encode('utf-8').decode('utf-8'), styles['CustomBody']))
    
    # Создаем PDF
    doc.build(story)
    
    print(f"Report generated: {os.path.abspath(filename)}")

if __name__ == "__main__":
    create_report() 