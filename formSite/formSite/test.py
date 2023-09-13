import smartsheet as ss 
import mysql.connector as mc
import difflib
import difflib
sheet_pos = ['1', '2', '4', '5']
input_str = '3'

closest_match = min(sheet_pos, key=lambda x: abs(int(x) - int(input_str)))

print(f"The closest match to '{input_str}' is '{closest_match}'")


# client=ss.Smartsheet("247qiwFXuBSRQRR7HafYDjdoQxQWrIE7l6t4V")
# sheet=client.Sheets.get_sheet('4849161627193220')
# for row in sheet.rows:
#     print(type(row.cells[0].value))
    



# 01_Marketing Request Tracker - Sheet Basics 4825788370446212
# 02_Marketing Request Tracker - Sheet Formatting 322188743075716
# 03_Marketing Request Tracker - Formulas 2573988556760964
# 04_Marketing Request Tracker - Filters and Views 7077588184131460
# 05_Marketing Request Tracker - Cell Linking 1448088649918340
# ANSWER_Marketing Request Tracker - Cell Linking 3136938510182276
# ANSWER_Marketing Request Tracker - Formulas 3699888463603588
# ANSWER_Marketing Request Tracker - Sheet Basics 8203488090974084
# ANSWER_Marketing Request Tracker-Filters and Views 5388738323867524
# ANSWER_Marketing Request Tracker-Sheet Formatting 885138696497028
# beneficiary 3302535968280452
# billing_type 6776649114668932
# ChatGPT - POC 8383340964958084
# Copy of MYSQL:Time-entries 6564826679562116
# Copy of time_entries 6987623260180356
# Creative Metrics for Dashboard 2952010065569668
# Creative Request Intake Sheet 5203809879254916
# holidays 7085619599593348
# invoice_terms_and_conditions 8677383871614852
# invoice_terms_and_conditions 6379088889466756
# Marketing Request Tracking Requirements 5190959374854020
# migrations 7296631342845828
# Monthly Tracking Sheet 700210251884420
# MYSQL 4100026562570116
# MYSQL_Time-entries 2295831060604804
# Project Details 4275262213908356
# Project Plan for request 3 7640538137552772
# Project Plan for request 3 5951688277288836
# project_assignment 1743458964295556
# Project_Assignments 8520336194621316
# Request Cost Tracking Sheet 8018559646361476
# Sheet - Sales Pipeline 6888367745984388
# START HERE: Core App Skills Badge Exercise 3514960018990980
# tax 4551155103256452
# tentries 4849161627193220
# Time_Entries 1487619305197444
# time_entries 2729289283751812
# users 4475194110332804
# Whatsapp Integration Sheet 3535287193233284

