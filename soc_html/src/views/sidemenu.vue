<template>
  <div class="left side-menu"
       v-bind:class="[status=='big' ? 'big-menu' : 'small-menu']">
    <div class="sidebar-inner slimscrollleft pos-r">
      <!--- Divider -->
      <div class="user-info" v-show="$route.topic=='home' && status=='big'">
        <p class="user-avatar">
          <img src="../assets/images/user-avatar.png" alt="user-img" class="img-circle mgr5">
        </p>
        <div class="user-con">
          <p>{{userInfo.username}}，欢迎您！</p>
          <table class="ys-info-table ys-info-color m-t-10">
            <tr>
              <td>角色类别：</td>
              <td>{{userInfo.role}}</td>
            </tr>
            <tr>
              <td>上次登录：</td>
              <td>{{userInfo.last_login_ip}}</td>
            </tr>
            <tr>
              <td></td>
              <td>{{userInfo.last_login | front}}</td>
            </tr>
            <tr>
              <td></td>
              <td>{{userInfo.last_login | back}}</td>
            </tr>
          </table>
        </div>
      </div>
      <div id="sidebar-menu" v-show="status=='big'">
        <ul style="display: none;">
          <li class="has_sub" v-for="parent in homeLink">
            <a class="second_menu">
              <span class="menuIcon"><i v-bind:class="parent.icon" class="icon"></i></span>
              <span class="verticalM">{{parent.name}}</span>
            </a>
            <ul v-show="$index==0">
              <li v-for="child in parent.data">
                <a v-link="{ name: child.link}" v-show="child.link!='company'||role_type!=3"
                   v-bind:class="{'subdrop': $route.menu==child.menu}">
                  {{child.name}}
                </a>
              </li>
            </ul>
          </li>
        </ul>
        <ul>
          <li class="has_sub" v-for="parent in curMenus" v-show="parent.enable==1">
            <a class="second_menu">
              <span class="menuIcon"><i v-bind:class="parent.icon" class="icon"></i></span>
              <span class="verticalM">{{parent.name}}</span>
            </a>
            <ul v-show="$index==0">
              <li v-for="child in parent.children" v-show="child.enable==1">
                <a v-link="{ name: child.link}"
                   v-bind:class="{'subdrop': $route.menu==child.menu}"><span style="margin-right:8px;">·</span>{{child.name}}</a>
              </li>
            </ul>
          </li>
        </ul>
        <ul v-show="$route.topic=='business'">
          <li class="has_sub" v-for="parent in businessLink">
            <a class="second_menu">
              <span class="menuIcon"><i v-bind:class="parent.icon" class="icon"></i></span>
              <span class="verticalM">{{parent.name}}</span>
            </a>
            <ul v-show="$index==0">
              <li v-for="child in parent.data">
                <a v-link="{ name: child.link}" v-show="child.link!='company'||role_type!=3"
                   v-bind:class="{'subdrop': $route.menu==child.menu}">
                  {{child.name}}
                </a>
              </li>
            </ul>
          </li>
        </ul>
        <div class="clearfix"></div>
      </div>
      <div id="small-sidebar-menu" v-show="status=='small'" class="small-sidebar-menu">
        <ul>
          <li class="has_sub pos-r"
              v-for="parent in curMenus"
              v-show="parent.enable==1">
            <a class="second_menu"
               style="display: block;">
              <span class="menuIcon"><i v-bind:class="parent.icon" class="icon"></i></span>
            </a>
            <ul style="display: none">
              <li class="small-menu-title"><span class="">{{parent.name}}</span></li>
              <li v-for="child in parent.children" v-show="child.enable==1">
                <a v-link="{ name: child.link}"
                   class="ys-info-color"
                   v-bind:class="{'subdrop': $route.menu==child.menu}">
                  {{child.name}}
                </a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
      <div class="clearfix"></div>
      <div class="menu-fold">
        <span @click="changeMenuStyle()">
          <i class="ys-icon ys-primary-color"
             v-bind:class="[status=='big' ? 'icon-arrow-left' : 'icon-arrow-right']"></i>
        </span>
      </div>
      <div class="textC ys-info-color" style="position:absolute;bottom:10px;width:100%;">{{versionData.version}}</div>
    </div>
  </div>
