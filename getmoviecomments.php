<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Movie Sentiments</title>
<!-- CSS goes in the document HEAD or added to your external stylesheet -->
<style type="text/css">
table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size:11px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
	width:800px;
}
table.gridtable th {
	border-width: 0px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #363636;
	color:#FFFFFF;
}
table.gridtable td {
	border-width: 0px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color:#F2F2F2;
}
</style>


</head>

<body bgcolor="#9D9DFF">
<?php 
if($_POST){
$moviename = $_POST["moviename"];
$moviepath = $moviename.".xml";
}
else{
$moviename = $_GET["moviename"];
$moviepath = $moviename.".xml";
}?>
<h1 align="center" style="color:#000000"><?php echo $moviename ?></h1>
<br />
<div align="center">  
<form style="color:#000000" action="/movieratings/getmoviecomments.php" method="post">
Search Movie:<input type="text" name="moviename" />
<input type="submit" value="Go" />
</form>

<div align="center"><br />

<script>
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  
xmlhttp.open("GET","<?php echo $moviepath; ?>",false);
xmlhttp.send();
xmlDoc=xmlhttp.responseXML; 

document.write("<table class=\"gridtable\">");
document.write("<tr><th>");
document.write("People liked the movie because:");
document.write("</th><th>");
document.write("People disliked the movie because:");
document.write("</th></tr>");
document.write("<tr>");
var x=xmlDoc.getElementsByTagName("pos");
document.write("<td><dl>");
for (i=0;i<x.length;i++)
  { 
  document.write("<dt><b>");
  document.write(x[i].getElementsByTagName("name")[0].childNodes[0].nodeValue);
  document.write("&nbsp;&nbsp;&nbsp;&nbsp;");
  document.write(x[i].getElementsByTagName("score")[0].childNodes[0].nodeValue);
  document.write("</b></dt><dd>-");
 
  document.write(x[i].getElementsByTagName("tweet1")[0].childNodes[0].nodeValue);
  document.write("</dd><br /><dd>-");
  document.write(x[i].getElementsByTagName("tweet2")[0].childNodes[0].nodeValue);
  document.write("</dd><br />");
  }
document.write("</dl></td>");
var x=xmlDoc.getElementsByTagName("neg");
document.write("<td><dl>");
for (i=0;i<x.length;i++)
  { 
  document.write("<dt><b>");
  document.write(x[i].getElementsByTagName("name")[0].childNodes[0].nodeValue);
  document.write("&nbsp;&nbsp;&nbsp;&nbsp;");
  document.write(x[i].getElementsByTagName("score")[0].childNodes[0].nodeValue);
  document.write("</b></dt><dd>-");
 
  document.write(x[i].getElementsByTagName("tweet1")[0].childNodes[0].nodeValue);
  document.write("</dd><br /><dd>-");
  document.write(x[i].getElementsByTagName("tweet2")[0].childNodes[0].nodeValue);
  document.write("</dd><br />");
  }
document.write("</dl></td>");
document.write("</tr>");
document.write("</table>");
</script>

</html>
