<template>
  <div>
    <div class="rule-manage-box-left">
      <div class="ys-box">
        <div class="ys-box-title">
          <ul class="file-edit-box">
            <li @click="addFolder()">
              <tooltip :content="'添加目录'" :delay="0" class="m-l-20">
                <span class="ys-info-color" ><i class="ys-icon icon-folder"></i></span>
              </tooltip>
            </li>
            <tooltip :content="'添加文件'" :delay="0" class="m-l-20">
              <span class="ys-info-color" @click="addFile()"><i class="ys-icon icon-file-single"></i></span>
            </tooltip>
            <tooltip :content="'删除'" :delay="0" class="m-l-20">
              <span class="ys-info-color" @click="deleteItem()"><i class="ys-icon icon-trash"></i></span>
            </tooltip>
            <tooltip :content="'重命名'" :delay="0" class="m-l-20">
              <span class="ys-info-color" @click="renameItem()"><i class="ys-icon icon-edit"></i></span>
            </tooltip>
          </ul>
        </div>
        <div class="ys-box-con rule-file-box" style="padding: 0;">
          <div v-for="folder in ruleTree" :key="folder.id" >
            <div class="file-item text-cursor" v-bind:class="[folder.id==selItem.id ? 'sel-item' : '']">
              <div class="m-l-15" @click="selItemBtn(folder)">
                <i class="ys-icon displayIco ys-primary-color" 
                  @click="folder.show = !folder.show"
                  v-bind:class="[folder.show==1 ? 'icon-minus-box' : 'icon-plus-box']"></i>
                  <i class="ys-icon icon-folder m-l-5 ys-info-color m-r-5"></i>
                  
                  <span v-if="folder.edit == 1">
                    <input v-model="folder.name" class="ys-input" style="width: 100px">
                    <i class="ys-icon icon-ok m-r-5 text-cursor ys-success-color" @click="saveEdit(folder)"></i>
                    <i class="ys-icon icon-quit text-cursor ys-error-color" @click="quitEdit(ruleTree, $index, folder)"></i>
                  </span>
                  <span v-else>{{folder.name}}</span>
              </div>
            </div>
            <div v-for="file in folder.data" :key="file.id" 
             @click="selItemBtn(file)"
              v-bind:class="[file.id==selItem.id ? 'sel-item' : '']"
              v-show="folder.show" class="file-item text-cursor">
              <div style="margin-left:55px;">
                <i class="ys-icon icon-file-single ys-info-color"></i>
                <!-- <span class="">{{file.name}}</span> -->
                <span v-if="file.edit == 1">
                  <input v-model="file.name" class="ys-input" style="width: 100px">
                  <i class="glyphicon glyphicon-ok m-r-5 text-cursor" @click="saveEdit(file)"></i>
                  <i class="glyphicon glyphicon-remove text-cursor" @click="quitEdit(folder.data, $index, file)"></i>
                </span>
                <span v-else>{{file.name}}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="rule-manage-box-right">
        <textarea v-model="selItem.sql" class="ys-input" style="width: 100%; height: 200px">
        </textarea>
        <div class="m-t-15">
          <button class="ys-btn ys-btn-blue" @click="executeSql()">运行</button>
          <button class="ys-btn m-l-10" @click="saveEdit(selItem)">保存规则</button>
        </div>
        <div class="ys-box m-t-15">
          <div class="ys-box-title">运行结果</div>
          <div class="ys-box-con rule-run-result-box">
            <div class="custom-table" style="width:100%;height:480px;" id="rule-run-result-table">
              <table class="ys-table" style="table-layout:fixed;">
                <thead>
                  <tr>
                    <th v-for="head in resultHeader" class="text-over p-l-5 p-r-5" style="width:300px;">{{head}}</th>
                    <th class="gutter"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in resultData">
                    <td v-for="head in resultHeader" nowrap="nowrap" class="text-over p-l-5 p-r-5" style="width:300px;">{{showField(row, head)}}</td>
                  </tr>
                </tbody>
              </table>
              <table-data :url='tableUrl'
                      :filter.sync="tableFilter"
                      :data.sync="tableList"
                      :search.sync="searchValue"
                      v-ref:table></table-data>
          </div>
          </div>
        </div>
    </div>
  </div>
</template>

