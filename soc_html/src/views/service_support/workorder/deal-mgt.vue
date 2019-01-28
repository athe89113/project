<template>
  <div class="ys-box">
    <div class="ys-box-con">
      <div class="tool-box">
        <div class="fRight d-i-b">
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
          <th>标题</th>
          <th>申请人</th>
          <th>处理人</th>
          <th>状态</th>
          <th>回复</th>
          <th>提交时间</th>
        </tr>
        </thead>
        <tbody>
        <tr v-bind:class="[$index%2==1 ? 'even' : 'odd' ]" v-for="list in tableList">
          <td>
            <a @click="showInfo(list.id)">{{list.title}}</a>
          </td>
          <td>{{list.applier}}</td>
          <td>{{list.handler}}</td>
          <td v-if="list.status=='未处理'" class="ys-error-color">{{list.status}}</td>
          <td v-if="list.status=='已经处理'" class="ys-success-color">已处理</td>
          <td v-if="list.status=='正在处理'">正在处理</td>
          <td>{{list.is_replied}}</td>
          <td>{{list.create_time}}</td>
        </tr>
        </tbody>
      </table>
      <table-data :url='tableUrl'
                  :data.sync="tableList"
                  :filter.sync="tableFilter"
                  :search.sync="searchValue"
                  v-ref:table></table-data>
    </div>
    <aside :show.sync="infoStatus"
           :header="'工单详情'"
           :left="'auto'"
           :width="'800px'">
      <deal-info :order_id="orderInfoId" :target="'deal'"></deal-info>
    </aside>
  </div>
</template>
<script>
  import tableData from 'src/components/table-data.vue'
  import tableOpt from 'src/components/table-opt.vue'
  import aside from 'src/components/Aside.vue'
  import dealInfo from './deal-info-mgt.vue'
  export default {
    data() {
      return {
        tableUrl: '/api/ticket_handle/dts',
        tableList: [],
        tableFliter: {},
        searchValue: '',
        showRight:false,
        tagList:{
          "applicant": {
            canDelete: true,
            text: "申请人:",
            value: "",
            display: false
          },
          "manage": {
            canDelete: true,
            text: "处理人:",
            value: "",
            display: false
          },
          "status": {
            canDelete: true,
            text: "状态:",
            value: "",
            display: false
          },
          "startTime": {
            canDelete: true,
            text: "时间:",
            value: "",
            display: false
          },
          "endTime": {
            canDelete: true,
            text: "时间:",
            value: "",
            display: false
          },
        },

        //
        infoStatus:false,
        orderInfoId:"",
      }
    },
    ready: function() {
    },
    methods:{
      tableRe(){
        this.$refs.table.Re()
      },
      showInfo(id){
        this.infoStatus=true;
        this.orderInfoId=id;
      },
    },
    components: {
      tableOpt,
      tableData,
      aside,
      dealInfo
    }
  }
</script>
