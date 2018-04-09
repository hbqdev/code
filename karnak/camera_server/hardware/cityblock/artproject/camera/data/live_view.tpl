<!DOCTYPE html>
<html>
  <head>
    <title>Live View</title>
    <style>
      #live-view-box {
        border:5px solid #000;
        height:{{af_point_height:none}}px;
        left:50%;
        margin-top:{{af_point_height_offset:none}}px;
        margin-{{START_EDGE:none}}:{{af_point_width_offset:none}}px;
        position:absolute;
        top:50%;
        width:{{af_point_width:none}}px;
      }

      #live-view-wrapper {
        margin:0 auto;
        position:relative;
        width:{{width:none}}px;
      }
    </style>
  </head>
  <body>
    <div id="live-view-wrapper">
      <img src="{{stream_url:none}}" width="{{width:none}}px"
       height="{{height:none}}px" alt="">
      <div id="live-view-box">
      </div>
    </div>
  </body>
</html>
