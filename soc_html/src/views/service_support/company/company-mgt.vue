<template>
  <div class="ys-con">
    <div class="pageHead">
      <p class="pageTitle"><span>支持管理 </span>- 公司管理</p>
    </div>
    <div class="tool-box">
      <div class="fLeft d-i-b">
        <button class="ys-btn" @click="showAdd()"><i class="ys-icon icon-add-circle"></i>添加公司</button>
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
        <th></th>
        <th>公司名</th>
        <th>套餐</th>
        <th>扩容套餐</th>
        <th>服务期限</th>
        <th>剩余天数</th>
        <th>服务状态</th>
        <th style="width:200px;" class="textC">操作</th>
      </tr>
      </thead>
      <tbody>
      <template v-for="list in tableList">
        <tr v-bind:class="[$index%2==1 ? 'even' : 'odd', showId==list.id? 'shown': ''] ">
          <td><i class="details-control verticalM" @click="showDetail(list)"></i></td>
          <td><a v-link="{ name: 'company-user', params: {company_id: list.id} }">{{ list.name }}</a></td>
          <td>{{ list.set_meal }}</td>
          <td>{{ list.other_meal }}</td>
          <td>{{ list.end_time }}</td>
          <td>{{ list.end_days }}</td>
          <td>{{ list.service_status }}</td>
          <td class="textC">
            <a class="m-r-10" v-link="{ name: 'company-user', params: {company_id: list.id} }"><i class="fa fa-eye m-r-2"></i>查看用户</a>
            <a class="m-r-10" @click="showEdit(list.id)"><i class="fa fa-pencil m-r-2"></i>编辑</a>
            <ys-poptip confirm
                       title="您确认删除此公司吗？"
                       :placement="'left'"
                       @on-ok="del(list.id)"
                       @on-cancel="">
              <a><i class="fa fa-trash m-r-2"></i>删除</a>
            </ys-poptip>
          </td>
        </tr>
        <template v-if="showId == list.id">
          <tr class="even" style="padding: 0px 35px 0px 35px;">
            <td colspan='8'>
              <div class="row">
                <div class="col-sm-12">公司电话: {{list.phone}}</div>
              </div>
              <div class="row">
                <div class="col-sm-12">公司邮箱: {{list.email}}</div>
              </div>
              <div class="row">
                <div class="col-sm-12">公司地址: {{list.address}}</div>
              </div>
            </td>
          </tr>
        </template>
      </template>
      </tbody>
    </table>

    <ys-table :url="tableUrl"
              :data.sync="tableList"
              :filter.sync="tableFilter"
              :search.sync="searchValue"
              v-ref:table></ys-table>
    <aside :show.sync="configStatus"
           :header="configHead"
           :left="'auto'"
           :width="'500px'">
      <div>
        <validator name="valCompany" @valid="onValid = true" @invalid="onValid = false">
          <div v-if="!showQRCode">
            <div class="ys-box">
              <div class="ys-box-title">填写公司基本信息</div>
              <div class="ys-box-con">
                <table class="ys-set-table">
                  <tbody>
                  <tr>
                    <td>公司名称</td>
                    <td>
                      <input class="ys-input"
                             v-model="companyInfo.name"
                             style="width: 218px"
                             v-validate:company_name="['required']">
                    </td>
                  </tr>
                  <tr>
                    <td>公司地址</td>
                    <td>
                      <input class="ys-input"
                             v-model="companyInfo.address"
                             style="width: 218px">
                    </td>
                  </tr>
                  <tr>
                    <td>联系电话</td>
                    <td>
                      <input class="ys-input"
                             v-model="companyInfo.phone"
                             style="width: 218px"
                             v-validate:company_phone="['numeric']">
                    </td>
                  </tr>
                  <tr>
                    <td>公司邮箱</td>
                    <td>
                      <input class="ys-input"
                             v-model="companyInfo.email"
                             style="width: 218px"
                             v-validate:company_email="['email']">
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="ys-box m-t-10" v-if="editType==0">
              <div class="ys-box-title">创建公司用户</div>
              <div class="ys-box-con">
                <table class="ys-set-table">
                  <tbody>
                  <tr>
                    <td>用户名</td>
                    <td>
                      <input class="ys-input"
                             v-model="companyInfo.username"
                             style="width: 218px"
                             v-validate:username="['required']">
                    </td>
                  </tr>
                  <tr>
                    <td>用户邮箱</td>
                    <td>
                      <input class="ys-input"
                             v-model="companyInfo.user_email"
                             style="width: 218px"
                             v-validate:user_email="['email', 'required']">
                    </td>
                  </tr>
                  <tr>
                    <td>密码</td>
                    <td>
                      <input type="password"
                             class="ys-input"
                             v-model="companyInfo.password"
                             style="width: 218px"
                             v-validate:password="['required']">
                    </td>
                  </tr>
                  <tr>
                    <td>重复密码</td>
                    <td>
                      <input type="password"
                             class="ys-input"
                             v-model="companyInfo._password"
                             style="width: 218px"
                             v-validate:_password="['required', '_password']">
                    </td>
                  </tr>
                  <tr>
                    <td>联系电话</td>
                    <td>
                      <input class="ys-input"
                             v-model="companyInfo.user_phone"
                             style="width: 218px"
                             v-validate:user_phone="['numeric', 'required']">
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="aside-foot m-t-20">
              <button class="ys-btn m-r-10" @click="changeConfig()">确定</button>
              <button class="ys-btn ys-btn-white" @click="configStatus=false">取消</button>
            </div>
          </div>
          <div v-if="showQRCode">
            <div class="ys-box m-t-10" v-if="editType==0">
              <div class="ys-box-title">二次验证</div>
              <div class="ys-box-con">
                <p class="textC">请扫描二次验证码：</p>
                <p class="textC"><img class="m-t-10" :src="QRCodeUrl" style="width:120px;"></p>
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
  </div>
