from bookingCom import Booking
from multiprocessing import Process


def waitUntilBookingComplete(s):
    processing = s.main()
    while not processing.iCanWorkAlone:
        print("lancement du navigateur...")
    print("ok")


# start_date = ["{}-11-2022".format(i) for i in ["04", "05", "06", "07", "08", "09", "10", "11"]]
# end_date = ["{}-11-2022".format(i) for i in ["05", "06", "07", "08", "09", "10", "11", "12"]]
start_date = ["04-11-2022"]
end_date = ["05-11-2022"]
nbr_adults = 2
city = "paris"
nbr_children = 2
nbr_rooms = 2
ages_of_children = [5, 9]
scraper = []

for s, e in zip(start_date, end_date):
    print(s, e)
    scraper.append(Booking(city=city,
                           start_date=s,
                           end_date=e,
                           nbr_adults=nbr_adults,
                           nbr_children=nbr_children,
                           nbr_room=nbr_rooms,
                           ages_of_children=ages_of_children,
                           filename="bookingCom_{0}_to_{1}.csv".format(s, e)))

from multiprocessing.dummy import Pool as ThreadPool

pool = ThreadPool(6)
results = pool.map(waitUntilBookingComplete, scraper)
