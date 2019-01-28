<template>
  <div class="ys-box-con ys-wrap">
    <table class="ys-form-table">
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
        <td class="ys-info-color">测试发信地址：</td>
        <td>
          <input class="ys-input ys-input-length" v-model="test_email" placeholder="输入邮箱地址"/>
        </td>
      </tr>
      <tr>
        <td colspan="2"><button class="ys-btn ys-btn-blue ys-btn-s m-r-10" @click="testPay()">测试发送邮件</button></td>
      </tr>
    </table>
    <section class="m-t-20">
      <admin-password :admin-password.sync="adminPassword"></admin-password>
    </section>
    <div class="m-t-20">
      <button class="ys-btn m-r-10" @click="saveSettings()">保存SendCloud配置</button>
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
    name: 'finance-parent',
    data () {
      return {
        parentNode: {
          ip: '',
          status: 0,
        },
        radioData: [
          {id: 1, text: '开启'},
          {id: 2, text: '关闭'},
        ],
        curRadio: 1,
        adminPassword: '',
        curcheckbox: '',
        tableList: '',
        test_email: '',
      }
    },
    ready: function () {
      this.getInfo()
    },
    methods: {
      getInfo () {
        this.$http.get('/api/system/cloud_email').then(function (response) {
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
        this.$http.put('/api/system/cloud_email', this.tableList).then(function (response) {
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
        this.tableList['send_test'] = this.test_email;
        this.$http.post('/api/system/cloud_email/send', this.tableList).then(function (response) {
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
