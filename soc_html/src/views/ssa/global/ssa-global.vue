<template>
  <div>
    <div class="global-wrap">
      <div class="global-head ys-box-con">
        <div class="global-title">
          <p class="font14 textC">态势感知平台</p>
          <span class="right"><button class="ys-btn" @click="showFullScreen()">全屏</button></span>
        </div>
        <div class="global-title m-t-5">
          <p class="ys-info-color textC">全局态势</p>
        </div>
      </div>
      <div class="m-t-10 pos-r">
        <div class="col-md-8 p-0">
          <div class="global-module-box">
            <div class="global-module-title ys-white-color">网络层</div>
            <div class="global-module-con">
              <div style="width:646px;margin:0 auto;" class="clearfix">
                <div class="col-md-3">
                  <p class="textC"><span class="title-mark blue"></span><span class="ys-info-color">网络出口</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{networkData.export.count | changeBand}}</span>{{networkData.export.count | changeUnit}}</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in networkData.export.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+changeValue(list.value)">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single blue text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-3">
                  <p class="textC"><span class="title-mark green"></span><span class="ys-info-color">IDS</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{networkData.ids.count}}</span>次攻击</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in networkData.ids.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+list.value+'次'">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single green text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-3">
                  <p class="textC"><span class="title-mark red"></span><span class="ys-info-color">防火墙</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{networkData.firewall.count}}</span>次拦截</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in networkData.firewall.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+list.value+'次'">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single red text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>     
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-3">
                  <p class="textC"><span class="title-mark yellow"></span><span class="ys-info-color">抗DDoS</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{networkData.ddos.count | changeBand}}</span>{{networkData.ddos.count | changeUnit}}</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in networkData.ddos.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+changeValue(list.value)">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single yellow text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="global-module-box m-t-5">
            <div class="global-module-title">主机层</div>
            <div class="global-module-con">
              <div style="width:646px;margin:0 auto;" class="clearfix">
                <div class="col-md-4">
                  <p class="textC"><span class="title-mark red"></span><span class="ys-info-color">漏洞扫描</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{serverData.hole.count}}</span>个漏洞</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in serverData.hole.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+list.value+'个'">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single red text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-4">
                  <p class="textC"><span class="title-mark green"></span><span class="ys-info-color">防病毒</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{serverData.viruses.count}}</span>个病毒感染</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in serverData.viruses.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+list.value+'个'">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single green text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-4">
                  <p class="textC"><span class="title-mark blue"></span><span class="ys-info-color">弱口令</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{serverData.weak_password.count}}</span>台主机</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in serverData.weak_password.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+list.value+'台'">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single blue text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="global-module-box m-t-5">
            <div class="global-module-title">应用层</div>
            <div class="global-module-con">
              <div style="width:646px;margin:0 auto;" class="clearfix">
                <div class="col-md-4">
                  <p class="textC"><span class="title-mark blue"></span><span class="ys-info-color">WAF</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{appData.waf.count}}</span>次攻击</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in appData.waf.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+list.value+'次'">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single blue text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-4">
                  <p class="textC"><span class="title-mark yellow"></span><span class="ys-info-color">漏洞</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{appData.hole.count}}</span>个漏洞</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in appData.hole.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+list.value+'个'">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single yellow text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="col-md-4">
                  <p class="textC"><span class="title-mark green"></span><span class="ys-info-color">数据库审计</span></p>
                  <p class="textC"><span class="font18 m-r-3">{{appData.database.count}}</span>次攻击</p>
                  <div class="module-list-box">
                    <ul class="module-list clearfix">
                      <li v-for="list in appData.database.new_data">
                        <tooltip :placement="'top'" :content="list.name+'&nbsp;&nbsp;'+list.value+'次'">
                          <div style="height:77px;width:4px;">
                            <div class="module-list-single green text-cursor"
                              v-bind:style="{height: list.height + 'px'}"></div>
                          </div> 
                        </tooltip>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="m-t-5 clearfix">
            <div class="col-md-6 p-0">
              <div class="ys-box">
                <div class="ys-box-title">危险等级比例</div>
                <div class="ys-box-con">
                  <div id="ssa-global-danger-grade-state" style="width:350px;height:250px;margin:0 auto;"></div>
                </div>
              </div>
            </div>
            <div class="col-md-6 p-0 p-l-5">
              <div class="ys-box">
                <div class="ys-box-title">攻击严重比例</div>
                <div class="ys-box-con">
                  <line-chart
                          :id="'ssa-global-serious-rate'"
                          :height="'250px'"
                          :name="lineData.name"
                          :x="lineData.x"
                          :color="lineData.color"
                          :series="lineData.series"></line-chart>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4 p-0 p-l-5">
          <div class="ys-box-con">
            <div class="security-grade-box m-t-10 m-b-10">
              <div class="title ys-info-color">安全评分</div>
              <div class="grade">{{securityGrade}}</div>
            </div>
          </div>
          <div class="ys-box m-t-5">
            <div class="ys-box-title">最新重大漏洞TOP5</div>
            <div class="ys-box-con" style="height：226px;">
              <table class="ys-chart-table over-table">
                <tr v-for="list in loopHoleTop5Data">
                  <td class="ys-error-color textL"><i class="ys-icon icon-menu-home m-r-5"></i><span>{{list.name}}</span></td>
                  <td>{{list.assets}}</td>
                </tr>
              </table>
              <no-data :height="'195px'" v-if="loopHoleTop5Data.length==0"></no-data>
            </div>
          </div>
          <div class="ys-box m-t-5">
            <div class="ys-box-title">攻击来源</div>
            <div class="ys-box-con">
              <pie-chart
                      :id="'ssa-global-attack-source'"
                      :height="'186px'"
                      :name="'攻击来源'"
                      :y.sync="attackSourceData"
                      :color="1"></pie-chart>
            </div>
          </div>
          <div class="ys-box m-t-5">
            <div class="ys-box-title">资产风险比例</div>
            <div class="ys-box-con">
              <pie-chart
                      :id="'ssa-global-risk-rate'"
                      :height="'250px'"
                      :name="'资产风险'"
                      :y.sync="AssetRiskData"
                      :rose="true"
                      :color="1"></pie-chart>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="global-full-page" v-show="globalFullStatus">
      <global-full-page :show.sync="globalFullStatus"></global-full-page>
    </div>
  </div>
