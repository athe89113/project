<template>
  <div>
    <ul class="ys-nav">
      <li class="waves-effect waves-light">
        <a v-link="{ name: 'two-validation', activeClass:'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">二次验证</span>
        </a>
      </li>
      <li>
        <a v-link="{ name: 'black-list', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">IP黑名单</span>
        </a>
      </li>
      <li>
        <a v-link="{ name: 'white-list', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">IP白名单</span>
        </a>
      </li>
      <div class="clearfix"></div>
    </ul>
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'system-safe',
    data () {
      return {
      }
    },
    ready: function () {
    },
    methods: {
    },
    components: {
    }
  }
</script>

