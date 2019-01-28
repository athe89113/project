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
  .bigTable tr td:nth-child(odd){ width:1%; white-space:nowrap; }
  .bigTable tr td:first-child{ padding-left:0; white-space:nowrap; word-break:keep-all; text-wrap:none; }
  .bigTable tr td:last-child{ padding-right:0; }
  .tableUl{ display:table; width:100%; }
  .tableUl li{ display:table-row-group; height:40px; }
  .tableUl li div.itemEdit{ display:none; }
  .tableUl li div.itemInfo{ display:table-row; height:40px; }
  .tableUl li.edit div.itemEdit{ display:table-row; height:40px; }
  .tableUl li.edit div.itemInfo{ display:none; }
  .tableUl li.th p{ text-align:center; background:rgba(0, 0, 0, 0.3); height:40px; }
  .tableUl li p{ padding:2px 10px; display:table-cell; vertical-align:middle; text-align:center; background:rgba(0, 0, 0, 0.1); }
  .tableUl li p:first-child{ text-align:center; width:4em; }
  .tableUl li p input{ width:100%; }
</style>
<template>
  <div class="ys-box">
    <a @click="href('plan-mgt')"><i class="ys-icon icon-arrow-right-circle mirror"></i><span class="m-l-5">返回预案库</span></a>
    <div class="pos-r m-t-10">
      <div class="box-left" style="margin-right:223px;">
        <div class="ys-box m-t-5">
          <div class="ys-box-title">添加新预案</div>
          <div class="ys-box-con">
            <table class="bigTable">
              <tr>
                <td>预案名称:</td>
                <td>
                  <input class="ys-input" placeholder="输入知识点名称" v-model="submitData.title" /><!--<span>*必选项</span>-->
                </td>
                <td>添加人:</td>
                <td>
                  <input class="ys-input" placeholder="输入编辑人姓名" v-model="submitData.user" /><!--<span>*必选项</span>-->
                </td>
              </tr>
              <tr>
                <td>预案等级:</td>
                <td>
                  <ys-select :option="levelSelectData" :selected.sync="currentLevelSelect" :searchable="false" :width="220" @change="levelSelectChange"></ys-select>
                </td>
                <td>添加场景:</td>
                <td>
                  <ys-select :option="sceneData" :selected.sync="currentSceneSelect" :searchable="false" :width="220" @change="sceneSelectChange"></ys-select>
                </td>
              </tr>
              <tr>
                <td>TAG标签:</td>
                <td colspan="3">
                  <tagator :width="220" :list="tagInput"></tagator><!--<span>*必选项</span>-->
                </td>
              </tr>
              <tr>
                <td>预案简介:</td>
                <td colspan="3">
                  <textarea class="ys-textarea" placeholder="" v-model="submitData.brief"></textarea>
                </td>
              </tr>
              <tr>
                <td>详细内容:</td>
                <td colspan="3">
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
                <td>相关联系人:</td>
                <td colspan="3">
                  <ul class="tableUl">
                    <li class="th">
                      <p></p>
                      <p>联系人</p>
                      <p>电话</p>
                      <p>邮箱地址</p>
                      <p>操作</p>
                    </li>
                    <li v-for="list in contactData">
                      <div class="itemEdit">
                        <p v-text="$index+1"></p>
                        <p>
                          <input class="ys-input" placeholder="输入姓名" v-model="editInput.name" />
                        </p>
                        <p>
                          <input class="ys-input" placeholder="输入电话" v-model="editInput.phone" />
                        </p>
                        <p>
                          <input class="ys-input" placeholder="输入邮箱" v-model="editInput.email" />
                        </p>
                        <p class="noBreak">
                          <a class="m-r-10 submitEdit" @click="editContactControl($event,$index)"><i class="ys-icon icon-check-circle m-r-3"></i><span class="font12">确定</span></a>
                          <a class="m-r-10 cancelEdit" @click="editContactControl($event,$index)"><i class="ys-icon icon-clear-circle m-r-3"></i><span class="font12">取消</span></a>
                        </p>
                      </div>
                      <div class="itemInfo">
                        <p v-text="$index+1"></p>
                        <p v-text="list.name"></p>
                        <p v-text="list.phone"></p>
                        <p v-text="list.email"></p>
                        <p class="noBreak">
                          <a class="edit" @click="editThisContact($event,$index)"><i class="ys-icon icon-edit"></i></a>
                          <ys-poptip :placement="'right'" :confirm="true" :title="'确认删除该联系人吗？'" @on-ok="deleteThisContact($index)">
                            <a class="m-l-20 delete"><i class="ys-icon icon-trash"></i></a>
                          </ys-poptip>
                        </p>
                      </div>
                    </li>
                    <li>
                      <p></p>
                      <p>
                        <input class="ys-input" placeholder="输入姓名" v-model="addInput.name" />
                      </p>
                      <p>
                        <input class="ys-input" placeholder="输入电话" v-model="addInput.phone" />
                      </p>
                      <p>
                        <input class="ys-input" placeholder="输入邮箱" v-model="addInput.email" />
                      </p>
                      <p>
                        <button class="ys-btn ys-btn-blue fRight m-r-10" @click="addContact">
                          <i class="ys-icon icon-add-circle"></i>添加联系人
                        </button>
                      </p>
                    </li>
                  </ul>
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
                  <p class="font12 ellipsis" v-text="list.title+' ('+list.level+')'" style="width:170px;"></p>
                  <div class="ys-info-color">{{list.create_time}}<span class="m-l-10"></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="ys-box m-t-5">
          <div class="ys-box-title">热门预案</div>
          <div class="ys-box-con" style="height:370px;">
            <div class="ys-timeline">
              <div class="time-item" v-for="list in hotList" v-show="$index<5">
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
  <ys-modal :show.sync="addSuccess" :title="'信息提示'">
    <div slot="content">
      <p>添加成功! 请问要继续添加吗?</p>
    </div>
    <div slot="footer">
      <button class="ys-btn" type="button" @click="initPage()">
        <span>继续添加</span>
      </button>
      <button class="ys-btn ys-btn-white m-l-20" type="button" @click="href('plan-mgt')">
        <span>返回预案库</span>
      </button>
    </div>
  </ys-modal>
