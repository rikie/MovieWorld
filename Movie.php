<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Movie Sentiments</title>
<link href="/movieratings/themes/5/js-image-slider.css" rel="stylesheet" type="text/css" />
<script src="/movieratings/themes/5/js-image-slider.js" type="text/javascript"></script>
<link href="/movieratings/generic.css" rel="stylesheet" type="text/css" />
</head>

<body>
<h1 align="center" style="color:#000000">MOVIE WORLD</h1>
<div align="center">
<form style="color:#000000" action="/movieratings/getmoviecomments.php" method="post">
Search Movie:<input type="text" name="moviename" />
<input type="submit" value="Go" />
</form></div>
<div class="div1"><h2>Hot This Week</h2>
    </div>

    <div id="sliderFrame">
        <div id="slider">
            <a href="/movieratings/getmoviecomments.php?&moviename=Captain America">
                <img src="/movieratings/images2/captain_america_BIG.jpg" alt="Captain America" />
            </a>
			 <a href="/movieratings/getmoviecomments.php?&moviename=Divergent">
                <img src="/movieratings/images2/divergent_BIG.jpg" alt="Divergent" />
            </a>
			<a href="/movieratings/getmoviecomments.php?&moviename=Heaven is for real">
                <img src="/movieratings/images2/heaven_is_for_real_BIG.jpg" alt="Heaven is for real" />
			</a>
			<a href="/movieratings/getmoviecomments.php?&moviename=Bears">
                <img src="/movieratings/images2/bears_BIG.jpg" alt="Bears" />
			</a>
			<a href="/movieratings/getmoviecomments.php?&moviename=A Haunted House 2">
                <img src="/movieratings/images2/a_haunted_house_2_BIG.jpg" alt="A haunted house 2" />
			</a>
			 <a href="/movieratings/getmoviecomments.php?&moviename=Noah">
                <img src="/movieratings/images2/noah_big.jpg" alt="Noah" />
            </a>
			 <a href="/movieratings/getmoviecomments.php?&moviename=Oculus">
                <img src="/movieratings/images2/oculus_big.jpg" alt="Oculus" />
            </a>
            
        </div>
        
                
        <!--thumbnails-->
        <div id="thumbs">
			<div class="thumb"><img src="/movieratings/images2/captainamerica.jpg" /></div>
            <div class="thumb"><img src="/movieratings/images2/divergent.jpg" /></div>
			<div class="thumb"><img src="/movieratings/images2/heaven_is_for_real.jpg" /></div>
			<div class="thumb"><img src="/movieratings/images2/bears.jpg" /></div>
			<div class="thumb"><img src="/movieratings/images2/a_haunted_house_2.jpg" /></div>
            <div class="thumb"><img src="/movieratings/images2/noah.jpg" /></div>
            <div class="thumb"><img src="/movieratings/images2/oculus.jpg" /></div>
            
        </div>
    </div>

   

</body>
</html>
