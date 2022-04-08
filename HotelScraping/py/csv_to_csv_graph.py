import pandas as pd

import commonFunctions as cf

# Add headers to csv
# Reorder the date like YYYY-MM-DD

def create_csvgraph_from_csv(path, column_ref_name, column_value_name):
    df = pd.read_csv(path, sep=";")
    column_ref = df[column_ref_name]
    column_value = df[column_value_name]
    return create_array_refs_sums(column_ref, column_value)


def create_array_refs_sums(references_list, values):
    sum = 0
    number_element = 0
    mean_list = []
    last_reference = references_list[0]
    for reference, value in zip(references_list, values):
        if reference == last_reference:
            sum += float(value.replace(",", "."))
            number_element += 1
        else:
            mean_list.append((last_reference, sum / number_element))
            sum = 0
            number_element = 0
        last_reference = reference
    return mean_list


def create_csv(path, list, column_name1, column_name2):
    f = open(path, "w")
    f.write("{};{}\n".format(column_name1, column_name2))
    for line in list:
        date = cf.date_format_MMDDYYYY_to_YYYYMMDD(line[0])
        print(date)
        f.write("{};{}\n".format(date, line[1]))
    f.close()


if __name__ == '__main__':
    booking_list = create_csvgraph_from_csv("../csv/csv_par_site/booking_general.csv", "start_date", "prices")
    create_csv("../csv/csv_graphs/booking_csv_graph.csv", booking_list, "Date", "Price")