</template>
<script>
  import editor from "../module/editor.vue";
  /* import "/static/js/ueditor/third-party/codemirror/codemirror.js";
   import "/static/js/ueditor/third-party/codemirror/codemirror.css";*/
  /*  require("/js/ueditor/ueditor.config.js");
   require("/js/ueditor/ueditor.all.js");
   require("/js/ueditor/lang/zh-cn/zh-cn.js");*/
  /* import "/static/js/ueditor/ueditor.parse.js";*/
  /*require('src/assets/js/wangeditor');*/
  /*require('https://unpkg.com/wangeditor/release/wangEditor.min.js');*/
  //require('./assets/js/wangeditor/release/wangEditor.js')
  export default {
    name:'private-node-mgt',
    data () {
      return {
        "attrPort":"/api/op_store/plan/attr",
        "lastAddPort":"/api/op_store/plan/last_add",//最近添加
        "hotPort":"/api/op_store/plan/hot",
        "addPort":"/api/op_store/plan/add",
        tableFilter:{"id":""},
        "recentAdd":[{
          "title":"...",
          "level":"...",
          "create_time":"..."
        }],
        "hotList":[{
          "name":"...",
          "search_time":"..."
        }],
        levelSelectData:[],
        currentLevelSelect:{},
        "sceneData":[],
        currentSceneSelect:{},
        "tagInput":[],//已输入的标签
        sceneInput:{},//应用场景下拉菜单当前选项
        contentHtml:'',
        relateHtml:'',
        submitData:{
          title:"",// 名称 
          user:"",// 添加人 
          level:"",//级别，
          scene:"",//应用场景
          tag:"",//标签 逗号分割
          brief:"",//简介
          description:'',//内容
          contact:'',//管理员用户id 逗号分割
        },
        contactData:[],//[{phone: "--", name: "--", email: "--"}],
        editInput:{
          "name":"",
          "phone":"",
          "email":""
        },
        addInput:{
          "name":"",
          "phone":"",
          "email":""
        },
        validator:{
          Name:/^[A-Za-z0-9\/\_\-\u0391-\uFFE5]{1,1024}$/,
          Email:/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/,
          Phone:/^((\(\d{3}\))|(\d{3}\-))?(\(0\d{2,3}\)|0\d{2,3}-)?[1-9]\d{6,7}$/,
          Mobile:/^((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)$/
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
      initForm:function(){
        let data={};
        let self=this;
        this.$http.get(this.attrPort,data).then(function(response){
          if(Number(response.data.status)===200){
            //self.typeData=response.data["data"]["type"];
            //tag标签,添加页面暂不需要
            self.tagData=[];
            let i=0;
            for(i; i<response.data["data"]["tag"].length; i++){
              self.tagData.push({
                "text":response.data["data"]["tag"][i],
                "selected":false
              });
            }
            //添加场景重置
            self.sceneData=[];
            for(i=0; i<response.data["data"]["scene"].length; i++){
              self.sceneData.push({
                "id":response.data["data"]["scene"][i].toString(),
                "name":response.data["data"]["scene"][i].toString()
              });
            }
            //预案等级重置
            self.levelSelectData=[];
            for(i=0; i<response.data["data"]["level"].length; i++){
              self.levelSelectData.push({
                "id":response.data["data"]["level"][i].toString(),
                "name":response.data["data"]["level"][i].toString()+"级"
              });
            }
            setTimeout(function(){
              self.currentSceneSelect=self.sceneData[0];
              self.currentLevelSelect=self.levelSelectData[0];
            },200);
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
      initHot:function(){
        let data={};
        let self=this;
        this.$http.get(this.hotPort,data).then(function(response){
          if(Number(response.data.status)===200){
            this.hotList=response.data["data"];
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
        this.sceneInput={};
        this.contactData=[];//[{phone: "--", name: "--", email: "--"}],
        this.editInput={
          "name":"",
          "phone":"",
          "email":""
        };
        this.addInput={
          "name":"",
          "phone":"",
          "email":""
        };
        this.submitData={
          title:"",// 名称 
          user:"",// 添加人 
          level:"",//级别，
          scene:"",//应用场景
          tag:"",//标签 逗号分割
          brief:"",//简介
          description:'',//内容
          contact:'',// 逗号分割
        };
        this.$root.alertError=false;
        this.contentHtml='';
        this.initForm();
        this.initLastAdd();
        this.initHot();
      },
      userArrToString:function(arr){
        let newArr=[];
        for(let i=0; i<arr.length; i++){
          if(arr[i]["name"]!=='--') newArr.push(arr[i]["name"]+"&"+arr[i]["phone"]+"&"+arr[i]["email"]);
        }
        return newArr.join(",");
      },
      validateContact:function(_data){
        let success=false;
        if(this.validator.Name.test(_data.name)===false){
          this.$root.alertError=true;
          this.$root.errorMsg="联系人姓名输入错误";
          success=false;
        }
        else if(this.validator.Mobile.test(_data.phone)===false){
          this.$root.alertError=true;
          this.$root.errorMsg="电话输入错误";
          success=false;
        }
        else if(this.validator.Email.test(_data.email)===false){
          this.$root.alertError=true;
          this.$root.errorMsg="邮箱输入错误";
          success=false;
        }
        else{
          this.$root.alertError=false;
          this.$root.errorMsg="";
          success=true;
        }
        return success;
      },
      editContactControl:function(e,_id){
        let $this=$(e.target).closest("a");
        if($this.hasClass("submitEdit")){
          if(!this.validateContact(this.editInput)) return false;
          this.contactData.splice(_id,1,{
            "name":this.editInput.name,
            "phone":this.editInput.phone,
            "email":this.editInput.email
          });
          this.editInput={
            "name":"",
            "phone":"",
            "email":""
          };
        }
        else if($this.hasClass("cancelEdit")){
          $this.closest("li").removeClass("edit");
        }
      },
      addContact:function(){
        if(!this.validateContact(this.addInput)) return false;
        this.contactData.push({
          "name":this.addInput.name,
          "phone":this.addInput.phone,
          "email":this.addInput.email
        });
        this.addInput={
          "name":"",
          "phone":"",
          "email":""
        };
      },
      editThisContact:function(e,_id){
        let $thisLi=$(e.target).closest("li");
        $thisLi.addClass("edit");
        this.editInput.name=this.contactData[_id].name;
        this.editInput.phone=this.contactData[_id].phone;
        this.editInput.email=this.contactData[_id].email;
      },
      deleteThisContact:function(_id){
        this.contactData.splice(_id,1);
      },
      submitPage:function(){
        /*let submitData={
         title:"",// 名称 
         user:"",// 添加人 
         type:"",//选择的分类ID， 
         content:"",//内容  
         relate:"",//关联内容  
         scene:"",// 应用场景  
         description:"",// 现象描述
         operate:"",// 运维操作  
         decide:"",// 信息研判  
         feedback:""//结果反馈
         };*/
        //this.submitData.title=this.submitData.title;
        //this.submitData.user=this.submitData.user;
        this.submitData.level=this.currentLevelSelect.id;
        this.submitData.scene=this.currentSceneSelect.id;
        this.submitData.tag=this.tagInput.join(",");
        //this.submitData.brief= this.submitData.brief;
        this.submitData.description=this.contentHtml;
        this.submitData.contact=this.userArrToString(this.contactData);
        let errsLength=0;
        let errInfo={
          "title":"请输入预案名称",
          "user":"请输入添加人",
          "level":"请选择预案等级",
          "scene":"请选择添加场景",
          "tag":"请输入TAG标签",
          "brief":"请输入预案简介",
          "description":"请输入详细内容",
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
              self.$root.alertError=true;
              self.$root.errorMsg=response.data.msg
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
