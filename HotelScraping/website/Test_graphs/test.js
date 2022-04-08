import * as dfd from "danfojs-node"

// dates format YYYY-MM-DD

dfd.readCSV("booking_csv_graph.csv")
    .then(df => {
        //do something with the CSV file
        df.head().print()

        let layout = {
            title: "A financial charts",
            xaxis: {
                title: "Dates",
            },
            yaxis: {
                title: "Prices",
            },
        };

        let config = {
            columns: ["dates"],
        };

        let new_df = df.setIndex({ column: "date" });
        new_df.plot("plot_div").line({ config, layout });

    }).catch(err=>{
    console.log(err);
})