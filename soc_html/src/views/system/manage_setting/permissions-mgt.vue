<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <div class="tool-box">
        <div class="fLeft d-i-b">
          <button class="ys-btn" @click="showAddBtn">
            <i class="ys-icon icon-add-circle"></i>添加角色
          </button>
        </div>
      </div>
      <table class="ys-table m-t-10 detail-table">
        <thead>
        <tr>
          <th class="textL">角色名称</th>
          <th>用户数</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
        </thead>
        <tbody v-for="list in tableList" >
        <tr class="odd" v-bind:class="[curEditId == list.id ? 'on' : '' ]">
          <td class="textL">
            <span class="m-r-5">{{list.name}}</span>
            <i class="ys-icon icon-user m-r-5 ys-warn-color" v-if="list.is_admin==1"></i>
          </td>
          <td>{{list.users}}</td>
          <td>
            <span class="ys-success-color" v-if="list.enable==1"><i class="ys-icon icon-check-circle m-r-5"></i>启用</span>
            <span class="ys-error-color" v-else><i class="ys-icon icon-clear-circle m-r-5"></i>关闭</span>
          </td>
          <td class="operate" v-else="" :class="{'disabled': list.is_admin}">
            <tooltip :content="'编辑'" :delay="1000">
              <a @click="edit(list)"><i class="ys-icon icon-edit"></i></a>
            </tooltip>
            <a v-if="list.users>0" class="ys-error-color disabled"><i class="ys-icon icon-trash"></i></a>
            <ys-poptip confirm  v-else=""
                       title="您确认删除此角色吗？"
                       :placement="'left'"
                       @on-ok="delPer(list.id)"
                       @on-cancel="">
              <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
            </ys-poptip>
          </td>
        </tr>
        </tbody>
      </table>
      <table-data :url='tableUrl'
                  :data.sync="tableList"
                  v-ref:table>
      </table-data>
    </div>
  </div>
  <aside :show.sync="showConfigStatus"
         :header="configHead"
         :left="'auto'"
         :width="'800px'">
    <validator name="valCluster" @valid="onConfigValid = true" @invalid="onConfigValid = false">
      <div>
        <table class="ys-form-table">
          <tr>
            <td>名称</td>
            <td>
              <ys-valid>
                <input class="ys-input"
                       placeholder="名称"
                       v-model="editFrom.name"/>
              </ys-valid>
            </td>
          </tr>
          <tr>
            <td>组别状态</td>
            <td>
              <radio :list="radioData" :value.sync="editFrom.enable"></radio>
            </td>
          </tr>
          <tr>
            <td style="vertical-align: top;">角色权限</td>
            <td>
              <div style="margin-top:-10px;">
                <tree :options="permissions" @edit="editPer"></tree>
              </div>
            </td>
          </tr>
        </table>
        <admin-password :admin-password.sync="editFrom.admin_password"></admin-password>
      </div>
      <div class="aside-foot m-t-20">
        <button class="ys-btn m-r-10" @click="saveEditPer">确定</button>
        <button class="ys-btn ys-btn-white" @click="quit()">取消</button>
      </div>
    </validator>

  </aside>
  <aside :show.sync="showAdd"
         :header="'添加角色'"
         :left="'auto'"
         :width="'800px'">
    <div>
      <table class="ys-form-table">
        <tr>
          <td>角色名称</td>
          <td>
            <ys-valid>
              <input class="ys-input"
                     placeholder="名称"
                     v-model="addFrom.name"/>
            </ys-valid>
          </td>
        </tr>
        <tr>
          <td>角色状态</td>
          <td>
            <radio :list="radioData" :value.sync="addFrom.enable"></radio>
          </td>
        </tr>
        <tr>
          <td style="vertical-align: top;">角色权限</td>
          <td>
            <div style="margin-top:-10px;">
              <tree :options="permissions" @edit="editPer"></tree>
            </div>
          </td>
        </tr>
      </table>
      <admin-password :admin-password.sync="addFrom.admin_password"></admin-password>
    </div>
    <div class="aside-foot m-t-20">
      <button class="ys-btn m-r-10" @click="createRole">确定</button>
      <button class="ys-btn ys-btn-white" @click="quitAdd()">取消</button>
    </div>

  </aside>
