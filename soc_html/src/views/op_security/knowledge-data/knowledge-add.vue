<style scoped>
  .mirror{
    transform:rotate(180deg);
  }
  .bigTable{ }
  .bigTable tr td{ padding:10px; text-align:left; }
  .bigTable tr input{ width:220px; }
  .bigTable tr textarea{ width:100%; min-width:220px; }
  .bigTable tr:first-child td{ padding-top:0 }
  .bigTable tr:last-child td{ padding-bottom:0 }
  .bigTable tr td:first-child{ padding-left:0; width:8em; white-space:nowrap; word-break:keep-all; text-wrap:none; }
  .bigTable tr td:last-child{ padding-right:0; }
</style>
<template>
  <div class="ys-box">
    <a @click="href('knowledge-mgt')"><i class="ys-icon icon-arrow-right-circle mirror"></i><span class="m-l-5">返回知识库</span></a>
    <div class="pos-r m-t-10">
      <div class="box-left" style="margin-right:223px;">
        <div class="ys-box m-t-5">
          <div class="ys-box-title">添加新知识点</div>
          <div class="ys-box-con">
            <table class="bigTable">
              <tr>
                <td>知识点名称:</td>
                <td>
                  <input class="ys-input" placeholder="输入知识点名称" v-model="submitData.title" /><!--<span>*必选项</span>-->
                </td>
              </tr>
              <tr>
                <td>添加人:</td>
                <td>
                  <input class="ys-input" placeholder="输入编辑人姓名" v-model="submitData.user" /><!--<span>*必选项</span>-->
                </td>
              </tr>
              <tr>
                <td>分类:</td>
                <td>
                  <ys-select :option="typeData" :width="220" :selected.sync="typeInput"></ys-select><!--<span>*必选项</span>-->
                </td>
              </tr>
              <tr>
                <td>TAG标签:</td>
                <td>
                  <tagator :width="400" :list="tagInput"></tagator><!--<span>*必选项</span>-->
                </td>
              </tr>
              <tr>
                <td>知识内容:</td>
                <td>
                  <editor :data.sync="contentHtml" :id="'contentHtml'"></editor>
                  <!--<span>*必选项</span>-->
                  <!--<div id="editor" type="text/plain" style="width:100%;height:500px;"></div>
                  <div class="m-t-10">
                    <button class="ys-btn" @click="submits">保存</button>
                    <button class="ys-btn m-l-20" @click="xieru">写入一段文字</button>
                  </div>-->
                </td>
              </tr>
              <tr>
                <td>关联实体:</td>
                <td>
                  <editor :data.sync="relateHtml" id="relateHtml"></editor><!--<span>*必选项</span>-->
                </td>
              </tr>
              <tr>
                <td>应用场景类别:</td>
                <td>
                  <ys-select :option="sceneData" :width="220" :selected.sync="sceneInput"></ys-select>
                </td>
              </tr>
              <tr>
                <td>现象描述:</td>
                <td>
                  <textarea class="ys-textarea" placeholder="本知识点关联运维事件的现象描述" v-model="submitData.description"></textarea>
                </td>
              </tr>
              <tr>
                <td>信息研判:</td>
                <td>
                  <textarea class="ys-textarea" placeholder="本知识点关联运维事件的信息研判" v-model="submitData.decide"></textarea>
                </td>
              </tr>
              <tr>
                <td>运维操作:</td>
                <td>
                  <textarea class="ys-textarea" placeholder="与本知识点关联运维事件的运维操作步骤及说明" v-model="submitData.operate"></textarea>
                </td>
              </tr>
              <tr>
                <td>结果反馈:</td>
                <td>
                  <textarea class="ys-textarea" placeholder="与本知识点关联运维事件运维后结果反馈" v-model="submitData.feedback"></textarea>
                </td>
              </tr>
            </table>
            <div class="m-t-10 m-b-10">
              <button class="ys-btn m-r-10" @click="submitPage">保存</button>
              <button class="ys-btn ys-btn-white m-r-10" @click="href('knowledge-mgt')">取消</button>
            </div>
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
  <ys-modal :show.sync="addSuccess" :title="'信息提示'">
    <div slot="content">
      <p>添加成功! 请问要继续添加吗?</p>
    </div>
    <div slot="footer">
      <button class="ys-btn" type="button" @click="initPage()">
        <span>继续添加</span>
      </button>
      <button class="ys-btn ys-btn-white m-l-20" type="button" @click="href('knowledge-mgt')">
        <span>返回知识库</span>
      </button>
    </div>
  </ys-modal>
