#!/usr/bin/python

#from pymongo.errors import BulkWriteError
from utils import *
import csv
import sys
import logging
import os
import shutil
import re
import time
_CHANNEL_ID = "vml"
CSV_FILEPATH = os.path.join(HOME_PATH, "Wasp_log")
CSV_PARAMETERS = ("dummy","start_time","end_time","duration","guid","advt_id","commercial_id")
CSV_DATE_FORMAT = "%Y-%m-%d  %H:%M:%S"
TRAFFIC_DATE_FORMAT = "%Y/%m/%d"
CG_ID_MATCH = True

caption_list = []
temp_data = []
timeband_caption_map = {}
tb_list = []
status = True

def get_date_from_csv_date(date):
    try:
        if not date:
            return
        return datetime.datetime.strptime(date, CSV_DATE_FORMAT).strftime(TRAFFIC_DATE_FORMAT)    
    except Exception, ex:
        #print "Exception in get_date_from_csv_date :::::%s"%str(ex)
        logging.error("Exception in get_date:::::%s"%str(ex))

def get_time_from_csv_time(date):
    try:
       if not date:
          return False
       return datetime.datetime.strptime(date, CSV_DATE_FORMAT).strftime("%H:%M:%S")
    except Exception, ex:
        #print "Exception in get_time_from_csv_date:::::%s"%str(ex)
        logging.error( "Exception in get_time_from_csv_date:::::%s"%str(ex))


def check_clip_caption_matched(cg_clip_caption,ro_clip_caption,ro_cg_id=None):
    try:
        #print "inside check_clip_caption_matched",cg_clip_caption,ro_clip_caption
        logging.info("check_clip_caption_matched:::%s, %s"%(cg_clip_caption,ro_clip_caption))
        if not cg_clip_caption:
            #logging.info("check_clip_caption_matched:: no cg clip caption")
            return False
        if not ro_clip_caption:
            #logging.info("check_clip_caption_matched::: No ro clip caption")	
            return False
        if (ro_clip_caption.lower()).strip() == (cg_clip_caption.lower()).strip():
            #logging.info("check_clip_caption_matched:::::::Matched clip name with normal method")
            return True
        if CG_ID_MATCH:
            ro_clip_caption_split_list = ro_clip_caption.split("_",2)
            if len(ro_clip_caption_split_list) < 2:
                return False
            if cg_clip_caption.startswith("CG"): #or ro_cg_id.startswith("CG"):
                cg_clip_split_list = cg_clip_caption.split("_",2)
                if len(cg_clip_split_list) < 2:
                    return False
                cg_id = "_".join(cg_clip_split_list[:2])
                if "_".join(ro_clip_caption_split_list[:2]) == cg_id:
                    return True
                elif ro_cg_id and ro_cg_id.startswith("CG"):
                    ro_cg_id_split_list  = ro_cg_id.split("_", 2)
                    if len(ro_cg_id_split_list) < 2:
                        return False
                    elif "_".join(ro_cg_id[:2]) == cg_id:
                        return True
        return False
    except Exception,ex:
        print "Exception in check_clip_caption_matched",ex


def get_date_from_date_time(date_time):
    try:
        date_obj = datetime.datetime.strptime(date_time,
            "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%Y/%m/%d")
    except Exception as ex:
        #print "Exception in get_date_from_date_time::::",ex
        pass

def get_cg_data_from_timeband_data(ro_details, cg_data):
    try:
        #print "Each CG Data Input::::::",cg_data
        cg_date = get_date_from_csv_date(cg_data.get("start_time"))
        if not cg_date:
            return
        real_start_time = get_time_from_csv_time(cg_data.get('start_time'))
        if not real_start_time:
            return
        timebands = ro_details.get("timebands")
        if not timebands:
            return
        #timebands.sort(key = itemgetter("rate"), reverse = True)
        for each_tb in timebands:
            advt_type = each_tb.get("type")
            if not advt_type:
                continue
            caption = each_tb[advt_type].get("caption")
            if caption == None:
                continue
            ro_cg_id = each_tb[advt_type].get("cg_id") 
            if ro_cg_id: 
                caption = "_".join([str(ro_cg_id), caption])
            dp_start_time = each_tb.get('start_time')
            dp_end_time = each_tb.get('end_time')
            if not (dp_start_time and dp_end_time):
                continue
            data = copy.deepcopy(cg_data)
            check_clip_matched = check_clip_caption_matched(data["commercial_id"],caption,ro_cg_id)
            if not check_clip_matched:
                continue
            else:
                dt_range = each_tb[advt_type].get("date_ranges", [])
                if not dt_range:
                    continue
                data["real_start_time"] = data["run_time"] = real_start_time
                data["date"] = data["date_time"] = cg_date
                ordered_spots = 0
                for each_dt_range in dt_range:
                    if compare_datetime(
                        data["date"], '>=', each_dt_range['from'], 'date', "%Y/%m/%d") and\
                          compare_datetime( 
                          data["date"], '<=', each_dt_range['to'], 'date', "%Y/%m/%d"):
                        if each_dt_range.get("num_spots"):
                            ordered_spots += int(each_dt_range["num_spots"])
                if not ordered_spots:
                    continue
                data["ordered_spots"] = ordered_spots
                data["device"] = "cg"
                data['clip_caption'] = data['commercial_id']
                data['type'] = 'auto'
                data["customer_id"] = ro_details.get("customer", "")
                data["channel_id"] = ro_details.get("channel_id")
                if not data["channel_id"]:
                    data["channel_id"] = _CHANNEL_ID
                data["order_id"] = str(ro_details["_id"])
                data["advt_type"] = advt_type
                data["dp_start_time"] = each_tb.get("start_time")
                data["dp_end_time"] = each_tb.get("end_time")
                data['clip_caption'] =  data["commercial_id"]
                if each_tb.get('spot_type'):
                    data['spot_type'] = each_tb['spot_type']
                if each_tb.get('rate') != None:
                    data['package_detail'] = each_tb.get('package_detail')
                    if compare_datetime(data.get("real_start_time"), \
                        '>=',data["dp_start_time"], 'time') and \
                        compare_datetime(data.get("real_start_time"),\
                        '<',data["dp_end_time"], 'time'):
                        data['rate'] = each_tb['rate']
                    else:
                        data['rate'] = 0
                        data['spot_type'] = "bonus"
                if "end_time" in data:
                    del data["end_time"] 
                if "start_time" in data:
                    del data["start_time"] 
                if "dummy" in data:
                    del data['dummy']
                return data
    except Exception, ex:
        print "Exception in get_cg_data_from_timeband_data:::::%s"%str(ex)
        logging.error( "Exception in get_cg_data_from_timeband_data:::::%s"%str(ex))

