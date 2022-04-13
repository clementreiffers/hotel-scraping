dfd.readCSV("https://raw.githubusercontent.com/clementreiffers/HotelScraping/main/HotelScraping/csv/csv_graphs/booking_csv_graph.csv")
    .then(df => {
        //do something with the CSV file
        df.head().print()

        let layout = {
            title: "Hotels' mean price per month",
            xaxis: {
                title: "Date",
            },
            yaxis: {
                title: "Price",
            },
        };

        let config = {
            columns: ["Price"],
        };

        let new_df = df.setIndex({ column: "Date" });
        new_df.plot("plot_div").line({ config, layout });

    }).catch(err => {
        console.log(err);
    })