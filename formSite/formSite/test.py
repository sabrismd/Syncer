import smartsheet as ss 
client=ss.Smartsheet("247qiwFXuBSRQRR7HafYDjdoQxQWrIE7l6t4V")
# sheets=client.Sheets.list_sheets()
# for sheet in sheets.data:
#     if sheet.name=='users':
#         print(sheet.id)
# sheet=client.Sheets.get_sheet('8254310265606020')
#  for row in sheet.rows:
#     print(type(row.cells[0].value))
# sheets=client.Sheets.list_sheets()
sheet=client.Sheets.share_sheet(
  8254310265606020,       # sheet_id
  ss.models.Share({
    'access_level': 'EDITOR',
    'email': 'sabrisyed3333@gmail.com'
  })                  # sendEmail
)