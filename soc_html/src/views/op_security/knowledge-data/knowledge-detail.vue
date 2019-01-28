<style scoped>
  .mirror{
    transform:rotate(180deg);
  }
  .textLineHeight{ line-height:1.4em; }
  table{ }
  table tr td{ padding:10px; text-align:left; }
  table tr input{ width:220px; }
  table tr textarea{ width:100%; min-width:220px; }
  table tr:first-child td{ padding-top:0 }
  table tr:last-child td{ padding-bottom:0 }
  table tr td:nth-child(odd){ padding-left:0; width:8em; white-space:nowrap; word-break:keep-all; text-wrap:none; color:#93a6d8; }
  table tr td:last-child{ padding-right:0; }
</style>
<template>
  <div class="ys-box">
    <a @click="href('knowledge-mgt')"><i class="ys-icon icon-arrow-right-circle mirror"></i><span class="m-l-5">返回知识库</span></a>
    <div class="pos-r m-t-10">
      <div class="box-left" style="margin-right:223px;">
        <div class="ys-box m-t-5" :data="detailData">
          <div class="ys-box-title clearfix">知识点详情
            <div class="d-i-b fRight">
              <a @click="href('knowledge-edit',detailData.id)"><i class="ys-icon ys-icon icon-edit m-r-3"></i>编辑</a>
              <ys-poptip confirm title="您确认此选项吗？" :placement="'right'" @on-ok="deleteThisItem(detailData.id)" @on-cancel="">
                <a class="m-l-20"><i class="ys-icon icon-trash m-r-3"></i>删除</a>
              </ys-poptip>
            </div>
          </div>
          <div class="ys-box-con">
            <p>
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span v-text="detailData.title">...</span>
            </p>
            <div class="ys-box-con m-t-10">
              <table class="fullWidth">
                <tr>
                  <td>添加人:</td>
                  <td v-text="detailData.user">...</td>
                  <td>分类:</td>
                  <td v-text="detailData.type">...</td>
                </tr>
                <tr>
                  <td>编辑时间:</td>
                  <td v-text="detailData.update_time">...</td>
                  <td>Tag标签:</td>
                  <td v-text="detailData.tag">...</td>
                </tr>
              </table>
            </div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>知识内容</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.content"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>关联实体</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.relate"> ...</div>
            <p class="d-i-b m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>应用场景类别: </span>
            </p>
            <div class="d-i-b m-t-20 m-l-10" v-html="detailData.scene"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>应用现象描述</span>
            </p>
            <div class="ys-box-con m-t-10 textLineHeight" v-html="detailData.description"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>信息研判</span>
            </p>
            <div class="ys-box-con m-t-10" v-html="detailData.decide"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>运维操作</span>
            </p>
            <div class="ys-box-con m-t-10" v-html="detailData.operate"> ...</div>
            <p class="m-t-20">
              <i class="ys-icon icon-title m-r-5 ys-primary-color"></i><span>结果反馈</span>
            </p>
            <div class="ys-box-con m-t-10" v-html="detailData.feedback"> ...</div>
          </div>
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
                  <p class="font12">{{list.title}}</p>
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
                  <p class="font12">{{list.name}}</p>
                  <div class="ys-info-color">{{list.search_time}}<span class="m-l-10"></span>
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
  import editor from "../module/editor.vue";
  export default {
    name:'private-node-mgt',
    data () {
      return {
        "lastAddPort":"api/op_store/knowledge/last_add",
        "lastSearchPort":"/api/op_store/knowledge/last_search",
        "deletePort":"/api/op_store/knowledge/detail/",
        "detailPort":"/api/op_store/knowledge/detail/",
        "detailData":{},
        "recentAdd":[{
          "title":"...",
          "create_time":"..."
        }],
        "recentSearch":[{
          "name":"...",
          "search_time":"..."
        }],
      }
    },
    ready:function(){
      this.initPage();
    },
    methods:{
      "href":function(_path){
        this.$router.go({"name":_path});
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
      initDetail:function(){
        this.$http.get(this.detailPort+this.$route.params.id,{}).then(function(response){
          if(Number(response.data.status)===200){
            this.detailData=response.data["data"];
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
        this.initLastAdd();
        this.initLastSearch();
        this.initDetail();
      },
      deleteThisItem:function(_id){
        this.$http.delete(this.deletePort+_id,{}).then(function(response){
          if(Number(response.data.status)===200){
            this.$root.errorMsg="删除成功!";
            this.$root.alertSuccess=true;
            this.href('knowledge-mgt');
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
      editor
    },
    mounted:function(){
    }
  }
</script>
