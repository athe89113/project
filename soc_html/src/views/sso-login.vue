<template>
<div class="top-content">
  <div class="inner-bg ys-blur"></div>
  <div class="login-dark-bg"></div>
  <div class="login-box">
    <div class="loginCon">
      <div class="ys-box">
        <div class="ys-box-con">
          <div v-if="status==0">
            <div>
              <span style="font-size: 1.5em">正在验证中...</span>
            </div>
            <div class="m-t-10">
              <span>当前登录信息正在验证，请稍候。</span>
            </div>
          </div>
          <div v-else="">
            <div>
              <span style="font-size: 1.5em" class="ys-error-color">发生登录错误！</span>
            </div>
            <div class="m-t-10">
              <span>您在跳转前所携带的登录信息异常，无法登录（{{status_code}}）</span>
              <button class="ys-btn ys-btn-green m-t-10" type="button" style="line-height: 30px" @click="goBack()">
                <i class="glyphicon glyphicon-circle-arrow-left"></i>
                返回
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="logo-box">
    <img v-bind:src="logoUrl" style="width:100px;"/>
  </div>
</div>
</template>
<style scoped>
  .logo-box{
    position:absolute;
    left:34px;
    top:34px;
  }
  .login-table{
    width:100%;
  }
  .login-table td{
    padding:12px 4px;
  }
  .login-table .label{

  }
  .top-content{
    position: relative;
  }
  .login-box{
    position: absolute;
    width:340px;
    top:50%;
    margin-top:-200px;
    left:50%;
    margin-left:-150px;
  }
  .inner-bg{
    height:100%;
    background-image: url(../assets/images/login_bg_1.jpg);
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;

    -webkit-filter: blur(6px);
    -ms-filter: blur(6px);
    filter: blur(6px);
    filter: progid:DXImageTransform.Microsoft.Blur(PixelRadius=6, MakeShadow=false) \9;
    position: relative;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }
  .login-dark-bg{
    position:absolute;
    top:0px;
    left:0px;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.45);
  }
  .captcha-box{
    display:inline-block;
    width:82px;
    background:rgba(255,255,255,0.1);
    text-align: center;
    border-radius: 3px;
    height: 32px;
    line-height: 24px;
    padding: 4px 7px;
    color:#e96157;
    vertical-align: middle;
  }
</style>
<script>
require('../assets/css/animate.min.css')
import { changeFromLogin } from 'src/lib/actions'
module.exports = {
  name: 'sso-login',
  vuex: {
    actions: {
      changeFromLogin
    }
  },
  data: function() {
    return {
      status: 0,
      status_code: 501,
    }
  },
  computed: {
    logoUrl: {
      get: function () {
        return this.$root.logoUrl
      }
    }
  },
  ready(){
    this.login()
    $(".inner-bg").css({'height':$(window).height()+"px"});
    $(window).resize(function() {
      $(".inner-bg").css({'height':$(window).height()+"px"});
    });
  },
  methods: {
    login(){
      this.$http.post('/api/sso/login/' + this.$route.params.base_str).then(function (response) {
        let self = this
        let data = response.data.data

        if (response.data.status == 200) {
          localStorage.setItem('current_user', data.username)
          this.changeFromLogin(true)
          this.$root.loadStatus = true
          setTimeout(function () {
            self.$root.loadStatus = false
            self.$router.go("/soc")
          }, 2000)
        } else {
          this.status = 1
          this.status_code = response.data.status
        }
      })
    },
    goBack(){
      window.location.href = document.referrer
    }
  },
}

</script>
