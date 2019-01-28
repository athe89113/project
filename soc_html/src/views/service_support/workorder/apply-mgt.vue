<template>
  <div class="ys-box">
    <div class="ys-box-con">
      <div class="tool-box">
        <div class="fLeft d-i-b">
          <button class="ys-btn" @click="showAdd"><i class="ys-icon icon-add-circle"></i>创建工单</button>
        </div>
        <div class="fRight d-i-b">
          <div class="ys-search d-i-b m-l-10">
            <input type="text" placeholder="输入关键词查询"
                   v-model="searchValue"
                   @keyup.enter="tableRe"
                   class="ys-input" style="width:180px;"/>
            <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
          </div>
        </div>
      </div>
      <table class="ys-table m-t-10">
        <thead>
        <tr>
          <th>标题</th>
          <th>申请人</th>
          <th>处理人</th>
          <th>状态</th>
          <th>回复</th>
          <th>提交时间</th>
        </tr>
        </thead>
        <tbody>
        <tr v-bind:class="[$index%2==1 ? 'even' : 'odd' ]" v-for="list in tableList">
          <td>
            <a @click="showInfo(list.id)">{{list.title}}</a>
          </td>
          <td>{{list.applier}}</td>
          <td>{{list.handler}}</td>
          <td v-if="list.status=='未处理'" class="ys-error-color">{{list.status}}</td>
          <td v-if="list.status=='已处理'" class="ys-success-color">{{list.status}}</td>
          <td>{{list.is_replied}}</td>
          <td>{{list.create_time}}</td>
        </tr>
        </tbody>
      </table>
      <table-data :url='tableUrl'
                  :data.sync="tableList"
                  :filter.sync="tableFilter"
                  :search.sync="searchValue"
                  v-ref:table></table-data>
    </div>
    <aside :show.sync="configStatus"
           :header="configHead"
           :left="'auto'"
           :width="'600px'">
      <div>
        <div class="ys-box m-t-10">
          <div class="ys-box-title">填写工单基本信息</div>
          <div class="ys-box-con">
            <table class="ys-set-table">
              <tbody>
                <tr>
                  <td>工单标题</td>
                  <td><input
                          class="ys-input"
                          v-model="workOrder.title"
                          style="width: 218px">
                  </td>
                </tr>
                <tr>
                  <td>描述</td>
                  <td>
                    <textarea class="ys-input"
                              style="width: 400px; height: 200px"
                              v-model="workOrder.content"></textarea>
                  </td>
                </tr>
                <tr>
                  <td>添加附件</td>
                  <td>
                    <div class="row nomargin m-t-10 snmpBox" >
                      <template v-for="img in imgData">
                        <div class="annexList" v-on:mouseenter="showIcons(img)" v-on:mouseleave="hideIcons(img)">
                          <a class="text-cursor preview" v-show="img.show" @click="previewImg(img)"><i
                                  class="glyphicon glyphicon-zoom-in font18"></i></a>
                          <a class="text-cursor delete" v-show="img.show" @click="deleteImg(img)"><i
                                  class="glyphicon glyphicon-remove font12"></i></a>
                          <img v-bind:src="img.src"/>
                        </div>
                      </template>
                      <div class="annexBox" id="selectImg" @click="selectImg" v-show="true">
                        <i class="glyphicon glyphicon-plus"></i>
                      </div>
                      <input id="img_input" type="file" accept="image/jpeg,image/gif,image/png,image/bmp"
                             style="display:none"/>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="aside-foot m-t-20">
          <button class="ys-btn m-r-10" @click="changeConfig()">确定</button>
          <button class="ys-btn ys-btn-white" @click="configStatus=false">取消</button>
        </div>
      </div>
    </aside>
    <aside :show.sync="infoStatus"
           :header="'工单详情'"
           :left="'auto'"
           :width="'800px'">
      <deal-info :order_id="orderInfoId" :target="'apply'"></deal-info>
    </aside>
  </div>
