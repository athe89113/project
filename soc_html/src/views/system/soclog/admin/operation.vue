<template>
  <div class="ys-box">
    <div class="ys-box-con">
      <div class="tool-box">
        <div class="fLeft d-i-b">
          下载前&nbsp;<input type="text" placeholder=""
                   v-model="download_numbers"
                   class="ys-input" style="width:50px;"/>&nbsp;条日志&nbsp;&nbsp;
          <a @click="downloadFile()">
            <i class="md md-file-download m-r-3 icon-vert font14"></i>下载</a>
        </div>
        <div class="fRight d-i-b">
          <div class="ys-search d-i-b m-l-10">
            <input type="text" placeholder="输入关键词查询"
                   v-model="searchValue"
                   @blur="tableRe()"
                   @keyup.enter="tableRe()"
                   class="ys-input" style="width:180px;"/>
            <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
          </div>
        </div>
      </div>
      <table class="ys-table m-t-10 detail-table">
        <thead>
        <tr>
          <th>用户名</th>
          <th>操作时间</th>
          <th>操作IP</th>
          <th>操作地点</th>
          <th>操作内容</th>
        </tr>
        </thead>
        <tbody v-for="list in tableList">
        <tr class="odd">
          <td>{{list.username}}</td>
          <td>{{list.datetime}}</td>
          <td>{{list.ip}}</td>
          <td>{{list.address}}</td>
          <td>{{list.info}}</td>
        </tr>

        </tbody>
      </table>
      <table-data :url='tableUrl'
                  :data.sync="tableList"
                  :filter.sync="tableFilter"
                  :search.sync="searchValue"
                  v-ref:table></table-data>
    </div>
  </div>
</template>
<style scoped>

</style>
<script>
  export default {
    name: 'admin-operation',
    data () {
      return {
        tableUrl: '/api/system/soclog/dts',
        tableList: '',
        tableFilter: {
          log_type: {'id': '1'},
          user_type: {'id': '2'}
        },
        filterLocations: [],
        filterIspLines: [],
        searchValue: '',
        download_numbers: 100,
      }
    },
    ready: function () {

    },
    methods: {
      downloadFile(){
        if(this.download_numbers<10 || this.download_numbers >10000){
            this.$root.alertError = true;
            this.$root.errorMsg = '下载数量介于10-10000'
        }else{
          this.$refs.table.Download(this.download_numbers)
        }
      },
      tableRe () {
        this.$refs.table.Re()
      },
    },
    components: {}
  }
</script>
