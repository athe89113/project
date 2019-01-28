<template>
  <div class="ys-con pos-r">
    <div class="box-left" style="margin-right:260px;">
      <div class="ys-box-con ys-wrap">
        <table class="ys-table">
          <thead>
          <tr>
            <th></th>
            <th>服务分类</th>
            <th>购买对象</th>
            <th>服务信息</th>
            <th>购买周期</th>
            <th>金额(元)</th>
            <th class="textC" style="width:80px">操作</th>
          </tr>
          </thead>
          <tbody>
          <tr class="odd" v-for="list in tableList">
            <td>
              <checkbox :show.sync="list.selected"></checkbox>
            </td>
            <td>{{list.type_msg}}</td>
            <td>{{list.target}}</td>
            <td class="ys-success-color">{{list.detail}}</td>
            <td v-if="list.time_modify==1">
              <ys-select :width="100" :option="timeData" :selected.sync="list.quantity_dict" @change="changeTime(list)"></ys-select>
            </td>
            <td v-else>{{list.quantity_dict.name}}</td>
            <td class="ys-error-color">{{list.total_fee}}</td>
            <td class="operate">
              <ys-poptip confirm
                         title="您确认删除吗？"
                         :placement="'right'"
                         @on-ok="deleteCart(list.id)"
                         @on-cancel="">
                <a class="ys-error-color"><i class="ys-icon icon-trash m-r-2"></i></a>
              </ys-poptip>
            </td>
          </tr>
          </tbody>
        </table>
        <ys-table
                :url="tableUrl"
                :data.sync="tableList"
                :all="true"
                v-ref:table>
        </ys-table>
        <div class="ys-row cart-table-foot" v-if="tableList.length>0">
          <p>
            <checkbox :text="'全选'"
                      :show="allSelected"
                      class="m-r-20"
                      :auto-set="false"
                      @ys-click="allSelected=!allSelected"></checkbox>
            <ys-poptip confirm
                       title="您确认删除吗？"
                       :placement="'right'"
                       @on-ok="deleteCarts"
                       @on-cancel="">
              <a class="m-l-10 ys-error-color"><i class="ys-icon icon-trash"></i></a>
            </ys-poptip>
          </p>
          <div class="textR">
            已选 <span class="ys-error-color">{{tableSel.length}}</span> 个服务, 总计:  <loading-mini :show.sync="loadMiniStatus"></loading-mini><span class="ys-error-color font14" v-if="!loadMiniStatus">{{totalFee}}</span> 元 <button class="ys-btn m-l-20" @click="submitOrder()">提交订单</button>
          </div>
        </div>
        <modal :show.sync="payAlert" :title="'请在新打开的页面中完成付款'" :width="'400'">
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
            <button class="ys-btn ys-btn-white" type="button" @click="payError">
              <span>支付遇到问题</span>
            </button>
          </div>
        </modal>
      </div>
    </div>
    <div class="box-right" style="width:250px">
      <div class="ys-box" style="min-height:500px">
        <p class="ys-box-title">
          <i class="ys-icon icon-help-circle m-r-5"></i>您可能遇到的问题
        </p>
        <div class="question-box">
          <p>1.同一个购买对象，同一时间只能购买一种服务。</p>
          <p>2.同一购买对象后添加到购物车中的记录会覆盖前一条记录。</p>
          <p>3.如果您想对同一购买对象既新购服务又续费，请先完成新购服务支付后再进行续费。续费价格将按新套餐价格支付。</p>
        </div>
      </div>
    </div>
    <modal :show.sync="orderAlert" :title="'订单信息'" :width="'450'">
      <div slot="content" class="clearfix">
        <p class="textC">
          <img src="../../assets/images/pay-success.png" class="verticalM" style="width:32px"/>
          <span class="verticalM m-l-10 font14">恭喜! 订单({{orderData.order_no}})提交成功.</span>
        </p>
        <p class="textC">(请在24小时内完成付款,超时会导致订单失效)</p>
        <table class="ys-table m-t-20">
          <tr class="odd" v-for="list in orderData.items">
            <td class="textL">{{list.detail}}</td>
            <td><span class="ys-error-color">{{list.fee}}</span> 元</td>
          </tr>
        </table>
        <p class="textR font14 m-t-10">合计: <span class="ys-error-color">{{orderData.total_fee}}</span> 元</p>
      </div>
      <div slot="footer">
        <button class="ys-btn m-r-10" type="button" @click="payOrder">
          <span>在线付款结算</span>
        </button>
        <button class="ys-btn ys-btn-white" type="button" @click="orderAlert=false">
          <span>稍后订单中心结算</span>
        </button>
      </div>
    </modal>
  </div>
