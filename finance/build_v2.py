"""Build the v2 finance tracker: single ledger + dashboard + in-sheet entry form.

Sheets:
- "Операции"   — master ledger, one row per transaction (grows forever).
- "Категории"  — Категория | Тип (Постоянные/Переменные) — expense categories
                 with their dashboard tier, feeds dropdowns.
- "Контрагенты"— counterparty list, feeds dropdown, extendable via the Форма.
- "Показатели" — month-picker dashboard (SUMIFS over Операции).
- "Форма"      — data-entry panel. Checkboxes are plain TRUE/FALSE cells here;
                 after import, replace them with real Google Sheets checkboxes
                 (Insert -> Checkbox) — openpyxl/xlsx has no equivalent widget.
"""

import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

FONT_NAME = "Arial"
HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
SUBHEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
INCOME_FILL = PatternFill(start_color="2E7D32", end_color="2E7D32", fill_type="solid")
EXPENSE_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
INPUT_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
TOTAL_FILL = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

MONTHS = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
]

# category -> tier ("Постоянные" or "Переменные"), matches the reference
# lists on the old "Техничка" sheet, with "Затраты доп" folded into
# "Переменные" (that's how they were grouped on the "Показатели" dashboard).
EXPENSE_CATEGORIES = [
    ("Аренда", "Постоянные"),
    ("Связь (мобильная)", "Постоянные"),
    ("Инкассация", "Постоянные"),
    ("Аудит", "Переменные"),
    ("Налоги", "Переменные"),
    ("Соц. взносы", "Переменные"),
    ("ФОТ", "Переменные"),
    ("Рекламные расходы", "Переменные"),
    ("Выравнивание кассы", "Переменные"),
    ("Канцелярия", "Переменные"),
    ("Оборудование", "Переменные"),
    ("Расходники", "Переменные"),
    ("Бензин", "Переменные"),
    ("Прочий расход", "Переменные"),
    ("Переводы между счетами", "Переменные"),
]
INCOME_CATEGORIES = [
    "Заказы", "Размещение рекламы", "Переводы между счетами", "Выравнивание кассы",
]
PAYMENT_METHODS = ["Наличные", "Безналичные"]
EXAMPLE_CONTRACTORS = ["Rawai House 3bdr", "Дом Бангтао", "AIS"]

# --- Операции columns ---
COL_DATE, COL_TYPE, COL_CATEGORY, COL_COUNTERPARTY, COL_METHOD, COL_AMOUNT, COL_COMMENT = range(1, 8)
LEDGER_HEADER_ROW = 1
LEDGER_FIRST_DATA_ROW = 2
LEDGER_RESERVED_ROWS = 500  # pre-formatted rows; the ledger can grow past this, formulas use whole-column refs


def style_title(cell, text, fill=HEADER_FILL):
    cell.value = text
    cell.font = Font(name=FONT_NAME, size=13, bold=True, color="FFFFFF")
    cell.fill = fill
    cell.alignment = Alignment(horizontal="left", vertical="center")


def style_header(cell, text):
    cell.value = text
    cell.font = Font(name=FONT_NAME, size=10, bold=True)
    cell.fill = SUBHEADER_FILL
    cell.border = BORDER
    cell.alignment = Alignment(horizontal="center", wrap_text=True)


def build_ledger_sheet(wb):
    ws = wb.create_sheet("Операции")
    ws.sheet_view.showGridLines = False
    widths = [12, 10, 22, 20, 14, 12, 30]
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(i + 1)].width = w

    headers = ["Дата", "Тип", "Статья", "Контрагент", "Вид платежа", "Сумма", "Комментарий"]
    for i, h in enumerate(headers):
        style_header(ws.cell(row=LEDGER_HEADER_ROW, column=i + 1), h)
    ws.freeze_panes = "A2"

    for r in range(LEDGER_FIRST_DATA_ROW, LEDGER_FIRST_DATA_ROW + LEDGER_RESERVED_ROWS):
        for c in range(1, 8):
            cell = ws.cell(row=r, column=c)
            cell.border = BORDER
            cell.font = Font(name=FONT_NAME, size=10)
        ws.cell(row=r, column=COL_AMOUNT).number_format = "#,##0"
        ws.cell(row=r, column=COL_DATE).number_format = "DD.MM.YYYY"

    # One example row so the format is obvious; delete before real use.
    # NOTE: date must be a real date value (not text) or the SUMIFS date
    # comparisons on the "Показатели" sheet won't match it.
    example_row = LEDGER_FIRST_DATA_ROW
    ws.cell(row=example_row, column=COL_DATE, value=datetime.date(2026, 2, 1))
    ws.cell(row=example_row, column=COL_TYPE, value="Расход")
    ws.cell(row=example_row, column=COL_CATEGORY, value="Аудит")
    ws.cell(row=example_row, column=COL_COUNTERPARTY, value="")
    ws.cell(row=example_row, column=COL_METHOD, value="Безналичные")
    ws.cell(row=example_row, column=COL_AMOUNT, value=70450)
    ws.cell(row=example_row, column=COL_COMMENT, value="пример — сотрите")

    type_dv = DataValidation(type="list", formula1='"Доход,Расход"', allow_blank=True)
    ws.add_data_validation(type_dv)
    type_dv.add(f"B{LEDGER_FIRST_DATA_ROW}:B{LEDGER_FIRST_DATA_ROW + LEDGER_RESERVED_ROWS}")

    method_dv = DataValidation(type="list", formula1=f'"{",".join(PAYMENT_METHODS)}"', allow_blank=True)
    ws.add_data_validation(method_dv)
    method_dv.add(f"E{LEDGER_FIRST_DATA_ROW}:E{LEDGER_FIRST_DATA_ROW + LEDGER_RESERVED_ROWS}")

    return ws


