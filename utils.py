import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import string
import datetime
import calendar
import time
from time import strftime, gmtime
import operator
from operator import itemgetter
from bson.objectid import ObjectId
from pymongo import MongoClient
from constants import *
from datetime import datetime as dt
import datetime
from datetime import date, timedelta
import xlwt
import xlsxwriter
import copy
import sys
import re
import logging
from num2words import *
import uuid
import math
import smtplib
import ssl


def email_to_client(message, receiver_list):
    print "Sending Email"

    port = EMAIL_PORT
    smtp_server = "smtp.gmail.com"
    sender_email = SENDER_EMAIL
    password = SENDER_PASSWORD
    #receiver_email = "sanidhyasingh@karthavya.com"
    #context = ssl.create_default_context()

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    if receiver_list:
        for each_receiver in receiver_list:
            server.sendmail(sender_email, each_receiver, message)
    else:
        print "No receiver found!"
        server.quit()


def get_auto_invoice_logger():
    try:
        auto_inv_logger = None
        inv_log_file_path = os.path.join(LOG_FILE_PATH , 'invoice_auto_gen.log')
        log_format = logging.Formatter('%(levelname)s: %(asctime)s %(message)s',\
            datefmt='%m/%d/%Y %I:%M:%S %p')
        fileHandler = logging.FileHandler(inv_log_file_path, mode='a')
        fileHandler.setFormatter(log_format)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(log_format)
        auto_inv_logger = logging.getLogger('invoice_auto_gen')
        auto_inv_logger.setLevel(logging.DEBUG)
        auto_inv_logger.addHandler(fileHandler)
        auto_inv_logger.addHandler(streamHandler)
        return auto_inv_logger
    except Exception as ex:
        print "Exception arised while getting logger for generating auto invoice initially....",ex

def is_valid_commercial(advt_type_details):
    valid_commercial = False
    if advt_type_details and advt_type_details.get('time_consumable',False):
       if advt_type_details.get('is_slot',False):
          valid_commercial = False
       else:
          valid_commercial = True
    return valid_commercial

def convert_string_to_float(val, defau_ret_val = 0.0):
    try:
        if isinstance(val, (str,int,float,unicode)) : return float(val)
    except Exception, ex:
        #print "Exception in convert_string_to_float::::::Hence returning 0.0",ex,val
        pass
    return defau_ret_val

def convert_to_two_decimal_float(val, defau_ret_val = 0.00):
    try:
        return float("{0:.2f}".format(val))
    except Exception as ex:
        pass
    return defau_ret_val

def convert_to_int(val_in, defau_ret_val = 0):
    try:
        if isinstance(val_in, (int, float)):
            return int(val_in)
        if isinstance(val_in, unicode): #and str(val_in).isdigit():
            val_in = str(val_in)
            #return int(val_in)
        if isinstance(val_in, str):
            if val_in.isdigit():
                return int(val_in)
            else:
                try:
                    val_in = float(val_in)
                    return int(val_in)
                except Exception as ex1:
                    #print "Exception while converting to float"
                    pass
        return defau_ret_val
    except Exception as ex:
        print "Exception arised while converting to int::::::::",ex
    return defau_ret_val

def get_current_date(date_format = "%Y/%m/%d"):
    try:
        return datetime.datetime.strftime(datetime.datetime.now(), date_format)
    except Exception, ex:
        return ""
        print "Exception in get_current_date:::: %s"%ex

#CURRENT_DATE = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d")
def get_current_time():
    try:
        return datetime.datetime.now().strftime("%H:%M:%S")
    except Exception, ex:
        print "Exception in get_current_time :::: %s"%ex 

def get_month_from_date(date):
    try:
        date_obj = datetime.datetime.strptime(date, "%Y/%m/%d")
        month = date_obj.month
        month = str(calendar.month_abbr[month])
        return month
    except Exception, ex:
        print "Exception in get_month_from_date: %s" %str(ex)

def get_number_of_days_in_month(date):
    try:
        date_obj = datetime.datetime.strptime(date, "%Y/%m/%d")
        year, month = date_obj.year, date_obj.month
        days_in_month = calendar.monthrange(year, month)[1] 
        return days_in_month
    except Exception, ex:
        print "Exception in get_number_of_days_in_month :::: %s" %str(ex)
 
def get_number_of_episodes_in_month(date, days):
    try:
        episodes = 0
        date_obj = datetime.datetime.strptime(date, "%Y/%m/%d")
        year, month = date_obj.year, date_obj.month
        day_int = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
        day_count = {}
        for day in day_int:
            day_count[day] = len([1 for week_day in calendar.monthcalendar(year, month) if week_day[day_int[day]] != 0]) 
        for day in days:
            if day_count[day]:
                episodes = episodes + day_count[day]
        return episodes
         
         
    except Exception, ex:
        print "Exception in get_number_of_episodes_in_month: %s" %str(ex)

def get_months_between_dates(start_date, end_date):
    try:
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        month_range = []
        start_obj = datetime.datetime.strptime(start_date, "%Y/%m/%d")
        start_month = start_obj.month - 1
        end_obj = datetime.datetime.strptime(end_date, "%Y/%m/%d")
        end_month = end_obj.month 
        for month in range(start_month, end_month):
            month_range.append(months[month]) 
        return month_range
    except Exception, ex:
        print "Exception in get_months_between_dates: %s" %str(ex)
#CURRENT_TIME = datetime.datetime.now().strftime("%H:%M:%S")
def get_diff_btwn_dates(from_dt, to_dt, abs_diff = True, date_fmt = "%Y/%m/%d"):
    try:
        diff = 0
        if from_dt and to_dt:
            f_dt = datetime.datetime.strptime(from_dt, date_fmt)
            t_dt = datetime.datetime.strptime(to_dt, date_fmt)
            diff = (t_dt-f_dt).days
        if not abs_diff:
            return diff
        return abs(diff)
    except Exception, ex:
        print "Exception in get_diff_btwn_dates", ex

def get_week_day(date):
    try:
        date_obj = datetime.datetime.strptime(date, "%Y/%m/%d")
        return str(date_obj.strftime("%A"))
    except Exception, ex:
        print "Exception in get_week_day() ", ex


def get_end_time(start_time, duration):
    try:
        time_list = []
        time_list.append(start_time)
        time_list.append(duration)
        end_time = datetime.timedelta()
        for i in time_list:
            (h, m, s) = i.split(':')
            d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            end_time += d
        if str(end_time) == '1 day, 0:00:00':
            end_time = "23:59:59"
        elif ',' in str(end_time) and str(end_time).split(',')[1].strip() > '0:00:00':
            print("Time exceeds for the day")
            return str(end_time)
        end_time = str(datetime.datetime.strptime(str(end_time), "%H:%M:%S")).split()[1]
        return str(end_time)
    except Exception, en:
        print "Exxception in get_end_time:  ", en

def get_uid_sequence(Label = "", date_format = "%Y%m", \
        fiscal_year_format = [], fiscal_position = "", delimiter = "", ref_date_datetime_obj = None, post_Label = ""):
    #Usage:: date_format->usually %m or %d format, fiscal_year_format-> %Y or %y
    #If fiscal position is in last then it will try append the fiscal year at last of the sequence
    try:
        date_year_month = ""
        fiscal_year = ""
        Label = Label.strip()
        post_Label = post_Label.strip()
        final_format = ""
        if type(ref_date_datetime_obj) != datetime.datetime:
            ref_date_datetime_obj = None
        if date_format != "":
            if ref_date_datetime_obj:
                date_year_month = ref_date_datetime_obj.strftime(date_format)
                #print "date year month as per reference:::::::",date_year_month
            else:
                date_year_month = datetime.datetime.now().strftime(date_format)
        #if fiscal_year_format != "":
        if len(fiscal_year_format) > 2:
            current_year = ""
            next_year = ""
            current_month = None
            if ref_date_datetime_obj:
                current_year = ref_date_datetime_obj.strftime(fiscal_year_format[0])
                next_year =  str(int(ref_date_datetime_obj.strftime(fiscal_year_format[1])) + 1)
                current_month = ref_date_datetime_obj.month
            else:
                curr_dt_obj = datetime.datetime.now()
                current_year = curr_dt_obj.strftime(fiscal_year_format[0])
                next_year =  str(int(curr_dt_obj.strftime(fiscal_year_format[1])) + 1)
                current_month = curr_dt_obj.month
            if current_year:
                if current_month and current_month <= FISCAL_END_MONTH_NUM:
                    current_dt_obj = datetime.datetime.strptime(current_year, fiscal_year_format[0])
                    current_year = str(int(current_dt_obj.strftime(fiscal_year_format[0])) - 1)
                    current_dt_obj = datetime.datetime.strptime(current_year, fiscal_year_format[0])
                    next_year = str(int(current_dt_obj.strftime(fiscal_year_format[1])) + 1)
            fiscal_delimiter = fiscal_year_format[2]
            #fiscal_year = current_year + str(int(current_year) + 1)
            fiscal_year = current_year + fiscal_delimiter + next_year
            if fiscal_position == "last":
                final_format = date_year_month + delimiter + fiscal_year
                if Label:
                    final_format = Label + delimiter + final_format
                '''if post_Label:
                    final_format = final_format + delimiter + post_Label'''
                #return Label + delimiter + date_year_month + delimiter + fiscal_year
                return final_format
        final_format = fiscal_year + delimiter + date_year_month
        if Label:
            final_format = Label +  delimiter + final_format
        '''if post_Label:
            final_format = final_format + delimiter + post_Label'''
        #return Label +  delimiter + fiscal_year + delimiter + date_year_month
        return final_format
    except Exception, ex:
        print "Exception in get_uid_sequence function::::",ex

def get_mongo_client():
    return MongoClient(MONGO_DB_IP, MONGO_DB_PORT, fsync=True)

def get_db_name(conx):
    return conx[QET_DB_NAME]

def auth(db):
    if MONGO_AUTHENTICATION:
        db.authenticate(MONGO_USERNAME, MONGO_PASSWORD)
    return db

def get_qet_db_instance(conx, dbname=QET_DB_NAME):
    return conx[dbname]

conx = get_mongo_client()
db = get_db_name(conx)
db = auth(db)

def random_string(length=10):
    return "".join([random.choice(string.ascii_letters +
                                  string.digits) for i in range(length)])


def json_friendly(obj):
    if not obj or type(obj) in (int, float, str, unicode, bool, long):
        return obj
    if type(obj) == datetime.datetime:
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    if type(obj) == dict:
        for k in obj:
            obj[k] = json_friendly(obj[k])
        return obj
    if type(obj) == list:
        for i, v in enumerate(obj):
            obj[i] = json_friendly(v)
        return obj
    if type(obj) == tuple:
        temp = []
        for v in obj:
            temp.append(json_friendly(v))
        return tuple(temp)
    return str(obj)



def is_valid_date_time_format(date_time, display_format="%d/%m/%Y %H:%M:%S"):
    if display_format == "%d/%m/%Y %H:%M:%S":
        try:
            return datetime.datetime.strptime(date_time, "%d/%m/%Y %H:%M:%S")
        except ValueError, ve:
            return False
    elif display_format == "%H:%M:%S":
        try:
            return datetime.datetime.strptime(date_time, "%H:%M:%S")
        except ValueError, ve:
            #print " escaping the check due to difference in time more than a day!!!!!!!!!!!!!!"
            return False
    else:
        return False        

def isValidDatetimeObject(datetime1, datetime_format = "%Y/%m/%d"):
    try:
        return datetime.datetime.strptime(datetime1, datetime_format)
    except Exception, ex:
        print "Exception while checking for valid datetime object:::::",ex

def get_time_with_two_digit(time, display_format="%H:%M:%S"):
    time_obj = is_valid_date_time_format(time, display_format)
    if not time_obj:
        return None
    h = time_obj.hour
    m = time_obj.minute
    s = time_obj.second
    return "%02d:%02d:%02d" % (h, m, s)


