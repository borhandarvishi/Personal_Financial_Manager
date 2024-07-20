
import pandas as pd
import csv
import jdatetime
from data_entry_translated import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            if csvfile.tell() == 0:  # Check if the file is empty to write the header
                writer.writeheader()
            writer.writerow(new_entry)
        print("تراکنش با موفقیت اضافه شد")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format=CSV.DATE_FORMAT)
        start_date = jdatetime.datetime.strptime(start_date, CSV.DATE_FORMAT).togregorian()
        end_date = jdatetime.datetime.strptime(end_date, CSV.DATE_FORMAT).togregorian()

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("هیچ تراکنشی در بازه زمانی مشخص شده یافت نشد")
        else:
            print(f"تراکنش‌ها از {start_date.strftime(CSV.DATE_FORMAT)} تا {end_date.strftime(CSV.DATE_FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.DATE_FORMAT)}))

            total_income = filtered_df[filtered_df['category'] == "درآمد"]["amount"].sum()
            total_expense = filtered_df[filtered_df['category'] == "هزینه"]["amount"].sum()
            print(f"جمع کل درآمد: {total_income} تومان")
            print(f"جمع کل هزینه: {total_expense} تومان")
            print(f"پس‌انداز خالص: {(total_income - total_expense): .2f} تومان")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("تاریخ تراکنش را وارد کنید (روز-ماه-سال) یا اینتر برای تاریخ امروز: ", allows_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index('date', inplace=True)
    
    income_df = df[df['category'] == 'درآمد'].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df['category'] == 'هزینه'].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="درآمد", color="g")
    plt.plot(expense_df.index, expense_df['amount'], label="هزینه", color="r")
    plt.xlabel("تاریخ")
    plt.ylabel("مقدار")
    plt.title("درآمد و هزینه در طول زمان")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. افزودن تراکنش جدید")
        print("2. مشاهده تراکنش‌ها و خلاصه در یک بازه زمانی")
        print("3. خروج")

        choice = input("---- انتخاب خود را وارد کنید (1-3:) ----> ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("تاریخ شروع را وارد کنید (روز-ماه-سال):")
            end_date = get_date("تاریخ پایان را وارد کنید (روز-ماه-سال):")
            df = CSV.get_transactions(start_date, end_date)
            if input("آیا می‌خواهید نمودار را مشاهده کنید؟ (y/n)").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("خداحافظ...")
            break
        else:
            print("انتخاب نامعتبر. لطفا 1، 2 یا 3 را وارد کنید.")

if __name__ == "__main__":
    main()
