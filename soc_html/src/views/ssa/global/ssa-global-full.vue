<template>
  <div class="global-full">
    <div class="global-title">
      <p class="font22 textC head">态势感知平台</p>
      <p class="info textC"><span>全局态势</span></p>
    </div>
    <div class="global-logo"></div>
    <div class="global-time">
      <span><i class="ys-icon icon-clock ys-success-color m-r-5"></i><span class="d-i-b p-r-5">{{curDate}}</span><span class="d-i-b p-r-5">{{curWeek}}</span><span class="d-i-b p-r-5">{{curTime}}</span></span>
      <button class="m-l-15" @click="closeFullPage()">关闭</button>
    </div>
    <div class="global-left">
      <div class="safe-grade-box">
        <div class="safe-grade-box-bg"></div>
        <div class="safe-grade-box-point" id="safe-grade-box-point">
          <div class="light"></div>
        </div>
        <div class="title ys-info-color">安全评分</div>
        <div class="value font36" style="font-family: digi">{{securityGrade}}</div>
      </div>
      <div class="composite-state-box">
        <div id="composite-state-bg"></div>
        <div id="composite-state"></div>
        <div id="composite-state-tag"><span>评分体系</span></div>
      </div>
      <div class="global-hole-tab-box">
        <div class="title">
          <span class="a">漏洞总数</span>
        </div>
        <div class="content">
          <div>
            <p><span class="ys-info-color">漏洞总数：</span><span class="ys-error-color">{{holeCountData.hole_count}}</span><span class="m-l-20"><i class="ys-icon" v-bind:class="[holeCountData.hole_ratio>0 ? 'icon-num-arrow-up ys-error-color' : 'icon-num-arrow-down ys-success-color' ]"></i>{{Math.abs(holeCountData.hole_ratio)}}%</span></p>
            <div class="clearfix">
              <div class="col-md-4">
                <div class="hole-rate-box" id="hole-rate-box"></div>
                <p class="ys-info-color m-t-10 textC">高危漏洞占比</p>
              </div>
              <div class="col-md-4">
                <div class="danger-hole-box">
                  <div class="text">{{holeCountData.severe}}</div>
                </div>
                <p class="ys-info-color m-t-10 textC">高危漏洞数</p>
              </div>
              <div class="col-md-4">
                <div class="danger-hole-box danger-hole-asset-box">
                  <div class="text">{{holeCountData.hole_ip_count}}</div>
                </div>
                <p class="ys-info-color m-t-10 textC">漏洞资产数</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="global-map-title">
      <span style="padding-left:22px;">全网态势状态</span>
      <span style="padding-left:20px;">目前安全态势：</span>
      <span style="color:#e96157"><i class="ys-icon icon-warning-three m-r-5"></i>存在风险</span>
      <span class="m-l-10">目前业务态势：</span>
      <span>正常</span>
    </div>
    <div class="global-map">
      <div id="global-map-chart"></div>
    </div>
    <div class="global-bottom clearfix">
      <div class="global-bottom-table">
        <div class="global-bottom-cell">
          <div class="global-auto-box">
            <div class="global-auto-box-left"></div>
            <div class="global-auto-box-right"></div>
            <div class="global-auto-box-middle"></div>
            <div class="global-auto-box-inner">
              <div class="title">最新重大漏洞TOP5</div>
              <div class="content">
                <div class="big-hole-top5-box">
                  <ul class="p-l-20">
                    <li v-for="list in bigHoleTop5Data">
                      <p class="top-title">TOP{{$index+1}}</p>
                      <p class="des">
                        <span class="text-over d-i-b verticalM" style="width:200px">{{list.name}}</span>
                        <span class="m-l-10 verticalM">漏洞资产：</span>
                        <span class="verticalM">{{list.assets}}</span>
                      </p>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="global-bottom-cell m-r-10" style="width:1044px;">
          <div class="global-box global-box-1 fLeft d-i-b m-l-10">
            <div class="title">攻击次数</div>
            <div class="content attck-time-box">
              <p class="text p-l-10"><span class="ys-info-color">攻击次数：</span><span class="ys-error-color">{{attackTotalNum}}</span><span class="m-l-10"><i class="ys-icon" v-bind:class="[attackChangeNum>0 ? 'icon-num-arrow-up ys-error-color' : 'icon-num-arrow-down ys-success-color' ]"></i>{{Math.abs(attackChangeNum)}}%</span></p>
              <div class="attck-time-bg"></div>
              <div id="ssa-attack-time" class="attck-time-rate"></div>
            </div>
          </div>
          <div class="global-box global-box-1 fLeft d-i-b m-l-10">
            <div class="title">攻击来源</div>
            <div class="content attck-source-box">
              <p class="text p-l-10"><span class="ys-info-color">来源地区top5</span></p>
              <div id="ssa-source-chart" class="attck-source-chart"></div>
            </div>
          </div>
          <div class="global-box global-box-1 fLeft d-i-b m-l-10">
            <div class="title">蠕虫感染总数</div>
            <div class="content worm-infect-box">
              <p class="text p-l-10"><span class="ys-info-color">感染总数：</span><span class="ys-error-color">{{infectTotalNum}}</span><span class="m-l-10"><i class="ys-icon" v-bind:class="[infectChangeNum>0 ? 'icon-num-arrow-up ys-error-color' : 'icon-num-arrow-down ys-success-color' ]"></i>{{Math.abs(infectChangeNum)}}%</span></p>
              <div class="worm-infect-bg"></div>
              <div id="worm-infect-chart" class="worm-infect-chart"></div>
            </div>
          </div>
        </div>
        <div class="global-bottom-cell">
          <div class="global-auto-box">
            <div class="global-auto-box-left"></div>
            <div class="global-auto-box-right"></div>
            <div class="global-auto-box-middle"></div>
            <div class="global-auto-box-inner">
              <div class="title">实时攻击信息</div>
              <div class="content">
                <table class="attack-info-table">
                  <thead>
                  <tr>
                    <th>时间</th>
                    <th>目标IP</th>
                    <th>位置</th>
                    <th>严重级别</th>
                    <th>源IP</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="list in attackInfoRealData" :class="tableColor(1)">
                    <td>{{list.time}}</td>
                    <td>{{list.dst_ip}}</td>
                    <td>{{list.src_ip_location}}</td>
                    <td>{{list.level}}</td>
                    <td>{{list.src_ip}}</td>
                  </tr>
                  <tr v-for="list in 5" v-show="attackInfoRealData.length==0">
                    <td style="height:32px;"> </td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="global-right">
      <div class="global-box global-trend-box">
        <div class="title">全网态势发展趋势</div>
        <div class="content">
          <div id="whole-net-ssa-trend" style="width:300px;height:170px;"></div>
        </div>
      </div>
      <div class="attack-detail-box">
        <div class="attack-detail-wrap clearfix">
          <div class="attack-detail-con host">
            <div class="tag">主机层</div>
            <div class="attack-detail-module">
              <p class="head" style="padding-left:80px;">漏洞扫描</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-scan.png" style="width:64px;"/></p>
              <p class="num"><span style="font-family: digi">{{serverData.hole.count | range}}</span>个漏洞</p>
            </div>
            <div class="attack-detail-module">
              <p class="head">防病毒</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-virus.png" style="width:64px;"/></p>
              <p class="num"><span style="font-family: digi">{{serverData.viruses.count | range}}</span>个病毒感染</p>
            </div>
            <div class="attack-detail-module" style="width:110px">
              <p class="head">弱口令</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-weak.png" style="width:51px;"/></p>
              <p class="num"><span style="font-family: digi">{{serverData.weak_password.count | range}}</span>台主机</p>
            </div>
          </div>
        </div>
        <div class="attack-detail-wrap clearfix">
          <div class="attack-detail-con app">
            <div class="tag">应用层</div>
            <div class="attack-detail-module">
              <p class="head" style="padding-left:80px;">WAF</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-waf.png" style="width:64px;"/></p>
              <p class="num"><span style="font-family: digi">{{appData.waf.count | range}}</span>次攻击</p>
            </div>
            <div class="attack-detail-module">
              <p class="head">漏洞</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-hole.png" style="width:64px;"/></p>
              <p class="num"><span style="font-family: digi">{{appData.hole.count | range}}</span>个漏洞</p>
            </div>
            <div class="attack-detail-module" style="width:110px">
              <p class="head">数据库审计</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-database.png" style="width:51px;"/></p>
              <p class="num"><span style="font-family: digi">{{appData.database.count | range}}</span>次攻击</p>
            </div>
          </div>
        </div>
        <div class="attack-detail-wrap clearfix">
          <div class="attack-detail-con net">
            <div class="tag">网络层</div>
            <div class="attack-detail-module">
              <p class="head" style="padding-left:80px;">网络出口</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-net.png" style="width:64px;"/></p>
              <p class="num"><span style="font-family: digi">{{networkData.export.count | changeBand}}</span>{{networkData.export.count | changeUnit}}</p>
            </div>
            <div class="attack-detail-module">
              <p class="head">IDS</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-ids.png" style="width:64px;"/></p>
              <p class="num"><span style="font-family: digi">{{networkData.ids.count | range}}</span>次攻击</p>
            </div>
            <div class="attack-detail-module" style="width:110px">
              <p class="head">防火墙</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-firewall.png" style="width:53px;"/></p>
              <p class="num"><span style="font-family: digi">{{networkData.firewall.count | range}}</span>次拦截</p>
            </div>
            <div class="attack-detail-module" style="width:110px">
              <p class="head">抗DDoS</p>
              <p class="icon"><img src="../../../assets/images/ssa/detail-icon-ddos.png" style="width:61px;"/></p>
              <p class="num"><span style="font-family: digi">{{networkData.ddos.count | changeBand}}</span>{{networkData.export.count | changeUnit}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .global-bottom-table{
    display: table;
    width:100%;
  }
  .global-bottom-cell{
    display: table-cell;
  }
  .global-auto-box{
    width:100%;
    height:280px;
    position:relative;
  }
  .global-auto-box-left{
    float: left;
    width:224px;
    height:280px;
    background: url("../../../assets/images/ssa/global-box-bg-left.png");
  }
  .global-auto-box-middle{
    margin-left: 224px;
    margin-right: 14px;
    height:280px;
    background: url("../../../assets/images/ssa/global-box-bg-middle.png") repeat-x;
  }
  .global-auto-box-right{
    float: right;
    width:14px;
    height:280px;
    background: url("../../../assets/images/ssa/global-box-bg-right.png");
  }
  .global-auto-box-inner{
    position: absolute;
    top:0px;
    left:0px;
    width:100%;
  }
  .global-auto-box-inner .title{
    height:38px;
    line-height:38px;
    padding-left:23px;
    border-bottom:1px solid rgba(60,150,255,0.65);
    margin-left:10px;
    margin-right:10px;
  }
  .global-auto-box-inner .content{
    padding:15px;
  }
  /*仪表盘*/
  .safe-grade-box{
    width:334px;
    height:190px;
    position:relative;
  }
  .safe-grade-box .title{
    width:334px;
    text-align:center;
    position:absolute;
    top:72px;
  }
  .safe-grade-box .value{
    width:334px;
    text-align:center;
    position:absolute;
    top:105px;
  }
  .safe-grade-box-bg{
    background: url("../../../assets/images/ssa/gauge-bg.png");
    background-size:220px;
    width:220px;
    height:172px;
    margin:0 auto;
  }
  .safe-grade-box-point{
    height: 146px;
    width: 146px;
    border-radius: 50%;
    position: absolute;
    top: 39px;
    left: 95px;
    transform: rotate(-90deg);
  }
  .safe-grade-box-point .light{
    height:4px;
    width:4px;
    position:absolute;
    background:#fff;
    border-radius:50%;
    top:10px;
    left:35px;
    box-shadow: 0 0 15px 5px rgba(0, 192, 255, 0.75);
  }
  @keyframes rond {
    0% {transform : rotate(-90deg);}
    100% {transform : rotate(180deg);}
  }
  @-webkit-keyframes rond {
    0%{-webkit-transform : rotate(-90deg);}
    100%{-webkit-transform : rotate(180deg);}
  }
  .global-full{
    width: 100%;
    height: 100%;
    background-image: url('../../../assets/images/ssa/global-bg.jpg');
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    position: relative;
  }
  .global-title{
    height:135px;
    width:100%;
    background-image: url('../../../assets/images/ssa/title-bg.png');
    background-position: center center;
    background-repeat: no-repeat;
  }
  .global-title .head{
    padding-top:17px;
    text-shadow: 0 0 15px #fff;
  }
  .global-title .info{
    margin-top:-30px;
  }
  .global-title .info span{
    display: inline-block;
    width:258px;
    height:128px;
    line-height:128px;
    color:#79eeff;
    background-image: url('../../../assets/images/ssa/top-title-bg.png');
  }
  .global-logo{
    position:absolute;
    width:195px;
    height:123px;
    left:0px;
    top:0px;
    background: url("../../../assets/images/ssa/logo-bg.png");
  }
  .global-map-title{
    width:441px;
    height:63px;
    line-height:63px;
    background: url("../../../assets/images/ssa/map-title-bg.png") no-repeat;
    background-size:441px;
    position:absolute;
    top:145px;
    left:50%;
    margin-left:-220px;
  }
  .global-time{
    position:absolute;
    right:13px;
    top:17px;
  }
  .global-time button{
    border:none;
    width:80px;
    height:34px;
    text-align: center;
    line-height: 34px;
    background: url("../../../assets/images/ssa/close-btn-bg.png");
  }
  .global-left{
    position: absolute;
    left:5px;
    bottom:300px;
  }
  .global-box .content{
    padding:15px;
    position: relative;
  }
  .global-box .content .chart{
    margin:0 auto;
  }
  .global-box.global-box-1{
    background: url("../../../assets/images/ssa/box-bg-1.png");
    width:334px;
    height:280px;
  }
  .global-box .title{
    height:38px;
    line-height:38px;
    padding-left:33px;
  }
  /*评分体系KDA*/
  .composite-state-box{
    width:334px;
    height:290px;
    position:relative;
  }
  #composite-state-bg{
    position:absolute;
    top:50px;
    left:69px;
    background: url("../../../assets/images/ssa/pie-chart-bg-2.png");
    background-size:202px;
    width:202px;
    height:198px;
  }
  #composite-state{
    position:absolute;
    top:0px;
    left:0px;
    width:340px;
    height:295px;
  }
  #composite-state-tag{
    position:absolute;
    top:3px;
    left:12px;
    background: url("../../../assets/images/ssa/grade-tag.png") no-repeat;
    background-size:99px;
    width:99px;
    height:67px;
    font-size:14px;
    padding-top:9px;
    padding-left:21px;
  }

  /*攻击次数*/
  .attck-time-box{
    position: relative;
  }
  .attck-time-bg{
    width:170px;
    height:170px;
    margin:10px auto;
    background: url("../../../assets/images/ssa/pie-chart-bg.png") no-repeat;
    background-size:170px;
  }
  .attck-time-rate{
    width:300px;
    height:300px;
    margin:0 auto;
    position: absolute;
    top:-21px;
    left:17px;
  }

  /*攻击资源*/
  .attck-source-box{
    position: relative;
  }
  .attck-source-chart{
    width:260px;
    height:180px;
    margin-left:20px;
  }
  /*蠕虫感染总数*/
  .worm-infect-box{
    position: relative;
  }
  .worm-infect-bg{
    width:170px;
    height:170px;
    margin:10px auto;
    background: url("../../../assets/images/ssa/pie-chart-bg.png") no-repeat;
    background-size:170px;
  }
  .worm-infect-chart{
    width:220px;
    height:220px;
    margin:0 auto;
    position: absolute;
    top:20px;
    left:54px;
  }
  .global-map{
    position:absolute;
    left:320px;
    right:350px;
    bottom:270px;
    top:80px;
  }
  .global-bottom{
    position: absolute;
    left:5px;
    bottom:0px;
    width:100%;
  }
  .global-right{
    position: absolute;
    right:0px;
    bottom:300px;
  }
  .global-trend-box{
    width:332px;
    height:210px;
    background: url("../../../assets/images/ssa/global-trend-box-bg.png") no-repeat;
    background-size:332px;
    float:right;
    margin-bottom:10px;
  }
  .attack-detail-wrap{
    width:529px;
  }
  .attack-detail-con{
    height:142px;
    display:inline-block;
    position:relative;
    float:right;
  }
  .attack-detail-con.host{
    width:401px;
    background: url("../../../assets/images/ssa/platform-bg-1.png") no-repeat;
    background-size:401px;
  }
  .attack-detail-con.app{
    width:465px;
    background: url("../../../assets/images/ssa/platform-bg-2.png") no-repeat;
    background-size:465px;
    margin-top:10px;
  }
  .attack-detail-con.net{
    width:529px;
    background: url("../../../assets/images/ssa/platform-bg-3.png") no-repeat;
    background-size:529px;
    margin-top:10px;
  }
  .attack-detail-con .tag{
    position:absolute;
    top:15px;
    left:-40px;
    background: url("../../../assets/images/ssa/grade-tag.png") no-repeat;
    background-size:99px;
    width:99px;
    height:67px;
    font-size:14px;
    padding-top:9px;
    text-align:center;
  }
  .attack-detail-module{
    width:130px;
    display:inline-block;
    float:left;
  }
  .attack-detail-module .head{
    padding-top:20px;
    text-align:center;
    padding-left:50px;
  }
  .attack-detail-module .icon{
    padding-top:4px;
    text-align:center;
    padding-left:25px;
    height:64px;
    line-height:64px;
  }
  .attack-detail-module .num{
    text-align:center;
  }
  .attack-detail-module .num span{
    font-size:24px;
    margin-right:3px;
  }
  .hole-rate-box{
    width:96px;
    height:96px;
  }
  .global-hole-tab-box{
    width:424px;
    height:210px;
    background: url("../../../assets/images/ssa/global-hole-tab-a.png") no-repeat;
    background-size:424px;
  }
  .global-hole-tab-box .title{
    height:38px;
    line-height:38px;
    padding-left:33px;
  }
  .global-hole-tab-box .content{
    padding:15px 40px;
  }
  .hole-rate-box{
    width:96px;
    height:96px;
    background: url("../../../assets/images/ssa/hole-rate-bg.png") no-repeat;
    background-size:96px;
  }
  .danger-hole-box{
    width:96px;
    height:96px;
    background: url("../../../assets/images/ssa/hole-num-bg.png") no-repeat;
    background-size:96px;
  }
  .danger-hole-box .text{
    height:96px;
    line-height:98px;
    text-align: center;
    font-family: digi;
    font-size:24px;
  }
  .danger-hole-asset-box{
    background: url("../../../assets/images/ssa/hole-asset-bg.png") no-repeat;
    background-size:96px;
  }

  .big-hole-top5-box ul{
    margin-top:-5px;
  }
  .big-hole-top5-box ul li{
    padding-bottom:4px;
  }
  .big-hole-top5-box ul li .top-title{
    padding-left:0px;
    font-size:14px;
    font-weight:bold;
    font-style:italic;
    text-shadow: 0 1px #e96157, 1px 0 #e96157, -1px 0 #e96157, 0 -1px #e96157;
  }
  .attack-info-table{
    width:100%;
    border-collapse: separate;
    border-spacing: 0px 2px;
  }
  .attack-info-table tr th{
    background:rgba(74,146,255,0.2);
    padding-top:8px;
    padding-bottom:8px;
    text-align:center;
    color:#93a6d8;
  }
  .attack-info-table tr th:first-child,.attack-info-table tr td:first-child{
    border-top-left-radius: 3px;
    border-bottom-left-radius: 3px;
  }
  .attack-info-table tr th:last-child,.attack-info-table tr td:last-child{
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
  }
  .attack-info-table tr td{
    background:rgba(74,146,255,0.1);
    padding-top:10px;
    padding-bottom:10px;
    text-align:center;
    collapse: 1;
  }
