<template>
  <div class="ys-con">
    <div class="pageHead" v-if="companyId==''">
      <p class="pageTitle"><span>支持管理 </span>- 用户管理</p>
    </div>
      <div class="m-l-10 m-t-10 m-b-10" v-else="">
        <button class="ys-btn" v-link="{ name: 'company' }">
          <i class="glyphicon glyphicon-circle-arrow-left"></i>
          返回公司列表
        </button>
      </div>
    <div class="tool-box">
      <div class="fLeft d-i-b" v-if="userIsAdmin==1">
        <div v-if="companyId==''">
          <button class="ys-btn" @click="showAdd()"><i class="ys-icon icon-add-circle"></i>添加用户</button>
        </div>
        <div v-else="">
          <button class="ys-btn" @click="showAddUser=!showAddUser"><i class="ys-icon icon-add-circle"></i>添加公司用户</button>
        </div>
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
    <table class="ys-table ys-table-bor m-t-10">
      <thead>
      <tr>
        <th>用户名</th>
        <th>电话</th>
        <th>邮件地址</th>
        <th>最后登录IP</th>
        <th>最后登陆时间</th>
        <th>角色</th>
        <th>状态</th>
        <th style="width:180px;" class="textC">操作</th>
      </tr>
      </thead>
      <tbody>
      <template v-for="list in tableList">
        <tr v-bind:class="[$index%2==1 ? 'even' : 'odd', showId==list.id? 'shown': ''] ">
          <td>{{ list.username }}</a></td>
          <td>{{ list.phone }}</td>
          <td>{{ list.email }}</td>
          <td>{{ list.last_login_ip }}</td>
          <td>{{ list.last_login }}</td>
          <td>{{ list.is_admin }}</td>
          <td>{{ list.lock_status }}</td>
          <td class="textC">
            <a class="m-r-10" v-if="list.is_locked==1" @click="lockUser(list)"><i class="fa fa-unlock m-r-2"></i>解锁</a>
            <a class="m-r-10" v-else @click="lockUser(list)"><i class="fa fa-lock m-r-2"></i>锁定</a>
            <a class="m-r-10" @click="showEdit(list.id)"><i class="fa fa-pencil m-r-2"></i>编辑</a>
            <ys-poptip confirm
                       title="您确认此用户吗？"
                       :placement="'left'"
                       @on-ok="del(list.id)"
                       @on-cancel="">
              <a class="m-r-10"><i class="fa fa-trash m-r-2"></i>删除</a>
            </ys-poptip>
          </td>
        </tr>
      </template>
      </tbody>
    </table>
    <ys-table :url="tableUrl" :data.sync="tableList" :filter.sync="tableFilter" :search.sync="searchValue"
              v-ref:table></ys-table>
    <aside :show.sync="configStatus"
           :header="configHead"
           :left="'auto'"
           :width="'500px'">
      <div>
        <validator name="valCompany" @valid="onValid = true" @invalid="onValid = false">
          <div v-if="!showQRCode">
            <div class="ys-box m-t-10">
              <div class="ys-box-title">填写用户基本信息</div>
              <div class="ys-box-con">
                <table class="ys-set-table">
                  <tbody>
                  <tr>
                    <td>用户名</td>
                    <td v-if="editType==0">
                      <input class="ys-input"
                             v-model="userInfo.username"
                             style="width: 218px"
                             v-validate:username="['required']">
                    </td>
                    <td v-else>{{userInfo.username}}</td>
                  </tr>
                  <tr>
                    <td>用户邮箱</td>
                    <td>
                      <input class="ys-input"
                             v-model="userInfo.email"
                             style="width: 218px"
                             v-validate:user_email="['email', 'required']">
                    </td>
                  </tr>
                  <tr>
                    <td>密码</td>
                    <td>
                      <input type="password"
                             class="ys-input"
                             v-model="userInfo.password"
                             style="width: 218px"
                             v-validate:password="['required']">
                    </td>
                  </tr>
                  <tr>
                    <td>重复密码</td>
                    <td>
                      <input type="password"
                             class="ys-input"
                             v-model="userInfo._password"
                             style="width: 218px"
                             v-validate:_password="['required', '_password']">
                    </td>
                  </tr>
                  <tr>
                    <td>联系电话</td>
                    <td>
                      <input class="ys-input"
                             v-model="userInfo.phone"
                             style="width: 218px"
                             v-validate:user_phone="['numeric', 'required']">
                    </td>
                  </tr>
                  <tr>
                    <td>状态</td>
                    <td>
                      <ys-select
                              :option="lockOptions"
                              @change="userInfo.is_locked = selectedLock.id"
                              :selected.sync="selectedLock"
                              :width="218"></ys-select>
                    </td>
                  </tr>
                  <tr>
                    <td>角色</td>
                    <td>
                      <ys-select
                              :option="roleOptions"
                              @change="userInfo.is_admin = selectedRole.id"
                              :selected.sync="selectedRole"
                              :width="218">
                      </ys-select>
                    </td>
                  </tr>
                  </tbody>
                </table>
                <p class="text-cursor m-t-10" v-if="editType==1" @click="reTwoFactor=!reTwoFactor">
                  <input type="checkbox"
                         class="m-r-3"
                         value="二次验证"
                         v-model="reTwoFactor">重新绑定二次验证</p>
              </div>
            </div>
            <div class="aside-foot m-t-20">
              <button class="ys-btn m-r-10" @click="changeConfig()">确定</button>
              <button class="ys-btn ys-btn-white" @click="configStatus=false">取消</button>
            </div>
          </div>
          <div v-if="showQRCode">
            <div class="ys-box m-t-10" v-if="editType==0">
              <div class="ys-box-title">绑定二次验证</div>
              <div class="ys-box-con">
                <p class="textC">请扫描二次验证码：</p>
                <p class="textC"><img class="m-t-10" :src="QRCodeUrl" style="width:120px;"></p>
                <p class="textC m-t-10">
                  <button class="ys-btn" @click="getQrCode(newUserId)">重新生成</button>
                </p>
              </div>
            </div>
            <div class="ys-box m-t-10" v-if="editType==1 && reTwoFactor">
              <div class="ys-box-title">绑定二次验证</div>
              <div class="ys-box-con">
                <p class="textC">请扫描二次验证码：</p>
                <p class="textC" v-if="QRCodeUrl!='/'"><img class="m-t-10" :src="QRCodeUrl" style="width:120px;"></p>
                <p class="textC m-t-10">
                  <button class="ys-btn" @click="getQrCode(editId)">重新生成</button>
                </p>
              </div>
            </div>
            <div class="aside-foot m-t-20">
              <button class="ys-btn m-r-10" @click="configStatus=false">确定</button>
              <button class="ys-btn ys-btn-white" @click="configStatus=false">关闭</button>
            </div>
          </div>
        </validator>
      </div>

    </aside>
    <aside :show.sync="showAddUser"
           :header="'添加公司用户'"
           :left="'auto'"
           :width="'500px'">
      <user-add-base :company-id="companyId" :show.sync="showAddUser" @added="tableRe"></user-add-base>

    </aside>
  </div>
