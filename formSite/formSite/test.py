import smartsheet as ss 
client=ss.Smartsheet("247qiwFXuBSRQRR7HafYDjdoQxQWrIE7l6t4V")
sheet=client.Sheets.list_sheets(include_all=True)
for sh in sheet.data:
    if sh.name=='tentries':
        print(sh.id)