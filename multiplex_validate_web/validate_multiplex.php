<html>
<head>
<?php $y = $_COOKIE["y"];?>
<title>Multiplex-validate</title>
<style>
.page_container {
    width: 100%;
    margin: auto;
    height: 100%;
}
.instance_container {
    float: left;
    padding: 2px;
    border: 2px solid #000000;
}
.info_frame {
    float: top;
    padding: 10px;
    background-color: #808080;
}
.label_frame {
    float: left;
    padding: 5px;
//    border: 2px solid #808080;
}
.img_frame {
    float: top;
}
.img_frame_cd16 {
    float: top;
    display: none;
}
.label_cd3{
    background-color: yellow;
    font-weight: bold;
}
.label_cd4{
    background-color: turquoise;
    font-weight: bold;
}
.label_cd8{
    background-color: purple;
    color: white;
}
.label_cd16{
    background-color: black;
    color: white;
}
.label_cd20{
    background-color: red;
    color: white;
}
.label_k17{
    background-color: brown;
    color: white;
}
.score{
    font-weight: 550;
    color: black;
}
.footer1{
    float: left;
    clear:left;
}
</style>

<script>
function myFunction(img_id){
  var img = document.getElementById("img_"+img_id);
  var img_cd16 = document.getElementById("img_cd16_"+img_id);
  var toggle_cd16 = document.getElementById("toggle_cd16_"+img_id);  
  if (img.style.display === "none") {
    img_cd16.style.display = "none";
    img.style.display = "block";
    toggle_cd16.style.backgroundColor = '';
  }
  else {
    img.style.display = "none";
    img_cd16.style.display = "block";
    toggle_cd16.style.backgroundColor = "grey";
  }
}
</script>

</head>
<body>

<?PHP
#ini_set('display_errors', 1);
#ini_set('display_startup_errors', 1);
#error_reporting(E_ALL);
print "<body onScroll=\"document.cookie='y=' + window.pageYOffset\" onLoad='window.scrollTo(0,$y)'>";
?>

<?PHP
$page = $_GET['page'];
if($page < 0)
    $page = 0;
?>

<a href=validate_multiplex.php?page=<?PHP printf("%d", $page - 10);?>>Prev Page-10</a>
<a href=validate_multiplex.php?page=<?PHP printf("%d", $page - 1);?>>Prev Page</a>
<a href=validate_multiplex.php?page=<?PHP printf("%d", $page + 1);?>>Next Page</a>
<a href=validate_multiplex.php?page=<?PHP printf("%d", $page + 10);?>>Prev Page+10</a>

<p>
<?PHP 
$N_per_page = 1;
$folder = 'validate_images_input';
$folder_a = 'validate_images_set_a';
$folder_b = 'validate_images_set_b';

$total_images = count( glob(sprintf("%s/*.png", $folder)));
$total_pages = round(($total_images)/ $N_per_page + 0.5);
printf('You are in page [<b>%d</b> of %d]', $page, $total_pages-1);
#printf('You are in page [<b>%d</b> of %d]', $page, $total_images);

?>

