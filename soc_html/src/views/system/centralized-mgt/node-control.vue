<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <div class="clearfix">
        <div class="col-md-6 p-l-0">
        <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5"></i>本级中心命名</div>
        <div class="ys-box-con">
          <div class="">
            <span class="ys-info-color">本级名称：</span>
          <span>
            <input class="ys-input"
                   placeholder="自定义本级中心名称"
                   v-model="configs.name"/>
          </span>
          </div>
          <div class="m-t-20">
            <span class="ys-info-color">备注说明：</span>
          <span>
            <input class="ys-input"
                   placeholder="添加描述说明"
                   v-model="configs.info"/>
          </span>
          </div>
        </div>

      </div>
      <div class="col-md-6">
        <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5"></i>本级角色</div>
        <div class="ys-box-con">
          <div :class="[parent==true || children==true ? 'disabled' : ''] ">
            <ys-radio :list="nodeData" :value.sync="configs.type"></ys-radio>
          </div>


        </div>
      </div>
      </div>
      <div class="ys-box m-t-20">
        <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5"></i>级联控制设置</div>
        <div class="ys-box-con">


                    <div v-if="configs.type!='center'" class="m-t-20">
          <span><ys-checkbox :text="'允许上级级联'"
                             :show.sync="configs.accept_parent_connection"></ys-checkbox></span>
          </div>
          <div v-if="configs.type!='center'" class="m-t-20">
            <span class="ys-info-color">级联密钥：</span>
          <span :class="[parent==true ? 'disabled' : ''] ">
            <input class="ys-input"
                   placeholder="级联秘钥"
                   v-model="configs.auth_key"/ >
          </span>
          </div>
          <div v-if="configs.type=='center'||configs.type=='sub_center'" class="m-t-20">
          <span><ys-checkbox :text="'当下级中心失联时发出告警'"
                             :show.sync="configs.notify_when_lose_children"></ys-checkbox></span>
          </div>



          <p class="m-t-15" v-if="show_accept_apply_policy==true">
            <ys-checkbox :text="'接收并应用上级控制中心下发的策略'"
                               :show.sync="configs.accept_apply_policy"></ys-checkbox>
          </p>
          <p class="m-t-15" v-if="show_accept_apply_event_db==true">
            <ys-checkbox :text="'接收并应用上级控制中心下发的事件库升级包'"
                               :show.sync="configs.accept_apply_event_db"></ys-checkbox>
          </p>
          <p class="m-t-15" v-if="show_accept_apply_engine==true">
            <ys-checkbox :text="'接收并应用上级控制中心下发的引擎升级包'"
                               :show.sync="configs.accept_apply_engine"></ys-checkbox>
          </p>
          <p class="m-t-15" v-if="show_accept_apply_center==true">
            <ys-checkbox :text="'接收并应用上级控制中心下发的控制中心升级包'"
                               :show.sync="configs.accept_apply_center"></ys-checkbox>
          </p>
          <!---->
          <p class="m-t-15" v-if="show_accept_apply_message==true">
            <ys-checkbox :text="'接收上级控制中心下发的事件通知'"
                               :show.sync="configs.accept_apply_message"></ys-checkbox>
          </p>
          <p class="m-t-15" v-if="show_accept_apply_loophole==true">
            <ys-checkbox :text="'接收并应用上级控制中心下发的漏洞库升级包'"
                               :show.sync="configs.accept_apply_loophole"></ys-checkbox>
          </p>
          <p class="m-t-15" v-if="show_next_message==true">
            <ys-checkbox :text="'接收下级控制中心上报的事件通知'"
                               :show.sync="configs.next_message"></ys-checkbox>
          </p>
          <p class="m-t-15" v-if="show_next_source==true">
            <ys-checkbox :text="'接收下级控制中心上报的资源数据'"
                               :show.sync="configs.next_source"></ys-checkbox>
          </p>
          <p class="m-t-15" v-if="show_next_monitor==true">
            <ys-checkbox :text="'接收下级控制中心上报的监控数据'"
                               :show.sync="configs.next_monitor"></ys-checkbox>
          </p>
          <p class="m-t-15" v-if="show_next_loophole==true">
            <ys-checkbox :text="'接收下级控制中心上报的漏洞信息'"
                               :show.sync="configs.next_loophole"></ys-checkbox>
          </p>
          <p class="m-t-15" v-if="show_next_attack==true">
            <ys-checkbox :text="'接收下级控制中心上报的攻击信息'"
                               :show.sync="configs.next_attack"></ys-checkbox>
          </p>
        </div>
        <p :class="[parent==false ? 'disabled' : ''] " class="m-t-10" style="float: left" >
          <button class="ys-btn ys-btn-s ys-btn-blue m-r-10" @click="nodeClear('parent')">解除上级中心</button>
        </p>
        <p :class="[children==false ? 'disabled' : '']" class="m-t-10" style="float: left">
          <button class="ys-btn ys-btn-s ys-btn-blue m-r-10" @click="nodeClear('children')">解除下级中心</button>
        </p>
      </div>
      <section class="m-t-40">
        <admin-password :admin-password.sync="adminPassword"></admin-password>
      </section>
      <div class="aside-foot m-t-20">
        <button class="ys-btn m-r-10" v-if="showAlert==false" @click="saveSettings()">保存</button>
        <ys-poptip :placement="'right'" :confirm="true" :title="'修改中心角色将有可能造成上下级关系丢失，是否继续操作？'"
                   @on-ok="saveSettings()"
                   @on-cancel="">
          <button class="ys-btn m-r-10" v-if="showAlert==true">保存</button>
        </ys-poptip>
      </div>
    </div>
  </div>
