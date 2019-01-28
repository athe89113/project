<style scoped>
  .m-l-1{ margin-left:1px; border-left:1px solid rgba(255, 255, 255, 0.05) }
  .m-t-3{ margin-top:3px; }
  .ellipsis{ text-overflow:ellipsis; overflow:hidden; word-break:keep-all; white-space:nowrap; }
  .selected{ background:#2c2831; }
  .disableText{ -webkit-user-select:none; -moz-user-select:none; -ms-user-select:none; user-select:none }
  .radius3{ border-radius:3px; }
  .textLineHeight{ line-height:1.4em; }
  .toggleTagSelectorButton{ display:inline-block; padding:0; width:1.6em; line-height:1.6em; text-align:center; border-radius:3px; }
  .tagSelector{ line-height:2em; text-align:left; }
  .tagSelector .ys-checkbox:not(:last-child){ margin-right:20px; }
  .letterBox a{ display:inline-block; padding:0.5em 0; width:1.6em; line-height:0.6em; text-align:center; }
  .letterBox a.current{ border-radius:3px; background-color:#2c2831; }
  .letterBox a:first-child{ }
  .activeTagData span.tag:not(:last-child):after{ content:","; margin:0 5px 0 2px; }
  .resultList li:not(:first-child){ margin-top:5px; }
  .topPanel{ background:#2c2831; border-radius:3px; box-shadow:0 3px 5px rgba(0, 0, 0, 0.4); }
</style>
<template>
  <div class="ys-box">
    <div class="pos-r">
      <div class="box-left" style="margin-right:223px;" :url='typePort' :data-sync="typeData">
        <ul class="ys-nav">
          <li @click="clickType">
            <a class="on" data-id="">
              <span class="ys-nav-cor"></span>
              <span class="text">全部</span>
            </a>
          </li>
          <li v-for="list in typeData" @click="clickType">
            <a :data-id="list.id">
              <span class="ys-nav-cor"></span>
              <span class="text" v-text="list.data_source">{{list.data_source}}</span>
            </a>
          </li>
          <div class="clearfix"></div>
        </ul>
      </div>
      <div class="box-right"></div>
    </div>
    <div class="pos-r">
      <div class="box-left" style="margin-right:223px;">
        <div class="ys-box-con">
          <div>
            <div class="fRight">
              <span class="m-l-20 m-r-5 ys-info-color">时间范围</span>
              <calendar :type="'date'" :text="'开始日期'" :value.sync="searchDateRange.start_date"></calendar>
              <span class="m-l-5 m-r-5 ys-info-color">至</span>
              <calendar :type="'date'" :text="'结束日期'" :value.sync="searchDateRange.end_date"></calendar>
              <button style="width:75px;" id="get-waf-log" class="ys-btn m-l-10" @click="searchRun()">查询</button>
            </div>
            <div class="ys-search d-i-b">
              <input type="text" placeholder="输入关键词查询" class="ys-input" style="width:180px;" v-model="searchInput" @keyup.enter="searchRun">
              <button class="ys-search-btn" @click="searchRun">
                <i class="ys-icon icon-search"></i>
              </button>
            </div>
            <div class="ys-info-color  disableText">
              <p class="d-i-b activeTagData vTop break m-t-10">
                <!--<span class="d-i-b m-r-5">标签搜索:</span>
                <span class="ys-primary-color tag" v-for="list in resultFilter.tag.id">{{list}}</span>
                <a class="d-i-b m-l-5 m-r-40 toggleTagSelectorButton" @click="toggleTagSelector"><i class="ys-icon icon-edit"></i></a>-->
              </p>
              <p class="d-i-b letterBox vTop break m-t-10" id="letterBox">
                <!--<span class="d-i-b m-r-5">字母搜索:</span>
                <a v-for="letter in letterData" @click="clickLetter">{{letter}}</a>-->
              </p>
            </div>
            <div class="topPanel p-10 m-t-2 displayNone tagSelector" id="tagSelector">
              <checkbox v-for="list in tagData" :show.sync="list.selected" :text="list.text" @click="selectTag"></checkbox>
            </div>
          </div>
          <ul class="m-t-10 resultList">
            <li class="displayTable ys-box-con fullWidth" v-for="list in searchResult">
              <div class="displayCell" style="width:1%;">
                <div style="margin-left:-15px;" v-html="flagSvgPath(list.level,list.vul_nam)"></div>
              </div>
              <div class="displayCell vTop p-l-5 p-r-5">
                <p v-text="list.vul_nam"></p>
                <p class="ys-info-color break">
                  <span class="d-i-b m-r-40 noBreak">发布时间：{{list.publish_date}}</span><span class="d-i-b m-r-40 noBreak">来源：{{list.source_name}}</span><span class="d-i-b m-r-40 noBreak">编码：{{list.vul_id}}</span><span class="d-i-b m-r-40 noBreak">危害等级：{{list.level}}</span><span class="d-i-b m-r-40 noBreak">漏洞类型：{{list.type}}</span><span class="d-i-b m-r-40 noBreak">威胁类型：{{list.attack_type}}</span>
                </p>
                <p class="ys-info-color break">
                  <span>漏洞简介：</span><span v-text="list.description"></span>
                </p>
              </div>
              <div class="displayCell vMiddle m-l-1 p-l-0 noBreak" style="width:1%;">
                <a class="m-l-20" @click="href('hole-detail',list.id)"><i class="ys-icon icon-eye m-r-3"></i>详情</a>
              </div>
            </li>
          </ul>
          <table-data :url='resultPort' v-ref:result_ref :data.sync="searchResult" :search.sync="search_word" :filter="resultFilter"></table-data>
        </div>
      </div>
      <div class="box-right" style="width:218px">
        <div class="ys-box">
          <div class="ys-box-title">最近搜索</div>
          <div class="ys-box-con" style="height:370px;">
            <div class="ys-timeline">
              <div class="time-item" v-for="list in recentSearch" v-show="$index<5">
                <span class="time-icon ys-primary-color"><i class="ys-icon icon-clock"></i></span>
                <div class="item-info">
                  <p class="font12 ellipsis" style="width:170px;" :title='list.name+"["+list["vul_id"]+"]"' v-text='list.name+"["+list["vul_id"]+"]"'></p>
                  <div class="ys-info-color">{{list.search_time}}<span class="m-l-10"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="ys-box m-t-5">
          <div class="ys-box-title">最新高危漏洞</div>
          <div class="ys-box-con" style="height:370px;">
            <ul class="textLineHeight">
              <li class="m-b-10 ellipsis" v-for="list in lastDangerData" v-show="$index<5" :style='{width:"188px", color:levelColor(list.level).color}' :title='list["vul_name"]+"["+list["vul_id"]+"]"'>
                <i class="ys-icon icon-warning-three m-r-5"></i>{{list["vul_name"]}}[{{list["vul_id"]}}]
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <ys-modal :show.sync="addSuccess" :title="'信息提示'">
      <div slot="content">
        <p>添加成功!</p>
      </div>
      <div slot="footer">
        <button class="ys-btn" type="button">
          <span>继续添加</span>
        </button>
        <button class="ys-btn" type="button">
          <span>返回知识库</span>
        </button>
      </div>
    </ys-modal>
  </div>
</template>
<script>
  import Checkbox from "../../../components/checkbox";
  export default {
    components:{Checkbox},
    name:'private-node-mgt',
    data () {
      return {
        "typePort":"/api/op_store/vul/data_source",//类别
        "resultPort":"/api/op_store/vul/dts",//列表
        "lastDangerPort":"/api/op_store/vul/last_high_vul",//最新高危漏洞
        "lastSearchPort":"/api/op_store/vul/last_search",//最近搜索
        "deletePort":"/api/op_store/knowledge/detail/",
        "search_word":"",//
        "searchInput":"",//输入框输入
        "typeData":[],//标签页头/类别
        searchDateRange:{
          "start_date":"",
          "end_date":""
        },
        "resultFilter":{
          "data_source":{"id":0},//已选的类型,0代表全部
          "start_date":{"id":""},
          "end_date":{"id":""}
          /*"tag":{"id":[]},//已选标签
           "letter":{"id":""}//已选的字母*/
        },
        "lastDangerData":[{
          "title":"...",
          "create_time":"..."
        }],
        "recentSearch":[{
          "name":"...",
          "search_time":"..."
        }],
        "searchResult":[{"atk_type":"ddos"},{"atk_type":"dns"}],
        "tagData":[{
          "text":"SQL",
          "selected":false
        },{
          "text":"DNS",
          "selected":false
        }],
        "letterData":["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
        "addSuccess":false
      }
    },
    methods:{
      "href":function(_path,_id){
        this.$router.go({
          "name":_path,
          params:{id:_id ? _id : ''}
        });
      },
      "removeHTMLTag":function(_str,_length){
        let length=60||_length;
        let str=_str||'';
        str=str.replace(/<\/?[^>]*>/g,''); //去除HTML tag
        str=str.replace(/[ | ]*\n/g,'\n'); //去除行尾空白
        //str = str.replace(/\n[\s| | ]*\r/g,'\n'); //去除多余空行
        str=str.replace(/&nbsp;/ig,'');//去掉&nbsp;
        str=str.replace(/\s/g,''); //将空格去掉
        return str.substr(0,length)+(str.length>length ? '...' : '');
      },
      initData:function(){
        this.initType();
        this.initLastAdd();
        this.initLastSearch();
      },
      initType:function(){
        let data={};
        let self=this;
        this.$http.get(this.typePort,data).then(function(response){
          if(Number(response.data.status)===200){
            self.typeData=response.data["data"];
            if(typeof(response.data["data"]["tag"])!=="undefined"){
              self.tagData=[];
              let i=0;
              for(i; i<response.data["data"]["tag"].length; i++){
                self.tagData.push({
                  "text":response.data["data"]["tag"][i],
                  "selected":false
                });
              }
            }
          }
          else{
            this.$root.alertError=true;
            this.$root.errorMsg=response.data.msg
          }
        },function(response){
          Api.user.requestFalse(response,this);
        });
      },
      initLastAdd:function(){
        let data={};
        this.$http.get(this.lastDangerPort,data).then(function(response){
          if(Number(response.data.status)===200){
            this.lastDangerData=response.data["data"];
          }
          else{
            this.$root.alertError=true;
            this.$root.errorMsg=response.data.msg
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      initLastSearch:function(){
        let data={};
        let self=this;
        this.$http.get(this.lastSearchPort,data).then(function(response){
          if(Number(response.data.status)===200){
            this.recentSearch=response.data["data"];
          }
          else{
            this.$root.alertError=true;
            this.$root.errorMsg=response.data.msg
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
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
      flagSvgPath:function(_n,_text){
        let thisColor=this.levelColor(_n);
        return '<div class="vMiddle" style="width:135px;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 36" width="102" height="36" class="vMiddle displayIB" ><path d="M3.5.5h97l-8,17,8,17H3.5a2.92,2.92,0,0,1-3-2.83V3.33A2.92,2.92,0,0,1,3.5.5Z" style="fill: '+thisColor.fill+'; stroke: '+thisColor.stroke+'; stroke-miterlimit: 10;"></path></svg><span style="float:left; margin-top:-24px;margin-left:10px;width:75px;font-size:12px;" class="threeDot">'+_text+'</span></div>';
      },
      searchRun:function(){
        this.search_word=this.searchInput;
        this.$refs.result_ref.search=this.search_word;
        this.resultFilter.start_date.id=this.searchDateRange.start_date;
        this.resultFilter.end_date.id=this.searchDateRange.end_date;
        this.tableRe();
      },
      clickType:function(e){
        let $thisLi=$(e.target).closest("li");
        $thisLi.find("a").addClass("on").end().siblings().find("a").removeClass("on");
        this.resultFilter.data_source.id=Number($thisLi.find("a").attr("data-id"));
        this.searchInput="";
        this.searchDateRange.start_date="";
        this.searchDateRange.end_date="";
        this.search_word=this.searchInput;
        this.resultFilter.start_date.id=this.searchDateRange.start_date;
        this.resultFilter.end_date.id=this.searchDateRange.end_date;
        this.tableRe();
      },
      toggleTagSelector:function(e){
        let $this=$(e.target).closest("a");
        let $tagSelector=$("#tagSelector");
        if($tagSelector.is(":visible")){
          $this.removeClass("selected");
          $tagSelector.hide();
        }
        else{
          $this.addClass("selected");
          $tagSelector.show();
        }
      },
      clickLetter:function(e){
        let $this=$(e.target).closest("a");
        if($this.hasClass("current")){
          $this.removeClass("current");
        }
        else{
          $this.addClass("current").siblings().removeClass("current");
        }
        this.searchRun();
      },
      selectTag:function(e){
        let self=this;
        let $this=$(e.target.closest(".ys-checkbox"));
        let thisText=$.trim($this.text());
        let runThis=function(){
          self.resultFilter.tag.id=[];
          let i=0;
          for(i; i<self.tagData.length; i++){
            if(self.tagData[i]["text"]===thisText) self.tagData[i]["selected"]=$this.hasClass("on");
            if(self.tagData[i]["selected"]) self.resultFilter.tag.id.push(self.tagData[i]["text"]);
          }
          self.searchRun();
        };
        setTimeout(runThis,100);
      },
      tableRe:function(){
        this.$refs.result_ref.Re();
      }
    },
    ready:function(){
      this.initData();
    }
  }
</script>
