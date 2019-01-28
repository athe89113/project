<template>
  <!-- Page-Title -->
  <div class="row">
    <div class="col-sm-12">
      <h4 class="page-title">soc代理管理</h4>
      <ol class="breadcrumb">
        <li>
          <a href="#">系统管理</a>
        </li>
        <li>
          <a href="#">soc代理管理</a>
        </li>
        <li class="active">
          代理列表
        </li>
      </ol>
    </div>
  </div>

  <div class="panel">

    <div class="panel-body">
      <div class="row">
        <!-- Start add modal -->
        <div id="add-soc-agent" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
             aria-hidden="true" style="display: none;">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <h4 class="modal-title">添加soc代理</h4>
              </div>
              <div class="modal-body">
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-agent-select" class="control-label">代理商<span class="mustInput">*</span></label>
                      <input type="text" class="form-control" id="add-agent-select" placeholder="代理商"
                             v-model="addSocAgentAgent">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-idc-select" class="control-label">所属IDC<span class="mustInput">*</span></label>
                      <input type="text" class="form-control" id="add-idc-select" placeholder="所属IDC"
                             v-model="addSocAgentIdc">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12">
                    <div class="form-group">
                      <label for="add-soc-agent-name" class="control-label">代理名字<span class="mustInput">*</span></label>
                      <input type="text" class="form-control" id="add-soc-agent-name" placeholder="代理名字"
                             v-model="addSocAgentName">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-soc-agent-ip" class="control-label">IP地址<span class="mustInput">*</span></label>
                      <input type="text" class="form-control" id="add-soc-agent-ip" placeholder="IP地址"
                             v-model="addSocAgentIp">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-soc-agent-port" class="control-label">端口<span class="mustInput">*</span></label>
                      <input type="text" class="form-control" id="add-soc-agent-port" placeholder="端口"
                             v-model="addSocAgentPort">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-soc-agent-mask" class="control-label">掩码地址<span class="mustInput">*</span></label>
                      <input type="text" class="form-control" id="add-soc-agent-mask" placeholder="掩码地址"
                             v-model="addSocAgentMask">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-soc-agent-gateway" class="control-label">网关地址<span class="mustInput">*</span></label>
                      <input type="text" class="form-control" id="add-soc-agent-gateway" placeholder="网关地址"
                             v-model="addSocAgentGateway">
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-white waves-effect" data-dismiss="modal">取消</button>
                <button type="button" class="btn btn-default waves-effect waves-light" @click="addSocAgentButton">保存</button>
              </div>
            </div>
          </div>
        </div>
        <!-- end add modal -->
        <div id="edit-soc-agent" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
             aria-hidden="true" style="display: none;">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <h4 class="modal-title">编辑soc代理</h4>
              </div>
              <div class="modal-body">
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-agent-select" class="control-label">代理商</label>
                      <input type="text" class="form-control" id="edit-agent-select" placeholder="代理商" disabled="disabled"
                             v-model="editSocAgentAgent">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-idc-select" class="control-label">所属IDC</label>
                      <input type="text" class="form-control" id="edit-idc-select" placeholder="所属IDC" disabled="disabled"
                             v-model="editSocAgentIdc">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-12">
                    <div class="form-group">
                      <label for="add-soc-agent-name" class="control-label">代理名字</label>
                      <input type="text" class="form-control" id="edit-soc-agent-name" placeholder="代理名字"
                             v-model="editSocAgentName">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-soc-agent-ip" class="control-label">IP地址</label>
                      <input type="text" class="form-control" id="edit-soc-agent-ip" placeholder="IP地址"
                             v-model="editSocAgentIp">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-soc-agent-port" class="control-label">端口</label>
                      <input type="text" class="form-control" id="edit-soc-agent-port" placeholder="端口"
                             v-model="editSocAgentPort">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-soc-agent-mask" class="control-label">掩码地址</label>
                      <input type="text" class="form-control" id="edit-soc-agent-mask" placeholder="掩码地址"
                             v-model="editSocAgentMask">
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="add-soc-agent-gateway" class="control-label">网关地址</label>
                      <input type="text" class="form-control" id="edit-soc-agent-gateway" placeholder="网关地址"
                             v-model="editSocAgentGateway">
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-white waves-effect" data-dismiss="modal">取消</button>
                <button type="button" class="btn btn-default waves-effect waves-light" @click="editSocAgentButton">保存</button>
              </div>
            </div>
          </div>
        </div>

        <div class="col-sm-12">
          <div class="m-b-15">
            <button id="addToTable" class="btn btn-default waves-effect waves-light" data-toggle="modal"
                    data-target="#add-soc-agent" @click="addSOcAgentReset">添加soc代理 <i class="fa fa-plus"></i></button>
          </div>
        </div>
        <!-- table 标题-->
        <div class="col-sm-12">
          <div class="card-box">
            <table id="datatable" class="table table-striped table-bordered">
              <thead>
              <tr>
                <th>代理名字</th>
                <th>IP地址</th>
                <th>端口</th>
                <th>掩码地址</th>
                <th>网关地址</th>
                <th>存活状态</th>
                <th>上次心跳</th>
                <th>IDC</th>
                <th>代理商</th>
                <th>主次</th>
                <th>操作</th>
              </tr>
              </thead>
              <tbody></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <!-- end: page -->

  </div>
  <!-- end Panel -->
