<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <table class="ys-form-table">
        <tr>
          <td class="ys-info-color">合作商Token：</td>
          <td>
            <input class="ys-input ys-input-length" v-model="tableList.qs_token" />
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">合作商密钥：</td>
          <td>
            <input class="ys-input ys-input-length" v-model="tableList.qs_token_secret" />
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">接口超时：</td>
          <td>
            <span class="ys-input-unit">
              <input class="ys-input ys-input-length" v-model="tableList.qs_api_timeout"/>
              <span class="unit ys-info-color">秒</span>
            </span>
          </td>
        </tr>
        <tr>
          <td colspan="2"><button class="ys-btn ys-btn-blue ys-btn-s" @click="testPay()">接口测试</button></td>
        </tr>
      </table>

      <section class="m-t-20">
        <admin-password :admin-password.sync="adminPassword"></admin-password>
      </section>
      <div class="aside-foot m-t-20">
        <button class="ys-btn m-r-10" @click="saveSettings()">保存接口配置</button>
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
        this.$http.get('/api/system/qs_api').then(function (response) {
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
        this.$http.put('/api/system/qs_api', this.tableList).then(function (response) {
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
        this.$http.post('/api/system/qs_api/test', this.tableList).then(function (response) {
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
      'admin-password': adminPassword
    }
  }
</script>