def build_categories_sheet(wb):
    ws = wb.create_sheet("Категории")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["D"].width = 26

    style_header(ws["A1"], "Статья расхода")
    style_header(ws["B1"], "Тип (для дашборда)")
    for i, (cat, tier) in enumerate(EXPENSE_CATEGORIES):
        r = i + 2
        ws.cell(row=r, column=1, value=cat).border = BORDER
        ws.cell(row=r, column=2, value=tier).border = BORDER
        ws.cell(row=r, column=1).font = Font(name=FONT_NAME, size=10)
        ws.cell(row=r, column=2).font = Font(name=FONT_NAME, size=10)

    style_header(ws["D1"], "Статья дохода")
    for i, cat in enumerate(INCOME_CATEGORIES):
        r = i + 2
        ws.cell(row=r, column=4, value=cat).border = BORDER
        ws.cell(row=r, column=4).font = Font(name=FONT_NAME, size=10)

    return ws, len(EXPENSE_CATEGORIES), len(INCOME_CATEGORIES)


def build_contractors_sheet(wb):
    ws = wb.create_sheet("Контрагенты")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 30
    style_header(ws["A1"], "Контрагент")
    for i, name in enumerate(EXAMPLE_CONTRACTORS):
        ws.cell(row=i + 2, column=1, value=name).border = BORDER
        ws.cell(row=i + 2, column=1).font = Font(name=FONT_NAME, size=10)
    return ws


