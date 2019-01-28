<template>
  <div>
    <div class="ys-con clearfix">
      <div class="col-md-6">
        <div class="ys-box work-tip">
          <div class="ys-box-title">
            <span>工单记录</span>
          </div>
          <div class="ys-box-con">
            <div class="logTab">
              <div class="timeline-2" id="user-recent" style="margin-left:10px;">
                <div>
                  <div class="time-item">
                    <div class="item-info">
                      <p><span class="self-color text-cursor">{{processData.ticket.user}}</span>&nbsp;&nbsp;&nbsp;创建工单</p>
                      <p>{{processData.ticket.title}}</p>
                      <p>{{processData.ticket.content}}</p>
                      <p>
                        <template v-for="img in processData.ticket.picture">
                          <img v-bind:src="img" @click="readImg(img)"/>
                        </template>
                      </p>
                      <p v-if="processData.ticket.picture.length>0" class="font12" style="margin-top:-3px;">
                        ( 点击查看大图 )
                      </p>
                      <div class="text-muted font12">提交时间: {{processData.ticket.create_time}}</div>
                    </div>
                  </div>
                  <div class="time-item" v-for="list in processData.ticket_hand">
                    <div class="item-info">
                      <p><span class="self-color text-cursor">{{list.user}}</span>{{list.msg}}<span class="self-color text-cursor">{{list.recv_user}}</span></p>
                      <p>{{list.content}}</p>
                      <div class="text-muted font12">提交时间: {{list.current_time}}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          </div>
      </div>
      <div class="col-md-6" style="min-height:400px;">
        <div class="m-l-20">
          <template v-if="target=='deal'">
            <div class="m-t-10">
              <span class="m-r-5">分配用户</span>
              <ys-select :option="userOption" :selected.sync="orderData.user" :width="200"></ys-select>
            </div>
            <div class="m-t-10">
              <span class="m-r-5">修改状态</span>
              <ys-select :option="statusOption" :selected.sync="orderData.status" :width="100"></ys-select>
            </div>
          </template>
          <div class="m-t-15">
            <div class="form-group">
              <label class="nofontw">回复内容:</label>
              <div>
                <textarea class="ys-input" style="width: 100%; height: 200px" v-model="orderData.content"></textarea>
              </div>
            </div>
          </div>
          <div><button class="ys-btn" @click="saveOrder">提交</button></div>
        </div>
      </div>
    </div>
    <ys-modal :show.sync="imgModal" :title="'查看图片'">
      <div slot="content">
        <p><img v-bind:src="curImgSrc" style="width:100%"/></p>
        <p class="textC m-t-10"><button class="ys-btn" @click="imgModal=false">关闭</button></p>
      </div>
    </ys-modal>
  </div>
</template>
<style scoped>
  .work-tip {
    margin-right: 20px;
    height:798px;
    overflow: hidden;
  }
  .work-order-box{border-radius: 5px;padding:15px;}
    .home-box {
    margin: 0 10px 10px 0;
  }
  .menu-box{
    padding:0 15px;
  }
  .menu-box .progress {
    background: #5f528f;
    margin-top:5px;
  }

  /* Time line 2 */
  .timeline-2 {
    border-left: 2px solid #3185db;
    position: relative;
  }

  .timeline-2 .time-item:after {
    background-color: #3185db;
    border-color: #ffffff;
    border-radius: 10px;
    border-style: solid;
    border-width: 2px;
    bottom: 0;
    content: '';
    height: 14px;
    left: 0;
    margin-left: -8px;
    position: absolute;
    top: 5px;
    width: 14px;
  }

  .time-item {
    border-color: #dee5e7;
    padding-bottom: 1px;
    position: relative;
  }

  .time-item:before {
    content: " ";
    display: table;
  }

  .time-item:after {
    background-color: #ffffff;
    border-color: #98a6ad;
    border-radius: 10px;
    border-style: solid;
    border-width: 2px;
    bottom: 0;
    content: '';
    height: 14px;
    left: 0;
    margin-left: -8px;
    position: absolute;
    top: 5px;
    width: 14px;
  }

  .time-item-item:after {
    content: " ";
    display: table;
  }

  .item-info {
    margin-bottom: 30px;
    margin-left: 15px;
  }

  .item-info p {
    margin-bottom: 10px !important;
  }
</style>
<script>
  import ysSelect from 'src/components/select.vue'
  import ysModal from 'src/components/modal.vue'
  export default {
    props: {
      order_id: {
        default: false
      },
      target: {
        default: 0
      }
    },
    computed: {
      role_type () {
        return this.$store.state.user.role_type
      },
    },
    data() {
      return {
        userOption: [],
        statusOption: [{id: 0, name: "未处理"}, {id: 1, name: "处理中"}, {id: 2, name: "已处理"}],
        curImgSrc:"",
        processData:{
          ticket:{
            picture:[]
          },
          ticket_hand:[]
        },
        orderData:{
          user: {id: '', name: ''},
          status: {id: '', name: ''},
          content:""
        },
        imgModal:false
      }
    },
    ready: function() {
      slimFunc()
      function slimFunc() {
        $('.logTab').slimScroll({
          height: '740px',
          position: 'right',
          size: "5px",
          color: '#cccccc',
          wheelStep: 5
        })
      }
    },
    methods:{
      getUserList(){
       this.$http.post('/api/ticket/users', {"all": 1}).then(function (response) {
          this.userOption = response.data.items
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      getOrderInfo(){
        this.$http.get('/api/ticket/'+this.order_id).then(function (response) {
          this.processData=response.data.data
          this.orderData.user = {
            id: this.processData.ticket.handeuser_id,
            name: this.processData.ticket.handeuser
          }
          var status_id = this.processData.ticket.status
          this.orderData.status = {
            id: status_id,
            name: this.statusOption[status_id].name
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },
      saveOrder(){
        let data= {
          user: this.orderData.user.id,
          status: this.orderData.status.id,
          content: this.orderData.content
        }
        this.$http.put('/api/ticket/'+this.order_id,data).then(function (response){
          if(response.data.status==200){
            this.$root.alertSuccess=true
            this.getOrderInfo()
          }else{
            this.$root.alertError=true
          }
          this.$root.errorMsg=response.data.msg
        },function(response){
          Api.user.requestFalse(response)
        })
      },
      readImg(src){
        this.curImgSrc=""
        this.imgModal=true
        this.curImgSrc=src
      },
    },
    watch: {
      order_id: function (val) {
        if(val!=""){
          this.getUserList();
          this.getOrderInfo();
          this.orderData={
            user: {id: '', name: ''},
            status: {id: '', name: ''},
            content:""
          }
        }else{
          return false
        }
      }
    },
    components: {
      ysSelect,
      ysModal
    }
  }
</script>
<style>
  .item-info img{width:100px;height:100px;margin-right:10px;cursor: pointer}
  #read-img img{width:100%;}
  #read-img-modal{background:none;border:none;padding:0px;}
</style>