</template>
<script>
  require('datatables.net')
  require('../assets/css/jquery.dataTables.min.css')
  require('dataTables.bootstrap')
  require('select2')
  require('select2.lang')
  import Api from '../lib/api'
  export default {
    data() {
      return {
        curIpsEditId:'',
        addSocAgentAgent: '',
        addSocAgentName: '',
        addSocAgentPort: '',
        addSocAgentIp:'',
        addSocAgentMask:'',
        addSocAgentGateway:'',
        addSocAgentIdc:'',

        editSocAgentAgent: '',
        editSocAgentName: '',
        editSocAgentPort: '',
        editSocAgentIp:'',
        editSocAgentMask:'',
        editSocAgentGateway:'',
        editSocAgentIdc:'',
      }
    },
    ready: function() {
      var self=this;
      var itemsPerpage=15;
      var datatable_el = $('#datatable');
      var table = datatable_el.DataTable({
        "ajax": {
          "url": "/api/soc_agent/dts",
          "type": "POST"
        },
        "order": [[1, 'asc']],
        "processing": true,
        "serverSide": true,
        "oLanguage": {
          "sLengthMenu": "每页显示 _MENU_ 条记录",
          "sZeroRecords": "对不起，查询不到任何相关数据",
          "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录",
          "sInfoEmtpy": "找不到相关数据",
          "sInfoFiltered": "数据表中共为 _MAX_ 条记录)",
          "sProcessing": "正在加载中...",
          "sSearch": "搜索: ",
          "sUrl": "", //多语言配置文件，可将oLanguage的设置放在一个txt文件中，例：Javascript/datatable/dtCH.txt
          "oPaginate": {
            "sFirst": "第一页",
            "sPrevious": " 上一页 ",
            "sNext": " 下一页 ",
            "sLast": " 最后一页 "
          }
        }, //多语言配置
        "columnDefs": [
          {
            "data": "id",
            "render": function (data, type, row) {
              return '<a data-toggle="modal" class="btn btn-default waves-effect waves-light edit" id="edit_' + data + '" role="button" href="#edit_modal">编辑</a>' +
                      ' <a data-toggle="modal" class="btn btn-danger waves-effect waves-light delete" id="del_' + data + '" href="#delete_modal_' + data + '">删除</a>';
            },
            "targets": 10
          }
        ],
        "columns": [
          {"data": 'name'},
          {"data": 'ip'},
          {"data": 'port'},
          {"data": 'mask'},
          {"data": 'gateway'},
          {"data": 'status'},
          {"data": 'last_heartbeat'},
          {"data": 'idc'},
          {"data": 'agent'},
          {"data": 'master'},
        ]
      });
      var $addSocAgentAgent=$('#add-agent-select').select2({
        placeholder: '选择代理商',
        ajax: {
          url: "/api/agent/list",
          type: "POST",
          dataType: 'json',
          quietMillis: 250,
          data: function(term, page) {
            return {
              q: term,
              page: page,
              page_size: itemsPerpage
            };
          },
          results: function(data, page ) {
            var more = (page * itemsPerpage) < data.total_count;
            return { results: data.items, more: more };
          }
        },
        formatResult: function(items) {
          return "<div class='select2-user-result'>" + items.name + "</div>";
        },
        formatSelection: function(items) {
          return "<div class='select2-user-result'>" + items.name + "</div>";
        }
      });
      var $addSocAgentIdc=$('#add-idc-select').select2({
        placeholder: '选择代理商',
        ajax: {
          url: "/api/agent_idc/list",
          type: "POST",
          dataType: 'json',
          quietMillis: 250,
          data: function(term, page) {
            return {
              q: term,
              page: page,
              page_size: itemsPerpage,
              agent_id: self.addSocAgentAgent
            };
          },
          results: function(data, page ) {
            var more = (page * itemsPerpage) < data.total_count;
            return { results: data.items, more: more };
          }
        },
        formatResult: function(items) {
          return "<div class='select2-user-result'>" + items.name + "</div>";
        },
        formatSelection: function(items) {
          return "<div class='select2-user-result'>" + items.name + "</div>";
        }
      });
      function resetEditForm(){
        self.editSocAgentAgent="";
        self.editSocAgentName="";
        self.editSocAgentPort="";
        self.editSocAgentIp="";
        self.editSocAgentMask="";
        self.editSocAgentGateway="";
        self.editSocAgentIdc="";
        $('#edit-agent-select').select2("data","");
        $('#edit-idc-select').select2("data","");
      }
      $('#datatable').find('tbody').on('click', 'td a.edit', function () {
        resetEditForm();
        var tr = $(this).closest('tr');
        var curListId = $(this).attr('id').replace("edit_","");
        self.curIpsEditId=curListId;
        self.$http.get('/api/soc_agent/'+curListId).then(function (response){
          self.curSocAgentData=response.data.data[0];
          var curSocAgentData = self.curSocAgentData;
          self.editSocAgentAgent=curSocAgentData.agent.name;
          self.editSocAgentName=curSocAgentData.name;
          self.editSocAgentPort=curSocAgentData.port;
          self.editSocAgentIp=curSocAgentData.ip;
          self.editSocAgentMask=curSocAgentData.mask;
          self.editSocAgentGateway=curSocAgentData.gateway;
          self.editSocAgentIdc=curSocAgentData.idc.name;
          $('#edit-soc-agent').modal();
        },function(response){
          Api.user.requestFalse(response,this);
        })
      });
      $('#datatable').find('tbody').on('click', 'td a.delete', function () {
        var tr = $(this).closest('tr');
        var curListId = $(this).attr('id').replace("del_","");
        self.$http.delete('/api/soc_agent/'+curListId).then(function (response){
          if(response.data.status==200){
            $('#datatable').DataTable().ajax.reload();//重新加载表格
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      });


    },
    methods:{
      addSocAgentButton(){
        $('#add-soc-agent').modal('hide');//关闭弹窗
        let data = {
          name: this.addSocAgentName,
          ip: this.addSocAgentIp,
          port: this.addSocAgentPort,
          mask: this.addSocAgentMask,
          gateway:this.addSocAgentGateway,
          idc_id: this.addSocAgentIdc,
        };
        this.$http.post('/api/soc_agent',data).then(function (response){
          if(response.data.status==200){
            this.successMsg = response.data.msg + " 密钥: " + response.data.data;
            swal(this.successMsg, "", "success");
            $('#datatable').DataTable().ajax.reload();//重新加载表格
          }else if(response.data.status==500) {
            this.errorMsg = response.data.msg;
            $('#error').modal();
          }else{
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },//添加保存按钮
      editSocAgentButton(){
        $('#edit-soc-agent').modal('hide');//关闭弹窗
        let data = {
          name: this.editSocAgentName,
          ip: this.editSocAgentIp,
          port: this.editSocAgentPort,
          mask: this.editSocAgentMask,
          gateway:this.editSocAgentGateway,
        };
        this.$http.put('/api/soc_agent/'+this.curIpsEditId,data).then(function (response){
          if(response.data.status==200){
            $('#datatable').DataTable().ajax.reload();//重新加载表格
          }else if(response.data.status==500) {
            this.errorMsg = response.data.msg;
            $('#error').modal();
          }else{
          }

        },function(response){
          Api.user.requestFalse(response,this);
        })
      },//添加保存按钮
      addSOcAgentReset(){
        this.addSocAgentName="";
        this.addSocAgentIp="";
        this.addSocAgentPort="";
        this.addSocAgentMask="";
        this.addSocAgentGateway="";
        this.addSocAgentIdc="";
        $("#add-agent-select").select2("data","");
        $("#add-idc-select").select2("data","");
      }
    }

  }
</script>

