<html>
<head>
<?php $y = $_COOKIE["y"];?>
<title>Multiplex-prediction</title>
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

<?php
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

<a href=view_pred_multiplex.php?page=<?PHP printf("%d", $page - 10);?>>Prev Page-10</a>
<a href=view_pred_multiplex.php?page=<?PHP printf("%d", $page - 1);?>>Prev Page</a>
<a href=view_pred_multiplex.php?page=<?PHP printf("%d", $page + 1);?>>Next Page</a>
<a href=view_pred_multiplex.php?page=<?PHP printf("%d", $page + 10);?>>Next Page+10</a>
<p>
<?PHP 
$N_per_page = 8;
$folder = 'images_test';
#$folder_cd16 = 'images_cd16';

$total_images = count( glob(sprintf("%s/*.png", $folder)));
$total_pages = round(($total_images)/ $N_per_page + 0.5);
printf('You are in page [<b>%d</b> of %d]', $page, $total_pages-1);
#printf('You are in page [<b>%d</b> of %d]', $page, $total_images);

?>

<p>

<div class="label_frame label_cd3">
CD3: Low &le; 2, High > 2 (cells)
</div>
<div class="label_frame label_cd4">
CD4: Low &le; 2, High > 2 (cells)
</div>
<div class="label_frame label_cd20">
CD20: Low &le; 2, High > 2 (cells)
</div>
<div class="label_frame label_cd8">
CD5: Low &le; 5, High > 5 (cells)
</div>
<div class="label_frame label_cd16">
CD16: Low &le; 20%, High > 20% (area)
</div>
</br></br>

<?PHP
printf("<section class=\"page_container\">\n\n");
for ($i = 1; $i <= $N_per_page; ++$i) {
$im_id = $i + $page * $N_per_page;
#printf("<p>%d</p>", $im_id);

$savef = sprintf("./images_test_pred_vgg/pred_%d.txt", $im_id);
if ($myfile = fopen($savef, 'r'))
$class0 = fread($myfile, 200);
else
$class0 = '';
   
#printf("<div>class0 =%s </div>", $class0); # debug

#$files_cd16 = glob(sprintf("%s/%d_*.png", $folder_cd16, $im_id));
#if(count($files_cd16)>0){
#$cd16_file = $files_cd16[0];
#printf("<p>%s</p>", $cd16_file);
#$score = substr($cd16_file, strpos($cd16_file, "=")+1, -4);
#printf("<p>%s</p>", substr($cd16_file, strpos($cd16_file, "=")+1, -4));
#}

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
#    $info_file = sprintf("%s/%d_info_FN.txt", $folder, $im_id);
#    if ($myfile = fopen($info_file, 'r')) {
#        $patch_filename = fread($myfile, 80);
#        printf("  %s\n", $patch_filename);
#    }


#printf("<form name=\"label\" method=\"POST\" action=label.php?page=%d&im_id=%d&userid=%d>\n", $page, $im_id, 0);
printf("<form name=\"label\">\n");
printf("<div class=\"label_frame\">\n");
printf("<div class=\"label_cd3\">");
printf("CD3<br/>");
printf("<input type=\"submit\" disabled name=\"cd3l\" value=\"%s\"> Low <br>\n", strpos($class0,'cd3l')!==false ? 'x':'  ');
printf("<input type=\"submit\" disabled name=\"cd3h\" value=\"%s\"> High <br>\n", strpos($class0,'cd3h')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd4\">");
printf("CD4<br/>");
printf("<input type=\"submit\" disabled  name=\"cd4l\" value=\"%s\"> Low <br>\n", strpos($class0,'cd4l')!==false ? 'x':'  ');
printf("<input type=\"submit\" disabled name=\"cd4h\" value=\"%s\"> High <br>\n", strpos($class0,'cd4h')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd20\">");
printf("CD20<br/>");
printf("<input type=\"submit\" disabled name=\"cd20l\" value=\"%s\"> Low <br>\n", strpos($class0,'cd20l')!==false ? 'x':'  ');
printf("<input type=\"submit\" disabled name=\"cd20h\" value=\"%s\"> High <br>\n", strpos($class0,'cd20h')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("</div>"); # label_frame

printf("<div class=\"label_frame\">\n");
printf("<div class=\"label_cd8\">");
printf("CD8<br/>");
printf("<input type=\"submit\" disabled name=\"cd8l\" value=\"%s\"> Low <br>\n", strpos($class0,'cd8l')!==false ? 'x':'  ');
printf("<input type=\"submit\" disabled name=\"cd8h\" value=\"%s\"> High <br>\n", strpos($class0,'cd8h')!==false ? 'x':'  ');
printf("</div>");

printf("<br>\n");
printf("<div class=\"label_cd16\">");
printf("CD16<br/>");
printf("<input type=\"submit\" disabled name=\"cd16l\" value=\"%s\"> Low <br>\n", strpos($class0,'cd16l')!==false ? 'x':'  ');
printf("<input type=\"submit\" disabled name=\"cd16h\" value=\"%s\"> High <br>\n", strpos($class0,'cd16h')!==false ? 'x':'  ');
printf("</div>");

#printf("<br>\n");
#printf("<div class=\"label_frame\">\n");
#printf("<input type=\"button\" id=\"toggle_cd16_%s\" value=\"CD16\" onclick=\"myFunction(%s)\" >\n", $im_id, $im_id);
#printf("</div>\n");

#printf("<div class=\"score\">\n");
#printf("<p>cd16 area <br>=%s %%</p>", $score);
#printf("</div>\n");

printf("<br>\n");
printf("</div>"); # label_frame

#printf("<div class=\"label_frame\">\n");
#printf("<input type=\"submit\" name=\"clr\" value=\"  \"> Clear Label\n");
#printf("</div>"); # label_frame
#printf("</form>\n");
#printf("</div>\n");


printf("<div id=\"img_%s\" class=\"img_frame\">\n", $im_id);
printf("<img height=200px src=\"%s/%d.png\"/>\n", $folder, $im_id);
printf("</div>\n");

#printf("<div id=\"img_cd16_%s\" class=\"img_frame_cd16\">\n", $im_id);
#printf("<img height=200px src=\"%s\"/>\n", $cd16_file);
#printf("</div>\n");

printf("</section>\n\n");
}
printf("<section class=\"footer1\">\n");
printf("<a href=view_pred_multiplex.php?page=%d>Prev Page</a>\n", $page-1);
printf("<a href=view_pred_multiplex.php?page=%d>Next Page</a>\n", $page+1);
printf("</section>\n");
printf("</section>\n");
?>



</body>
</html>
