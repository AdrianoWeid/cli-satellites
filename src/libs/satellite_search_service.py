import pandas as pd

def get_satellites(satellite_name: str=None, page: int=1, page_size: int=10):
    df = pd.read_excel("../../data/satellite_database.xlsx", usecols=['Current Official Name of Satellite', 'NORAD Number'])
    
    if satellite_name:
        df = df.loc[df['Current Official Name of Satellite'].str.contains(satellite_name, case=False, na=False)]
    
    start = (page - 1) * page_size
    end = start + page_size
    filtered_df = df.iloc[start:end]

    
    return filtered_df




if __name__ == "__main__":
    print(get_satellites("Starlink", 6 , 100))