<?PHP
printf("<section class=\"page_container\">\n\n");
for ($i = 1; $i <= $N_per_page; ++$i) {
$im_id = $i + $page * $N_per_page;

$savef = sprintf("./validate_files/im_id_label_%d.txt", $im_id);
if ($myfile = fopen($savef, 'r'))
$class0 = fread($myfile, 200);
else
$class0 = '';
   
#printf("<div>class0 =%s </div>", $class0); # debug


$info_file = sprintf("%s/%d_info_FN.txt", $folder, $im_id);
if ($myfile = fopen($info_file, 'r')) {
$im_filename = fread($myfile, 200);
printf("<section class=\"instance_container\">\n"); # only begin an instance container if the image exists
printf("<div class=\"info_frame\">\n");
printf("Image:%d (%s)", $im_id, $im_filename);
printf("</div>\n");
}
else
break;



printf("<form name=\"label\" method=\"POST\" action=validate_label.php?page=%d&im_id=%d&userid=%d>\n", $page, $im_id, 0);

# Image Set A

printf("<div class=\"label_frame\">\n");
printf("<p>Result A</p>\n");
# input image
printf("<div id=\"img_%s\" class=\"img_frame\">\n", $im_id);
printf("<img height=200px src=\"%s/%d.png\"/>\n", $folder, $im_id);
printf("</div>\n");
printf("<p/>\n");

# segmented image
printf("<div id=\"img_%s\" class=\"img_frame\">\n", $im_id);
printf("<img height=200px src=\"%s/%d.png\"/>\n", $folder_a, $im_id);
printf("</div>\n");
printf("<p/>\n");

printf("<div class=\"label_cd3\">");
printf("<input type=\"submit\" name=\"cd3a\" value=\"%s\"> CD3 <br>\n", strpos($class0,'cd3a')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd4\">");
printf("<input type=\"submit\" name=\"cd4a\" value=\"%s\"> CD4 <br>\n", strpos($class0,'cd4a')!==false ? 'x':'  ');
printf("</div>");
printf("<br>\n");

printf("<div class=\"label_cd20\">");
printf("<input type=\"submit\" name=\"cd20a\" value=\"%s\"> CD20 <br>\n", strpos($class0,'cd20a')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd8\">");
printf("<input type=\"submit\" name=\"cd8a\" value=\"%s\"> CD8 <br>\n", strpos($class0,'cd8a')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd16\">");
printf("<input type=\"submit\" name=\"cd16a\" value=\"%s\"> CD16 <br>\n", strpos($class0,'cd16a')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_k17\">");
printf("<input type=\"submit\" name=\"k17a\" value=\"%s\"> K17 <br>\n", strpos($class0,'k17a')!==false ? 'x':'  ');
printf("</div>");

printf("</div>\n");

# Image Set B
printf("<div class=\"label_frame\">\n");
printf("<p>Result B</p>\n");

# input image
printf("<div id=\"img_%s\" class=\"img_frame\">\n", $im_id);
printf("<img height=200px src=\"%s/%d.png\"/>\n", $folder, $im_id);
printf("</div>\n");
printf("<p/>\n");

# segmented image
printf("<div id=\"img_%s\" class=\"img_frame\">\n", $im_id);
printf("<img height=200px src=\"%s/%d.png\"/>\n", $folder_b, $im_id);
printf("</div>\n");

printf("<br>\n");
printf("<div class=\"label_cd3\">");
printf("<input type=\"submit\" name=\"cd3b\" value=\"%s\"> CD3 <br>\n", strpos($class0,'cd3b')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd4\">");
printf("<input type=\"submit\" name=\"cd4b\" value=\"%s\"> CD4 <br>\n", strpos($class0,'cd4b')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd20\">");
printf("<input type=\"submit\" name=\"cd20b\" value=\"%s\"> CD20 <br>\n", strpos($class0,'cd20b')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd8\">");
printf("<input type=\"submit\" name=\"cd8b\" value=\"%s\"> CD8 <br>\n", strpos($class0,'cd8b')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd16\">");
printf("<input type=\"submit\" name=\"cd16b\" value=\"%s\"> CD16 <br>\n", strpos($class0,'cd16b')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_k17\">");
printf("<input type=\"submit\" name=\"k17b\" value=\"%s\"> K17 <br>\n", strpos($class0,'k17b')!==false ? 'x':'  ');
printf("</div>");

printf("</div>\n");
printf("</form>\n");

printf("</section>\n\n");
}
printf("<section class=\"footer1\">\n");
printf("<a href=validate_multiplex.php?page=%d>Prev Page</a>\n", $page-1);
printf("<a href=validate_multiplex.php?page=%d>Next Page</a>\n", $page+1);
printf("</section>\n");
printf("</section>\n");
?>



</body>
</html>
