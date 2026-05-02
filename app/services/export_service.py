import io
import zipfile
from sqlalchemy.orm import Session
from sqlalchemy import select, inspect as sa_inspect


# obtiene los nombres de columnas del modelo usando SQLAlchemy
def _columns(model) -> list[str]:
    return [c.key for c in sa_inspect(model).mapper.column_attrs]


# convierte los objetos del modelo a lista de filas con valores como string
def _rows(items, columns: list[str]) -> list[list[str]]:
    return [
        [str(getattr(item, col)) if getattr(item, col) is not None else "" for col in columns]
        for item in items
    ]


# convierte índice numérico de columna a letra Excel (1→A, 27→AA, etc.)
def _col_letter(n: int) -> str:
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result


# genera CSV manualmente sin librerías, envuelve en comillas si el valor contiene comas o comillas
def generate_csv(db: Session, model) -> str:
    items = list(db.execute(select(model)).scalars().all())
    columns = _columns(model)
    rows = _rows(items, columns)

    def escape(val: str) -> str:
        if "," in val or '"' in val or "\n" in val:
            return '"' + val.replace('"', '""') + '"'
        return val

    lines = [",".join(columns)]
    for row in rows:
        lines.append(",".join(escape(v) for v in row))

    return "\n".join(lines)


# genera XLSX en formato SpreadsheetML (ZIP con XMLs) manualmente sin librerías
def generate_xlsx(db: Session, model) -> bytes:
    items = list(db.execute(select(model)).scalars().all())
    columns = _columns(model)
    rows = _rows(items, columns)

    all_rows = [columns] + rows

    # construye el XML de la hoja con todas las filas y celdas
    sheet_rows = []
    for r_idx, row in enumerate(all_rows, start=1):
        cells = []
        for c_idx, val in enumerate(row, start=1):
            col = _col_letter(c_idx)
            safe = val.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
            cells.append(f'<c r="{col}{r_idx}" t="inlineStr"><is><t>{safe}</t></is></c>')
        sheet_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')

    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData>'
        "</worksheet>"
    )

    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )

    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )

    # empaqueta todos los XMLs en un ZIP en memoria (formato real de un .xlsx)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml)

    return buf.getvalue()
