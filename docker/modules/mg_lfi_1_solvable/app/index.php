<!doctype html>
<html>
<head>
</head>
<body>
<div style="border: 1px solid black">
    <a href="?p=<?php echo base64_encode('welcome.php'); ?>">Welcome</a>
    <a href="?p=<?php echo base64_encode('forum.php'); ?>">Forum</a>
    <a href="?p=<?php echo base64_encode('about.php'); ?>">About</a>
</div>
<?php
error_reporting(-1);
ini_set('display_errors', 'On');
$page = isset($_GET['p']) ? $_GET['p'] : base64_encode('welcome.php');
$page = base64_decode($page);
include($page);
?>
</body>
</html>
