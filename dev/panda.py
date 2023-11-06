import pandas as pd
import json

def get_value_names(data, path=''):
    names = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            names += get_value_names(value, f'{path}{key}.')
    elif isinstance(data, list):
        for i, item in enumerate(data):
            names += get_value_names(item, f'{path}{i}.')
    else:
        names.append(path[:-1])
        
    return names
    
if __name__ == '__main__':
    # Load JSON data
    with open('../src/source.json') as f:
        data = json.load(f)
    
    # Initialize dataframe  
    df = pd.DataFrame(data)
    
    # Recursively flatten data
    while True:
        new_columns = {}
        
        for col in df.columns:
            if isinstance(df[col].iloc[0], dict): 
                # If column is a dict, expand
                for k,v in df[col].iloc[0].items():
                    new_columns[col+'_'+k] = df[col].apply(lambda x: x[k] if isinstance(x, dict) else None)
            elif isinstance(df[col].iloc[0], list):
                # If column is a list, expand
                df = pd.concat([df.drop(col, axis=1), df[col].apply(pd.Series)], axis=1)
            else:
                # Otherwise, keep column
                new_columns[col] = df[col]
                
        # Update dataframe with new columns
        df = pd.DataFrame(new_columns)
        
        # Check if dataframe was changed, break if not
        if len(new_columns) == len(df.columns):
            break
        
    # Write flattened data to CSV
    df.to_csv('./result/flattened.csv', index=False)