<!doctype html>
<html>
<head>
</head>
<body>
    <table>
        <tr>
            <th><a href="?order=<?php echo str_rot13('id'); ?>">id</a></th>
            <th><a href="?order=<?php echo str_rot13('name'); ?>">name</a></th>
            <th><a href="?order=<?php echo str_rot13('description'); ?>">description</a></th>
            <th><a href="?order=<?php echo str_rot13('price'); ?>">price</a></th>
        </tr>

<?php
mysql_connect('localhost', 'root');
mysql_select_db('test');

error_reporting(-1);
ini_set('display_errors', 'On');

$order = isset($_GET['order']) ? $_GET['order'] : str_rot13('id');
$order = str_rot13($order);
$result = mysql_query("SELECT * FROM products ORDER BY $order");
while($row = mysql_fetch_row($result)) {
    echo '        <tr>';
    foreach ($row as $cell) echo "            <td>$cell</td>";
    echo '        </tr>';
}
// TODO: authenticated administrator access to the 'secrets' table
?>

    </table>
</body>
</html>
