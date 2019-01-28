<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <div class="clearfix">
        <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5"></i>注册设置</div>

        <div class="ys-box-con" style="height:130px;">
          <div class="m-t-20">
            <p>
              <span class="m-r-5 verticalM ys-info-color">开启注册:</span>
              <ys-switch :checked.sync="visitData.register_allow">
                <span slot="open">开启</span>
                <span slot="close">关闭</span>
              </ys-switch>
            </p>
          </div>
          <div class="m-t-20">
            <p class="ys-info-color">每IP注册限制: 在  <input class="ys-input ys-input-length" v-model="visitData.register_time"/>  分钟之内可注册  <input
              class="ys-input ys-input-length" v-model="visitData.register_count"/>  个账号</p>
          </div>

        </div>

        <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5 m-t-10"></i>登录设置</div>
        <div class="ys-box-con" style="height:240px;">
          <div class="m-t-20">
            <p>
              <span class="m-r-5 verticalM ys-info-color">开启登录:</span>
              <ys-switch :checked.sync="visitData.login_allow">
                <span slot="open">开启</span>
                <span slot="close">关闭</span>
              </ys-switch>
            </p>
          </div>

          <div class="m-t-20 ys-info-color">会员登陆:
            <checkbox :show.sync="visitData.username" :text="'用户名'"></checkbox>
            <checkbox :show.sync="visitData.email" :text="'邮箱'"></checkbox>
            <checkbox :show.sync="visitData.phone" :text="'手机'"></checkbox>
            <checkbox :show.sync="visitData.wechat" :text="'微信'"></checkbox>
          </div>
          <div class="m-t-20">
            <p class="ys-info-color">登录账号保护: 在  <input class="ys-input ys-input-length" v-model="visitData.user_fail_range_time"/>  分钟内，登录失败  <input
            class="ys-input ys-input-length" v-model="visitData.user_fail_count"/>  次，锁定账号。锁定账号  <input
              class="ys-input ys-input-length" v-model="visitData.user_fail_ban_time"/>  分钟。</p>

          </div>
          <div class="m-t-20">
            <checkbox :show.sync="visitData.is_find_password" :text="'可通过密码找回解锁'"></checkbox>
          </div>
          <div class="m-t-20">
            <p class="ys-info-color">登录系统保护: 同一IP在  <input class="ys-input ys-input-length" v-model="visitData.fail_range_time"/>  分钟内，登录失败  <input
            class="ys-input ys-input-length" v-model="visitData.fail_count"/>  次，将IP封禁。封禁IP  <input
              class="ys-input ys-input-length" v-model="visitData.fail_ban_time"/>  分钟。</p>
          </div>
        </div>

        <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5 m-t-10"></i>会话设置</div>
        <div class="ys-box-con" style="height:90px;">
          <div class="m-t-20">
            <p class="ys-info-color">当无操作  <input class="ys-input ys-input-length" v-model="visitData.login_timeout"/>  分钟后结束会话</p>
          </div>
        </div>
      </div>
      <section class="m-t-20">
        <admin-password :admin-password.sync="adminPassword"></admin-password>
      </section>
      <p class="m-t-20">
        <button class="ys-btn m-r-10" @click="saveSettings()">保存</button>
      </p>
    </div>
  </div>
</template>
<style scoped>
  .ys-input-length{
    width:45px;
  }
</style>
<script>
  import adminPassword from 'src/components/admin-password.vue'
  export default {
    name: 'system-visit',
    data () {
      return {
        visitData: {},
      }
    },
    ready: function () {
      this.getInfo();
    },
    methods: {
      getInfo () {
        this.$http.get('/api/system/visit').then(function (response) {
          if (response.data.status === 200) {
            this.visitData = response.data.data;
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      saveSettings () {
        this.visitData.admin_password = this.adminPassword;
        this.$http.put('/api/system/visit', this.visitData).then(function (response) {
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
      adminPassword
    },
  }
</script>