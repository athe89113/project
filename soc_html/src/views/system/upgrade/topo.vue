<template>
  <ul>
    <li v-for="per in options">
      <div class="treeList"
           v-bind:class="[selectClass(per),statusClass(per.status)]"
           @click="selectTarget(per)">
        <p class="icon-bg" v-bind:class="[per.is_self==1 ? 'cur' : '']">
          <i class="ys-icon typeIcon verticalM"
             v-bind:class="per.u_type | iconFil"
             style="font-size:18px;"></i>
        </p>
        <p style="margin-top:7px;"><i class="ys-icon icon-map" v-show="per.is_self==1"></i>{{per.name}}</p>
      </div>
      <upgrade-topo :options="per.children" v-if="per.children.length>0"></upgrade-topo>
    </li>
  </ul>
</template>
<style scoped>
  .tree ul {
    position: relative;
    padding: 20px 0;
    white-space: nowrap;
    margin: 0 auto;
    text-align: center;

  }

  .tree ul::after {
    content: '';
    display: table;
    clear: both;
  }

  .tree li {
    display: inline-block;
    vertical-align: top;
    text-align: center;
    list-style-type: none;
    position: relative;
    padding: 20px .5em 0 .5em;

  }

  .tree li::before,
  .tree li::after {
    content: '';
    position: absolute;
    top: 0;
    right: 50%;
    border-top: 1px solid #5373b1;
    width: 50%;
    height: 20px;
  }

  .tree li::after {
    right: auto;
    left: 50%;
    border-left: 1px solid #5373b1;
  }

  .tree li:only-child::after,
  .tree li:only-child::before {
    display: none;
  }

  .tree li:only-child {
    padding-top: 0;
  }

  .tree li:first-child::before,
  .tree li:last-child::after {
    border: 0 none;
  }

  .tree li:last-child::before {
    border-right: 1px solid #5373b1;
    border-radius: 0 5px 0 0;
  }

  .tree li:first-child::after {
    border-radius: 5px 0 0 0;
  }

  .tree ul ul::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    border-left: 1px solid #5373b1;
    width: 0;
    height: 20px;
  }

  .tree li .treeList {
    border: 1px dashed rgba(74,146,255,0.6);
    background: none;
    text-align: center;
    width:98px;
    height:90px;
    text-decoration: none;
    display: inline-block;
    border-radius: 3px;
    position: relative;
    top: 1px;
    cursor:pointer;
  }
  .tree li .treeList .typeIcon{
    color:#463f4d!important;
  }
  .treeList .icon-bg{
    width:36px;
    height:36px;
    display: inline-block;
    background:#4a92ff;
    color:rgba(0,0,0,0);
    border-radius: 2px;
    line-height:36px;
    margin-top:17px;
  }
  .treeList .icon-bg.cur{
    background:#00bd85;
  }
  .treeList.on{
    border:1px solid #00bd85!important;
  }
  .treeList.hasUpgrade{
    border:none!important;
    background:rgba(74,146,255,0.13)!important;
  }
  .treeList.hasUpgrade:before{
    content:'';
    position:absolute;
    right:-1px;
    top:-1px;
    width:44px;
    height:44px;
    background:url(../../../assets/images/system-upgrade-ok.png);
  }
  .treeList.noUpgrade:before{
    content:'';
    position:absolute;
    right:-1px;
    top:-1px;
    width:44px;
    height:44px;
    background:url(../../../assets/images/system-upgrade-false.png);
  }
  .treeList.on:before{
    content:'';
    position:absolute;
    right:0px;
    bottom:0px;
    width:12px;
    height:12px;
    background:#00bd85;
    border-radius: 2px;
  }
  .treeList.on:after{
    font-family:'ys';
    content:"\E82C";
    position:absolute;
    right:-1px;
    bottom:-1px;
  }
</style>
<script>
  export default {
    name: 'upgrade-topo',
    props: {
      options: [],
      target:[]
    },
    filters: {
      iconFil: function (type) {
        switch(type) {
          case "center"://中心服务器
            return "icon-core"
            break;
          case "cloud_defense"://云防服务器
            return "icon-cloud"
            break;
          case "hids"://终端安全服务器
            return "icon-computer"
            break;
          case "defense"://高防服务器
            return "icon-defense"
            break;
          case "nids"://网络安全服务器
            return "icon-internet"
            break;
          case "monitor"://监控服务器
            return "icon-monitor"
            break;
          case "scan"://漏扫服务器
            return "icon-scan"
            break;
          default:
            return "icon-core"
        }
      }
    },
    data () {
      return {
        show: false,
      }
    },
    ready: function () {


    },

    methods: {
      selectClass(per){
        if(per.select && per.status==1){
          return "on"
        }else{
          return ""
        }
      },
      statusClass(status){
        switch(status) {
          case 0://不可升级
            return "disabled"
            break;
          case 1://可升级
            return "upgrade"
            break;
          case 2://已升级
            return "hasUpgrade"
            break;
          case 3://上级未升级
            return "noUpgrade"
            break;
          default:
            return "upgrade"
        }
      },
      selectTarget(list){
        if(list.status==1){
          list.select=!list.select
        }
      },
    },
    components: {}

  }
</script>