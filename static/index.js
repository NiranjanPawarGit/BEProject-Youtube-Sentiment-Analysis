var videoid = [];
var videotitle = [];
var videothumbnails = [];
var videolink = [];
window.onload = function (){
$.get(
    "https://www.googleapis.com/youtube/v3/videos",{
        part:'snippet',
        chart:'mostPopular',
        maxResults: 50,
        key : 'AIzaSyDdLpCjSPAShuLZMbLW78fsUCJHK6ag9rE',
        },
        function (data) {
            $.each(data.items,function(i, item){

                // console.log(item);
                thumbnail = item.snippet.thumbnails.standard.url;
                title = item.snippet.title;
                id = item.id;
                link = "https://www.youtube.com/watch?v="+id;
                videoid.push(id);
                videotitle.push(title);
                videothumbnails.push(thumbnail);
                videolink.push(link);

                // console.log(link);
                // console.log(title);
                // console.log(thumbnail);
                document.getElementById("image").style.backgroundImage = "url('" + videothumbnails[0] + "')";
                document.getElementById("bottom").href = videolink[0];
                document.getElementById("videodetails").innerHTML = " Currently trending #1 &ensp; &raquo; &ensp; "+ videotitle[0];

                var ik = 1;
                var imageHead = document.getElementById("image");
                // console.log(videothumbnails[0]);
                setInterval(function() {
                      imageHead.style.backgroundImage = "url(" + videothumbnails[i] + ")";
                      document.getElementById("image").style.backgroundImage = "url('" + videothumbnails[i] + "')";
                    document.getElementById("bottom").href = videolink[i];
                    document.getElementById("videodetails").innerHTML = " Currently trending #" + (i+1) + "&ensp; &raquo; &ensp; " + videotitle[i];
                      i = i + 1;
                      if (i == videothumbnails.length) {
                        i =  0;
                     }
                }, 10000);
                            });

    }
);
};

