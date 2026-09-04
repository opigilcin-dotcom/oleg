"""Build the income/expense tracker workbook.

Layout:
- One sheet per month (Январь..Декабрь 2026): income log, expense log
  (with a category dropdown), category subtotals, month totals.
- "Сводка" sheet: pulls each month's totals into one yearly table with a
  running total row and a per-category yearly breakdown.

All totals are formulas (SUM / SUMIF / cross-sheet refs), not hardcoded
numbers, so the sheet recalculates when rows are filled in.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

MONTHS = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
]
YEAR = 2026

CATEGORIES = ["Аудит", "Аренда офиса", "Бензин", "Телефонная связь", "Расходники", "Прочее"]

FONT_NAME = "Arial"
HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
SUBHEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
TOTAL_FILL = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
INPUT_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

INCOME_ROWS = 15   # blank rows available for income entries
EXPENSE_ROWS = 30  # blank rows available for expense entries

INCOME_START = 5
INCOME_END = INCOME_START + INCOME_ROWS - 1        # 19
INCOME_TOTAL_ROW = INCOME_END + 1                  # 20

EXPENSE_HEADER_ROW = INCOME_TOTAL_ROW + 3           # 23
EXPENSE_START = EXPENSE_HEADER_ROW + 1              # 24
EXPENSE_END = EXPENSE_START + EXPENSE_ROWS - 1      # 53
EXPENSE_TOTAL_ROW = EXPENSE_END + 1                 # 54

CATEGORY_BOX_ROW = EXPENSE_TOTAL_ROW + 2            # 56
SUMMARY_ROW = CATEGORY_BOX_ROW + len(CATEGORIES) + 2


def style_title(cell, text):
    cell.value = text
    cell.font = Font(name=FONT_NAME, size=14, bold=True, color="FFFFFF")
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="left", vertical="center")


def style_section(cell, text):
    cell.value = text
    cell.font = Font(name=FONT_NAME, size=11, bold=True)
    cell.fill = SUBHEADER_FILL


def style_col_header(cell, text):
    cell.value = text
    cell.font = Font(name=FONT_NAME, size=10, bold=True)
    cell.fill = SUBHEADER_FILL
    cell.border = BORDER
    cell.alignment = Alignment(horizontal="center")


def build_month_sheet(wb, month_name, with_example=False):
    ws = wb.create_sheet(title=month_name)
    ws.sheet_view.showGridLines = False
    for col, width in zip("ABCD", (14, 26, 34, 16)):
        ws.column_dimensions[col].width = width

    style_title(ws["A1"], f"ДОХОДЫ И РАСХОДЫ — {month_name} {YEAR}")
    ws.merge_cells("A1:D1")
    ws.row_dimensions[1].height = 24

    legend = ws["A2"]
    legend.value = (
        "Жёлтые ячейки — сюда вносить данные (дата, источник/категория, сумма). "
        "Остальное считается само (не трогать)."
    )
    legend.font = Font(name=FONT_NAME, size=9, italic=True, color="7F7F7F")
    ws.merge_cells("A2:D2")

    # --- Income table ---
    style_section(ws["A3"], "ДОХОДЫ")
    ws.merge_cells("A3:D3")
    for col, text in zip("ABC", ("Дата", "Источник (объект)", "Сумма")):
        style_col_header(ws[f"{col}4"], text)

    for r in range(INCOME_START, INCOME_END + 1):
        for col in "ABC":
            ws[f"{col}{r}"].border = BORDER
            ws[f"{col}{r}"].font = Font(name=FONT_NAME, size=10)
            ws[f"{col}{r}"].fill = INPUT_FILL
        ws[f"C{r}"].number_format = "#,##0"

    if with_example:
        ws[f"A{INCOME_START}"] = "15.01"
        ws[f"B{INCOME_START}"] = "Объект №1 (пример — сотрите)"
        ws[f"C{INCOME_START}"] = 250000

    ws[f"A{INCOME_TOTAL_ROW}"] = "ИТОГО ДОХОДЫ"
    ws[f"A{INCOME_TOTAL_ROW}"].font = Font(name=FONT_NAME, bold=True)
    ws.merge_cells(f"A{INCOME_TOTAL_ROW}:B{INCOME_TOTAL_ROW}")
    ws[f"C{INCOME_TOTAL_ROW}"] = f"=SUM(C{INCOME_START}:C{INCOME_END})"
    ws[f"C{INCOME_TOTAL_ROW}"].font = Font(name=FONT_NAME, bold=True)
    ws[f"C{INCOME_TOTAL_ROW}"].number_format = "#,##0"
    for col in "ABC":
        ws[f"{col}{INCOME_TOTAL_ROW}"].fill = TOTAL_FILL
        ws[f"{col}{INCOME_TOTAL_ROW}"].border = BORDER

    # --- Expense table ---
    style_section(ws[f"A{EXPENSE_HEADER_ROW - 1}"], "РАСХОДЫ")
    ws.merge_cells(f"A{EXPENSE_HEADER_ROW - 1}:D{EXPENSE_HEADER_ROW - 1}")
    for col, text in zip("ABCD", ("Дата", "Категория", "Описание", "Сумма")):
        style_col_header(ws[f"{col}{EXPENSE_HEADER_ROW}"], text)

    dv = DataValidation(type="list", formula1=f'"{",".join(CATEGORIES)}"', allow_blank=True)
    ws.add_data_validation(dv)

    for r in range(EXPENSE_START, EXPENSE_END + 1):
        for col in "ABCD":
            ws[f"{col}{r}"].border = BORDER
            ws[f"{col}{r}"].font = Font(name=FONT_NAME, size=10)
            ws[f"{col}{r}"].fill = INPUT_FILL
        ws[f"D{r}"].number_format = "#,##0"
        dv.add(ws[f"B{r}"])

    if with_example:
        example_expenses = [
            ("05.01", "Аренда офиса", "Аренда за январь (пример — сотрите)", 60000),
            ("10.01", "Бензин", "Заправка служебной машины (пример — сотрите)", 8000),
            ("20.01", "Аудит", "Ежемесячный аудит (пример — сотрите)", 15000),
        ]
        for i, (date, cat, desc, amount) in enumerate(example_expenses):
            r = EXPENSE_START + i
            ws[f"A{r}"] = date
            ws[f"B{r}"] = cat
            ws[f"C{r}"] = desc
            ws[f"D{r}"] = amount

    ws[f"A{EXPENSE_TOTAL_ROW}"] = "ИТОГО РАСХОДЫ"
    ws[f"A{EXPENSE_TOTAL_ROW}"].font = Font(name=FONT_NAME, bold=True)
    ws.merge_cells(f"A{EXPENSE_TOTAL_ROW}:C{EXPENSE_TOTAL_ROW}")
    ws[f"D{EXPENSE_TOTAL_ROW}"] = f"=SUM(D{EXPENSE_START}:D{EXPENSE_END})"
    ws[f"D{EXPENSE_TOTAL_ROW}"].font = Font(name=FONT_NAME, bold=True)
    ws[f"D{EXPENSE_TOTAL_ROW}"].number_format = "#,##0"
    for col in "ABCD":
        ws[f"{col}{EXPENSE_TOTAL_ROW}"].fill = TOTAL_FILL
        ws[f"{col}{EXPENSE_TOTAL_ROW}"].border = BORDER

    # --- Category breakdown box ---
    style_section(ws[f"A{CATEGORY_BOX_ROW - 1}"], "РАСХОДЫ ПО КАТЕГОРИЯМ")
    ws.merge_cells(f"A{CATEGORY_BOX_ROW - 1}:B{CATEGORY_BOX_ROW - 1}")
    for i, cat in enumerate(CATEGORIES):
        r = CATEGORY_BOX_ROW + i
        ws[f"A{r}"] = cat
        ws[f"A{r}"].font = Font(name=FONT_NAME, size=10)
        ws[f"A{r}"].border = BORDER
        ws[f"B{r}"] = f'=SUMIF(B{EXPENSE_START}:B{EXPENSE_END},A{r},D{EXPENSE_START}:D{EXPENSE_END})'
        ws[f"B{r}"].number_format = "#,##0"
        ws[f"B{r}"].border = BORDER
        ws[f"B{r}"].font = Font(name=FONT_NAME, size=10)

    # --- Month summary ---
    style_section(ws[f"A{SUMMARY_ROW}"], "ИТОГ ЗА МЕСЯЦ")
    ws.merge_cells(f"A{SUMMARY_ROW}:B{SUMMARY_ROW}")
    ws[f"A{SUMMARY_ROW + 1}"] = "Доходы"
    ws[f"B{SUMMARY_ROW + 1}"] = f"=C{INCOME_TOTAL_ROW}"
    ws[f"A{SUMMARY_ROW + 2}"] = "Расходы"
    ws[f"B{SUMMARY_ROW + 2}"] = f"=D{EXPENSE_TOTAL_ROW}"
    ws[f"A{SUMMARY_ROW + 3}"] = "Прибыль / убыток"
    ws[f"B{SUMMARY_ROW + 3}"] = f"=B{SUMMARY_ROW + 1}-B{SUMMARY_ROW + 2}"
    for i in range(1, 4):
        ws[f"A{SUMMARY_ROW + i}"].font = Font(name=FONT_NAME, bold=(i == 3))
        ws[f"B{SUMMARY_ROW + i}"].font = Font(name=FONT_NAME, bold=(i == 3))
        ws[f"B{SUMMARY_ROW + i}"].number_format = "#,##0"
        ws[f"A{SUMMARY_ROW + i}"].border = BORDER
        ws[f"B{SUMMARY_ROW + i}"].border = BORDER
    ws[f"A{SUMMARY_ROW + 3}"].fill = TOTAL_FILL
    ws[f"B{SUMMARY_ROW + 3}"].fill = TOTAL_FILL

    return {
        "income_total_cell": f"'{month_name}'!C{INCOME_TOTAL_ROW}",
        "expense_total_cell": f"'{month_name}'!D{EXPENSE_TOTAL_ROW}",
        "category_cells": {
            cat: f"'{month_name}'!B{CATEGORY_BOX_ROW + i}" for i, cat in enumerate(CATEGORIES)
        },
    }


def build_dashboard(wb, month_refs):
    ws = wb.create_sheet(title="Сводка", index=0)
    ws.sheet_view.showGridLines = False
    widths = [16] + [16] * len(CATEGORIES) + [16, 16, 16]
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(i + 1)].width = w

    style_title(ws["A1"], f"СВОДКА ЗА {YEAR} ГОД")
    last_col = 1 + len(CATEGORIES) + 3
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=last_col)
    ws.row_dimensions[1].height = 24

    headers = ["Месяц"] + CATEGORIES + ["Доход", "Расход", "Прибыль"]
    for i, h in enumerate(headers):
        c = ws.cell(row=3, column=i + 1)
        style_col_header(c, h)

    first_data_row = 4
    for i, month in enumerate(MONTHS):
        r = first_data_row + i
        refs = month_refs[month]
        ws.cell(row=r, column=1, value=month).font = Font(name=FONT_NAME)
        ws.cell(row=r, column=1).border = BORDER
        for j, cat in enumerate(CATEGORIES):
            cell = ws.cell(row=r, column=2 + j)
            cell.value = f"={refs['category_cells'][cat]}"
            cell.number_format = "#,##0"
            cell.border = BORDER
            cell.font = Font(name=FONT_NAME, size=10)
        income_col = 2 + len(CATEGORIES)
        expense_col = income_col + 1
        profit_col = expense_col + 1
        ic = ws.cell(row=r, column=income_col)
        ic.value = f"={refs['income_total_cell']}"
        ic.number_format = "#,##0"
        ic.border = BORDER
        ec = ws.cell(row=r, column=expense_col)
        ec.value = f"={refs['expense_total_cell']}"
        ec.number_format = "#,##0"
        ec.border = BORDER
        pc = ws.cell(row=r, column=profit_col)
        ic_letter = get_column_letter(income_col)
        ec_letter = get_column_letter(expense_col)
        pc.value = f"={ic_letter}{r}-{ec_letter}{r}"
        pc.number_format = "#,##0"
        pc.border = BORDER
        pc.font = Font(name=FONT_NAME, size=10, bold=True)

    total_row = first_data_row + len(MONTHS)
    ws.cell(row=total_row, column=1, value="ИТОГО ЗА ГОД").font = Font(name=FONT_NAME, bold=True)
    ws.cell(row=total_row, column=1).fill = TOTAL_FILL
    ws.cell(row=total_row, column=1).border = BORDER
    for col in range(2, last_col + 1):
        letter = get_column_letter(col)
        cell = ws.cell(row=total_row, column=col)
        cell.value = f"=SUM({letter}{first_data_row}:{letter}{total_row - 1})"
        cell.number_format = "#,##0"
        cell.font = Font(name=FONT_NAME, bold=True)
        cell.fill = TOTAL_FILL
        cell.border = BORDER

    ws.freeze_panes = "B4"
    return ws


def main():
    wb = Workbook()
    wb.remove(wb.active)  # drop the default blank sheet; dashboard is inserted at index 0 later

    month_refs = {}
    for month in MONTHS:
        month_refs[month] = build_month_sheet(wb, month, with_example=(month == "Январь"))

    build_dashboard(wb, month_refs)

    out_path = "/home/user/oleg/finance/доходы-расходы-2026.xlsx"
    wb.save(out_path)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
