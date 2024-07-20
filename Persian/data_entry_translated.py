
from datetime import datetime
import jdatetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "درآمد", "E": "هزینه"}

def get_date(prompt, allows_default=False):
    date_str = input(prompt)
    if allows_default and not date_str:
        return jdatetime.date.today().strftime(date_format)
    
    try:
        valid_date = jdatetime.datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("فرمت تاریخ نامعتبر است. لطفا تاریخ را به صورت روز-ماه-سال وارد کنید")
        return get_date(prompt, allows_default=False)

def get_amount():
    try:
        amount = float(input("مقدار را وارد کنید: "))
        if amount <= 0:
            raise ValueError("مقدار باید غیر منفی و غیر صفر باشد.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("دسته‌بندی را وارد کنید ('I' برای درآمد یا 'E' برای هزینه): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("دسته‌بندی نامعتبر است. لطفا 'I' برای درآمد یا 'E' برای هزینه وارد کنید")
    return get_category()

def get_description():
    return input("توضیحات را وارد کنید (اختیاری): ")
