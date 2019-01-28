<template>
  <div class="pageHead">
    <p class="pageTitle"><span>支持管理 </span>- 添加工单</p>
  </div>
  <ys-modal :show.sync="imgModal" :title="'查看图片'">
    <div slot="content">
      <p><img v-bind:src="curImgSrc" style="width:100%"/></p>
      <p class="textC m-t-10"><button class="ys-btn" @click="imgModal=false">关闭</button></p>
    </div>
  </ys-modal>
  <div class="ys-con" style="padding-bottom:300px">
    <validator name="valFrom">
      <!--第一步-->
      <div class="ys-card-box">
        <div class="mon-step step-one m-t-10">
          <span>填写工单基本信息</span>
          <div class="stepArrow step-one"></div>
        </div>
        <div class="step-info m-b-20">
          <div class="ys-row">
            <section>
              <div class="m-t-20">
                <span class="left-name">工单标题</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="workOrder.title"
                    style="width: 218px"
                    v-validate:title="['required']">
                  <div class="select-remark"
                       v-show="$valFrom.title.required && checked">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">工单标题不能为空</span>
                  </div>
                  <div class="select-remark" v-else>
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写工单的标题</span>
                  </div>
                </div>
              </div>
            </section>
            <div class="clearfix"></div>
          </div>
          <div class="clearfix"></div>
          <div class="ys-row m-t-30">
            <section>
              <span class="left-name">描述</span>
              <div class="add-step-input">
                  <textarea
                          class="ys-input"
                          style="width: 400px; height: 200px"
                          v-model="workOrder.content">
                  </textarea>
              </div>
            </section>
            <div class="clearfix"></div>
          </div>
          <div class="clearfix"></div>
          <div class="ys-row m-t-20">
            <section>
              <span class="left-name">添加附件</span>
              <div class=" add-step-input verticalM" style="height: 100px">
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
              </div>
            </section>
            <div class="clearfix"></div>
          </div>
        </div>
        <div class="clearfix"></div>
      </div>
      <div class="m-t-40 m-l-40 p-l-3">
        <button class="ys-btn" @click="add()">添加工单</button>
      </div>
      <div class="clearfix"></div>
    </validator>
  </div>
</template>
<style scoped>
  .add-step-input {
    display: inline-block;
    line-height: 30px;
    position: relative;
  }

  .add-step-input .select-remark {
    width: 835px;
    position: absolute;
    z-index: 2;
    top: 25px;
    left: 0px;
    color: #aaa;
    font-size: 12px;
  }

  .remark-text {
    color: #6c6874;
    font-size: 12px;
  }
</style>
<script>
  import Api from  'src/lib/api'
  import ysSelect from 'src/components/select.vue'
  import ysModal from 'src/components/modal.vue'
  export default {
    name: "workorder-add",
    data() {
      return {
        checked: false,
        keyData: [],
        imgData: [],
        curImgSrc: '',
        workOrder: {
          title: "",
          content: ""
        },
        imgModal:false
      }
    },
    ready: function () {
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
    methods: {
      add(){
        this.checked = true
        var self = this

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
            this.$router.go({name: "workorder-apply"})
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
    watch: {},
    components: {
      ysSelect,
      ysModal
    },
    validators: {
      email: function (val/*,rule*/) {
        if (val == "") {
          return true
        }
        return /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(val)
      },
      _password: function (val) {
        return this.vm.companyInfo.password == this.vm.companyInfo._password
      },
      numeric: function (val/*,rule*/) {
        if (val == "") {
          return true
        }
        return /^[-+]?[0-9]+$/.test(val)
      }
    },
  }
</script>
<style scoped>
  .annexBox {
    width: 80px;
    height: 80px;
    border: 1px dashed #3185db;
    border-radius: 5px;
    color: #3185db;
    font-size: 36px;
    text-align: center;
    line-height: 80px;
    cursor: pointer;
    float: left;
    margin-right: 20px;
    border-radius: 3px;
  }

  .annexList {
    width: 80px;
    height: 80px;
    float: left;
    margin-right: 20px;
    display: inline-block;
    position: relative;
  }

  .annexList .preview {
    position: absolute;
    color: #fff;
    width: 100%;
    height: 100%;
    background: rgba(53, 54, 68, .7);
    line-height: 80px;
    text-align: center;
    vertical-align: middle;
  }

  .annexList .delete {
    position: absolute;
    right: -6px;
    top: -5px;
    background: #D23F40;
    border-radius: 50%;
    width: 15px;
    height: 15px;
    color: #fff;
    text-align: center;
    line-height: 15px;
    display: inline-block;
  }

  .annexList img {
    width: 100%;
    height: 100%;
    border-radius: 3px;
  }
</style>
