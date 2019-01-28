<template>
  <div class="ys-box-con ys-wrap">
    <p class="ys-info-color">强制启用二次验证的权限组:
    <span v-for="list in tableList">
      <span v-bind:class="['管理员' === list.name ? 'disabled' : '' ]">
      <checkbox :show.sync="list.status" :text="list.name"></checkbox>&nbsp;
      </span>
    </span>
    </p>
    <section class="m-t-20">
      <admin-password :admin-password.sync="adminPassword"></admin-password>
    </section>
    <div class="m-t-20">
      <button class="ys-btn m-r-10" @click="saveSettings()">保存</button>
    </div>
  </div>
</template>
<script>
  import adminPassword from 'src/components/admin-password.vue'
  export default {
    name: 'two-validation',
    data () {
      return {
        tableList: [
        ]
      }
    },
    ready: function () {
      this.getinfo ()
    },
    methods: {
      getinfo () {
        this.$http.get('/api/system/two_validation').then(function (response) {
          if (response.data.status === 200) {
            this.tableList = response.data.data;
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      saveSettings () {
        let data = {
          'admin_password': this.adminPassword,
          'tablelist': this.tableList
        };
        this.$http.put('/api/system/two_validation', data).then(function (response) {
          if (response.data.status === 200) {
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      }
    },
    components: {
      adminPassword
    }
  }
</script>