def build_dashboard(wb, n_expense_cats, n_income_cats):
    ws = wb.create_sheet("Показатели", index=0)
    ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDE", (24, 14, 24, 14, 24)):
        ws.column_dimensions[col].width = w

    style_title(ws["A1"], "ПОКАЗАТЕЛИ")
    ws.merge_cells("A1:E1")

    ws["A2"] = "Выберите месяц:"
    ws["A2"].font = Font(name=FONT_NAME, bold=True)
    ws["B2"] = MONTHS[0]
    ws["B2"].fill = INPUT_FILL
    ws["B2"].border = BORDER
    month_dv = DataValidation(type="list", formula1=f'"{",".join(MONTHS)}"', allow_blank=False)
    ws.add_data_validation(month_dv)
    month_dv.add("B2")

    ledger_last = f"Операции!A{LEDGER_FIRST_DATA_ROW + LEDGER_RESERVED_ROWS}"
    date_range = f"Операции!$A${LEDGER_FIRST_DATA_ROW}:$A${LEDGER_FIRST_DATA_ROW + LEDGER_RESERVED_ROWS}"
    type_range = f"Операции!$B${LEDGER_FIRST_DATA_ROW}:$B${LEDGER_FIRST_DATA_ROW + LEDGER_RESERVED_ROWS}"
    cat_range = f"Операции!$C${LEDGER_FIRST_DATA_ROW}:$C${LEDGER_FIRST_DATA_ROW + LEDGER_RESERVED_ROWS}"
    amt_range = f"Операции!$F${LEDGER_FIRST_DATA_ROW}:$F${LEDGER_FIRST_DATA_ROW + LEDGER_RESERVED_ROWS}"

    # month-of(date) matched via TEXT(date,"MMMM") is locale-dependent, so we
    # instead compare MONTH(date) to the position of the chosen name in MONTHS.
    month_num = "MATCH($B$2,{" + ",".join(f'"{m}"' for m in MONTHS) + "},0)"

    def month_sumifs(extra_criteria_range=None, extra_criteria=None, type_value=None):
        parts = [amt_range, date_range, f"\">=\"&DATE(YEAR(TODAY()),{month_num},1)",
                 date_range, f"\"<\"&EDATE(DATE(YEAR(TODAY()),{month_num},1),1)"]
        if type_value:
            parts += [type_range, f'"{type_value}"']
        if extra_criteria_range and extra_criteria:
            parts += [extra_criteria_range, extra_criteria]
        return "SUMIFS(" + ",".join(parts) + ")"

    row = 4
    style_title(ws.cell(row=row, column=1), "Постоянные расходы", fill=EXPENSE_FILL)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    fixed_cats = [c for c, t in EXPENSE_CATEGORIES if t == "Постоянные"]
    fixed_start = row + 1
    for i, cat in enumerate(fixed_cats):
        r = fixed_start + i
        ws.cell(row=r, column=1, value=cat).border = BORDER
        ws.cell(row=r, column=1).font = Font(name=FONT_NAME, size=10)
        c = ws.cell(row=r, column=2)
        c.value = f'={month_sumifs(cat_range, f"$A{r}", "Расход")}'
        c.number_format = "#,##0"
        c.border = BORDER
        c.font = Font(name=FONT_NAME, size=10)
    fixed_end = fixed_start + len(fixed_cats) - 1
    fixed_total_row = fixed_end + 1
    ws.cell(row=fixed_total_row, column=1, value="ИТОГО Постоянные").font = Font(name=FONT_NAME, bold=True)
    ws.cell(row=fixed_total_row, column=1).fill = TOTAL_FILL
    ws.cell(row=fixed_total_row, column=1).border = BORDER
    tc = ws.cell(row=fixed_total_row, column=2)
    tc.value = f"=SUM(B{fixed_start}:B{fixed_end})"
    tc.number_format = "#,##0"
    tc.font = Font(name=FONT_NAME, bold=True)
    tc.fill = TOTAL_FILL
    tc.border = BORDER

    row2 = 4
    style_title(ws.cell(row=row2, column=3), "Переменные расходы", fill=EXPENSE_FILL)
    ws.merge_cells(start_row=row2, start_column=3, end_row=row2, end_column=4)
    var_cats = [c for c, t in EXPENSE_CATEGORIES if t == "Переменные"]
    var_start = row2 + 1
    for i, cat in enumerate(var_cats):
        r = var_start + i
        ws.cell(row=r, column=3, value=cat).border = BORDER
        ws.cell(row=r, column=3).font = Font(name=FONT_NAME, size=10)
        c = ws.cell(row=r, column=4)
        c.value = f'={month_sumifs(cat_range, f"$C{r}", "Расход")}'
        c.number_format = "#,##0"
        c.border = BORDER
        c.font = Font(name=FONT_NAME, size=10)
    var_end = var_start + len(var_cats) - 1
    var_total_row = var_end + 1
    ws.cell(row=var_total_row, column=3, value="ИТОГО Переменные").font = Font(name=FONT_NAME, bold=True)
    ws.cell(row=var_total_row, column=3).fill = TOTAL_FILL
    ws.cell(row=var_total_row, column=3).border = BORDER
    tc2 = ws.cell(row=var_total_row, column=4)
    tc2.value = f"=SUM(D{var_start}:D{var_end})"
    tc2.number_format = "#,##0"
    tc2.font = Font(name=FONT_NAME, bold=True)
    tc2.fill = TOTAL_FILL
    tc2.border = BORDER

    income_col_letter = "E"
    style_title(ws.cell(row=4, column=5), "Доходы", fill=INCOME_FILL)
    inc_start = 5
    for i, cat in enumerate(INCOME_CATEGORIES):
        r = inc_start + i
        ws.cell(row=r, column=5, value=cat).border = BORDER
        ws.cell(row=r, column=5).font = Font(name=FONT_NAME, size=10)
    # amounts one column further right (F), keep category label in E
    ws.column_dimensions["F"].width = 14
    for i, cat in enumerate(INCOME_CATEGORIES):
        r = inc_start + i
        c = ws.cell(row=r, column=6)
        c.value = f'={month_sumifs(cat_range, f"$E{r}", "Доход")}'
        c.number_format = "#,##0"
        c.border = BORDER
        c.font = Font(name=FONT_NAME, size=10)
    inc_end = inc_start + len(INCOME_CATEGORIES) - 1
    inc_total_row = inc_end + 1
    ws.cell(row=inc_total_row, column=5, value="ИТОГО Доходы").font = Font(name=FONT_NAME, bold=True)
    ws.cell(row=inc_total_row, column=5).fill = TOTAL_FILL
    ws.cell(row=inc_total_row, column=5).border = BORDER
    tc3 = ws.cell(row=inc_total_row, column=6)
    tc3.value = f"=SUM(F{inc_start}:F{inc_end})"
    tc3.number_format = "#,##0"
    tc3.font = Font(name=FONT_NAME, bold=True)
    tc3.fill = TOTAL_FILL
    tc3.border = BORDER

    summary_row = max(fixed_total_row, var_total_row, inc_total_row) + 2
    style_title(ws.cell(row=summary_row, column=1), "ИТОГ ЗА МЕСЯЦ", fill=HEADER_FILL)
    ws.merge_cells(start_row=summary_row, start_column=1, end_row=summary_row, end_column=2)
    labels = ["Выручка (доходы)", "Постоянные затраты", "Переменные затраты", "Общий расход", "Прибыль / убыток"]
    formulas = [
        f"=F{inc_total_row}",
        f"=B{fixed_total_row}",
        f"=D{var_total_row}",
        f"=B{fixed_total_row}+D{var_total_row}",
        f"=F{inc_total_row}-(B{fixed_total_row}+D{var_total_row})",
    ]
    for i, (label, formula) in enumerate(zip(labels, formulas)):
        r = summary_row + 1 + i
        ws.cell(row=r, column=1, value=label).border = BORDER
        ws.cell(row=r, column=1).font = Font(name=FONT_NAME, bold=(i == len(labels) - 1))
        c = ws.cell(row=r, column=2)
        c.value = formula
        c.number_format = "#,##0"
        c.border = BORDER
        c.font = Font(name=FONT_NAME, bold=(i == len(labels) - 1))
        if i == len(labels) - 1:
            c.fill = TOTAL_FILL
            ws.cell(row=r, column=1).fill = TOTAL_FILL

    return ws


