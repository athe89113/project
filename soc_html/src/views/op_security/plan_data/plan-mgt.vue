<style scoped>
  .m-l-1{ margin-left:1px; border-left:1px solid rgba(255, 255, 255, 0.05) }
  .m-t-3{ margin-top:3px; }
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
  .levelImg{ display:inline-block; width:76px; height:100px; line-height:120px; font-size:16px; text-align:center; }
  .levelImg.l1{ background:url("../../../assets/images/envelope.png") 0 0 no-repeat; }
  .levelImg.l2{ background:url("../../../assets/images/envelope.png") -76px 0 no-repeat; }
  .levelImg.l3{ background:url("../../../assets/images/envelope.png") -152px 0 no-repeat; }
  .levelImg.l4{ background:url("../../../assets/images/envelope.png") -228px 0 no-repeat; }
  .ellipsis{ text-overflow:ellipsis; overflow:hidden; word-break:keep-all; white-space:nowrap; }
  .clearAfter:after{ clear:both; }
  .groupBy{ -webkit-user-select:none; }
  .groupBy:before{ content:"\E854"; display:inline-block; width:1.25em; height:1.25em; line-height:1.25em; vertical-align:middle; text-align:center; margin-right:5px; font-family:"ys"; }
  .groupBy.up:before{ content:'\E81E'; background:rgba(0, 0, 0, 0.3); }
  .groupBy.down:before{ content:'\E824'; background:rgba(0, 0, 0, 0.3); }
