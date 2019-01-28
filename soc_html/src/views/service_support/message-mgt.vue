<template>
  <div class="">
    <div class="pageHead">
      <p class="pageTitle"><span>支持管理 </span>- 消息管理</p>
    </div>
    <ul class="ys-nav">
      <li class="waves-effect waves-light">
        <a v-link="{ name: 'message-all', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">全部消息</span>
          <span v-show="unRead.count != 0" class=" font-600">({{ unRead.count }})</span>
        </a>
      </li>
      <li>
        <a v-link="{ name: 'message-security', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">安全消息</span>
          <span v-show="unRead.security != 0" class=" font-600">({{ unRead.security }})</span>
        </a>
      </li>
      <li>
        <a v-link="{ name: 'message-monitor', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">故障消息</span>
          <span v-show="unRead.monitor != 0" class=" font-600">({{ unRead.monitor }})</span>
        </a>
      </li>
      <li>
        <a v-link="{ name: 'message-other', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">其他消息</span>
          <span v-show="unRead.other != 0" class=" font-600">({{ unRead.other }})</span>
        </a>
      </li>
      <div class="clearfix"></div>
    </ul>
    <router-view></router-view>
  </div>
</template>

<script>
  import Api from '../../lib/api'
  export default {
    name: "service-support-message",
    data(){
      return {
        unRead: {
          count: 0,
          security: 0,
          monitor: 0,
          other: 0
        }
      }
    },
    ready: function () {
      this.getUnRead()
    },
    methods:{
      getUnRead(){
        this.$http.get({"url": "/api/message", "timeout": 3000}).then(function (response) {
          if(response.status == 200){
              this.unRead = response.data.data
          }
        })
      }

    },
    components: {
    },
    events: {
    'un-read-re': function () {
      this.getUnRead()
    }
  }
  }
</script>
