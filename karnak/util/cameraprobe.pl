#!/usr/bin/perl

use File::Basename;

%keys = ();
%values = ();
# @ports =  ( "002,003", "002,004", "002,005");
@ports =  ();

print "reading yaml file\n";
# - type: ArtProjectCamera
#   guid: 7beb069
#   server_url: localhost:8092

open YAML, "<$ARGV[0]";
@cameras = ();
$cam_info = {};
foreach $line (<YAML>) {
  if ($line =~ /\-\s+type:/) {
    if (exists  $cam_info->{'camera'}) {
	push @cameras, $cam_info;
    }
    $cam_info = {};
    if ($line =~ /ArtProjectCamera/) {
      $cam_info->{'camera'} = "ArtProjectCamera";
    }
  } 
  if ($line =~ /guid: ([0-9A-Za-z]+)/) {
      $cam_info->{'guid'} = $1;
  }
  if ($line =~ /server_url: ([0-9A-Za-z:]+)/) {
      my ($server, $port) = split ":", $1;
      $cam_info->{'server'} = $server;
      $cam_info->{'port'} = $port;
  }
}
close YAML;

foreach $h (@cameras) {
 print keys %{$h};
}

for $cam (split /\n/, `gphoto2 --auto-detect`) {
   if ($cam =~ /usb:([0-9,]+)/) {
	my $port = $1;
	unshift @ports, $port;
   }
}

open STARTER, ">util/start_camera_server.sh" or die "couldnt open output file";
print STARTER <<EOL;
# This is a generated file, DO NOT EDIT.
base="./camera_server --alsologtostderr --gid="" --uid=""  --camera_settings_filename="./artproject_config.json" --bodies_json_filename="./bodies.json" --lenses_json_filename="./lenses.json""
topbase="./camera_server --alsologtostderr --gid="" --uid=""  --camera_settings_filename="./artproject_config_top.json" --bodies_json_filename="./bodies.json" --lenses_json_filename="./lenses.json""

cd ~/scanning-ops/karnak/camera_server/
EOL

for $port ( @ports ) {
 print "probing camera at $port ";
 for $val ( split /\n/, `gphoto2 --port usb:$port --list-config` ) {
	$cmd = "gphoto2 --port usb:$port --get-config $val | grep Current";
	$result = `$cmd`;
	print ".";
	if ($result =~ /Current: ([a-zA-Z0-9_\.\-,\/\ %]*)\n$/ ) {
	  my $x = ($1);
	  $values{$port}{$val} = $x;	
	}
	$keys{$val} = 1;
 }
 $serial = `gphoto2 --port usb:$port --summary | grep Serial`;
 if ($serial =~ /Serial Number: ([a-zA-Z0-9]+)/) {
   my $sn = $1;
   $values{$port}{'real_serial'} = $sn;
   $keys{'real_serial'} = 1;
   # hack, but does the trick :)
   `gphoto2 --port usb:$port --set-config /main/settings/ownername=$sn`;
   for $camera (@cameras) {
     if ($camera->{'guid'} eq $sn) {
        ($pt = $port) =~ s/,/:/g;
	if (${$camera}{'port'} == 8092) {
         print STARTER "\$topbase -port ".${$camera}{'port'}." -device_location $pt &\n";
        }
	else {
         print STARTER "\$base -port ".${$camera}{'port'}." -device_location $pt &\n";
        }
     }
   }
 }
 print "\n";
}
close STARTER;

open FILE, ">$ARGV[1]";
print FILE <<"EOL"
<head>
<style type="text/css">
tr:nth-child(even) {
  background-color: lightgrey;
}

tr:nth-child(odd) {
  background-color: white;
}
</style>
</head>
<html>
EOL
; 

print FILE "<table>"; 
print FILE "<tr><td></td>";
for $port (@ports) { 
   @d = split /,/, $port;
   if ($d[1] < 3 || $d[1] > 5 ) {
	$font = "color=red";
   }
   else {
	$font = "";
   }
   print FILE "<td><font $font><b>$port</b></font></td>";
}
print FILE "</tr>";
for $key ( reverse sort keys %keys) {
	$k = basename ($key);
	print FILE "<tr><td>$k</td>";	
	for $port ( @ports ) {
	 print FILE "<td>";
	 if ($key =~ /shuttercounter/ && $values{$port}{$key} > 250000) {

	   $font = "color=red";
	   print "SHUTTER COUNT OVER THRESHOLD OF 250000\n"
	 }
	 elsif ($key =~ /lensname/ && $values{$port}{$key} ne "") {
	   $font = "color=red";
	   print "LENS ERROR DETECTED LENS ERROR DETECTED LENS ERROR DETECTED\n"
	 }
	# elsif ($key =~ /aperture/ && $values{$port}{$key} ne "") {
	 #  $font = "color=red";

	  # $font = "color=red";
	  # print "SHUTTER COUNT OVER THRESHOLD OF 250000\n"
	# }
	 elsif ($key =~ /lensname/ && $values{$port}{$key} ne "") {
	   $font = "color=red";
	   print "LENS ERROR DETECTED LENS ERROR DETECTED LENS ERROR DETECTED\n"
	 }
	 elsif ($key =~ /aperture/ && $values{$port}{$key} ne "") {
	   $font = "color=red";

	   print "BAD APERTURE BAD APERTURE BAD APERTURE\n"
	 }
	 else {
	   $font = "";
	 }	
	 print FILE "<font $font><pre>$values{$port}{$key}</pre></font>";
	 
	 print FILE "</td>";
	} 
	print FILE "</tr>";
}
print FILE "</table>";
close FILE;
