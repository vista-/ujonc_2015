<!doctype html>
<html>
<head>
</head>
<body>

<h1>Please test our brand new, open source NoSQL key-value store.</h1>

<form>
    <input type="text" name="key" placeholder="Key">
    <input type="submit" value="GET">
</form>
<br>

<form>
    <input type="text" name="key" placeholder="Key">
    <input type="text" name="value" placeholder="Value">
    <input type="submit" value="SET">
</form>
<br>

<?php
error_reporting(-1);
ini_set('display_errors', 'On');

if (isset($_GET['key']) && isset($_GET['value'])) {
    $file = base64_encode($_GET['key']);
    file_put_contents($file, $_GET['value']);
}

if (isset($_GET['key'])) {
    $file = base64_encode($_GET['key']);
    if (file_exists($file)) {
        echo htmlspecialchars($_GET['key']) . ' ---> ';
        include($file);
        echo '<br>';
    } else {
        echo htmlspecialchars($_GET['key']) . ' ---> No value! <br>';
    }
}
?>

<h2>The source code:</h2>
<pre>
<?php echo htmlspecialchars(file_get_contents(__FILE__)); ?>
</pre>
</body>
</html>
