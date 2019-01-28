<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <div class="tool-box">
        <div class="fLeft d-i-b" v-if="userIsAdmin==1">
          <div>
            <button class="ys-btn" @click="showAdd()"><i class="ys-icon icon-add-circle"></i>添加用户</button>
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
      <table class="ys-table m-t-10">
        <thead>
        <tr>
          <th>工号</th>
          <th>用户名</th>
          <th>电话</th>
          <th>邮件地址</th>
          <th>最后登录IP</th>
          <th>最后登录时间</th>
          <th>角色</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
        </thead>
        <tbody>
        <template v-for="list in tableList">
          <tr v-bind:class="[$index%2==1 ? 'even' : 'odd', showId==list.id? 'shown': ''] ">
            <td>{{ list.employee_id }}</a></td>
            <td>{{ list.username }}</a></td>
            <td>{{ list.phone }}</td>
            <td>{{ list.email }}</td>
            <td>{{ list.last_login_ip }}</td>
            <td>{{ list.last_login }}</td>
            <td>{{ list.role_name }}</td>
            <td>
              <span v-if="list.is_locked==0" class="ys-success-color">正常</span>
              <span v-if="list.is_locked==1" class="ys-error-color">禁用</span>
              <span v-if="list.is_locked==2" class="ys-error-color">锁定</span>
            </td>
            <td class="operate">
              <!--<tooltip :content="'解锁'" :delay="1000" v-if="list.is_locked==1">-->
                <!--<a @click="lockUser(list)"><i class="ys-icon icon-unlock"></i></a>-->
              <!--</tooltip>-->
              <!--<tooltip :content="'锁定'" :delay="1000" v-else>-->
                <!--<a @click="lockUser(list)"><i class="ys-icon icon-lock"></i></a>-->
              <!--</tooltip>-->
              <tooltip :content="'编辑'" :delay="1000">
                <a @click="showEdit(list)"><i class="ys-icon icon-edit"></i></a>
              </tooltip>
              <ys-poptip confirm
                         title="您确认删除此用户吗？"
                         :placement="'left'"
                         @on-ok="del(list.id)"
                         @on-cancel="">
                <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
              </ys-poptip>
            </td>
          </tr>
        </template>
        </tbody>
      </table>
      <ys-table :url="tableUrl" :data.sync="tableList" :filter.sync="tableFilter" :search.sync="searchValue"
                v-ref:table></ys-table>
    </div>
    <aside :show.sync="configStatus"
           :header="configHead"
           :left="'auto'"
           :width="'500px'">
      <div>
        <validator name="valCompany" @valid="onValid = true" @invalid="onValid = false">
          <div v-if="!showQRCode">
            <table class="ys-form-table">
              <tbody>
              <tr>
                <td>用户名</td>
                <td v-if="editType==0">
                  <input class="ys-input"
                         v-model="userInfo.username"
                         placeholder="最多30个字符"
                         style="width: 218px"
                         v-validate:username="['required']">
                </td>
                <td v-else>{{userInfo.username}}</td>
              </tr>
              <tr>
                <td>手机</td>
                <td>
                  <input class="ys-input"
                         v-model="userInfo.phone"
                         style="width: 218px"
                         placeholder="填写11位手机号"
                         v-validate:user_phone="['numeric', 'required']">
                </td>
              </tr>
              <tr>
                <td>用户邮箱</td>
                <td>
                  <input class="ys-input"
                         v-model="userInfo.email"
                         placeholder="填写邮件地址"
                         style="width: 218px"
                         v-validate:user_email="['email', 'required']">
                </td>
              </tr>
               <tr>
                <td>工号</td>
                <td>
                  <input class="ys-input"
                         v-model="userInfo.employee_id"
                         placeholder="工号由1-16位大小写字母和数字组成"
                         style="width: 218px">
                </td>
              </tr>
              <tr>
                <td>密码</td>
                <td v-show="editType==0">
                  <input type="password"
                         class="ys-input"
                         v-model="userInfo.password"
                         placeholder="设置密码"
                         style="width: 218px"
                         v-validate:password="['required']">
                </td>
                <td v-else="">
                  <input type="password"
                         class="ys-input"
                         v-model="userInfo.password"
                         placeholder="设置密码, 留空则不修改"
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
                         placeholder="确认密码"
                         v-validate:_password="['required', '_password']">
                </td>
              </tr>
              <tr>
                <td>状态</td>
                <td>
                  <radio :list="userLockedOption" :value.sync="userInfo.is_locked"></radio>

                  <!--<ys-select-->
                          <!--:option="lockOptions"-->
                          <!--@change="userInfo.is_locked = selectedLock.id"-->
                          <!--:selected.sync="selectedLock"-->
                          <!--:width="218"></ys-select>-->
                </td>
              </tr>
              <tr>
                <td>角色</td>
                <td>
                  <ys-select
                          :option="perOption"
                          :selected.sync="selectPer"
                          :width="218">
                  </ys-select>
                </td>
              </tr>
              <tr>
                <td>二次验证</td>
                <td v-if="editType==1">
                  <span v-if="userInfo.gs_status==1" class="ys-success-color">已开启</span>
                  <span v-if="userInfo.gs_status==0" class="ys-error-color">已关闭</span>
                  <!--<input type="checkbox"-->
                         <!--class="m-l-10"-->
                         <!--value="二次验证"-->
                         <!--@click="reTwoFactor=!reTwoFactor"-->
                         <!--v-model="reTwoFactor">-->
                  <!--<span class="m-l-3">重新绑定二次验证</span>-->

                  <input type="checkbox"
                         class="m-l-10"
                         @click="closeTwoFactor=!closeTwoFactor"
                         v-model="closeTwoFactor">
                  <span class="m-l-3">解绑二次验证</span>

                </td>
              </tr>
              </tbody>

            </table>
            <div class="m-t-10">
              <admin-password :admin-password.sync="adminPassword"></admin-password>
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
  import userAddBase from "../../service_support/user/user-add-base.vue"
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
        adminPassword: '',
        userLockedOption: [
          {id:0,text:"正常"},
          {id:1,text:"禁用"},
          {id:2,text:"锁定", disabled: true},
        ],
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
          _password: "",
          phone: "",
          email: "",
          is_locked: 0,
          is_admin: 0,
          role_id: '',
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
        perOption: [],
        selectPer: {},
        showQRCode: false,
        QRCodeUrl: "/",
        newUserId:"",
        reTwoFactor: false,
        closeTwoFactor: false
      }
    },
    ready: function () {
      this.getPerList()
    },
    methods: {
      tableRe(){
        var self = this
        self.$refs.table.Re()
      },
      showAdd(){
        this.selectPer = this.perOption[0]
        this.configStatus=true;
        this.configHead="添加用户";
        this.editType=0;
        this.userInfo={
          username: "",
          password: "",
          _password: "",
          phone: "",
          email: "",
          is_locked: 0,
          is_admin: 0
        };
        this.showQRCode=false;
        this.QRCodeUrl="/"
      },
      showEdit(list){
        let id = list.id
        this.configStatus=true;
        this.configHead="编辑用户信息";
        this.editType=1;
        this.editId=id;
        this.getUserInfo();
        this.reTwoFactor=false;
        this.closeTwoFactor=false;
        this.showQRCode=false;
        this.QRCodeUrl="/";
        this.selectPer=list.roles[0]
      },
      getPerList(){
        this.$http.get('/api/permission/list').then ( (response) => {
          this.perOption = response.data.data
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getUserInfo(){
        let self = this
        self.$http.get('/api/user/' + self.editId).then(function (response) {
          if (response.data.status == 200) {
            response.data.data.password=''
            response.data.data._password=''
            self.userInfo = response.data.data
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      changeConfig(){
        if (this.userInfo.password != this.userInfo._password) {
          this.$root.errorMsg = '密码不一致'
          this.$root.alertError = true
          return false
        }

        this.userInfo.role_id = this.selectPer.id
        this.userInfo.admin_password = this.adminPassword
        if(this.editType==0){
          this.$http.post('/api/admin/user', this.userInfo).then(function (response) {
            if (response.data.status == 200) {
              this.$root.alertSuccess = true;
              this.configStatus = false;
              this.tableRe();
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
            employee_id: this.userInfo.employee_id,
            roles: this.selectPer,
            role_id: this.selectPer.id,
            admin_password: this.adminPassword,
            gs_status: this.closeTwoFactor ? 0 : 1
          }
          if (this.userInfo.password != "") {
            data.password = this.userInfo.password
            data.re_password = this.userInfo.re_password

          }
          if (this.userIsAdmin == 1) {
            data.is_admin = this.userInfo.is_admin
            data.is_locked = this.userInfo.is_locked
          }
          this.$http.put('/api/admin/user/' + this.editId, data).then(function (response) {
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