</style>
<script>
  import Api from 'src/lib/api'
  let echarts =  require('echarts/lib/echarts');
  export default {
    name: "global-full-page",
    props:{
      show:{
        default:false
      }
    },
    data() {
      return {
        curDate:"",
        curWeek:"",
        curTime:"",
        realMapData:[],
        securityGrade:0,
        networkData:{
          export:{},
          ids:{},
          firewall:{},
          ddos:{},
        },
        serverData:{
          hole:{},
          viruses:{},
          weak_password:{},
        },
        appData:{
          waf:{},
          hole:{},
          database:{},
        },
        attackChangeNum:0,
        attackTotalNum:0,
        infectChangeNum:0,
        infectTotalNum:0,
        bigHoleTop5Data:[],
        holeCountData:{
          hole_count:0,
          severe:0,
          hole_ip_count:0,
          hole_ratio:0
        },
        attackInfoRealData:[]
      }
    },
    filters: {
      changeBand(val){
        if (val < 1024) {
          return val
        } else if (val >= 1024 && val < 1024 * 1024) {
          val = (val / 1024).toFixed(1);
          return val
        } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
          val = (val / (1024 * 1024)).toFixed(1);
          return val
        } else if (val >= 1024 * 1024 * 1024) {
          val = (val / (1024 * 1024 * 1024)).toFixed(1);
          return val
        }
      },
      changeUnit(val){
        if (val < 1024) {
          return "b"
        } else if (val >= 1024 && val < 1024 * 1024) {
          return "Kb"
        } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
          return "Mb"
        } else if (val >= 1024 * 1024 * 1024) {
          return "Gb"
        }
      },
      range(val){
        if(val>=1000){
          return "999+"
        }else{
          return val
        }
      }
    },
    ready: function() {
    },
    methods:{
      setRealTime(){
        let self=this;
        function run(){
          var time = new Date();//获取系统当前时间
          var year = time.getFullYear();
          var month = time.getMonth()+1;
          var date= time.getDate();//系统时间月份中的日
          var day = time.getDay();//系统时间中的星期值
          var weeks = ["星期日","星期一","星期二","星期三","星期四","星期五","星期六"];
          var week = weeks[day];//显示为星期几
          var hour = time.getHours();
          var minutes = time.getMinutes();
          var seconds = time.getSeconds();
          if(month<10){
            month = "0"+month;
          }
          if(date<10){
            date = "0"+date;
          }
          if(hour<10){
            hour = "0"+hour;
          }
          if(minutes<10){
            minutes = "0"+minutes;
          }
          if(seconds<10){
            seconds = "0"+seconds;
          }
          self.curDate=year+"年"+month+"月"+date+"日";
          self.curWeek=week;
          self.curTime=hour+":"+minutes+":"+seconds;
        }
        setInterval(function(){
          run()
        },1000)
      },
      getRealMapData(){
        let self=this;
          this.realMapData=[
            [{
              "name": "北京"
            }, {
              "name": "南京",
              "value": 16.67
            }],
            [{
              "name": "沈阳"
            }, {
              "name": "南京",
              "value": 16.67
            }],
            [{
              "name": "国外"
            }, {
              "name": "南京",
              "value": 33.33
            }],
            [{
              "name": "厦门"
            }, {
              "name": "南京",
              "value": 16.67
            }],
            [{
              "name": "广州"
            }, {
              "name": "南京",
              "value": 16.67
            }]
          ];
          let width=window.screen.width-320-350;
          let height=window.screen.height-270;
          $("#global-map-chart").css({"width":width+"px","height":height+"px"});
          let myChart = echarts.init(document.getElementById('global-map-chart'));
          let geoCoordMap={
            '国外':[104.77,45.56],
            '北京市': [116.4551,40.2539],
            '天津市': [117.2, 39.12],
            '厦门':[118.1,24.46],
            '河北省石家庄市': [114.52, 38.05],
            '河北省唐山市': [118.2, 39.63],
            '河北省秦皇岛市': [119.6, 39.93],
            '河北省邯郸市': [114.48, 36.62],
            '河北省邢台市': [114.48, 37.07],
            '河北省保定市': [115.47, 38.87],
            '河北省张家口市': [114.88, 40.82],
            '河北省承德市': [117.93, 40.97],
            '河北省沧州市': [116.83, 38.3],
            '河北省廊坊市': [116.7, 39.52],
            '河北省衡水市': [115.68, 37.73],
            '山西省太原市': [112.55, 37.87],
            '山西省大同市': [113.3, 40.08],
            '山西省长治市': [113.12, 36.2],
            '山西省晋城市': [112.83, 35.5],
            '山西省朔州市': [112.43, 39.33],
            '山西省晋中市': [112.75, 37.68],
            '山西省运城市': [110.98, 35.02],
            '山西省忻州市': [112.73, 38.42],
            '山西省临汾市': [111.52, 36.08],
            '山西省吕梁市': [111.13, 37.52],
            '内蒙古呼和浩特市': [111.73, 40.83],
            '内蒙古包头市': [109.83, 40.65],
            '内蒙古乌海市': [106.82, 39.67],
            '内蒙古赤峰市': [118.92, 42.27],
            '内蒙古通辽市': [122.27, 43.62],
            '内蒙古鄂尔多斯市': [109.8, 39.62],
            '内蒙古呼伦贝尔市': [119.77, 49.22],
            '内蒙古巴彦淖尔市': [107.42, 40.75],
            '内蒙古乌兰察布市': [113.12, 40.98],
            '内蒙古兴安盟': [122.05, 46.08],
            '内蒙古锡林郭勒盟': [116.07, 43.95],
            '内蒙古阿拉善盟': [105.67, 38.83],
            '辽宁省沈阳市': [123.43, 41.8],
            '辽宁省大连市': [121.62, 38.92],
            '辽宁省鞍山市': [122.98, 41.1],
            '辽宁省抚顺市': [123.98, 41.88],
            '辽宁省本溪市': [123.77, 41.3],
            '辽宁省丹东市': [124.38, 40.13],
            '辽宁省锦州市': [121.13, 41.1],
            '辽宁省营口市': [122.23, 40.67],
            '辽宁省阜新市': [121.67, 42.02],
            '辽宁省辽阳市': [123.17, 41.27],
            '辽宁省盘锦市': [122.07, 41.12],
            '辽宁省铁岭市': [123.83, 42.28],
            '辽宁省朝阳市': [120.45, 41.57],
            '辽宁省葫芦岛市': [120.83, 40.72],
            '吉林省长春市': [125.32, 43.9],
            '吉林省吉林市': [126.55, 43.83],
            '吉林省四平市': [124.35, 43.17],
            '吉林省辽源市': [125.13, 42.88],
            '吉林省通化市': [125.93, 41.73],
            '吉林省白山市': [126.42, 41.93],
            '吉林省松原市': [124.82, 45.13],
            '吉林省白城市': [122.83, 45.62],
            '吉林省延边州': [129.5, 42.88],
            '吉林省延边州': [129.5, 42.88],
            '吉林省延边州': [129.5, 42.88],
            '黑龙江省哈尔滨市': [126.53, 45.8],
            '黑龙江省齐齐哈尔市': [123.95, 47.33],
            '黑龙江省鸡西市': [130.97, 45.3],
            '黑龙江省鹤岗市': [130.27, 47.33],
            '黑龙江省双鸭山市': [131.15, 46.63],
            '黑龙江省大庆市': [125.03, 46.58],
            '黑龙江省伊春市': [128.9, 47.73],
            '黑龙江省佳木斯市': [130.37, 46.82],
            '黑龙江省七台河市': [130.95, 45.78],
            '黑龙江省牡丹江市': [129.6, 44.58],
            '黑龙江省黑河市': [127.48, 50.25],
            '黑龙江省绥化市': [126.98, 46.63],
            '黑龙江省大兴安岭地区': [124.12, 50.42],
            '上海市': [121.4648,31.2891],
            '江苏省南京市': [118.78, 32.07],
            '江苏省无锡市': [120.3, 31.57],
            '江苏省徐州市': [117.18, 34.27],
            '江苏省常州市': [119.95, 31.78],
            '江苏省苏州市': [120.58, 31.3],
            '江苏省南通市': [120.88, 31.98],
            '江苏省连云港市': [119.22, 34.6],
            '江苏省淮安市': [119.02, 33.62],
            '江苏省盐城市': [120.15, 33.35],
            '江苏省扬州市': [119.4, 32.4],
            '江苏省镇江市': [119.45, 32.2],
            '江苏省泰州市': [119.92, 32.45],
            '江苏省宿迁市': [118.28, 33.97],
            '浙江省杭州市': [120.15, 30.28],
            '浙江省宁波市': [121.55, 29.88],
            '浙江省温州市': [120.7, 28.0],
            '浙江省嘉兴市': [120.75, 30.75],
            '浙江省湖州市': [120.08, 30.9],
            '浙江省绍兴市': [120.57, 30.0],
            '浙江省金华市': [119.65, 29.08],
            '浙江省衢州市': [118.87, 28.93],
            '浙江省舟山市': [122.2, 30.0],
            '浙江省台州市': [121.43, 28.68],
            '浙江省丽水市': [119.92, 28.45],
            '安徽省合肥市': [117.25, 31.83],
            '安徽省芜湖市': [118.38, 31.33],
            '安徽省蚌埠市': [117.38, 32.92],
            '安徽省淮南市': [117.0, 32.63],
            '安徽省马鞍山市': [118.5, 31.7],
            '安徽省淮北市': [116.8, 33.95],
            '安徽省铜陵市': [117.82, 30.93],
            '安徽省安庆市': [117.05, 30.53],
            '安徽省黄山市': [118.33, 29.72],
            '安徽省滁州市': [118.32, 32.3],
            '安徽省阜阳市': [115.82, 32.9],
            '安徽省宿州市': [116.98, 33.63],
            '安徽省巢湖市': [117.87, 31.6],
            '安徽省六安市': [116.5, 31.77],
            '安徽省亳州市': [115.78, 33.85],
            '安徽省池州市': [117.48, 30.67],
            '安徽省宣城市': [118.75, 30.95],
            '福建省福州市': [119.3, 26.08],
            '福建省厦门市': [118.08, 24.48],
            '福建省莆田市': [119.0, 25.43],
            '福建省三明市': [117.62, 26.27],
            '福建省泉州市': [118.67, 24.88],
            '福建省漳州市': [117.65, 24.52],
            '福建省南平市': [118.17, 26.65],
            '福建省龙岩市': [117.03, 25.1],
            '福建省宁德市': [119.52, 26.67],
            '江西省南昌市': [115.85, 28.68],
            '江西省景德镇市': [117.17, 29.27],
            '江西省萍乡市': [113.85, 27.63],
            '江西省九江市': [116.0, 29.7],
            '江西省新余市': [114.92, 27.82],
            '江西省鹰潭市': [117.07, 28.27],
            '江西省赣州市': [114.93, 25.83],
            '江西省吉安市': [114.98, 27.12],
            '江西省宜春市': [114.38, 27.8],
            '江西省抚州市': [116.35, 28.0],
            '江西省上饶市': [117.97, 28.45],
            '山东省济南市': [116.98, 36.67],
            '山东省青岛市': [120.38, 36.07],
            '山东省淄博市': [118.05, 36.82],
            '山东省枣庄市': [117.32, 34.82],
            '山东省东营市': [118.67, 37.43],
            '山东省烟台市': [121.43, 37.45],
            '山东省潍坊市': [119.15, 36.7],
            '山东省济宁市': [116.58, 35.42],
            '山东省泰安市': [117.08, 36.2],
            '山东省威海市': [122.12, 37.52],
            '山东省日照市': [119.52, 35.42],
            '山东省莱芜市': [117.67, 36.22],
            '山东省临沂市': [118.35, 35.05],
            '山东省德州市': [116.3, 37.45],
            '山东省聊城市': [115.98, 36.45],
            '山东省滨州市': [117.97, 37.38],
            '山东省菏泽市': [115.43, 35.25],
            '河南省郑州市': [113.62, 34.75],
            '河南省开封市': [114.3, 34.8],
            '河南省洛阳市': [112.45, 34.62],
            '河南省平顶山市': [113.18, 33.77],
            '河南省安阳市': [114.38, 36.1],
            '河南省鹤壁市': [114.28, 35.75],
            '河南省新乡市': [113.9, 35.3],
            '河南省焦作市': [113.25, 35.22],
            '河南省濮阳市': [115.03, 35.77],
            '河南省许昌市': [113.85, 34.03],
            '河南省漯河市': [114.02, 33.58],
            '河南省三门峡市': [111.2, 34.78],
            '河南省南阳市': [112.52, 33.0],
            '河南省商丘市': [115.65, 34.45],
            '河南省信阳市': [114.07, 32.13],
            '河南省周口市': [114.65, 33.62],
            '河南省驻马店市': [114.02, 32.98],
            '湖北省武汉市': [114.3, 30.6],
            '湖北省黄石市': [115.03, 30.2],
            '湖北省十堰市': [110.78, 32.65],
            '湖北省宜昌市': [111.28, 30.7],
            '湖北省襄阳市': [112.15, 32.02],
            '湖北省鄂州市': [114.88, 30.4],
            '湖北省荆门市': [112.2, 31.03],
            '湖北省孝感市': [113.92, 30.93],
            '湖北省荆州市': [112.23, 30.33],
            '湖北省黄冈市': [114.87, 30.45],
            '湖北省咸宁市': [114.32, 29.85],
            '湖北省随州市': [113.37, 31.72],
            '湖北省恩施州': [109.47, 30.3],
            '湖北省仙桃市': [113.45, 30.37],
            '湖南省长沙市': [112.93, 28.23],
            '湖南省株洲市': [113.13, 27.83],
            '湖南省湘潭市': [112.93, 27.83],
            '湖南省衡阳市': [112.57, 26.9],
            '湖南省邵阳市': [111.47, 27.25],
            '湖南省岳阳市': [113.12, 29.37],
            '湖南省常德市': [111.68, 29.05],
            '湖南省张家界市': [110.47, 29.13],
            '湖南省益阳市': [112.32, 28.6],
            '湖南省郴州市': [113.02, 25.78],
            '湖南省永州市': [111.62, 26.43],
            '湖南省怀化市': [110.0, 27.57],
            '湖南省娄底市': [112.0, 27.73],
            '湖南省湘西州': [109.73, 28.32],
            '广东省广州市': [113.27, 23.13],
            '广东省韶关市': [113.6, 24.82],
            '广东省深圳市': [114.05, 22.55],
            '广东省珠海市': [113.57, 22.27],
            '广东省汕头市': [116.68, 23.35],
            '广东省佛山市': [113.12, 23.02],
            '广东省江门市': [113.08, 22.58],
            '广东省湛江市': [110.35, 21.27],
            '广东省茂名市': [110.92, 21.67],
            '广东省肇庆市': [112.47, 23.05],
            '广东省惠州市': [114.42, 23.12],
            '广东省梅州市': [116.12, 24.28],
            '广东省汕尾市': [115.37, 22.78],
            '广东省河源市': [114.7, 23.73],
            '广东省阳江市': [111.98, 21.87],
            '广东省清远市': [113.03, 23.7],
            '广东省东莞市': [113.75, 23.05],
            '广东省中山市': [113.38, 22.52],
            '广东省潮州市': [116.62, 23.67],
            '广东省揭阳市': [116.37, 23.55],
            '广东省云浮市': [112.03, 22.92],
            '广西南宁市': [108.37, 22.82],
            '广西柳州市': [109.42, 24.33],
            '广西桂林市': [110.28, 25.28],
            '广西梧州市': [111.27, 23.48],
            '广西北海市': [109.12, 21.48],
            '广西防城港市': [108.35, 21.7],
            '广西钦州市': [108.62, 21.95],
            '广西贵港市': [109.6, 23.1],
            '广西玉林市': [110.17, 22.63],
            '广西百色市': [106.62, 23.9],
            '广西贺州市': [111.55, 24.42],
            '广西河池市': [108.07, 24.7],
            '广西来宾市': [109.23, 23.73],
            '广西崇左市': [107.37, 22.4],
            '海南省海口市': [110.32, 20.03],
            '海南省三亚市': [109.5, 18.25],
            '海南省五指山市': [109.52, 18.78],
            '重庆市': [106.55, 29.57],
            '四川省成都市': [104.07, 30.67],
            '四川省自贡市': [104.78, 29.35],
            '四川省攀枝花市': [101.72, 26.58],
            '四川省泸州市': [105.43, 28.87],
            '四川省德阳市': [104.38, 31.13],
            '四川省绵阳市': [104.73, 31.47],
            '四川省广元市': [105.83, 32.43],
            '四川省遂宁市': [105.57, 30.52],
            '四川省内江市': [105.05, 29.58],
            '四川省乐山市': [103.77, 29.57],
            '四川省南充市': [106.08, 30.78],
            '四川省眉山市': [103.83, 30.05],
            '四川省宜宾市': [104.62, 28.77],
            '四川省广安市': [106.63, 30.47],
            '四川省达州市': [107.5, 31.22],
            '四川省雅安市': [103.0, 29.98],
            '四川省巴中市': [106.77, 31.85],
            '四川省资阳市': [104.65, 30.12],
            '四川省阿坝州': [102.22, 31.9],
            '四川省甘孜州': [101.97, 30.05],
            '四川省凉山州': [102.27, 27.9],
            '贵州省贵阳市': [106.63, 26.65],
            '贵州省六盘水市': [104.83, 26.6],
            '贵州省遵义市': [106.92, 27.73],
            '贵州省安顺市': [105.95, 26.25],
            '贵州省铜仁地区': [109.18, 27.72],
            '贵州省兴义市': [104.9, 25.08],
            '贵州省毕节地区': [105.28, 27.3],
            '贵州省黔东南州': [107.97, 26.58],
            '贵州省黔南州': [107.52, 26.27],
            '贵州省黔西南州': [106.04, 27.03],
            '云南省昆明市': [102.72, 25.05],
            '云南省曲靖市': [103.8, 25.5],
            '云南省玉溪市': [102.55, 24.35],
            '云南省保山市': [99.17, 25.12],
            '云南省昭通市': [103.72, 27.33],
            '云南省丽江市': [100.23, 26.88],
            '云南省普洱市': [101.68, 23.43],
            '云南省临沧市': [100.08, 23.88],
            '云南省楚雄州': [101.55, 25.03],
            '云南省红河州': [103.4, 23.37],
            '云南省文山州': [104.25, 23.37],
            '云南省西双版纳州': [100.8, 22.02],
            '云南省大理州': [100.23, 25.6],
            '云南省德宏州': [98.58, 24.43],
            '云南省怒江州': [98.85, 25.85],
            '云南省迪庆州': [99.7, 27.83],
            '西藏拉萨市': [91.13, 29.65],
            '西藏昌都地区': [97.18, 31.13],
            '西藏山南地区': [91.77, 29.23],
            '西藏日喀则地区': [88.88, 29.27],
            '西藏那曲地区': [92.07, 31.48],
            '西藏阿里地区': [80.1, 32.5],
            '西藏林芝地区': [94.37, 29.68],
            '陕西省西安市': [108.93, 34.27],
            '陕西省铜川市': [108.93, 34.9],
            '陕西省宝鸡市': [107.13, 34.37],
            '陕西省咸阳市': [108.7, 34.33],
            '陕西省渭南市': [109.5, 34.5],
            '陕西省延安市': [109.48, 36.6],
            '陕西省汉中市': [107.02, 33.07],
            '陕西省榆林市': [109.73, 38.28],
            '陕西省安康市': [109.02, 32.68],
            '陕西省商洛市': [109.93, 33.87],
            '甘肃省兰州市': [103.82, 36.07],
            '甘肃省嘉峪关市': [98.27, 39.8],
            '甘肃省金昌市': [102.18, 38.5],
            '甘肃省白银市': [104.18, 36.55],
            '甘肃省天水市': [105.72, 34.58],
            '甘肃省武威市': [102.63, 37.93],
            '甘肃省张掖市': [100.45, 38.93],
            '甘肃省平凉市': [106.67, 35.55],
            '甘肃省酒泉市': [98.52, 39.75],
            '甘肃省庆阳市': [107.63, 35.73],
            '甘肃省定西市': [104.62, 35.58],
            '甘肃省陇南市': [104.92, 33.4],
            '甘肃省临夏州': [103.22, 35.6],
            '甘肃省甘南州': [102.92, 34.98],
            '青海省西宁市': [101.78, 36.62],
            '青海省海东地区': [102.12, 36.5],
            '青海省海北州': [100.9, 36.97],
            '青海省黄南州': [102.02, 35.52],
            '青海省海南州': [100.62, 36.28],
            '青海省果洛州': [100.23, 34.48],
            '青海省玉树州': [97.02, 33.0],
            '青海省海西州': [97.37, 37.37],
            '宁夏银川市': [106.28, 38.47],
            '宁夏石嘴山市': [106.38, 39.02],
            '宁夏吴忠市': [106.2, 37.98],
            '宁夏固原市': [106.28, 36.0],
            '宁夏中卫市': [105.18, 37.52],
            '新疆乌鲁木齐市': [87.62, 43.82],
            '新疆克拉玛依市': [84.87, 45.6],
            '新疆吐鲁番地区': [89.17, 42.95],
            '新疆哈密地区': [93.52, 42.83],
            '新疆昌吉州': [87.3, 44.02],
            '新疆博尔塔拉州': [82.07, 44.9],
            '新疆巴音郭楞州': [86.15, 41.77],
            '新疆阿克苏地区': [80.27, 41.17],
            '新疆阿图什市': [76.17, 39.72],
            '新疆喀什地区': [75.98, 39.47],
            '新疆和田地区': [79.92, 37.12],
            '新疆伊犁州': [81.32, 43.92],
            '新疆塔城地区': [82.98, 46.75],
            '新疆阿勒泰地区': [88.13, 47.85],
            '新疆石河子市': [86.03, 44.3],
            '香港': [114.08, 22.2],
            '澳门': [113.33, 22.13],
            '台湾': [121.5, 25.03],
            '台湾省台北': [121.5, 25.03],
            '台湾省高雄': [120.28, 22.62],
            '台湾省基隆': [121.73, 25.13],
            '台湾省台中': [120.67, 24.15],
            '台湾省台南': [120.2, 23.0],
            '台湾省新竹': [120.95, 24.82],
            '台湾省嘉义': [120.43, 23.48],
            '台湾省台北': [121.5, 25.03],
            '台湾省宜兰': [121.75, 24.77],
            '台湾省桃园': [121.3, 24.97],
            '台湾省苗栗': [120.8, 24.53],
            '台湾省台中': [120.67, 24.15],
            '台湾省彰化': [120.53, 24.08],
            '台湾省南投': [120.67, 23.92],
            '台湾省云林': [120.53, 23.72],
            '台湾省台南': [120.2, 23.0],
            '台湾省高雄': [120.28, 22.62],
            '台湾省屏东': [120.48, 22.67],
            '台湾省台东': [121.15, 22.75],
            '台湾省花莲': [121.6, 23.98],
            '台湾省澎湖': [119.58, 23.58],
            '海门':[121.15,31.89],
            '鄂尔多斯':[109.781327,39.608266],
            '招远':[120.38,37.35],
            '舟山':[122.207216,29.985295],
            '齐齐哈尔':[123.97,47.33],
            '盐城':[120.13,33.38],
            '赤峰':[118.87,42.28],
            '青岛':[120.33,36.07],
            '乳山':[121.52,36.89],
            '金昌':[102.188043,38.520089],
            '泉州':[118.58,24.93],
            '莱西':[120.53,36.86],
            '日照':[119.46,35.42],
            '胶南':[119.97,35.88],
            '南通':[121.05,32.08],
            '拉萨':[91.11,29.97],
            '云浮':[112.02,22.93],
            '梅州':[116.1,24.55],
            '文登':[122.05,37.2],
            '上海':[121.48,31.22],
            '攀枝花':[101.718637,26.582347],
            '威海':[122.1,37.5],
            '承德':[117.93,40.97],
            '厦门':[118.1,24.46],
            '汕尾':[115.375279,22.786211],
            '潮州':[116.63,23.68],
            '丹东':[124.37,40.13],
            '太仓':[121.1,31.45],
            '曲靖':[103.79,25.51],
            '烟台':[121.39,37.52],
            '福州':[119.3,26.08],
            '瓦房店':[121.979603,39.627114],
            '即墨':[120.45,36.38],
            '抚顺':[123.97,41.97],
            '玉溪':[102.52,24.35],
            '张家口':[114.87,40.82],
            '阳泉':[113.57,37.85],
            '莱州':[119.942327,37.177017],
            '湖州':[120.1,30.86],
            '汕头':[116.69,23.39],
            '昆山':[120.95,31.39],
            '宁波':[121.56,29.86],
            '湛江':[110.359377,21.270708],
            '揭阳':[116.35,23.55],
            '荣成':[122.41,37.16],
            '连云港':[119.16,34.59],
            '葫芦岛':[120.836932,40.711052],
            '常熟':[120.74,31.64],
            '东莞':[113.75,23.04],
            '广东-东莞':[113.75,23.04],
            '河源':[114.68,23.73],
            '淮安':[119.15,33.5],
            '泰州':[119.9,32.49],
            '南宁':[108.33,22.84],
            '营口':[122.18,40.65],
            '惠州':[114.4,23.09],
            '江阴':[120.26,31.91],
            '蓬莱':[120.75,37.8],
            '韶关':[113.62,24.84],
            '嘉峪关':[98.289152,39.77313],
            '广州':[113.23,23.16],
            '延安':[109.47,36.6],
            '太原':[112.53,37.87],
            '清远':[113.01,23.7],
            '中山':[113.38,22.52],
            '昆明':[102.73,25.04],
            '寿光':[118.73,36.86],
            '盘锦':[122.070714,41.119997],
            '长治':[113.08,36.18],
            '深圳':[114.07,22.62],
            '珠海':[113.52,22.3],
            '宿迁':[118.3,33.96],
            '咸阳':[108.72,34.36],
            '铜川':[109.11,35.09],
            '平度':[119.97,36.77],
            '佛山':[113.11,23.05],
            '海口':[110.35,20.02],
            '江门':[113.06,22.61],
            '章丘':[117.53,36.72],
            '肇庆':[112.44,23.05],
            '大连':[121.62,38.92],
            '临汾':[111.5,36.08],
            '吴江':[120.63,31.16],
            '石嘴山':[106.39,39.04],
            '沈阳':[123.38,41.8],
            '苏州':[120.62,31.32],
            '茂名':[110.88,21.68],
            '嘉兴':[120.76,30.77],
            '长春':[125.35,43.88],
            '胶州':[120.03336,36.264622],
            '银川':[106.27,38.47],
            '张家港':[120.555821,31.875428],
            '三门峡':[111.19,34.76],
            '锦州':[121.15,41.13],
            '南昌':[115.89,28.68],
            '柳州':[109.4,24.33],
            '三亚':[109.511909,18.252847],
            '自贡':[104.778442,29.33903],
            '吉林':[126.57,43.87],
            '阳江':[111.95,21.85],
            '泸州':[105.39,28.91],
            '西宁':[101.74,36.56],
            '宜宾':[104.56,29.77],
            '呼和浩特':[111.65,40.82],
            '成都':[104.06,30.67],
            '大同':[113.3,40.12],
            '镇江':[119.44,32.2],
            '桂林':[110.28,25.29],
            '张家界':[110.479191,29.117096],
            '宜兴':[119.82,31.36],
            '北海':[109.12,21.49],
            '西安':[108.95,34.27],
            '金坛':[119.56,31.74],
            '东营':[118.49,37.46],
            '牡丹江':[129.58,44.6],
            '遵义':[106.9,27.7],
            '绍兴':[120.58,30.01],
            '扬州':[119.42,32.39],
            '常州':[119.95,31.79],
            '潍坊':[119.1,36.62],
            '重庆':[106.54,29.59],
            '台州':[121.420757,28.656386],
            '南京':[118.78,32.04],
            '滨州':[118.03,37.36],
            '贵阳':[106.71,26.57],
            '无锡':[120.29,31.59],
            '本溪':[123.73,41.3],
            '克拉玛依':[84.77,45.59],
            '渭南':[109.5,34.52],
            '马鞍山':[118.48,31.56],
            '宝鸡':[107.15,34.38],
            '焦作':[113.21,35.24],
            '句容':[119.16,31.95],
            '北京':[116.46,39.92],
            '徐州':[117.2,34.26],
            '衡水':[115.72,37.72],
            '包头':[110,40.58],
            '绵阳':[104.73,31.48],
            '乌鲁木齐':[87.68,43.77],
            '枣庄':[117.57,34.86],
            '杭州':[120.19,30.26],
            '淄博':[118.05,36.78],
            '鞍山':[122.85,41.12],
            '溧阳':[119.48,31.43],
            '库尔勒':[86.06,41.68],
            '安阳':[114.35,36.1],
            '开封':[114.35,34.79],
            '济南':[117,36.65],
            '德阳':[104.37,31.13],
            '温州':[120.65,28.01],
            '九江':[115.97,29.71],
            '邯郸':[114.47,36.6],
            '临安':[119.72,30.23],
            '兰州':[103.73,36.03],
            '沧州':[116.83,38.33],
            '临沂':[118.35,35.05],
            '南充':[106.110698,30.837793],
            '天津':[117.2,39.13],
            '富阳':[119.95,30.07],
            '泰安':[117.13,36.18],
            '诸暨':[120.23,29.71],
            '郑州':[113.65,34.76],
            '哈尔滨':[126.63,45.75],
            '聊城':[115.97,36.45],
            '芜湖':[118.38,31.33],
            '唐山':[118.02,39.63],
            '平顶山':[113.29,33.75],
            '邢台':[114.48,37.05],
            '德州':[116.29,37.45],
            '济宁':[116.59,35.38],
            '荆州':[112.239741,30.335165],
            '宜昌':[111.3,30.7],
            '义乌':[120.06,29.32],
            '丽水':[119.92,28.45],
            '洛阳':[112.44,34.7],
            '秦皇岛':[119.57,39.95],
            '株洲':[113.16,27.83],
            '石家庄':[114.48,38.03],
            '莱芜':[117.67,36.19],
            '常德':[111.69,29.05],
            '保定':[115.48,38.85],
            '湘潭':[112.91,27.87],
            '金华':[119.64,29.12],
            '岳阳':[113.09,29.37],
            '长沙':[113,28.21],
            '衢州':[118.88,28.97],
            '廊坊':[116.7,39.53],
            '菏泽':[115.480656,35.23375],
            '合肥':[117.27,31.86],
            '武汉':[114.31,30.52],
            '大庆':[125.03,46.58]
          };
          let convertData = function (data) {
            var res = [];
            for (var i = 0; i < data.length; i++) {
              var dataItem = data[i];
              var fromCoord = geoCoordMap[dataItem[0].name];
              var toCoord = geoCoordMap[dataItem[1].name];
              if (fromCoord && toCoord) {
                res.push({
                  fromName: dataItem[0].name,
                  toName: dataItem[1].name,
                  coords: [fromCoord, toCoord]
                });
              }
            }
            return res;
          };
          let mapOption = {
            title: {
              text: '',
              x: 'center',
              y: '20',
              textStyle: {
                color: '#fff',
                fontSize:28,
              }
            },
            tooltip: {
              trigger: 'item',
              formatter: '{b}'
            },
            dataRange: {
              show:false
            },
            geo: {
              zoom:1.3,
              map: 'china',
              label:{
                normal:{
                  show:false,
                  textStyle:{
                    color:"#fff"
                  }
                },
                emphasis: {
                  show:false,
                  textStyle:{
                    color:"#fff"
                  }
                }
              },
              roam: false,
              itemStyle: {
                normal: {
                  borderColor: 'rgba(74,146,255,0.5)',
                  borderWidth: 0.5,
                  areaColor: 'rgba(74,146,255,0.32)'
                },
                emphasis: {
                  areaColor: 'rgba(74,146,255,0.6)'
                }
              },
            },
            series: [
              {
                name: '',
                type: 'lines',
                zlevel: 1,
                polyline:false,
                label:{
                  emphasis:{
                    show:true,
                    formatter: '{b}>{c}'
                  }
                },
                lineStyle: {
                  normal: {
                    color: "#00bd85",
                    type:'solid',
                    width:2,
                    curveness: 0.2
                  }
                },
                data: convertData(self.realMapData)
              },
              {
                name: '',
                type: 'lines',
                zlevel: 2,
                polyline:false,
                effect: {
                  show: true,
                  period: 1.2,
                  trailLength:0.4,
                  color: '#db615e',
                  symbol:"triangle",
                  symbolSize: 4
                },
                label:{
                  emphasis:{
                    show:true,
                    formatter: '{b}>{c}'
                  }
                },
                lineStyle: {
                  normal: {
                    color: "#db615e",
                    type:'solid',
                    width:0,
                    curveness: 0
                  }
                },
                data: convertData(self.realMapData)
              },
              {
                name: "",
                type: 'effectScatter',
                coordinateSystem: 'geo',
                zlevel: 3,
                rippleEffect: {
                  brushType: 'stroke',
                  period:2,
                  scale:15
                },
                itemStyle: {
                  normal: {
                    color: "#db615e"
                  }
                },
                symbolSize:5,
                data: self.realMapData.map(function (dataItem) {
                  return {
                    name: dataItem[1].name,
                    value: geoCoordMap[dataItem[1].name].concat([dataItem[1].value])
                  };
                })
              },
              {
                name: "",
                type: 'effectScatter',
                coordinateSystem: 'geo',
                zlevel: 4,
                rippleEffect: {
                  brushType: 'stroke',
                  period:4,
                  scale:10
                },
                label:{
                  emphasis:{
                    show:true,
                    formatter: function(params){
                      let data=params.data;
                      return data.name + " ---> " + data.target
                    }
                  }
                },
                itemStyle: {
                  normal: {
                    color: "#db615e"
                  }
                },
                symbolSize: 5,
                data: self.realMapData.map(function (dataItem) {
                  return {
                    name: dataItem[0].name,
                    value: geoCoordMap[dataItem[0].name],
                    target:dataItem[1].name
                  };
                })
              }
            ]
          };
          myChart.setOption(mapOption);
      },
      getAttackInfoData(){
        let self=this;
        if(window.WebSocket != undefined) {
          let host='10.10.10.33';
          //let host=window.location.host;
          var connection = new WebSocket('ws://'+host+'/api/ssa/websocket/security/attack_map');
          //console.log(connection.readyState);
          //握手协议成功以后，readyState就从0变为1，并触发open事件
          connection.onopen = function wsOpen (event) {
            connection.send('向客户端发送消息');
          };
          connection.onmessage = function wsMessage (event) {
            let data=JSON.parse(event.data);
            if(self.attackInfoRealData.length>4){
              self.attackInfoRealData.shift()
            }
            self.attackInfoRealData.push(data);
          };//监听
          connection.onclose = function wsClose () {
            console.log("Closed");
          };//关闭WebSocket连接，会触发close事件。
          connection.onerror = wsError;//出现错误
          function wsError(event) {
            console.log("Error: " + event.data);
          }
        }
      },
      getSecurityGrade(){
        this.$http.get('/api/ssa/global/security_overview').then(function (response) {
          if (response.data.status == 200) {
            this.securityGrade=response.data.data.security_mark;
            let deg=2.43*this.securityGrade-90;
            $("#safe-grade-box-point").css({"transform":"rotate("+deg+"deg)"})
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getAssetData(){
        this.$http.get('/api/ssa/global/assets_overview').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data;
            this.networkData=data.network;
            this.serverData=data.server;
            this.appData=data.application;
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getDangerGrade(){
        this.$http.get('/api/ssa/global/danger_rating').then(function (response) {
          if (response.data.status == 200) {
            let chartData=response.data.data;
            let compositeStateChart = echarts.init(document.getElementById('composite-state'));
            let option = {
              radar: {
                shape: 'polygon',
                name: {
                  textStyle: {
                    color: '#e6edff',
                  }
                },
                radius:'66%',
                nameGap:10,
                indicator: [
                  { name: '漏洞资产比例', max: 100},
                  { name: '业务访问指数', max: 100},
                  { name: '业务流康指数', max: 100},
                  { name: '僵木蠕感染指数', max: 100},
                  { name: '攻击指数', max: 100},
                  { name: '漏洞严重指数', max: 100},
                ],
                splitArea:{
                  show:true,
                  areaStyle:{
                    color:"rgba(74, 146, 255, 0.2)",
                  },
                },
                splitLine:{
                  lineStyle:{
                    color:"rgba(74, 146, 255, 0.2)"
                  }
                },
                axisLine:{
                  show:true,
                  lineStyle:{
                    color:"rgba(74, 146, 255, 0.2)"
                  }
                },
              },
              series: [{
                name: '预算 vs 开销（Budget vs spending）',
                type: 'radar',
                areaStyle:{
                  color:"rgba(233,97,87,0.35)"
                },
                lineStyle:{
                  color:"rgba(233,97,87,1)",
                },
                data : [
                  {
                    value : [chartData.hole_assets, chartData.business_visit, chartData.business_health, chartData.trojan, chartData.attack, chartData.hole_serious],
                    name : '预算分配（Allocated Budget）'
                  }
                ]
              }]
            };
            compositeStateChart.setOption(option);
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getAttackNum(){
        this.$http.get('/api/ssa/global/attack_num').then(function (response) {
          if (response.data.status == 200) {
            this.attackTotalNum=response.data.data.total;
            this.attackChangeNum=response.data.data.proportion;
            let attackNumData=response.data.data.data;
            let attackTimeChart = echarts.init(document.getElementById('ssa-attack-time'));
            let attackTimeOption = {
              tooltip:{
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
              },
              calculable : true,
              color:["#4a92ff", "#e77d4e", "#dabb61", "#e96157"],
              series:[
                {
                  name:'攻击次数',
                  type:'pie',
                  radius : ['20%','50%'],
                  center: ['150', '150'],
                  roseType : 'area',
                  labelLine:{
                    length:5,
                    length2:5,
                  },
                  data:attackNumData
                }
              ]
            };
            attackTimeChart.setOption(attackTimeOption);
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getAttackSource(){
        this.$http.get('/api/ssa/global/attack_source_total').then(function (response) {
          if (response.data.status == 200) {
            let sourceData=response.data.data.table;
            let attackSourceChart = echarts.init(document.getElementById('ssa-source-chart'));
            var dataAxis = sourceData.x;
            var data = sourceData.y;
            var yMax = Math.max.apply(null, sourceData.y);
            var dataShadow = [];
            for (var i = 0; i < data.length; i++) {
              dataShadow.push(yMax);
            }
            let attackSourceOption = {
              xAxis: {
                data: dataAxis,
                axisLabel: {
                  textStyle: {
                    color: '#93a6d8'
                  }
                },
                axisTick: {
                  show: false
                },
                axisLine: {
                  show: false
                },
                splitLine:{
                  show: false
                },
                z: 10
              },
              yAxis: {
                axisLine: {
                  show: false
                },
                axisTick: {
                  show: false
                },
                axisLabel: {
                  textStyle: {
                    color: '#93a6d8'
                  }
                },
                splitLine:{
                  show: false
                }
              },
              grid: {
                top: 10,
                bottom:0,
                left:0,
                right:0,
                containLabel: true
              },
              dataZoom: [
                {
                  type: 'inside'
                }
              ],
              series: [
                { // For shadow
                  type: 'bar',
                  itemStyle: {
                    normal: {color: 'rgba(74,146,255,0.15)'}
                  },
                  barGap:'-100%',
                  barWidth:12,
                  data: dataShadow,
                  animation: false
                },
                {
                  type: 'bar',
                  barWidth:12,
                  itemStyle: {
                    normal: {
                      color: new echarts.graphic.LinearGradient(
                          0, 0, 0, 1,
                          [
                            {offset: 0, color: '#e96157'},
                            {offset: 1, color: '#ccb060'}
                          ]
                      ),
                      borderColor:"#00c0ff",
                      shadowColor:"#00c0ff",
                      shadowBlur:10
                    },
                    emphasis: {
                      color: new echarts.graphic.LinearGradient(
                          0, 0, 0, 1,
                          [
                            {offset: 0, color: '#e96157'},
                            {offset: 1, color: '#ccb060'}
                          ]
                      )
                    }
                  },
                  data: data
                }
              ]
            };
            attackSourceChart.setOption(attackSourceOption);
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getWormInfect(){
        this.$http.get('/api/ssa/global/worm_num').then(function (response) {
          if (response.data.status == 200) {
            this.infectChangeNum=response.data.data.trend;
            this.infectTotalNum=response.data.data.worm_total;
            let use=response.data.data.proportion;
            let no_use=100-use;
            let wormInfectChart = echarts.init(document.getElementById('worm-infect-chart'));
            let wormInfectOption = {
              color:[{
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                  offset: 0, color: "#e56358" // 0% 处的颜色
                }, {
                  offset: 1, color: "#37a77a" // 100% 处的颜色
                }],
              },"#000000"],
              series: [
                {
                  name:'ring',
                  type:'pie',
                  radius: ['54%', '62%'],
                  avoidLabelOverlap: false,
                  hoverAnimation:false,
                  label: {
                    normal: {
                      show: true,
                      position: 'center',
                      color:"#e56358",
                      textStyle: {
                        fontSize: '20',
                        fontWeight: ''
                      }
                    },
                    emphasis: {
                      show: false,
                      textStyle: {
                        fontSize: '24',
                        fontWeight: 'bold'
                      }
                    }
                  },
                  data: [
                    {
                      value: use,
                      name:use+"%",
                      itemStyle:{
                        normal:{
                          borderColor:"#00c0ff",
                          shadowColor:"#00c0ff",
                          shadowBlur:10
                        }
                      }
                    },
                    {
                      value: no_use,
                      name:use+"%",
                      itemStyle:{
                        normal:{
                          color:"#4a92ff",
                          opacity:0.15
                        }
                      }
                    }
                  ]
                }
              ]
            };
            wormInfectChart.setOption(wormInfectOption);
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getBigHoleTop5(){
        this.$http.get('/api/ssa/global/loophole_top5').then(function (response) {
          if (response.data.status == 200) {
            this.bigHoleTop5Data=response.data.data;
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getHoleCount(){
        this.$http.get('/api/ssa/global/hole_count').then(function (response) {
          if (response.data.status == 200) {
            this.holeCountData=response.data.data;
            let countData=response.data.data;
            let use=((countData.severe/countData.hole_count)*100).toFixed(1);
            let no_use=100-use;
            let holeRateChart = echarts.init(document.getElementById('hole-rate-box'));
            let holeRateOption = {
              color:["#00bd85"],
              series: [
                {
                  name:'ring',
                  type:'pie',
                  radius: ['71%', '82%'],
                  avoidLabelOverlap: false,
                  hoverAnimation:false,
                  label: {
                    normal: {
                      show: true,
                      position: 'center',
                      color:"#e6edff",
                      textStyle: {
                        fontSize: '24',
                        fontWeight: '',
                        fontFamily:"digi"
                      }
                    },
                    emphasis: {
                      show: false,
                      textStyle: {
                        fontSize: '24',
                        fontWeight: 'bold'
                      }
                    }
                  },
                  data: [
                    {
                      value: use,
                      name:use+"%",
                    },
                    {
                      value: no_use,
                      name:"",
                      itemStyle:{
                        normal:{
                          color:"rgba(0,0,0,0)",
                        }
                      }
                    }
                  ]
                }
              ]
            };
            holeRateChart.setOption(holeRateOption);
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getWholeNetTrend(){
        this.$http.get('/api/ssa/global/situation_trend').then(function (response) {
          if (response.data.status == 200) {
            let trendData=response.data.data;
            let trendChart = echarts.init(document.getElementById('whole-net-ssa-trend'));
            let trendOption = {
              xAxis: {
                type: 'category',
                data:trendData.x,
                axisLine:{
                  show:true,
                  lineStyle:{
                    color:"#46578e",
                    opacity:"0.75"
                  }
                },
                axisTick: {
                  show:false,
                },
                axisLabel:{textStyle:{color:"#93a6d8"}}
              },
              grid: {
                top: '15',
                bottom:'40',
                left:20,
                right:20,
                containLabel: true
              },
              yAxis: {
                type: 'value',
                axisLabel:{
                  show:false,
                },
                axisLine:{
                  show:true,
                  lineStyle:{
                    color:"#46578e",
                    opacity:"0.75"
                  }
                },
                axisTick: {
                  show:false,
                },
                splitLine:{
                  lineStyle:{
                    color:"#46578e",
                    opacity:"0.75"
                  }
                }
              },
              series: [{
                data: trendData.y,
                type: 'line',
                smooth: true,
                lineStyle:{
                  color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [{
                      offset: 0, color: '#dabb61' // 0% 处的颜色
                    }, {
                      offset: 1, color: '#e96157' // 100% 处的颜色
                    }],
                    globalCoord: false // 缺省为 false
                  }
                }
              }]
            };
            trendChart.setOption(trendOption);
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      tableColor(status){
        if(status=="严重"){
          return "ys-error-color"
        }else if(status=="高"){
          return "ys-medium-color"
        }else if(status=="中"){
          return "ys-warn-color"
        }else if(status=="低"){
          return "ys-white-color"
        }
      },
      closeFullPage(){
        this.show=false
      }
    },
    watch:{
      'show':function(){
        if(this.show){
          this.setRealTime()
          this.getSecurityGrade()
          this.getAssetData()
          this.getDangerGrade()
          this.getAttackNum()
          this.getAttackSource()
          this.getWormInfect()
          this.getHoleCount()
          this.getBigHoleTop5()
          this.getWholeNetTrend()
          this.getRealMapData()
          this.getAttackInfoData()
        }
      }
    }
  }
</script>
