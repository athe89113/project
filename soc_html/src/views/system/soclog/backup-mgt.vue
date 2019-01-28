<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <div class="tool-box">
        <div class="fLeft d-i-b">
          <button class="ys-btn" @click="createBackupData()">
            <i class="ys-icon icon-add-circle"></i>生成备份
          </button>
        </div>
      </div>
      <table class="ys-table m-t-10 detail-table">
        <thead>
        <tr>
          <th class="textL">备份文件名</th>
          <th>备份状态</th>
          <th>生成日期</th>
          <th class="textC" style="width: 120px;">操作</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="list in tableList" class="odd">
          <td class="textL">{{list.name}}</td>
          <td>
            <span v-if="list.status==0" class="ys-warn-color">正在备份</span>
            <span v-else class="ys-success-color">完成</span>
          </td>
          <td>{{list.backup_time}}</td>
          <td class="operate">
            <a @click="downloadBackup(list)" class="m-r-10"
                   v-bind:class="[list.status==0 ? 'disabled':'']" download><i class="fa fa-eye m-r-2"></i></a>
          </td>
        </tr>
        <tr v-if="tableList.length==0" class="even">
          <td colspan="7" class="textC">查询不到任何相关数据</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
  import Api from 'src/lib/api'
  import adminPassword from 'src/components/admin-password.vue'
  export default {
    name: "backup-mgt",
    data(){
      return {
        curEditId: '',
        tableList: [],
        fetchInterval: ''
      }
    },
    ready: function () {
      let self = this
      self.getBackupData()
      self.fetchInterval = setInterval(function () {
        self.getBackupData()
      }, 15000)
    },
    methods: {
      tableRe(){
        this.getBackupData()
      },
      downloadBackup(list){
        if(list.status==0 || list.download_url==''){
          return
        }
        window.open(list.download_url)
      },
      getBackupData(){
        this.$root.loadStatus = true;
        this.$http.get('/api/system/backup/data').then(function (response) {
          if (response.data.status == 200) {
            this.$root.loadStatus = false
            this.tableList = response.data.data
          } else {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      createBackupData(){
        this.$root.loadStatus = true;
        this.$http.post('/api/system/backup/data').then(function (response) {
          if (response.data.status == 200) {
            this.tableRe()
            this.$root.loadStatus = false
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg;
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      }
    },
    components: {
      "admin-password": adminPassword
    },
    beforeDestroy() {
      clearInterval(this.fetchInterval);
    },
  }
</script>
