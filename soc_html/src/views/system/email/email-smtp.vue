<template>
  <div class="ys-box-con ys-wrap">

    <table class="ys-form-table">
      <tr>
        <td class="ys-info-color">SMTP邮件服务器：</td>
        <td>
          <input class="ys-input ys-input-length" v-model="tableList.smtp_server" />
        </td>
      </tr>
      <tr>
        <td class="ys-info-color">发信地址：</td>
        <td>
          <input class="ys-input ys-input-length" v-model="tableList.send_sender"
                 value="{{ tableList.send_sender }}"/>
        </td>
      </tr>
      <tr>
        <td class="ys-info-color">用户名：</td>
        <td>
          <input class="ys-input ys-input-length" v-model="tableList.user" />
        </td>
      </tr>
      <tr>
        <td class="ys-info-color">密码：</td>
        <td>
          <input class="ys-input ys-input-length" type="password" v-model="tableList.password" placeholder="不输入或输入为空则不修改"/>
        </td>
      </tr>
      <tr>
        <td class="ys-info-color">加密方式</td>
        <td>
          <radio :list="radioData" :value.sync="tls_or_ssl"></radio>
        </td>
      </tr>
      <tr>
        <td class="ys-info-color">测试发信地址：</td>
        <td>
          <input class="ys-input ys-input-length" v-model="test_email" placeholder="输入邮箱地址"/>
        </td>
      </tr>
      <tr>
        <td colspan="2"><button class="ys-btn ys-btn-blue ys-btn-s" @click="testPay()">测试发送邮件</button></td>
      </tr>
    </table>
    <section class="m-t-20">
      <admin-password :admin-password.sync="adminPassword"></admin-password>
    </section>
    <div class="m-t-20">
      <button class="ys-btn m-r-10" @click="saveSettings()">保存SMTP配置</button>
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
    name: 'email-parent',
    data () {
      return {
        parentNode: {
          ip: '',
          status: 0
        },
        tableList: '',
        radioData: [
          {id: 0, text: 'TLS'},
          {id: 1, text: 'SSL'},
        ],
        adminPassword: '',
        test_email: '',
        tls_or_ssl: 0,
      }
    },
    ready: function () {
      this.getInfo()
    },
    methods: {
      getInfo () {
        this.$http.get('/api/system/smtp_info').then(function (response) {
          if (response.data.status === 200) {
            this.tableList = response.data.data;
            if (response.data.data.tls_or_ssl === false) {
              this.tls_or_ssl = 0
            } else {
              this.tls_or_ssl = 1
            }
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      saveSettings () {
        this.tableList['admin_password'] = this.adminPassword;
        if (this.tls_or_ssl === 0) {
          this.tableList.tls_or_ssl = 0;
        } else {
          this.tableList.tls_or_ssl = 1;
        }
        this.$http.put('/api/system/smtp_info', this.tableList).then(function (response) {
          if (response.data.status === 200) {
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg
          }else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      testPay () {
        if (this.tls_or_ssl === 0) {
          this.tableList.tls_or_ssl = 0;
        } else {
          this.tableList.tls_or_ssl = 1;
        }
        this.tableList['send_test'] = this.test_email;
        this.$http.post('/api/system/smtp_info/test', this.tableList).then(function (response) {
          if (response.data.status === 200) {
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg;
          }else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg;
          }
        })
      }
    },
    components: {
      'admin-password': adminPassword,
    }
  }
</script>