def convert_seconds_to_hms_format(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def convert_milliseconds_to_hms_format(milliseconds):
    s, ms = divmod(milliseconds, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def change_date_format_from_date_time(date, format_from,
                                      format_to, year_first):
    date_obj = datetime.datetime.strptime(
        date, "%d"+format_from+"%m"+format_from+"%Y"+" %H:%M:%S")
    if year_first:
        return date_obj.strftime("%Y"+format_to+"%m"+format_to+"%d")
    else:
        return date_obj.strftime("%d"+format_to+"%m"+format_to+"%Y")


def change_date_format_from_date(date, format_from, format_to, year_first):
    date_obj = datetime.datetime.strptime(
        date, "%d"+format_from+"%m"+format_from+"%Y")
    if year_first:
        return date_obj.strftime("%Y"+format_to+"%02m"+format_to+"%02d")
    else:
        return date_obj.strftime("%02d"+format_to+"%02m"+format_to+"%Y")

def change_datetime_format(ref_datetime, ref_dt_format, target_dt_format):
    if not isValidDatetimeObject(ref_datetime, ref_dt_format) : return ref_datetime
    return datetime.datetime.strptime(ref_datetime, ref_dt_format).strftime(target_dt_format)

def find_time_from_date_time(date_time):
    time_obj = datetime.datetime.strptime(date_time,
                                          "%d/%m/%Y %H:%M:%S").time()
    return str(time_obj)


def get_time_in_the_underscore_format(time):
    time_obj = datetime.datetime.strptime(time, "%H:%M:%S")
    h = time_obj.hour
    m = time_obj.minute
    s = time_obj.second
    return "%02d_%02d_%02d" % (h, m, s)


def find_date_from_date_time(date_time):
    date_obj = datetime.datetime.strptime(date_time,
                                          "%d/%m/%Y %H:%M:%S").date()
    date = str(date_obj.strftime("%d/%m/%Y"))
    return str(date)


def compare_datetime(datetime1, oper, datetime2, value, display_format="%d/%m/%Y"):
    if value == 'date':
        if display_format == "%d/%m/%Y":
            datetime_obj1 = datetime.datetime.strptime(datetime1, "%d/%m/%Y")
            datetime_obj2 = datetime.datetime.strptime(datetime2, "%d/%m/%Y")
        elif display_format == "%Y/%m/%d":
            datetime_obj1 = datetime.datetime.strptime(datetime1, "%Y/%m/%d")
            datetime_obj2 = datetime.datetime.strptime(datetime2, "%Y/%m/%d")
    elif value == 'time':
        datetime_obj1 = datetime.datetime.strptime(datetime1, "%H:%M:%S")
        datetime_obj2 = datetime.datetime.strptime(datetime2, "%H:%M:%S")
    if oper == OPER_GT:
        if datetime_obj1 > datetime_obj2:
            return True
        else:
            return False
    elif oper == OPER_GTE:
        if datetime_obj1 >= datetime_obj2:
            return True
        else:
            return False
    elif oper == OPER_LT:
        if datetime_obj1 < datetime_obj2:
            return True
        else:
            return False
    elif oper == OPER_LTE:
        if datetime_obj1 <= datetime_obj2:
            return True
        else:
            return False
    elif oper == OPER_EQ:
        if datetime_obj1 == datetime_obj2:
            return True
        else:
            return False
    else:
        return False


def add_time(time1, time2):
    time_obj1 = datetime.datetime.strptime(time1, "%H:%M:%S")
    time_obj2 = datetime.datetime.strptime(time2, "%H:%M:%S")
    t1 = datetime.timedelta(hours=time_obj1.hour, minutes=time_obj1.minute,
                            seconds=time_obj1.second)
    t2 = datetime.timedelta(hours=time_obj2.hour, minutes=time_obj2.minute,
                            seconds=time_obj2.second)
    result = t1 + t2
    return get_time_with_two_digit(str(result))


def subtract_time(time1, time2):
    time_obj1 = datetime.datetime.strptime(time1, "%H:%M:%S")
    time_obj2 = datetime.datetime.strptime(time2, "%H:%M:%S")
    t1 = datetime.timedelta(hours=time_obj1.hour, minutes=time_obj1.minute,
                            seconds=time_obj1.second)
    t2 = datetime.timedelta(hours=-time_obj2.hour, minutes=-time_obj2.minute,
                            seconds=-time_obj2.second)
    result = t1 + t2
    return get_time_with_two_digit(str(result))


def find_relative_time_based_on_duration(time1, duration):
    time_obj = datetime.datetime.strptime(time1, "%H:%M:%S")
    t1 = datetime.timedelta(hours=time_obj.hour, minutes=time_obj.minute,
                            seconds=time_obj.second)
    t2 = datetime.timedelta(seconds=int(duration))
    result = t1 + t2
    return get_time_with_two_digit(str(result))


def duration_between_time(break_end_time, break_start_time):
    time1 = subtract_time(break_end_time, break_start_time)
    if not time1:
        return 0
    x = datetime.datetime.strptime(time1, '%H:%M:%S')
    return int(datetime.timedelta(hours=x.hour, minutes=x.minute,
                                  seconds=x.second).total_seconds())

def hms_to_sec(hms):
     seconds = 0
     count = 0
     for part in hms.split(':'):
         if count == 3:
             break
         seconds= seconds*60 + int(part)
         count = count + 1
     return seconds

def get_one_week_dates(start_date):
    date_list = []
    try:
        for i in range(0, 7):
            date = (datetime.datetime.strptime(start_date,"%d/%m/%Y") + datetime.timedelta(days = i)).strftime('%02d/%02m/%Y')
            #print date
            date_list.append(date)
        return date_list
    except Exception, ex:
        print "Exception in get_one_week_dates ::::::", ex

def get_days_list(from_date, to_date, date_format="%Y/%m/%d"):
    try:
        date_list = []
        date_diff = None
        if from_date and to_date:
            from_date_obj = datetime.datetime.strptime(from_date, date_format)
            to_date_obj = datetime.datetime.strptime(to_date, date_format)
            from_date_obj_copy = copy.deepcopy(from_date_obj)
            to_date_obj_copy = copy.deepcopy(to_date_obj)
            from_date_obj = min(from_date_obj_copy,to_date_obj_copy)
            to_date_obj = max(from_date_obj_copy,to_date_obj_copy)
            date_diff = (to_date_obj - from_date_obj).days
            for each_day in xrange(date_diff + 1):
                each_date = (from_date_obj + datetime.timedelta(each_day)).strftime(date_format)
                date_list.append(each_date)
        return (date_diff,date_list)
    except Exception,ex:
        print "Exception arised while getting days list in get_days_list",ex

'''def get_uid_sequence(Label=""):
    year_month_day=datetime.datetime.now().strftime("%Y%m%d")
    return Label+year_month_day'''


def get_weekday_name(date, date_format = "%Y/%m/%d", wkday_format = "%A"):
    try:
        return datetime.datetime.strptime(date, date_format).strftime(wkday_format)
    except Exception as ex:
        print "Exception arised while getting weekday's name for date::::{}".format(date)

############################################################################
####################### XLS DEFINITIONS ####################################

def write_heading(sheet1, heading_list, row_index=0):
    column_index = 0
    try:
        for heading in heading_list:
            #print "writing heading -------------------",heading
            sheet1.write(row_index, column_index, heading)
            column_index += 1
    except Exception, ex:
        print "Exception in write heading ::::::", ex

def write_data(sheet1, data, row_index, order_dict, style_format = None):
    try:
        for value in data:
            index = -1
            if value in order_dict:
               index = order_dict.index(value)
            
            if value in order_dict:
                #print "valueeeeee",value 
                '''if type(data[value]) != int and type(data[value]) != float and data[value] != None and type(data[value]) != list:
                    sheet1.write(row_index, order_dict[value], data[value].upper())
                else:
                    sheet1.write(row_index, order_dict[value], data[value])'''
                if index!=-1 and type(data[value]) != int and  type(data[value]) != float\
                  and data[value] != None and type(data[value]) != list:
                    if style_format:
                        sheet1.write(row_index, index, data.get(value,'').upper(), style_format)
                    else : sheet1.write(row_index, index, data.get(value,'').upper())
                else:
                    if style_format:
                        sheet1.write(row_index,index, data.get(value,''), style_format)
                    else : sheet1.write(row_index,index, data.get(value,''))
                    
    except Exception, ex:
        print "Exception in write data ::::::", ex

def write_to_xls(result, heading_list, order_dict, filename="test.xls", FPC=False, date_heading=[]):
    try:
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1",cell_overwrite_ok=True)
        starting_row_index = 2
        write_heading(sheet1, heading_list)
        if FPC:
            write_heading(sheet1, date_heading, 1)
            starting_row_index = 3
        print "heading written"
        severe_warning_format = xlwt.easyxf(\
            'borders: left thick, right thick, top thick, bottom thick;'\
            'pattern: pattern solid, fore_colour red;')
        mild_warning_format = xlwt.easyxf(\
            'borders: left thick, right thick, top thick, bottom thick;'\
            'pattern: pattern solid, fore_colour aqua;')
        normal_warning_format = xlwt.easyxf(\
            'borders: left thick, right thick, top thick, bottom thick;'\
            'pattern: pattern solid, fore_colour light_green;')
        for data in result:
            if "date" in data and data["date"]:
                data["date"] = datetime.datetime.strptime(data["date"],'%Y/%m/%d').strftime("%d-%m-%Y")
            if "style_format_key" in data:
                style_format = data.pop("style_format_key")
                if style_format == "severe":
                    write_data(sheet1, data, starting_row_index, order_dict, severe_warning_format)
                elif style_format == "mild":
                    write_data(sheet1, data, starting_row_index, order_dict, mild_warning_format)
                elif style_format == "normal":
                    write_data(sheet1, data, starting_row_index, order_dict, normal_warning_format)
            else : write_data(sheet1, data, starting_row_index, order_dict)
            starting_row_index += 1
        path = EXPORT_PATH + os.sep + filename.replace("/",".") 
        book.save(path)
        print "filename::::",filename
        #print "book saved returning file in path-------------", path
        return {"filename":filename.replace("/",".")}
    except Exception, ex:
        print "Exception in write_to_xls :::::::", ex   
       
###### Xls operation using xlsxwriter module ########

def check_valid_filepath(filename = None, base_path = None):
    try:
        if filename:
            print "File Name Got as::::",filename
            #filename = filename.strip()
            #print "File Name Got as11111::::",filename
            '''if filename.find(" "):
                total_spaces = filename.count(" ")
                print "Found Spacessssss",total_spaces
                filename = filename.replace(" ", "\ ", total_spaces)
                print "File Name2222222222",filename'''
            if base_path:
                filename = base_path + os.sep + filename
            print "Filename:::::::::",filename
            if not os.path.exists(filename):
                print "File Path Not Exists::::%s"%filename
                filename = None
        return filename
    except Exception, ex:
        print "Exception while checking valid valid filepath", ex

def merge_cells(workbook, worksheet, first_row, last_row, first_column, last_column, merge_text = "", merge_format = None):
    try:
        if not merge_format:
            merge_format = workbook.add_format({"align": "left"})
        worksheet.merge_range(first_row, first_column, last_row, last_column, merge_text, merge_format)
    except Exception, ex:
        print "Exception while merging cells row wise:::",ex

def write_header_list(workbook, worksheet, row, headers_list = [], write_format = None):
    try:
        if not write_format:
            write_format = workbook.add_format({"align":"center"})
        column = -1
        worksheet.set_row(row, 30)
        for each_header in headers_list:
            column += 1
            worksheet.write(row, column, each_header, write_format)
    except Exception, ex:
        print "Exception while writing in xls file", ex

def create_grid(workbook, worksheet, cell_first_row , cell_last_row, cell_first_col, cell_last_col, grid_text = "", grid_format = None):
    try:
        for each_row in xrange(cell_first_row, cell_last_row + 1):
            for each_col in xrange(cell_first_col, cell_last_col + 1):
                #print "Grid Row::%s  Grid Col::%s grid_text::%s  grid_format::%s"%(each_row, each_col,grid_text, grid_format)
                try:
                    worksheet.write(each_row, each_col, grid_text, grid_format)
                except Exception, ex:
                    print " Exception in create_grid write-----", str(ex)
    except Exception, ex:
        print "Exception while creating empty grid rowwise",ex

def design_header_and_footer(workbook, worksheet, header_text_fill_values = {},\
                             footer_text_fill_values = {}, image_filename = None, header_text_image_filename = None):
    try:
        print "Inside design_header_and_footer:::",image_filename, header_text_image_filename
        worksheet.set_margins(top=1.3)
        # Write Header Text Body
        if header_text_image_filename:
            header_text1 = ""
        else:
            header_text1 = '&C&"Courier New,Bold"&20' + DEFAULT_PLAYLIST_XLS_HEADER_TEXT
        if header_text_fill_values :
            header_text1 += '&R&10&"Courier New,Bold"Date:%s'%(header_text_fill_values.get("log_date", ""))
            #print "Header Text 1:::",header_text1
        if image_filename and not image_filename.startswith("/"):
            image_filename = "/" + image_filename
        if header_text_image_filename and not header_text_image_filename.startswith("/"):
            header_text_image_filename = "/" + header_text_image_filename
        if image_filename and header_text_image_filename:
            print "Header Text with image  %s ::::::%s"%(image_filename,header_text_image_filename)
            worksheet.set_header(header_text1 + '&L&G&C&G', {'image_left' : image_filename,\
                                                            'image_center' : header_text_image_filename})
        elif image_filename and not header_text_image_filename:
            print "Header Text with image::::::%s"%(image_filename)
            worksheet.set_header(header_text1 + '&L&G', {'image_left' : image_filename})
        elif header_text_image_filename and not image_filename:
            print "Header Text with image::::::%s"%(header_text_image_filename)
            worksheet.set_header(header_text1 + '&C&G', {'image_center' : header_text_image_filename})
        else:
            worksheet.set_header(header_text1)
        # write Footer Text Body
        user = "ADMIN"
        if footer_text_fill_values:
            user = footer_text_fill_values.get("username", "ADMIN")
        footer_text1 = '&L&"Courier New"&6Report Generated by: %s\
            &C&"Courier New"&6Page &P of &N&R&"Courier New"&6Report Generated on:&D &T'%(user)
        print "Footer Text::::",footer_text1
        worksheet.set_footer(footer_text1)
    except Exception, ex:
        print "Exception arised during design of header and footer::::",ex

def write_playlist_in_xls(channel_info, user, log_date, play_list, headers_list, \
        ordered_dict_key_list, filename="test.xlsx", merge_format_details = None):
    try:
        CHANNEL_LOGO_FILEPATH = "/opt/topspot/web_service/client/images/logo/Raj_xls_logos"
        '''default_channel_info_image_filepath = None
        default_channel_info_image_filepath = "/opt/topspot/web_service/client/images" + \
            "/logo/sushee_strip_for_centre_Headder_logs_imports.jpg"'''
        COLUMN_START_ALBHABET = "A"
        COLUMN_START_ALBHABET_ASCII = ord(COLUMN_START_ALBHABET)
        xls_file_path = EXPORT_PATH + os.sep + filename
        workbook = xlsxwriter.Workbook(xls_file_path)
        worksheet = workbook.add_worksheet()
        worksheet.center_horizontally()
        worksheet.fit_to_pages(1, 0)
        style_format = workbook.add_format()
        border =  workbook.add_format({'border': 2})
        bold = workbook.add_format({'bold': True})
        # Set Header Footer
        footer_text_values = {"username" : user}
        header_text_values = {"log_date" : log_date}
        if channel_info:
            header_text_values.update({"channel_address" : channel_info.get("address",{}), \
                "channel_telephone" : channel_info.get("telephone","")})
        image_file = channel_info.get("channel_logo_name", None)
        '''if image_file:
            image_file = image_file.strip()
            if image_file.find(" "):
                total_spaces = image_file.count(" ")
                image_file.replace(" ", "\ ", total_spaces)
            image_file = CHANNEL_LOGO_FILEPATH + os.sep + image_file
            print "Image File:::::::::",image_file
            if not os.path.exists(image_file):
                print "Image File Path Not Exists for Header Logo::::%s"%image_file
                logging.info("Image File Path Not Exists for Header Logo::::%s"%image_file)
                image_file = None'''
        logo_image = check_valid_filepath(image_file, CHANNEL_LOGO_FILEPATH)
        print "Logo Image Received after validation:::::",logo_image
        #header_text_image = check_valid_filepath(default_channel_info_image_filepath)
        header_text_image = check_valid_filepath(DEFAULT_CHANNEL_INFO_IMAGE_FILEPATH)
        design_header_and_footer(workbook, worksheet, header_text_values, footer_text_values,\
            logo_image, header_text_image)

        # Set Column width and  style format:::
        worksheet.set_column(0, 0, 10, None) #workbook.add_format({"valign":"vjustify", "border" : 1})) # Break Name
        worksheet.set_column(1, 1, 5, None) #workbook.add_format({"valign":"vjustify", "border" : 1}))  # Break Position
        worksheet.set_column(2, 2, 10, None) #workbook.add_format({"valign":"vjustify", "border" : 1})) # RO Code
        #worksheet.set_column(3, 3, 9, None) #workbook.add_format({"valign":"vjustify", "border" : 1})) # Spot Type
        worksheet.set_column(3, 3, 10, None) #workbook.add_format({"valign":"vjustify", "border" : 1})) # Brand
        worksheet.set_column(4, 4, 15, None) #workbook.add_format({"bold":True,"valign":"vjustify", "border" : 1})) # Clip Name Tape
        worksheet.set_column(5, 5, 5, None) #workbook.add_format({"valign":"vjustify", "border" : 1}))  # Duration
        worksheet.set_column(6, 6, 10, None) #workbook.add_format({"valign":"vjustify", "border" : 1})) # Time Schedule
        worksheet.set_column(7, 7, 15, None) #workbook.add_format({"valign":"vjustify", "border" : 1}))  # Remarks
        #worksheet.set_default_row(24)
        DEFAULT_WORKSHEET_STYLE_FORMAT = workbook.add_format({"font_size":8, \
            "align":"center", "text_wrap":True,"valign":"top","border" : 1})
        DEFAULT_WORKSHEET_STYLE_MAP = {"font_size" : 8, \
            "align" : "center", "text_wrap" : True,"valign" : "top","border" : 1}
        HEADER_STYLE_FORMAT = workbook.add_format({"font_size":10,"align":"center",\
            "text_wrap":True,"border":1,"valign":"top","bold":True})
        PROGRAM_STYLE_FORMAT = workbook.add_format({"font_size":10,"bold":True, "fg_color":"#C0C0C0","border":1})
        MERGED_STYLE_FORMAT = workbook.add_format({"font_size": 10, "bold":True,"fg_color": "#00FFC0", "border" : 1})
        #print "Workbook created:::",workbook
        #print "Play list len:::",len(play_list)
        #print "play list path::::",xls_file_path
        row = 0
        program_name_list = []
        total_column = len(headers_list)
        #print "Initial Row:::%s  Header List:::%s"%(row, headers_list)
        write_header_list(workbook, worksheet, row, headers_list, HEADER_STYLE_FORMAT)
        if len(play_list) == 0:
            design_header_and_footer(workbook, worksheet, header_text_values,\
                footer_text_values, logo_image, header_text_image)
            workbook.close()
            return {"filename":filename}
        print "Play List Length received from ui as:::",len(play_list)
        program_name_list = list(set([(each_schedule.get("program_id", None),\
            each_schedule.get("program_start_time", "00:00:00")) for each_schedule in play_list]))
        program_name_list = sorted(program_name_list, key = itemgetter(1))
        first_prog_start_time = program_name_list[0][1]
        last_prog_start_time =  program_name_list[-1][1]
        final_program_name_list = [each_prog[0] for each_prog in program_name_list]
        print "Total Individual Program Names",len(final_program_name_list)
        final_play_list = []
        total_break_progwise = 0
        for each_prog in final_program_name_list:
            play_list_program_wise = [matched_prog for matched_prog in play_list\
                                      if matched_prog.get("program_id", None) == each_prog]
            play_list_program_wise = sorted(play_list_program_wise, key = itemgetter("break_start_time", "start_time"))
            total_break_progwise += len(play_list_program_wise)
            final_play_list.append(play_list_program_wise)
        print "Total Break program wise::::",total_break_progwise
        total_break_final = 0
        for each_prog_list in final_play_list:
            if len(each_prog_list) == 0: 
                continue
            prog_break_write_style_format = DEFAULT_WORKSHEET_STYLE_FORMAT
            play_list_break_wise = []
            total_break_duration = 0.0
            each_break_total_duration = 0.0
            cell_first_col = 0
            row += 1
	    program_name_row = row
            cell_first_row = cell_last_row = program_name_row
            cell_last_col = total_column - 1
            create_grid(workbook, worksheet, cell_first_row , cell_last_row,\
                cell_first_col, cell_last_col, "", DEFAULT_WORKSHEET_STYLE_FORMAT)
            # Merge Cells to create a program name row
            if cell_first_col != cell_last_col:
                prog_info = None
                prgm_obj_id = each_prog_list[0].get("program_id", None)
                prog_name = each_prog_list[0].get("prgm_name", "")
                prog_color = None
                if prgm_obj_id:
                    prog_info = db.programs.find_one({"_id":ObjectId(str(prgm_obj_id))})
                    if not prog_info:
                        prog_info = {}
                    if not prog_name:
                        prog_name = prog_info.get("program_name", "")
                    if prog_info.get("color") and re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(prog_info["color"])):
                        prog_color = prog_info.get("color")
                prog_merge_sub_text = ""
                if prog_info.get("start_time", None) and prog_info.get("end_time", None):
                    prog_merge_sub_text = prog_info.get("start_time", "") + " - " + prog_info.get("end_time", "")
                else:
                    prog_merge_sub_text = prog_name
                if merge_format_details and merge_format_details.get("playlist_grouped_xls_program_name"):
                    if prog_merge_sub_text != prog_name:
                        prog_merge_sub_text = prog_name + prog_merge_sub_text
                prog_merge_text = " Program : " + prog_merge_sub_text
                if prog_color and merge_format_details and merge_format_details.get("playlist_grouped_xls_program_color"):
                    prog_break_write_style_map = copy.copy(DEFAULT_WORKSHEET_STYLE_MAP)
                    prog_break_write_style_map["fg_color"] = prog_color
                    prog_break_write_style_format = workbook.add_format(prog_break_write_style_map)
                merge_cells(workbook, worksheet, cell_first_row, cell_last_row, cell_first_col, \
                        cell_last_col, prog_merge_text, PROGRAM_STYLE_FORMAT)
            #break_name_list = list(set([each_break.get("break_name","BRK") for each_break in each_prog_list]))
            break_name_list = []
            for each_break in each_prog_list:
                break_name = each_break.get("break_name","BRK")
                if break_name not in break_name_list:
                    break_name_list.append(break_name)
            #print "Break List!!!!!!!!!!!",break_name_list
            for each_break_name in break_name_list:
                play_list_break_wise.append([each_break for each_break in each_prog_list \
                                           if each_break.get("break_name",None) == each_break_name])
            for each_break_list in play_list_break_wise:
                break_row_start_index = None
                cell_first_col = 0
                cell_last_col = total_column - 1
                each_break_total_duration = 0.0
                if len(each_break_list) > 0 :
                    break_row_start_index = row + 1
                for each_break in each_break_list:
                    string_max_len = max([len(str(each_value)) for each_value in each_break.values() if type(each_value) not in [dict, list, set]])
                    row += 1
                    cell_first_row = cell_last_row = row
                    worksheet.set_row(cell_first_row, string_max_len)
                    '''create_grid(workbook, worksheet, cell_first_row , cell_last_row, \
                        cell_first_col, cell_last_col, "", DEFAULT_WORKSHEET_STYLE_FORMAT)'''
                    create_grid(workbook, worksheet, cell_first_row , cell_last_row, \
                        cell_first_col, cell_last_col, "", prog_break_write_style_format)
                    for dict_key in each_break:
                        if dict_key not in ordered_dict_key_list:
                            continue
                        col_index = ordered_dict_key_list.index(dict_key)
                        if len(headers_list) < col_index:
                            continue
                        cell_write_value = ""
                        if headers_list[col_index] == "Remarks":
                            dp_time = each_break.get("dp_start_end_time", {})
                            if dp_time and dp_time.get("dp_start_time","") and dp_time.get("dp_end_time",""):
                                cell_write_value = "Ordered Start Time: %s"\
                                    %dp_time["dp_start_time"] + \
                                    " Ordered End Time: %s"%dp_time["dp_end_time"]
                        else:
                            cell_write_value = each_break[dict_key]
                        #worksheet.write(row, col_index, cell_write_value, DEFAULT_WORKSHEET_STYLE_FORMAT)
                        worksheet.write(row, col_index, cell_write_value, prog_break_write_style_format)
                        if dict_key == "duration" and each_break[dict_key]:
                            each_break_total_duration += float(each_break[dict_key])
                    total_break_final += 1
                total_break_duration += each_break_total_duration
                # Merge First Column Containing only Break Name
                if "break_name" in ordered_dict_key_list:
                    merge_column_index = ordered_dict_key_list.index("break_name")
                    first_column = last_column = merge_column_index
                    merge_text = each_break["break_name"]
                    if break_row_start_index and break_row_start_index != row:
                        '''merge_cells(workbook, worksheet, break_row_start_index, row, \
                            first_column, last_column, merge_text, DEFAULT_WORKSHEET_STYLE_FORMAT)'''
                        merge_cells(workbook, worksheet, break_row_start_index, row, \
                            first_column, last_column, merge_text, prog_break_write_style_format)
                break_row_last_index = row
                # Merge Cells to create Break Total Row
                row += 1
                create_grid(workbook, worksheet, row, row, cell_first_col,\
                    cell_last_col, "", DEFAULT_WORKSHEET_STYLE_FORMAT)
                last_merge_col = (total_column-1) - 3
                last_col_merge = last_merge_col
                if first_column != last_col_merge:
                    merge_text = "   ***BREAK TOTAL***"
                    merge_cells(workbook, worksheet, row, row, first_column, last_col_merge, merge_text, MERGED_STYLE_FORMAT)
                    # This part is to assign a formula for a specific column
                    '''if last_col_merge + 1 <= total_column -1:
                        first_row_col_index_alphabet = chr(COLUMN_START_ALBHABET_ASCII + last_col_merge + 1) + \
                            str(break_row_start_index + 1) # As Excel Rows start from numeric 1
                        last_row_col_index_alphabet = chr(COLUMN_START_ALBHABET_ASCII + last_col_merge + 1) + \
                            str(break_row_last_index + 1)
                        print "first_row_col_index_alphabet:::%s  last_row_col_index_alphabet:::%s"\
                            %(first_row_col_index_alphabet, last_row_col_index_alphabet)
                        sum_formula = "=SUM({0}:{1})".format(first_row_col_index_alphabet, last_row_col_index_alphabet)
                        print "SUM Formula:::",sum_formula
                        last_col_merge += 1
                        worksheet.write_formula(row, last_col_merge, sum_formula, merge_style_format)
                        if last_col_merge + 1 != total_column -1:
                            merge_style_format = workbook.add_format({"bold":True, \
                                "num_format":"hh:mm:ss" ,"fg_color": "#000080"})
                            merge_cells(workbook, worksheet, row, row, last_col_merge + 1,\
                                total_column -1, sum_formula, merge_style_format)'''
                    last_col_merge += 1
                    if last_col_merge <= total_column -1:
                        worksheet.write(row, last_col_merge, str(int(each_break_total_duration)), MERGED_STYLE_FORMAT)
                        last_col_merge += 1
                        dur_in_hms = convert_seconds_to_hms_format(int(each_break_total_duration))
                        dur_in_hms = "(%s)"%dur_in_hms
                        if last_col_merge == total_column -1:
                            worksheet.write(row, last_col_merge, dur_in_hms, MERGED_STYLE_FORMAT)
                        elif last_col_merge < total_column -1:
                            merge_cells(workbook, worksheet, row, row, last_col_merge,\
                                total_column -1, dur_in_hms, MERGED_STYLE_FORMAT)
            merge_text = "   ***PROGRAM TOTAL***"
            row += 1
            last_col_merge = last_merge_col
            merge_cells(workbook, worksheet, row, row, first_column, last_col_merge, merge_text, PROGRAM_STYLE_FORMAT)
            last_col_merge += 1
            if last_col_merge <= total_column -1:
                worksheet.write(row, last_col_merge, str(int(total_break_duration)), PROGRAM_STYLE_FORMAT)
                last_col_merge += 1
                dur_in_hms = convert_seconds_to_hms_format(int(total_break_duration))
                dur_in_hms = "(%s)"%dur_in_hms
                if last_col_merge == total_column -1:
                    worksheet.write(row, last_col_merge, dur_in_hms, PROGRAM_STYLE_FORMAT)
                elif last_col_merge < total_column -1:
                    merge_cells(workbook, worksheet, row, row, last_col_merge,\
                        total_column -1, dur_in_hms, PROGRAM_STYLE_FORMAT)
        print "Total Break counted as::",total_break_final
        #design_header_and_footer(workbook, worksheet, header_text_values_list, footer_text_values_list, image_file)
        workbook.close()
        print "File Name To be returned:::",filename
        return {"filename":filename}
    except Exception, ex:
        print "Exception in write_playlist_in_xls",ex

#################################### Generate a unique Sequence ID #########################
'''def get_uid_sequence(Label=""):
    date_year_month=dt.now().strftime("%Y%m")
    return Label+date_year_month'''
    
    
##################################### CG ########################################    

def cg_recon_status(cg_as_run_logs):
    onaired = []
    run_with_discrepancy = [] 
    try:
        for log in cg_as_run_logs:
            if 'dp_start_time' in log and 'dp_end_time' in log: 
                if compare_datetime(
                          log["real_start_time"], '>=', log["dp_start_time"], 'time') and\
                   compare_datetime(
                          log["real_start_time"], '<', log["dp_end_time"], 'time'):
                    log["status"] = "On Aired"
                    onaired.append(log)
                else:
                    log["status"] = "Run with discrepancy"
                    run_with_discrepancy.append(log)
        return onaired,run_with_discrepancy
    except Exception, ex:
        print "Exception in cg_recon::::::::::::%s"%str(ex)  
        
#################################### DASHBOARD TODAY ORDERS ##################        

def get_program_start_end_time(program_id, program_generated_from):
    try:
        program = {}
        program_start_time = program_end_time = None
        if program_generated_from == "master" :
            program = db.master_programs.find_one({"_id": ObjectId(program_id), "status" : {"$ne" : "deleted"}})
        else :
            program = db.special_programs.find_one({"_id":ObjectId(program_id), "status" : {"$ne" : "deleted"}})
        if not program : return (program_start_time,program_end_time)
        elif not (program.get("start_time") and program.get("duration") is not None) : return (program_start_time,program_end_time)
        program_start_time = program["start_time"]
        program_end_time = get_end_time(program_start_time,program["duration"])
        print "prgm start and edn",program_start_time,program_end_time
        return (program_start_time,program_end_time)
    except Exception, ex :
        print "Exception in get_program_start_end_time : reson :%s"%str(ex)
    return (program_start_time,program_end_time)
#################################### BULK RO INVENTORY ######################################

def get_bro_program_wise_quota_inventory(quota):
    try:
        months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        master_programs = db.master_programs
        #special_programs = db.special_programs
        program_wise_inventory = {}
        bulk_ro_programs = db.bulk_orders.find({},{"programs":1, "_id":0})
        for bulk_ro in bulk_ro_programs:
            for program in bulk_ro["programs"]:
                month_range = get_months_between_dates(program["start_date"], program["end_date"])
                consumed = int(program["duration"]) / len(month_range)
                if program["program_wise"] and program["program_gen_from"] == "master":
                    master_pgm = master_programs.find_one({"_id": ObjectId(program["program_id"])}) 
                    program_name = str(master_pgm["program_name"])
                    program_wise_inventory[program_name] = {}
                    episodes = get_number_of_episodes_in_month(program["start_date"], master_pgm['days'])
                    for month in month_range:
                        program_wise_inventory[program_name][month] = {}
                        program_wise_inventory[program_name][month]["total"] = (int(episodes) * ONE_EPISODE_DURATION)
                        program_wise_inventory[program_name][month]["consumed"] = consumed
                        program_wise_inventory[program_name][month]["free"]  = \
                        program_wise_inventory[program_name][month]["total"] - program_wise_inventory[program_name][month]["consumed"]
                    for month in months_list:
                        if month not in program_wise_inventory[program_name]:
                            program_wise_inventory[program_name][month] = {}
                            program_wise_inventory[program_name][month]["total"] = (int(episodes) * ONE_EPISODE_DURATION)
                            program_wise_inventory[program_name][month]["consumed"] = 0
                            program_wise_inventory[program_name][month]["free"]  = \
                            program_wise_inventory[program_name][month]["total"] - program_wise_inventory[program_name][month]["consumed"]
                        if quota == "all":
                            pass
                        elif quota == "free":
                            del program_wise_inventory[program_name][month]["total"]
                            del program_wise_inventory[program_name][month]["consumed"]
                        elif quota == "total":
                            del program_wise_inventory[program_name][month]["consumed"]
                            del program_wise_inventory[program_name][month]["free"]
                        elif quota == "consumed":
                            del program_wise_inventory[program_name][month]["total"]
                            del program_wise_inventory[program_name][month]["free"]
        return program_wise_inventory
    except Exception, ex:
        print "Exception in get_bro_program_wise_quota_inventory: %s" %str(ex)

def get_bro_program_wise_type_inventory(ad_type):
    try:
        master_programs = db.master_programs
        months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        master_program_list = master_programs.find()
        #special_programs = db.special_programs
        program_wise_inventory = {}
        program_wise_inventory[ad_type] = {}
        for program in master_program_list:
            program_wise_inventory[ad_type][program["program_name"]] = {}
            for month in months_list:
                program_wise_inventory[ad_type][program["program_name"]][month] = {}
                program_wise_inventory[ad_type][program["program_name"]][month]["available"] = True
        bulk_ro_programs = db.bulk_orders.find({},{"programs":1, "_id":0})
        for bulk_ro in bulk_ro_programs:
            for program in bulk_ro["programs"]:
                if program["type"].strip().lower() == ad_type.strip().lower():
                    month_range = get_months_between_dates(program["start_date"], program["end_date"])
                    if program["program_wise"] and program["program_gen_from"] == "master":
                        program_name = master_programs.find_one({"_id": ObjectId(program["program_id"])})["program_name"]
                        for month in month_range:
                            program_wise_inventory[ad_type][program_name][month]["available"] = False
        return program_wise_inventory
    except Exception, ex:
        print "Exception in get_bro_program_wise_type_inventory: %s" %str(ex)



'''def get_bro_timeband_wise_inventory(quota):
    try:
        months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        consumed_dur = 0
        timeband_wise_inventory = {}
        orders = db.orders
        timeband_wise_inventory = {}
        bulk_ro_programs = db.bulk_orders.find({},{"programs":1, "_id":0})
        for bulk_ro in bulk_ro_programs:
            for program in bulk_ro["programs"]:
                if not program["program_wise"]:
                    order = orders.find_one({"start_date": program["start_date"], \
                                             "end_date": program["end_date"]},{"timebands": 1})["timebands"]
                    if order:
                        for timeband in order:
                            time_band = timeband["time_band"]
                            print "time_band ", time_band
                            timeband_wise_inventory[time_band] = {}
                            if program["type"] == timeband["type"]:
                                date_ranges = timeband[timeband["type"]]["date_ranges"]
                                for date_range in date_ranges:
                                    if compare_datetime(date_range["from"], '>=', program["start_date"], 'date',"%Y/%m/%d") and\
                                    compare_datetime(date_range["to"], "<=", program["end_date"], "date", "%Y/%m/%d"):
                                        month =  str(get_month_from_date(program["start_date"]))
                                        timeband_wise_inventory[time_band][month] = {}
                                        consumed_dur += int(timeband[timeband["type"]]["duration"]) * int(date_range["num_spots"])
                                        timeband_wise_inventory[time_band][month]["consumed"] = consumed_dur
                                        timeband_wise_inventory[time_band][month]["total"] = int(program["duration"])
                                        timeband_wise_inventory[time_band][month]["free"]  = \
                                        timeband_wise_inventory[time_band][month]["total"] - consumed_dur
                                        
        print "timeband_wise_inventory : ", timeband_wise_inventory
    except Exception, ex:
        print "Exception in get_bro_timeband_wise_inventory: %s" %str(ex)'''

def get_bro_client_wise_type_inventory(ad_type):
    try:
        months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        client_wise_inventory = {}
        client_wise_inventory[ad_type] = {}
        clients  = db.customers.find()
        for client in clients:
            client_name = client["name"]
            client_wise_inventory[ad_type][client_name] = {}
            for month in months_list:
                client_wise_inventory[ad_type][client_name][month] = {}
                client_wise_inventory[ad_type][client_name][month]["available"] = True
        bulk_ro_programs = db.bulk_orders.find({})
        for bulk_ro in bulk_ro_programs:
            for program in bulk_ro["programs"]:
                if program["type"].strip().lower() == ad_type.strip().lower():
                    month_range = get_months_between_dates(program["start_date"], program["end_date"])
                    if "client_id" in bulk_ro and bulk_ro["client_id"]:
                        client_name = db.customers.find_one({"_id": ObjectId(bulk_ro["client_id"])})["name"]
                        for month in month_range:
                            client_wise_inventory[ad_type][client_name][month]["available"] = False
        return client_wise_inventory
    except Exception, ex:
        print "Exception in get_bro_client_wise_type_inventory: %s" %str(ex)

def get_order_details(channel_id,date):
    errors = []
    orders_list = []
    all_orders_list = []
    try:
        if channel_id and date:
            orders_list = json_friendly(list(db.orders.find({
               "end_date": {"$gte": date},
               "start_date": {"$lte": date},
               "status": "active",
               "channel_id": channel_id})))
            orders_length = len(orders_list)
            for order in orders_list:
                order_details = {}
                order_details["_id"] = str(order.get("_id"))
                order_details["start_date"] = order.get("start_date")
                order_details["end_date"] = order.get("end_date")
                order_details["ro_date"] = order.get("ro_date")
                order_details["booking_date"] = order.get("booking_date")
                order_details["order_id"] =  str(order.get("_id"))
                customer_id = order.get("customer")
                if customer_id != None:
                    cust_details = db.customers.find_one({"_id":ObjectId(str(customer_id))})
                    order_details["customer"] = cust_details.get("name")
                agency_id = order.get("agency_id")
                if agency_id != None:
                    agency_details = db.agencies.find_one({"_id":ObjectId(str(agency_id))})
                    order_details["agency"] = agency_details.get("name")
                order_details["ro_num"] = order.get("ro_num")
                order_details["ro_id"] = order.get("ro_id")
                order_details["timebands"] = order.get("timebands")
                order_details["one_spot_billing"] = order.get("one_spot_billing")
                all_orders_list.append(order_details)
            return all_orders_list

    except Exception, ex:
        print "Exception in get_order_details:   %s" % ex
        logging.exception("Exception in get_order_details : "+str(ex))

def get_today_orders(channel_id,date):
    today_orders_list = []
    orders_length = 0
    order_details = []
    today_orders_count = 0
    Today_orders = False
    try:
        order_details = get_order_details(channel_id,date)
        for order in order_details:
            clip_list = []
            if order:
                timebands = order.get("timebands")
                del order["timebands"]
                for band in timebands:
                  if "date_ranges" in band[band['type']]:  
                    dt_ranges = band[band['type']]['date_ranges']
                    for dt in dt_ranges:
                        if compare_datetime(date,'>=',dt.get("from") ,'date', '%Y/%m/%d') \
                             and compare_datetime(date,'<=',dt.get("to") ,'date', '%Y/%m/%d'):
                             order_spots = dt.get("num_spots",0)
                             if order_spots > 0 :
                                 Today_orders = True
                                 clip_list.append(band[band['type']]['caption'])
                if Today_orders:
                    order["clips"] = clip_list
                    today_orders_count =+ 1
                    today_orders_list.append(order)
        return today_orders_list
    except Exception, ex:
        print "Exception in get_today_orders:   %s" % ex
        logging.exception("Exception in get_today_orders : "+str(ex))     

################################## INVOICE VOLUME #############################
def num_to_words(number):
   try:
        if number:  
            words = num2words(int(number))       
            return num2words(int(number), lang="en_IN") + " Rupees Only"  
   except Exception, ex:
       print "Exception in Num_to_words", ex
   return ""

def tax_additions(gross_amt,billing_type,agency):
    final_cost = 0
    agency_comm = 0.0
    discounted_amt = 0.0
    service_tax = 0.0
    swatch_bharat = 0.0
    krishi_kalyan = 0.0
    net_taxable_amount = 0.0
    try:
        #print "BILLING TYPE:::::::::::::::::;;",billing_type
        #print "GROSS AMOUNT TO TAX CALCULATIONS:::",gross_amt
        logging.info("GROSS AMOUNT TO TAX CALCULATIONS::: %s"%(gross_amt))
        invoice_master_details = db.invoice_master.find_one()
        #print "Invoice Master Details::::",invoice_master_details
        logging.info("Invoice Master Details :: %s"%(invoice_master_details))
        net_taxable_amount = gross_amt
        if invoice_master_details:
            if agency and billing_type == "gross":
                agency_comm = float(gross_amt) * (float(invoice_master_details.get("agency_commission"))/ 100)
                #print "Agency Commission:::::;;",agency_comm
                logging.info("Agency Commission::::::: %s"%(agency_comm))
                discounted_amt = float(gross_amt) - float(agency_comm)   
                net_taxable_amount = discounted_amt
            service_tax = float(net_taxable_amount) * (float(SERVICE_TAX)/ 100)
            #print "Service Tax:::::;",service_tax
            logging.info("Service Tax::::::: %s"%(service_tax))
            swatch_bharat = float(net_taxable_amount) * (float(SWACHH_BHARAT_PERCENTAGE)/ 100)
            #print "Swatch Bharath Cess::::",swatch_bharat
            logging.info("Swatch Bharath Cess::::::: %s"%(swatch_bharat))
            krishi_kalyan = float(net_taxable_amount) * (float(KRISHI_KALYAN_CESS_PERCENTAGE)/ 100)    
            #print "Krishi Kalyan Cess::::",krishi_kalyan
            logging.info("Krishi Kalyan Cess::::::: %s"%(krishi_kalyan))
            final_cost = round(float(service_tax + swatch_bharat + krishi_kalyan + net_taxable_amount))
            #print "Final Cost::::::::::",final_cost
            logging.info("FINAL COST::::::: %s"%(final_cost))
            return {"final_cost": final_cost, "krishi_kalyan_cess":"%.2f" % krishi_kalyan,\
                    "swatch_bharat":"%.2f" % swatch_bharat, "service_tax":"%.2f" % service_tax,\
                    "agency_discount":"%.2f" % agency_comm, "gross_amount":"%.2f" % gross_amt,\
                    "net_taxable_amount":"%.2f" % net_taxable_amount} 
    except Exception, ex:
       print "Exception in tax additions", ex
        
            
############################## BILLING ######################################
def calculate_total_ro_amount(ro_details):
    total_amt = 0
    try:
       if not ro_details:
           print "No ro details Hence retuning"
           return
       timebands = ro_details.get("timebands")
       if not timebands:
           return
       for band in timebands:
          print "TTTTB IDDDDDD",band.get("tb_id")
    
	  rate_per_package = 0.0
          final_tb_rate = 0.0
	  if "date_ranges" in  band[band['type']]:
	      dt_ranges = band[band['type']]['date_ranges']
	  else:
	      continue    
	  package_details = band.get("package_detail")
	  tb_advt_type_details  = band[band['type']]
	  if package_details == 'per_day':
	      rate_per_package = float(band.get('rate',0))
	  elif package_details == 'per_10_sec':
	      rate_per_package = float(band.get('rate',0))/10
	  elif package_details == "per_15_sec":
	      rate_per_package = float(band.get('rate',0))/15
	  elif package_details == "per_30_min":
	      rate_per_package = float(band.get('rate',0))
	  elif package_details == "per_unit":
	      rate_per_package = float(band.get('rate',0))
	  dur = tb_advt_type_details.get('duration')
	  if dur=="" and tb_advt_type_details.get('clip_id'):
	     ad_type_query = {}
	     ad_type_query["status"] = "active"
	     ad_type_query["ad_type_identity"] = re.compile(band.get("type"), re.IGNORECASE)
	     advt_type_details = db.ad_types.find_one(ad_type_query)
	     if is_valid_commercial(advt_type_details):
		clip_details = db.commercials.find_one({'_id':ObjectId(tb_advt_type_details.get('clip_id'))})
		if clip_details:
		   dur  = float(clip_details.get('dur')/1000)
	     elif not advt_type_details.get('time_consumable'):
		  dur  = 0     
	  if dur == "":        
	       dur = 0
	  paid_spots = 0
	  bonus_spots = 0
	  order_spots = 0
	  if band.get('spot_type') =='paid':
	     for dt in dt_ranges:
                 start_date = dt.get("from")
                 end_date = dt.get("to")
		 diff = 0
		 dt_paid_spots = 0
		 order_spots = dt.get("num_spots",0)
		 diff = get_diff_btwn_dates(start_date,end_date)
		 if diff >= 0:
		     dt_paid_spots = (diff+1)*order_spots
		     paid_spots = paid_spots + dt_paid_spots
		 if order_spots > 0:
		    if package_details == "per_day":
		        final_tb_rate = final_tb_rate + float( rate_per_package)*int(diff+1)
		    elif package_details == "per_unit":
		        final_tb_rate += float( rate_per_package)*int(dt_paid_spots)
		    else:
		        final_tb_rate += float( rate_per_package)*float(dur)*int(dt_paid_spots)
	  elif band.get('spot_type') =='bonus':
	       for dt in dt_ranges:
                 start_date = dt.get("from")
                 end_date = dt.get("to")
		 diff = 0
		 order_spots = dt.get("num_spots",0)
		 diff = get_diff_btwn_dates(start_date,end_date)
		 if diff >= 0:
		     bonus_spots = bonus_spots + (diff+1)*order_spots
		 if order_spots > 0:
		    final_tb_rate = 0.0
          print "FINNNNNNNNNNNNNNNNNNNNNN",final_tb_rate
          total_amt =  total_amt +  final_tb_rate
          print "Total tb rate calculated",total_amt
       return total_amt

    except Exception,ex:
        print "Exception in calculate_total_ro_amount",ex

def get_timeband_details(ro_details):
    try:
        zipped_timeband = []
        timebands = ro_details['timebands']
        for timeband in timebands:
            timeband_dict = {}
            if "type" in timeband:
                advt_type = timeband['type']
                timeband_dict['advt_type'] = timeband['type']
                if "caption" in timeband[advt_type]:
                    timeband_dict['clip'] = timeband[advt_type]["caption"]
                if "user_media_caption" in timeband[advt_type]:
                    timeband_dict['brand'] = timeband[advt_type]["user_media_caption"]
                if "media_vertical" in timeband[advt_type]:
                    timeband_dict['vertical'] = timeband[advt_type]['media_vertical']
                if "vid" in timeband[advt_type] and timeband[advt_type]["vid"]:
                    timeband_dict['vid'] = int(timeband[advt_type]['vid'])
                else:
                    vertical_details = db.verticals.find_one({"name":timeband[advt_type]['media_vertical']})
                    if vertical_details:
                        timeband_dict['vid'] = int(vertical_details.get("vid"))
                if "media_subvertical" in timeband[advt_type]:
                    timeband_dict['sub_vertical'] = timeband[advt_type]['media_subvertical']
                if "subvid" in timeband[advt_type] and timeband[advt_type]["subvid"]:
                    timeband_dict['subvid'] = int(timeband[advt_type]['subvid']) 
            if "spot_type" in timeband:
                timeband_dict['spot_type'] = timeband['spot_type']
            if "priority" in timeband:
                timeband_dict['priority'] = timeband['priority']
            if "position" in timeband:
                timeband_dict['position'] = timeband['position']
            zipped_timeband.append(timeband_dict)
        print zipped_timeband
        return zipped_timeband
    except Exception, ex:
        print "Exception in get_timeband_details::::",str(ex)

def ro_data_modification(data):
    errors = []
    ro_modification = {}
    client_code = ""
    cust_id = None
    agency_id=  None
    agency_code = ""
    branch_id = None
    branch_name = ""
    sales_name = ""
    total_ro_amount = 0 
    try:
        #print "daaaaaaaaaattttttttttttttttt",data
        if not data:
           errors.append("Ro data is empty")
           logging.errors("Ro data is empty")
           return
        ro_modification["_id"] = str(data.get("_id"))
        cust_id = data.get("customer")
        if cust_id:
            customer_details = db.customers.find_one({"_id":ObjectId(str(cust_id))})
            if customer_details:
               if "clientcode" in customer_details and customer_details["clientcode"]:
                   ro_modification["clientcode"] = customer_details.get("clientcode")           
        agency_id = data.get("agency_id")
        if agency_id:
            agency_details = db.agencies.find_one({"_id":ObjectId(str(agency_id))})
            if agency_details:
               if "agencycode" in agency_details and agency_details["agencycode"]:
                   ro_modification["agencycode"] = agency_details.get("agencycode")  
        else:
             ro_modification['agencycode'] = "107625"                     
        branch_id = data.get("branch_id")
        if branch_id:
            branch_details = db.branches.find_one({"_id":ObjectId(str(branch_id))})
            if branch_details:
               if "name" in branch_details and branch_details["name"]:
                   ro_modification["branch_name"] = branch_details.get("name")           
        sales_id = data.get("sales_ex")
        if sales_id:
            sales_details = db.users.find_one({"_id":ObjectId(str(sales_id))})
            if sales_details:
               if "first_name" in sales_details and sales_details["first_name"]:
                   ro_modification["sales_ex_name"] = sales_details.get("first_name")     
               if 'sales_empid' in sales_details and sales_details['sales_empid']:  
                   ro_modification['sales_empid'] = sales_details.get('sales_empid')
        if "ro_num" in data and data["ro_num"]:
            ro_modification["ro_num"] = data["ro_num"]           
        if "booking_date" in data and data["booking_date"]:
            ro_modification["booking_date"] = data["booking_date"]
        if "ro_date" in data and data["ro_date"]:
            ro_modification["ro_date"] = data["ro_date"]
        if "start_date" in data and data["start_date"]:
            ro_modification["start_date"] = data["start_date"]
        if "end_date" in data and data["end_date"]:
            ro_modification["end_date"] = data["end_date"]
        if "channel_id" in data and data["channel_id"]:
            ro_modification["channel_id"] = data["channel_id"]
        if "remarks" in data and data["remarks"]:
            ro_modification["remarks"] = data["remarks"]
        if "ro_id" in data and data["ro_id"]:
            ro_modification["ro_id"] = data["ro_id"]
        if "receipt_no" in data and data["receipt_no"]:
            ro_modification["receipt_no"] = data["receipt_no"]
        if 'advance_payment' in data and data['advance_payment']:
            ro_modification['advance_payment'] = data['advance_payment']                            
        total_ro_amount = calculate_total_ro_amount(data)
        timebands = get_timeband_details(data)
        if timebands:
            ro_modification['timebands'] = timebands 
        ro_modification['total_ro_amount'] = "%.2f" % total_ro_amount
        print "modified ro details------------------------", ro_modification["total_ro_amount"] 
        return ro_modification            
    except Exception,ex:
        print "Exception in ro_data_modification",ex

def change_agency_to_inhouse_format(agency):
    try:
        data = {}
        data['name'] = agency['agencyname']
        data['agencycode'] = agency['agencycode']
        data['agency_type'] = agency['agencytype']
        data['parentid'] = agency['parentid']
        data['location'] = agency["location"]
        data['paymode'] = agency['paymode']
        data['creditdays'] = agency['creditdays']
        data['contact_name'] = agency['contactperson']
        data["gst_address"] = agency["gstaddress"]
        data['address'] = {}
        data['address']['city'] = agency['location']
        data['address']['street'] = agency['address1']
        data['address']['area'] = agency['address2']
        data['address']['landmark'] = agency['address3']
        data['address']['pincode'] = agency['pincode']
        if 'gststate' in agency and agency['gststate'] != "*":
            data['address']['state'] = agency['gststate']
            if "gstno" in agency and agency['gstno'] != '0':
               data['gst_no'] = agency['gstno']
               data['gst_status'] = "registered"
            else:
                data['gst_status'] = "unregistered"
        if "pancardnumber" in agency:
            data['pan_num'] = agency['pancardnumber']
        
        data['status'] = "active"
        data['channel_id'] = "vml"
        return data
    except Exception, ex:
        print "Exception in change_agency_to_inhouse_format",str(ex)

def change_customer_to_inhouse_format(client):
    try:
        data = {}
        data['name'] = client['clientname']
        data['status'] = "active"
        data['channel_id'] = "vml"
        data['telephone'] = client['phoneno']
        data['address'] = {}
        data['address']['city'] = client['city']
        data['address']['area'] = client['address2']
        data['address']['street'] = client['address1']
        data['address']['landmark'] = client['address3']
        data['address']['pincode'] = client['pincodeno']
        if 'gststate' in client and client['gststate'] != "*":
            if "gstno" in client and client['gstno'] != '0':
               data['gst_no'] = client['gstno']       
               data['gst_status'] = "registered"
            else:
                data['gst_status'] = "unregistered"

            data['address']['state'] = client['gststate']
        data['clientcode'] = client['clientcode']
        if "email" in client:
            data['email'] = client['email']
        if "contactperson" in client:
            data['contact_person'] = client['contactperson']
        if "panno" in client:
            data['pan_num'] = client['panno']

        data['gst_status'] = "unregistered"    
        return data  
    except Exception, ex:
        print "Exception in change_customer_to_inhouse_format",str(ex)

def get_clips_info_from_invoice(clips):
    invoice_list = []
    try:
        for clip in clips:
            if "count" in clip:
                del clip['count']
            if "date" in clip:
                del clip['date'] 
            #clip_name['caption'] = clip
            #clip_name['timeband'] = timeband
            clip['unit'] = clip.pop('package_detail')
            invoice_list.append(clip)
        #print "final invoice_details----------------", invoice_list
        return invoice_list
    except Exception, ex:
        print "Exception in get_clips_info_from_invoice::::::",str(ex)

def get_telecast_data(invoice_no):
    telecast_list = [] 
    try:
        telecast = db.telecast.find_one({"telecast_num":invoice_no},{"ads_log":1})
        #print "telecast--------------",telecast
        for ad_log in telecast['ads_log']:
            telecast_dict = {}
            if "date" in ad_log: 
                telecast_dict['telecast_date'] = ad_log['date']
            if "program_name" in ad_log:
                telecast_dict['programme'] = ad_log['program_name']
            if "real_start_time" in ad_log:
                telecast_dict['telecast_time'] = ad_log['real_start_time'] 
            if "_id" in ad_log:
                telecast_dict['unique_id'] = str(ad_log['_id'])
            telecast_list.append(telecast_dict)
        #print "telecast list",telecast_list
        return telecast_list
    except Exception, ex:
        print "Exception in get_telecast_data::::",str(ex)

def change_invoice_format(data):
    bill_to = None
    final_invoice = {}
    try:
        print "data----------",data
        if 'tax_and_final_cost' in data:
            final_invoice.update(data['tax_and_final_cost'])
        if "invoice_num" in data:
            final_invoice['invoice_no'] = data['invoice_num']
        if "invoice_date" in data:
            final_invoice['invoice_date'] = data['invoice_date']
        if "invoice_num" in final_invoice:
            del final_invoice['invoice_num']
        if "customer" in data:
            order_details = db.orders.find_one({'ro_id':data['ro_id']})
            if "ro_details" in data['customer']:
                final_invoice.update(data['customer']['ro_details'])
                final_invoice['booking_no'] = final_invoice['ro_id']
                if "branch_name" in final_invoice:
                    del final_invoice['branch_name']
                if "ro_date" in final_invoice:
                    del final_invoice['ro_date']
                if "ro_timeband_clip_list" in final_invoice:
                    del final_invoice['ro_timeband_clip_list']
                if "bill_type" in data['customer']['ro_details']:
                    bill_to = data['customer']['ro_details']['bill_to']
                    if bill_to and bill_to == "client":
                        final_invoice["customer_gst_status"] =  data['customer']['gst_status']
                        if final_invoice["customer_gst_status"] == "registered":
                            final_invoice["customer_gst_no"] = data['customer']['gst_no']
                        elif final_invoice["customer_gst_status"] == "unregistered":
                            final_invoice["customer_state_code"] = data['customer']['address']['state']
                        final_invoice["customer_pan_num"] = data["customer"]["pan_num"]
                    elif bill_to and bill_to == "agency":
                        final_invoice["agency_gst_status"] =  data['customer']['agency_gst_status']
                        if final_invoice["agency_gst_status"] == "registered":
                            final_invoice["agency_gst_no"] = data['customer']['agency_gst_no']
                        elif final_invoice["agency_gst_status"] == "unregistered":
                            final_invoice["agency_state_code"] = data['customer']['agency_gst_state']
                        final_invoice["agency_pan_num"] = data["customer"]["agency_pan_num"]
            if "clientcode" in data['customer']:
                final_invoice['clientcode'] = data['customer']['clientcode']
           
            if "agencycode" in data['customer']:
                final_invoice['agencycode'] = data['customer']['agencycode']
                invoice_master_details = db.invoice_master.find_one()
                if "agency_commission" in invoice_master_details:
                    final_invoice['disc_percentage'] = invoice_master_details['agency_commission']
            else:
                final_invoice['agencycode'] = "107625"
                '''order_reciept_no = db.orders.find_one({"ro_id":final_invoice['ro_id']},\
                                           {"receipt_no":1})'''
                if "receipt_no" in order_details:
                    final_invoice['receipt_no'] = order_details['receipt_no']
            if  order_details.get('sales_ex'):
                sales_ex_info = db.users.find_one({'_id':ObjectId(order_details.get('sales_ex'))})
                if sales_ex_info:
                   final_invoice['sales_ex'] = sales_ex_info.get('username','')        
                
        if "clips" in data:
            clips = get_clips_info_from_invoice(data['clips'])
            final_invoice['invoice_details'] = clips
        
        #telecast_list = get_telecast_data(data['invoice_no'])
        #if telecast_list:
        #    final_invoice['telecast_data'] = telecast_list
        print "Before returning final invoice:::",final_invoice
        return final_invoice
    except Exception, ex:
        print "Exception in change_invoice_format:::::::",str(ex)
        
def get_vertical_subvertical_map():
    try:
        return json_friendly(list(db.verticals.find()))
    except Exception, ex:
        print "Exception in get_vertical_sub_vertical_id:::::::",str(ex)

def compare_commercial_code_for_auto_scheduled(timeband,log_data,is_timeband_list=False):
   matched_tb = None
   try:
       if not (timeband or log_data):
           print "COMPARE COMMERCIAL CODE:::No timeband \
             or log details hence returning"
           return False
       if not is_timeband_list:#Single timeband matched
           print "COMPARE COMMERCIAL CODE::::::Timeband not a list"
           tb_advt_details = timeband[timeband.get("type")]
           ad_type_query = {}
           ad_type_query["status"] = "active"
           ad_type_query["ad_type_identity"] = re.compile(timeband.get('type'),re.IGNORECASE)
           ad_type = db.ad_types.find_one(ad_type_query)
           if not ad_type.get("time_consumable",False):
               print "COMPARE COMMERCIAL CODE:::::: Advt type is Time not cosumable"
               return
           if not tb_advt_details:
              print "COMPARE COMMERCIAL CODE::::::\
               No advertisment type details"
              return
           clip_caption = tb_advt_details.get("caption",None)
           print "COMPARE COMMERCIAL CODE::::::clip caption",clip_caption
           if not clip_caption:
              print "COMPARE COMMERCIAL CODE::::::No clip caption"
           caption_split_list = clip_caption.split("_")
           log_data_caption_split_list = log_data.get("commercial_id").split("_")
           print "COMPARE COMMERCIAL CODE::::::Caption split list and log data \
             caption split list",caption_split_list,log_data_caption_split_list
           if caption_split_list and log_data_caption_split_list:
               if caption_split_list[1].lower() == log_data_caption_split_list[1].lower():
                   #print "COMPARE COMMERCIAL CODE:::::::: Commercial code matched"
                   log_data["advt_type"] = timeband.get('type')
                   status = check_valid_timeband_spots(timeband,log_data)
                   if status:
                       print "COMPARE COMMERCIAL CODE:::Valid timeband spots hence returning true"
                       return True
                   else:
                       return False
               else:
                   return False    


   except Exception,ex:
       print "Exception in compare_commercial_code_for_auto_scheduled",ex


'''def get_program_start_end_time(program_id, program_generated_from):
    try:
        if program_generated_from == "master" :
            program = db.master_programs.find_one({"_id": ObjectId(program_id)})
        else :
            program = db.special_programs.find_one({"_id":ObjectId(program_id)})
        program_start_time = program["start_time"]
        program_end_time = get_end_time(program_start_time,program["duration"])
        print "prgm start and edn",program_start_time,program_end_time
        return (program_start_time,program_end_time)
    except Exception, ex :
        print "Exception in get_program_start_end_time : reson :%s"%str(ex)'''


def get_clip_details_program_wise_scheduled(log_data,timeband,tb_details=False):
   try:
     print "Inside Get clip details program wise scheduled function::::"
     clip_details = None
     prgm_details = None
     valid_tb = False
     prgm_start_time = None
     prgm_end_time = None
     clip_details = None
     program_gen_from = timeband.get("program_gen_from")
     program_id = timeband.get("program_id")
     if not program_id:
         return (None,None)
     if program_gen_from == "master":
         prgm_details = db.programs.find_one({"master_prg_id":str(program_id)})
     elif program_gen_from == "special":
         prgm_details = db.programs.find_one({"special_prg_id":str(program_id)})
     print "GET CLIP DETAILS PROGRAM WISE SCHEDULED ::Prgram details found",prgm_details
     if not prgm_details:
        return (None,None)
     log_data["program_name"] = prgm_details.get("program_name")
     start_time,end_time = get_program_start_end_time(program_id,program_gen_from)
     prgm_start_time = get_time_with_two_digit(start_time)
     prgm_end_time = get_time_with_two_digit(end_time)
     timeband["start_time"] = prgm_start_time
     timeband["end_time"] = end_time
     clip_details = timeband[timeband.get("type")]
     if tb_details:
         print "GET CLIP DETAILS PROGRAM WISE SCHEDULED:: Tb details was true"
         if log_data.get("tb_id") == timeband.get("tb_id"):
             clip_details["tb_id"] = timeband.get("tb_id")
             return clip_details
     else:
         print "GET CLIP DETAILS PROGRAM WISE SCHEDULED:: Returning program start and end time"
         return (prgm_start_time,prgm_end_time)
             
   except Exception, ex:
     print "Exception in get_clip_details_program_wise_scheduled::::::",str(ex)

def get_clip_details_timeband_wise_scheduled(log_data,timeband):
   try:
     clip_details = None
     advt_type_details = None
     advt_type_details = timeband[timeband.get('type')]
     print "GET CLIP DETAILS TIMEBAND WISE::::::Entered Function to check"
     if log_data["tb_id"] == timeband.get("tb_id"):
         print "GET CLIP DETAILS TIMEBAND WISE::: Matched tb id of log and timeband:: both matched"
         advt_type_details["tb_id"] = timeband.get("tb_id")
         return advt_type_details
     else:
         return None
   except Exception, ex:
     print "Exception in  get_clip_details_timeband_wise_scheduled:::",str(ex)



def check_valid_timeband_spots(timeband,log):
    try:
        #print "CHECK VALID TIMEBAND SPOTS:::Inside check valid timeband spots:::"
        if (not timeband) or (not log):
           #print "CHECK VALID TIMEBAND SPOTS:: Returning false since no timeband or log"
           return False
        advt_type = timeband.get("type")
        if not advt_type:
            #print "CHECK VALID TIMEBAND SPOTS:: Returning false since no advt type"
            logging.error("Type key not found while get rate from ro")
            return False
        advt_type_details = timeband[advt_type]
        if not advt_type_details:
            #print "CHECK VALID TIMEBAND SPOTS:: Returning false since no advt type details in db"
            return False
            logging.error("Advt type details not found")
        #print "advt types::::::::::;",advt_type,log.get("advt_type",'')
        if not ((log.get("advt_type",'').lower() == advt_type.lower()) or\
          (log.get("advt_type_name",'').lower() == advt_type.lower())):
           #print "CHECK VALID TIMEBAND SPOTS:: Returning false since advt type name didnt match"
           return False
        date_ranges = advt_type_details.get("date_ranges",[])
        if not date_ranges:
            #print "CHECK VALID TIMEBAND SPOTS:: Returning false since no valid date ragnes in tb"
            logging.info("Date ranges is empty in this orderid %s" %(log.get("order_id", "")))
            return False
        log_date = log.get("date")
        if not log_date:
           #print "CHECK VALID TIMEBAND SPOTS:: Returning false since no date in log"
           return
        valid_dt_range = False
        if date_ranges:
            for each_dt_range in date_ranges:
                valid_date = compare_datetime(each_dt_range["from"], "<=", log_date, "date", display_format="%Y/%m/%d")\
                        and  compare_datetime(each_dt_range["to"], ">=", log_date, "date", display_format="%Y/%m/%d")
                if valid_date:
                    #print "CHECK VALID TIMEBAND SPOTS:: Given date range in valid"
                    num_of_spots = each_dt_range.get("num_spots",0)
                    if num_of_spots >= 0:
                       valid_dt_range = True
                       if advt_type_details.get('user_media_caption'):
                          log['brand'] = advt_type_details.get('user_media_caption')
                    else:
                        continue
            if valid_dt_range:
                #print "CHECK VALID TIMEBAND SPOTS::Valid date range hence retuning true"
                log['rate'] = timeband.get('rate')
                log['spot_type'] = timeband.get('spot_type')
                return True
            else:
                #print "CHECK VALID TIMEBAND SPOTS::Not a valid date range hence returning false"
                return False
    except Exception,ex:
        print "check valid timeband spots",ex

def check_program_wise(timeband,log):
    try:
        program_gen_from = timeband.get("program_gen_from")
        program_id = timeband.get("program_id")
        if not program_id:
            print "No Program id"
            return (False,None)
        if program_gen_from == "master":
            prgm_details = db.programs.find_one({"master_prg_id":str(program_id)})
        elif program_gen_from == "special":
            prgm_details = db.special_program.find_one({"special_prg_id":str(program_id)})
        start_time = prgm_details.get("start_time")
        end_time = get_end_time(start_time,prgm_details["duration"]) 
        prgm_start_time = get_time_with_two_digit(start_time)
        prgm_end_time = get_time_with_two_digit(end_time)          
        timeband_advt_type = timeband[timeband["type"]]
        if log.get("tb_id") == timeband.get("tb_id"):
            return(True,timeband)
        elif compare_datetime(log.get("real_start_time"), \
                '>=',timeband["start_time"], 'time') and\
                compare_datetime(log.get("real_start_time"), \
                '<=',timeband["end_time"], 'time')\
                and timeband['type'] == log.get('advt_type'):
            print "CHECK TB ID RO DP :: checking RODP logic time and type ok"
            timeband_advt_type = timeband[timeband["type"]]
            if 'time_consumable' in ad_type and ad_type['time_consumable'] and \
                log.get("comm_id",None) == timeband_advt_type.get("clip_id",None):
                #print "CHECK TB ID RO DP::::checking RODP logic commercial id is matched"
                status = check_valid_timeband_spots(timeband,log)
                print "CHECK TB ID RO DP:::status after checking proper date range%s"%(status)
                if status:
                    return(True,timeband)
                else:
                   return(False,None)   
            else:
               return(False,None)
    except Exception,ex:
        print "Exception in check_program_wise",ex 

def check_tb_id_ro_dp(order_tb_list,log,ad_type):
    tb_matched = False
    matched_timeband = None
    tb_spots_status = False
    try:
        #print "CHECK TB ID RO DP:::: Inside check tb id ro dp function"
        for timeband in order_tb_list:
            if "program_wise" in timeband and timeband["program_wise"]:
                (timeband_or_prgm_start_time,timeband_or_prgm_end_time) = \
                        get_clip_details_program_wise_scheduled(log,timeband)
                if not (timeband_or_prgm_start_time or timeband_or_prgm_end_time):
                    return False
                timeband["start_time"] = timeband_or_prgm_start_time
                timeband["end_time"] = timeband_or_prgm_end_time
                log["program_wise"] = True
                '''print "CHECK TB ID RO DP:::: It was Program wise and Hence slected \
                  prgm start and end:::::",timeband_or_prgm_start_time,timeband_or_prgm_end_time'''
                #print "Log after setting everything",log

            if "tb_id" in log and log["tb_id"]:
                #print "CHECK TB ID RO DP:::::::Log tb id and timeband tb id::",log["tb_id"],timeband["tb_id"]
                if log["tb_id"] == timeband["tb_id"]:
                    log["tb_caption"] = timeband["tb_caption"]
                    #print "CHECK TB ID RO DP::: Timeband id is equal and matched" 
                    status = check_valid_timeband_spots(timeband,log)
                    #print "CHECK TB ID RO DP::: Status after check valid date range %s"%(status)
                    if status:
                        matched_timeband = timeband
                        tb_matched = True       
                        break
                    else:
                       continue
                else:
                    continue
        if not tb_matched:
            '''print "CHECK TB ID RO DP::: None of the timeband matched with tb id logic \
                   Hence coming to check dp start and dp en time",log'''
            tb_matched = False 
            for timeband in order_tb_list:
                if "program_wise" in timeband and timeband["program_wise"]:
                    (timeband_or_prgm_start_time,timeband_or_prgm_end_time) = \
                        get_clip_details_program_wise_scheduled(log,timeband)
                    if not (timeband_or_prgm_start_time or timeband_or_prgm_end_time):
                       return False
                    timeband["start_time"] = timeband_or_prgm_start_time
                    timeband["end_time"] = timeband_or_prgm_end_time
                    log["program_wise"] = True
                    '''print "CHECK TB ID RO DP:::: It was Program wise and Hence slected \
                  prgm start and end:::::",timeband_or_prgm_start_time,timeband_or_prgm_end_time'''
                else:
                   timeband_or_prgm_start_time = timeband["start_time"]
                   timeband_or_prgm_end_time = timeband["end_time"]

                if compare_datetime(log.get("dp_start_time"), \
                     '==',timeband_or_prgm_start_time, 'time') and\
                     compare_datetime(log.get("dp_end_time"), \
                     '==',timeband_or_prgm_end_time, 'time')\
                     and timeband['type'] == log.get('advt_type'):
                    #print "CHECK TB ID RO DP :: checking RODP logic it is matching DP STRT ND END"  
                   
                    timeband_advt_type = timeband[timeband["type"]]   
                    if 'time_consumable' in ad_type and ad_type['time_consumable'] and \
                           log.get("comm_id",None) == timeband_advt_type.get("clip_id",None):
                        #print "CHECK TB ID RO DP::::checking RODP logic commercial id is matched"
                        status = check_valid_timeband_spots(timeband,log) 
                        #print "CHECK TB ID RO DP:::status after checking proper date range%s"%(status) 
                        if status:
                            matched_timeband = timeband
                            log["tb_caption"] = timeband.get("tb_caption")
                            tb_matched = True       
                            break
                        else:
                            continue
                    else:
                        continue
        return(tb_matched,matched_timeband)   
    except Exception,ex:
       print "Exception in check_tb_id_ro_dp",ex

def match_timeband_with_commercial_id(log_data,timeband):
    try:
        if not (log_data or timeband):
            return
        #print "Inside Function match timeband with commercial id::::to check RODP"
        if "program_wise" in timeband and timeband["program_wise"]:
             #print "MATCH TIMEBAND WITH COMM ID::: It was program wise hence taking prgm start and end time"
             (timeband_or_prgm_start_time,timeband_or_prgm_end_time) = \
             get_clip_details_program_wise_scheduled(log,timeband)
             if not (timeband_or_prgm_start_time or timeband_or_prgm_end_time):
                 return False
             timeband["start_time"] = timeband_or_prgm_start_time
             timeband["end_time"] = timeband_or_prgm_end_time
        else:
            timeband_or_prgm_start_time = timeband["start_time"]
            timeband_or_prgm_end_time = timeband["end_time"]

        if compare_datetime(log_data.get("real_start_time"), \
            '>=',timeband_or_prgm_start_time, 'time') and\
            compare_datetime(log_data.get("real_start_time"), \
            '<=',timeband_or_prgm_end_time, 'time'):
            #print "MATCH TIMEBAND WITH COMMERCIAL ID CODE:::::real start time comes in BTWN RODP"
            status = compare_commercial_code_for_auto_scheduled(timeband,log_data,False)
            if status:
               return True
    except Exception,ex:
        print "Exception in match_timeband_with_commercial_id",ex

       
       
def get_rate_from_ro(log, ad_type):
    condition = False
    final_tb_details = None
    try:
        #print "GET RATE FROM RO::::Entered Function:::::::::::"
        order_details = None
        if log.get('order_id'):
           order_details = db.orders.find_one({"_id":ObjectId(str(log.get('order_id')))})
        ordered_count = log.get("ordered_spots")
        if order_details:
            #print "GET RATE FROM RO::::Order details found"
            timebands_list = order_details.get("timebands")
            (status,tb_details) = check_tb_id_ro_dp(timebands_list,log,ad_type)
            if status and tb_details: 
                #print "GET RATE FROM RO :::::::;status and tb details after check tb id ro dp",tb_details
                final_tb_details = tb_details
            else:
                '''print "GET RATE FROM RO::::: Nor tb id and dp start nd end matched in latest.. \
                          Hence going to archive to find"'''
                archive_order_tb = get_matching_timeband_from_orders_archive(order_details,log)
                if archive_order_tb:
                   #print "GET RATE FROM RO:: Matched a timeband with archived tb hence taking Latest id now"
                   order_query = [{"$match":{"_id":ObjectId(log.get("order_id"))}},{"$unwind":"$timebands"},\
                    {"$match":{"timebands.tb_id":archive_order_tb.get("tb_id")}}]
                   result = db.orders.aggregate(order_query).get("result")
                   final_tb_details = result[0].get("timebands")
                      
        if not final_tb_details:
           #print "GET RATE FROM RO::::::No final tb details hence returning log data oly"
           return (log.get('rate'),log.get('duration'),log.get('spot_type'),False)
        else:        
           timeband_advt_type = final_tb_details[final_tb_details.get("type")]
 
           program_wise_flag = final_tb_details.get("program_wise",False)
           clip_dur = timeband_advt_type.get("duration",0)
           if "rate" in final_tb_details:
               if "rate" in log and log['rate'] == 0 and log["spot_type"] == "bonus":
                   '''print "GET RATE FROM RO::: Log has rate 0 and bonus%s %s \
                   %s"%(0,clip_dur,final_tb_details['spot_type'])'''
                   return (final_tb_details['rate'],clip_dur,final_tb_details['spot_type'],program_wise_flag)
               '''print "GET RATE FROM RO:::::Normal return of rate %s %s %s"\
                 %(float(final_tb_details['rate']),clip_dur,final_tb_details['spot_type'])'''
               return (float(final_tb_details['rate']),clip_dur,final_tb_details['spot_type'],program_wise_flag)
           else:
               '''print "GET RATE FROM RO::: No rate key hence returning 0::\
                 %s %s %s"%(0,clip_dur,final_tb_details['spot_type'])'''
               return (0,clip_dur,final_tb_details['spot_type'],program_wise_flag)             
    except Exception, ex:
        print "Exception in get_rate_from_ro::::::",str(ex)       
       
                

        
def get_matching_timeband_from_orders_archive(order_details,log_data):
    errors = []
    matched_timeband = None
    matched_archived_order = None
    timeband_matched = False
    try:
        print "Inside Get matching Timeband from orders archive collection"
        logging.info("Inside Get matching Timeband from orders archive collection")
        if not order_details and log_data:
            print "No order details and log data"
            logging.errors("No order details and log data")
            return
        db_orders_archive = db.orders_archive.find({"ro_id":order_details.get("ro_id"),\
                "channel_id":order_details.get("channel_id")}).sort("_id",-1)
        if db_orders_archive:
            for every_archvied_order in db_orders_archive:
                print "GET MATCHING ORDER ARCHIVE::: Version number::",every_archvied_order.get("version")
                matched_archived_order = every_archvied_order
                timebands_list = every_archvied_order.get("timebands")
                for timeband in timebands_list:
                    print "GET MATCHING ORDER ARCHIVE:::Going to fetch timeband"
                    if not("program_wise" in timeband and timeband["program_wise"]):
                       clip_details = get_clip_details_timeband_wise_scheduled(log_data,timeband)
                       if clip_details:
                           print "GET MATCHING ORDER ARCHIVE::::: Clip details timeband wise matched"
                           matched_timeband = timeband
                           timeband_matched = True
                           break
                       else:
                           continue
                    else:
                        print "GET MATCHING ORDER ARCHIVE::::: It was program wise"
                        log_data["program_wise"] = timeband.get("program_wise",False)
                        clip_details = get_clip_details_program_wise_scheduled(log_data,timeband,True)
                        if clip_details:
                            print "GET MATCHING ORDER ARCHIVE::::: Clip details program wise matched"
                            matched_timeband = timeband
                            timeband_matched = True
                            break
                        else:
                           continue
                if timeband_matched:
                    print "GET MATCHING ORDER ARCHIVE::: Timeband matched Hence returning matched one"
                    return matched_timeband 
                else:
                    print "GET MATCHING ORDER ARCHIVE::: None of the timeband matched with TB ID logic"
                    for timeband in timebands_list:
                        status = match_timeband_with_commercial_id(log_data,timeband)
                        if status:
                           print "GET MATCHING ORDER ARCHIVE:::::: Matched timeband with commercia id code",timeband
                           matched_timeband = timeband
                           timeband_matched = True
                           break
                        else:
                           continue
    except Exception, ex:
        print " Exception in get_matching_timeband_from_orders_archive ", ex
        logging.exception("Exception in get_matching_timeband_from_orders_archive: "+str(ex))
        
def get_agency_type(ro_id):
    agency_type = ''
   
    order_details = db.orders.find_one({'_id':ObjectId(str(ro_id))})
   
    if order_details and 'agency_id' in order_details and order_details['agency_id']:
        
        agency_info = db.agencies.find_one({'_id':ObjectId(str(order_details['agency_id']))})
        if agency_info:
           agency_type = agency_info.get('agency_type') 
    elif order_details and 'agency_id' not in order_details:
         agency_type = 'Direct'
       
    return agency_type            
       
def change_sales_to_inhouse_format(sales_data):
    try:
        data = {}
        data['username'] = sales_data['username']
        data['first_name'] = sales_data['username']
        data['sales_empid'] = str(int(sales_data['emp_id']))
        data['logging'] = 0
        data['status'] = sales_data['status']
        data['privileges'] = "Sales"
        data['assigned_channel'] = "vml"
        data['channel_id'] = "vml" 
        if 'email' in sales_data and sales_data['email']:
            data['email'] = sales_data['email']
        if "contact_num" in sales_data and sales_data['contact_num']:
            data['contact_num'] = sales_data['contact_num']
        return data
    except Exception, ex:
        print "Exception in change_agency_to_inhouse_format",str(ex)  



def get_rate_from_ro_cg(each_log):
    try:
        if not "order_id" in each_log:
            return
        log_date = each_log.get("date")
        order = db.orders.find_one({"_id":ObjectId(str(each_log['order_id']))})
        if not order:
           return
        timebands_list = order.get("timebands")
        for timeband in timebands_list:
           if not("program_wise" in timeband and timeband["program_wise"]):
              if compare_datetime(each_log.get("dp_start_time"), \
                       '==',timeband["start_time"], 'time') and\
                       compare_datetime(each_log.get("dp_end_time"), \
                       '==',timeband["end_time"], 'time')\
                       and timeband['type'] == each_log.get('advt_type'):
                 spot_type = timeband.get("spot_type")
                 timeband_advt_type = timeband[timeband["type"]]
                 date_ranges = timeband_advt_type.get("date_ranges")
                 status = check_valid_timeband_spots(timeband,each_log)
                 if "cg_id" in timeband_advt_type:
                    ro_clip_id_append = timeband_advt_type.get("cg_id").lower() + "_" + timeband_advt_type.get("caption").lower()
                    if each_log.get("commercial_id").lower() == ro_clip_id_append:
                       clip_dur = timeband_advt_type.get("duration")
                       if "rate" in timeband:
                          rate = (float(timeband['rate']))
                       else:
                          rate = 0
                       if not status:
                          rate = 0
                          spot_type = "bonus"
                          each_log["info"] = each_log.get("info",'')  + "Spots Does not exists for this day"
                       else:
                          for each_dt_range in date_ranges:
                               valid_date = compare_datetime(each_dt_range["from"], "<=", \
                                     log_date, "date", display_format="%Y/%m/%d")\
                                     and  compare_datetime(each_dt_range["to"], ">=", \
                                     log_date, "date", display_format="%Y/%m/%d")
                               if valid_date:
                                  each_log["ordered_spots"] = each_dt_range.get("num_spots",0)
                               else:
                                  continue
                       each_log["rate"] = rate
                       each_log["spot_type"] = spot_type
 
                       return each_log
              else:
                 spot_type = timeband.get("spot_type")
                 timeband_advt_type = timeband[timeband["type"]]
                 status = check_valid_timeband_spots(timeband,each_log)
                 if "cg_id" in timeband_advt_type:
                    ro_clip_id_append = timeband_advt_type.get("cg_id").lower() + "_" + timeband_advt_type.get("caption").lower()
                    if each_log.get("commercial_id").lower() == ro_clip_id_append:
                       clip_dur = timeband_advt_type.get("duration")
                       if "rate" in timeband:
                          rate = (float(timeband['rate']))
                       else:
                          rate = 0
                       if not status:
                          rate = 0
                          spot_type = "bonus"
                          each_log["info"] = each_log.get("info","")  + "Spots Does not exists for this day"
                       else:
                           for each_dt_range in date_ranges:
                               valid_date = compare_datetime(each_dt_range["from"], "<=", \
                                     log_date, "date", display_format="%Y/%m/%d")\
                                     and  compare_datetime(each_dt_range["to"], ">=", \
                                     log_date, "date", display_format="%Y/%m/%d")
                               if valid_date:
                                  each_log["ordered_spots"] = each_dt_range.get("num_spots",0)
                               else:
                                  continue

                       each_log["rate"] = rate
                       each_log["spot_type"] = spot_type
                          
                       return each_log
    except Exception,ex:
        print "Exception in get_rate_from_ro_cg",str(ex)


def get_perunit_cg_data(cg_logs):
    final_dict = {}
    cg_volume_list = []
    result_dict = {}
    try:
         logging.info("Function::: get_perunit_cg_volume:::Inside get per unit cg volume")
         for each_log in cg_logs:
             each_log["timeband"] = each_log["dp_start_time"] + "_" + each_log["dp_end_time"]
             obj = {}
             key = each_log['commercial_id'] + "_" + each_log['date'] + "_"  + each_log["spot_type"]\
                   + each_log['dp_start_time'] + "_" + each_log['dp_end_time']
             if key in final_dict and final_dict[key]:
                 obj = final_dict[key]
             get_rate_from_ro_cg(each_log)
             if not obj:
                obj = {'clip_caption':each_log['clip_caption'],\
                       'date':each_log['date'],\
                       'rate':each_log.get("rate"),\
                       'spot_type':each_log.get("spot_type"),\
                       'count':0,\
                       'timeband': each_log['dp_start_time'] + "_" + each_log['dp_end_time'],\
                       "actual_count": each_log.get('ordered_spots',0)}
                final_dict[key] = obj
             obj['count'] = obj['count'] + 1
             if obj['count'] > obj['actual_count']:
                 each_log['info']  = "Played more than ordered for this timeband"
                 #each_log['rate'] = 0
                 each_log['spot_type'] = "bonus"
         return cg_logs
    except Exception, ex:
        print "Exception in get_perday_cg_volume",str(ex)


def get_perday_cg_volume(cg_logs):
    final_dict = {}
    cg_volume_list = []
    result_dict = {}
    try:
         #print "Inside get per day cg volume:::::::::::;;"
         logging.info("Function::: get_perday_cg_volume:::Inside get per day cg volume")
         for each_log in cg_logs:
             obj = {}
             key = each_log['commercial_id'] +"_" +each_log['date']+ "_" +each_log["spot_type"]
             #print "key---------",key
             if key in final_dict and final_dict[key]:
                 #print "inside if final_dict['key']-------------------",final_dict
                 obj = final_dict[key]
                 #print "obj--------------starting",obj
             get_rate_from_ro_cg(each_log)
             #cg_volume_list.append(obj)
             if not obj:
                obj = {'clip_caption':each_log['clip_caption'],\
                       'date':each_log['date'],'rate':each_log['rate'],\
                       'count':0,'spot_type':each_log['spot_type'],\
                       'advt_type':each_log['advt_type'],\
                       "timeband":each_log.get("dp_start_time") + "_" + each_log.get("dp_end_time"),\
                       "package_detail":each_log.get("package_detail"),\
                        "uuid": str(uuid.uuid1())}
                #print "initializing obj---------------------"
                final_dict[key] = obj

             obj['count'] = obj['count'] + 1

         cg_volume_list = final_dict.values()
         #print "cg valume dat::::::::::::::;;",cg_volume_list
         return cg_volume_list
    except Exception, ex:
        print "Exception in get_perday_cg_volume",str(ex)



def get_cg_data(data):
    final_list = []
    per_day_cg_data = []
    per_unit_cg_data = []
    rate = 0
    #per_day_cg_result = []
    try:
        logging.info("Function :: get_cg_data:::Inside Get cg data")
        for each_log in data:
            if "package_detail" in each_log and each_log["package_detail"] == "per_day":
                per_day_cg_data.append(each_log)
            elif "package_detail" in each_log and each_log["package_detail"] == "per_unit":
                per_unit_cg_data.append(each_log)
        per_day_cg_result = get_perday_cg_volume(per_day_cg_data)
        per_unit_cg_result = get_perunit_cg_data(per_unit_cg_data)
        if per_day_cg_result:
            logging.info("Function:: get_cg_data :::::per_day_cg------%s"%(per_day_cg_result))
            final_list.extend(per_day_cg_result)
        if per_unit_cg_result:
            logging.info("Function:: get_cg_data :::::Final result------%s"%(per_unit_cg_result))
            final_list.extend(per_unit_cg_result)
        return final_list
    except Exception, ex:
        print "Exception in get_cg_data::::::%s"%str(ex)    

def get_objects(collection_name, cond = {}, fields = None, sortby = None):
    if not collection_name:
        return
    try:
        return json_friendly(list(db[collection_name].find(cond, fields, sort=sortby)))
    except Exception, ex:
        print "get_objects: exception:", ex

def get_object(collection_name, cond = {}, fields = None):
    if not collection_name:
        return
    try:
        return json_friendly(db[collection_name].find_one(cond, fields))
    except Exception, ex:
        print "get_objects: exception:", ex

def get_dicts_with_common_keys(dict1 = {}, dict2 = {}):
    try:
        dict11 = {}
        dict22 = {}
        common_keys = set(dict1).intersection(dict2)
        for key in common_keys:
            dict11[key] = dict1[key]
            dict22[key] = dict2[key]
    except Exception, ex:
        print "Exception arised while getting common keyed dictionary from two dicts",ex
    return (dict11, dict22)

def getListItem(list_in, index = 0):
    try:
        return list_in[index]
    except Exception, ex:
        #print "Exception in getListItem::::",ex
        pass

def get_dict_match_count(dict_list, dict_in = {}):
    try:
        ## dict_in is one key:value pair
        match_count = 0
        dict_list_copy = copy.deepcopy(dict_list)
        for each_item in dict_list_copy:
            dict_cmp, dict_ref = get_dicts_with_common_keys(each_item, dict_in)
            if dict_cmp and dict_ref and dict_ref == dict_in and dict_cmp == dict_ref:
                match_count += 1
    except Exception as ex:
        print "Exception in get_dict_match_count:::::::",ex
    finally:
        return match_count

def get_timestamp_custom(datetime1, datetime_format = "%Y/%m/%d"):
    try:
        if isinstance(datetime1, datetime.datetime):
            return time.mktime(datetime1.timetuple())
        elif not isValidDatetimeObject(datetime1, datetime_format):
            return
        return time.mktime(time.strptime(datetime1, datetime_format))
    except Exception, ex:
        print "Exception in get_unix_timestamp::::::",ex
        pass

def getTsFromMongoID(mongo_obj_id = None):
    try:
        if not ObjectId.is_valid(mongo_obj_id):
            return
        if isinstance(mongo_obj_id, (str,unicode)):
            mongo_obj_id = ObjectId(str(mongo_obj_id))
            return get_timestamp_custom(mongo_obj_id.generation_time)
        #print "generation_time:::::::",mongo_obj_id, type(mongo_obj_id), mongo_obj_id.generation_time, type(mongo_obj_id.generation_time)
    except Exception, ex:
        print "Exception arised while getting ts from mongo obj id:::::",mongo_obj_id,ex

def rename_dict_key(dict_in, old_key, new_key, inplace = True):
    try:
        dict_out = dict_in
        if not inplace:
            dict_out = copy.deepcopy(dict_in)
        dict_out[new_key] = dict_in[old_key]
        del dict_out[old_key]
        return dict_out
    except Exception, ex:
        return dict_in

def get_db_backup_filename(relative_day = -1):
    try:
        BACKUP_FOLDER_NAME = "TrafficDatabaseDumps"
        BACKUP_DATE_FOLDER = (datetime.date.today() + datetime.timedelta(relative_day)).strftime("%d-%m-%Y")
        DB_BACKUP_LOCAL_DEST_PATH = os.path.join(HOME_PATH, "db_back_up_test")
        tar_file_name = 'QuickEdgeTrafficDB_%s.tar.gz' %BACKUP_DATE_FOLDER
        return os.path.join(DB_BACKUP_LOCAL_DEST_PATH, tar_file_name)
    except Exception as ex:
        print "Exception in get_db_backup_filename:::::::",ex

def unwind_list(dict_in, unwind_key):
    try:
        unwound_list = []
        if not (dict_in and unwind_key) : return []
        elif unwind_key not in dict_in: return []
        elif not dict_in.get(unwind_key):
            del dict_in[unwind_key]
            return unwound_list.append(dict_in)
        unwind_dict_val = dict_in.pop(unwind_key)
        #basic_dict = dict_in
        for each_doc in unwind_dict_val:
            each_doc.update(dict_in)
            unwound_list.append(each_doc)
    except Exception as ex:
        print "Exception arised in unwind_timeband_list::::::",ex
    return unwound_list

def findDiff(d1, d2, path=""):
    difflist = []
    rem = {}
    for k in d1.keys():
        if not d2.has_key(k):
            print path, ":"
            print k + " as key not in d2", "\n"
        else:
            if type(d1[k]) is dict:
                if path == "":
                    path = k
                else:
                    path = path + "->" + k
                findDiff(d1[k],d2[k], path)
            else:
                if d1[k] != d2[k]:
                    print path, ":"
                    print " - ", k," : ", d1[k]
                    print " + ", k," : ", d2[k]

def compare_dictionaries(dict_1, dict_2, dict_1_name, dict_2_name, path=""):
    """Compare two dictionaries recursively to find non mathcing elements

    Args:
        dict_1: dictionary 1
        dict_2: dictionary 2

    Returns:

    """
    err = ''
    key_err = ''
    value_err = ''
    old_path = path
    for k in dict_1.keys():
        path = old_path + "[%s]" % k
        if not dict_2.has_key(k):
            #key_err += "Key %s%s not in %s\n" % (dict_2_name, path, dict_2_name)
            pass
        else:
            if isinstance(dict_1[k], dict) and isinstance(dict_2[k], dict):
                err += compare_dictionaries(dict_1[k],dict_2[k],'d1','d2', path)
            else:
                if dict_1[k] != dict_2[k]:
                    value_err += "Value of %s changed from %s to %s | "\
                        % (path, dict_1[k], dict_2[k])

    for k in dict_2.keys():
        path = old_path + "[%s]" % k
        if not dict_1.has_key(k):
            #key_err += "Key %s%s not in %s\n" % (dict_2_name, path, dict_1_name)
            pass

    return key_err + value_err + err

def get_dict_key_list(d, final_key_list):
    try:
        if not (isinstance(d, dict) and isinstance(final_key_list, list)) : return []
        l = []
        for k,v in d.items():
            if isinstance(v, dict):
                get_dict_key_list(v, final_key_list)
            l.append(k)
        if l : final_key_list.append(l)
        return final_key_list
    except Exception as ex:
        print "Exception arised while getting all keys as a list from a given dictionary:::",ex
    return []


def get_min_max_time_from_sched_file(date, channel_id = "", dir_path = "", date_format = "%d%m%y"):
    try:
        st_time = "00:00:00"
        en_time = "00:00:00"
        if not isValidDatetimeObject(str(date), date_format):
            raise ValueError("Not a valid date format received. Date format expected is ::::{}".format(date_format))
            #return
        if not dir_path:
            if QEA_EXPORT_PATH_LIST:
                if isinstance(QEA_EXPORT_PATH_LIST, list):
                    dir_path = QEA_EXPORT_PATH_LIST[0]
                elif isinstance(QEA_EXPORT_PATH_LIST, str):
                    dir_path = QEA_EXPORT_PATH_LIST
        if not dir_path :
            raise ValueError("No Dir Path Found")
        if not os.path.isdir(dir_path):
            raise ValueError("The Received Path is not a directory")
        elif not os.path.exists(dir_path):
            raise ValueError("The received path doesn't exist")
        time_list = []
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for f_name in files:
                if not f_name.startswith(date) : continue
                splitted_f_name = f_name.split("_", 7)
                if len(splitted_f_name) < 7 : continue
                time_list.append((":".join(splitted_f_name[1 : 4]), ":".join(splitted_f_name[4 : 7])))
        if time_list:
            time_list.sort(key=itemgetter(0))
            st_time = time_list[0][0]
            time_list.sort(key=itemgetter(1), reverse = True)
            en_time = time_list[0][1]
    except Exception as ex:
        print "Exception arised in get_min_max_time_from_sched_file:::::::::::",ex
    return "_".join([st_time,en_time])


def generate_invoice_format_as_per_channel(db_telecast_seq):
    try:
        full_year_as_per_datetime = int(datetime.datetime.now().strftime("%Y")) - 1
        half_year_as_per_datetime = str(datetime.datetime.now().strftime("%y"))
        seq_num_for_uid_val = str(db_telecast_seq.get("seq_id"))
        uid_val_complete = INVOICE_PREFIX + INVOICE_DELIMITER + seq_num_for_uid_val\
                           + INVOICE_DELIMITER + str(full_year_as_per_datetime) + "-" + str(half_year_as_per_datetime)
        if len(uid_val_complete) < MAX_INVOICE_SEQUENCE_LENGTH:
            seq_num_for_uid_val = seq_num_for_uid_val.zfill(MAX_INVOICE_SEQUENCE_LENGTH - len(uid_val_complete) + 1)
            uid_val_complete = INVOICE_PREFIX + INVOICE_DELIMITER + seq_num_for_uid_val\
                           + INVOICE_DELIMITER + str(full_year_as_per_datetime) + "-" + str(half_year_as_per_datetime)
        return uid_val_complete
    except Exception, ex:
        print "Exception in generate_invoice_format_as_per_channel_id: ", ex


def validate_mandatory_api_data(form_data, validate_keys = []):
    print "--- validating form data ---"
    print "Validation data received: ", form_data, "  ", validate_keys
    errors = []
    try:
        for keys in validate_keys:
            if not form_data.get(str(keys)):
                errors.append("{} not received.".format(keys))
        print "errors from validate_post_data: {}".format(errors)
        return errors
    except Exception, ex:
        print "Exception in validate post data: {}".format(str(ex))

