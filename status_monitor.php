<!DOCTYPE html>
<html lang="en">
    <head>
        <!-- META -->
        <meta http-equiv="Cache-Control" content="No-Cache"/>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="robots" content="noindex,nofollow">
        <!-- Style 2025L06-->
        <style>
        @media all{
            html{font-size:100%;font-family:sans-serif;color:#666666;font-weight:400;}
            body{margin-top:9%;}
            a{font-size:0.917rem;text-decoration:none;color:#00A896;}
            .banner{margin-top:1.5rem;margin-bottom:1rem;margin:0px auto;text-align:center;font-size:1rem;color:#05668D;font-weight:500;padding:0.5rem;}
            /* If load fail */
            .fail{margin:0px auto;text-align:center;font-size:1rem;color:#02C39A;font-weight:500;padding:0.5rem;}
            /* Table */
            table{margin:0px auto;border:0.063rem solid #FFFFFF;width:80%;border-collapse:collapse;}
            /* Table*/
            table tr{background:#FFFFFF;height:1.563rem;border-left:none;padding:0.188rem 0.125rem;}
            /*Header*/
            table tr:nth-child(1){background:#028090;color:#FFFFFF;border-left:none;padding:0.188rem 0.125rem;}
            /*Column*/
            table td{padding:0.5rem;}
            /*Hentai@Home status*/
            #ehentai td:nth-child(2){display:none;}
            #ehentai td:nth-child(3){text-align:center;font-weight:600;}
            #ehentai td:nth-child(4){display:none;}
            #ehentai td:nth-child(5){text-align:center;min-width:3rem;}
            #ehentai td:nth-child(6){text-align:center;min-width:5rem;}
            #ehentai td:nth-child(7){display:none;}
            #ehentai td:nth-child(8){display:none;}
            #ehentai td:nth-child(9){display:none;}
            #ehentai td:nth-child(10){display:none;}
            #ehentai td:nth-child(11){text-align:center;min-width:2rem;}
            #ehentai td:nth-child(12){text-align:center;min-width:2rem;}
            #ehentai td:nth-child(13){display:none;}
            #ehentai td:nth-child(14){display:none;}
            #ehentai td:nth-child(15){text-align:center;min-width:2rem;}
            /*Status4Hah runtime*/
            #program tr:nth-child(1){background: #3399CC;color: #FFFFFF;border-left:none;padding:0.188rem 0.125rem;}}
        /* RWD in mobile device */
        @media print,screen and (max-width: 960px){
            body{font-size:1rem;line-height:1.2rem;font-weight:450;}
            .banner{display:none;}
            .footer{margin-top:5rem;margin:0px auto;text-align:center;font-size:0.6rem;font-weight:500;padding:0.5rem}
            table{margin:0px auto;border:0.063rem solid #FFFFFF;width:95%;border-collapse:collapse;}
            #ehentai td:nth-child(2){display:none;}
            #ehentai td:nth-child(3){text-align:center;font-weight:600;}
            #ehentai td:nth-child(4){display:none;}
            #ehentai td:nth-child(5){text-align:center;font-weight:500;}
            #ehentai td:nth-child(6){display:none;}
            #ehentai td:nth-child(7){display:none;}
            #ehentai td:nth-child(8){display:none;}
            #ehentai td:nth-child(9){display:none;}
            #ehentai td:nth-child(10){display:none;}
            #ehentai td:nth-child(11){display:none;}
            #ehentai td:nth-child(12){display:none;}
            #ehentai td:nth-child(13){display:none;}
            #ehentai td:nth-child(14){display:none;}
            #ehentai td:nth-child(15){display:none;}}
        </style>
        <!-- Title -->
        <title>Hentai@Home Client Status</title>
    </head>
    <!-- Body -->
    <body>
        <!-- Load CSV file -->
        <div class="banner">Hentai@Home Status</div>
        <table id="ehentai">
            <!-- php block -->
            <?php
            header("refresh:600");
            // File path as you python script location
            if ($file = fopen("/script_location/status4hah.check.csv","r")){
                while (($line = fgetcsv($file)) !== false){
                    echo "<tr>";
                    foreach ($line as $cell) {echo "<td>" . htmlspecialchars($cell) . "</td>";}
                    echo "</tr>\n";}
                    fclose($file);
                }else{
                    // If unable open file
                    echo '<div class="fail">';
                    echo "Unable to open monitoring file.";
                    echo "</div>";}
            ?>
            <!-- php block -->
        </table>
        <br>
        <div class="banner">Monitor Status</div>
        <table id="program">
            <!-- php block -->
            <?php
            header("refresh:600");
            // File path as you python script location
            if ($file = fopen("/script_location/status4hah.status.csv","r")){
                while (($line = fgetcsv($file)) !== false){
                    echo "<tr>";
                    foreach ($line as $cell) {echo "<td>" . htmlspecialchars($cell) . "</td>";}
                    echo "</tr>\n";}
                    fclose($file);
                }else{
                    // If unable open file
                    echo '<div class="fail">';
                    echo "Unable to open monitoring file.";
                    echo "</div>";}
            ?>
            <!-- php block -->
        </table>
    </body>
</html>