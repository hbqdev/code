#!/usr/bin/perl

$cnt = 2;
$item_cnt = 0;
while ($#ARGV > 1) {
  open FILE, ">$cnt.html";

  foreach $x (0 .. 49) {

    $thumb = pop @ARGV;
    if ($thumb =~ /(K[0-9]+).jpg/) {
      $kid = $1;
      print "$kid\n";
      # put in a maker so we know about where we are.
#       if ($item_cnt++ % 10 == 0) {
# 	print FILE <<EOL;
# <div class="box col2">
#       <h3>$kid</h3>
# </div>
# EOL
#      }

      $nail = $thumb;
      $nail =~ s/\.jpg/\.thumb\.jpg/;
      `convert -resize 128x96 $thumb $nail`;

      print FILE <<EOL;
<div class="box col2">
        <a href="index.htm" onclick="return hs.htmlExpand(this, { headingText: '$kid' })">
        <img src="content/thumbs/$kid.thumb.jpg" title="$kid"></a>
        <div class="highslide-maincontent">
            <img src="content/thumbs/$kid.jpg">
            $kid<br>
EOL
#https://sandbox.google.com/storage/katamari-2d-test/20120113-11s0200-1-K0000000041-2d.tar
#http://gfsviewer/cns/vb-d/home/katamari/objects-raw/20120330-15s5756-1-K0000001311-2d/2d_tn.jpg

      my $twod = 0;
      my $threed = 0;

      foreach $tarball (split "\n", `gsutil ls gs://katamari-2d-test/*$kid*` ) {
	$http_path = $tarball;
	$http_path =~ s/gs\:\/\//https\:\/\/sandbox\.google\.com\/storage\//;
	print FILE "<a href='$http_path'>$tarball</a><br>";
      }

      print FILE "<hr>The following content is available on colossus ...<br>";
      print FILE "<pre>";
      foreach $line (split "\n", `fileutil ls /cns/vb-d/home/katamari/objects-raw/*$kid*` ) {
	$threed += 1 if ($line =~ /3d/);
	$twod += 1 if ($line =~ /2d/);
	chomp $line;
	print FILE "<a href=\"http://gfsviewer$line\" target=\"_blank\">$line</a><br>";
      }
      print FILE "</pre></div>";
      print FILE "<b>$kid</b>";
      print FILE "<twod>2D</twod>" if $twod > 0;
      print FILE "<threed>3D</threed>" if $threed > 0;
      print FILE "</div>";

    }
    else {
      
    }
  }

  close FILE;
  $cnt++;
}
