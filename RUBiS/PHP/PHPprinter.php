<?php
 
function getDatabaseLink(&$link)
{
  $link = mysql_pconnect("152.46.16.115", "rubis", "rubis") or die ("ERROR: Could not connect to database");
  mysql_select_db("rubis", $link) or die("ERROR: Couldn't select RUBiS database");
}

function getMicroTime()
{
  list($usec, $sec) = explode(" ", microtime());
  return ((float)$usec + (float)$sec);
}

function printHTMLheader($title)
{
  include("header.html");
  print("<title>$title</title>");
}

function printHTMLHighlighted($msg)
{
  print("<TABLE width=\"100%\" bgcolor=\"#CCCCFF\">\n");
  print("<TR><TD align=\"center\" width=\"100%\"><FONT size=\"4\" color=\"#000000\"><B>$msg</B></FONT></TD></TR>\n");
  print("</TABLE><p>\n");
}

function printHTMLfooter($scriptName, $startTime)
{
  $endTime = getMicroTime();
  $totalTime = $endTime - $startTime;
  printf("<br><hr>RUBiS (C) Rice University/INRIA<br><i>Page generated by $scriptName in %.3f seconds</i><br>\n", $totalTime);
  print("</body>\n");
  print("</html>\n");	
}

function printError($scriptName, $startTime, $title, $error)
{
  printHTMLheader("RUBiS ERROR: $title");
  print("<h2>We cannot process your request due to the following error :</h2><br>\n");
  print($error);
  printHTMLfooter($scriptName, $startTime);      
}

function authenticate($nickname, $password, $link)
{
  $result = mysql_query("SELECT id FROM users WHERE nickname=\"$nickname\" AND password=\"$password\"", $link) or die("ERROR: Authentification query failed");
  if (mysql_num_rows($result) == 0)
    return -1;
  $row = mysql_fetch_array($result);
  return $row["id"];
}

function begin($link)
{
  mysql_query("BEGIN", $link);
}

function commit($link)
{
  mysql_query("COMMIT", $link);
}

function rollback($link)
{
  mysql_query("ROLLBACK", $link);
}

?>
