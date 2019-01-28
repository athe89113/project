<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <table class="ys-form-table">
        <tr>
          <td class="ys-info-color">短信API地址：</td>
          <td>
            <input class="ys-input ys-input-length" v-model="tableList.api" />
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">API账号：</td>
          <td>
            <input class="ys-input ys-input-length" v-model="tableList.user" />
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">API密码：</td>
          <td>
            <input class="ys-input ys-input-length" type="password" v-model="tableList.password" placeholder="不输入或输入为空则不修改"/>
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">测试接收手机：</td>
          <td>
            <input class="ys-input ys-input-length" v-model="test_phone" placeholder="请输入接收测试短信手机号"/>
          </td>
        </tr>
        <tr>
          <td colspan="2"><button class="ys-btn ys-btn-blue ys-btn-s" @click="testPay()">测试发送短信</button></td>
        </tr>
      </table>

      <section class="m-t-20">
        <admin-password :admin-password.sync="adminPassword"></admin-password>
      </section>
      <div class="aside-foot m-t-20">
        <button class="ys-btn m-r-10" @click="saveSettings()">保存短信配置</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.ys-input-length{
  width:260px;
}
</style>
<script>
  import adminPassword from 'src/components/admin-password.vue'
  export default {
    name: 'message-setting',
    data () {
      return {
        adminPassword: '',
        tableList: '',
        test_phone: '',
      }
    },
    ready: function () {
      this.getInfo()
    },
    methods: {
      getInfo () {
        this.$http.get('/api/system/message').then(function (response) {
          if (response.data.status === 200) {
            this.tableList = response.data.data;
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      saveSettings () {
        this.tableList['admin_password'] = this.adminPassword;
        this.$http.put('/api/system/message', this.tableList).then(function (response) {
          if (response.data.status === 200) {
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      testPay () {
        this.tableList['send_test'] = this.test_phone;
        this.$http.post('/api/system/message/send', this.tableList).then(function (response) {
          if (response.data.status === 200) {
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      }
    },
    components: {
      'admin-password': adminPassword,
    }
  }
</script>