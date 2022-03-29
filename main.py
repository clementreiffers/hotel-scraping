from bookingCom import Booking
from multiprocessing import Process
from multiprocessing.dummy import Pool as ThreadPool


def waitUntilBookingComplete(s):
    s.process_search_results()


start_date = ["{}-11-2022".format(i) for i in ["04", "05", "06", "07", "08"]]
end_date = ["{}-01-2022".format(i) for i in ["05", "06", "07", "08", "09"]]

nbr_adults = 2
city = "paris"
nbr_children = 2
nbr_rooms = 2
ages_of_children = [5, 9]
scraper = []

for s, e in zip(start_date, end_date):
    print(s, e)
    b = Booking(city=city,
                start_date=s,
                end_date=e,
                nbr_adults=nbr_adults,
                nbr_children=nbr_children,
                nbr_room=nbr_rooms,
                ages_of_children=ages_of_children,
                filename="bookingCom_{0}_to_{1}.csv".format(s, e))
    b.process_search_results()
    scraper.append(b)

pool = ThreadPool(6)
pool.map(lambda s: s.main(), scraper)