</template>
<style scoped>
  .over-table{table-layout: fixed;} 
  .over-table td{
    width:100%;
    word-break:keep-all;/* 不换行 */
    white-space:nowrap;/* 不换行 */
    overflow:hidden;/* 内容超出宽度时隐藏超出部分的内容 */
    text-overflow:ellipsis;/* 当对象内文本溢出时显示省略标记(...) ；需与overflow:hidden;一起使用。*/
  }
  .global-title{
    width: 100%;
    position: relative;
  }
  .global-title .right{
    position:absolute;
    top:9px;
    right:10px;
  }
  .global-module-box{
    background:rgba(0,0,0,0.15);
    border-top:1px solid rgba(74,146,255,0.25);
  }
  .global-module-title{
    height:36px;
    line-height:36px;
    position: relative;
    padding-left:15px;
    font-size:14px;
  }
  .global-module-title:before{
    content:'';
    position: absolute;
    left:0px;
    width:154px;
    height:36px;
    background: url("../../../assets/images/ssa/global-box-title-corner.png") no-repeat;
    background-size:154px;
    z-index:0;
  }
  .security-grade-box{
    width:166px;
    height:153px;
    margin:0px auto;
    background: url("../../../assets/images/ssa/security-grade-bg-1.png") no-repeat;
    background-size:166px;
  }
  .security-grade-box .title{
    text-align:center;
    padding-top:50px;
  }
  .security-grade-box .grade{
    text-align:center;
    font-size:40px;
    margin-top:10px;
  }
  .global-module-con{
    padding:25px 0px;
  }
  .global-module-con .title-mark{
    display:inline-block;
    width:10px;
    height:10px;
    border-radius: 50%;
    background:#4a92ff;
    margin-right:5px;
  }
  .title-mark.blue{
    background:#4a92ff;
  }
  .title-mark.green{
    background:#00bd85;
  }
  .title-mark.red{
    background:#d75c56;
  }
  .title-mark.yellow{
    background:#cbae5f;
  }
  .module-list-box{
    margin-top:30px;
  }
  .module-list{
    display:inline-block;
  }
  .module-list li{
    float:left;
    margin-right:14px;
    position:relative;
    width:4px;
    height:77px;
  }
  .module-list li:last-child{
    margin-right:0px;
  }
  .module-list-single{
    width:4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    height:77px;
    background:#4a92ff;
    position:absolute;
    bottom:0px;
  }
  .module-list-single.blue{
    background:#4a92ff;
  }
  .module-list-single.green{
    background:#00bd85;
  }
  .module-list-single.red{
    background:#d75c56;
  }
  .module-list-single.yellow{
    background:#cbae5f;
  }
  .global-module-con .col-md-3,.global-module-con .col-md-4{
    padding:0px!important;
  }
