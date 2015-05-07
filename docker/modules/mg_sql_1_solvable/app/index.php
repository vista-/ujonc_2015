<!doctype html>
<html>
<head>
</head>
<body>
    <table>
        <tr>
            <th><a href="?order=id">id</a></th>
            <th><a href="?order=name">name</a></th>
            <th><a href="?order=description">description</a></th>
            <th><a href="?order=price">price</a></th>
        </tr>

<?php
mysql_connect('localhost', 'root');
mysql_select_db('test');

error_reporting(-1);
ini_set('display_errors', 'On');

$order = isset($_GET['order']) ? $_GET['order'] : 'id';
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
