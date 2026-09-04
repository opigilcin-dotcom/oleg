/**
 * Автоматическая раскладка ответов Google Формы по листам
 * "доходы-расходы-2026" (Январь..Декабрь).
 *
 * Установка: Extensions → Apps Script в таблице → вставить этот код →
 * Триггеры (значок часов слева) → Add Trigger →
 *   function: onFormSubmitHandler
 *   event source: From spreadsheet
 *   event type: On form submit
 *
 * Названия вопросов формы должны совпадать один в один со строками ниже
 * (см. ФОРМА-ввода-инструкция.md — там точные тексты для полей формы).
 */

const MONTHS = [
  "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
  "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь",
];

function onFormSubmitHandler(e) {
  const responses = e.namedValues;
  const type = getValue(responses, "Тип записи");
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  if (type === "Доход") {
    addIncomeRow(
      ss,
      getValue(responses, "Дата дохода"),
      getValue(responses, "Источник / объект"),
      getValue(responses, "Сумма дохода")
    );
  } else if (type === "Расход") {
    addExpenseRow(
      ss,
      getValue(responses, "Дата расхода"),
      getValue(responses, "Категория расхода"),
      getValue(responses, "Описание расхода"),
      getValue(responses, "Сумма расхода")
    );
  }
}

function getValue(namedValues, key) {
  return namedValues[key] ? namedValues[key][0] : "";
}

function monthNameFromDateString(dateStr) {
  // Google Forms отдаёт дату как текст "YYYY-MM-DD"
  const parts = String(dateStr).split("-");
  const monthIndex = parseInt(parts[1], 10) - 1;
  return MONTHS[monthIndex];
}

function findRowByLabel(sheet, label) {
  const lastRow = sheet.getLastRow();
  const values = sheet.getRange(1, 1, lastRow, 1).getValues();
  for (let i = 0; i < values.length; i++) {
    if (values[i][0] === label) return i + 1;
  }
  return -1;
}

function addIncomeRow(ss, dateStr, source, amount) {
  const monthName = monthNameFromDateString(dateStr);
  const sheet = ss.getSheetByName(monthName);
  if (!sheet) {
    Logger.log("Лист не найден: " + monthName);
    return;
  }
  const totalRow = findRowByLabel(sheet, "ИТОГО ДОХОДЫ");
  if (totalRow === -1) {
    Logger.log("Не нашёл строку 'ИТОГО ДОХОДЫ' на листе " + monthName);
    return;
  }
  sheet.insertRowBefore(totalRow);
  sheet.getRange(totalRow, 1, 1, 3).setValues([[dateStr, source, Number(amount) || 0]]);
}

function addExpenseRow(ss, dateStr, category, description, amount) {
  const monthName = monthNameFromDateString(dateStr);
  const sheet = ss.getSheetByName(monthName);
  if (!sheet) {
    Logger.log("Лист не найден: " + monthName);
    return;
  }
  const totalRow = findRowByLabel(sheet, "ИТОГО РАСХОДЫ");
  if (totalRow === -1) {
    Logger.log("Не нашёл строку 'ИТОГО РАСХОДЫ' на листе " + monthName);
    return;
  }
  sheet.insertRowBefore(totalRow);
  sheet.getRange(totalRow, 1, 1, 4).setValues([[dateStr, category, description, Number(amount) || 0]]);
}