</style>
<template>
  <div class="ys-box">
    <div class="pos-r">
      <button class="ys-btn fRight" @click="href('plan-add')">
        <i class="ys-icon icon-add-circle"></i>添加新预案
      </button>
      <div class="clearfix"></div>
    </div>
    <div class="pos-r m-t-10">
      <div class="box-left" style="margin-right:223px;">
        <div class="ys-box-con">
          <div>
            <div class="fLeft">
              <div class="ys-search d-i-b">
                <input type="text" placeholder="输入关键词查询" class="ys-input" style="width:180px;" v-model="searchInput" @keyup.enter="searchRun">
                <button class="ys-search-btn" @click="searchRun">
                  <i class="ys-icon icon-search"></i>
                </button>
              </div>
              <div class="ys-info-color d-i-b  disableText">
                <p class="d-i-b activeTagData vTop break">
                  <span class="d-i-b m-r-5">标签搜索:</span>
                  <span class="ys-primary-color tag" v-for="list in currentTags">{{list}}</span>
                  <a class="d-i-b m-l-5 m-r-40 toggleTagSelectorButton" @click="toggleTagSelector"><i class="ys-icon icon-edit"></i></a>
                </p>
              </div>
            </div>
            <div class="fRight">
              <div class="groupByBox d-i-b">
                <a class="groupBy groupByTimeButton" data-sort="update_time" @click="groupByThis"><span>时间</span></a>
                <span class="m-l-20"></span>
                <a class="groupBy groupByNameButton" data-sort="title" @click="groupByThis"><span>名称</span></a>
              </div>
              <ys-select :option="levelSelectData" :selected.sync="currentLevelSelect" :searchable="false" :filter="true" :width="75" @change="levelSelectChange"></ys-select>
            </div>
            <div class="clearfix"></div>
          </div>
          <div class="topPanel p-10 m-t-2 displayNone tagSelector" id="tagSelector">
            <checkbox v-for="list in tagData" :show.sync="list.selected" :text="list.text" @click="selectTag"></checkbox>
          </div>
          <ul class="m-t-10 resultList">
            <li class="pos-r displayTable ys-box-con fullWidth" v-for="list in searchResult">
              <div class="displayCell" style="width:1%;">
                <div class="levelImg " :class="reLevelClass(list.level)" v-text="list.level+'级'"></div>
              </div>
              <div class="displayCell vTop p-l-10 p-r-5">
                <p v-html="list.title"></p>
                <p class="ys-info-color">
                  <span>添加人：</span><span v-html="list.user">...</span><span class="m-l-40">最后编辑时间：</span><span v-text="list.update_time">...</span><span class="m-l-40">标签：</span><span v-text="list.tag">...</span><span class="m-l-40">等级：</span><span :style="{color:levelColor(list.level).color}" v-html="list.level+'级'">...</span>
                </p>
                <div class="break m-t-5 ys-info-color">
                  <div class="fLeft">简介：</div>
                  <div class="textLineHeight" v-html="list.brief">....</div>
                </div>
              </div>
              <div class="displayCell vMiddle textRight  m-l-1 p-l-0 noBreak" style="width:10em;">
                <a @click="href('plan-edit',list.id)"><i class="ys-icon ys-icon icon-edit m-r-3"></i></a>
                <ys-poptip confirm title="您确认此选项吗？" :placement="'right'" @on-ok="deleteThisItem(list.id)" @on-cancel="">
                  <a class="m-l-20"><i class="ys-icon icon-trash"></i></a>
                </ys-poptip>
                <a class="m-l-20" @click="href('plan-detail',list.id)"><i class="ys-icon icon-eye m-r-3"></i></a>
              </div>
            </li>
          </ul>
          <table-data :url='resultPort' v-ref:result_ref :data.sync="searchResult" :search.sync="search_word" :filter="resultFilter"></table-data>
        </div>
      </div>
      <div class="box-right" style="width:218px">
        <div class="ys-box">
          <div class="ys-box-title">最新添加</div>
          <div class="ys-box-con" style="height:370px;">
            <div class="ys-timeline">
              <div class="time-item" v-for="list in recentAdd" v-show="$index<5">
                <span class="time-icon ys-primary-color"><i class="ys-icon icon-clock"></i></span>
                <div class="item-info">
                  <p class="font12 ellipsis" v-text="list.title+' ('+list.level+')'" style="width:170px;"></p>
                  <div class="ys-info-color">{{list.create_time}}<span class="m-l-10"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="ys-box m-t-5">
          <div class="ys-box-title">最近搜索</div>
          <div class="ys-box-con" style="height:370px;">
            <div class="ys-timeline">
              <div class="time-item" v-for="list in recentSearch" v-show="$index<5">
                <span class="time-icon ys-primary-color"><i class="ys-icon icon-clock"></i></span>
                <div class="item-info">
                  <p class="font12 ellipsis" v-text="list.name" style="width:170px"></p>
                  <div class="ys-info-color">{{list.search_time}}<span class="m-l-10"></span>
                  </div>
                </div>
              </div>
            </div>
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
        "attrPort":"/api/op_store/plan/attr",
        "resultPort":"/api/op_store/plan/dts",
        "lastAddPort":"/api/op_store/plan/last_add",//最近添加
        "lastSearchPort":"/api/op_store/plan/last_search",//最近搜索
        "deletePort":"/api/op_store/plan/detail/",
        "search_word":"",//
        "searchInput":"",//输入框输入
        //"typeData":[],//标签页头/类别
        "resultFilter":{
          "tag":{"id":""},//已选标签
          "sort_col":{"id":''},//title|update_time
          "sort":{"id":0}, //0 不排序  1 降序 2 升序
          "level":{"id":""}//级别:1,2,3,4
        },
        "recentAdd":[{
          "title":"...",
          "level":"...",
          "create_time":"..."
        }],
        "recentSearch":[{
          "name":"...",
          "search_time":"..."
        }],
        "searchResult":[{"atk_type":"ddos"},{"atk_type":"dns"}],
        "tagData":[{
          "text":"...",
          "selected":false
        },{
          "text":"...",
          "selected":false
        }],
        levelSelectData:[],
        currentLevelSelect:{},
        "currentTags":[],
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
      initForm:function(){
        let data={};
        let self=this;
        this.$http.get(this.attrPort,data).then(function(response){
          if(Number(response.data.status)===200){
            self.tagData=[];
            self.levelSelectData=[{"id":"","name":"所有级别"}];
            let i=0;
            for(i; i<response.data["data"]["tag"].length; i++){
              self.tagData.push({
                "text":response.data["data"]["tag"][i],
                "selected":false
              });
            }
            for(i=0; i<response.data["data"]["level"].length; i++){
              self.levelSelectData.push({
                "id":response.data["data"]["level"][i].toString(),
                "name":response.data["data"]["level"][i].toString()+"级"
              });
            }
            self.currentLevelSelect=self.levelSelectData[0];
          }
          else{
            this.$root.alertError=true;
            this.$root.errorMsg=response.data.msg
          }
        },function(response){
          Api.user.requestFalse(response,this);
        });
      },
      initData:function(){
        this.initForm();
        this.initLastAdd();
        this.initLastSearch();
      },
      initLastAdd:function(){
        let data={};
        this.$http.get(this.lastAddPort,data).then(function(response){
          if(Number(response.data.status)===200){
            this.recentAdd=response.data["data"];
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
      reLevelClass:function(_level){
        return 'l'+_level;
      },
      typeSvgPath:function(_type){
        let thisColor=this.typeColor(_type);
        return '<div class="vMiddle" style="width:135px;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 36" width="102" height="36" class="vMiddle displayIB" ><path d="M3.5.5h97l-8,17,8,17H3.5a2.92,2.92,0,0,1-3-2.83V3.33A2.92,2.92,0,0,1,3.5.5Z" style="fill: '+thisColor.fill+'; stroke: '+thisColor.stroke+'; stroke-miterlimit: 10;"></path></svg><span style="float:left; margin-top:-24px;margin-left:10px;width:75px;font-size:12px;" class="threeDot">'+_type+'</span></div>';
      },
      searchRun:function(){
        this.search_word=this.searchInput;
        this.$refs.result_ref.search=this.search_word;
        this.tableRe();
      },
      clickType:function(e){
        let $thisLi=$(e.target).closest("li");
        $thisLi.find("a").addClass("on").end().siblings().find("a").removeClass("on");
        this.resultFilter.type.id=$.trim($thisLi.text());
        if(this.resultFilter.type.id==="全部") this.resultFilter.type.id="";
        this.searchInput="";
        this.search_word=this.searchInput;
        this.resultFilter.tag.id='';
        this.currentTags=[];
        let i=0;
        for(i; i<this.tagData.length; i++){
          this.tagData[i]["selected"]=false;
        }
        $("#letterBox").find("a.current").removeClass("current");
        this.resultFilter.letter.id="";
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
      clickGroupBy:function(e){
        let $this=$(e.target.closest("a.groupBy"));
        $this.siblings().removeClass("up").removeClass("down");
        if($this.hasClass("up")){
          $this.removeClass("up").addClass("down");
        }
        else if($this.hasClass("down")){
          $this.removeClass("down");
        }
        else{
          $this.addClass("up");
        }
      },
      groupByThis:function(e){
        this.clickGroupBy(e);
        let $this=$(e.target).closest("a");
        let self=this;
        let runThis=function(){
          self.resultFilter.sort_col.id=$this.attr("data-sort");
          if($this.hasClass("up")){
            self.resultFilter.sort.id=2;
          }
          else if($this.hasClass("down")){
            self.resultFilter.sort.id=1;
          }
          else{
            self.resultFilter.sort.id=0;
          }
          self.searchRun();
        };
        setTimeout(runThis,100);
      },
      levelSelectChange:function(){
        let self=this;
        setTimeout(function(){
          self.resultFilter.level.id=self.currentLevelSelect.id;
          self.searchRun();
        },50);
      },
      selectTag:function(e){
        let self=this;
        let $this=$(e.target.closest(".ys-checkbox"));
        let thisText=$.trim($this.text());
        let runThis=function(){
          self.resultFilter.tag.id="";
          self.currentTags=[];
          let i=0;
          for(i; i<self.tagData.length; i++){
            if(self.tagData[i]["text"]===thisText) self.tagData[i]["selected"]=$this.hasClass("on");
            if(self.tagData[i]["selected"]) self.currentTags.push(self.tagData[i]["text"]);
          }
          self.resultFilter.tag.id=self.currentTags.join(",");
          self.searchRun();
        };
        setTimeout(runThis,100);
      },
      tableRe:function(){
        this.$refs.result_ref.Re();
      },
      deleteThisItem:function(_id){
        this.$http.delete(this.deletePort+_id,{}).then(function(response){
          if(Number(response.data.status)===200){
            this.$root.errorMsg="删除成功!";
            this.$root.alertSuccess=true;
            this.tableRe();
          }
          else{
            this.$root.errorMsg=response.data.msg;
            this.$root.alertError=true;
          }
        },function(response){
          Api.user.requestFalse(response,this);
        });
      }
    },
    ready:function(){
      this.initData();
    }
  }
</script>
