<html>
<head>
<title>label</title>
</head>

<body>

<?PHP
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


$page = $_GET['page'];
$im_id = $_GET['im_id'];
$userid = $_GET['userid'];

$savef = sprintf("./validate_files/im_id_label_%d.txt", $im_id);
if (isset($_POST['clr']))
    unlink($savef);
else {
    if ($myfile = fopen($savef, 'r'))
        $class = fread($myfile, 200);
    else
        $class = '';

    touch($savef);
    $myfile = fopen($savef, 'w') or die('Unable to open file for status saving!');
    if      (isset($_POST['cd3a']))
        fwrite($myfile, sprintf("cd3a,"));
    else if (strpos($class,'cd3a')!==false)
        fwrite($myfile, sprintf("cd3a,"));

    if      (isset($_POST['cd3b']))
        fwrite($myfile, sprintf("cd3b,"));
    else if (strpos($class,'cd3b')!==false)
        fwrite($myfile, sprintf("cd3b,"));

    if      (isset($_POST['cd4a']))
        fwrite($myfile, sprintf("cd4a,"));
    else if (strpos($class,'cd4a')!==false)
        fwrite($myfile, sprintf("cd4a,"));

    if      (isset($_POST['cd4b']))
        fwrite($myfile, sprintf("cd4b,"));
    else if (strpos($class,'cd4b')!==false)
        fwrite($myfile, sprintf("cd4b,"));

    if      (isset($_POST['cd8a']))
        fwrite($myfile, sprintf("cd8a,"));
    else if (strpos($class,'cd8a')!==false)
        fwrite($myfile, sprintf("cd8a,"));

    if      (isset($_POST['cd8b']))
        fwrite($myfile, sprintf("cd8b,"));
    else if (strpos($class,'cd8b')!==false)
        fwrite($myfile, sprintf("cd8b,"));

    if      (isset($_POST['cd16a']))
        fwrite($myfile, sprintf("cd16a,"));
    else if (strpos($class,'cd16a')!==false)
        fwrite($myfile, sprintf("cd16a,"));

    if      (isset($_POST['cd16b']))
        fwrite($myfile, sprintf("cd16b,"));
    else if (strpos($class,'cd16b')!==false)
        fwrite($myfile, sprintf("cd16b,"));

    if      (isset($_POST['cd20a']))
        fwrite($myfile, sprintf("cd20a,"));
    else if (strpos($class,'cd20a')!==false)
        fwrite($myfile, sprintf("cd20a,"));

    if      (isset($_POST['cd20b']))
        fwrite($myfile, sprintf("cd20b,"));
    else if (strpos($class,'cd20b')!==false)
        fwrite($myfile, sprintf("cd20b,"));


    if      (isset($_POST['k17a']))
        fwrite($myfile, sprintf("k17a,"));
    else if (strpos($class,'k17a')!==false)
        fwrite($myfile, sprintf("k17a,"));

    if      (isset($_POST['k17b']))
        fwrite($myfile, sprintf("k17b,"));
    else if (strpos($class,'k17b')!==false)
        fwrite($myfile, sprintf("k17b,"));


    fclose($myfile);
}

$url = sprintf("Location: validate_multiplex.php?page=%d", $page);
header($url);
?>

</body>
</html>
