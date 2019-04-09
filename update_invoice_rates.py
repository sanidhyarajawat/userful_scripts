#!/usr/bin/python -u

import sys
sys.path.append("/opt/topspot/web_service/src")
from constants import *
from utils import *
sys.path.append(TRAFFIC_CONFIG_PATH)
import datetime
import pymongo
import os
from bson.objectid import ObjectId
import json
from traffic_config import *

DRY_RUN = False

def get_sys_args():
    if len(sys.argv) != 5:
        print "Complete arguments not received, Run the script as: ./update_invoice_rates <invoice_num> <amount> <gst_type> <agency_commission>"
        sys.exit(0)
    invoice_num = sys.argv[1]
    amount = float(sys.argv[2])
    gst_type = sys.argv[3]
    agency_commission = int(sys.argv[4])
    if gst_type not in ["igst", "cgst", "sgst"]:
        print "Wrong gst_type is given. Please choose from the following: ['igst', 'cgst', 'sgst']"
    return invoice_num, amount, gst_type, agency_commission

def calculate_new_amount_and_update(invoice_num,amount,gst_type,agency_commission):
    tax_update_dict = {}
    gst_percent_dict = {}
    igst = 0
    csgt = 0
    sgst = 0
    tgst = 0
    db_invoice = db.invoice.find_one({"invoice_num": str(invoice_num)})
    tax_and_final_cost_dict = db_invoice.get("tax_and_final_cost")

    gross_amount = float(amount)
    if agency_commission != 0:
        net_taxable_amount = float(gross_amount - agency_commission)
        agency_discount = float(agency_commission)
    else:
        net_taxable_amount = float(gross_amount)
        agency_discount = 0.00
    tax_type = "gst"
    consolidated_gst = False
    if gst_type == "igst":
        igst = (net_taxable_amount*18)/100
        final_cost = net_taxable_amount + igst
        tgst = igst
        sgst = 0.00
        cgst = 0.00
        gst_percent_dict["igst"] = "@ 18%"
        gst_percent_dict["cgst"] = ""
        gst_percent_dict["sgst"] = ""
    else:
        igst = 0.00
        cgst = float((net_taxable_amount*(18/2)/100))
        sgst = float((net_taxable_amount*(18/2)/100))
        tgst = cgst + sgst
        final_cost = net_taxable_amount + cgst + sgst
        gst_percent_dict["igst"] = ""
        gst_percent_dict["cgst"] = "@ 9%"
        gst_percent_dict["sgst"] = "@ 9%"

    round_off = (final_cost - round(final_cost)) * -1
    final_cost = round(final_cost)

    tax_update_dict["gross_amount"] = str("{0:.2f}".format(gross_amount))
    tax_update_dict["final_cost"] = int(final_cost)
    tax_update_dict["net_taxable_amount"] = str("{0:.2f}".format(net_taxable_amount))
    tax_update_dict["agency_discount"] = str("{0:.2f}".format(agency_discount))
    tax_update_dict["round_off"] = str("{0:.2f}".format(round(round_off,2)))
    tax_update_dict["igst"] = str("{0:.2f}".format(igst))
    tax_update_dict["cgst"] = str("{0:.2f}".format(cgst))
    tax_update_dict["sgst"] = str("{0:.2f}".format(sgst))
    tax_update_dict["tgst"] = str("{0:.2f}".format(tgst))
    tax_update_dict["tax_type"] = tax_type
    tax_update_dict["consolidated_gst"] = consolidated_gst
    tax_update_dict["gst_percent"] = gst_percent_dict
    if DRY_RUN:
        print tax_update_dict
    else:
        db.invoice.update({"invoice_num": str(invoice_num)}, {"$set": {"tax_and_final_cost": tax_update_dict}})


if __name__ == '__main__':
    invoice_num, amount, gst_type, agency_commission = get_sys_args()
    calculate_new_amount_and_update(invoice_num,amount,gst_type,agency_commission)
