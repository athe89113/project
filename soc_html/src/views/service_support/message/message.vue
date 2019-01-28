<template>
  <div class="btn-group m-b-20 hidden">
    <button @click="filterStatus(2)" type="button" v-bind:class="[isRead=='2' ? 'btn-primary' : 'btn-white' ]" class="btn waves-effect btn-40">全部</button>
    <button @click="filterStatus(1)" type="button" v-bind:class="[isRead=='1' ? 'btn-primary' : 'btn-white' ]" class="btn waves-effect btn-40">已读</button>
    <button @click="filterStatus(0)" type="button" v-bind:class="[isRead=='0' ? 'btn-primary' : 'btn-white' ]" class="btn waves-effect btn-40">未读<span v-show="unRead != 0" class=" font-600">({{ unRead }})</span></button>
  </div>
  <div class="tool-box">
    <div class="fLeft d-i-b">
      <button class="ys-btn" @click="readSelected">标记已读</button>
    </div>
    <div class="fRight d-i-b">
      <div class="d-i-b"></div>
      <span>筛选类型</span>
      <ys-select :option="filterMsgTypes"
                 :width="150" :selected.sync="tableFilter.is_read" @change="tableRe()"></ys-select>
      <div class="ys-search d-i-b m-l-10">
        <input type="text" placeholder="输入关键词查询"
               v-model="searchValue"
               @keyup.enter="tableRe"
               class="ys-input" style="width:180px;"/>
        <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
      </div>
    </div>
  </div>
  <table class="ys-table m-t-10">
    <thead>
    <tr>
      <th><checkbox :show.sync="allSelected"></checkbox></th>
      <th></th>
      <th>标题</th>
      <th>提交时间</th>
      <th>类型</th>
    </tr>
    </thead>
    <tbody>
    <tr v-bind:class="[$index%2==1 ? 'even' : 'odd' ]" v-for="list in tableList">
      <td><checkbox :show.sync="list.selected"></checkbox></td>
      <td><i v-if="list.is_read == 0" class="fa fa-circle text-primary" style="font-size: 1.5em"></i></td>
      <td>
        <a @click="showRead(list.id)">{{list.title}}</a>
      </td>
      <td>{{list.create_time}}</td>
      <td>
        <span v-if="list.type == 0">其他消息</span>
        <span v-if="list.type == 1">安全扫描</span>
        <span v-if="list.type == 2">监控告警</span>
      </td>
    </tr>
    </tbody>
  </table>
  <table-data :url='tableUrl' :data.sync="tableList" :filter.sync="tableFilter" :search.sync="searchValue" v-ref:table></table-data>
  <aside :show.sync="configStatus"
         :header="'查看消息'"
         :left="'auto'"
         :width="'400px'">
    <div class="ys-box">
      <div class="ys-box-title">{{ curMessage.title }}</div>
      <div class="ys-box-con">
        {{curMessage.content}}
      </div>
    </div>
    <div class="aside-foot m-t-20">
      <button class="ys-btn m-r-10" @click="configStatus=false">确定</button>
      <button class="ys-btn ys-btn-white" @click="configStatus=false">关闭</button>
    </div>
  </aside>
  </div>
</template>

<style>
  .btn-40 {
    height: 40px;
    min-width: 70px;
  }
</style>

<script>
  import tableData from 'src/components/table-data.vue'
  import tableOpt from 'src/components/table-opt.vue'
  import ysSelect from 'src/components/select.vue'
  import aside from 'src/components/Aside.vue'
  export default {
    props: {
      messageType: {
        type: String,
        default: "other"
      }
    },
    data: function () {
      var messageTypeMap = {
          other: 0,
          security : 1,
          monitor: 2,
          assets: 3,
          all: null
        }
      var typeId = messageTypeMap[this.messageType]
      return {
        tableUrl: '/api/message/dts',
        tableList: [],
        tableFilter: {
          type: {name: '', id: typeId},
          is_read: {name: '全部消息', id: 2},
        },
        typeId: typeId,
        searchValue: '',
        filterMsgTypes: [
          {name: '全部消息', id: 2},
          {name: '未读消息', id: 0},
          {name: '已读消息', id: 1},
        ],
        isRead: 2,
        unRead: 0,
        selectIds: [],
        configStatus:false,
        curMessage:"",
      }
    },
    computed: {
      msgType: {
        get: function () {
          return this.messageTypeMap[this.messageType]
        }
      },
      allSelected:{
        get: function () {
          if(this.tableList.length==0){
            return false
          }
          return this.tableList.reduce(function(prev, curr) {
            return prev && curr.selected;
          },true);
        },
        set: function (newValue) {
          this.tableList.forEach(function(list){
            list.selected = newValue;
          });
        }
      }
    },
    ready: function () {
      this.getUnRead()
    },
    methods:{
      showRead(id){
        this.configStatus=true
        this.getCurMessage(id)
      },
      getCurMessage(id){
        this.$http('/api/message/' + id).then(function (response) {
          if(response.status == 200){
            this.curMessage = response.data.data
          }
        })
      },
      tableRe(){
        this.$refs.table.Re()
      },
      readSelected(){
        var ids = []
        this.tableList.forEach(function(list){
          if (list.selected) {
            ids.push(list.id)
          }
        })
        var data = {"ids": ids}
        this.$http.put("/api/message", data).then(function (response) {
          this.tableRe()
          if(response.status==200){
            this.$root.alertSuccess=true
            this.$root.errorMsg=response.data.msg
          }
        })

      },
      getUnRead(){
        this.$http.get({"url": "/api/message", "timeout": 3000}).then(function (response) {
          if(response.status == 200){
              if(this.messageType == 'all'){
                this.unRead = response.data.data['count']
              }else{
                this.unRead = response.data.data[this.messageType]
              }
          }
        })
      }
    },
    components: {
      ysSelect,
      tableOpt,
      tableData,
      aside
    },
  }
</script>