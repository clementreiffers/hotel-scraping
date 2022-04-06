from itertools import product
from multiprocessing.dummy import Pool as ThreadPool

from ScrapingTrivago import ScrapingTrivago


def call_main(s):
    try:
        s.copy_hotels()
    except:
        ...


years = ["2022", "2023"]
month = ["01", "02", "03", "06", "07", "08", "09", "10", "11", "12"]

start_date = []
end_date = []
isFuture = False
for y in years:
    for m in range(len(month)):
        if isFuture:
            start_date.append("{0}-11-{1}".format(month[m], y))
            end_date.append("{0}-12-{1}".format(month[m], y))
        if month[m] == "11" and y == "2022":
            isFuture = True
        if month[m] == "05" and y == "2023":
            break

nbr_adults = [1, 2]
nbr_children = [0, 2]
nbr_rooms = [1, 2, 3, 4, 5, 6]
city = "Paris"

nbr_csv = 0
for start, end in zip(start_date, end_date):
    scraper_list = []
    for adults, children, rooms in list(product(nbr_adults, nbr_children, nbr_rooms)):
        if rooms <= (adults + children):
            nbr_csv += 1
            t = ScrapingTrivago("trivago", city, start, end, adults, [9 for _ in range(children)], rooms)
            try:
                t.process_search_results()
                scraper_list.append(t)
                print("csv : ", nbr_csv)
            except:
                print("FATAL ERROR : Closing explorer")
                t.force_driver_close()


    pool = ThreadPool(50)
    pool.map(call_main, scraper_list)
