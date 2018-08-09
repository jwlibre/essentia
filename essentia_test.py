import pandas as pd
import numpy as np
import datetime
import random

# PART 1 - Generating random client data

# generates toy data as trades taking place hourly over a single 9-5 working day.
start = datetime.datetime(2018, 8, 8, 9, 0, 0)
end = datetime.datetime(2018,8,8,17,0,0)
interval = datetime.timedelta(1/24)


instruments_types = [["Inst1","Security"], ["Inst2","Security"], ["Inst3","Derivative"], ["Inst4","Derivative"]]
timestamps = []

# generate timestamps
for k in range(0,9):
    timestamps.append(start + k*interval)


trade_references = [["AAAA","BBBB","CCCC"],
              ["DDDD","EEEE","FFFF"],
              ["GGGG","HHHH","IIII"],
              ["JJJJ","KKKK","LLLL"]]
client_references = ["client1","client2","client3","client4"]

# filenames to which the generated data will be assigned
filenames = ["input1.csv","input2.csv","input3.csv","input4.csv"]

for j in range(0,4):
    
    instruments_ = []
    types_ = []
    timestamps_ = []
    prices_ = []
    quantities_ = []
    trade_refs_ = []
    client_refs_ = []
    
    for i in range(0,20):
        print(i)
        
        # generate random numbers to select from the instrument and timestamp lists
        inst_index = random.randrange(0,4)
        time_index = random.randrange(0,9)
        
        # add randomly-chosen elements to the lists
        instruments_.append(instruments_types[inst_index][0])
        types_.append(instruments_types[inst_index][1])
        timestamps_.append(timestamps[time_index])
        
        # generate random prices
        prices_.append(random.randrange(-1000,1000,1)/20) # negative price == purchase, positive price == sale
        quantities_.append(random.randrange(1,11))
        trade_refs_.append(trade_references[j][random.randrange(0,3)])
        client_refs_.append(client_references[j])
        
        
    # save the generated dataset as a pandas dataframe    
    dataset = pd.DataFrame(
            {'Instrument': instruments_,
             'Type': types_,
             'Timestamp': timestamps_,
             'Price': prices_,
             'Quantity': quantities_,
             'Trade_Reference': trade_refs_,
             'Client_Reference': client_refs_
            })
    
    # save to file
    dataset.to_csv(filenames[j],index = False)
    



# PART 2 - Reading in the data and manipulating it

# filenames post-processing
output_filenames = ["output_1.csv","output_2.csv","output_3.csv","output_4.csv"]

for j in range(0,4):
    
    # read in the data
    trades = pd.read_csv(filenames[j])
    
    # create Market Value variable
    trades['Market_Value'] = np.abs(trades['Price']) * trades['Quantity']
    
    # group trades by instrument
    trades_grouped_inst = trades.groupby("Instrument")
    
    # for a given instrument, calculate total market value
    total_market_values = trades_grouped_inst["Market_Value"].sum()
    
    # create empty list to be populated by each instrument's closing price
    closing_prices_ = []
    
    # loop over each instrument's subgroup dataset
    for name, group in trades_grouped_inst:
        
        group = group.sort_values('Timestamp')
        final_row_index = group.index.max()
        closing_prices_.append(group['Price'].loc[final_row_index])

    summary = pd.DataFrame(total_market_values)
    
    # append the closing price as a separate column to the dataset
    summary['Closing_Price'] = closing_prices_

    summary.to_csv(output_filenames[j], index= True)
        
        