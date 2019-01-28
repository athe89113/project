<template>
  <div class="ys-con" style="padding-bottom:300px">
    <validator name="valCompany">
      <div class="pageHead">
        <p class="pageTitle"><span>支持管理 </span>- 公司管理</p>
      </div>
      <!--第一步-->
      <div class="ys-card-box">
        <div class="mon-step step-one m-t-10">
          <span>修改公司基本信息</span>
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
                       v-show="$valCompany.company_name.required && $valCompany.company_name.touched">
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
                  <div class="select-remark" v-show="$valCompany.company_email.email">
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
      <div class="m-t-40 m-l-40 p-l-3">
        <button class="ys-btn" @click="editCompany()" :disabled="!$valCompany.valid">确认修改</button>
      </div>
      <div class="clearfix"></div>
    </validator>
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
    name: "company-edit",
    data() {
      return {
        editCompanyId: this.$route.params.company_id,
        companyInfo: {
          name: "",
          email: "",
          phone: "",
          address: "",
        }
      }
    },
    ready: function () {
      this.getCompanyInfo()
    },
    methods: {
      getCompanyInfo(){
        var self = this
        self.$http.get('/api/company/' + self.editCompanyId).then(function (response) {
          if (response.data.status == 200) {
            this.companyInfo = response.data.data
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      editCompany(){
        var self = this
        self.$http.put('/api/company/' + self.editCompanyId, self.companyInfo).then(function (response) {
          this.$root.errorMsg = response.data.msg;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.$router.go({name: "company"})
          } else {
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
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