</template>
<style scoped>
  .side-menu {
    bottom: 0;
    top: 0;
    width: 180px;
    z-index: 4;
  }
  .side-menu.left {
    background:rgba(0, 0, 0, 0.25);
    position: absolute;
    top: 50px;
  }
  .second_menu.hover{
    background:rgba(0, 0, 0, 0.15);
  }
  .second_menu.on{
    background:rgba(0, 0, 0, 0.15);
    color:#00bd85!important;
  }
  .second_menu.on:hover{
    background:rgba(0, 0, 0, 0.15);
    color:#00bd85!important;
  }
  .second_menu.on .menuIcon{
    color:#00bd85!important;
    border: 1px solid #00bd85!important;
  }
  #sidebar-menu {
    padding-bottom: 30px;
    width: 100%;
    padding-top:10px;
  }
  #sidebar-menu ul ul{
    width:180px;
    left:0px;
    position: relative;
    background: rgba(0,0,0,0.15);
    padding-bottom:20px;
  }
  #sidebar-menu p{
    height:50px;
    line-height:50px;
    color:#e4e6f1;
    padding-left:20px;
    margin:0px;
    border-bottom:1px solid rgba(255,255,255, 0.1);
  }
  #sidebar-menu a {
    line-height: 1.3;
  }


  #sidebar-menu ul ul li.active a {
    color: #BFCBDE;
  }
  #sidebar-menu ul ul a {
    color: #7e9fd0;
    display: block;
    padding-left:48px;
    height:35px;
    line-height:35px;
  }
  #sidebar-menu ul ul a.subdrop{
    padding-left:44px;
  }
  #sidebar-menu ul ul a span{
    margin-right:8px;
    font-size:14px;
  }
  #sidebar-menu ul ul a:hover {
    color:#e6edfe!important;
  }
  #sidebar-menu ul ul a i {
    margin-right: 5px;
  }
  #sidebar-menu ul ul ul a {
    padding-left: 80px;
  }
  #sidebar-menu .label {
    margin-top: 2px;
  }
  #sidebar-menu .subdrop {
    color:#e6edfe!important;
    border-left:4px solid #00bd85;
    background:#333d65;
  }
  #sidebar-menu > ul > li > a {
    color: #93a6d8;
    display: block;
    height:45px;
    line-height:43px;
    padding-left: 15px;
    position:relative;
  }
  #sidebar-menu > ul > li > a:hover {
    text-decoration: none;
    color:#93a6d8!important;
  }
  #sidebar-menu > ul > li > a .arrow{
    font-size:20px;
    margin-left:5px;
  }
  #sidebar-menu > ul > li > a .icon{
    font-size:12px;
  }
  .small-sidebar-menu{
    padding-top:25px;
  }
  .small-sidebar-menu>ul>li{
    width:100%;
    height:47px;
    line-height:47px;
    text-align:center;
    cursor: pointer;
  }
  .small-sidebar-menu>ul>li:hover{
    /*background:rgba(0,0,0,0.3);*/
  }
  .small-sidebar-menu>ul>li>ul{
    position:absolute;
    left:54px;
    top:0px;
    width:150px;
    background:#192442;
    min-height:90px;
    box-shadow: rgba(0, 0, 0, 0.5) 0px 0px 15px;
  }
  .small-sidebar-menu>ul>li>ul:before{
    border: 8px solid transparent;
    border-right: 8px solid #192442;
    width: 0;
    height: 0;
    position: absolute;
    left:-16px;
    top:12px;
    content: ' '
  }
  .small-sidebar-menu>ul>li>ul>li{
    text-align: left;
    height:36px;
    line-height:36px;
  }
  .small-sidebar-menu>ul>li>ul>li a{
    display:block;
    padding-left:25px;
  }
  .small-sidebar-menu>ul>li>ul>li a.subdrop{
    background: #00bd85;
    color:#e6edfe!important;
  }
  .small-sidebar-menu .menuIcon{
    margin-right:0px;
    margin-top:0px;
  }
  .small-menu-title{
    color:#4a92ff;
    padding-left:25px;
    border-bottom:1px solid rgba(255,255,255,0.1);
  }
  .small-menu{
    width:46px;
    transition-property: width;
    transition-duration: 1000ms;
  }
  .big-menu{
    width:180px;
    transition-property: width;
    transition-duration: 1000ms;
  }
  .menu-fold{
    position:absolute;
    bottom:40px;
    width:100%;
    text-align: center;
  }
  .menu-fold span{
    display: inline-block;
    width:37px;
    height:37px;
    background:rgba(0,0,0,0.2);
    border-radius: 50%;
    text-align:center;
    line-height:37px;
    cursor:pointer;
  }
  .user-avatar{
    text-align:center;
    padding:20px 0px;
  }
  .user-con{
    padding-left:5px;
  }
  .user-info .user-avatar img{
    width:60px;
    height:60px;
    border-radius: 50%;
    border: 2px solid #4a92ff;
  }
  .menuIcon{
    width:18px;
    height:18px;
    border-radius:50%;
    border:1px solid #4a92ff;
    line-height:16px;
    text-align: center;
    display: inline-block;
    background:none;
    box-shadow:none;
    color:#4a92ff;
    margin-right:10px;
  }

