<template>
  <div class="topbar" v-bind:class="topBarStyle">
    <!-- LOGO -->
    <div class="topbar-left">
      <div class="text-center">
        <a class="logo" v-if="userInfo.agent" style="cursor: default"><!--v-link="{ path: '/soc/home' }" -->
          <!--<img v-bind:src="logoUrl"/>-->
          <img src="../assets/images/anguanLogo.png"/>
        </a>
      </div>
    </div>
    <!-- Button mobile view to collapse sidebar menu -->
    <div class="navbar-default">
      <div class="">
        <div class="pull-left">
          <!--<div class="topbar-menu"-->
               <!--v-link="{ path: '/soc/home'}"-->
               <!--v-bind:class="{'on': $route.topic=='home'}">-->
            <!--<p>首页</p>-->
          <!--</div>-->
          <div class="topbar-menu"
               v-show="list.enable==1 && $index<showNum"
               v-for="list in topMenu" track-by="$index"
               @click="goLink(list.link)"
               v-bind:class="{'on': $route.topic==list.topic}">
            <p>{{list.name}}</p>
          </div>
          <div class="topbar-menu"
               v-for="list in customData"
               @click="goCustom(list.link)">
            <p>{{list.name}}</p>
          </div>
          <div class="topbar-more"
               v-if="topMenu.length>showNum"
               v-clickoutside="closeMore"
               v-bind:class="{'on': moreStatus}">
            <a @click="moreStatus=true">
              <i class="ys-icon icon-topbar-more"></i>
              <span>更多</span>
            </a>
            <div class="topbar-more-box" v-if="moreStatus" transition="slide">
              <ul>
                <li v-show="list.enable==1 && $index>=showNum"
                    v-for="list in topMenu"
                    v-bind:class="{'on': $route.topic==list.topic}"
                    @click="goMoreLink(list.link)">{{list.name}}</li>
              </ul>
            </div>
          </div>
          <span class="clearfix"></span>
        </div>
        <div class="fRight">
          <div class="userbox" @click="changeUserList()">
            <img src="../assets/images/user-avatar.png" alt="user-img" class="img-circle mgr5">
            <span>{{userInfo.username}}</span>
            <ul v-show="userList==1">
              <li>
                <a @click="logExit()"><i class="ti-power-off m-r-5"></i> 退出</a>
              </li>
            </ul>
          </div>
        </div>
        <div class="clearfix"></div>
      </div>
    </div>
  </div>
