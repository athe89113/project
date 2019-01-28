<template>
  <div :class="[mt == 10 ? 'm-t-10' : 'm-t--10']">
    <div class="info-head">
      <span v-show="head">
        <i class="ys-icon icon-check-circle ys-success-color" v-if="status==true"></i>
        <i class="ys-icon icon-clear-circle ys-error-color" v-if="status==false && required==true"></i>
        <i class="ys-icon icon-minus-circle ys-warn-color" v-if="status==false && required==false"></i>
        <i class="ys-icon icon-ellipsis" v-if="status=='loading'"></i>
       <span class="ys-info-color">{{name}}</span>
      </span>
    </div>
    <span v-show="body">
      <span v-if="status==true">{{smsg}}</span>
      <span v-if="status==false && required==true" class="ys-error-color">{{emsg}}</span>
      <span v-if="status==false && required==false">{{emsg}}</span>
      <a v-if="status==false && retry==true" class="m-l-5" @click="call_retry()">重试</a>
      <a v-if="status==false && router" class="m-l-5" @click="goRoute()">设置</a>
      <span v-show="status=='loading' && body">
        <loading-mini :show.sync="true"></loading-mini>
      正在检查
    </span>
    </span>

  </div>
</template>
<style scoped>
  .info-head {
    width: 100px;
    display: inline-block;
  }
  .m-t--10{
    margin-top: -10px;
  }
</style>

<script>
  export default {
    name: 'info-line',
    props: {
      id: {
        type: String,
      },
      name: {
        type: String,
      },
      smsg: {
        type: String,
      },
      emsg: {
        type: String,
      },
      status: {
        twoWay: true,
        default: 'loading'
      },
      required: {
        default: true
      },
      retry: {
        default:  true
      },
      head: {
        default:  true
      },
      body: {
        default:  true
      },
      router: {
        default: false
      },
      mt: {
        default: 10
      }
    },
    data () {
      return {
        loading: false,

      }
    },
    ready: function () {
      if(this.status=='loading'){
        this.loading = true
      }
    },
    methods: {
      call_retry () {
        this.status = 'loading'
        this.$dispatch('Callretry', this.id)
      },
      goRoute(){
        this.$router.go({name: this.router})
      }
    },
    components: {},
    watchs: {
      status: function (val) {
        if(val=='loading'){
          this.loading = true
        }else {
          this.loading = false
        }
      }

    }

  }
</script>