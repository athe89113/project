<template>
  <div>
    <ul class="ys-nav">
      <li class="waves-effect waves-light">
        <a v-link="{ name: 'node-state-topo', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">级联拓扑</span>
        </a>
      </li>
      <li>
        <a v-link="{ name: 'node-state-parent', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">上级状态</span>
        </a>
      </li>
      <li>
        <a v-link="{ name: 'node-state-children', activeClass: 'on'}">
          <span class="ys-nav-cor"></span>
          <span class="text">下级状态</span>
        </a>
      </li>
      <div class="clearfix"></div>
    </ul>
    <router-view></router-view>
  </div>
</template>

<script>
  import Api from 'src/lib/api'
  export default {
    name: "node-state",
    data(){
      return {
      }
    },
    ready: function () {
    },
    methods:{
    },
    components: {
    }
  }
</script>