</template>
<style scoped>
</style>
<script>
  import Api from 'src/lib/api'
  import ysCheckbox from 'src/components/checkbox.vue'
  import ysRadio from 'src/components/radio.vue'
  import icon from 'src/components/icon.vue'
  import adminPassword from 'src/components/admin-password.vue'
  export default {
    name: "node-control",
    data() {
      return {
        adminPassword: "",
        nodeData: [
          {id: "center", text: '一级中心'},
          {id: "sub_center", text: '二级中心'},
          {id: "child_center", text: '三级中心'}
        ],
        configs: {
          "ip": "127.0.0.1",
          "role": "self",
          "type": "",
          "accept_parent_connection": !!0, // 允许上级级联
          "accept_apply_policy": !!0, // 接收并应用上级控制中心下发的策略
          "accept_apply_event_db": !!0, // 接收并应用上级控制中心下发的事件库升级包
          "accept_apply_engine": !!0, // 接收并应用上级控制中心下发的引擎升级包
          "accept_apply_center": !!0, // 接收并应用上级控制中心下发的控制中心升级包
          "accept_apply_message": !!0,
          "accept_apply_loophole": !!0,
          "next_message": !!0,
          "next_source": !!0,
          "next_monitor": !!0,
          "next_loophole": !!0,
          "next_attack": !!0,
          "notify_when_lose_children": !!1,  // 当下级中心失联时发出告警
          "auth_key": '',
          "name":"",
          "info":"",
        },
        show_accept_apply_policy: false,
        show_accept_apply_event_db: false,
        show_accept_apply_engine: false,
        show_accept_apply_center: false,
        show_accept_apply_message: false,
        show_accept_apply_loophole: false,
        show_next_message: false,
        show_next_source: false,
        show_next_monitor: false,
        show_next_loophole: false,
        show_next_attack: false,
        showAlert: false,
        children: false, // 当children为false的时候 去除下级中心的按钮应该禁止点击
        parent: false, // 当parent为false的时候 去除上级中心的俺就应该禁止点击
      }
    },
    ready: function () {
      this.getSettings()
    },
    methods: {
      nodeClear(node_type){
        this.$http.delete('/api/system/nodes/clear', {"node_type":node_type}).then(function(response){
          if (response.data.status == 200) {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertSuccess = true;
          }else{
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
          this.getNodes()
        })
      },
      getNodes(){
        this.$http.post('/api/system/nodes/clear/status').then(function (response) {
          if (response.data.status == 200) {
            this.children = response.data.data.children
            this.parent = response.data.data.parent
          } else {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        })
      },
      getSettings(){
        this.$http.get('/api/system/nodes/self').then(function (response) {
          if (response.data.status == 200) {
            let data_configs = response.data.data
            this.configs.accept_parent_connection = !!(data_configs.accept_parent_connection)
            this.configs.accept_apply_policy = !!(data_configs.accept_apply_policy)
            this.configs.accept_apply_event_db = !!(data_configs.accept_apply_event_db)
            this.configs.accept_apply_engine = !!(data_configs.accept_apply_engine)
            this.configs.accept_apply_center = !!(data_configs.accept_apply_center)
            this.configs.notify_when_lose_children = !!(data_configs.notify_when_lose_children)
            this.configs.role = data_configs.role
            this.configs.type = data_configs.type
            this.configs.auth_key = data_configs.auth_key
            this.configs.name = data_configs.name
            this.configs.info = data_configs.info
            this.configs.accept_apply_message = !!(data_configs.accept_apply_message)
            this.configs.accept_apply_loophole = !!(data_configs.accept_apply_loophole)
            this.configs.next_message = !!(data_configs.next_message)
            this.configs.next_source = !!(data_configs.next_source)
            this.configs.next_monitor = !!(data_configs.next_monitor)
            this.configs.next_loophole = !!(data_configs.next_loophole)
            this.configs.next_attack = !!(data_configs.next_attack)
          } else {
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
          this.getNodes()
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      saveSettings() {
        this.configs["accept_parent_connection"] = Number(this.configs["accept_parent_connection"])
        this.configs["accept_apply_policy"] = Number(this.configs["accept_apply_policy"])
        this.configs["accept_apply_event_db"] = Number(this.configs["accept_apply_event_db"])
        this.configs["accept_apply_engine"] = Number(this.configs["accept_apply_engine"])
        this.configs["accept_apply_center"] = Number(this.configs["accept_apply_center"])
        this.configs["accept_apply_message"] = Number(this.configs["accept_apply_message"])
        this.configs["accept_apply_loophole"] = Number(this.configs["accept_apply_loophole"])
        this.configs["next_message"] = Number(this.configs["next_message"])
        this.configs["next_source"] = Number(this.configs["next_source"])
        this.configs["next_monitor"] = Number(this.configs["next_monitor"])
        this.configs["next_loophole"] = Number(this.configs["next_loophole"])
        this.configs["next_attack"] = Number(this.configs["next_attack"])
        this.configs["notify_when_lose_children"] = Number(this.configs["notify_when_lose_children"])
        this.configs["admin_password"] = this.adminPassword
        this.configs['info'] = this.configs['info']
        this.configs['name'] = this.configs['name']
        this.$http.put('/api/system/nodes/self', this.configs).then(function (response) {
          if (response.data.status == 200) {
            this.$root.errorMsg = "保存配置成功";
            this.$root.alertSuccess = true;
            this.getSettings()
          } else {
            this.getSettings()
            this.$root.errorMsg = response.data.msg;
            this.$root.alertError = true;
          }
        }, function (response) {
          this.getSettings()
          Api.user.requestFalse(response, this);
        })
      }
    },
    components: {
      "ys-radio": ysRadio,
      "ys-checkbox": ysCheckbox,
      "icon": icon,
      "admin-password": adminPassword
    },
    watch: {
      "configs.type" :function (val, oldval) {
        if(val && oldval){
          // 修改中心角色将有可能造成上下级关系丢失，是否继续操作
          this.showAlert = true
        }
        this.show_accept_apply_policy = false,
        this.show_accept_apply_event_db = false,
        this.show_accept_apply_engine = false,
        this.show_accept_apply_center = false,
        this.show_accept_apply_message = false,
        this.show_accept_apply_loophole = false,
        this.show_next_message = false,
        this.show_next_source = false,
        this.show_next_monitor = false,
        this.show_next_loophole = false,
        this.show_next_attack = false,
        this.showAlert = false
        if (val == 'center'){
            this.show_next_message = true
            this.show_next_source = true
            this.show_next_monitor = true
            this.show_next_loophole = true
            this.show_next_attack = true
          }else if(val == 'sub_center'){
            this.show_accept_apply_policy = true
            this.show_accept_apply_event_db = true
            this.show_accept_apply_engine = true
            this.show_accept_apply_center = true
            this.show_accept_apply_message = true
            this.show_accept_apply_loophole = true
            this.show_next_message = true
            this.show_next_source = true
            this.show_next_monitor = true
            this.show_next_loophole = true
            this.show_next_attack = true
          }else{
        this.show_accept_apply_policy = true
        this.show_accept_apply_event_db = true
        this.show_accept_apply_engine = true
        this.show_accept_apply_center = true
        this.show_accept_apply_message = true
        this.show_accept_apply_loophole = true
          }
      }
    },
  }
</script>