</template>
<script>
  import Api from  '../../../lib/api'
  import ysTable from 'src/components/table-data.vue'
  import ysSelect from 'src/components/select.vue'
  import ysPoptip from 'src/components/poptip.vue'
  import aside from 'src/components/Aside.vue'
  import userAddBase from "../user/user-add-base.vue"
  export default {
    name: "service-support-user-list",
    props: [
      "companyId"
    ],
    computed: {
      userIsAdmin () {
        return this.$store.state.user.is_admin
      },
    },
    data(){
      return {
        showAddUser: false,
        userIsAdmin: localStorage.getItem('is_admin'),
        tableUrl: '/api/user/dts',
        tableList: "",
        tableFilter: {
          company_id: {id: this.companyId, name: ""},
        },
        searchValue: "",
        delUserId: "",
        //添加
        configStatus:false,
        configHead:"",
        editType:0,
        editId:"",
        userInfo: {
          username: "",
          password: "",
          re_password: "",
          phone: "",
          email: "",
          is_locked: 0,
          is_admin: 0
        },
        roleOptions: [
          {id: 0, name: "普通用户"},
          {id: 1, name: "管理员"}
        ],
        selectedRole: {id: 0, name: "普通用户"},
        lockOptions: [
          {id: 0, name: "正常"},
          {id: 1, name: "锁定"}
        ],
        selectedLock: {id: 0, name: "正常"},
        showQRCode: false,
        QRCodeUrl: "/",
        newUserId:"",
        reTwoFactor: false,
      }
    },
    ready: function () {},
    methods: {
      tableRe(){
        var self = this
        self.$refs.table.Re()
      },
      showAdd(){
        this.configStatus=true;
        this.configHead="添加用户";
        this.editType=0;
        this.userInfo={
          username: "",
          password: "",
          re_password: "",
          phone: "",
          email: "",
          is_locked: 0,
          is_admin: 0
        };
        this.showQRCode=false;
        this.QRCodeUrl="/"
      },
      showEdit(id){
        this.configStatus=true;
        this.configHead="编辑用户信息";
        this.editType=1;
        this.editId=id;
        this.getUserInfo();
        this.reTwoFactor=false;
        this.showQRCode=false;
        this.QRCodeUrl="/";
      },
      getUserInfo(){
        let self = this
        self.$http.get('/api/user/' + self.editId).then(function (response) {
          if (response.data.status == 200) {
            self.userInfo = response.data.data
            self.$set("userInfo.password", "")
            self.$set("userInfo.re_password", "")
            if (self.userInfo.is_locked == 1) {
              self.selectedLock = {id: 1, name: "锁定"}
            }else{
              self.selectedLock = {id: 0, name: "正常"}
            }
            if (self.userInfo.is_admin == 1) {
              self.selectedRole = {id: 1, name: "管理员"}
            }else{
              self.selectedRole = {id: 0, name: "普通用户"}
            }
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      changeConfig(){
        if(this.editType==0){
          this.$http.post('/api/user', this.userInfo).then(function (response) {
            if (response.data.status == 200) {
              this.$root.alertSuccess = true;
              this.tableRe();
              this.newUserId = response.data.data.user_id;
              this.getQrCode(response.data.data.user_id)
            } else {
              this.$root.alertError = true;
            }
            this.$root.errorMsg = response.data.msg;
          }, function (response) {
            Api.user.requestFalse(response,this);
          })
        }else{
          let data = {
            email: this.userInfo.email,
            phone: this.userInfo.phone,
          }
          if (this.userInfo.password != "") {
            data.password = this.userInfo.password
            data.re_password = this.userInfo.re_password
          }
          if (this.userIsAdmin == 1) {
            data.is_admin = this.userInfo.is_admin
            data.is_locked = this.userInfo.is_locked
          }
          this.$http.put('/api/user/' + this.editId, data).then(function (response) {
            this.$root.errorMsg = response.data.msg;
            if (response.data.status == 200) {
              this.$root.alertSuccess = true;
              if(this.reTwoFactor){
                this.showQRCode=true
                this.QRCodeUrl="/";
              }else{
                this.showQRCode=false
                this.configStatus=false
              }
              if (this.userInfo.username == localStorage.getItem('current_user') && this.userInfo.password != "") {
                this.logoutCurrentUser()
              }else{
                this.tableRe();
              }
            } else {
              this.$root.alertError = true;
            }
          }, function (response) {
            Api.user.requestFalse(response,this);
          })
        }

      },
      getQrCode(id){
        this.$http.post("/api/user/two_factor", {"user_id": id}).then(function (response) {
          if (response.status == 200) {
            this.QRCodeUrl = 'data:image/png;base64,' + response.data
            this.showQRCode = true
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      del(id){
        this.delUserId = id
        this.$http.delete('/api/user/' + this.delUserId).then(function (response) {
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
          this.tableRe()
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      lockUser(user){
        var lock_data = {
          is_locked: !user.is_locked,
        }
        this.$http.put('/api/user/' + user.id, lock_data).then(function (response) {
          this.$root.errorMsg = response.data.msg;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
          } else {
            this.$root.alertError = true;
          }
          this.tableRe()
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      }
    },
    components: {
      ysTable,
      ysSelect,
      ysPoptip,
      aside,
      userAddBase
    }
  }

</script>