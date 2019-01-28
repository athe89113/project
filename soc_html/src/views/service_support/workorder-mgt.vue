<template>
  <div>
    <div class="pageHead">
      <p class="pageTitle"><span>支持管理 </span>- 工单管理</p>
    </div>
    <ul class="ys-nav">
      <li v-if="role_type==2 || role_type==3">
        <a v-link="{ name: 'workorder-apply', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">工单申请</span>
        </a>
      </li>
      <li class="waves-effect waves-light" v-if="role_type==1 || role_type==2">
        <a v-link="{ name: 'workorder-deal', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">工单处理</span>
        </a>
      </li>
      <div class="clearfix"></div>
    </ul>
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    computed: {
      role_type () {
        return this.$store.state.user.role_type
      },
    },
  }
</script>
