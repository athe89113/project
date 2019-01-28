<template>
  <div class="ys-con pos-r" v-if="loadTable">
    <div class="ys-box-title">
      显示最新10条数据，共{{Precount}}条数据
      [最新更新时间：{{newestTime}}]
    </div>
    <div class="ys-box-con rule-run-result-box m-t-10">
      <div class="custom-table data-preview" style="width:100%;height:480px;" id="rule-run-result-table">
        <table class="ys-table">
          <thead>
            <tr>
              <th v-if="PreresultHeader.length==0"></th>
              <th v-for="head in PreresultHeader">{{head}}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in PreresultData">         
              <td v-for="col in row" track-by="$index" class="text-l operate" nowrap="nowrap">{{col}}</td>
            </tr>
          </tbody>
        </table>
        <table-data v-if="loadTable" :url='PretableUrl'
        :data.sync="PreresultData"
        :whole.sync="PretableTotal"
        :filter.sync="PretableFilter"
        :search.sync="PresearchValue"
        v-ref:table>
        </table-data>
      </div>
    </div>
  </div>
</template>
<style scoped>
.ys-table tr th.text-l,.ys-table tr td.text-l{
  text-align: left;
}
.ys-table tr th.operate{
  border-left: 2px solid rgba(255,255,255,0.05);
}
</style>
<script>
require('src/assets/js/jquery.nicescroll.js');
export default {
  name: "data-preview",
  data () {
    return {
      PretableUrl: '/api/ssa/file_manage/preview/dts',
      PretableFilter: {
        "path": {id: "", name: ""}
      },
      PretableTotal:10,
      newestTime:'',
      Precount: '',
      PresearchValue:'',
      loadTable:false,
      PreresultData: [],
      PreresultHeader: []
    }
  },
  ready () {  
      if(Object.keys(this.$route.query).length==0) return false
      let path = this.$route.query.path;
      let index = path.lastIndexOf('/');
      let filepath = path.substring(0,index)
      this.loadTable = true
      this.newestTime = path.substring(index+1)
      this.PretableFilter= {
        "path": {id: filepath, name: filepath}
      }
      this.getData (filepath) 
  },
  methods:{
    getData (filepath){ 
      this.$http.post('/api/ssa/file_manage/preview/dts', {
        "path": filepath,
        "start": 0,
        "length":10
      }).then(function (response) {
        let res = response.data;
        if (res.status == 200) {
          this.Precount = res.recordsTotal 
          this.PreresultHeader = res.headers
          this.$root.alertSuccess = true;
          this.$root.errorMsg = response.data.msg
          setTimeout(function(){
            $("#rule-run-result-table").niceScroll({
              cursorborder: "1px solid rgba(0,0,0,0)",
              autohidemode:false,
              cursorwidth: "7px",
              cursorcolor:"rgba(74,146,255,0.3)"
            });
          },2000)
        } else {
          this.$root.alertError = true;
          this.$root.errorMsg = response.data.msg
        }
      })
    }
  }
}
</script>