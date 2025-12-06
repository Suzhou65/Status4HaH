<!DOCTYPE html>
<html lang="en">
    <head>
        <!-- META -->
        <meta http-equiv="Cache-Control" content="max-age=604800"/>
        <meta http-equiv="Content-Type" content="text/html" charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="robots" content="noindex,nofollow">
        <!-- Style, 2025L06 -->
        <style>
        @media all{
            body{background: #FFFFFF;color: #24292E;font-family:sans-serif;font-size:100%;font-weight:400;margin-top:2rem;}
            h1{font-size:1.12rem;font-weight:600;margin:0 0 1.125rem;line-height:1.1;}
            h2{font-size:1.06rem;font-weight:600;color: #028090;margin:1.125 0.25 0.25 0.25rem;line-height:1.1;}
            h3{font-size:1.06rem;font-weight:600;color: #3399CC;margin:1.125 0.25 0.25 0.25rem;line-height:1.1;}
            a{font-size:0.917rem;text-decoration:none;color: #3399CC;}
            small{font-size:0.85rem;font-weight:600;}
            a small{font-size:0.75rem;color: #777777;margin-top:-0.3em;display:block;font-weight:600;}
            strong{color: #222222;font-weight:600;}
            .wrapper{max-width:73.75rem;margin:0 auto;}
            header{width:16.875rem;float:left;position:fixed;}
            header ul{list-style:none;width:16.875rem;height:2.5rem;padding:0;background:#F4F4F4;border-radius:0.313rem;border:0.063rem solid #E0E0E0;}
            header li{width:5.563rem;height:2.5rem;float:left;border-right:0.063rem solid #E0E0E0;}
            header ul a{height:2.125rem;padding-top:0.375rem;display:block;font-size:0.88rem;color: #999999;font-weight:600;line-height:1;text-align:center;}
            header ul li + li + li{width:5.563rem;border-right:none;}
            header ul a strong{font-size:0.875rem;color:#222222;font-weight:600;display:block;}
            footer{width:16.875rem;float:left;position:fixed;bottom:3.125rem;font-size:0.85rem;}
            section{width:51.875rem;float:right;padding-bottom:3.125rem;}
            .fail{margin:0px auto;text-align:center;font-size:1rem;color:#02C39A;padding:0.5rem;}
            table{margin:0px auto;border:0.063rem solid #FFFFFF;width:100%;border-collapse:collapse;}
            table tr{background: #FFFFFF;height:1.563rem;border-left:none;padding:0.188rem 0.125rem;}
            table tr:nth-child(1){background: #028090;color: #FFFFFF;border-left:none;padding:0.188rem 0.125rem;}
            table td{padding:0.5rem;}
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
            #program tr{background: #3399CC;color: #FFFFFF;border-left:none;padding:0.188rem 0.125rem;}
        }@media print,screen and (min-width:1280px){
            header{padding-right:11.25rem;}
        }@media print,screen and (max-width:1136px){
            .wrapper{width:auto;margin:0;}
            header,section,footer{float:none;position:static;width:auto;}
            header{padding-right:20rem;}
            section{border:0.063rem solid #E5E5E5;border-width:0.063rem 0;padding:1.25rem 0;margin:0 0 1.25rem;}
            header a small{display:inline;}
            header ul{position:absolute;right:3.125rem;top:3.25rem;}
        }@media print,screen and (max-width:960px){
            body{word-wrap:break-word;font-size:1rem;line-height:1.2rem;}
            header{padding:0;}
            header ul,header p.view{position:static;}
            table{margin:0px auto;border:0.063rem solid #FFFFFF;width:95%;border-collapse:collapse;}
            #ehentai td:nth-child(2){display:none;}
            #ehentai td:nth-child(3){text-align:center;font-weight:600;}
            #ehentai td:nth-child(4){display:none;}
            #ehentai td:nth-child(5){text-align:center;}
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
        <title>Status4HaH</title>
    </head>
    <body>
        <div class="wrapper">
            <header>
                <h1>Status4HaH</h1>
                <p>Demonstration</p>
                <ul>
                    <li><a href="javascript:history.back()">Previous<strong>Pages</strong></a></li>
                    <li><a href="javascript:window.location.reload()">Refresh<strong>Pages</strong></a></li>
                    <li><a href="https://github.com/Suzhou65/Status4HaH" target="_self">Source<strong>Code</strong></a></li>
                </ul>
            </header>
            <section>
                <!-- Load Status -->
                <h2>Hentai@Home Status</h2>
                <table id="ehentai">
                    <!-- php Start -->
                    <?php
                    header("refresh:600");
                    // File path as you python script location
                    if ($file = fopen("/script_location/status4hah.web.csv","r")){
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
                    <!-- php End -->
                </table>
                <!-- Load Runtime -->
                <h3>Status4HaH Runtime</h3>
                <table id="program">
                    <!-- php Start -->
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
                    <!-- php End -->
                </table>
            </section>
            <footer>
                <!-- FOOTER -->
                <!-- FOOTER -->
            </footer>
        </div>
    </body>
</html>