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

$savef = sprintf("./label_files/im_id_label_%d.txt", $im_id);
if (isset($_POST['clr']))
    unlink($savef);
else {
    if ($myfile = fopen($savef, 'r'))
        $class = fread($myfile, 200);
    else
        $class = '';

    touch($savef);
    $myfile = fopen($savef, 'w') or die('Unable to open file for status saving!');
    if      (isset($_POST['cd3l']))
        fwrite($myfile, sprintf("cd3l,"));
    else if (isset($_POST['cd3h']))
        fwrite($myfile, sprintf("cd3h,"));
    else if (strpos($class,'cd3l')!==false)
        fwrite($myfile, sprintf("cd3l,"));
    else if (strpos($class,'cd3h')!==false)
        fwrite($myfile, sprintf("cd3h,"));

    if      (isset($_POST['cd4l']))
        fwrite($myfile, sprintf("cd4l,"));
    else if (isset($_POST['cd4h']))
        fwrite($myfile, sprintf("cd4h,"));
    else if (strpos($class,'cd4l')!==false)
        fwrite($myfile, sprintf("cd4l,"));
    else if (strpos($class,'cd4h')!==false)
        fwrite($myfile, sprintf("cd4h,"));

    if      (isset($_POST['cd8l']))
        fwrite($myfile, sprintf("cd8l,"));
    else if (isset($_POST['cd8h']))
        fwrite($myfile, sprintf("cd8h,"));
    else if (strpos($class,'cd8l')!==false)
        fwrite($myfile, sprintf("cd8l,"));
    else if (strpos($class,'cd8h')!==false)
        fwrite($myfile, sprintf("cd8h,"));

    if      (isset($_POST['cd16l']))
        fwrite($myfile, sprintf("cd16l,"));
    else if (isset($_POST['cd16h']))
        fwrite($myfile, sprintf("cd16h,"));
    else if (strpos($class,'cd16l')!==false)
        fwrite($myfile, sprintf("cd16l,"));
    else if (strpos($class,'cd16h')!==false)
        fwrite($myfile, sprintf("cd16h,"));

    if      (isset($_POST['cd20l']))
        fwrite($myfile, sprintf("cd20l,"));
    else if (isset($_POST['cd20h']))
        fwrite($myfile, sprintf("cd20h,"));
    else if (strpos($class,'cd20l')!==false)
        fwrite($myfile, sprintf("cd20l,"));
    else if (strpos($class,'cd20h')!==false)
        fwrite($myfile, sprintf("cd20h,"));

    fclose($myfile);
}

$url = sprintf("Location: view_patches_multiplex.php?page=%d", $page);
header($url);
?>

</body>
</html>
