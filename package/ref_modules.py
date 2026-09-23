# Import libraries
import pyodbc
import pandas as pd
import os
import datetime
import sys

import package

def interface():
    print('**************************************** Selection Menu Start ****************************************')
    print('***** (A) General *****')
    print('0: Update reference date')
    print('1: ukcci_check_rep_class - to check if all active ISINs are accounted for in representative class table')
    print('2: Run 3 to 16')
    print('3: ukcci_refresh_in_scope_class_view - to refresh list of in-scope classes')
    print('4: ukcci_refresh_rep_class_details - to refresh supplementary details of representative classes')
    print('')
    print('***** (B) Risk and Return *****')
    print('5: ukcci_rar_mth_ret_import - to refresh monthly returns in database with respect to reference date')
    print('6: ukcci_rar_calc - to calculate the INITIAL RaR score')
    print('7: ukcci_rar_preset_adj_data - to prepare data for adjustment of INITIAL RaR score')
    print('8: ukcci_rar_preset_adj_logic - to adjust INITIAL RaR score')
    print('')
    print('***** (C) Performance *****')
    print('9: ukcci_perf_annual_ret_import - to refresh YTD returns in database with respect to reference date')
    print('10: ukcci_cost_assumed_inv_amt_refresh - to refresh assumed investment amount of reference date based on latest ex rate')
    print('11: ukcci_perf_line_graph_refresh - to prepare data for performance line graph')
    print('')
    print('***** (D) Cost and Charges *****')
    print('12: ukcci_cost_oneoff_refresh - to calculate one-off costs')
    print('13: ukcci_cost_ce_cost_refresh - to calculate ongoing costs of closed-ended investments')
    print('14: ukcci_cost_ongoing_refresh - to calculate ongoing costs')
    print('')
    print('***** (E) Post-refresh *****')
    print('15: ukcci_compile_py - to compile data sheet for Python publication module')
    print('16: ukcci_compile_uds - to compile underlying data sheet for the CCI summary, as one of the required output')
    print('17: ukcci_log_latest_ver_refresh - to get an overview as of reference date, useful for EPT templates')
    print('')
    print('**************************************** Selection Menu End ****************************************\n')

    startinput = input('Input number and press Enter to run procedure (one at a time). Leave blank and press Enter twice to exit:')

    if startinput == '':
        print('===================================================================================================================')
        print("***** Exit module. Goodbye Earthling! *****")
        print('===================================================================================================================')
        sys.exit(0)
    else:
        print('===================================================================================================================')
        print("***** Procedure " + startinput + " Starts *****")
        print('===================================================================================================================')

        if startinput == '0':
            refdate_update()
        elif startinput == '1':
            ukcci_check_rep_class(query = "EXEC ukcci_check_rep_class")
        elif startinput == '3':
            sql_exec(query = "EXEC ukcci_refresh_in_scope_class_view ?", params=[package.refdate])
        elif startinput == '4':
            sql_exec(query = "EXEC ukcci_refresh_rep_class_details")
        elif startinput == '5':
            sql_exec(query = "EXEC ukcci_rar_mth_ret_import ?", params=[package.refdate])
        elif startinput == '6':
            sql_exec(query = "EXEC ukcci_rar_calc ?", params=[package.refdate])
        elif startinput == '7':
            sql_exec(query = "EXEC ukcci_rar_preset_adj_data ?", params=[package.refdate])
        elif startinput == '8':
            sql_exec(query = "EXEC ukcci_rar_preset_adj_logic ?", params=[package.refdate])
        elif startinput == '9':
            sql_exec(query = "EXEC ukcci_perf_annual_ret_import ?", params=[package.refdate])
        elif startinput == '10':
            sql_exec(query = "EXEC ukcci_cost_assumed_inv_amt_refresh ?", params=[package.refdate])
        elif startinput == '11':
            sql_exec(query = "EXEC ukcci_perf_line_graph_refresh ?", params=[package.refdate])
        elif startinput == '12':
            sql_exec(query = "EXEC ukcci_cost_oneoff_refresh ?", params=[package.refdate])
        elif startinput == '13':
            sql_exec(query = "EXEC ukcci_cost_ce_cost_refresh ?", params=[package.refdate])
        elif startinput == '14':
            sql_exec(query = "EXEC ukcci_cost_ongoing_refresh ?", params=[package.refdate])
        elif startinput == '15':
            ukcci_compile_py(query = "EXEC ukcci_compile_py ?", params=[package.refdate])
        elif startinput == '16':
            ukcci_compile_uds(query = "EXEC ukcci_compile_uds ?", params=[package.refdate])
        elif startinput == '17':
            ukcci_log_latest_ver_refresh(query = "ukcci_log_latest_ver_refresh ?", params=[package.refdate])
        elif startinput == '2':
            sql_exec(query="EXEC ukcci_refresh_in_scope_class_view ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_refresh_rep_class_details")
            sql_exec(query="EXEC ukcci_rar_mth_ret_import ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_rar_calc ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_rar_preset_adj_data ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_rar_preset_adj_logic ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_perf_annual_ret_import ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_perf_line_graph_refresh ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_cost_assumed_inv_amt_refresh ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_cost_oneoff_refresh ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_cost_ce_cost_refresh ?", params=[package.refdate])
            sql_exec(query="EXEC ukcci_cost_ongoing_refresh ?", params=[package.refdate])
            ukcci_compile_py(query="EXEC ukcci_compile_py ?", params=[package.refdate])
            ukcci_compile_uds(query="EXEC ukcci_compile_uds ?", params=[package.refdate])

        # To recall the selection menu again
        interface()

