<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <table class="ys-form-table m-t-10">
        <tr>
          <td class="ys-info-color">地址:</td>
          <td>
            <span>{{ parentNode.ip }}</span>
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">角色:</td>
          <td>
            <span v-if="parentNode.type=='center'">一级中心</span>
            <span v-if="parentNode.type=='sub_center'">二级中心</span>
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">版本:</td>
          <td>
            <span>{{parentNode.version}}</span>
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">连接状态:</td>
          <td>
            <span class="ys-error-color" v-if="parentNode.status==2">连接错误</span>
            <span class="ys-success-color" v-if="parentNode.status==1">已连接</span>
            <span class="ys-warn-color" v-if="parentNode.status==0">未连接</span>
          </td>
        </tr>
        <tr>
          <td class="ys-info-color">状态更新:</td>
          <td>
            <span>{{parentNode.last_heartbeat}}</span>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
  import Api from 'src/lib/api'
  import adminPassword from 'src/components/admin-password.vue'
  export default {
    name: "node-state-parent",
    data(){
      return {
        parentNode: {
          ip: '',
          type: '',
          version: '',
          status: 0,
          last_heartbeat: ''
        },
        adminPassword: ''
      }
    },
    ready: function () {
      this.getParentSettings()
    },
    methods: {
      getParentSettings(){
        this.$http.get('/api/system/nodes?type=parent').then(function (response) {
          if (response.data.status == 200) {
            this.parentNode = response.data.data.parent;
          } else {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      }
    },
    components: {
    }
  }
</script>
