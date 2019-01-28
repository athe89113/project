//power by baiyukey@qq.com
//version:0.0.4
//设置一个切角背景
;(function($){
  $.fn.extend({
    "setBackground":function(_val){
      var val=$.extend({
        'fill':'rgba(21,39,68,0.6)',
        'borderColor':'#05607F',
        'borderWidth':1,
        'cutLeftTop':10,
        'cutLeftBottom':3,
        'cutRightTop':3,
        'cutRightBottom':10,
        'cut':'',//切角简写,例如"20 10 10 15",分别代表cutLeftTop,cutLeftBottom,cutRightTop,cutRightBottom
        'talkBubble':{},
        'callback':null
      },_val);
      val.talkBubble=$.extend({
        "angle":0,//角度
        "distance":0,//距离
        "beginWidth":20//喇叭口宽度
      },val.talkBubble);
      if(val.cut!=''){
        var cut=val.cut.split(" ");
        val.cutLeftTop=cut[0]||val.cutLeftTop;
        val.cutRightTop=cut[1]||val.cutRightTop;
        val.cutRightBottom=cut[2]||val.cutRightBottom;
        val.cutLeftBottom=cut[3]||val.cutLeftBottom;
        val.cutLeftTop=Number(val.cutLeftTop);
        val.cutRightTop=Number(val.cutRightTop);
        val.cutRightBottom=Number(val.cutRightBottom);
        val.cutLeftBottom=Number(val.cutLeftBottom);
      }
      var thisLength=$(this).length;
      var talkBubbleDirection=function(_width,_height,_angle){
        var sectionUnit=[0,0];
        sectionUnit[0]=Math.atan2(_width,_height)/Math.PI/2*360;//二维坐标点离原点的角度
        sectionUnit[1]=90-sectionUnit[0];
        var range={
          "top":[],
          "right":[],
          "bottom":[],
          "left":[]
        };
        range.top=[360-sectionUnit[0],sectionUnit[0]];
        range.right=[90-sectionUnit[1],90+sectionUnit[1]];
        range.bottom=[180-sectionUnit[0],180+sectionUnit[0]];
        range.left=[270-sectionUnit[1],270+sectionUnit[1]];
        var angle=Math.abs((_angle+360)%360);
        var direction=angle<=range.top[1]||angle>range.top[0] ? "top" : "unKnow";
        if(direction==="unKnow"){
          for(var k in range){
            if(angle>range[k][0]&&angle<=range[k][1]){
              direction=k;
              break;
            }
          }
        }
        return direction;
      };//返回尖角指向的位置,返回数值有top,right,bottom,left
      var rePath=function(_width,_height,_direction,_val){
        var thisPath=[];
        var adjacent=0;//邻边
        var angle=Math.abs((val.talkBubble.angle+360)%360);
        var subtense=function(_angle,_adjacent){
          return Math.tan(2*Math.PI/360*(Math.abs(_angle%90)))*_adjacent;
        };//返回对边长度
        var half=1;//边角在某边线的前半部分-1,后半部分为1
        var x1=0,x2=0,x3=0,y1=0,y2=0,y3=0;
        switch(_direction){
          case "top":
            adjacent=_height/2;
            half=angle>270 ? -1 : 1;
            x1=(_width/2)+subtense((angle>270 ? 360-angle : -angle),adjacent)*half-_val.talkBubble.beginWidth/2;
            x1=Math.max(x1,val.cutLeftTop);
            x2=(_width/2)+subtense((angle>270 ? 360-angle : -angle),adjacent+_val.talkBubble.distance)*half;
            x2=Math.max(0.5,x2);
            x2=Math.min(_width+val.talkBubble.distance-0.5,x2);
            x3=x1+_val.talkBubble.beginWidth;
            x3=Math.min(x3,(_width-val.cutRightTop));
            x1=x3-_val.talkBubble.beginWidth;
            thisPath.push(x1+","+(_val.talkBubble.distance+0.5));
            thisPath.push(x2+","+0.5);
            thisPath.push(x3+","+(_val.talkBubble.distance+0.5));
            break;
          case "right":
            adjacent=_width/2;
            half=angle>90 ? 1 : -1;
            y1=(_height/2)+subtense((angle<90 ? 90-angle : -angle),adjacent)*half-_val.talkBubble.beginWidth/2;
            y1=Math.max(y1,val.cutRightTop);
            y2=(_height/2)+subtense((angle<90 ? 90-angle : -angle),adjacent+_val.talkBubble.distance)*half;
            y2=Math.max(0.5,y2);
            y2=Math.min(_height+val.talkBubble.distance,y2);
            y3=y1+_val.talkBubble.beginWidth;
            y3=Math.min(y3,_height-val.cutRightBottom);
            y1=y3-_val.talkBubble.beginWidth;
            thisPath.push((_width-0.5)+","+y1);
            thisPath.push((_width-0.5+_val.talkBubble.distance+0.5)+","+y2);
            thisPath.push((_width-0.5)+","+y3);
            break;
          case "bottom":
            adjacent=_height/2;
            half=angle>180 ? -1 : 1;
            x1=(_width/2)+subtense((angle<180 ? 180-angle : angle),adjacent)*half+_val.talkBubble.beginWidth/2;
            x1=Math.min(x1,(_width-val.cutLeftBottom));
            x2=(_width/2)+subtense((angle<180 ? 180-angle : -angle),adjacent+_val.talkBubble.distance)*half;
            x2=Math.max(0.5,x2);
            x2=Math.min(_width+val.talkBubble.distance-0.5,x2);
            x3=x1-_val.talkBubble.beginWidth;
            x3=Math.max(x3,val.cutLeftBottom);
            x1=x3+_val.talkBubble.beginWidth;
            thisPath.push(x1+","+(_height-0.5));
            thisPath.push(x2+","+(_height+_val.talkBubble.distance-0.5));
            thisPath.push(x3+","+(_height-0.5));
            break;
          case "left":
            adjacent=_width/2;
            half=angle>270 ? -1 : 1;
            y1=(_height/2)+subtense((angle<270 ? 270-angle : -angle),adjacent)*half+_val.talkBubble.beginWidth/2;
            y1=Math.min(y1,(_height-val.cutLeftBottom));
            y2=(_height/2)+subtense((angle<270 ? 270-angle : -angle),adjacent+_val.talkBubble.distance)*half;
            y2=Math.max(0.5,y2);
            y2=Math.min(_height+val.talkBubble.distance,y2);
            y3=y1-_val.talkBubble.beginWidth;
            y3=Math.max(y3,val.cutLeftTop);
            y1=y3+_val.talkBubble.beginWidth;
            thisPath.push((val.talkBubble.distance+0.5)+","+y1);
            thisPath.push(0.5+","+y2);
            thisPath.push((val.talkBubble.distance+0.5)+","+y3);
            break;
          default:
            break;
        }
        return thisPath.join(" ");
      };
      $(this).each(function(i,e){
        var $this=$(e);
        var thisWidth=$this.outerWidth();
        var thisHeight=$this.outerHeight();
        var thisTalkBubbleDirection=talkBubbleDirection(thisWidth,thisHeight,val.talkBubble.angle);
        var thisTalkIndicate,top,left;
        if(val.talkBubble.distance!==0){
          thisTalkIndicate=rePath(thisWidth,thisHeight,thisTalkBubbleDirection,val);
          if(thisTalkBubbleDirection==="top"){
            top=val.talkBubble.distance;
            left=0;
          }
          else if(thisTalkBubbleDirection==="left"){
            top=0;
            left=val.talkBubble.distance;
          }
          else{
            top=0;
            left=0;
          }
        }
        else{
          thisTalkIndicate='';
          top=0;
          left=0;
        }
        var svgStyle='position:absolute;width:'+(thisWidth+val.talkBubble.distance)+'px;height:'+(thisHeight+val.talkBubble.distance)+'px;z-index:0;left:'+(0-left)+'px;top:'+(0-top)+'px;';
        var thisAnchor=[];
        thisAnchor.push((val.cutLeftTop+left)+","+((val.borderWidth/2)+top));
        if(thisTalkBubbleDirection==="top"&&val.talkBubble.distance!==0) thisAnchor.push(thisTalkIndicate);
        thisAnchor.push(($this.outerWidth()-val.cutRightTop+left)+","+((val.borderWidth/2)+top));
        thisAnchor.push(($this.outerWidth()-(val.borderWidth/2)+left)+","+(val.cutRightTop+top));
        if(thisTalkBubbleDirection==="right"&&val.talkBubble.distance!==0) thisAnchor.push(thisTalkIndicate);
        thisAnchor.push(($this.outerWidth()-(val.borderWidth/2)+left)+","+(($this.outerHeight()-val.cutRightBottom)+top));
        thisAnchor.push(($this.outerWidth()-val.cutRightBottom+left)+","+($this.outerHeight()-val.borderWidth/2+top));
        if(thisTalkBubbleDirection==="bottom"&&val.talkBubble.distance!==0) thisAnchor.push(thisTalkIndicate);
        thisAnchor.push((val.cutLeftBottom+left)+","+($this.outerHeight()-val.borderWidth/2+top));
        thisAnchor.push((val.borderWidth/2+left)+","+($this.outerHeight()-val.cutLeftBottom+top));
        if(thisTalkBubbleDirection==="left"&&val.talkBubble.distance!==0) thisAnchor.push(thisTalkIndicate);
        thisAnchor.push((val.borderWidth/2+left)+","+(val.cutLeftTop+top));
        var thisHtml='<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" version="1.1" style="'+svgStyle+'" class="setBackground"><polygon points="'+thisAnchor.join(" ")+'" style="fill:'+val.fill+'; stroke:'+val.borderColor+';stroke-width:'+val.borderWidth+'"/></svg>';
        if($this.attr("data-setBackground")==="true"){
          $this.find("svg.setBackground").attr("style",svgStyle);
          $this.find("svg.setBackground polygon").eq(0).attr("points",thisAnchor.join(" ")).attr("style",('fill:'+val.fill+'; stroke:'+val.borderColor+';stroke-width:'+val.borderWidth));
        }
        else{
          $this.attr("data-setBackground","true").css({"position":"relative"}).prepend(thisHtml);
        }
        if(i===(thisLength-1)&&val.callback!=null) val.callback.call(this);
      });
      return this.each(function(){});
    }
  });
})(jQuery);