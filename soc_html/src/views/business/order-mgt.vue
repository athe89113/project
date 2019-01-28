<template>
  <div class="ys-con">
    <table class="ys-table ys-table-center">
      <thead>
        <tr>
          <th>订单编号</th>
          <th>订单时间</th>
          <th>服务信息</th>
          <th>订单状态</th>
          <th>金额(元)</th>
          <th style="width:120px"></th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr class="odd" v-for="list in tableList">
          <td>{{list.order_no}}</td>
          <td>{{list.create_time}}</td>
          <td>{{list.detail}}</td>
          <td>
            <span class="ys-info-color" v-if="list.status==0">等待支付</span>
            <span class="ys-success-color" v-if="list.status==1">支付完成</span>
            <span class="ys-error-color" v-if="list.status==2">支付错误</span>
            <span class="ys-error-color" v-if="list.status==3">支付超时</span>
          </td>
          <td class="ys-error-color">{{list.total_fee}}</td>
          <td>
            <span v-if="list.status==0">
              <i class="md md-access-time m-r-2 font14 icon-vert"></i>剩余{{list.left_time | timeFil}}
            </span>
          </td>
          <td class="operate">
            <a v-if="list.status==1 || list.status==2">--</a>
            <a v-if="list.status==0"
               @click="goPay(list.id)"
               class="m-r-10">立即支付</a>
            <a v-if="list.status==0"
               @click="cancelOrder(list.id)"></i>取消订单</a>
            <span v-if="list.status==3">
              <ys-poptip confirm
                         title="您确认删除此订单吗？"
                         :placement="'left'"
                         @on-ok="deleteOrder(list.id)"
                         @on-cancel="">
                <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
              </ys-poptip>
            </span>
          </td>
        </tr>
      </tbody>
    </table>
    <ys-table
            :url.sync='tableUrl'
            :data.sync="tableList"
            v-ref:table>
    </ys-table>
    <modal :show.sync="payAlert" :title="'请在新打开的页面中完成付款'" :width="'330'">
      <div slot="content" class="clearfix">
        <div class="fLeft d-i-b m-l-10">
          <img src="../../assets/images/pay-error.png" class="verticalM" style="width:32px"/>
        </div>
        <div class="fLeft d-i-b m-l-10">
          <p>付款完成前请不要关闭此窗口</p>
          <p class="m-t-15">付款成功后订单状态可能会有1分钟左右延迟</p>
          <p class="m-t-15">您也可以稍后刷新页面查看</p>
        </div>
      </div>
      <div slot="footer">
        <button class="ys-btn m-r-10" type="button" @click="paySuccess">
          <span>付款成功</span>
        </button>
        <button class="ys-btn white-btn" type="button" @click="payError">
          <span>支付遇到问题</span>
        </button>
      </div>
    </modal>
  </div>
</template>
<style scoped>
.cart-table-foot{
  background:rgba(0,0,0,0.3);
  padding:10px 20px;
}
</style>
<script>
  import Api from 'src/lib/api'
  import ysSelect from 'src/components/select.vue'
  import ysTable from 'src/components/table-data.vue'
  import modal from 'src/components/modal.vue'
  import ysPoptip from 'src/components/poptip.vue'
  export default {
    name: "defense-order-mgt",
    data() {
      return {
        tableUrl: '/api/purchase/order/dts',
        tableList:"",
        tableSel:[],
        payAlert:false,
        curOrderId:"",
      }
    },
    ready: function() {

    },
    filters: {
      timeFil:function(value){
        return formatSeconds(value);
        function formatSeconds(value) {
          var theTime = parseInt(value);// 秒
          var theTime1 = 0;// 分
          var theTime2 = 0;// 小时
          if(theTime > 60) {
            theTime1 = parseInt(theTime/60);
            theTime = parseInt(theTime%60);
            if(theTime1 > 60) {
              theTime2 = parseInt(theTime1/60);
              theTime1 = parseInt(theTime1%60);
            }
          }
          var result = "";
          if(theTime1 > 0) {
            result = ""+parseInt(theTime1)+"分"+result;
          }
          if(theTime2 > 0) {
            result = ""+parseInt(theTime2)+"小时"+result;
          }
          return result;
        }
      }
    },
    methods:{
      goPay(id){
        this.curOrderId=id;
        this.$root.loadStatus=true;
        this.$http.post('/api/purchase/order/'+id+'/repay').then(function (response) {
          this.$root.loadStatus=false;
          if (response.data.status == 200) {
            this.payAlert=true;
            window.open(response.data.data.pay_url);
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      cancelOrder(id){
        this.$root.loadStatus=true;
        let data = {
          "status": 2
        }
        this.$http.put('/api/purchase/order/'+id+'/cancel', data).then(function (response) {
          this.$root.loadStatus=false;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.tableRe()
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      deleteOrder(id){
        this.$root.loadStatus=true;
        this.$http.delete('/api/purchase/order/'+id).then(function (response) {
          this.$root.loadStatus=false;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.tableRe()
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      paySuccess(){
        this.checkPay()
      },
      checkPay(){
        this.$root.loadStatus=true;
        this.$http.post('/api/purchase/order/'+this.curOrderId+'/refresh').then(function (response) {
          this.$root.loadStatus=false;
          if (response.data.status == 200) {
            if(response.data.data.status==1){
              this.$root.alertSuccess = true;
            }else{
              this.$root.alertError = true;
            }
            this.payAlert=false;
            this.$root.errorMsg = response.data.data.status_msg;
            this.tableRe()
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      payError(){
        this.payAlert=false;
      },
      tableRe(){
        this.$refs.table.Re()
      },
    },
    computed: {
    },
    watch:{
    },
    components: {
      ysTable,
      ysSelect,
      modal,
      ysPoptip
    }
  }
</script>
