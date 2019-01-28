<template>
  <div class="ys-con pos-r">
    <div class="ys-box-con">
      <p>结合综合网络态势感知，为用户提供定制态势预警配置、管理页面，方便用户及时、快速发现问题，处理问题。</p>
    </div>
    <ul class="ys-nav m-t-10">
      <li @click="changeConfType(1)">
        <a v-bind:class="[curType==1  ? 'on' : '' ]">
          <span class="ys-nav-cor"></span>
          <span class="text">漏洞态势</span>
        </a>
      </li>
      <li @click="changeConfType(2)">
        <a v-bind:class="[curType==2  ? 'on' : '' ]">
          <span class="ys-nav-cor"></span>
          <span class="text">攻击态势</span>
        </a>
      </li>
      <!--<li @click="changeConfType(3)">-->
        <!--<a v-bind:class="[curType==3  ? 'on' : '' ]">-->
          <!--<span class="ys-nav-cor"></span>-->
          <!--<span class="text">业务态势</span>-->
        <!--</a>-->
      <!--</li>-->
      <li @click="changeConfType(4)">
        <a v-bind:class="[curType==4  ? 'on' : '' ]">
          <span class="ys-nav-cor"></span>
          <span class="text">安全态势</span>
        </a>
      </li>
      <div class="clearfix"></div>
    </ul>
    <div class="ys-box-con">
      <table class="ys-form-table">
        <tr>
          <td>最大告警次数：</td>
          <td>
            <ys-select :option="timeList" :width="150" :selected.sync="holeWarningData.curTime"></ys-select>
          </td>
        </tr>
        <tr v-for="list in holeWarningData.cells" :key="list.id">
          <td colspan="2">
            <span class="d-i-b" style="width:180px;">
              <checkbox :show.sync="list.enable" :text="list.name"></checkbox>
            </span>
            <div class="d-i-b" v-bind:class="[list.enable ? '' : 'disabled']">
              <span class="d-i-b" style="width:180px;">
                预警阈值&nbsp;&nbsp;{{list.expression}}&nbsp;&nbsp;
                <input class="ys-input" style="width:60px;" v-model="list.warning" />&nbsp;
                <span>{{list.unit}}</span>
              </span>
              <span class="m-l-20">
                告警阈值&nbsp;&nbsp;{{list.expression}}&nbsp;&nbsp;
                <input class="ys-input" style="width:60px;" v-model="list.alarm" />&nbsp;
                <span>{{list.unit}}</span>
              </span>
            </div>
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <radio :list="touchTypeData" :value.sync="holeWarningData.toggle_condition"></radio>
          </td>
        </tr>
      </table>
      <div class="ys-box m-t-15">
        <div class="ys-box-title ys-box-title-s">
          <i class="ys-icon icon-title ys-primary-color m-r-5"></i>预警告警通知配置
        </div>
        <div class="ys-box-con p-0" style="background:none;">
          <div class="custom-table">
            <table class="ys-table" style="table-layout:fixed;">
              <tr>
                <th>告警联系人</th>
                <th>邮件通知</th>
                <th>短信通知</th>
                <th class="gutter"></th>
              </tr>
            </table>
            <div class="custom-table--body-wrapper" style="height: 300px;" id="warning-user-table">
              <table class="ys-table" style="table-layout:fixed;">
                <tr v-for="list in holeWarningData.notifys" :key="list.id">
                  <td>{{list.username}}</td>
                  <td><checkbox :text="''" :show.sync="list.email"></checkbox></td>
                  <td><checkbox :text="''" :show.sync="list.sms"></checkbox></td>
                </tr>
              </table>
            </div>
          </div>
        </div>
      </div>
      <p class="m-b-20"><button class="ys-btn m-t-15" @click="saveChange()"><span><i class=""></i>保存修改</span></button></p>
    </div>
  </div>
</template>
<style scoped>
.custom-table {
  position: relative;
}
.custom-table .table {
  table-layout: fixed;
  margin-bottom: 0;
}

/** Header 右侧的空隙 */
.custom-table th.gutter {
  width: 0px;
  padding: 0;
}

.custom-table--body-wrapper {
  margin-top: -1px;
}
</style>
<script>
  import notify from './components/notify.vue'
  export default {
    name: "template-mgt",
    data() {
      return {
        timeList: [],
        curTime: {},
        curType: 1,
        touchTypeData: [{
            id: 1,
            text: "单项触发"
          },
          {
            id: 2,
            text: "多项触发"
          }
        ],
        holeWarningData: {},
      }
    },
    ready() {
      for (let a = 1; a < 25; a++) {
        this.timeList.push({
          id: a,
          name: a
        });
      }
      this.getWarningData(1);
      $('#warning-user-table').slimScroll({
          height: '320',
          position: 'right',
          size: "5px",
          color: '#4a92ff',
          wheelStep: 5,
          alwaysVisible: true
        })
    },
    methods: {
      changeConfType(conf_type) {
        if (this.curType == conf_type) {
          return
        }
        this.curType = conf_type
        this.getWarningData(conf_type)
      },
      saveChange(){
        let conf_type = this.curType
        let cells = []
        let notifys = []
        this.holeWarningData.cells.forEach(e => {
          let enable =  e.enable ? 1 : 0
          cells.push({
            id: e.id,
            alarm: e.alarm,
            warning: e.warning,
            enable: enable,
          })
        })
        this.holeWarningData.notifys.forEach(e => {
          let email =  e.email ? 1 : 0
          let sms =  e.sms ? 1 : 0
          notifys.push({
            id: e.id,
            sms: e.sms,
            email: e.email,
          })
        })
        let data = {
          max_alarm_count: this.holeWarningData.curTime.id,
          toggle_condition: this.holeWarningData.toggle_condition,
          cells: cells,
          notifys: this.holeWarningData.notifys
        }
        this.$http.put('/api/ssa/alarm/' + conf_type, data).then(function (response) {
          this.$root.loadStatus = false;
          this.$root.errorMsg = response.data.msg;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.getWarningData(conf_type)
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg;
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      getWarningData(conf_type) {
        this.$root.loadStatus = true;
        this.$http.get('/api/ssa/alarm/' + conf_type).then(function (response) {
          this.$root.loadStatus = false;
          if (response.data.status == 200) {
            let data = response.data.data;
            for (let x in this.timeList) {
              if (this.timeList[x].id == data.max_alarm_count) {
                data.curTime = this.timeList[x];
              }
            }
            this.holeWarningData = data;
          } else {
            this.$root.alertError = true;
          this.$root.errorMsg = response.data.msg;            
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
    },
    components: {
      notify
    }
  }
</script>