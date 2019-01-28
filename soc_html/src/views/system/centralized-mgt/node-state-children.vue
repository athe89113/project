<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <div class="tool-box">
        <div class="fLeft d-i-b">
          <button class="ys-btn" @click="showAddBtn">
            <i class="ys-icon icon-add-circle"></i>添加下级中心
          </button>
        </div>
      </div>
      <table class="ys-table m-t-10 detail-table">
        <thead>
        <tr>
          <th class="textL">名称</th>
          <th>地址</th>
          <th>角色</th>
          <th>版本</th>
          <th>状态</th>
          <th>状态更新</th>
          <th class="textC" style="width: 120px;">操作</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="list in tableList" class="odd" v-bind:class="[curEditId == list.id ? 'on' : '' ]">
          <td class="textL">{{list.name}}</td>
          <td>{{list.ip}}</td>
          <td>
            <span v-if="list.type=='sub_center'">二级中心</span>
            <span v-if="list.type=='child_center'">三级中心</span>
          </td>
          <td>{{list.version}}</td>
          <td>
            <span class="ys-success-color" v-if="list.status==1">已连接</span>
            <span class="ys-error-color" v-else="">未连接</span>
          </td>
          <td>{{list.last_heartbeat}}</td>
          <td class="operate">
            <a @click="refreshChildNode(list)" class="m-r-10">
              <i class="ys-icon icon-update m-r-2" v-bind:class="[list.id==curRefreshId ? 'fa-spin' : '']"></i>
            </a>
            <a @click="showEditBtn(list)" class="m-r-10"><i class="ys-icon icon-edit"></i></a>
            <ys-poptip confirm
                       title="您确认删除此下级中心吗？"
                       :placement="'left'"
                       @on-ok="delChildNode(list)"
                       @on-cancel="">
              <a class="m-r-10">删除</a>
            </ys-poptip>
          </td>
        </tr>
        <tr v-if="tableList.length==0" class="even">
          <td colspan="7" class="textC">查询不到任何相关数据</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
  <aside :show.sync="showAdd"
         :header="'添加下级中心'"
         :left="'auto'"
         :width="'500px'">
    <div>
      <table class="ys-form-table m-t-10">
        <tr>
          <td>下级名称：</td>
          <td>
            <input class="ys-input"
                   placeholder="填写一个名称标识"
                   v-model="childNode.name"/>
          </td>
        </tr>
        <tr>
          <td>级联密钥：</td>
          <td>
            <input class="ys-input"
                   placeholder="级联秘钥"
                   v-model="childNode.auth_key"/>
          </td>
        </tr>
        <tr>
          <td>下级地址：</td>
          <td>
            <input class="ys-input"
                   placeholder="例如 192.168.1.2"
                   v-model="childNode.ip"/>
          </td>
        </tr>
      </table>
    </div>
    <div>
      <admin-password :admin-password.sync="adminPassword"></admin-password>
    </div>
    <div class="aside-foot m-t-20">
      <button class="ys-btn m-r-10" @click="createChildNode">确定</button>
      <button class="ys-btn ys-btn-white" @click="quitAdd()">取消</button>
    </div>
  </aside>
  <aside :show.sync="showEdit"
         :header="'修改下级中心'"
         :left="'auto'"
         :width="'500px'">
    <div>
      <table class="ys-form-table m-t-10">
        <tr>
          <td>下级名称：</td>
          <td>
            <input class="ys-input"
                   placeholder="填写一个名称标识"
                   v-model="curEditNode.name"/>
          </td>
        </tr>
        <tr>
          <td>下级角色：</td>
          <td>
            <span v-if="curEditNode.type=='sub_center'">二级中心</span>
            <span v-if="curEditNode.type=='child_center'">三级中心</span>
          </td>
        </tr>
        <tr>
          <td>级联密钥：</td>
          <td>{{curEditNode.auth_key}}
          </td>
        </tr>
        <tr>
          <td>下级地址：</td>
          <td>{{curEditNode.ip}}
          </td>
        </tr>
      </table>
    </div>
    <div>
      <admin-password :admin-password.sync="adminPassword"></admin-password>
    </div>
    <div class="aside-foot m-t-20">
      <button class="ys-btn m-r-10" @click="editChildNode">确定</button>
      <button class="ys-btn ys-btn-white" @click="quitAdd()">取消</button>
    </div>
  </aside>
</template>

<script>
  import Api from 'src/lib/api'
  import adminPassword from 'src/components/admin-password.vue'
  export default {
    name: "node-state-children",
    data(){
      return {
        showAdd: false,
        showEdit: false,
        curEditNode: {},
        tableUrl: "",
        tableList: [],
        childNode: {
          ip: '',
          name: '',
          role: 'child',
          type: '',
          auth_key: ''
        },
        typeList: [
          {id: 'sub_center', text: "二级中心"},
          {id: 'child_center', text: "三级中心"}
        ],
        curRefreshId: '',
      }
    },
    ready: function () {
      this.getChildrenNodes()
    },
    methods: {
      showAddBtn(){
        this.showAdd = !this.showAdd
      },
      quitAdd(){
        this.showAdd = false
        this.showEdit = false
        this.curEditNode = {}
        this.childNode = {
          ip: '',
          name: '',
          role: 'child',
          type: '',
          auth_key: ''
        }
      },
      tableRe(){
        this.getChildrenNodes()
      },
      // 删除
      delChildNode(list){
        this.$http.delete('/api/system/nodes/' + list.id).then(function (response) {
          if (response.data.status == 200) {
            this.tableRe()
          } else {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      // 刷新
      refreshChildNode(list){
        this.curRefreshId = list.id
        this.$http.post('/api/system/nodes/' + list.id + '/refresh').then(function (response) {
          if (response.data.status == 200) {
            list.status = response.data.data.status
          } else {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
          this.tableRe()
          this.curRefreshId = ''
        }, function (response) {
          this.curRefreshId = ''
          Api.user.requestFalse(response, this);
        })
      },
      // 创建
      createChildNode(){
        this.childNode.admin_password = this.adminPassword
        this.$http.post('/api/system/nodes', this.childNode).then(function (response) {
          if (response.data.status == 200) {
            this.showAdd = false;
            this.tableRe()
          } else {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      showEditBtn(list){
        this.showEdit = !this.showEdit
        this.curEditNode = list
        //this.curEditNode.auth_key = ''
      },
      editChildNode(){
        this.curEditNode.admin_password = this.adminPassword
        this.$http.put('/api/system/nodes/' + this.curEditNode.id, this.curEditNode).then(function (response) {
          if (response.data.status == 200) {
            this.quitAdd()
            this.tableRe()
          } else {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      getChildrenNodes(){
        this.$http.get('/api/system/nodes').then(function (response) {
          if (response.data.status == 200) {
            this.tableList = response.data.data.children
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
      "admin-password": adminPassword
    }
  }
</script>
