<template>
<div class="top-content">
  <div class="inner-bg ys-blur"></div>
  <div class="login-dark-bg"></div>
  <div class="login-box">
    <div class="loginCon">
      <div class="ys-box" v-show="page==1">
        <div class="ys-box-title">登录</div>
        <div class="ys-box-con">
          <div class="login-module">
            <validator name="validation1">
              <table class="login-table">
                <tbody>
                <tr>
                  <td class="lab"><i class="fa fa-user font14 ys-info-color"></i></td>
                  <td class="pos-r">
                    <input type="text"
                           class="ys-input ys-input-bg fullWidth"
                           style="height:32px;line-height:32px;"
                           v-model="username"
                           autofocus="autofocus"
                           placeholder="用户名"
                           initial='off'
                           @change="closeStatus()"
                           v-validate:user-name="{required: { rule: true, message: '请输入用户名' }}"/>
                    <div v-if="$validation1.userName.touched" class="input-warn ys-info-color" style="margin-left:4px;margin-top:3px;">
                      <span v-if="$validation1.userName.required">{{ $validation1.userName.required }}</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="lab"><i class="fa fa-lock font14 ys-info-color"></i></td>
                  <td class="pos-r">
                    <input type="password"
                           class="ys-input ys-input-bg fullWidth"
                           style="height:32px;line-height:32px;"
                           v-model="password"
                           placeholder="密码"
                           initial='off'
                           @change="closeStatus()"
                           v-validate:password="{required: { rule: true, message: '请输入密码!'}}"/>
                    <div v-if="$validation1.password.touched" class="input-warn ys-info-color" style="margin-left:4px;margin-top:3px;">
                      <span v-if="$validation1.password.required">{{ $validation1.password.required }}</span>
                    </div>
                  </td>
                </tr>
                <!--<tr>-->
                  <!--<td></td>-->
                  <!--<td>-->
                    <!--&lt;!&ndash;<checkbox :show.sync="remember" :text="'记住我'"></checkbox>&ndash;&gt;-->
                    <!--&lt;!&ndash;<a class="fRight disabled">忘记密码</a>&ndash;&gt;-->
                  <!--</td>-->
                <!--</tr>-->
                <tr v-if="status">
                  <td></td>
                  <td>{{statusMsg}}</td>
                </tr>
                <tr>
                  <td></td>
                  <td><input type="button"
                             value="登录"
                             @click="login"
                             class="ys-btn fullWidth"
                             style="height:32px;line-height:32px;"/></td>
                </tr>
                </tbody>
              </table>
              <!--<p class="textR m-t-20">没有账号?<a class="m-l-3" @click="get_register_status()">立即注册</a></p>-->
            </validator>
          </div>
        </div>
      </div>
      <div class="ys-box" v-show="page==2">
        <div class="ys-box-title">二次验证</div>
        <div class="ys-box-con">
          <div class="login-module">
            <validator name="validation1">
              <table class="login-table">
                <tbody>
                <tr>
                  <td class="lab"><i class="fa fa-key font14 ys-info-color"></i></td>
                  <td>
                    <input type="text"
                           class="ys-input ys-input-bg fullWidth"
                           v-model="gcode"
                           placeholder="二次验证码"
                           @change="closeStatus()"
                           v-validate:password="{required: { rule: true, message: '请输入密码!'}}"/>
                  </td>
                </tr>
                <tr v-if="status">
                  <td></td>
                  <td>{{statusMsg}}</td>
                </tr>
                <tr>
                  <td></td>
                  <td><input type="button" value="验证" @click="twoFactor" class="ys-btn fullWidth"/></td>
                </tr>
                <tr>
                  <td></td>
                  <td>
                    <p><i class="fa fa-info-circle m-r-3 ys-info-color"></i>打开您移动设备上的二次验证APP,</p>
                    <p style="text-indent:13px;">并输入验证码</p>
                  </td>
                </tr>
                </tbody>
              </table>
            </validator>
          </div>
        </div>
      </div>
      <div class="ys-box" v-show="page==3">
        <div class="ys-box-title">注册</div>
        <div class="ys-box-con">
          <div class="login-module">
            <validator name="vRegister">
              <table class="login-table">
                <tbody>
                <tr>
                  <td class="lab textR ys-info-color">邮箱</td>
                  <td class="pos-r">
                    <input type="text"
                           class="ys-input ys-input-bg fullWidth"
                           v-model="registerData.email"
                           autofocus="autofocus"
                           placeholder="请输入您的邮箱"
                           @change="closeStatus()"
                           v-validate:email="{required: { rule: true, message: '请输入邮箱!' }}"/>
                    <div v-if="$vRegister.email.touched" class="input-warn" style="margin-left:4px;">
                      <span v-if="$vRegister.email.required">{{ $vRegister.email.required }}</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="lab textR ys-info-color">密码</td>
                  <td class="pos-r">
                    <input type="password"
                           class="ys-input ys-input-bg fullWidth"
                           v-model="registerData.password"
                           placeholder="6位以上,字母,数字,字符"
                           @change="closeStatus()"
                           v-validate:password="{required: { rule: true, message: '请输入密码!'}}"/>
                    <div v-if="$vRegister.password.touched" class="input-warn" style="margin-left:4px;">
                      <span v-if="$vRegister.password.required">{{ $vRegister.password.required }}</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="lab textR ys-info-color">确认密码</td>
                  <td class="pos-r">
                    <input type="password"
                           class="ys-input ys-input-bg fullWidth"
                           v-model="registerData.confirm_password"
                           placeholder="确认密码"
                           @change="closeStatus()"
                           v-validate:_password="['required', '_password']"/>
                    <div v-if="$vRegister._password.touched" class="input-warn" style="margin-left:4px;">
                      <span v-if="$vRegister._password._password">两次输入密码不一致!</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="lab textR ys-info-color">手机</td>
                  <td class="pos-r">
                    <input type="text"
                           class="ys-input ys-input-bg fullWidth"
                           v-model="registerData.phone"
                           placeholder="请输入手机号"
                           @change="closeStatus()"
                           v-validate:phone="{required: { rule: true, message: '请输入手机号!'}}"/>
                    <div v-if="$vRegister.phone.touched" class="input-warn" style="margin-left:4px;">
                      <span v-if="$vRegister.phone.required">{{ $vRegister.phone.required }}</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="lab textR ys-info-color">验证码</td>
                  <td class="pos-r">
                    <input type="text"
                           class="ys-input ys-input-bg"
                           v-model="registerData.captcha"
                           style="width:90px"
                           @change="closeStatus()"
                           v-validate:captcha="{required: { rule: true, message: '请输入验证码!'}}"/>
                    <span class="captcha-box m-l-10" v-if="captchaStatus">{{captchaTime}}s</span>
                    <a class="m-l-10" v-if="!captchaStatus" @click="getCaptcha">获取验证码</a>
                    <div v-if="$vRegister.captcha.touched" class="input-warn" style="margin-left:4px;">
                      <span v-if="$vRegister.captcha.required">{{ $vRegister.captcha.required }}</span>
                    </div>
                  </td>
                </tr>
                <tr v-if="status">
                  <td></td>
                  <td>{{statusMsg}}</td>
                </tr>
                <tr>
                  <td></td>
                  <td><input type="button" value="注册" @click="register" class="ys-btn fullWidth"/></td>
                </tr>
                </tbody>
              </table>
              <p class="textC" v-if="registerStatus">恭喜您注册成功! 将会在{{registerTime}}s后自动跳转到登录</p>
              <p class="textR m-t-20">已有账号?<a class="m-l-3" @click="returnLogin()">返回登录</a></p>
            </validator>
          </div>
        </div>
      </div>
      <div class="ys-box" v-show="page==4">
        <div class="ys-box-con">
          <div class="login-module">
            <validator name="vRegister">
              <p class="textC">禁止注册，请联系机房管理员</p>
              <p class="textR m-t-20">已有账号?<a class="m-l-3" @click="page=1">返回登录</a></p>
            </validator>
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
    padding:14px 4px;
  }
  .login-table .label{

  }
  .top-content{
    position: relative;
  }
  .login-box{
    position: absolute;
    width:300px;
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
import { changeMenu } from 'src/lib/actions'
import { changeFromLogin } from 'src/lib/actions'
module.exports = {
  vuex: {
    actions: {
      changeMenu,
      changeFromLogin
    }
  },
  data: function() {
    return {
      remember:true,
      username: null,
      password: null,
      gcode:null,
      status:false,
      statusMsg:"",
      token:"",
      page:1,//1登录 2验证 3注册 4禁止登录页面
      registerData:{
        email:"",
        password:"",
        confirm_password:"",
        phone:"",
        captcha:"",
        hostname:location.hostname
      },
      captchaStatus:false,
      captchaTime:150,
      registerStatus:false,
      registerTime:5,
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
    var self=this;
    $(".inner-bg").css({'height':$(window).height()+"px"});
    $(window).resize(function() {
      $(".inner-bg").css({'height':$(window).height()+"px"});
    });
    document.addEventListener('keydown', this.documentHandler)
      self.username = localStorage.getItem('current_user')
  },
  beforeDestroy(){
    document.removeEventListener('keydown', this.documentHandler);
  },
  methods: {
    documentHandler(e){
      let self=this;
      if(e.keyCode == 13){
        if(self.page==1){
          self.login()
        }else if(self.page==2){
          self.twoFactor()
        }else{
          self.register()
        }
      }
    },
    get_register_status () {
      this.$http.get('/api/register_status').then(function (response) {
        if (response.data.status === 200) {
          if (response.data.data.status === 0) {
            this.page = 4
          } else {
            this.page = 3
          }
        } else {
          this.page = 3
        }
      })
    },
    login(){
      let data = {
        username: this.username,
        password: this.password,
        step:"auth"
      };
      this.removeStorage()
      this.$root.loadStatus=true;
      this.$http.post('/api/login', data).then(function (response) {
        this.$root.loadStatus=false;
        if (response.data.status == 200) {
          if(response.data.data.step=="token"){
            this.token=response.data.data.token;
            this.page=2;
          }else{
            this.setStorage(response.data.data);
            this.changeFromLogin(true);
            this.$root.loadStatus=true;
            let self=this;
            setTimeout(function(){
              self.$router.go("/dp")
            },2000)
          }
        } else {
          this.status=true
          this.statusMsg=response.data.msg
        }
      })
    },
    returnLogin(){
      this.page=1;
      this.$validation1.userName.required="";
      this.$validation1.password.required="";
    },
    twoFactor(){
      let data = {
        token: this.token,
        g_code: this.gcode,
        step : "token"
      };
      this.removeStorage()
      this.$http.post('/api/login', data).then(function (response) {
        if (response.data.status == 200) {
          this.setStorage(response.data.data);
          window.location.href="/dp/home";
        } else {
          this.status=true
          this.statusMsg=response.data.msg
        }
      })
    },
    setStorage(data){
      if(this.remember){
        localStorage.setItem('current_user', data.username)
      }else{
        sessionStorage.setItem('current_user', data.username)
      }
    },
    removeStorage(){
      localStorage.removeItem("current_user")
      sessionStorage.removeItem("current_user")
    },
    getCaptcha(){
      let data={
        email:this.registerData.email,
        phone:this.registerData.phone
      }
      this.$http.post('/api/phone_captcha', data).then(function (response) {
        if(response.data.status == 200){
          this.setCaptchaTime();
        }else{
          this.status=true
          this.statusMsg=response.data.msg
        }
      })
    },
    register(){
      this.$http.post('/api/register', this.registerData).then(function (response) {
        if(response.data.status == 200){
          this.captchaStatus=false;
          this.registerStatus=true;
          this.setRegisterTime();
        }else{
          this.status=true
          this.statusMsg=response.data.msg
        }
      })
    },
    setCaptchaTime(){
      this.captchaStatus=true;
      this.captchaTime=150;
      let self = this
      let repeat=setInterval(function () {
        if(self.captchaTime==0){
          self.captchaStatus=false;
          clearInterval(repeat);
        }else{
          self.captchaTime -= 1
        }
      }, 1000)
    },
    setRegisterTime(){
      this.registerTime=5;
      let self = this
      let repeat=setInterval(function () {
        if(self.registerTime==1){
          self.page=1;
          this.registerStatus=false;
          clearInterval(repeat);
        }else{
          self.registerTime -= 1
        }
      }, 1000)
    },
    closeStatus(){
      this.status=false
      this.statusMsg=""
    }
  },
  watch:{
    username:function(){
      this.status=false
    },
    password:function(){
      this.status=false
    },
    gcode:function(){
      this.status=false
    },
    page:function(){
      this.statusMsg="";
    }
  },
  validators: {
    email: function (val/*,rule*/) {
      if (val == "") {
        return true
      }
      return /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(val)
    },
    _password: function (val) {
      return this.vm.registerData.password == this.vm.registerData.confirm_password
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
