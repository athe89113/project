<template>
  <div>
    <ul class="ys-nav">
      <li class="waves-effect waves-light">
        <a v-link="{ name: 'email-smtp', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">SMTP</span>
        </a>
      </li>
      <li>
        <a v-link="{ name: 'email-cloud', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">SendCloud</span>
        </a>
      </li>
      <div class="clearfix"></div>
    </ul>
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'email',
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
