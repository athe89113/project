<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <table class="ys-table m-t-10 detail-table">
        <thead>
        <tr>
          <th>ID</th>
          <th>排序</th>
          <th class="textL">菜单名称</th>
          <th>登录着陆页</th>
          <th>是否启用</th>
          <th>操作</th>
        </tr>
        </thead>
        <tbody v-for="list in tableList">
          <tr class="odd" v-bind:class="[curEditId == list.id ? 'on' : '' ]">
            <td><span>{{list.index}}</span></td>
            <td>{{list.sort}}</td>
            <td class="textL">
              <div v-if="list.level==1">{{list.name}}</div>
              <div v-if="list.level==2" style="padding-left:24px">
                <span class="menuLine">
                  <span class="middle"></span>
                </span>
                <span class="ys-primary-color">{{list.name}}</span>
              </div>
              <div v-if="list.level==3" style="padding-left:76px">
                <span class="menuLine">
                  <span class="top" v-if="!list.final"></span>
                  <span class="bottom"></span>
                  <span class="middle"></span>
                </span>
                <span class="ys-info-color">{{list.name}}</span>
              </div>
            </td>
            <td>
              <span v-if="list.is_landing==1"><i class="ys-icon icon-ok ys-warn-color font12"></i></span>
              <span v-if="list.is_landing==0" @click="switchLanding(list)" class="ys-error-color">-</span>
            </td>
            <td>
              <span v-if="list.enable==1" class="ys-success-color" @click="switchEnable(list, 0)"><i class="ys-icon icon-check-circle m-r-5"></i>启用</span>
              <span v-if="list.enable==0" class="ys-error-color" @click="switchEnable(list, 1)"><i class="ys-icon icon-clear-circle m-r-5"></i>禁用</span>
            </td>
            <td class="operate">
              <tooltip :content="'编辑'" :delay="1000">
                <a @click="editDetail(list)"><i class="ys-icon icon-edit"></i></a>
              </tooltip>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <aside :show.sync="showConfigStatus"
         :header="configHead"
         :left="'auto'"
         :width="'500px'">
    <validator name="valMenu" @valid="onConfigValid = true" @invalid="onConfigValid = false">
      <div>
        <table class="ys-form-table">
          <tr>
            <td>菜单 ID</td>
            <td>
              {{curDetail.index}}
            </td>
          </tr>
          <tr>
            <td>菜单名称</td>
            <td>
              <div v-if="curDetail.level==1">
                <ys-valid>
                  <input class="ys-input"
                         placeholder="最多六个字符"
                         v-model="curDetail.name"
                         v-validate:name="['length1']"
                         initial='off'/>
                  <div slot="content"
                       v-show="$valMenu.name.length1">
                    <p>输入六个字符</p>
                  </div>
                </ys-valid>
              </div>
              <div v-else>
                <ys-valid>
                  <input class="ys-input"
                         placeholder="最多七个字符"
                         v-model="curDetail.name"
                         v-validate:name="['length2']"
                         initial='off'/>
                  <div slot="content"
                       v-show="$valMenu.name.length2">
                    <p>输入七个字符</p>
                  </div>
                </ys-valid>
              </div>
            </td>
          </tr>
          <tr>
            <td>是否启用</td>
            <td>
              <radio :list="enableData" :value.sync="curDetail.enable"></radio>
            </td>
          </tr>
          <tr>
            <td>登录着陆页</td>
            <td>
              <radio :list="landingData" :value.sync="curDetail.is_landing"></radio>
            </td>
          </tr>
          <tr>
            <td>排序</td>
            <td>
              <ys-valid>
                <input class="ys-input"
                       placeholder="输入排序序号， 0-99"
                       v-model="curDetail.sort"/>
              </ys-valid>
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <span class="ys-info-color"><i class="ys-icon icon-info-circle m-r-5"></i>修改配置成功后您需要手动刷新页面看到新的菜单</span>
            </td>
          </tr>
        </table>
      </div>
      <section class="m-t-20">
        <admin-password :admin-password.sync="adminPassword"></admin-password>
      </section>
      <div class="aside-foot m-t-20">
        <button class="ys-btn m-r-10" @click="saveDetail()">保存</button>
        <button class="ys-btn ys-btn-white" @click="showConfigStatus=false">取消</button>
      </div>
    </validator>
  </aside>