</template>
<script>
  import Api from 'src/lib/api'
  import ysSelect from 'src/components/select.vue'
  import ysTable from 'src/components/table-data.vue'
  import modal from 'src/components/modal.vue'
  import ysPoptip from 'src/components/poptip.vue'
  import loadingMini from 'src/components/loading-mini.vue'
  import { changeCartNum } from 'src/lib/actions'
  export default {
    name: "shop-cart",
    vuex: {
      actions: {
        changeCartNum
      }
    },
    data() {
      return {
        tableUrl: '/api/purchase/shopping_cart/dts',
        tableList:[],
        tableSel:[],
        totalFee:0,
        timeData:[
          {id:1,name:"1个月"},{id:2,name:"2个月"},{id:3,name:"3个月"},{id:4,name:"4个月"},{id:5,name:"5个月"},{id:6,name:"6个月"},
          {id:7,name:"7个月"},{id:8,name:"8个月"},{id:9,name:"9个月"},{id:10,name:"10个月"},{id:11,name:"11个月"},{id:12,name:"12个月"},
        ],
        payAlert:false,
        orderAlert:false,
        orderData:{},
        loadMiniStatus: false,
      }
    },
    ready: function() {},
    methods:{
      changeTime(list){
        let data = {
          quantity:list.quantity_dict.id,
          unit:"months",
        }
        this.$http.put('/api/purchase/shopping_cart/'+list.id, data).then(function (response) {
          if (response.data.status == 200) {
            list.total_fee=response.data.data.total_fee;
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      deleteCart(id){
        this.$http.delete('/api/purchase/shopping_cart/'+id).then(function (response) {
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.tableRe();
            this.getCartNum();
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      CountCart(carts){
        this.loadMiniStatus=true
        let data = {
          cart_ids: carts
        }
        this.$http.post('/api/purchase/shopping_cart/count', data).then(function (response) {
          this.loadMiniStatus=false
          if (response.data.status == 200) {
            this.totalFee = response.data.data.total_fee;
          }else{
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        })
      },
      deleteCarts(){
        this.$root.loadStatus=true
        let cart_ids=[];
        for(let x in this.tableSel){
          cart_ids.push(this.tableSel[x].id);
        }
        let data={cart_ids:cart_ids}
        this.$http.delete('/api/purchase/shopping_cart', data).then(function (response) {
          this.$root.loadStatus=false
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.tableRe();
            this.getCartNum();
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      submitOrder(){
        if(this.tableSel.length==0){
          this.$root.alertError = true;
          this.$root.errorMsg = "请先选择"
        }else{
          this.$root.loadStatus=true
          let cart_ids=[];
          for(let x in this.tableSel){
            cart_ids.push(this.tableSel[x].id)
          }
          let data = {"cart_ids": cart_ids}
          this.$http.post('/api/purchase/shopping_cart/checkout', data).then(function (response) {
            this.$root.loadStatus=false
            if (response.data.status == 200) {
              this.tableRe();
              this.orderAlert=true;
              this.orderData=response.data.data;
              this.getCartNum();
            } else {
              this.$root.alertError = true;
            }
            this.$root.errorMsg = response.data.msg
          }, function (response) {
            Api.user.requestFalse(response,this);
          })
        }
      },
      payOrder(){
        this.orderAlert=false;
        this.payAlert=true;
        window.open(this.orderData.pay_url);
      },
      checkPay(){
        this.$http.post('/api/purchase/order/'+this.orderData.order_id+'/refresh').then(function (response) {
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
      paySuccess(){
        this.checkPay()
      },
      payError(){
        this.payAlert=false;
      },
      getCartNum(){
        this.$http.get({"url": "/api/purchase/shopping_cart", "timeout": 3000}).then(function (response) {
          if(response.status == 200){
            this.changeCartNum(response.data.data.total_num);
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      tableRe(){
        this.$refs.table.Re()
      },
    },
    computed: {
      allSelected:{
        get: function () {
          this.tableSel=[];
          for(let x in this.tableList){
            if(this.tableList[x].selected) {
              this.tableSel.push({
                id:this.tableList[x].id,
                fee:this.tableList[x].total_fee,
                unit:this.tableList[x].quantity_dict
              })
            }
          }
          if(this.tableList.length==0){
            return false
          }
          return this.tableList.reduce(function(prev, curr) {
            return prev && curr.selected;
          },true);
        },
        set: function (newValue) {
          this.tableList.forEach(function(list){
            list.selected = newValue;
          });
        }
      }
    },
    watch:{
      'tableSel': function(){
        this.totalFee=0;
        var carts = [];
        for(let x in this.tableSel){
          carts.push(Number(this.tableSel[x].id))
        }
        this.CountCart(carts)
      }
    },
    components: {
      ysTable,
      ysSelect,
      modal,
      ysPoptip,
      loadingMini,
    }
  }
</script>
