# Test
import pandas as pd
import io

data_json = """[{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },
{ "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },
{ "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },
{ "Gender": "Female", "HeightCm": 166, "WeightKg": 62},
{"Gender": "Female", "HeightCm": 150, "WeightKg": 70},
{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]"""

table_csv = """BMI Category,BMI Limit,Health risk
Underweight,18.5,Malnutrition risk
Normal weight,25.0,Low risk
Overweight,30.0,Enhanced risk
Moderately obese,35.0,Medium risk
Severely obese,40.0,High risk
Very severely obese,9999.0,Very high risk"""

tbl = pd.read_csv(  io.StringIO(table_csv ) )
tbl['BMI Limit'] = tbl['BMI Limit'].astype(float)

def bmi_calc( WKg, HCm):
    global tbl
    bmi = WKg / ( ( HCm/100) ** 2 )
    bmi_cat  = None
    bmi_risk = None
    if bmi < tbl['BMI Limit'][0]:
        bmi_cat, bmi_risk = tbl['BMI Category'][0], tbl['Health risk'][1]
    elif bmi < tbl['BMI Limit'][1]:
        bmi_cat, bmi_risk = tbl['BMI Category'][1], tbl['Health risk'][1]
    elif bmi < tbl['BMI Limit'][2]:
        bmi_cat, bmi_risk = tbl['BMI Category'][2], tbl['Health risk'][2]
    elif bmi < tbl['BMI Limit'][3]:
        bmi_cat, bmi_risk = tbl['BMI Category'][3], tbl['Health risk'][3]
    elif bmi < tbl['BMI Limit'][4]:
        bmi_cat, bmi_risk = tbl['BMI Category'][4], tbl['Health risk'][4]
    else:
        bmi_cat, bmi_risk = tbl['BMI Category'][5], tbl['Health risk'][5]
    return ( bmi, bmi_cat, bmi_risk )


df = pd.read_json( data_json, orient='records' )


# Answers to (1) ro (3) ----------------------------------------------
df['BMI'], df['BMI Category'], df['BMI Health Risk'] = zip( *map( bmi_calc, df["WeightKg"], df["HeightCm"] ))
print( df )


# Answers to (2) and (3) ----------------------------------------------
exactly_overweight = sum( df['BMI Category'] == 'Overweight' ) 
print( "Count of people in Overweight Category exactly: ", exactly_overweight)

normal_bmi_idx = tbl.index[ tbl[ 'BMI Category'] == 'Normal weight' ].tolist()[0]
normal_bmi_limit = tbl['BMI Limit'][normal_bmi_idx]
all_overweight = sum( df['BMI'] >= normal_bmi_limit )
print( "Count of all overweight people: ", all_overweight)


# Answers to (4) and (3) ----------------------------------------------
import multiprocessing as mp
from threading import Lock
import bmi      #  please see bmi.py attached
bmi_calc = bmi.BMI()

# assume the million record data is stored in a line-delimited json file name "million_data.json"
# with 1 data record per line.
BATCH_SIZE = 100
DATA_FILE = "million_data.json"

total_exact_count = 0
total_full_count = 0
mutex = Lock()

def run_bmi_counter( df_batch ):
    global total_exact_count, total_full_count, mutex
    ec, fc = bmi_calc.count_overweight(df_batch)
    mutex.acquire()
    total_exact_count += ec
    total_full_count += fc
    mutex.release()


reader =  pd.read_json( DATA_FILE, orient='records', lines=True, chunksize=BATCH_SIZE)
with mp.Pool(10) as p:
    p.map( run_bmi_counter, reader)
#
print( "Total exact overweight count: ", total_exact_count)
print( "Total all overweight count: ", total_full_count)

        
