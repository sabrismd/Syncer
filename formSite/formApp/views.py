from django.shortcuts import render
from django.http import HttpResponse
import smartsheet as ss
import mysql.connector as mc
import warnings
import pandas as pd
import pyautogui

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
        return HttpResponse("<h1>Token not provided</h1>")

def display_sheet_user(request):
    global client
    client=ss.Smartsheet(token)
    user_profile=client.Users.get_current_user()
    if 'result' in user_profile.to_dict():
        return render(request,"access_token_error.html")
    else:
        accountId=user_profile.account.id
        accountName1=user_profile.first_name
        accountName2=user_profile.last_name
        acc={'id':accountId,'fname':accountName1,'lname':accountName2}
        return render(request,"sheet_user.html",context=acc)
      
def server_details(request):
    return render(request,"server_details.html")

def server_connection(request):
    global host,user,pwd,dbname,connection
    host=request.POST["hostname"]
    user=request.POST["username"]
    pwd=request.POST["password"]
    dbname=request.POST["databasename"]
    try:
        connection=mc.connect(host=host,user=user,password=pwd,db=dbname)
        return render(request,"success_server_connection_status.html")
    except mc.errors.DatabaseError as e:
        return render(request,"failed_server_connection_status.html")
    
def tables(request):
    global sheet
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

def create_sheet(request):
    global selectedTable,workspace
    selectedTable=request.POST["nmb"]
    workspace=client.Workspaces.list_workspaces(include_all=True)
    workspaces={'ws':[]}
    for l in workspace.data:
        workspaces['ws'].append(l.name)
    context={'workspaces':workspaces,'table':selectedTable}
    return render(request, "wtc.html",context=context)
    
def sheetinworkspace(request):
    global selectedTable,workspace
    space=request.POST["workspace"]
    w_id=''
    for w in workspace.data:
        if w.name==space:
            w_id=w.id
    cursor = connection.cursor()
    query = f"SHOW COLUMNS FROM {selectedTable}"
    cursor.execute(query)
    column_title = [column[0] for column in cursor.fetchall()]
    # # to create a sheet
    sheet_specifications = ss.models.Sheet()
    sheet_specifications.name=selectedTable
    prim = True
    for i in column_title:
         col = ss.models.Column()
         col.title=i
         col.type = 'TEXT_NUMBER'
         col.primary=prim
         prim = False
         sheet_specifications.columns.append(col)
    wspace=client.Workspaces.create_sheet_in_workspace(w_id,sheet_specifications)
    cont={'sheet':selectedTable,'workspace':space}
    return render(request,"wp.html",context=cont)

def sheetinsheets(request):
    global selectedTable
    cursor = connection.cursor()
    query = f"SHOW COLUMNS FROM {selectedTable}"
    cursor.execute(query)
    column_title = [column[0] for column in cursor.fetchall()]
    # # to create a sheet
    sheet_specifications = ss.models.Sheet()
    sheet_specifications.name=selectedTable
    prim = True
    for i in column_title:
        col = ss.models.Column()
        col.title=i
        col.type = 'TEXT_NUMBER'
        col.primary=prim
        prim = False
        sheet_specifications.columns.append(col)
    res=client.Home.create_sheet(sheet_specifications)
    cont={'sheet':selectedTable}
    return render(request,"createsheet.html",context=cont)


def selected(request):
    global tab,sh
    tab=request.POST["tab"]
    sh=request.POST["sh"]
    selected={'table':tab,'sheet':sh}
    return render(request,"selected.html",context=selected)

def insert(a,df,sheet_id,sheet):
    global isInsert
    initial_column=df.columns[0]
    sibling_id='' 
    row_values = df[df[initial_column] == int(a)].values.tolist()
    sheetLists=[row.cells[0].value for row in sheet.rows]
    if sheetLists:
        closest_match = min(sheetLists, key=lambda x: abs(int(x) - int(a)))
        closest_match=str(closest_match)
        columns=sheet.columns
        for row in sheet.rows:
            if row.cells[0].value==closest_match:
                sibling_id=row.id
    
        cells = []
        col_ids = [col.id for col in columns]
        for i in range(len(col_ids)):
            cell_value = row_values[0][i]
            cell = ss.models.Cell()
            cell.column_id=col_ids[i]
            cell.value=str(cell_value)
            cells.append(cell)
        new_row = ss.models.Row()
        new_row.sibling_id=sibling_id
        new_row.cells = cells
        if int(a)>int(closest_match):
            new_row.above=False
        else:
            new_row.above=True 
        client.Sheets.add_rows(sheet_id, [new_row])
        isInsert=True
    else:
        cells = []
        col_ids = [col.id for col in sheet.columns]
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
    # tab_rows={'irows':[]}
    # for i in range(len(dfRows)):
    #     tab_rows["irows"].append(dfRows[i])
    # sh_rows={'irows':[]}
    # for j in range(len(sheetrows)):
    #     sh_rows["irows"].append(sheetrows[j])
    # context={
    #     'tab_rows':tab_rows,
    #     'sh_rows':sh_rows,
    # }
    for x in dfRows:
        if x not in sheetrows:
            insert(x,df,sheet_id,sheet)
        else:
            update(x,df,sheet_id,sheet)
    for y in sheetrows:
        if y not in dfRows:
            delete(y,df,sheet_id,sheet)

    if isInsert and isDelete and isUpdate:
        isInsert=False
        isUpdate=False
        isDelete=False
        return render(request,"riud.html")
    elif isInsert:
        isInsert=False
        return render(request,"insert.html")
    elif isDelete:
        isDelete=False
        return render(request,"delete.html")
    elif isUpdate:
        isUpdate=False
        return render(request,"update.html")
    else:
        return render(request,"nnu.html")

def matching(request):
    global sh,tab
    global connection
    sheets=client.Sheets.list_sheets(include_all=True)
    cursor=connection.cursor()
    query=f"SHOW COLUMNS FROM {tab}"
    cursor.execute(query)
    sheet_id=''
    context={'t':tab,'s':sh}
    for v in sheets.data:
        if v.name==sh:
            sheet_id=v.id
    sheet_obj=client.Sheets.get_sheet(sheet_id)
    table_columns=[columns[0] for columns in cursor.fetchall()]
    sheet_columns=[col.title for col in sheet_obj.columns]
    if table_columns==sheet_columns:
        return render(request,"success_match.html")
    else:
        return render(request,"mismatch.html",context=context)

def closetab(request):
    pyautogui.hotkey('ctrl','w')
    

             
    


        

