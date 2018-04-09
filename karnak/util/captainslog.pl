#!/usr/bin/perl

# Simple script to scrub the current logs on each rig for detailed info.
# TODO(katamari-tech): extend to include reports over weeks/months/years.

use Time::Piece;

$debug = 0;

# TODO(arshan): Should these just be cmd line args?
@rigs = (
"172.17.26.1",
"172.17.26.2",
"172.17.26.3",
"172.17.26.4",
"172.17.26.5",
"172.17.26.6",
"172.17.26.7",
"172.17.26.8",
"172.17.26.9",
# "172.17.26.51"
);


%summary = ();

#foreach $day (19..31){
#  scrubLogs("log.txt.2012_10_$day");
#}
#foreach $day (1..4){
#  scrubLogs("log.txt.2012_11_$day");
#} 

scrubLogs("log.txt.2013_3_4");

for $key (sort keys %summary) {
  print "$key : " . join (", ", @{$summary{$key}}). "\n"; 
}

sub scrubLogs {

  my ($logfile) = @_;
  
  $current = -1;
  $previews = 0;
  %scans = ();
  %cancelled = ();
  
  %start = ();
  %end   = ();

  # Get the log file and populate the datastructure.
  for $rig (@rigs) {
    print "checking $rig\n";
    $lfile = "$rig.log.txt";
    `wget $rig:8080/logs/$logfile -O $lfile`;
    if (-e $lfile) {
      $scans{$rig} = [];
      $cancelled{$rig} = [];
      $start{$rig} = 0; 
      unlog($lfile, $rig);
    } 
    else {
      print "couldnt get the log file $logfile from $rig\n";
    }
  }
  
  
  # Move this into a function and clean the script up, maybe python it?
  $global_total = 0;
  $global_cancelled = 0;
  
  foreach $key (sort keys %scans) {
    
    $avg_scantime = 0;
    $avg_downtime = 0;
    $last = undef;
    for $scan ( @{$scans{$key}} ) {
      # vprint "Scan : \n";
      if (defined $last) {
	$downtime = $scan->[1][1] - $last->[2][1];
	# Filter the noise of down time > 30min
	$avg_downtime += $downtime if $downtime < 60*30 && $downtime > 0;
      }
      $avg = $scan->[2][1] - $scan->[1][1];
      $avg_scantime += $avg;
      $last = $scan;
    }
    
    
    $total_scans = $#{$scans{$key}} + 1;
    $total_cancelled = $#{$cancelled{$key}} + 1;
    if ($total_scans > 0) {
      $avg_scantime /= $total_scans;
    }
    if ($total_scans > 1) {
      $avg_downtime /= ($total_scans - 1);
    }
    
    $global_total += $total_scans;
    $global_cancelled += $total_cancelled;
    
    print "---- \n";
    print "Summary : $key \n";
    print " from : $start{$key}\n";
    print " to   : $end{$key}\n";
    print " average scan time : ". $avg_scantime/60 . "\n";
    print " average down time : ". $avg_downtime/60 . "\n";
    print " total completed: $total_scans\n";
    print " total cancelled: $total_cancelled\n";
  }


  $summary{$logfile} = [$global_total, 
			$global_cancelled ];

  print " ======\n";
  print " TOTALS: \n";
  print " Scans - $global_total\n";
  print " Cancelled - $global_cancelled\n";
}

# Debug print routine, easy place to make it verbos-er.
sub vprint {
  my ($msg) = @_;
  if ($debug) {
    print $msg;
  }
}

sub unlog {
  my $filename = $_[0];
  my $key      = $_[1];
  print "checking $filename\n";
  open LOGFILE, "<$filename";
  for $line (<LOGFILE>) {
  # 2012-10-21 00:02:27-0700
  if ($line =~ /^([0-9]+)\-([0-9]+)\-([0-9]+)\ ([0-9]+):([0-9]+):([0-9]+)/) {
    my ($year, $month, $day, $hour, $minute, $second) = ($1,$2,$3,$4,$5,$6);

    $tag = "$year/$month/$day $hour:$minute:$second";
    $tpiece = Time::Piece->strptime($tag, "%Y/%m/%d %H:%M:%S");
    $epoch = $tpiece->epoch;
 
    if ($start{$key} == 0) { $start{$key} = $tpiece; }
    $end{$key} = $tpiece;

    if ($line =~ /([0-9]+\-[0-9ds]+\-sbs[0-9]+\-K\-[a-zA-Z0-9]+\-2d)/) {
        $fullname = $1;
    }

    if ($line =~ /katamari_id=([a-zA-Z0-9]+)/) {
	$ksid = $1;
    }


    if ($line =~ /operator_id=([a-zA-Z0-9]+)/) {
	$operator = $1;
    }	

    # TODO(katamari-tech): Should support an admin mode, for machine state change.
    if ($line =~ /BroadcastServerFactory starting on 9000/) {
	vprint "$tag > server restart\n";
    }   

    if ($line =~ /configure for capture of type : swivel/) {

	if ( $#{$current} > 0 ) {
	  push @{$cancelled{$key}}, $current;
	  vprint "$tag > scan cancelled\n";
	}
	
	vprint "$tag > start scan [$ksid/$operator]\n";

	$current = [];
	push @{$current}, ["previews", $previews];
	$previews = 0;
	push @{$current}, ["start", $epoch];
    }

    if ($line =~ /uploading to config/) {
        vprint "$tag > scan finish\n";
	push @{$current}, ["finish", $epoch];
    }

    if ($line =~ /upload complete/) {
	
	if ($#{$current} != 2) {
	  vprint "skipping scan\n";	
	}
	else {
	  vprint "$tag > upload complete\n";
	  push @{$current}, ["complete", $epoch];
	  push @{$scans{$key}} , $current;
	}
	$current = [];
    }

    if ($line =~ /capturing to static\/preview/) {
        vprint "$tag > preview\n";
	$previews += 1;
    }
  }
}
close LOGFILE;  
}