</template>
<script>
  import Api from 'src/lib/api'
  import icon from 'src/components/icon.vue'
  import { changeUser } from 'src/lib/actions'
  import { changeCartNum } from 'src/lib/actions'
  import { changeOrderNum } from 'src/lib/actions'
  import { getCartNum } from 'src/lib/getter'
  import { getOrderNum } from 'src/lib/getter'
  import { getMenu } from 'src/lib/getter'
  import clickoutside from 'src/directives/clickoutside';
  export default {
    directives: { clickoutside },
    vuex: {
      getters: {
        cartNum: getCartNum,
        menuList: getMenu,
        orderNum:getOrderNum
      },
      actions: {
        changeUser,
        changeCartNum,
        changeOrderNum
      }
    },
    computed: {
      role_type () {
        return this.$store.state.user.role_type
      },
      logoUrl: {
        get: function () {
          return this.$root.logoUrl
        }
      },
      showNum:{
        get: function () {
          let width=$(document).width()-600;
          let num=Math.floor(width/80);
          if(this.menuNum!=0){
            return this.menuNum
          }else{
            return num;
          }
        }
      },
      topMenu(){
        let menuData=[];
        let data=this.menuList;
        for(let x in data){
          for(let y in this.topData){
            if(data[x].topic==this.topData[y].topic){
              if(data[x].topic=="service_support"){
                if(this.$store.state.user.role_type==3){
                  let list=data[x];
                  list.link="user-mgt";
                  menuData.push(list);
                }else{
                  let list=data[x];
                  list.link="company";
                  menuData.push(list);
                }
              }else{
                let list=data[x];
                list.link=this.topData[y].link;
                menuData.push(list);
              }

            }
          }
        }
        let arr=[];
        for(let x in menuData){
          if(menuData[x].enable==1){
            arr.push(menuData[x])
          }
        }
        return arr;
      }
    },
    data() {
      return {
        iconId:0,
        userInfo: [],
        showMessage: false,
        showWorkOrder: false,
        messages: {
          count: 0,
          security: 0,
          assets: 0,
          monitor: 0,
          other: 0
        },
        orders: {
          count: 0,
          security: 0,
          assets: 0,
          monitor: 0,
          other: 0
        },
        userList:0,
        topData:[
          {
            link:"home",
            topic:"home",
          },
          {
            link:"dashboard",
            topic:"asset",
          },
          {
            link:"mon-dashboard",
            topic:"monitor"
          },
          {
            link:"defense-dashboard",
            topic:"defense"
          },
          {
            link:"cloud-defense-dash",
            topic:"cloud_defense"
          },
          {
            link:"waf-dash",
            topic:"waf"
          },
          {
            link:"scan-dashboard",
            topic:"dashboard"
          },
          {
            link:"hids-file",
            topic:"hids"
          },
          {
            link:"nids-base",
            topic:"nids"
          },
          {
            link:"user-mgt",
            topic:"service_support"
          },
          {
            link:"admin-mgt",
            topic:"system"
          },
          {
            link:"dbs-overview",
            topic:"db-security"
          },
          {
            link:"create-ds",
            topic:"di"
          },
          {
            link:"knowledge-mgt",
            topic:"op"
          },
          {
            link:"new-global",
            topic:"ssa"
          },
            {
            link:"scan-search",
            topic:"scan"
          },
          {
            link:'dama-mgt',
            topic: 'dama'
          },
          {
            link:'data-report-mgt',
            topic: 'data-report'
          },
          {
            link:'analysis-event-search',
            topic: 'event-detect'
          }
        ],
        customData:[],
        topBarStyle:"",
        moreStatus:false,
        menuNum:0,
      }
    },
    ready: function() {
      let self=this;
      window.addEventListener('scroll', this.handleScroll);
      this.$http.get('/api/profile').then(function (response) {
        this.userInfo=response.data.data;
        this.changeUser(response.data.data)
      },function(response){
          Api.user.requestFalse(response,this);
      })
      $(window).resize(function() {
        let width=$(window).width()-600;
        let num=Math.floor(width/80)
        self.menuNum=num;
      });
//      this.get_message_order()
//      this.getCartNum();
//      this.getOrderNum();
    },
    methods: {
      goLink(link){
        let LinkMap = {}
        if (this.role_type == 3) {
          LinkMap = {
            "dashboard": "host-net-device",
            "defense-dashboard": "defense-ip-mgt",
            "mon-dashboard": "server-mon-mgt",
            "scan-dashboard": "scan-domain-list",

          }
        }
        if(LinkMap[link]){
            link = LinkMap[link]
          }
        this.$router.go({"name": link})
      },
      goMoreLink(link){
        this.$router.go({"name": link});
        this.moreStatus=false
      },
      handleScroll () {
        if(getScrollTop()==0){
          this.topBarStyle="";
        }else{
          this.topBarStyle="scroll-top-bar";
        }
        function getScrollTop(){
          var scrollTop = 0, bodyScrollTop = 0, documentScrollTop = 0;
          if(document.body){
            bodyScrollTop = document.body.scrollTop;
          }
          if(document.documentElement){
            documentScrollTop = document.documentElement.scrollTop;
          }
          scrollTop = (bodyScrollTop - documentScrollTop > 0) ? bodyScrollTop : documentScrollTop;
          return scrollTop;
        }
      },
      logExit:function(){
        this.$http.get('/api/logout').then(function (response) {
          if (response.data.status === 200) {
            this.$router.go({name: "login"});
          } else {
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      getCartNum(){
        this.$http.get({"url": "/api/purchase/shopping_cart", "timeout": 3000}).then(function (response) {
          if(response.status == 200){
            this.changeCartNum(response.data.data.total_num);
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      getOrderNum(){
        this.$http.get({"url": "/api/purchase/order", "timeout": 3000}).then(function (response) {
          if(response.status == 200){
            this.changeOrderNum(response.data.data.unpaid);
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      get_message_order(){
        this.$http.get({"url": "/api/message", "timeout": 3000}).then(function (response) {
          if(response.status == 200){
              this.messages = response.data.data
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
        //获取信息
        this.$http.get({"url": "/api/ticket/service", "timeout": 3000}).then(function (response) {
          if(response.status == 200){
              this.orders = response.data.data
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
        //获取工单
      },
      goToOrderDeal(){
        this.$router.go({name: "workorder-deal"})

      },
      goToTicketAdd(){
        this.$router.go({name: "workorder-apply","params": {"type": "create"}})
      },
      changeUserList(){
        if(this.userList==1){this.userList=0}else{this.userList=1}
      },
      goCustom(link){
        window.open(link);
      },
      closeMore(){
        this.moreStatus=false;
      }
    },
    beforeDestroy() {

    },
    components: {
      icon
    }
  }
</script>
<style scoped>
  .topbar {
    left: 0px;
    position: fixed;
    right: 0;
    top: 0px;
    z-index: 3;
    color:#f2f2f2;
    background: rgba(0,0,0,0.25);
  }
  .topbar .topbar-left {
    float: left;
    position: relative;
    width: 180px;
    z-index: 1;
  }
  .logo {
    color: #ffffff !important;
    font-size: 20px;
    line-height: 50px;
  }
  .navbar-default {
    background-attachment: fixed;
    background-size: cover;
    margin-left:180px;
    height:50px;
    box-shadow: -3px -2px 2px 1px rgba(0,0,0,0.05) inset;
  }
  .slide-transition {
    display: inline-block; /* 否则 scale 动画不起作用 */
  }
  .slide-enter {
    animation: antSlideUpIn .5s;
  }
  .slide-leave {
    animation: antSlideUpOut 0s;
  }
  @-webkit-keyframes antSlideUpIn {
    0% {
      opacity: 0;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(0.8);
      transform: scaleY(0.8);
    }
    100% {
      opacity: 1;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
  }
  @keyframes antSlideUpIn {
    0% {
      opacity: 0;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(0.8);
      transform: scaleY(0.8);
    }
    100% {
      opacity: 1;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
  }
  @-webkit-keyframes antSlideUpOut {
    0% {
      opacity: 1;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
    100% {
      opacity: 0;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(0.8);
      transform: scaleY(0.8);
    }
  }
  @keyframes antSlideUpOut {
    0% {
      opacity: 1;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(1);
      transform: scaleY(1);
    }
    100% {
      opacity: 0;
      -webkit-transform-origin: 0% 0%;
      transform-origin: 0% 0%;
      -webkit-transform: scaleY(0.8);
      transform: scaleY(0.8);
    }
  }
  .logo{
    border:none!important;
  }
  .logo img{
    height:36px;
    margin-top: 10px;
  }
  .scroll-top-bar:before{
    content:"";
    position: absolute;
    top:0px;
    width:100%;
    height:100%;
    z-index:-2;
    background: linear-gradient(145deg, #283868 0%, #495373 100%);
  }
  .scroll-top-bar:after{
    content:"";
    position: absolute;
    top:0px;
    width:100%;
    height:100%;
    z-index:-1;
    background: rgba(0,0,0,0.2);
  }
  .topbar-menu{
    width:80px;
    height:50px;
    float:left;
    cursor: pointer;
    display:inline-block;
    color:#9abcee;
  }
  .topbar-menu>span{
    margin-top:8px;
    display:block;
    color:#9abcee;
    text-align:center;
    height:20px;
  }
  .topbar-menu span i{
    font-size:14px;
  }
  .topbar-menu span img{
    width:14px;
  }
  .topbar-menu p{
    text-align:center;
    line-height:50px;
  }
  .topbar-menu.on{
    color:#f2f2f2;
    background: linear-gradient(145deg, #4a92ff 1000%, #2cb7ff 100%);
    transition-property: background;
    transition-duration: 5500ms;
  }
  .topbar-menu.on span{
    color:#f2f2f2;
  }
  .navbar-default{
    background:none;
  }
  .right-icon-box{
    display: inline-block;
    width:36px;
    height:50px;
    line-height:50px;
    cursor:pointer;
    float:left;
  }
  .extend{
    width:70px;
    overflow: hidden;
    transition-property: width;
    transition-duration: 300ms;
    transition-timing-function: ease-out;
  }
  .icon-mark{
    position:absolute;
    left:8px;
    top:5px;
    z-index:1;
    display: inline-block;
    min-width: 10px;
    color: #fff;
    line-height: 1;
    vertical-align: middle;
    white-space: nowrap;
    text-align: center;
    border-radius: 10px;
    text-transform: uppercase;
    padding: 3px 6px;
    margin-top: 1px;
    background-color: #ea6256;
    font-size:10px;
    transform:scale(0.8);
    font-weight: normal;
  }
  .userbox{
    display: inline-block;
    height:50px;
    line-height: 50px;
    padding:0px 10px;
    cursor:pointer;
    position: relative;
    /*border-left:1px solid rgba(0,0,0,0.3);*/
  }
  .userbox img{
    width:30px;
    height:30px;
  }
  .userbox ul{
    min-width:160px;
    position: absolute;
    top:52px;
    left: auto;
    right: 0;
    background:white;
    border-top-left-radius: 3px;
    border-bottom-left-radius: 3px;
    line-height: normal;
    padding: 4px 0;
  }
  .userbox ul li{
    padding-left:5px;
  }
  .userbox ul li a{
    padding: 6px 20px;
    display: block;
    padding: 3px 20px;
    clear: both;
    font-weight: 400;
    line-height: 1.42857143;
    color: #333;
    white-space: nowrap;
  }
  .topbar-more{
    display: inline-block;
    height:50px;
    line-height:50px;
    width:56px;
    text-align:center;
  }
  .topbar-more.on,.topbar-more:hover{
    color:#f2f2f2;
    background: rgba(0,0,0,0.2);
    transition-property: background;
    transition-duration: 2000ms;
    position: relative;
  }
  .topbar-more-box{
    position:absolute;
    top:50px;
    width:100px;
    background:#161a2f;
    background: linear-gradient(to right, #1c1c2d 0%, #2d2831 100%);
    border-top:none;
    border-radius: 3px;
    box-shadow: 2px 2px 5px 1px rgba(0,0,0,0.3);
    right:0px;
  }

  .topbar-more-box ul li{
    color:#6591d2;
    padding-left:10px;
    height:32px;
    line-height:32px;
    cursor: pointer;
    overflow: hidden;
    text-align:left;
  }
  .topbar-more-box ul li:hover{
    color:#6591d2;
    background: rgba(74, 146, 255, 0.2);
  }
  .topbar-more-box ul li.on{
    color:#ffffff;
    background:#4a92ff;
  }
  .topbar-more-box ul li.on:hover{
    color:#ffffff;
    background:#4a92ff;
  }
</style>
