<template>
  <div class="ys-con pos-r">
    <div class="box-left" style="margin-right:260px;">
      <div class="ys-box-con  ys-wrap">
        <div class="ys-box-con bor-blue-dashed">
          <p class="ys-info-color">您可以在这里查询已经购买过的服务记录和开具发票的情况</p>
        </div>
        <div class="m-t-20">
          <table class="ys-table ys-table-center">
            <thead>
            <tr>
              <th>订单编号</th>
              <th>购买日期</th>
              <th>服务信息</th>
              <th>订单花费(元)</th>
              <th class="textC" style="width:120px">开具发票状态</th>
            </tr>
            </thead>
            <tbody>
            <tr class="odd" v-for="list in tableList">
              <td>{{list.order_no}}</td>
              <td>{{list.create_time}}</td>
              <td>{{list.detail}}</td>
              <td class="ys-error-color">{{list.total_fee}}</td>
              <td class="textC">
                <span class="ys-success-color" v-if="list.is_invoice==1">已开发票</span>
                <span class="ys-error-color" v-else>未开发票</span>
              </td>
            </tr>
            </tbody>
          </table>
          <ys-table
                  :url.sync='tableUrl'
                  :data.sync="tableList"
                  :filter.sync="tableFilter"
                  v-ref:table>
          </ys-table>
        </div>
      </div>
    </div>
    <div class="box-right" style="width:250px">
      <div class="ys-box">
        <div class="ys-box-title">申请发票</div>
        <div class="ys-box-con p-b-10">
          <div class="sel-buy-box">
            <div class="sel-buy-list">
              <p class="font24">
                <img src="../../assets/images/invoice.png" style="width:34px;"/>
              </p>
            </div>
          </div>
          <div class="m-t-20">
            <table class="ys-form-table">
              <tr>
                <td class="ys-info-color">可开发票金额:</td>
                <td><span class="font14 ys-error-color">{{invoicePrice}}</span>元</td>
              </tr>
              <tr>
                <td class="ys-info-color">发票类型:</td>
                <td>增值税普通发票</td>
              </tr>
              <tr>
                <td class="ys-info-color">发票抬头:</td>
                <td><radio :list="radioData" :value.sync="invoiceData.i_type"></radio></td>
              </tr>
            </table>
            <p v-bind:class="[invoiceData.i_type==1 ? 'disabled' : '' ]">
              <input class="ys-input fullWidth"
                     v-model="invoiceData.title"/>
            </p>
            <p class="m-t-10 ys-info-color">邮寄地址:</p>
            <p><input class="ys-input m-t-5 fullWidth" v-model="invoiceData.address"/></p>
            <p class="m-t-10 ys-info-color">邮政编码:</p>
            <p><input class="ys-input m-t-5 fullWidth" v-model="invoiceData.post"/></p>
            <p class="m-t-10 ys-info-color">联系方式(手机):</p>
            <p><input class="ys-input m-t-5 fullWidth" v-model="invoiceData.phone"/></p>
            <p class="m-t-10 ys-info-color">收件人:</p>
            <p><input class="ys-input m-t-5 fullWidth" v-model="invoiceData.account"/></p>
          </div>
        </div>
      </div>
      <div class="buy-split-box">
        <div class="buy-split-box-bottom"></div>
        <div class="buy-split-box-line"></div>
        <div class="buy-split-box-top"></div>
      </div>
      <div class="ys-box">
        <div class="ys-box-con p-t-10 p-l-10 p-r-10">
          <div class="textC">
            <button class="ys-btn" @click="goInvoice()">将未开具发票的服务合并申请发票</button>
          </div>
        </div>
      </div>
      <div class="ys-jag-box">
        <span v-for="n in 24"></span>
        <span class="final"></span>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .sel-buy-box{
    display: table;
    margin:0px auto;
  }
  .sel-buy-list{
    width:70px;
    height:70px;
    border:2px solid #f2f2f2;
    text-align: center;
    border-radius: 50%;
    display: table-cell;
    vertical-align: middle;
  }
</style>
<script>
  import Api from 'src/lib/api'
  import ysSelect from 'src/components/select.vue'
  import ysTable from 'src/components/table-data.vue'
  import modal from 'src/components/modal.vue'
  export default {
    name: "invoice-mgt",
    data() {
      return {
        tableUrl: '/api/purchase/order/dts',
        tableList:"",
        tableFilter: {
          status: {"id": "1", "name": "1" },
        },
        invoiceData:{
          type:1,
          i_type:2,
          title:"",
          address:"",
          post:"",
          account:"",
          phone:""
        },
        invoicePrice:0,
        radioData:[
          {id:1,text:"个人"},
          {id:2,text:"公司"},
        ],
      }
    },
    ready: function() {
      this.getInvoicePrice()
    },
    computed: {

    },
    methods:{
      getInvoicePrice(){
        this.$http.get('/api/purchase/invoice', this.invoiceData).then(function (response) {
          if (response.data.status == 200) {
            this.invoicePrice=response.data.data.total_fee;
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      changeType(type){
        this.invoiceData.i_type=type;
        if(this.invoiceData.i_type==1){
          this.invoiceData.title="";
        }
      },
      goInvoice(){
        if(this.tableList.length>0){
          this.$http.post('/api/purchase/invoice', this.invoiceData).then(function (response) {
            if (response.data.status == 200) {
              this.$root.alertSuccess = true;
              this.$refs.table.Re();
            } else {
              this.$root.alertError = true;
            }
            this.$root.errorMsg = response.data.msg
          }, function (response) {
            Api.user.requestFalse(response,this);
          })
        }else{
          this.$root.alertError = true;
          this.$root.errorMsg="当前没有可以开具发票的订单";
        }

      }
    },
    watch:{},
    components: {
      ysSelect,
      ysTable,
      modal
    }
  }
</script>