# Procedure functions
######################################################################################################################
# Update reference date
######################################################################################################################
def refdate_update_decor(func):
    def wrapper(*args, **kwargs):
        print('Current reference date: ' + datetime.datetime.strftime(package.refdate, '%Y-%m-%d'))
        package.refdate = func(*args, **kwargs)
        print('New reference date: ' + datetime.datetime.strftime(package.refdate, '%Y-%m-%d'))
        print('===================================================================================================================')
        print("***** Procedure Ends *****")
        print('===================================================================================================================')
        interface()
    return wrapper

@refdate_update_decor
def refdate_update():
    refdate_input = input('Please input reference date in YYYY-MM-DD format and press Enter: ')
    refdate_input = datetime.datetime.strptime(refdate_input, '%Y-%m-%d')
    refdate_input = package.get_last_day_of_month(refdate_input)
    return refdate_input #To be assigned to "package.refdate" global variable through package.refdate_update_decor


######################################################################################################################
# SQL Decorator
######################################################################################################################
def sql_connect(func):
    def wrapper(*args, **kwargs):
        # Connection parameters
        server = 'devuksvappimo01\IMDR'
        database = 'Sandbox'

        # Connection string for Windows Authentication
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
        connection = pyodbc.connect(connection_string)

        print("***** Connected to SQL database " + server + "\\" + database + " using Windows Authentication *****")

        # Execute stored procedure
        try:
            cursor = connection.cursor()
            result = func(cursor, *args, **kwargs)
            connection.commit()
            # print("***** Python sent instruction for SQL execution *****")
        except pyodbc.Error as e: #Python error
            print(f"Python error: {e}")
            print("")
        finally:
            if connection:
                connection.close()

        print('===================================================================================================================')
        print("***** Procedure Ends *****")
        print('===================================================================================================================')

    return wrapper

######################################################################################################################
# SQL Stored Procedures
######################################################################################################################

### Standard execution
@sql_connect
def sql_exec(cursor, query, params=None):
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)

    while True: #Print SQL messages
        if cursor.messages:
            for sqlstate, msg in cursor.messages:
                print(msg)
        if not cursor.nextset():
            break
    print("")


### Specific execution
@sql_connect
def ukcci_check_rep_class(cursor, query, params=None):
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)

    ret = cursor.fetchall()
    if ret[0][0] == 'No unaccounted ISIN.':
        print('Latest active ISINs (N.B. not as of reference date) are all accounted for in the representative class table.\n')
    else:
        print('These latest active ISINs (N.B. not as of reference date) are not accounted for in the representative class table.')
        columns = [col[0] for col in cursor.description]
        print(columns)
        for row in ret:
            print(row)
        print('\n')


@sql_connect
def ukcci_compile_py(cursor, query, params=None):
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)

    while True: #Print SQL messages and fetch query results
        if cursor.messages:
            for sqlstate, msg in cursor.messages:
                print(msg)

        if cursor.description is not None:
            dict_list = []
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            # print(columns)
            for row in rows:
                # print(row)
                dict_list.append({k:v for k,v in zip(columns, row)})
            df = pd.DataFrame(dict_list)
            df = df.replace(r'\r?\n', ' ', regex=True) #to remove unwanted line breaks in fields
            print('Number of rows in df: ' + str(len(df)))
            fname = package.refdate.strftime('%Y%m') + '_PyDataSheet_' + datetime.datetime.now().strftime('%y%m%d%H%M%S') + '.csv'
            df.to_csv(path_or_buf=str(os.path.join(package.outputfolderpath,fname)),
                      sep='|',
                      index=False,
                      encoding="utf-8",
                      date_format='%Y-%m-%d')
            print('\n')

        if not cursor.nextset():
            break

    return df


@sql_connect
def ukcci_compile_uds(cursor, query, params=None):
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)

    while True: #Print SQL messages and fetch query results
        if cursor.messages:
            for sqlstate, msg in cursor.messages:
                print(msg)

        if cursor.description is not None:
            dict_list = []
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            # print(columns)
            for row in rows:
                # print(row)
                dict_list.append({k:v for k,v in zip(columns, row)})
            df = pd.DataFrame(dict_list)
            df = df.replace(r'\r?\n', ' ', regex=True) #to remove unwanted line breaks in fields
            print('Number of rows in df: ' + str(len(df)))
            fname = package.refdate.strftime('%Y%m') + '_UnderlyingDataSheet_' + datetime.datetime.now().strftime('%y%m%d%H%M%S') + '.csv'
            df.to_csv(path_or_buf=str(os.path.join(package.outputfolderpath,fname)),
                      sep='|',
                      index=False,
                      encoding="utf-8",
                      date_format='%Y-%m-%d')
            print('\n')

        if not cursor.nextset():
            break

    return df


@sql_connect
def ukcci_log_latest_ver_refresh(cursor, query, params=None):
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)

    while True: #Print SQL messages and fetch query results
        if cursor.messages:
            for sqlstate, msg in cursor.messages:
                print(msg)

        if cursor.description is not None:
            dict_list = []
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            # print(columns)
            for row in rows:
                # print(row)
                dict_list.append({k:v for k,v in zip(columns, row)})
            df = pd.DataFrame(dict_list)
            df = df.replace(r'\r?\n', ' ', regex=True) #to remove unwanted line breaks in fields
            print('Number of rows in df: ' + str(len(df)))
            fname = package.refdate.strftime('%Y%m') + '_Overview_' + datetime.datetime.now().strftime('%y%m%d%H%M%S') + '.csv'
            df.to_csv(path_or_buf=str(os.path.join(package.outputfolderpath,fname)),
                      sep='|',
                      index=False,
                      encoding="utf-8",
                      date_format='%Y-%m-%d')
            print('\n')

        if not cursor.nextset():
            break

    return df
######################################################################################################################

