<template>
  <div class="ys-con">
    <div class="ys-box-con ys-wrap">
      <div class="clearfix">
        <div class="col-md-6 p-l-0">
          <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5"></i>支付宝</div>
          <div class="ys-box-con" style="height:300px;">
            <p><checkbox :show.sync="payonline" :text="'启用支付宝支付'"></checkbox></p>
            <!-- <div class="disabled"> -->
            <div :class="[ payonline ? '' : 'disabled' ]">
              <table class="ys-form-table m-t-10">
                <tr>
                  <td class="ys-info-color">合作伙伴身份ID：</td>
                  <td>
                    <input class="ys-input ys-input-length" v-model="tableList.pay_pid" />
                  </td>
                </tr>
                <tr>
                  <td class="ys-info-color">支付宝MD5密钥：</td>
                  <td>
                    <input class="ys-input ys-input-length" type="password" v-model="tableList.pay_private_key" placeholder="不输入或输入为空则不修改"/>
                  </td>
                </tr>
                <tr>
                  <td class="ys-info-color">合作伙伴邮箱：</td>
                  <td>
                    <input class="ys-input ys-input-length" v-model="tableList.email" />
                  </td>
                </tr>
                <tr>
                  <td class="ys-info-color">支付测试金额：</td>
                  <td>
                  <span class="ys-input-unit">
                    <input class="ys-input ys-input-length" v-model="testPayMoney" placeholder="请输入一定金额 如0.01"/>
                    <span class="unit ys-info-color">元</span>
                  </span>
                  </td>
                </tr>
              </table>
              <p class="m-t-15"><button class="ys-btn m-r-10" @click="testPay()">测试支付</button></p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5"></i>离线支付</div>
          <div class="ys-box-con" style="height:300px;">
            <p><checkbox :show.sync="payoffline" :text="'启用离线支付'"></checkbox></p>
             <div :class="[ payoffline ? '' : 'disabled' ]">
              <table class="ys-form-table m-t-10">
                <tr>
                  <td class="ys-info-color">开户银行：</td>
                  <td>
                    <input class="ys-input ys-input-length" v-model="tableList.bank" />
                  </td>
                </tr>
                <tr>
                  <td class="ys-info-color">账户名称：</td>
                  <td>
                    <input class="ys-input ys-input-length" v-model="tableList.username" />
                  </td>
                </tr>
                <tr>
                  <td class="ys-info-color">银行账号：</td>
                  <td>
                    <input class="ys-input ys-input-length"  v-model="tableList.bank_user" />
                  </td>
                </tr>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div class="ys-box m-t-15">
        <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5"></i>发票设置</div>
        <div class="ys-box-con">
          <p>
            <span class="m-r-5 verticalM">开启发票申请:</span>
            <ys-switch :checked.sync="invoice">
              <span slot="open">开启</span>
              <span slot="close">关闭</span>
            </ys-switch>
          </p>
        </div>
      </div>
      <section class="m-t-20">
        <admin-password :admin-password.sync="adminPassword"></admin-password>
      </section>
      <p class="m-t-20"><button class="ys-btn m-r-10" @click="saveSettings()">保存</button></p>
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
    name: 'finance',
    data () {
      return {
        tableList: '',
        radioData: [
          {id: 1, text: '开启'},
          {id: 0, text: '关闭'},
        ],
        curRadio: 0,
        invoice: false,
        payonline: false,
        payoffline: false,
        adminPassword: '',
      }
    },
    ready: function () {
      this.getInfo();
    },
    methods: {
      getInfo () {
        this.$http.get('/api/system/finance').then(function (response) {
          if (response.data.status === 200) {
            this.tableList = response.data.data;
            this.payonline = Boolean(Number(response.data.data.pay_online));
            this.payoffline = Boolean(Number(response.data.data.pay_outline));
            this.invoice = Boolean(Number(response.data.data.invoice));
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      saveSettings () {
/*        let data = {
          'pay_private_key': this.tableList.pay_private_key,
          'pay_pid': this.tableList.pay_pid,
          'email': this.tableList.email,
          'invoice': this.curRadio,
          'pay_online': Number(this.curcheckbox),
          'admin_password': this.adminPassword
        };*/

        this.tableList.invoice = this.invoice;
        this.tableList.pay_online = this.payonline;
        this.tableList.pay_outline = this.payoffline;
        this.tableList.admin_password = this.adminPassword;
        this.$http.put('/api/system/finance', this.tableList).then(function (response) {
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
        let data = {
          'money': this.testPayMoney,
          'pay_private_key': this.tableList.pay_private_key,
          'pay_pid': this.tableList.pay_pid,
          'email': this.tableList.email,
        };
        this.$http.post('/api/system/paytest', data).then(function (response) {
          if (response.data.status === 200) {
            window.open(response.data.url);
          }else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      }
    },
    components: {
      adminPassword
    },
  }
</script>
