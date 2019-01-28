<template>
  <div class="ys-con" style="padding-bottom:300px">
    <validator name="valUser">
      <div class="pageHead">
        <p class="pageTitle"><span>支持管理 </span>- 用户管理</p>
      </div>
      <!--第一步-->
      <div class="ys-card-box">
        <div class="mon-step step-one m-t-10">
          <span>用户基本信息</span>
          <div class="stepArrow step-one"></div>
        </div>
        <div class="step-info m-b-20" v-show="!showQRCode">
          <div class="ys-row">
            <section>
              <div class="m-t-20">
                <span class="left-name">用户名</span>
                <div class="add-step-input">
                  <span>{{userInfo.username}}</span>
                </div>
              </div>
              <div class="m-t-30">
                <span class="left-name">密码</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="userInfo.password"
                    style="width: 218px">
                  <div class="select-remark" v-else="">
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写用户的密码</span>
                  </div>
                </div>
              </div>
              <div class="m-t-30">
                <span class="left-name">联系电话</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="userInfo.phone"
                    style="width: 218px"
                    v-validate:phone="['numeric']">
                  <div class="select-remark" v-show="$valUser.phone.numeric">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">电话格式不正确</span>
                  </div>
                  <div class="select-remark" v-else="">
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写联系电话</span>
                  </div>
                </div>
              </div>
              <div class="m-t-30" v-if="userIsAdmin==1">
                <span class="left-name">角色</span>
                <ys-select
                  :option="roleOptions"
                  @change="userInfo.is_admin = selectedRole.id"
                  :selected.sync="selectedRole"
                  :width="218"
                  :remark="'选择用户对应的角色'">
                </ys-select>
              </div>
            </section>
            <section>
              <div class="m-t-20">
                <span class="left-name">用户邮箱</span>
                <div class="add-step-input">
                  <input
                    class="ys-input"
                    v-model="userInfo.email"
                    style="width: 218px"
                    v-validate:email="['email', 'required']">
                  <div class="select-remark" v-show="$valUser.email.required && $valUser.email.touched">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">用户邮箱不能为空</span>
                  </div>
                  <div class="select-remark" v-show="$valUser.email.email">
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
                    v-model="userInfo.re_password"
                    style="width: 218px"
                    v-validate:re_password="['_password']">
                  <div class="select-remark" v-show="$valUser.re_password._password">
                    <i class="md md-info verticalM font16 input-opt"></i>
                    <span class="verticalM input-opt">重复密码不正确</span>
                  </div>
                  <div class="select-remark" v-else="">
                    <i class="md md-info verticalM font16"></i>
                    <span class="verticalM">填写用户的密码</span>
                  </div>
                </div>
              </div>
              <div class="m-t-30">
                <span class="left-name">状态</span>
                <ys-select
                  :option="lockOptions"
                  @change="userInfo.is_locked = selectedLock.id"
                  :selected.sync="selectedLock"
                  :width="218"
                  :remark="'设置用户状态'">
                </ys-select>
              </div>
            </section>
            <div class="clearfix"></div>
          </div>
        </div>
      </div>
      <div class="m-t-40 m-l-40 p-l-3" v-show="!showQRCode">
        <button class="ys-btn" @click="editUser()" :disabled="!$valUser.valid">确认修改</button>
      </div>
      <!--第二步-->
      <div class="ys-card-box m-t-20">
        <div class="mon-step step-two m-t-10">
          <span>绑定二次验证</span>
          <div class="stepArrow step-two"></div>
        </div>
        <div class="step-info m-b-20">
          <div class="ys-row">
            <div class="m-t-30">
              <div class="add-step-input m-l-40">
                <input
                  type="checkbox"
                  value="二次验证"
                  v-model="reTwoFactor">
                <span class="text-cursor">重新绑定二次验证</span>
              </div>
            </div>
            <div class="m-t-20" v-show="showQRCode">
              <div class="textL">请扫描二次验证码：</div>
              <img class="m-t-10" :src="QRCodeUrl">
            </div>
          </div>
        </div>
      </div>

      <div class="m-t-40 m-l-40 p-l-3" v-show="reTwoFactor">
        <button class="ys-btn" @click="regenerateTwoFactorImg()">重新生成</button>
        <button class="ys-btn" v-link="{ name: 'user-mgt'}" style="margin-left: 60px;width: 90px;">完成</button>
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
    name: "user-edit",
    computed: {
      userIsAdmin () {
        return this.$store.state.user.is_admin
      },
    },
    data() {
      return {
        roleOptions: [
          {id: 0, name: "普通用户"},
          {id: 1, name: "管理员"}
        ],
        selectedRole: {id: 0, name: "普通用户"},
        lockOptions: [
          {id: 0, name: "正常"},
          {id: 1, name: "锁定"}
        ],
        selectedLock: {id: 0, name: "正常"},
        editUserId: this.$route.params.user_id,
        showQRCode: false,
        reTwoFactor: false,
        QRCodeUrl: "/",
        userInfo: {
          username: "",
          password: "",
          re_password: "",
          phone: "",
          email: "",
          is_locked: 0,
          is_admin: 0
        }
      }
    },
    ready: function () {
      this.getUserInfo()
    },
    methods: {
      getUserInfo(){
        let self = this
        self.$http.get('/api/user/' + self.editUserId).then(function (response) {
          if (response.data.status == 200) {
            self.userInfo = response.data.data
            self.$set("userInfo.password", "")
            self.$set("userInfo.re_password", "")
            if (self.userInfo.is_locked == 1) {
              self.selectedLock = {id: 1, name: "锁定"}
            }
            if (self.userInfo.is_admin == 1) {
              self.selectedRole = {id: 1, name: "管理员"}
            }
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      editUser(){
        let self = this
        let data = {
          email: self.userInfo.email,
          phone: self.userInfo.phone,
        }
        if (self.userInfo.password != "") {
          data.password = self.userInfo.password
          data.re_password = self.userInfo.re_password
        }
        if (self.userIsAdmin == 1) {
          data.is_admin = self.userInfo.is_admin
          data.is_locked = self.userInfo.is_locked
        }
        self.$http.put('/api/user/' + self.editUserId, data).then(function (response) {
          this.$root.errorMsg = response.data.msg;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            if (self.userInfo.username == (localStorage.getItem('current_user') || sessionStorage.getItem('current_user')) && self.userInfo.password != "") {
              self.logoutCurrentUser()
            }else{
              this.$route.router.go(window.history.back())
            }
          } else {
            this.$root.alertError = true;
          }
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
      },
      regenerateTwoFactorImg(){
        var self = this
        self.getQrCode(self.editUserId)
      },
      logoutCurrentUser(){
        localStorage.removeItem("current_user")
        sessionStorage.removeItem("current_user")
        window.location.href = '/login';
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
        return this.vm.userInfo.password == this.vm.userInfo.re_password
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