</template>
<style scoped>

</style>
<script>
  import Api from 'src/lib/api'
  import tree from './tree.vue'
  export default {
    name: "permissions-mgt",
    data() {
      return {
        showAdd: false,
        tableUrl: "/api/role/dts",
        tableList:"",
        tableFilter: {
          location_id: {"id": "", "name": "全部位置" },
          isp_line: {"id": "", "name": "全部线路" }
        },
        filterLocations: [],
        filterIspLines: [],
        searchValue: "",
        showConfigStatus:false,
        configHead:"编辑权限组",

        curEditId:0,
        curDetailId:0,

        radioData:[
          {id:1,text:"启用"},
          {id:0,text:"关闭"}
        ],
        curStep:1,

        permissions: [],
        editPermissions: {},
        editFrom: {
          name: "",
          enable: 1,
          admin_password: ''
        },
        addFrom: {
          name: "",
          enable: 1,
          admin_password: ''
        }

      }
    },
    ready: function() {
      this.fetchPermissions(1)
    },
    methods:{
      quit(){
        this.showConfigStatus=false
        this.curEditId=""
      },
      showAddBtn(){
        this.addFrom = {
          name: "",
          enable: 1,
          admin_password: ''
        }
        this.editPermissions = {}
        this.permissions  = []
        this.showAdd=!this.showAdd
        this.curEditId=""
        this.$http.get('/api/permission').then(function (response) {
          this.permissions = response.data.data
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      quitAdd(){
        this.showAdd=false
      },
      showMiniLoad(){
        this.loadMini=true
      },
      tableRe(){
        this.$refs.table.Re()
      },
      edit(list){
        this.editFrom.name=list.name
        this.editFrom.enable=list.enable
        this.curEditId=list.id;//设置当前编辑id
        this.curDetailId="";//把当前展示详情ID置为空
        this.showConfigStatus=true;//弹出右侧滑出界面
        this.fetchPermissions(list.id)
      },
      showDetail(id){
        this.curEditId="";//设置当前编辑ID为空
        //如果curEditId和此条id相同,就关闭,否则就展示详情
        if(this.curDetailId==id){
          this.curDetailId=""
        }else{
          this.curDetailId=id;
        }
      },
      addIdcSave(){
        this.showConfigStatus=true;
      },
      fetchPermissions(role_id){
        this.$http.get('/api/permission/'+role_id).then(function (response) {
          this.editPermissions = {}
          this.permissions = response.data.data
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      editPer(data){
        this.editPermissions[data.id] = !!data.enable

      },
      saveEditPer(){
        let data = {
          id:this.curEditId,
          name:this.editFrom.name,
          enable:this.editFrom.enable,
          admin_password:this.editFrom.admin_password,
          roles: []
        }
        for (let i in this.editPermissions) {
          data.roles.push(
            {
              id: i,
              enable: this.editPermissions[i]
            }
          )
        }
        this.$http.put('/api/permission/' + this.curEditId, data).then(function (response) {
          this.$root.errorMsg = response.data.msg;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.tableRe()
            this.quit()
          } else {
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })

      },
      delPer(id){
        this.$http.delete('/api/permission/'+id).then(function (response) {
          this.$root.errorMsg = response.data.msg;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.tableRe()
          } else {
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      createRole(){
        let data = {
          roles: [],
          name: this.addFrom.name,
          enable:this.addFrom.enable,
          admin_password:this.addFrom.admin_password
        }
        for (let i in this.editPermissions) {
          data.roles.push(
            {
              id: i,
              enable: this.editPermissions[i]
            }
          )
        }
        this.$http.post('/api/permission', data).then(function (response) {
          this.$root.errorMsg = response.data.msg;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true
            this.quitAdd()
            this.tableRe()
          } else {
            this.$root.alertError = true;
          }

        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      }


    },
    components: {
      tree: tree
    }
  }
</script>
