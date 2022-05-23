<!DOCTYPE html>
<html>
    <head>
        <!-- META -->
        <meta http-equiv="Cache-Control" content="No-Cache"/>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <!-- Style -->
        <style>
        @media all{
            html{font-size:100%; font-family:sans-serif; color:#666666; font-weight:400;}
            body{margin-top:9%;}
            a{font-size:0.917rem; text-decoration:none; color:#00A896;}
            .banner{margin-top:1rem; margin-bottom:1rem; margin:0px auto; text-align:center; font-size:1rem; color:#05668D; font-weight:500; padding:0.5rem;}
            /* If load fail */
            .fail{margin:0px auto; text-align:center; font-size:1rem; color:#02C39A; font-weight:500; padding:0.5rem;}
            /* Show source code */
            .footer{margin-top:2rem; margin:0px auto; text-align:center; font-size:0.8rem; font-weight:500; padding:0.917rem}
            /* Table */
            table{margin:0px auto; border:0.063rem solid #FFFFFF; width:80%; border-collapse:collapse;}
                tr{background:#FFFFFF; height:1.563rem; border-left:none; padding:0.188rem 0.125rem;}
                /*Header*/
                tr:nth-child(1){background:#028090; color:#FFFFFF; border-left:none; padding:0.188rem 0.125rem;}
                /*Column*/
                td{padding:0.5rem;}
                td:nth-child(2){text-align:center;font-weight:600;}
                td:nth-child(4){text-align:center;min-width:5rem;}
                td:nth-child(5){text-align:center;min-width:2rem;}
                td:nth-child(6){text-align:center;min-width:3rem;}
                td:nth-child(7){text-align:center;min-width:2rem;}
                td:nth-child(8){text-align:center;min-width:2rem;}}
        /* RWD */
        @media print,screen and (max-width: 960px){
            body{font-size:1rem; line-height:1.2rem; font-weight:500;}
            .banner{margin-top:0.5rem; margin-bottom:1rem; margin:0px auto; text-align:center; font-size:0.5rem; color:#05668D; font-weight:600; padding:0.5rem;}
            .footer{margin-top:1.5rem; margin:0px auto; text-align:center; font-size:0.5rem; font-weight:500; padding:0.5rem}
            table{margin:0px auto; border:0.063rem solid #FFFFFF; width:95%; border-collapse:collapse;}
                td:nth-child(4){display:none;}
                td:nth-child(5){display:none;}
                td:nth-child(6){display:none;}
                td:nth-child(7){display:none;}
                td:nth-child(8){display:none;}}
        /* 20220523 */
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
            <a href="https://github.com/Suzhou65/Status4HaH">Source Code</a>
        </div>
    </body>
</html>