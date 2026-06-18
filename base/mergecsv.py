import pandas as pd
from pathlib import Path

def ext_MergeCSV(origem, destino):
    """Merge multiple CSV files into a single Excel workbook.
    
    Args:
        origem (str): Source directory containing CSV files
        destino (str): Output Excel file path
    """
    origem_path = Path(origem)
    csv_list = list(origem_path.glob('*.csv'))

    if not csv_list:
        print("No CSV files found in source directory!")
        return False

    print("Found %d files..." % len(csv_list))

    writer = pd.ExcelWriter(destino)  # Arbitrary output name
    for csv_file in csv_list:
        df = pd.read_csv(str(csv_file), engine='python', delimiter=',').sort_values('DN')
        sname = csv_file.stem
        df.to_excel(writer, sheet_name=sname, index=False)
        
    writer.close()
