<template>
  <div class="ys-con" style="padding-bottom:300px">
    <div class="pageHead">
      <p class="pageTitle"><span>支持管理 </span>- 公司管理</p>
    </div>
    <validator name="valCompany" @valid="onValid = true" @invalid="onValid = false">
      <!--第一步-->
      <div class="ys-card-box">
        <div class="mon-step step-one m-t-10">
          <span>第一步 : 填写公司基本信息</span>
          <div class="stepArrow step-one"></div>
        </div>
        <div class="step-info m-b-20" v-show="!showQRCode">
          <div class="ys-row">
            <section>
              <div class="m-t-20">
                <span class="left-name">公司名称</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="companyInfo.name"
                    style="width: 218px"
                    v-validate:company_name="['required']">
                  <div class="select-remark"
                       v-show="$valCompany.company_name.required && check">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">公司名称不能为空</span>
                  </div>
                  <div class="select-remark" v-else>
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写公司的名称</span>
                  </div>
                </div>
              </div>
              <div class="m-t-30">
                <span class="left-name">联系电话</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="companyInfo.phone"
                    style="width: 218px"
                    v-validate:company_phone="['numeric']">
                  <div class="select-remark" v-show="$valCompany.company_phone.numeric">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">电话格式不正确</span>
                  </div>
                  <div class="select-remark" v-else>
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写公司的联系电话</span>
                  </div>
                </div>
              </div>
            </section>
            <section>
              <div class="m-t-20">
                <span class="left-name">公司地址</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="companyInfo.address"
                    style="width: 218px"
                  >
                  <div class="select-remark" v-else>
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写公司的地址</span>
                  </div>
                </div>
              </div>
              <div class="m-t-30">
                <span class="left-name">公司邮箱</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="companyInfo.email"
                    style="width: 218px"
                    v-validate:company_email="['email']">
                  <div class="select-remark" v-show="$valCompany.company_email.email && check">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">邮箱格式不正确</span>
                  </div>
                  <div class="select-remark" v-else>
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写公司的邮箱</span>
                  </div>
                </div>
              </div>
            </section>
            <div class="clearfix"></div>
          </div>
        </div>
      </div>
      <!--第二步-->
      <div class="ys-card-box m-t-20">
        <div class="mon-step step-two m-t-10">
          <span>第二步 : 创建公司用户</span>
          <div class="stepArrow step-two"></div>
        </div>
        <div class="step-info m-b-20" v-show="!showQRCode">
          <div class="ys-row">
            <section>
              <div class="m-t-20">
                <span class="left-name">用户名</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="companyInfo.username"
                    style="width: 218px"
                    v-validate:username="['required']">
                  <div class="select-remark" v-show="$valCompany.username.required && check">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">用户名不能为空</span>
                  </div>
                  <div class="select-remark" v-else>
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写公司用户的用户名</span>
                  </div>
                </div>
              </div>
              <div class="m-t-30">
                <span class="left-name">密码</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="companyInfo.password"
                    style="width: 218px"
                    v-validate:password="['required']">
                  <div class="select-remark" v-show="$valCompany.password.required && check">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">用户密码不能为空</span>
                  </div>
                  <div class="select-remark" v-else>
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写公司用户的密码</span>
                  </div>
                </div>
              </div>
              <div class="m-t-30">
                <span class="left-name">联系电话</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="companyInfo.user_phone"
                    style="width: 218px"
                    v-validate:user_phone="['numeric', 'required']">
                  <div class="select-remark"
                       v-show="check && $valCompany.user_phone.required || $valCompany.user_phone.numeric">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">电话格式不正确</span>
                  </div>
                  <div class="select-remark" v-else>
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写公司用户的联系电话</span>
                  </div>
                </div>
              </div>
            </section>
            <section>
              <div class="m-t-20">
                <span class="left-name">用户邮箱</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="companyInfo.user_email"
                    style="width: 218px"
                    v-validate:user_email="['email', 'required']">
                  <div class="select-remark"
                       v-if="check && $valCompany.user_email.required || $valCompany.user_email.email">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">邮箱格式不正确</span>
                  </div>
                  <div class="select-remark" v-else="">
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写用户的邮箱</span>
                  </div>
                </div>
              </div>
              <div class="m-t-30">
                <span class="left-name">重复密码</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="companyInfo._password"
                    style="width: 218px"
                    v-validate:_password="['required', '_password']">
                  <div class="select-remark"
                       v-show="check && $valCompany._password.required || $valCompany._password._password">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">用户密码不正确</span>
                  </div>
                  <div class="select-remark" v-else="">
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写用户的密码</span>
                  </div>
                </div>
              </div>
            </section>
            <div class="clearfix"></div>
          </div>
        </div>
      </div>
      <!--第三步-->
      <div class="ys-card-box m-t-20">
        <div class="mon-step step-three m-t-10">
          <span>第三步 : 二次验证</span>
          <div class="stepArrow step-three"></div>
        </div>
        <div class="step-info m-b-20" v-show="showQRCode">
          <div class="ys-row">
            <div class="m-t-20">
              <div class="textL">请扫描二次验证码：</div>
              <img class="m-t-10" :src="QRCodeUrl">
            </div>
          </div>
        </div>
      </div>

      <div class="m-t-40 m-l-40 p-l-3" v-show="!showQRCode">
        <button class="ys-btn" @click="addCompany()">添加公司</button>
      </div>
      <div class="m-t-40 m-l-40 p-l-3" v-show="showQRCode">
        <button class="ys-btn" v-link="{ name: 'company'}">确定</button>
      </div>
    </validator>
    <div class="clearfix"></div>

  </div>

</template>
<style scoped>
  .add-step-input {
    display: inline-block;
    width: 220px;
    height: 30px;
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
  import Api from  '../../../lib/api'
  import ysSelect from '../../../components/select.vue'
  export default {
    name: "company-add",
    data() {
      return {
        showQRCode: false,
        QRCodeUrl: "/",
        companyInfo: {
          name: "",
          email: "",
          phone: "",
          address: "",
          username: "",
          password: "",
          _password: "",
          user_email: "",
          user_phone: "",
        },
        onValid: false,
        check: false,
      }
    },
    ready: function () {
    },
    methods: {
      addCompany(){
        var self = this
        self.check = true
        if (!self.onValid) {
          return
        }
        self.$http.post('/api/company', self.companyInfo).then(function (response) {
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.getQrCode(response.data.data.user_id)
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getQrCode(id){
        this.$http.post("/api/user/two_factor", {"user_id": id}).then(function (response) {
          if (response.status == 200) {
            this.QRCodeUrl = 'data:image/png;base64,' + response.data
            this.showQRCode = true
          } else {
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      }
    },
    watch: {},
    components: {
      ysSelect,
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
