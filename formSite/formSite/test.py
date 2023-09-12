import smartsheet as ss 
import mysql.connector as mc
client=ss.Smartsheet("247qiwFXuBSRQRR7HafYDjdoQxQWrIE7l6t4V")
sheets=client.Sheets.list_sheets(include_all=True)
for sheet in sheets.data:
    print(sheet.name,sheet.id)
# client.Sheets.delete_sheet('4854496630886276')

