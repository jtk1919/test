# Answer to (4) ----------------------------------------------
import pandas as pd
import io


class BMI:
    def __init__(self):
        self.table_csv = """BMI Category,BMI Limit,Health risk
Underweight,18.5,Malnutrition risk
Normal weight,25.0,Low risk
Overweight,30.0,Enhanced risk
Moderately obese,35.0,Medium risk
Severely obese,40.0,High risk
Very severely obese,9999.0,Very high risk"""
        self.tbl = pd.read_csv(  io.StringIO(self.table_csv ) )
        self.tbl['BMI Limit'] = self.tbl['BMI Limit'].astype(float)
    #
    def __bmi_calc( self, WKg, HCm):
        bmi = WKg / ( ( HCm/100) ** 2 )
        bmi_cat  = None
        bmi_risk = None
        if bmi < self.tbl['BMI Limit'][0]:
            bmi_cat, bmi_risk = self.tbl['BMI Category'][0], tbl['Health risk'][1]
        elif bmi < tbl['BMI Limit'][1]:
            bmi_cat, bmi_risk = self.tbl['BMI Category'][1], tbl['Health risk'][1]
        elif bmi < tbl['BMI Limit'][2]:
            bmi_cat, bmi_risk = self.tbl['BMI Category'][2], tbl['Health risk'][2]
        elif bmi < tbl['BMI Limit'][3]:
            bmi_cat, bmi_risk = self.tbl['BMI Category'][3], tbl['Health risk'][3]
        elif bmi < tbl['BMI Limit'][4]:
            bmi_cat, bmi_risk = self.tbl['BMI Category'][4], tbl['Health risk'][4]
        else:
            bmi_cat, bmi_risk = self.tbl['BMI Category'][5], tbl['Health risk'][5]
        return ( bmi, bmi_cat, bmi_risk )
    #
    def bmi_calculations( self, bmi_df ):
        assert isinstance( bmi_df, pd.DataFrame ), f'[ERROR] bmi_df must be a Pandas DataFrame.'
        assert 'WeightKg' in bmi_df.columns, f'[ERROR] \"WeightKg\" column missing in bmi_df.'
        assert 'HeightCm' in bmi_df.columns, f'[ERROR] \"HeightCm\" column missing in bmi_df.'
        bmi_df['BMI'], bmi_df['BMI Category'], bmi_df['BMI Health Risk'] = zip( *map( self.__bmi_calc, bmi_df["WeightKg"], bmi_df["HeightCm"] ))
        return bmi_df
    #
    def count_overweight( self, bmi_df ):
        cols = bmi_df.columns
        if (not 'BMI' in cols) or (not 'BMI Category' in cols) or (not 'BMI Health Risk' in cols):
            bmi_df = self.bmi_calculations( bmi_df)
        exactly_overweight = sum( bmi_df['BMI Category'] == 'Overweight' ) 
        #
        normal_bmi_idx = self.tbl.index[ tbl[ 'BMI Category'] == 'Normal weight' ].tolist()[0]
        normal_bmi_limit = self.tbl['BMI Limit'][normal_bmi_idx]
        all_overweight = sum( bmi_df['BMI'] >= normal_bmi_limit )
        return exactly_overweight, all_overweight


if __name__ == "__main__":
    ## run unit tests
    data_json = """[{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },
    { "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },
    { "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },
    { "Gender": "Female", "HeightCm": 166, "WeightKg": 62},
    {"Gender": "Female", "HeightCm": 150, "WeightKg": 70},
    {"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]"""

    df = pd.read_json( data_json, orient='records' )

    bmi_calc = BMI()
    print( bmi_calc.tbl)

    df = bmi_calc.bmi_calculations( df )
    ov_exact, ov_all = bmi_calc.count_overweight( df)
    assert (ov_exact == 1), 'Test failed for exact overweight count == 1'
    print( 'Test passed for exact overweight count == 1')
    assert (ov_all == 4), 'Test failed for all overweight count == 4'
    print( 'Test passed for all overweight count == 4')