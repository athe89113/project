<style scoped>
  .mirror{
    transform:rotate(180deg);
  }
  .ys-btn-box{ font-size:0; }
  .ys-btn-box button.ys-btn{ border-radius:0; }
  .ys-btn-box button.ys-btn:first-child{ border-top-left-radius:3px; border-bottom-left-radius:3px; }
  .ys-btn-box button.ys-btn:last-child{ border-top-right-radius:3px; border-bottom-right-radius:3px; }
  .ys-btn-box button.ys-btn:not(:first-child):before{ content:"\200B"; display:inline-block; width:1px; line-height:1.25em; float:left; border-left:1px solid rgba(255, 255, 255, .3); margin-top:4px; margin-left:-12.5px; }
  button.ys-btn{ font-size:12px; }
  button.ys-btn.ys-btn-alpha{ background:rgba(0, 0, 0, 0.3); }
  .ys-btn-box button:hover{ cursor:auto; }
  .textLineHeight{ line-height:1.4em; }
  .ellipsis{ text-overflow:ellipsis; overflow:hidden; word-break:keep-all; white-space:nowrap; }
  table{ }
  table tr td{ padding:10px; text-align:left; }
  table tr input{ width:220px; }
  table tr textarea{ width:100%; min-width:220px; }
  table tr:first-child td{ padding-top:0 }
  table tr:last-child td{ padding-bottom:0 }
  table tr td:nth-child(odd){ padding-left:0; width:5em; white-space:nowrap; word-break:keep-all; text-wrap:none; color:#93a6d8; }
  table tr td:last-child{ padding-right:0; }
  .onlyRead{ position:relative; }
  .onlyRead:after{ content:"\200b"; display:block; position:absolute; left:0; top:0; width:100%; height:100%; background:rgba(0, 0, 0, 0.01); }
</style>
<template>
  <div class="ys-box">
    <a @click="href('hole-detail',$route.params.id)"><i class="ys-icon icon-arrow-right-circle mirror"></i><span class="m-l-5">返回漏洞详情</span></a>
    <div class="ys-box-con p-30 m-t-10">
      <span class="vMiddle" v-text="scoreData.vul_name"></span><span class="m-l-40 m-r-5 vMiddle ys-info-color">严重评分:</span><span class="font24 vMiddle" v-text="scoreData.score+'分'" :style='{color:levelColor(scoreData.level).color}'></span>
    </div>
    <div class="pos-r m-t-5">
      <div class="box-left" style="margin-right:295px;">
        <div class="ys-box-title clearix">厂商类别
          <div class="d-i-b fRight">
            <a class="ys-icon icon-downlist"></a>
          </div>
        </div>
        <div class="ys-box-con">
          <div class="onlyRead">
            <radio :list="factoryData" :value.sync="currentFactory"></radio>
          </div>
        </div>
        <div class="ys-box-title m-t-5 clearfix">基础分
          <div class="d-i-b fRight">
            <a class="ys-icon icon-downlist"></a>
          </div>
        </div>
        <div class="ys-box-con ys-info-color">
          <p>攻击向量 (AV)</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" :class="reCurrent(list,scoreData.base.AV)" v-for="list in baseData.AV" v-text="list">...</button>
          </div>
          <p class="m-t-15">权限要求 (PR)</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" :class="reCurrent(list,scoreData.base.PR)" v-for="list in baseData.PR" v-text="list">...</button>
          </div>
          <p class="m-t-15">机密性影星 (C)</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" :class="reCurrent(list,scoreData.base.C)" v-for="list in baseData.C" v-text="list">...</button>
          </div>
          <p class="m-t-15">完整性影响 (I)</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" :class="reCurrent(list,scoreData.base.I)" v-for="list in baseData.I" v-text="list">...</button>
          </div>
          <p class="m-t-15">可用性影响 (A)</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" :class="reCurrent(list,scoreData.base.A)" v-for="list in baseData.A" v-text="list">...</button>
          </div>
          <p class="m-t-15">攻击复杂度 (AC)</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" :class="reCurrent(list,scoreData.base.AC)" v-for="list in baseData.AC" v-text="list">...</button>
          </div>
          <p class="m-t-15">用户交互 (UI)</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" :class="reCurrent(list,scoreData.base.UI)" v-for="list in baseData.UI" v-text="list">...</button>
          </div>
          <p class="m-t-15">范围 (S)</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" :class="reCurrent(list,scoreData.base.S)" v-for="list in baseData.S" v-text="list">...</button>
          </div>
        </div>
        <div class="ys-box-title  m-t-5 clearfix">环境分
          <div class="d-i-b fRight">
            <a class="ys-icon icon-downlist"></a>
          </div>
        </div>
        <div class="ys-box-con ys-info-color">
          <p>修正攻击矢量 (MAV) </p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.MAV" :class="reCurrent(list,scoreData.environmental.MAV)" v-text="list">...</button>
          </div>
          <p class="m-t-15">完整性需求（IR） </p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.IR" :class="reCurrent(list,scoreData.environmental.IR)" v-text="list">...</button>
          </div>
          <p class="m-t-15">可能性需求（AR）</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.AR" :class="reCurrent(list,scoreData.environmental.AR)" v-text="list">...</button>
          </div>
          <p class="m-t-15">机密性需求（CR） </p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.CR" :class="reCurrent(list,scoreData.environmental.CR)" v-text="list">...</button>
          </div>
          <p class="m-t-15">修正权限需求（MPR） </p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.MPR" :class="reCurrent(list,scoreData.environmental.MPR)" v-text="list">...</button>
          </div>
          <p class="m-t-15">修正机密性影响（MC） </p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.MC" :class="reCurrent(list,scoreData.environmental.MC)" v-text="list">...</button>
          </div>
          <p class="m-t-15">修正完整性影响（MI） </p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.MI" :class="reCurrent(list,scoreData.environmental.MI)" v-text="list">...</button>
          </div>
          <p class="m-t-15">修正可用性影响（MA） </p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.MA" :class="reCurrent(list,scoreData.environmental.MA)" v-text="list">...</button>
          </div>
          <p class="m-t-15">修正攻击复杂度（MAC）</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.MAC" :class="reCurrent(list,scoreData.environmental.MAC)" v-text="list">...</button>
          </div>
          <p class="m-t-15">修正用户交互（MUI）</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.MUI" :class="reCurrent(list,scoreData.environmental.MUI)" v-text="list">...</button>
          </div>
          <p class="m-t-15">修正范围（MS）</p>
          <div class="ys-btn-box m-t-10">
            <button class="ys-btn" v-for="list in environmentalData.MS" :class="reCurrent(list,scoreData.environmental.MS)" v-text="list">...</button>
          </div>
        </div>
      </div>
      <div class="box-right" style="width:290px">
        <div class="ys-box">
          <div class="ys-box-title">什么是漏洞评分体系？</div>
          <div class="ys-box-con textLineHeight">
            为了客观的评估漏洞的严重程度，基于CVSS v3（Common Vulnerability Scoring System，即“通用漏洞评分系统”），并根据实际应用场景进行优化。
            <br><br> 为了解决漏洞评级各自为政的局面，解决漏洞的脆弱性、客观性、可重复性等问题。由NIAC（美国基础设施顾问委员会）提出了CVSS标准，并由FIRST组织进行维护。CVSS是一个“行业公开标准，它被设计用来评测漏洞的严重程度，并帮助应用者确定漏洞所需反应的紧急性和重要性”。
            <br><br> 盒子CVSS评估系统有评估指标和评估过程两大部分构成。评估指标分为三个组成部分，分别是基础分，环境分和厂商类型。
            <br><br> 漏洞的评分范围为0-10.0，分为严重（critical）、高（high）、中（medium）、低（low）四个级别。下表是评分范围与等级映射关系表。
            <br><br> • 严重：9.0-10.0<br> • 高：7.0-8.9<br> • 中：4.0-6.9<br> • 低：0-3.9<br>
            <br> CVSS的计算方式通过选择每个评估指标，按照一定的权重进行计算。首先用得到一个基础分，这个分数是漏洞评分的基础，也是必须存在的；然后在此基础上添加临时分，临时分与漏洞发布时间关系密切，因此非0day场景下可以选择not defined；最后再添加环境分，得到一个最终分数。
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name:'private-node-mgt',
    data () {
      return {
        "scorePort":"/api/op_store/vul/vul_score/",
        "scoreData":{
          "base":{
            A:"N",
            AC:"N",
            AV:"N",
            C:"N",
            I:"N",
            PR:"N",
            S:"U",
            UI:"N"
          },
          "environmental":{
            AR:"X",
            CR:"X",
            IR:"X",
            MA:"X",
            MAC:"X",
            MAV:"X",
            MC:"X",
            MI:"X",
            MPR:"X",
            MS:"X",
            MUI:"X",
          }
        },
        factoryData:[{
          id:1,
          text:"A类厂商"
        },{
          id:2,
          text:"B类厂商"
        },{
          id:3,
          text:"C类厂商"
        }],
        currentFactory:1,
        baseData:{
          "AV":["Network (N)","Adjacent (A)","Local (L)","Physical (P)"],
          "PR":["None (N)","Low (L)","High (H)"],
          "C":["None (N)","Low (L)","High (H)"],
          "I":["None (N)","Low (L)","High (H)"],
          "A":["None (N)","Low (L)","High (H)"],
          "AC":["Low (L)","High (H)"],
          "UI":["None (N)","Required (R)"],
          "S":["Unchanged (U)","Changed (C)"]
        },
        environmentalData:{
          "MAV":["Not Defined (X)","Network (N)","Adjacent Network (A)","Local (L)","Physical (P)"],
          "IR":["Not Defined (X)","Low (L)","Medium (M)","Local (L)","High (H)"],
          "AR":["Not Defined (X)","Low (L)","Medium (M)","Local (L)","High (H)"],
          "CR":["Not Defined (X)","Low (L)","Medium (M)","Local (L)","High (H)"],
          "MPR":["Not Defined (X)","Low (L)","Medium (M)","Local (L)","High (H)"],
          "MC":["Not Defined (X)","Low (L)","Medium (M)","Local (L)","High (H)"],
          "MI":["Not Defined (X)","Low (L)","Medium (M)","Local (L)","High (H)"],
          "MA":["Not Defined (X)","Low (L)","Medium (M)","Local (L)","High (H)"],
          "MAC":["Not Defined (X)","Low (L)","Local (L)","High (H)"],
          "MUI":["Not Defined (X)","None (N)","Required (R)"],
          "MS":["Not Defined (X)","Unchanged (U)","Changed (C)"]
        }
      }
    },
    ready:function(){
      this.initPage();
    },
    methods:{
      "href":function(_path){
        this.$router.go({"name":_path});
      },
      "reScoreLinkClass":function(_score){
        return /^\d+\.*\d*$/.test(_score) ? '' : 'displayNone'
      },
      levelColor:function(_n){
        let n="_"+_n;
        let reColor=function(_rgb){
          return {
            color:'rgba('+_rgb+',1)',
            stroke:'rgba('+_rgb+',0.5)',
            fill:'rgba('+_rgb+',0.05)'
          }
        };
        let rgb='';
        switch(n){
          case "_4" ://红
            rgb='233,97,87';
            break;
          case "_3" ://黄
            rgb="218,187,97";
            break;
          case "_2" ://绿
            rgb="0,189,133";
            break;
          case "_1" ://蓝
            rgb="74,146,255";
            break;
          default ://蓝
            rgb="74,146,255";
            break;
        }
        return reColor(rgb);
      },
      reCurrent:function(_thisText,_thisValue){
        let getValue=_thisText.substring(_thisText.indexOf("(")+1,_thisText.indexOf(")"));
        return _thisValue===getValue ? "ys-btn-blue" : "ys-btn-alpha";
      },
      initScore:function(){
        this.$http.get(this.scorePort+this.$route.params.id,{}).then(function(response){
          if(Number(response.data.status)===200){
            this.scoreData=response.data["data"];
          }
          else{
            this.$root.alertError=true;
            this.$root.errorMsg=response.data.msg
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      initPage:function(){
        this.addSuccess=false;
        this.$root.alertError=false;
        this.initScore();
      },
    },
    components:{}
  }
</script>