</style>
<script>
  let screenfull =  require('screenfull/dist/screenfull');
  import globalFullPage from './ssa-global-full'
  import Api from 'src/lib/api'
  let echarts =  require('echarts/lib/echarts');
  export default {
    name: "",
    data() {
      return {
        globalFullStatus:false,
        lineData:{
          name:["严重","高","中","低"],
          x:[],
          color:['#8375d0',"#e96157","#e77d4e","#4a8aee"],
          series:[
            {data:[]},
            {data:[]},
            {data:[]},
            {data:[]},
          ]
        },
        securityGrade:0,
        loopHoleTop5Data:[],
        attackSourceData:[],
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
        AssetRiskData:[]
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
      }
    },
    ready: function() {
      let self=this;
      if(screenfull.enabled){
        screenfull.on('change', function() {
          if(!screenfull.isFullscreen){
            self.globalFullStatus=false;
          }
        });
      }
      this.getSecurityGrade()
      this.getLoopHoleTop5()
      this.getAttackSource()
      this.getDangerGrade()
      this.getAttackSerious()
      this.getAssetData()
      this.getAssetRisk()
    },
    methods:{
      changeValue(val){
        if (val < 1024) {
          return val+"b"
        } else if (val >= 1024 && val < 1024 * 1024) {
          val = (val / 1024).toFixed(1);
          return val+"Kb"
        } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
          val = (val / (1024 * 1024)).toFixed(1);
          return val+"Mb"
        } else if (val >= 1024 * 1024 * 1024) {
          val = (val / (1024 * 1024 * 1024)).toFixed(1);
          return val+"Gb"
        }
      },
      showFullScreen(){
        this.globalFullStatus=true;
        let width=window.screen.width;
        let height=window.screen.height;
        $("#global-full-page").css({"width":width+"px","height":height+"px"});
        const target = $('#global-full-page')[0];
        if (screenfull.enabled) {
          screenfull.request(target)
        }
      },
      getAssetData(){
        this.$http.get('/api/ssa/global/assets_overview').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data;
            this.networkData=data.network;
            this.serverData=data.server;
            this.appData=data.application;
            for(let a in this.networkData){
              this.networkData[a].new_data=[];
              for(let x in this.networkData[a].data.x){
                let height=77*(this.networkData[a].data.y[x]/Math.max.apply(null, this.networkData[a].data.y));
                if(height<5){height=5}
                this.networkData[a].new_data.push({
                  name:this.networkData[a].data.x[x],
                  value:this.networkData[a].data.y[x],
                  height:height
                })
              }
            }
            for(let a in this.serverData){
              this.serverData[a].new_data=[];
              for(let x in this.serverData[a].data.x){
                let height=77*(this.serverData[a].data.y[x]/Math.max.apply(null, this.serverData[a].data.y));
                if(height<5){height=5}
                this.serverData[a].new_data.push({
                  name:this.serverData[a].data.x[x],
                  value:this.serverData[a].data.y[x],
                  height:height
                })
              }
            }
            for(let a in this.appData){
              this.appData[a].new_data=[];
              for(let x in this.appData[a].data.x){
                let height=77*(this.appData[a].data.y[x]/Math.max.apply(null, this.appData[a].data.y));
                if(height<5){height=5}
                this.appData[a].new_data.push({
                  name:this.appData[a].data.x[x],
                  value:this.appData[a].data.y[x],
                  height:height
                })
              }
            }

          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getSecurityGrade(){
        this.$http.get('/api/ssa/global/security_overview').then(function (response) {
          if (response.data.status == 200) {
            this.securityGrade=response.data.data.security_mark;
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getLoopHoleTop5(){
        this.$http.get('/api/ssa/global/loophole_top5').then(function (response) {
          if (response.data.status == 200) {
            this.loopHoleTop5Data=response.data.data;
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
            this.attackSourceData=response.data.data.pie;
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
            let dangerGradeStateChart = echarts.init(document.getElementById('ssa-global-danger-grade-state'));
            let dangerGradeStateOption = {
              radar: {
                shape: 'polygon',
                name: {
                  textStyle: {
                    color: '#93a6d8',
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
                    color:"rgba(74, 146, 255, 0.05)",
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
                  color:"rgba(233,97,87,0.2)"
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
            dangerGradeStateChart.setOption(dangerGradeStateOption);
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })

      },
      getAttackSerious(){
        this.$http.get('/api/ssa/global/attack_rating').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data;
            this.lineData.x=data.x;
            this.lineData.series[0].data=data.serious;
            this.lineData.series[1].data=data.high;
            this.lineData.series[2].data=data.middle;
            this.lineData.series[3].data=data.low;
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getAssetRisk(){
        this.$http.get('/api/ssa/global/assets_risk').then(function (response) {
          if (response.data.status == 200) {
            this.AssetRiskData=response.data.data;
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
    },
    watch:{
      'globalFullStatus':function(){
        if(this.globalFullStatus==false){
          screenfull.exit();
        }
      }
    },
    components: {
      globalFullPage
    }
  }
</script>