</template>
<script>
  import editor from "../module/editor.vue";
  export default {
    name:'private-node-mgt',
    data () {
      return {
        "typePort":"/api/op_store/knowledge/attr",
        "lastAddPort":"api/op_store/knowledge/last_add",
        "lastSearchPort":"/api/op_store/knowledge/last_search",
        "addPort":"/api/op_store/knowledge/add",
        tableFilter:{"id":""},
        "recentAdd":[{
          "title":"...",
          "create_time":"..."
        }],
        "recentSearch":[{
          "name":"...",
          "search_time":"..."
        }],
        "typeData":[],
        "sceneData":[{
          id:"排障处理",
          name:"排障处理"
        },{
          id:"断电应急",
          name:"断电应急"
        },{
          id:"攻击响应",
          name:"攻击响应"
        }],
        "tagInput":[],//已输入的标签
        typeInput:{},//分类当前选项
        sceneInput:{},//应用场景下拉菜单当前选项
        contentHtml:'',
        relateHtml:'',
        submitData:{
          title:"",// 名称 
          user:"",// 添加人 
          type:"",//选择的分类ID， 
          tag:"",//标签
          content:"",//内容  
          relate:"",//关联内容  
          scene:"",// 应用场景  
          description:"",// 现象描述
          operate:"",// 运维操作  
          decide:"",// 信息研判  
          feedback:""//结果反馈
        },
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
      initEditor:function(){
        /*var E=window.wangEditor;
         var editor=new E('#editor');
         // 或者 var editor = new E( document.getElementById('editor') )
         editor.create();*/
        /*this.ue=UE.getEditor('editor',{
         BaseUrl: '',
         UEDITOR_HOME_URL: '/static/js/ueditor',
         // toolbars:[] 
         });*/
      },
      initType:function(){
        let data={};
        let self=this;
        this.$http.get(this.typePort,data).then(function(response){
          if(Number(response.data.status)===200){
            self.typeData=response.data["data"]["type"];
            self.typeData=[];
            let i=0;
            for(i; i<response.data["data"]["type"].length; i++){
              self.typeData.push({
                "id":response.data["data"]["type"][i],
                "name":response.data["data"]["type"][i]
              });
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
      initPage:function(){
        this.addSuccess=false;
        this.tagInput=[];//已输入的标签
        this.typeInput={};
        this.sceneInput={};
        this.submitData={
          title:"",// 名称 
          user:"",// 添加人 
          type:"",//选择的分类ID， 
          tag:"",//标签
          content:"",//内容  
          relate:"",//关联内容  
          scene:"",// 应用场景  
          description:"",// 现象描述
          operate:"",// 运维操作  
          decide:"",// 信息研判  
          feedback:""//结果反馈
        };
        this.$root.alertError=false;
        this.initEditor();
        this.contentHtml='';
        this.relateHtml='';
        this.initType();
        this.initLastAdd();
        this.initLastSearch();
      },
      submitPage:function(){
        this.submitData.tag=this.tagInput.join(",");
        this.submitData.content=this.contentHtml;
        this.submitData.relate=this.relateHtml;
        this.submitData.scene=this.sceneInput.name;
        this.submitData.type=this.typeInput.name;
        let errsLength=0;
        let errInfo={
          "title":"请输入知识点名称",
          "user":"请输入添加人",
          "type":"请选择分类",
          "tag":"请输入TAG标签",
          "content":"请输入知识内容",
          "relate":"请输入关联实体"
        };
        for(let k in this.submitData){
          if(typeof(errInfo[k])!=="undefined"&&(!this.submitData[k]||this.submitData[k]==="")){
            errsLength+=1;
            this.$root.errorMsg=errInfo[k];
            break;
          }
        }
        if(errsLength>0){
          this.$root.alertError=true;
        }
        else{
          let self=this;
          this.$http.post(this.addPort,this.submitData).then(function(response){
            if(Number(response.data.status)===200){
              this.addSuccess=true;
            }
            else{
              this.$root.alertError=true;
              this.$root.errorMsg=response.data.msg
            }
          },function(response){
            Api.user.requestFalse(response,this);
          })
        }
      }
    },
    components:{
      editor
    },
    mounted:function(){
    }
  }
</script>