</template>
<style scoped>
  .menuLine{
    display: inline-block;
    width:35px;
    position: relative;
    vertical-align: middle;
  }
  .menuLine>span{
    display: inline-block;
    position:absolute;
    background:#5373b1;
  }
  .menuLine .top{
    top:0px;
    left:0px;
    width:1px;
    height:18px;
  }
  .menuLine .bottom{
    bottom:0px;
    left:0px;
    width:1px;
    height:18px;
  }
  .menuLine .middle{
    bottom:0px;
    left:1px;
    width:25px;
    height:1px;
  }
</style>
<script>
  import Api from 'src/lib/api'
  import icon from 'src/components/icon.vue'
  export default {
    name: "menu-mgt",
    data() {
      return {
        tableUrl: "",
        tableList: [],
        showConfigStatus: false,
        configHead: "编辑菜单",

        curEditId: 0,
        curDetailId: 0,
        curDetail: {},

        enableData: [
          {id: 1, text: "启用"},
          {id: 0, text: "禁用"},
        ],
        landingData: [
          {id: 1, text: "是"},
          {id: 0, text: "否"},
        ],
        adminPassword: '',
      }
    },
    filters: {
      nameLabelFil:function(level){
        if(level==1){
          return "最多六个字符"
        }else{
          return "最多七个字符"
        }
      }
    },
    ready: function () {
      this.getMenuList()
    },
    methods: {
      // 获取菜单列表
      getMenuList(){
        this.$http.get('/api/system/menus').then(function (response) {
          if (response.data.status == 200) {
            //this.tableList = response.data.data;
            let data = response.data.data.default;
            let list=[];
            for(let topic in data){
              data[topic].level=1;
              list.push(data[topic])
              for(let menu in data[topic].children){
                data[topic].children[menu].level=2;
                list.push(data[topic].children[menu])
                for(let page in data[topic].children[menu].children){
                  data[topic].children[menu].children[page].level=3;
                  if(page==data[topic].children[menu].children.length-1){
                    data[topic].children[menu].children[page].final=true;
                  }else{
                    data[topic].children[menu].children[page].final=false;
                  }
                  list.push(data[topic].children[menu].children[page])
                }
              }
            }
            this.tableList=list;
          }else{

          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      showMiniLoad(){
        this.loadMini = true;
      },
      switchEnable(list, status){
        let data = {}
        if (status == 0){
          // disable
          data.enable = 0
        } else {
          // enable
          data.enable = 1
        }
        this.$http.put('/api/system/menus/' + list.id + '/status', data).then(function (response) {
          if (response.data.status == 200) {
            this.getMenuList()
          }else{
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      switchLanding(list){
        let data = {
          is_landing: 1
        }
        this.$http.put('/api/system/menus/' + list.id + '/landing', data).then(function (response) {
          if (response.data.status == 200) {
            this.getMenuList()
          }else{
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      editDetail(list){
        this.curDetail=JSON.parse(JSON.stringify(list));
        this.curEditId = list.id;//设置当前编辑id
        this.curDetailId = "";//把当前展示详情ID置为空
        this.showConfigStatus = true;//弹出右侧滑出界面
      },
      showDetail(id){
        this.curEditId = "";//设置当前编辑ID为空
        //如果curEditId和此条id相同,就关闭,否则就展示详情
        if (this.curDetailId == id) {
          this.curDetailId = ""
        } else {
          this.curDetailId = id;
        }
      },
      // 保存修改
      saveDetail() {
        if(!this.$valMenu.valid){
          return false
        }
        let data = {
          "name": this.curDetail.name,
          "is_landing": this.curDetail.is_landing,
          "enable": this.curDetail.enable,
          "sort": this.curDetail.sort,
          "admin_password": this.adminPassword,
        }
        this.$http.put('/api/system/menus/' + this.curDetail.id, data).then(function (response) {
          if (response.data.status == 200) {
            this.showConfigStatus = false;
            this.getMenuList()
          }else{
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      addIdcSave(){
        this.showConfigStatus = true;
      }
    },
    watch: {
      showConfigStatus() {
        if(!this.showConfigStatus){this.curEditId=""}
      }
    },
    validators: {
      length1: function (val) {
        if(val!="" && val.length>6){
          return false
        }else{
          return true
        }
      },
      length2: function (val) {
        if(val!="" && val.length>7){
          return false
        }else{
          return true
        }
      }
    },
    components: {
      "icon": icon
    }
  }
</script>
