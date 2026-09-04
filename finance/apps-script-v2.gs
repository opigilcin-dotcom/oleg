/**
 * Чекбокс-форма для "финансы-2026.xlsx" (после импорта в Google Таблицы).
 *
 * Установка: Extensions -> Apps Script в таблице -> вставить этот код целиком
 * (заменить всё, что там было) -> сохранить (значок дискеты).
 * Триггер НЕ нужно настраивать отдельно — функция называется onEdit,
 * это "простой" триггер, Google запускает её сама при любом изменении ячейки.
 *
 * Перед использованием на листе "Форма" нужно один раз вручную вставить
 * настоящие чекбоксы Google Таблиц (Excel-формат их не поддерживает):
 *   выделить ячейку -> Вставка -> Флажок (Insert -> Checkbox)
 *   Ячейки: B7 (Занести приход), B15 (Занести расход), E19 (Добавить контрагента)
 */

function onEdit(e) {
  const sheet = e.range.getSheet();
  if (sheet.getName() !== "Форма") return;

  const row = e.range.getRow();
  const col = e.range.getColumn();
  const value = e.range.getValue();

  if (row === 7 && col === 2 && value === true) {
    handleIncome(e.source, sheet);
  } else if (row === 15 && col === 2 && value === true) {
    handleExpense(e.source, sheet);
  } else if (row === 19 && col === 5 && value === true) {
    handleNewContractor(e.source, sheet);
  }
}

function handleIncome(ss, formSheet) {
  const category = formSheet.getRange("B2").getValue();
  const amount = formSheet.getRange("B3").getValue();
  const method = formSheet.getRange("B4").getValue();
  const contractor = formSheet.getRange("B5").getValue();
  const comment = formSheet.getRange("B6").getValue();
  const date = formSheet.getRange("B18").getValue();

  if (!category || !amount) {
    formSheet.getRange("B7").setValue(false);
    SpreadsheetApp.getUi().alert("Заполни статью и сумму дохода перед тем, как отмечать галочку.");
    return;
  }

  appendLedgerRow(ss, date, "Доход", category, contractor, method, amount, comment);
  formSheet.getRange("B2:B6").clearContent();
  formSheet.getRange("B7").setValue(false);
  refreshLast5(ss, formSheet);
}

function handleExpense(ss, formSheet) {
  const category = formSheet.getRange("B10").getValue();
  const amount = formSheet.getRange("B11").getValue();
  const method = formSheet.getRange("B12").getValue();
  const contractor = formSheet.getRange("B13").getValue();
  const comment = formSheet.getRange("B14").getValue();
  const date = formSheet.getRange("B18").getValue();

  if (!category || !amount) {
    formSheet.getRange("B15").setValue(false);
    SpreadsheetApp.getUi().alert("Заполни статью и сумму расхода перед тем, как отмечать галочку.");
    return;
  }

  appendLedgerRow(ss, date, "Расход", category, contractor, method, amount, comment);
  formSheet.getRange("B10:B14").clearContent();
  formSheet.getRange("B15").setValue(false);
  refreshLast5(ss, formSheet);
}

function handleNewContractor(ss, formSheet) {
  const name = formSheet.getRange("E18").getValue();
  if (!name) {
    formSheet.getRange("E19").setValue(false);
    return;
  }
  const contractorsSheet = ss.getSheetByName("Контрагенты");
  const nextRow = contractorsSheet.getLastRow() + 1;
  contractorsSheet.getRange(nextRow, 1).setValue(name);
  formSheet.getRange("E18").clearContent();
  formSheet.getRange("E19").setValue(false);
}

function appendLedgerRow(ss, date, type, category, contractor, method, amount, comment) {
  const ledger = ss.getSheetByName("Операции");
  const row = ledger.getLastRow() + 1;
  ledger.getRange(row, 1, 1, 7).setValues([[date, type, category, contractor, method, amount, comment]]);
}

function refreshLast5(ss, formSheet) {
  const ledger = ss.getSheetByName("Операции");
  const lastRow = ledger.getLastRow();
  const firstRow = Math.max(2, lastRow - 4);
  const count = lastRow - firstRow + 1;
  const data = ledger.getRange(firstRow, 1, count, 7).getValues();
  data.reverse(); // most recent first

  formSheet.getRange(27, 1, 5, 7).clearContent();
  if (data.length > 0) {
    formSheet.getRange(27, 1, data.length, 7).setValues(data);
  }
}
