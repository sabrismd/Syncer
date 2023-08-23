from django.shortcuts import render
from django.http import HttpResponse
import smartsheet
import mysql.connector as mc

global token,host,user,pwd,dbname,connection,client
# Create your views here.
def home(request):
    return render(request,'home.html')

def display_token(request):
    global token
    token = request.GET["token"]
    if token:
        inf = {'tok': token}
        return render(request, 'result.html', context=inf)
    else:
        return HttpResponse("Token not provided")

def display_sheet_user(request):
    global client
    client=smartsheet.Smartsheet(token)
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
    host=request.GET["hostname"]
    user=request.GET["username"]
    pwd=request.GET["password"]
    dbname=request.GET["databasename"]
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
    tab=request.GET["tab"]
    sh=request.GET["sh"]
    selected={'table':tab,'sheet':sh}
    return render(request,"selected.html",context=selected)



        

