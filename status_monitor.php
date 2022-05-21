<!DOCTYPE html>
<html>
    <head>
        <!-- META -->
        <meta http-equiv="Cache-Control" content="No-Cache"/>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <!-- Style -->
        <style>
        @media all{
            html{font-size:100%; font-family:sans-serif; color:#666666;}
            body{margin-top:9%;}
            a{font-size:0.917rem; text-decoration:none; color:#0B6FA4;}
            .banner{margin:0px auto; text-align:center; font-size:1rem; color:#05668D; font-weight:bold; padding:1rem;}
            .fail{margin:0px auto; text-align:center; font-size:1rem; color:#FF5733; font-weight:bold; padding:1rem;}
            .footer{margin:0px auto; text-align:center; font-size:0.8rem; font-weight:bold; padding:0.917rem}
            .time{margin:0px auto; text-align:center; font-size:0.917rem; padding:1rem;}
            /* Table */
            table{margin:0px auto; border:0.063rem solid #FFFFFF; width:80%; border-collapse:collapse;}
                tr{background:#FFFFFF; height:1.563rem; border-left:none; padding:0.188rem 0.125rem;}
                /*Header*/
                tr:nth-child(1){background:#028090; color:#FFFFFF; border-left:none; padding:0.188rem 0.125rem;}
                /*Column*/
                td{padding:0.5rem;}
                td:nth-child(2){text-align:center;font-weight:bold;}
                td:nth-child(4){text-align:center;min-width:5rem;}
                td:nth-child(5){text-align:center;min-width:2rem;}
                td:nth-child(6){text-align:center;min-width:3rem;}
                td:nth-child(7){text-align:center;min-width:2rem;}
                td:nth-child(8){text-align:center;min-width:2rem;}}
        /*RWD*/
        @media print,screen and (max-width: 960px){
            body {font-size:1rem; line-height:1.2rem;}
            .banner{margin:0px auto; text-align:center; font-size:0.5rem; color:#05668D; font-weight:bold; padding:0.5rem;}
            .time{margin:0px auto; text-align:center; font-size:0.563rem; padding:0.5rem;}
            table{margin:0px auto; border:0.063rem solid #FFFFFF; width:95%; border-collapse:collapse;}
                td:nth-child(4){display:none;}
                td:nth-child(5){display:none;}
                td:nth-child(6){display:none;}
                td:nth-child(7){display:none;}
                td:nth-child(8){display:none;}}
        </style>
        <!-- Title -->
        <title>Hentai@Home Client Status</title>
    </head>
    <!-- Body -->
    <body>
        <!-- Load CSV file -->
        <div class="banner">Hentai@Home Status</div>
        <table class="ehentai">
            <!-- php block -->
            <?php
            header("refresh:600");
            // File path as you python script location
            if ($file = fopen("/python_script_location/status_monitor.csv","r")){
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
        <table class="program">
            <!-- php block -->
            <?php
            header("refresh:600");
            // File path as you python script location
            if ($file = fopen("/python_script_location/status_program.csv","r")){
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
        <div class="footer">
            <a href="https://github.com/Suzhou65/Status4HaH">Source Code</a> | <a href="javascript:history.back()">Previous Pages</a>
        </div>
    </body>
</html>