</style>
<script>
require('jquery.slimscrooll')
import {getMenu, getVersion, getUser} from 'src/lib/getter'
export default {
  vuex: {
    getters: {
      menuData: getMenu,
      userInfo:getUser,
      versionData: getVersion,
    },
  },
  ready: function() {
    $(document).click(function(e){
      var _con = $(' #small-sidebar-menu ul li ul ');   // 设置目标区域
      if(!_con.is(e.target) && _con.has(e.target).length === 0){ // Mark 1
        // 功能代码
        $(' #small-sidebar-menu ul li ul ').hide();
        $(' #small-sidebar-menu ').find(".second_menu").removeClass("hover")
      }
    });
  },
  filters: {
    front(val){
      if(val){
        return val.split(" ")[0]
      }else{
        return ""
      }
    },
    back(val){
      if(val){
        return val.split(" ")[1]
      }else{
        return ""
      }
    },
  },
  computed: {
    curMenus:function(){
      let curTopic=this.$route.topic;
      let linkData=this.menuData;
      let totalData=[];
      for(let x in linkData){
        if(linkData[x].topic==curTopic){
          totalData=linkData[x].children
        }
      }
      this.setMenuShow();
      return totalData
    },
    logoUrl: {
      get: function () {
        return this.$root.logoUrl
      }
    }
  },
  data() {
    return {
      status:"big",
      domain_count: 1,
      businessLink:[
        {
          name:"订单中心",
          icon:"ys-icon icon-menu-cart",
          key:"dashboard",
          data:[
            {name:"购物车", link:"shop-cart",menu:"shop-cart"},
            {name:"订单管理", link:"order-mgt",menu:"order-mgt"},
          ]
        },
        {
          name:"发票管理",
          icon:"ys-icon icon-menu-eye-ract",
          key:"config",
          data:[
            {name:"申请发票",link:"invoice-apply",menu:"invoice-apply"},
          ]
        }
      ],
      // homeLink:[
      //   {
      //     name:"信息视图",
      //     icon:"md md-dashboard",
      //     key:"dashboard",
      //     data:[
      //       {name:"信息总览", link:"user-overview",menu:"shop-cart"},
      //       {name:"用户苹果树", link:"user-tree",menu:"order-mgt"},
      //     ]
      //   },
      // ],
    }
  },
  methods: {
    setLink(){
      if(this.serviceSupportLink[0].data){
        if(this.role_type==1){
          this.serviceSupportLink[0].data[3].link="workorder-deal"
        }else{
          this.serviceSupportLink[0].data[3].link="workorder-apply"
        }
      }
    },
    setMenuShow(){
      let repeat=setInterval(function(){
        if($("#sidebar-menu>ul").length>1){
          $("#sidebar-menu>ul>li>a").unbind("click")
          $("#sidebar-menu>ul>li>a").on("click",function(){
            if($(this).parent().find("ul").is(":hidden")){
              $(this).parent().find("ul").slideDown();
              $(this).parent().siblings().find("ul").slideUp();
            }else{
              $(this).parent().find("ul").slideUp();
            }
          })
          $("#sidebar-menu>ul>li>ul>li").on("click",function(){

          })
          clearInterval(repeat)
        }
      },300)
      let show=setInterval(function(){
        if($("#sidebar-menu ul li a.subdrop").parent().parent()){
          $("#sidebar-menu ul li a.subdrop").parent().parent().parent().find(".second_menu").addClass("on");
          $("#sidebar-menu ul li a.subdrop").parent().parent().parent().siblings().find(".second_menu").removeClass("on");
          $("#sidebar-menu ul li a.subdrop").parent().parent().parent().siblings().find("ul").hide();
          $("#sidebar-menu ul li a.subdrop").parent().parent().slideDown();
          clearInterval(show)
        }
      },300)
      let repeatSmall=setInterval(function(){
        if($("#small-sidebar-menu>ul").length>0){
          $("#small-sidebar-menu>ul>li>a").on("mouseover",function(event){
            event.stopPropagation();
            event.preventDefault();
            if($(this).parent().find("ul").is(":hidden")){
              $(this).parent().find("ul").show();
              $(this).parent().siblings().find("ul").hide();
              $(this).parent().find(".second_menu").addClass("hover");
              $(this).parent().siblings().find(".second_menu").removeClass("hover");
            }
          })
          $("#small-sidebar-menu>ul>li>ul>li").on("click",function(event){
            event.stopPropagation();
            event.preventDefault();
            $(this).parent().hide();
            $(this).parent().parent().find(".second_menu").addClass("on");
            $(this).parent().parent().siblings().find(".second_menu").removeClass("on");
          })
          clearInterval(repeatSmall)
        }
      },300)
      let smallShow=setInterval(function(){
        if($("#small-sidebar-menu ul li a.subdrop").parent().parent()){
          $("#small-sidebar-menu ul li a.subdrop").parent().parent().parent().find(".second_menu").addClass("on");
          $("#small-sidebar-menu ul li a.subdrop").parent().parent().parent().siblings().find(".second_menu").removeClass("on");
          clearInterval(smallShow)
        }
      },300)
    },
    handleClose(){
      $("#small-sidebar-menu ul li ul").hide();
    },
    changeMenuStyle(){
      if(this.status=='big'){
        this.status='small';
        $(".content-page").addClass("small-content-page").removeClass("big-content-page")
        this.setMenuShow()
      }else{
        $(".content-page").addClass("big-content-page").removeClass("small-content-page")
        this.status='big'
      }
    }
  },
  components: {

  },
}
</script>