def read_cg_file(filepath):
    try:
        cg_data_list = []
        cg_data = csv.DictReader(open(filepath), CSV_PARAMETERS)
        for each_data in cg_data:
            if not all(each_data.values()):
                logging.info("Line ERROR in CSV File ====> %s"%filepath)
                continue
            cg_data_list.append(each_data)
    except Exception as ex:
        print "Exception arised in read_cg_file::::::",filepath
    finally:
        #print "Returning CG Data List:::::", cg_data_list
        return cg_data_list

def get_all_files(root_dir):
    try:
        complete_file_list = []
        for root,dirs,files in os.walk(CSV_FILEPATH):
            for _dir in dirs:
                if date != _dir:
                    continue
                csv_dir = os.path.join(CSV_FILEPATH,_dir)
                for root1, dirs1, files1 in os.walk(csv_dir):
                    if not files1:
                        logging.error("No csv file found")
                    for csv_file in files1:
                        #logging.info("CG script name is %s"%str(csv_file))
                        path = os.path.join(csv_dir, csv_file)
                        complete_file_list.append(path)
            break
    except Exception, ex:
        print "Exception in get_all_files:::::",ex
        logging.info("Exception in get_all_files:::::%s"%ex)
    finally:
        print "Returning %s number CSV Files from the give Root Path::::%s"%(len(complete_file_list), root_dir)
        logging.info("Returning %s number CSV Files from the give Root Path::::%s"%(len(complete_file_list), root_dir))
        return complete_file_list

if __name__ == "__main__":
    try:
        log_file_path = os.path.join(os.path.join(HOME_PATH, "qet_logs") , 'csv_to_json_%s.log' % str(datetime.date.today()))
        log_format = '%(asctime)s [%(levelname)s] %(message)s'
        logging.basicConfig(format=log_format, filename=log_file_path, level=logging.DEBUG)
        args = []
        args = sys.argv
        if len(sys.argv) > 1:
            date = (datetime.datetime.today() +
                datetime.timedelta(
                    days=int(sys.argv[1]))).strftime('%Y-%02m-%02d')
        if len(sys.argv) > 2:
            _CHANNEL_ID = sys.argv[2]
        print CSV_FILEPATH,  _CHANNEL_ID, date
        all_files = get_all_files(CSV_FILEPATH)
        print "Total Number Of CSV Files found as::::%s"%len(all_files)
        if not all_files:
            logging.info("No Files Got from File Directory::::%s"%CSV_FILEPATH)
            sys.exit(-1)
        logging.info("Total Number Of CSV Files found as::::%s"%len(all_files))
        date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime(TRAFFIC_DATE_FORMAT)
        query = {}
        query['end_date'] = {"$gte": date}
        query['start_date'] = {"$lte": date}
        query['channel_id'] = _CHANNEL_ID
        query['status'] = "active"
        ro_list = json_friendly(list(db.orders.find(query)))
        if not ro_list:
            print "No Release Order Found For this date::::::%s"%date
            logging.info("No Release Order Found For this date::::::%s"%date)
            sys.exit(-1)
        #print "Total Ro Found As::::::",len(ro_list)
        complete_cg_list = []
        for each_cg_file in all_files:
            cg_list = read_cg_file(each_cg_file)
            for each_cg_entry in cg_list:
                for each_ro in ro_list:
                    cg_data = get_cg_data_from_timeband_data(each_ro, each_cg_entry)
                    if not cg_data:
                        logging.info("CG Data ====== %s  ======not matched with existing ROs"%each_cg_entry)
                        continue
                    complete_cg_list.append(cg_data)
                    break
        #print "Toatl Number of CG Entries to be inserted in As Run Log Collection is",len(complete_cg_list)
        if complete_cg_list:
            db.as_run_logs.insert(complete_cg_list)
        logging.info("Total Number of As Run Log Inserted SuccessFully is:::::%s"%len(complete_cg_list))
        sys.exit(0)
    except Exception, ex:
        print "Exception in csv_to_json.py:::::::::%s"%str(ex)
        logging.error("Exception in csv_to_json.py:::::::::%s"%str(ex))
        sys.exit(-1)