</template>

<style>
</style>

<script>
  import ysTable from 'src/components/table-data.vue'
  import ysSelect from 'src/components/select.vue'
  import ysPoptip from 'src/components/poptip.vue'
  import aside from 'src/components/Aside.vue'
  export default {
    name: "service-support-company",
    data(){
      return {
        tableUrl: '/api/company/dts',
        tableList: "",
        tableFilter: "",
        searchValue: "",
        showId: 0,
        delCompanyId: "",

        //添加
        configStatus:false,
        configHead:"",
        editType:0,
        editId:"",

        showQRCode: false,
        QRCodeUrl: "/",
        companyInfo: {
          name: "",
          email: "",
          phone: "",
          address: "",
          username: "",
          password: "",
          _password: "",
          user_email: "",
          user_phone: "",
        },
        onValid: false,
        check: false,
      }
    },
    ready: function () {

    },
    methods: {
      tableRe(){
        this.$refs.table.Re()
      },
      showAdd(){
        this.configStatus=true;
        this.configHead="添加公司";
        this.editType=0;
        this.showQRCode=false;
        this.companyInfo={
          name: "",
          email: "",
          phone: "",
          address: "",
          username: "",
          password: "",
          _password: "",
          user_email: "",
          user_phone: "",
        }
      },
      showEdit(id){
        this.configStatus=true;
        this.configHead="编辑公司信息";
        this.editType=1;
        this.editId=id;
        this.getCompanyInfo();
      },
      getCompanyInfo(){
        this.$http.get('/api/company/' + this.editId).then(function (response) {
          if (response.data.status == 200) {
            this.companyInfo = response.data.data
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
          this.$http.post('/api/company', this.companyInfo).then(function (response) {
            if (response.data.status == 200) {
              this.$root.alertSuccess = true;
              this.tableRe();
              this.getQrCode(response.data.data.user_id)
            } else {
              this.$root.alertError = true;
            }
            this.$root.errorMsg = response.data.msg;
          }, function (response) {
            Api.user.requestFalse(response,this);
          })
        }else{
          this.$http.put('/api/company/' + this.editId, this.companyInfo).then(function (response) {
            this.$root.errorMsg = response.data.msg;
            if (response.data.status == 200) {
              this.$root.alertSuccess = true;
              this.configStatus=false;
              this.tableRe();
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
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      showDetail(list){
        var self = this
        if (self.showId == list.id) {
          // 关闭
          self.showId = 0
        } else {
          // 展开
          self.showId = list.id
        }
      },
      del(id){
        this.delCompanyId = id
        this.$http.delete('/api/company/' + this.delCompanyId).then(function (response) {
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
    },
    components: {
      ysTable,
      ysSelect,
      ysPoptip,
      aside
    },
    validators: {
      email: function (val/*,rule*/) {
        if (val == "") {
          return true
        }
        return /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(val)
      },
      _password: function (val) {
        return this.vm.companyInfo.password == this.vm.companyInfo._password
      },
      numeric: function (val/*,rule*/) {
        if (val == "") {
          return true
        }
        return /^[-+]?[0-9]+$/.test(val)
      }
    },
  }
</script>
