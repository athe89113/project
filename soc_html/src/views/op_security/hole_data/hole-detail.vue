<style scoped>
  .mirror{
    transform:rotate(180deg);
  }
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
</style>
<template>
  <div class="ys-box">
    <a @click="href('hole-mgt')"><i class="ys-icon icon-arrow-right-circle mirror"></i><span class="m-l-5">返回漏洞库</span></a>
    <div class="pos-r m-t-10">
      <div class="box-left" style="margin-right:295px;">
        <div class="ys-box m-t-5" :data="detailData">
          <div class="ys-box-title clearfix">漏洞详情
            <div class="d-i-b fRight">
              <!--<a @click="href('knowledge-edit',detailData.id)"><i class="ys-icon ys-icon icon-edit m-r-3"></i>编辑</a>
              <ys-poptip confirm title="您确认此选项吗？" :placement="'right'" @on-ok="deleteThisItem(detailData.id)" @on-cancel="">
                <a class="m-l-20"><i class="ys-icon icon-trash m-r-3"></i>删除</a>
              </ys-poptip>-->
            </div>
          </div>
          <div class="ys-box-con">
            <p>
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span v-text="detailData.vul_name">...</span>
            </p>
            <div class="ys-box-con m-t-10">
              <table class="fullWidth">
                <tr>
                  <td>编&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码:</td>
                  <td v-text="detailData.vul_id">...</td>
                  <td>危害等级:</td>
                  <td v-text="detailData.vul_level">...</td>
                </tr>
                <tr>
                  <td>漏洞来源:</td>
                  <td v-text="detailData.vul_type">...</td>
                  <td>严重评分:</td>
                  <td>
                    <span v-text="detailData.score"></span><a class="m-l-5" :class=" reScoreLinkClass(detailData.score)" @click="href('hole-score',detailData.id)">详细评分体系</a>
                  </td>
                </tr>
                <tr>
                  <td>发布时间:</td>
                  <td v-text="detailData.publish_date">...</td>
                  <td>漏洞类型:</td>
                  <td v-text="detailData.vul_type">...</td>
                </tr>
                <tr>
                  <td>更新时间:</td>
                  <td v-text="detailData.update_date">...</td>
                  <td>威胁类型:</td>
                  <td v-text="detailData.attack_type">...</td>
                </tr>
                <tr>
                  <td>影响组件:</td>
                  <td v-text="detailData.impact">...</td>
                  <td>漏洞作者:</td>
                  <td v-text="detailData.impact">...</td>
                </tr>
                <tr>
                  <td>修复补丁:</td>
                  <td v-text="detailData.patch">...</td>
                  <td>厂&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;商:</td>
                  <td v-text="detailData.firm">...</td>
                </tr>
              </table>
            </div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>漏洞简介</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.description"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>漏洞公告</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.advice"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>受影响范围</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.range"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>受影响实体</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.impact"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>修复建议</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.suggest"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>厂商补丁</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.patch"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>参考信息</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.reference"> ...</div>
          </div>
        </div>
      </div>
      <div class="box-right" style="width:290px">
        <div class="ys-box">
          <div class="ys-box-title">
            <i class="ys-icon icon-menu-search ys-primary-color font20 vMiddle"></i><span>快速搜索</span>
          </div>
          <div class="ys-box-con" style="height:200px;">
            <table>
              <tr>
                <td>漏洞名称:</td>
                <td>
                  <input type="text" placeholder="输入关键词查询" class="ys-input" style="width:180px;" v-model="searchInputName">
                </td>
              </tr>
              <tr>
                <td>漏洞编码:</td>
                <td>
                  <input type="text" placeholder="输入关键词查询" class="ys-input" style="width:180px;" v-model="searchInputCode">
                </td>
              </tr>
              <tr>
                <td>发布时间:</td>
                <td>
                  <div>
                    <calendar :type="'date'" :text="'开始日期'" :value.sync="searchDateRange.start_date" :width="78" :place="'right'"></calendar>
                    <span class="m-l-3 m-r-3 ys-info-color">至</span>
                    <calendar :type="'date'" :text="'结束日期'" :value.sync="searchDateRange.end_date" :width="78" :place="'right'"></calendar>
                  </div>
                </td>
              </tr>
              <tr>
                <td></td>
                <td>
                  <button style="width:55px;" class="ys-btn ys-btn-blue" @click="searchRun()">搜索</button>
                  <button style="width:55px;" class="ys-btn ys-btn-white m-l-10" @click="searchReset()">重置</button>
                </td>
              </tr>
            </table>
          </div>
        </div>
        <div class="ys-box m-t-5">
          <div class="ys-box-title">相关漏洞</div>
          <div class="ys-box-con" style="height:370px;">
            <ul class="textLineHeight">
              <li class="m-b-10 ellipsis" v-for="list in aboutData" v-show="$index<5" :style='{width:"260px", color:levelColor(list.level).color}' :title='list["vul_name"]+"["+list["vul_id"]+"]"'>
                <i class="ys-icon icon-warning-three m-r-5"></i>{{list["vul_name"]}}[{{list["vul_id"]}}]
              </li>
            </ul>
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
        "aboutPort":"/api/op_store/vul/similar/",
        "detailPort":"/api/op_store/vul/detail/",
        "searchPort":"/api/op_store/vul/quick_search",
        "searchInputName":"",
        "searchInputCode":"",
        searchDateRange:{
          "start_date":"",
          "end_date":""
        },
        "detailData":{},
        "aboutData":[]
      }
    },
    ready:function(){
      this.initPage();
    },
    methods:{
      "href":function(_path,_id){
        this.$router.go({
          "name":_path,
          params:{id:_id ? _id : ''}
        });
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
      initAbout:function(_type){
        let data={};
        this.$http.get(this.aboutPort+_type,{}).then(function(response){
          if(Number(response.data.status)===200){
            this.aboutData=response.data["data"];
          }
          else{
            this.$root.alertError=true;
            this.$root.errorMsg=response.data.msg
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      initDetail:function(){
        this.$http.get(this.detailPort+this.$route.params.id,{}).then(function(response){
          if(Number(response.data.status)===200){
            this.detailData=response.data["data"];
            this.initAbout(this.detailData.vul_type);
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
        this.initDetail();
      },
      searchReset:function(){
        this.searchInputName="";
        this.searchInputCode="";
        this.searchDateRange.start_date="";
        this.searchDateRange.end_date="";
        this.initDetail();
      },
      searchRun:function(){
        let searchData={};
        searchData.vul_name=this.searchInputName;
        searchData.vul_id=this.searchInputCode;
        searchData.start_date=this.searchDateRange.start_date;
        searchData.end_date=this.searchDateRange.end_date;
        if(this.searchInputName===""&&this.searchInputCode===""&&this.searchDateRange.start_date===""&&this.searchDateRange.end_date==="") return false;
        this.$http.post(this.searchPort,searchData).then(function(response){
          if(Number(response.data.status)===200){
            this.detailData=response.data["data"];
            this.initAbout(this.detailData.vul_type);
          }
          else{
            this.$root.alertError=true;
            this.$root.errorMsg=response.data.msg
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
    },
    components:{}
  }
</script>
