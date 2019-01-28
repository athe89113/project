<template>
  <div class="content-page">
    <!-- Start content -->
    <div class="content">
      <!--<div class="container-dis"-->
           <!--v-show="$route.topic!='hids' && $route.topic!='service_support'">-->
        <!--<p>当前功能未激活，请联系厂商</p>-->
      <!--</div>-->
      <div class="container">
          <router-view></router-view>
      </div> <!-- container -->
    </div> <!-- content -->
  </div>
</template>
<script>
  export default {
    data() {
      return {

      }
    },
    ready:function(){
    },
    events: {
      'alert-msg': function (status, msg) {
        if (status==200){
          this.alertSuccess = true
        }else{
          this.alertError = true
        }
        this.errorMsg = msg
      }
    }
  }
</script>
<style>
  .content-page {
    left: 180px;
    right: 0px;
    padding-top: 50px;
    z-index: 4;
    margin-left: 180px;
  }
  .small-content-page{
    margin-left: 46px;
    transition-property: margin-left;
    transition-duration: 1000ms;
  }
  .big-content-page{
    margin-left: 180px;
    transition-property: margin-left;
    transition-duration: 1000ms;
  }
  .content-page > .content {
    padding: 15px;
  }
  .container-dis{
    background: rgba(0,0,0,0.7)!important;
    position: fixed;
    top: 0px;
    bottom: 0px;
    right: 0px;
    left: 190px;
    cursor:not-allowed;
    z-index:999;
  }
  .container-dis p{
    margin:0px auto;
    text-align:center;
    position: relative;
    top:50%;
    transform:translateY(-50%);
    font-size:14px;
  }
  .confirm-dialog{
    width:200px!important;
    height:80px!important;
    position: absolute!important;
    top:50%;
    left:50%;
    margin-top:-250px!important;
    margin-left:-100px!important;
  }
  .confirm-dialog .modal-body{
    min-height:80px!important;
  }
  .modal-content{
    padding:0px!important;
    background:rgba(0,0,0,0.7)!important;
    border:none!important;
    color:#f2f2f2!important;
  }
  .confirm-dialog .modal-content{
    padding:0px!important;
    background:rgba(0,0,0,0.7);
    border:none;
    color:#f2f2f2;
  }
  .confirm-dialog .modal-body{
    padding:15px!important;
  }
  .confirm-p{
    color:#c4bdd2
  }
  .confirm-p i{margin-right:3px;}
  .confirm-btn{
    width:80px;
    height:32px;
    text-align:center;
    line-height:30px;
    border:none;
    border-radius: 3px;
  }
  .confirm-btn.sure{
    background: rgba(44,126,191,0.75);
    border: 1px solid #357ebd;
    color: #f2f2f2;
  }
  .confirm-btn.quit{
    background: rgba(210,207,230,0.75);
    border: 1px solid #d2cfe6;
  }
  .operate-dialog{
    width:300px!important;
    height:200px!important;
    margin-top:-250px!important;
    margin-left:-150px!important;
    color:#000000;
  }
  .operate-dialog .modal-body{
    min-height:300px!important;
  }
</style>

