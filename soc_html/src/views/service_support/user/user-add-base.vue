<template>
   <div>
        <validator name="valUser">
          <div v-if="!showQRCode">
            <div class="ys-box m-t-10">
              <div class="ys-box-title">填写用户基本信息</div>
              <div class="ys-box-con">
                <table class="ys-set-table">
                  <tbody>
                  <tr>
                    <td>用户名</td>
                    <td>
                      <input class="ys-input"
                             v-model="userInfo.username"
                             style="width: 218px"
                             v-validate:username="['required']">
                    </td>
                  </tr>
                  <tr>
                    <td>用户邮箱</td>
                    <td>
                      <input class="ys-input"
                             v-model="userInfo.email"
                             style="width: 218px"
                             v-validate:user_email="['email', 'required']">
                    </td>
                  </tr>
                  <tr>
                    <td>密码</td>
                    <td>
                      <input type="password"
                             class="ys-input"
                             v-model="userInfo.password"
                             style="width: 218px"
                             v-validate:password="['required']">
                    </td>
                  </tr>
                  <tr>
                    <td>重复密码</td>
                    <td>
                      <input type="password"
                             class="ys-input"
                             v-model="userInfo._password"
                             style="width: 218px"
                             v-validate:_password="['required', '_password']">
                    </td>
                  </tr>
                  <tr>
                    <td>联系电话</td>
                    <td>
                      <input class="ys-input"
                             v-model="userInfo.phone"
                             style="width: 218px"
                             v-validate:user_phone="['numeric', 'required']">
                    </td>
                  </tr>
                  <tr>
                    <td>状态</td>
                    <td>
                      <ys-select
                              :option="lockOptions"
                              @change="userInfo.is_locked = selectedLock.id"
                              :selected.sync="selectedLock"
                              :width="218"></ys-select>
                    </td>
                  </tr>
                  <tr>
                    <td>角色</td>
                    <td>
                      <ys-select
                              :option="roleOptions"
                              @change="userInfo.is_admin = selectedRole.id"
                              :selected.sync="selectedRole"
                              :width="218">
                      </ys-select>
                    </td>
                  </tr>
                  </ys-select>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="aside-foot m-t-20">
              <button class="ys-btn m-r-10" @click="addUser()">确定</button>
              <button class="ys-btn ys-btn-white" @click="show=false">取消</button>
            </div>
          </div>
          <div v-if="showQRCode">
            <div class="ys-box m-t-10">
              <div class="ys-box-title">绑定二次验证</div>
              <div class="ys-box-con">
                <p class="textC" v-if="showQRCode">请扫描二次验证码：</p>
                <p class="textC" v-if="showQRCode"><img class="m-t-10" :src="QRCodeUrl" style="width:120px;"></p>
                <p class="textC m-t-10" v-if="showQRCode">
                  <button class="ys-btn" @click="getQrCode(newUserId)">重新生成</button>
                </p>
              </div>
            </div>
            <div class="aside-foot m-t-20">
              <button class="ys-btn m-r-10" @click="show=false">确定</button>
              <button class="ys-btn ys-btn-white" @click="show=false">关闭</button>
            </div>
          </div>
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
    name: "user-add-base",
    props: {
      show: {
          default: false
      },
      companyId: {
          default: 0
      }
    },
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
        newUserId: 0,
        showQRCode: false,
        QRCodeUrl: "/",
        userInfo: {
          username: "",
          password: "",
          re_password: "",
          phone: "",
          email: "",
          is_locked: 0,
          is_admin: 0
        },
        onValid: false,
        check: false,
      }
    },
    methods: {
      initForm() {
        this.userInfo = {
          username: "",
          password: "",
          re_password: "",
          phone: "",
          email: "",
          is_locked: 0,
          is_admin: 0
        }
        this.QRCodeUrl = '/'
        this.showQRCode = false
      },
      addUser(){
        var self = this
        self.check = true
        self.userInfo.company_id = this.companyId
        self.$http.post('/api/user', self.userInfo).then(function (response) {
          this.$root.errorMsg = response.data.msg;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.newUserId = response.data.data.user_id
            this.getQrCode(response.data.data.user_id)
            this.$dispatch('added')
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
        self.getQrCode(self.newUserId)
      },
      logoutCurrentUser(){
        localStorage.removeItem("current_user")
        sessionStorage.removeItem("current_user")
        window.location.href = '/login';
      },
    },
    watch: {
      show :function (val, oldval) {
        if(!val){
          this.initForm()
        }
      }
    },
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
