<template>
  <div class="ys-box">
    <div class="ys-box-con ys-wrap">
      <checkbox :show.sync="confs.enable" :text="'启用系统检查失效告警'">
      </checkbox>
      <table class="ys-table m-t-10">
        <thead>
        <tr>
          <th>告警联系人</th>
          <template v-for="type in msgTypeData">
            <th>{{type.name}}</th>
          </template>
        </tr>
        </thead>
        <tbody>
        <template v-if="prevUserList.length>0">
          <template v-for="user in userData">
            <tr class="viewTr" v-bind:class="[$index%2==1 ? 'even' : 'odd' ]">
              <td>{{user.username}}</td>
              <template v-for="type in msgTypeData">
                <td>
                  <checkbox
                      :show="{user_id:user.id,msg_id:type.id} | check"
                      @ys-click="addToUserSel(type.id,user.id)" ></checkbox>
                </td>
              </template>
            </tr>
          </template>
        </template>
        <template v-else>
          <template v-for="user in userData">
            <tr class="viewTr" v-bind:class="[$index%2==1 ? 'even' : 'odd' ]">
              <td>{{user.username}}</td>
              <template v-for="type in msgTypeData">
                <td>
                  <checkbox @ys-click="addToUserSel(type.id,user.id)" ></checkbox>

                  <!--<input type="checkbox" @click="addToUserSel(type.id,user.id)"/>-->
                </td>
              </template>
            </tr>
          </template>
        </template>
        </tbody>
      </table>
      <button class="ys-btn m-r-10 m-t-20" @click="saveConf">确定</button>

    </div>
  </div>
</template>
<script>
  import Api from 'src/lib/api'
  import ysSelect from 'src/components/select.vue'
  export default {
    name: "system-action-alert",
    data() {
      return {
        confs: {
          enable: false
        },
        curTmpId: "",
        tmpName: "",
        warnRateData: [
          {id: 60, name: "1分钟"},
          {id: 180, name: "3分钟"},
          {id: 300, name: "5分钟"},
          {id: 600, name: "10分钟"},
          {id: 900, name: "15分钟"},
          {id: 1800, name: "30分钟"},
          {id: 3600, name: "60分钟"},
        ],
        curWarnRate: {id: 60, name: "1分钟"},
        userData: [],
        msgTypeData: [],
        prevUserList: [],
        selUserList: [],
      }
    },
    filters: {
      'check': function (notify) {
        let contains = false
        this.prevUserList.forEach((item) => {
          if(notify.msg_id == item.msg_id && notify.user_id == item.user_id){
            contains = true
          }
        })
        return contains
      }
    },
    ready: function () {
      this.getConf()
      this.getWarnUserData()
    },
    methods: {
      getWarnData(){
        this.$http.get('/api/monitor/notify_group/' + this.curTmpId).then(function (response) {
          let data = response.data.data
          this.tmpName = data.name
          this.curWarnRate = {id: data.delay, name: Number(data.delay) / 60 + "分钟"}
          this.prevUserList = data.notifys
          this.selUserList = data.notifys
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      getWarnUserData(){
        this.$http.get('/api/message/user_list').then(function (response) {
          this.userData = response.data.data
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
        this.$http.get('/api/message/msg_list').then(function (response) {
          this.msgTypeData = response.data.data
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      containsNotify(notify){
        let contains = false
        let newList = []
        this.selUserList.forEach((item) => {
          if(notify.msg_id == item.msg_id && notify.user_id == item.user_id){
            contains = true
          }else {
            newList.push(item)
          }
        })
        this.selUserList = newList
        return contains
      },
      addToUserSel(type, userId){
        let notify = {"msg_id": type, "user_id": userId}
        if (this.selUserList.length == 0) {
          this.selUserList.push(notify);
        } else {
          if (this.containsNotify(notify)){

          } else {
            this.selUserList.push(notify);
          }
        }
      },
      getConf () {

        this.$root.loadStatus = true
        this.$http.get('/api/message/system/alert').then( (response) => {
          this.$root.loadStatus = false
          if (response.data.status == 200) {
            this.confs = response.data.data
            this.selUserList = response.data.data.notifys
            this.prevUserList = response.data.data.notifys
          }
        }, function (response) {
          this.$root.loadStatus = false
          Api.user.requestFalse(response, this)
        })
      },
      saveConf () {
        this.$root.loadStatus = true
        this.confs['notifys'] = this.selUserList
        this.$http.put('/api/message/system/alert', this.confs).then( (response) => {
          this.$root.loadStatus = false
          this.$root.errorMsg = response.data.msg
          if (response.data.status == 200) {
            this.getConf()
            this.$root.alertSuccess = true
          }else {
            this.$root.alertError = true
          }
        }, function (response) {
          this.$root.loadStatus = false
          Api.user.requestFalse(response, this)
        })
      }
    },
    components: {
      ysSelect,
    }
  }
</script>
