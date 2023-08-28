from django.shortcuts import render
from django.http import HttpResponse
import smartsheet as ss
import mysql.connector as mc
import warnings
import pandas as pd

warnings.filterwarnings("ignore",category=UserWarning)

global token,host,user,pwd,dbname,connection,client,tab,sh,isInsert,isUpdate,isDelete
isInsert=False
isDelete=False
isUpdate=False
# Create your views here.
def home(request):
    return render(request,'home.html')

def display_token(request):
    global token
    token = request.POST["token"]
    if token:
        inf = {'tok': token}
        return render(request, 'result.html', context=inf)
    else:
        return HttpResponse("Token not provided")

def display_sheet_user(request):
    global client
    client=ss.Smartsheet(token)
    user_profile=client.Users.get_current_user()
    if 'result' in user_profile.to_dict():
        return render(request,"access_token_error.html")
    else:
        accountId=user_profile.account.id
        accountName=user_profile.account.name
        acc={'id':accountId,'name':accountName}
        return render(request,"sheet_user.html",context=acc)
      
def server_details(request):
    return render(request,"server_details.html")

def server_connection(request):
    global host,user,pwd,dbname,connection
    host=request.POST["hostname"]
    user=request.POST["username"]
    pwd=request.POST["password"]
    dbname=request.POST["databasename"]
    connection=mc.connect(host=host,user=user,password=pwd,db=dbname)
    if connection.is_connected():
        return render(request,"success_server_connection_status.html")
    else:
        return render(request,"failed_server_connection_status.html")
    
def tables(request):
    sheet=client.Sheets.list_sheets(include_all=True)
    sheets={'sheet':[]}
    for j in sheet.data:
        sheets['sheet'].append(j.name)
    cursor=connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = {'table': []}
    for x in cursor:
        tables['table'].append(x[0])
    context={
        'sheets':sheets,
        'tables':tables,
    }
    return render(request,"database_details.html",context=context)

def selected(request):
    global tab,sh
    tab=request.POST["tab"]
    sh=request.POST["sh"]
    selected={'table':tab,'sheet':sh}
    return render(request,"selected.html",context=selected)

def insert(a,df,sheet_id,sheet):
    global isInsert
    columns=sheet.columns
    initial_column=df.columns[0]
    row_values = df[df[initial_column] == int(a)].values.tolist()
    cells = []
    col_ids = [col.id for col in columns]
    for i in range(len(col_ids)):
        cell_value = row_values[0][i]
        cell = ss.models.Cell()
        cell.column_id=col_ids[i]
        cell.value=str(cell_value)
        cells.append(cell)
    new_row = ss.models.Row()
    new_row.cells = cells
    client.Sheets.add_rows(sheet_id, [new_row])
    isInsert=True

def delete(b,df,sheet_id,sheet):
    global isDelete
    for row in sheet.rows:
        if (str(row.cells[0].value)) == b:
            client.Sheets.delete_rows(sheet_id,row.id)
            isDelete=True

def update(c,df,sheet_id,sheet):
    global isUpdate
    columns=sheet.columns
    initial_column=df.columns[0]
    rows=sheet.rows
    row_values = []
    row_id = ''
    col_ids = []
    df_row_values = df[df[initial_column] == int(c)].values.tolist()
    df_row_values2 = [str(i) for i in df_row_values[0]]
    for row in rows:
        if row.cells[0].value == c:
            res = client.Sheets.get_row(sheet_id, row.id)
            row_id = row.id
            for cell in res.cells:
                row_values.append(cell.value)
                col_ids.append(cell.column_id)
    if df_row_values2 != row_values:
        for i,j in zip(range(len(df_row_values2)), range(len(col_ids))):
            new_cell = ss.models.Cell()
            new_row = ss.models.Row()
            new_row.id = row_id
            new_cell.column_id = col_ids[j]
            new_cell.value = df_row_values2[i]
            new_row.cells.append(new_cell)
            client.Sheets.update_rows(sheet_id, [new_row])
            isUpdate=True
    
def sync(request):
    global df,sheet_id,sheet,isInsert,isUpdate,isDelete
    query=f"select * from {tab}"
    df = pd.read_sql(query,connection)
    df = df.replace(r'^\s*$', 0, regex=True)
    initial_column = df.columns[0]
    df = df.sort_values(by=initial_column)
    sheets = client.Sheets.list_sheets(include_all=True)
    sheet_id=''
    for sh in sheets.data:
        if sh.name==tab:
            sheet_id=sh.id
    sheet=client.Sheets.get_sheet(sheet_id)
    dfRows = [str(row[0]) for _, row in df.iterrows()]
    sheetrows = [str(rows.cells[0].value) for rows in sheet.rows]
    for x in dfRows:
        if x not in sheetrows:
            insert(x,df,sheet_id,sheet)
        else:
            update(x,df,sheet_id,sheet)
    for y in sheetrows:
        if y not in dfRows:
            delete(y,df,sheet_id,sheet)
    if isInsert and isDelete and isUpdate:
        return HttpResponse("<h1>Rows inserted/deleted/updated to the sheet</h1>")
    elif isInsert:
        return HttpResponse("<h1>Rows inserted to the sheet</h1>")
    elif isDelete:
        return HttpResponse("<h1>Rows deleted from the sheet</h1>")
    elif isUpdate:
        return HttpResponse("<h1>Rows updated to the sheet</h1>")
    else:
        return HttpResponse("<h1>No Need To Update</h1>")
            
    


        

