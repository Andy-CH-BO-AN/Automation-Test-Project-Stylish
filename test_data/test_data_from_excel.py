import pandas as pd


def read_data(file_name, sheet_name):
    df = pd.read_excel(file_name, sheet_name=sheet_name, dtype=str)
    df = df.fillna("")
    test_data = []
    for _, row in df.iterrows():
        customer_detail = row.to_dict()
        if "Product" in sheet_name and "chars" not in customer_detail['Title'] and len(customer_detail['Title']) > 0:
            customer_detail['Title'] += "m"
        for i in customer_detail:
            if "chars" in customer_detail[i]:
                nums = int(customer_detail[i].split(" ")[0])
                customer_detail[i] = nums * "m"
        test_data.append(customer_detail)
    return test_data
