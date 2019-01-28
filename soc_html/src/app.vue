<template>
  <div>
    <progress :percent.sync="myProgress.percent" :options="myProgress.options"> </progress>
    <alert :show.sync="alertSuccess"
           :duration="3000"
           type="success"
           width="200px"
           placement="top-right"
           dismissable>
      <p>
        <i class="ys-icon icon-check-circle m-r-3"></i>{{errorMsg}}
      </p>
    </alert>
    <alert :show.sync="alertError" :duration="3000" type="danger" width="200px" placement="top-right" dismissable>
      <p>
        <i class="ys-icon icon-warn-circle m-r-3"></i>{{errorMsg}}
      </p>
    </alert>
    <loading-global :show.sync="loadStatus"></loading-global>
    <router-view></router-view>
  </div>
</template>
<script>
  import Api from 'src/lib/api'
  import progress from 'vue-progressbar/vue-progressbar.vue'
  import alert from './components/Alert.vue'
  import loadingGlobal from 'src/components/loading-global.vue'
  import store from 'src/lib/store' // import 我们刚刚创建的 store

  export default {
    data() {
      return {
        alertSuccess: false,
        alertError: false,
        errorMsg: "",
        loadStatus:false,
        myProgress: {
          percent: 0,
          options: {
            show: true,
            canSuccess: true,
            color: '#77b6ff',
            failedColor: 'red',
            height: '2px'
          }
        },
        topic:"11111",
        logoUrl: '',
      }
    },
    store: store,// 在根组件加入 store，让它的子组件和 store 连接
    components: {
      alert,
      progress,
      loadingGlobal
    },
    ready() {
      var hostname = location.hostname
      this.$http.post('/api/agent_info', {hostname: hostname}).then(function (response) {
          if(response.status == 200){
              this.logoUrl = response.data.data.logo,
              document.title = response.data.data.title
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      this.$progress.setHolder(this.myProgress)

    },
  }

</script>