</template>
<script>
  import tableData from 'src/components/table-data.vue'
  import tableOpt from 'src/components/table-opt.vue'
  import ysSelect from 'src/components/select.vue'
  import aside from 'src/components/Aside.vue'
  import dealInfo from './deal-info-mgt.vue'
  export default {
    data() {
      return {
        tableUrl: '/api/ticket_apply/dts',
        tableList: [],
        tableFliter: {},
        searchValue: '',
        type:this.$route.params.type,
        clickType:"0",

        configStatus:false,
        configHead:"",

        checked: false,
        keyData: [],
        imgData: [],
        curImgSrc: '',
        workOrder: {
          title: "",
          content: ""
        },
        imgModal:false,

        //
        infoStatus:false,
        orderInfoId:"",
      }
    },
    ready: function() {
      let self = this
      $("#img_input").on("change", function (e) {
        e.preventDefault()
        var file = e.target.files[0]; //获取图片资源
        if (!file.type.match('image.*')) {
          alert("请选择正确格式的文件!")
          return false;
        }// 只选择图片文件
        var reader = new FileReader();
        reader.readAsDataURL(file); // 读取文件
        reader.onload = function (arg) {
          self.uploadImg(arg)
        }// 渲染文件
      });
    },
    methods:{
      tableRe(){
        this.$refs.table.Re()
      },
      showAdd(){
        this.configStatus=true;
        this.configHead="创建工单";
        this.keyData=[];
        this.imgData=[];
        this.curImgSrc='';
        this.workOrder={
          title: "",
          content: ""
        };
        this.imgModal=false
      },
      showInfo(id){
        this.infoStatus=true;
        this.orderInfoId=id;
      },
      changeConfig(){
        let keyData = []
        for (let img of this.imgData) {
          keyData.push(img.key)
        }
        let data = {
          title: this.workOrder.title,
          content: this.workOrder.content,
          attach_keys: keyData
        }
        this.$http.post('/api/ticket', data).then(function (response) {
          this.$root.errorMsg = response.data.msg;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true
            this.configStatus=false
            this.tableRe()
          } else {
            this.$root.alertError = true
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      selectImg(){
        $("#img_input").click()
      },
      showIcons(img){
        img.show = true
      },
      hideIcons(img){
        img.show = false
      },
      previewImg(img){
        this.curImgSrc = img.src
        this.imgModal=true;
      },
      deleteImg(img){
        this.imgData.$remove(img)
      },
      uploadImg(arg){
        var self = this;
        var form_data = new FormData();
        var file_data = $("#img_input").prop("files")[0];
        form_data.append("attachment", file_data);// 把上传的数据放入form_data
        this.$http.post('/api/ticket/attach', form_data).then(function (response) {
          if (response.data.status == 200) {
            self.keyData.push(response.data.data)
            self.imgData.push({key: response.data.data, src: arg.target.result, show: false})
          } else {
            this.$parent.$parent.alertError = true;
            this.$parent.$parent.errorMsg = response.data.msg;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })

      },
    },
    components: {
      ysSelect,
      tableOpt,
      tableData,
      aside,
      dealInfo
    },
  }
</script>
<style scoped>
  .annexBox{
    width:80px;
    height:80px;
    border:1px dashed #3185db;
    border-radius: 5px;
    color:#3185db;
    font-size:36px;
    text-align: center;
    line-height: 80px;
    cursor:pointer;
    float:left;
    margin-right:20px;
  }
  .annexList{
    width:80px;
    height:80px;
    margin-bottom:10px;
    background:#fff;
    float:left;
    margin-right:20px;
    display:inline-block;
    position:relative;
  }
  .annexList .preview{
    position:absolute;
    color:#fff;
    width: 100%;
    height: 100%;
    background: rgba(53,54,68,.7);
    line-height: 80px;
    text-align:center;
    vertical-align:middle;
  }
  .annexList .delete{
    position:absolute;
    right:-6px;
    top:-5px;
    background: #D23F40;
    border-radius: 50%;
    width: 15px;
    height: 15px;
    color:#fff;
    text-align:center;
    line-height:15px;
    display: inline-block;
  }
  .annexList img{width:100%;height:100%}
</style>
