import pathlib
import pandas as pd


def concatenate_monthly_data(pivot_month: str = "2018-11") -> pd.DataFrame:
    """
    method to concatenate one-month amount data into single dataframe
    """
    files = [str(path) for path in pathlib.Path("data").glob(f"{pivot_month}-*.csv")]
    concatenated_data = []
    for file in files:
        concatenated_data.extend(pd.read_csv(file).to_dict("records"))
    return pd.DataFrame(concatenated_data)


def save_concatenated_data(monthly_data: pd.DataFrame, file_name: str = "events.csv") -> None:
    """
    method to save concatednated monthly data
    """
    monthly_data.to_csv(f"data/{file_name}", index=False)
    
    
def main():
    """
    main routine to execute preprocessing logic
    """
    monthly_data = concatenate_monthly_data()
    save_concatenated_data(monthly_data)
    

if __name__ == "__main__":
    main()