<template>
  <div class="ys-box-con ys-wrap">
    <div class="tool-box">
      <div class="fLeft d-i-b">
        <button class="ys-btn" @click="showAdd()"><i class="ys-icon icon-add-circle"></i>添加IP</button>
      </div>
      <div class="fRight d-i-b">
        <div class="ys-search d-i-b m-l-10">
          <input type="text" placeholder="输入关键词查询"
                 v-model="searchValue"
                 @keyup.enter="tableRe()"
                 class="ys-input" style="width:180px;"/>
          <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
        </div>
      </div>
    </div>
      <table class="ys-table m-t-10 detail-table">
        <thead>
        <tr>
          <th>IP</th>
          <th>开始时间</th>
          <th>结束时间</th>
          <th>操作</th>
        </tr>
        </thead>
        <tbody v-for="list in tableList">
        <tr class="odd">
          <td>{{list.ip}}</td>
          <td>{{list.starttime}}</td>
          <td>{{list.endtime}}</td>
          <td>
            <ys-poptip confirm
                       title="您确认删除此IP吗？"
                       :placement="'left'"
                       @on-ok="del(list.id)"
                       @on-cancel="">
              <a><i class="fa fa-trash m-r-2"></i>删除</a>
            </ys-poptip>
          </td>
        </tr>

        </tbody>
      </table>
      <table-data :url='tableUrl'
                  :data.sync="tableList"
                  :filter.sync="tableFilter"
                  :search.sync="searchValue"
                  v-ref:table></table-data>
        <aside :show.sync="configStatus"
           :header="configHead"
           :left="'auto'"
           :width="'500px'">
      <div>
        <validator name="valCompany" @valid="onValid = true" @invalid="onValid = false">

            <div class="ys-box">
              <div class="ys-box-title">添加IP到白名单</div>
              <div class="ys-box-con">
                <table class="ys-set-table">
                  <tbody>
                  <tr>
                    <td>IP</td>
                    <td>
                      <input class="ys-input"
                             v-model="addip"
                             style="width: 218px"
                             >
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
              <section class="m-t-20">
                <admin-password :admin-password.sync="adminPassword"></admin-password>
              </section>
            <div class="aside-foot m-t-20">
              <button class="ys-btn m-r-10" @click="add()">确定</button>
              <button class="ys-btn ys-btn-white" @click="configStatus=false">取消</button>
            </div>

        </validator>
      </div>
    </aside>

  </div>
</template>
<script>
  import adminPassword from 'src/components/admin-password.vue'
  export default {
    name: 'white-list',
    data () {
      return {
        tableUrl: '/api/system/system_safe/dts',
        tableList: '',
        tableFilter: {
          is_black: {'id': '2'},
        },
        Status: '成功',
        filterLocations: [],
        filterIspLines: [],
        searchValue: '',
        addip: '',
        configStatus: false,
      }
    },
    ready: function () {
    },
    methods: {
      tableRe () {
        this.$refs.table.Re()
      },
      del (id) {
        this.$http.delete('/api/system/system_safe', {'id': id}).then(function (response) {
          if (response.data.status === 200) {
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }this.tableRe()
        })
      },
      add () {
        this.$http.post('/api/system/system_safe', {'ip': this.addip, 'is_black': 2, 'admin_password': this.adminPassword}).then(function (response) {
          if (response.data.status === 200) {
            this.$root.alertSuccess = true;
            this.$root.errorMsg = response.data.msg
            this.configStatus = false
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
          this.tableRe()
        })
      },
      showAdd () {
        this.configStatus = true;
      },
    },
    components: {
      adminPassword
    }
  }
</script>
