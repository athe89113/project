<style scoped>
  .mirror{
    transform:rotate(180deg);
  }
  .displayNone{ display:none; }
  .textLineHeight{ line-height:1.4em; }
  .bigTable{ width:100%; }
  .bigTable tr td{ padding:10px; text-align:left; }
  .bigTable tr input{ width:220px; }
  .bigTable tr textarea{ width:100%; min-width:220px; }
  .bigTable tr:first-child td{ padding-top:0 }
  .bigTable tr:last-child td{ padding-bottom:0 }
  .bigTable tr td:nth-child(odd){ width:1%; white-space:nowrap; }
  .bigTable tr td:first-child{ padding-left:0; white-space:nowrap; word-break:keep-all; text-wrap:none; }
  .bigTable tr td:last-child{ padding-right:0; }
  .tableUl{ display:table; width:100%; }
  .tableUl li{ display:table-row; height:40px; }
  .tableUl li.th{ }
  .tableUl li.th p{ text-align:center; background:rgba(0, 0, 0, 0.3); }
  .tableUl li p{ padding:2px 10px; display:table-cell; vertical-align:middle; text-align:center; background:rgba(0, 0, 0, 0.1); }
  .tableUl li p:first-child{ text-align:center; width:4em; }
</style>
<template>
  <div class="ys-box">
    <a @click="href('plan-mgt')"><i class="ys-icon icon-arrow-right-circle mirror"></i><span class="m-l-5">返回预案库</span></a>
    <div class="pos-r m-t-10">
      <div class="box-left" style="margin-right:223px;">
        <div class="ys-box m-t-5">
          <div class="ys-box-title">处理预案详情
            <p class="d-i-b m-t-10 fRight">
              <a :class='downloadHref[0]==="#" ? "displayNone" : ""' :href.sync="downloadHref[0]" :target.sync="downloadHref[1]"><i class="ys-icon icon-download"></i></a><a class="m-l-20" @click="href('plan-edit',$route.params.id)"><i class="ys-icon icon-edit"></i></a>
              <ys-poptip confirm title="您确认此选项吗？" :placement="'right'" @on-ok="deleteThisItem(detailData.id)" @on-cancel="">
                <a class="m-l-20"><i class="ys-icon icon-trash"></i></a>
              </ys-poptip>
            </p>
          </div>
          <div class="ys-box-con">
            <p>
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span v-text="detailData.title">...</span>
            </p>
            <div class="ys-box-con m-t-10">
              <table class="bigTable">
                <tr>
                  <td class="ys-info-color">添加人:</td>
                  <td v-text="detailData.user"></td>
                  <td class="ys-info-color">预案等级:</td>
                  <td v-text="detailData.level+'级'" :style="{color:levelColor(detailData.level).color}"></td>
                </tr>
                <tr>
                  <td class="ys-info-color">编辑时间:</td>
                  <td v-text="detailData.update_time"></td>
                  <td class="ys-info-color">应用场景:</td>
                  <td v-text="detailData.scene"></td>
                </tr>
                <tr>
                  <td class="ys-info-color">TAG标签:</td>
                  <td v-text="detailData.tag"></td>
                  <td></td>
                  <td></td>
                </tr>
              </table>
            </div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>预案简介</span>
            </p>
            <div class="m-t-10 ys-box-con textLineHeight" v-html="detailData.brief"></div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>详细内容</span>
            </p>
            <div class="m-t-10 ys-box-con textLineHeight" v-html="detailData.description"></div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>相关联系人</span>
            </p>
            <ul class="m-t-10 tableUl">
              <li class="th">
                <p></p>
                <p>联系人</p>
                <p>电话</p>
                <p>邮箱地址</p>
              </li>
              <li v-for="list in detailData.contact">
                <p v-text="$index+1"></p>
                <p v-text="list.name"></p>
                <p v-text="list.phone"></p>
                <p v-text="list.email"></p>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="box-right" style="width:218px">
        <div class="ys-box">
          <div class="ys-box-title">热门预案</div>
          <div class="ys-box-con" style="height:370px;">
            <div class="ys-timeline">
              <div class="time-item" v-for="list in hotData" v-show="$index<5">
                <span class="time-icon ys-primary-color"><i class="ys-icon icon-clock"></i></span>
                <div class="item-info">
                  <p class="font12 ellipsis" v-text="list.name" style="width:170px;"></p>
                  <div class="ys-info-color">{{list.create_time}}<span class="m-l-10"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="ys-box m-t-5">
          <div class="ys-box-title">相关预案</div>
          <div class="ys-box-con" style="height:370px;">
            <div class="ys-timeline">
              <div class="time-item" v-for="list in aboutList" v-show="$index<5">
                <span class="time-icon ys-primary-color"><i class="ys-icon icon-clock"></i></span>
                <div class="item-info">
                  <p class="font12">{{list.name}}</p>
                  <div class="ys-info-color">{{list.create_time}}<span class="m-l-10"></span>
                  </div>
                </div>
              </div>
            </div>
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
        "detailPort":"/api/op_store/plan/detail/",
        "downloadPort":"/api/op_store/plan/load_pdf/",
        "deletePort":"/api/op_store/plan/detail/",
        "hotPort":"/api/op_store/plan/hot",//热门预案
        "aboutPort":"/api/op_store/plan/similar/",//相关预案
        "detailData":{
          brief:"",
          contact:[],
          description:"",
          id:0,
          level:0,
          scene:"",
          tag:[],
          title:"",
          type:0,
          user:"",
        },
        "hotData":[{
          "title":"...",
          "create_time":"..."
        }],
        "aboutList":[{
          "name":"...",
          "search_time":"..."
        }],
        downloadHref:['#',""],
        levelSelectData:[],
        currentLevelSelect:{},
        addSuccess:false
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
      sceneSelectChange:function(){
        let self=this;
        setTimeout(function(){
          self.submitData.scene=self.currentSceneSelect.id;
        },50);
      },
      levelSelectChange:function(){
        let self=this;
        setTimeout(function(){
          self.submitData.level=self.currentLevelSelect.id;
        },50);
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
      initDetail:function(){
        let id=this.$route.params.id;
        this.$http.get(this.detailPort+id,{}).then(function(response){
          if(Number(response.data.status)===200){
            this.detailData=response.data.data;
            //this.submitData=response.data["data"];
            //this.initAbout(this.detailData.vul_type);
            this.initAbout();
            this.download(id);
          }
          else{
            this.$root.alertError=true;
            this.$root.errorMsg=response.data.msg
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      initLastAdd:function(){
        let data={};
        this.$http.get(this.hotPort,data).then(function(response){
          if(Number(response.data.status)===200){
            this.hotData=response.data["data"];
          }
          else{
            this.$root.alertError=true;
            this.$root.errorMsg=response.data.msg
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      initAbout:function(){
        let data={};
        let self=this;
        this.$http.get(this.aboutPort+this.detailData.scene,data).then(function(response){
          if(Number(response.data.status)===200){
            this.aboutList=response.data["data"];
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
        this.initLastAdd();
      },
      download:function(_id){
        this.$http.get(this.downloadPort+_id,{}).then(function(response){
          if(Number(response.data.status)===200){
            //this.$root.successMsg="将为你输出pdf文档.";
            //this.$root.alertSuccess=true;
            this.downloadHref=[response.data.data.url,"_blank"];
          }
          else{
            this.$root.errorMsg=response.data.msg;
            this.$root.alertError=true;
          }
        },function(response){
          Api.user.requestFalse(response,this);
        });
      },
      deleteThisItem:function(_id){
        this.$http.delete(this.deletePort+_id,{}).then(function(response){
          if(Number(response.data.status)===200){
            this.$root.errorMsg="删除成功!";
            this.$root.alertSuccess=true;
            this.href("plan-mgt");
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
    components:{
      /*editor*/
    },
    mounted:function(){
    }
  }
</script>
