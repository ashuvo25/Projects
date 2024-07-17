import pandas as pd
import matplotlib
import csv
from datetime import datetime 
import os

class CSV:
    csv_File = os.path.join(os.path.dirname(__file__), "data.csv")
    col = ["date","amount","catagory","description"]
    @classmethod
    def init_csv(file):
        try:
            pd.read_csv(file.csv_File)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["date","amount","catagory","description"])
            df.to_csv(file.csv_File,index = False)
        
        file_path = os.path.abspath(file.csv_File)
        print(f"The CSV file path is: {file_path}")
    @classmethod
    def add_items(file , date , amount , catagory , description):
        new_entry = {
             "date" : date,
             "amount" :amount,
             "catagory" : catagory,
             "description" : description,
        }
        with open(file.csv_File, "a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile , fieldnames=file.col)
            writer.writerow(new_entry)
        print("Successfully added!")

    @classmethod
    def history(file , start_date , end_date):
        df = pd.read_csv(file.csv_File)
        df["date"] = pd.to_datetime(df["date"] ,format="%d-%m-%Y")
        start_date = datetime.strptime(start_date , "%d-%m-%Y")
        end_date = datetime.strptime(end_date , "%d-%m-%Y")
        #useing mask
        between_start_and_end = (df["date"] >= start_date ) & (df["date"] <= end_date)
        filter_df = df.loc[between_start_and_end]

        if filter_df.empty:
            print("No Transection happend")
        else:
            print(f"Transection start {start_date.strftime("%d-%m-%Y")} to {end_date.strftime("%d-%m-%Y")}: ")
            print(filter_df.to_string(index=False , formatters={"date": lambda x : x.strftime("%d-%m-%Y")}))
            total_save = filter_df[filter_df["catagory"] == "Deposit"]["amount"].sum()
            total_cost = filter_df[filter_df["catagory"] == "Cost"]["amount"].sum()
            print("\nShort Details:")
            print(f"Total Deposit : {total_save:.2f}")
            print(f"Total Cost : {total_cost:.2f}")

            print(f"Present Amount : {total_save - total_cost:.2f}")
        return filter_df

# ----------------------- Functionssss --------------


catagorys = {
    "D" : "Deposit" , "C" : "Cost" 
}

def get_time(prompt, default=False):
    user_input = input(prompt)
    if default and not user_input:
        return datetime.today().strftime("%d-%m-%Y")
    try:
        valid_date = datetime.strptime(user_input, "%d-%m-%Y")
        return valid_date.strftime("%d-%m-%Y")
    except ValueError:
        print("Invalid format, dd-mm-yyyy correct format")
        return get_time(prompt, default)

def get_amount():
    try:
        amount = float(input("Enter amount: "))
        if amount < 0 :
            raise ValueError("Less then Zero not accpted")
        return amount
    except ValueError as e :
        print(e)
        return get_amount()
    


def get_catagory():
    cata = input("Enter catagory (< D > for Deposit,< C > for cost)  : ").upper()
    if cata in catagorys:
        return catagorys[cata]
    else:
        print("Invalid catagory")
        return get_catagory()

def get_description():
    return input("Optional:: \nEnter any discription: ")

# ----------------------------------------------------------------------------------------------


def add():
    CSV.init_csv()
    date = get_time("Enter date  (dd-mm-yyyy) or just press enter for today: ", default=True)
    amount = get_amount()
    catag = get_catagory()
    desc = get_description()
    CSV.add_items(date , amount , catag , desc)

# CSV.history("05-07-2002","18-07-2024")
# add()

def main():
    while True:
        print(
          "1.add \n2.History \n3.exit"  
        )
        val = int(input("Enter Option Number: "))
        if val == 1:
            add()
        elif val == 2:
            start_date = get_time("Date Formate (dd-mm-yyyy)")
            end_date = get_time("Date Formate (dd-mm-yyyy)")
            df = CSV.history(start_date,end_date)
        elif val == 3:
            print("Exit ....")
            break
        else:
            print("invalid input")

if __name__ == "__main__":
    main()           