def build_form_sheet(wb):
    ws = wb.create_sheet("Форма")
    ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFG", (20, 22, 4, 20, 22, 4, 30)):
        ws.column_dimensions[col].width = w

    style_title(ws["A1"], "ДОХОДЫ", fill=INCOME_FILL)
    ws.merge_cells("A1:C1")
    fields_income = ["Статья дохода", "Сумма", "Вид платежа", "Контрагент (необязательно)", "Комментарий"]
    for i, label in enumerate(fields_income):
        r = 2 + i
        ws.cell(row=r, column=1, value=label).font = Font(name=FONT_NAME, size=10)
        cell = ws.cell(row=r, column=2)
        cell.fill = INPUT_FILL
        cell.border = BORDER
    income_dv = DataValidation(type="list", formula1="Категории!$D$2:$D$100", allow_blank=True)
    ws.add_data_validation(income_dv)
    income_dv.add("B2")
    method_dv1 = DataValidation(type="list", formula1=f'"{",".join(PAYMENT_METHODS)}"', allow_blank=True)
    ws.add_data_validation(method_dv1)
    method_dv1.add("B4")
    contractor_dv1 = DataValidation(type="list", formula1="Контрагенты!$A$2:$A$200", allow_blank=True)
    ws.add_data_validation(contractor_dv1)
    contractor_dv1.add("B5")

    ws["A7"] = "Занести приход"
    ws["A7"].font = Font(name=FONT_NAME, bold=True)
    ws["B7"] = False
    ws["B7"].fill = INPUT_FILL
    ws["B7"].border = BORDER
    ws["C7"] = "← после импорта: выделить, Вставка → Флажок"
    ws["C7"].font = Font(name=FONT_NAME, size=8, italic=True, color="7F7F7F")

    style_title(ws["A9"], "РАСХОДЫ", fill=EXPENSE_FILL)
    ws.merge_cells("A9:C9")
    fields_expense = ["Статья расхода", "Сумма", "Вид платежа", "Контрагент", "Комментарий / основание"]
    for i, label in enumerate(fields_expense):
        r = 10 + i
        ws.cell(row=r, column=1, value=label).font = Font(name=FONT_NAME, size=10)
        cell = ws.cell(row=r, column=2)
        cell.fill = INPUT_FILL
        cell.border = BORDER
    expense_dv = DataValidation(type="list", formula1="Категории!$A$2:$A$100", allow_blank=True)
    ws.add_data_validation(expense_dv)
    expense_dv.add("B10")
    method_dv2 = DataValidation(type="list", formula1=f'"{",".join(PAYMENT_METHODS)}"', allow_blank=True)
    ws.add_data_validation(method_dv2)
    method_dv2.add("B12")
    contractor_dv2 = DataValidation(type="list", formula1="Контрагенты!$A$2:$A$200", allow_blank=True)
    ws.add_data_validation(contractor_dv2)
    contractor_dv2.add("B13")

    ws["A15"] = "Занести расход"
    ws["A15"].font = Font(name=FONT_NAME, bold=True)
    ws["B15"] = False
    ws["B15"].fill = INPUT_FILL
    ws["B15"].border = BORDER
    ws["C15"] = "← после импорта: выделить, Вставка → Флажок"
    ws["C15"].font = Font(name=FONT_NAME, size=8, italic=True, color="7F7F7F")

    style_title(ws["A17"], "ДАТА ОПЕРАЦИИ", fill=HEADER_FILL)
    ws.merge_cells("A17:B17")
    ws["A18"] = "Дата (по умолчанию — сегодня)"
    ws["A18"].font = Font(name=FONT_NAME, size=10)
    ws["B18"] = "=TODAY()"
    ws["B18"].number_format = "DD.MM.YYYY"
    ws["B18"].fill = INPUT_FILL
    ws["B18"].border = BORDER

    style_title(ws["D17"], "НОВЫЙ КОНТРАГЕНТ", fill=HEADER_FILL)
    ws.merge_cells("D17:E17")
    ws["D18"] = "Название"
    ws["D18"].font = Font(name=FONT_NAME, size=10)
    ws["E18"] = ""
    ws["E18"].fill = INPUT_FILL
    ws["E18"].border = BORDER
    ws["D19"] = "Добавить"
    ws["D19"].font = Font(name=FONT_NAME, bold=True)
    ws["E19"] = False
    ws["E19"].fill = INPUT_FILL
    ws["E19"].border = BORDER
    ws["D20"] = "← после импорта: Вставка → Флажок"
    ws["D20"].font = Font(name=FONT_NAME, size=8, italic=True, color="7F7F7F")

    style_title(ws["A21"], "БАЛАНС (по всем операциям)", fill=HEADER_FILL)
    ws.merge_cells("A21:B21")
    ws["A22"] = "Баланс нал"
    ws["A22"].font = Font(name=FONT_NAME, bold=True)
    ws["B22"] = (
        '=SUMIFS(Операции!$F:$F,Операции!$B:$B,"Доход",Операции!$E:$E,"Наличные")'
        '-SUMIFS(Операции!$F:$F,Операции!$B:$B,"Расход",Операции!$E:$E,"Наличные")'
    )
    ws["B22"].number_format = "#,##0"
    ws["A23"] = "Баланс безнал"
    ws["A23"].font = Font(name=FONT_NAME, bold=True)
    ws["B23"] = (
        '=SUMIFS(Операции!$F:$F,Операции!$B:$B,"Доход",Операции!$E:$E,"Безналичные")'
        '-SUMIFS(Операции!$F:$F,Операции!$B:$B,"Расход",Операции!$E:$E,"Безналичные")'
    )
    ws["B23"].number_format = "#,##0"
    for cell in (ws["A22"], ws["B22"], ws["A23"], ws["B23"]):
        cell.border = BORDER

    style_title(ws["A25"], "ПОСЛЕДНИЕ 5 ЗАПИСЕЙ", fill=HEADER_FILL)
    ws.merge_cells("A25:G25")
    last5_headers = ["Дата", "Тип", "Статья", "Контрагент", "Вид платежа", "Сумма", "Комментарий"]
    for i, h in enumerate(last5_headers):
        style_header(ws.cell(row=26, column=i + 1), h)
    for r in range(27, 32):
        for c in range(1, 8):
            cell = ws.cell(row=r, column=c)
            cell.border = BORDER
            cell.font = Font(name=FONT_NAME, size=10)
    ws["A33"] = "(заполняется автоматически скриптом после каждой записи)"
    ws["A33"].font = Font(name=FONT_NAME, size=8, italic=True, color="7F7F7F")

    return ws


def main():
    wb = Workbook()
    wb.remove(wb.active)

    cat_ws, n_exp, n_inc = build_categories_sheet(wb)
    build_contractors_sheet(wb)
    build_ledger_sheet(wb)
    build_dashboard(wb, n_exp, n_inc)
    build_form_sheet(wb)

    wb.move_sheet("Показатели", offset=-len(wb.sheetnames))

    out_path = "/home/user/oleg/finance/финансы-2026.xlsx"
    wb.save(out_path)
    print("Saved:", out_path)


if __name__ == "__main__":
    main()
