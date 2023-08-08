from django.shortcuts import render
from django.http import HttpResponse
import smartsheet
import mysql.connector as mc

global token,host,user,pwd,dbname
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
    global host,user,pwd,dbname
    host=request.GET["hostname"]
    user=request.GET["username"]
    pwd=request.GET["password"]
    dbname=request.GET["databasename"]
    try:
        connection=mc.connect(host=host,user=user,password=pwd,db=dbname)
        if connection.is_connected():
            return HttpResponse("<h1>SUCCESSFULLY CONNECTED TO DATABASE</h1>")
    except mc.errors.DatabaseError:
        return HttpResponse("<h1>Can't Connect To a Database, Please Check Your host/userName/pwd/databaseName and Ensure started the mysql server </h1>")