<style scoped>
.rule-manage-box-left{
  float: left; 
  width: 200px;
}
.rule-manage-box-right{
  margin-left:210px;
}
.file-item {
  height: 30px;
  line-height: 30px;
}
.sel-item {
  background:rgba(0,0,0,0.45);
}
.file-edit-box {
  display: table-cell;
}
.file-edit-box li {
  display: inline-block;
}
</style>

<script>
  require('src/assets/js/jquery.nicescroll.js');
  import Api from 'src/lib/api'
  export default {
    name: "rule-manage",
    data() {
      return {
        ruleTree: [],
        selItem: {id: 0, type: 1, parent_id: 0},
        oldName: "",
        resultData: [],
        resultHeader: [],
        tableUrl: "/api/ssa/rule_manage/execute/dts",
        tableList:"",
        tableFilter: {
          sql:{id:""}
        },
      }
    },
    ready: function () {
      let height=window.screen.height-80-170;
      $(".rule-file-box").css({"height":height+"px"});
      this.getRuleTree();
    },
    methods: {
      showField(data, key) {
        return data[key]
      },
      selItemBtn(obj) {
        if(obj.id == this.selItem.id){
          this.selItem = {id: 0, type: 1, parent_id: 0}
        }else{
          this.selItem = obj
        }
      },
      getRuleTree () {
        this.$http.get('/api/ssa/rule_manage').then(function (response) {
          this.ruleTree = response.data.data;
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      addFolder() {
        this.ruleTree.push({
          id: 0,
          edit: 1,
          parent_id: 0,
          name: "",
          type: 1,
          data: []
        })
      },
      addFile(){
        if (this.selItem.id == 0){
          this.$root.alertError = true;
          this.$root.errorMsg = "请选择文件夹"
          return
        }
        this.selItem.show = 1
        if (this.selItem.type == 1){
          this.selItem.data.push({
            id: 0,
            edit: 1,
            parent_id: this.selItem.id,
            name: "",
            type: 2
          })
        }else{
          this.ruleTree.forEach(e => {
            if (e.id == this.selItem.parent_id){
              e.data.push({
                id: 0,
                edit: 1,
                parent_id: this.selItem.parent_id,
                name: "",
                type: 2
              }
              )
            }
          });
        }
      },
      renameItem(){
        this.selItem.edit = 1
        this.oldName =this.selItem.name
      },
      quitEdit(obj, index, item){
        if (item.id == 0){
          obj.splice(index, 1)
        }else{
          item.edit = 0
          item.name = this.oldName
        }
      },
      saveEdit(item){
        // 编辑
        if (item.id > 0){
          this.$http.put('/api/ssa/rule_manage/' + item.id, item).then(function (response) {
            if (response.data.status == 200) {
              item.edit = 0
              this.$root.alertSuccess = true;
              this.$root.errorMsg = response.data.msg
            } else {
              this.$root.alertError = true;
              this.$root.errorMsg = response.data.msg
            }
          }, function (response) {
            Api.user.requestFalse(response, this);
          })
        }
        // 新建
        else{
          this.$http.post('/api/ssa/rule_manage', item).then(function (response) {
            if (response.data.status == 200) {
              if(item.type == 1){
                item.edit = 0
                item.id = response.data.data.id
              }else{
                item.edit = 0
                item.id = response.data.data.id
                this.$root.alertSuccess = true;
                this.$root.errorMsg = response.data.msg
              }
            } else {
              this.$root.alertError = true;
              this.$root.errorMsg = response.data.msg
            }
          }, function (response) {
            Api.user.requestFalse(response, this);
          })
        }
        
      },
      deleteItem(){
        if(this.selItem.id == 0){
          return 
        }
        this.$http.delete('/api/ssa/rule_manage/'+ this.selItem.id).then(function (response) {
          if (response.data.status == 200) {
            this.getRuleTree()
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      executeSql(){
        if (!this.selItem.sql){
          return
        }
        this.tableRe();
      },
      tableRe(){
        this.tableFilter.sql.id=this.selItem.sql;
        this.$refs.table.Re();
        $("#rule-run-result-table").niceScroll({
          cursorborder: "1px solid rgba(0,0,0,0)",
          autohidemode:false,
          cursorwidth: "7px",
          cursorcolor:"rgba(74,146,255,0.3)"
        });
      },
    },
    watch:{
      'tableList':function(){
        let resultHeader = []
        this.resultData = this.tableList;
        if(this.resultData.length > 0){
          for (var k in this.resultData[0]){
            resultHeader.push(k)
          }
        }
        this.resultHeader = resultHeader
      }
    }
  }
</script>
