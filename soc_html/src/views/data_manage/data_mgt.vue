<template>
  <div class="ys-con pos-r" @mouseenter="tabFromWidth()" v-if="preview">
      <div class="pageHead">
        <p class="pageTitle"><span>数据管理 </span>- 数据管理</p>
      </div>
      <div class="pos-r ys-info-title">
          <div class="tool-box">
              <button class="ys-btn m-l-5" @click="newFile">
                <i class="ys-icon icon-add-circle"></i>创建新文件夹
              </button>
              <div class="fRight d-i-b">
									<a class="m-r-5" href="javascript:;" @click="tabFrom(false)"><i class="ys-icon icon-topbar-more"></i></a>
									<a class="m-r-5" href="javascript:;" @click="tabFrom(true)">
                    <i class="ys-icon icon-list-display"></i>
                  </a>
									<a class="m-r-5" href="javascript:;" @click="sort('change_time')">
                    <i class="ys-icon icon-time-sort" :class="classTime"></i>
                  时间</a>
									<a class="m-r-5" href="javascript:;" @click="sort('name')">
                    <i class="ys-icon icon-name-sort" :class="className"></i>
                  名称</a>
									<div class="ys-search d-i-b m-l-10">
									<input type="text" placeholder="输入关键词查询"
													v-model="searchValue"
													@keyup.enter="tableRe()"
													class="ys-input" style="width:180px;"/>
									<button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
									</div>
							</div>
          </div>
          <div class="m-t-10">
            <span class="m-l-5">
              <span>当前目录共有</span>
              <span class="ys-warn-color">{{recordsTotal}}</span> 个文件夹
              <span>|</span>
              <span class="ys-success-color">{{count}}</span> 个数据表
              <a class="m-r-5" v-for="item in tableS" :key="$index" @click="goback(item.path,$index)">
                <span v-if="$index!=0">></span>
                {{item.name}}
              </a>
            </span>
          </div>
          <template v-if="TabForm">
					<table class="ys-table ys-table-bor m-t-10 ys-table-center">
						<thead>
							<tr>
								<th></th>
								<th class="text-left">文件夹名称  
                  <i @click="sort('name')" class="ys-icon icon-name-sort" :class="className"></i>
                </th>
								<th>数据标签</th>
								<th>修改时间</th>
								<th>大小</th>
								<th>所属用户</th>
								<th>所属组</th>
								<th style="width:160px;" class="textC">操作</th>
							</tr>
						</thead>
          	<tbody>
              <tr v-for="list in tableList" :key="list">
                <td class="check operate left">
                  <checkbox v-if="(!list.lock)&&list.type=='file'" :show.sync="list.selected"></checkbox>         
                </td>       
                <td v-if="editId===list.id" class="text-left"> 
                  <input type="text" class="ys-input" v-model="newName" 
                    autofocus="autofocus"
                    @keyup.enter="removeFile(list,false)">
                </td> 
                <td class="cursor text-left" v-else @click.stop="tableGoto(list)">
                  <a href="javascript:;" v-if="list.type=='file'" >
                    <i class="ys-icon icon-work-list"></i>
                  </a>
                  <a v-else href="javascript:;">
                    <i v-if="list.lock" class="ys-icon icon-file-lock"></i>
                    <i v-else class="ys-icon icon-file-edit"></i>
                  </a>
                  {{list.name}}
                </td>
                <td>{{list.tag}}</td>
                <td>{{list.change_time}}</td>
                <td>{{list.size|filterFun}}</td>
                <td>{{list.owner}}</td>
                <td>{{list.group}}</td>
                <td class="textC operate"  v-if="editId===list.id">
                  <tooltip :content="'取消'">
                    <a @click="removeFile(list,true)"><i class="glyphicon glyphicon-remove text-cursorr"></i></a>
                  </tooltip>
                  <tooltip :content="'确定'">
                    <a @click="removeFile(list,false)"><i class="glyphicon glyphicon-ok text-cursor"></i></a>
                  </tooltip>
                </td>
                <td class="textC operate" v-else>
                  <template v-if="!list.lock">
                    <tooltip :content="'文件下载'" v-if="list.type  =='file'">
                      <a @click="download(list)"><i class="ys-icon icon-cloud-download"></i></a>
                    </tooltip>
										<a v-else class="m-r-15">--</a>
                    <tooltip :content="'修改名称'">
                      <a @click="EditName(list)"><i class="ys-icon icon-edit"></i></a>
                    </tooltip>				
                    <ys-poptip confirm
                              title="您确认删除这条内容吗？"
                              :placement="'left'"
                              @on-ok="deleteFile(list)">
                      <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
                    </ys-poptip>
                  </template>
                </td> 
              </tr> 
						</tbody>
					</table>
          <div class="ys-row cart-table-foot" v-if="tableList.length>0&&curPath!=''">
            <p>
              <checkbox :text="'全选'"
                        :show="allSelected"
                        class="m-r-20"
                        :auto-set="false"
                        @ys-click="allSelected=!allSelected"></checkbox>
              <ys-poptip confirm
                        title="您确认删除已选内容吗？"
                        :placement="'left'"
                        @on-ok="deleteFileAll(list)">
                <a class="ys-error-color m-l-5"><i class="ys-icon icon-trash"></i></a>
              </ys-poptip>
            </p>
          </div>
					<table-data :url='tableUrl'
                      :data.sync="tableList"
                      :whole.sync="tableTotal"
                      :filter.sync="tableFilter"
                      :search.sync="searchValue"
                      v-ref:table>
          </table-data>
          </template>
					<div v-else class="tableFile">
						<ul>
							<li v-for="list in tableList" @mouseenter="move(list)" @mouseleave ="moveId=0">
                <div v-if="moveRome(list)" class="showSet">
                  <div class="check32">
                    <checkbox class="m-10" v-if="(!list.lock)&&list.type=='file'" :show.sync="list.selected"></checkbox>
                  </div>
                  <div class="type-box">
                    <div class="sign textC cursor" @click="fileGoto(list)">
                      <a href="javascript:;" v-if="list.type=='file'" >
                        <img class="imgF" src="../../assets/images/dama/work-list.png" alt="">
                      </a>
                      <a v-else href="javascript:;">
                        <img v-if="list.lock" class="img" src="../../assets/images/dama/file-default.png" alt="">
                        <img v-else class="img" src="../../assets/images/dama/file-edit.png" alt="">            
                      </a>              
                    </div>
                    <div>	
                      <p v-if="editId===list.id" class="textC inherit p-t-5 m-b-5">
                        <input type="text" class="ys-input" v-model="newName"
                        autofocus="autofocus"
                        @keyup.enter="removeFile(list,false)">
                      </p>
                      <p v-else class="textC inherit p-t-5 cursor threeDot" @click="fileGoto(list)">{{list.name}}</p>
                    </div>	
                    <div class="textC operate" v-if="editId===list.id">
                      <button @click="removeFile(list,false)" class="ys-btn ys-btn-s m-l-10 m-r-10">确认</button>
                      <button @click="removeFile(list,true)" class="ys-btn ys-btn-s ys-btn-white m-r-10">取消</button>
                    </div>
                    <div class="btns" v-else>
                      <template v-if="!list.lock">
                        <tooltip :content="'文件下载'" v-if="list.type=='file'">
                          <a @click="download(list)" class="m-5"><i class="ys-icon icon-cloud-download"></i></a>
                        </tooltip>
                        <tooltip :content="'编辑配置'">
                          <a @click="EditName(list)" class="m-5"><i class="ys-icon icon-edit"></i></a>
                        </tooltip>	
                        <ys-poptip confirm
                                  title="您确认删除这条内容吗？"
                                  :placement="$index%difference==0?'right':'left'"
                                  @on-ok="deleteFile(list,$index)">
                          <a class="ys-error-color m-5"><i class="ys-icon icon-trash"></i></a>
                        </ys-poptip>
                      </template>
                    </div>               
                  </div>
                </div>
                <div v-else>
                  <div class="check32"></div>
                  <div class="type-box">
                    <div class="sign textC cursor" @click="fileGoto(list)">
                      <a href="javascript:;" v-if="list.type=='file'" >
                        <img class="imgF" src="../../assets/images/dama/work-list.png" alt="">     
                      </a>
                      <a v-else href="javascript:;">
                        <img v-if="list.lock" class="img" src="../../assets/images/dama/file-default.png" alt="">
                        <img v-else class="img" src="../../assets/images/dama/file-edit.png" alt="">            
                      </a>              
                    </div>
                    <div>	
                      <p v-if="editId===list.id" class="textC inherit p-t-5 m-b-5">
                        <input type="text" class="ys-input" v-model="newName"
                        autofocus="autofocus"
                        @keyup.enter="removeFile(list,false)">
                      </p>
                      <p v-else class="textC inherit p-t-5 cursor threeDot" @click="fileGoto(list)">{{list.name}}</p>
                    </div>	            
                  </div>
                </div>
							</li>
						</ul>
            <div class="ys-row all" v-if="tableList.length>0&&curPath!=''">
              <p>
                <checkbox :text="'全选'"
                          :show="allSelected"
                          class="m-r-20"
                          :auto-set="false"
                          @ys-click="allSelected=!allSelected"></checkbox>
                <ys-poptip confirm
                          title="您确认删除已选内容吗？"
                          :placement="'left'"
                          @on-ok="deleteFileAll(list)">
                  <a class="ys-error-color m-l-5"><i class="ys-icon icon-trash"></i></a>
                </ys-poptip>
              </p>
            </div>
					</div>
      </div>
      <loading-global :show.sync="loadGlobal"></loading-global>
  </div>
  <div v-else>
    <div class="ys-con pos-r" v-if="loadTable">
      <div class="m-b-10">
        <button class="ys-btn ys-btn-blue"  @click="backData_mgt()">返回数据列表</button>
      </div>
      <div class="ys-box-title">
        显示最新10条数据，共{{Precount}}条数据
        [最新更新时间：{{newestTime}}]  
      </div>
      <div class="ys-box-con rule-run-result-box m-t-10">
        <div class="custom-table data-preview" style="width:100%;height:480px;" id="rule-run-result-table">
          <table class="ys-table">
            <thead>
              <tr>
                <th v-if="PreresultHeader.length==0"></th>
                <th v-for="head in PreresultHeader">{{head}}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in PreresultData">         
                <td v-for="col in row" track-by="$index" class="text-l operate" nowrap="nowrap">{{col}}</td>
              </tr>
            </tbody>
          </table>
          <table-data v-if="loadTable" :url='PretableUrl'
          :data.sync="PreresultData"
          :whole.sync="PretableTotal"
          :filter.sync="PretableFilter"
          :search.sync="PresearchValue"
          v-ref:table>
          </table-data>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.inherit{
  color: inherit;
}
.tableFile{
  margin-top:20px;
}
.tableFile ul::after{
  content: '';
  clear: both;
  height: 0;
  display: block;
}
.tableFile ul>li{
	float: left;
	height: 140px;
	width: 140px;
  position: relative;
	margin-right: 10px;
  margin-bottom: 10px;
}
.tableFile ul>li .showSet{
  position: relative;
  height: 100%;
	background: rgba(0,0,0,0.2);
  border-radius: 5px;
}
.btns{
  position: absolute;
  right: 5px;
  bottom: 10px;
}
.all{
  padding: 10px;
}
.check32{
  height: 30px;
}
.cursor{
  cursor: pointer;
}
.ys-table tr th.text-left,.ys-table tr td.text-left{
  text-align: left;
}
.ys-icon.icon-file-edit::before{
  color: #DABB61;
  width: 22px;
  height: 20px;
}
.ys-icon.icon-work-list::before{
  color: #00BD85;
  width: 20px;
  height: 23px;
}
.ys-table tr td.operate.left{
  text-align:left;
  padding: 0px 12px;
  width: 7%;
}
.img{
  height: 48px;
  width: 56px;
}
.imgF{
  height: 57px;
  width: 44px;
}
.flipy{
  -moz-transform:scaleY(-1);
  -webkit-transform:scaleY(-1);
  -o-transform:scaleY(-1);
  transform:scaleY(-1);
}

</style>
<script>
import Api from 'src/lib/api'
import loadingGlobal from 'src/components/loading-global.vue'
export default {
  name: "data-manage",
  components: {
    loadingGlobal
  },
  data () {
      return {
        moveId: 1,
        editId: 0,
        preview: true,
        newName:'',
        editName: '',
        searchValue:'',
        recordsTotal: '',
        count:'',
        TabForm:false,
        loadGlobal:false,
        difference:0,
        order_type: "asc",
        curPath: "",
        tableUrl: "/api/ssa/file_manage/dts",
        tableFilter: {
          "path": {id: "", name: ""},
          //"order": {id: "change_time", name: "change_time"},
          //"order_type": {id: "desc", name: "desc"},
        },
        tableTotal:0,
        tableList:[],
        tableS:[{
          name:"全部文件",
          path: '/'
        }],
        classTime:{
          'flipy': false
        },
        className:{
          'flipy': false
        },
        //preview
        PretableUrl: '/api/ssa/file_manage/preview/dts',
        PretableFilter: {
          "path": {id: "", name: ""}
        },
        PretableTotal:10,
        newestTime:'',
        Precount: '',
        PresearchValue:'',
        loadTable:false,
        PreresultData: [],
        PreresultHeader: []
    }
  },
  computed: {
    allSelected:{
      get: function () {
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
  filters: {  
    filterFun: function (value) {  
      if(value>1024){
        let kb = parseInt(value/1024);
        if(kb>1024){
          let mb = parseInt(kb/1024);
          return mb+"MB"
        }else{
          return kb+"KB"
        }     
      }else{
        if(value==0){
          return '--'
        }else{
          return value+"B"
        }
        
      }
    }  
  },
  ready () {  
    this.getData(this.curPath,'desc','change_time')
  },
	methods:{
    getData (path,order_type='',name='') {
      this.$http.post('/api/ssa/file_manage/dts', {
       "path": path,
       "order": name,
       "search": this.searchValue,
       "order_type": order_type
       }).then(function (response) {
        
        let res = response.data;
        this.count = res.recordsTotal -res.dir_count;
        this.recordsTotal = res.recordsTotal;
        this.tableList = res.data;
        this.loadGlobal = false
      })
    },
    getDataPreview (filepath){ 
      this.$http.post('/api/ssa/file_manage/preview/dts', {
        "path": filepath,
        "start": 0,
        "length":10
      }).then(function (response) {
        let res = response.data;
        if (res.status == 200) {
          this.Precount = res.recordsTotal 
          this.PreresultHeader = res.headers
          this.$root.alertSuccess = true;
          this.$root.errorMsg = response.data.msg
          setTimeout(function(){
            $("#rule-run-result-table").niceScroll({
              cursorborder: "1px solid rgba(0,0,0,0)",
              autohidemode:false,
              cursorwidth: "7px",
              cursorcolor:"rgba(74,146,255,0.3)"
            });
          },2000)
        } else {
          this.$root.alertError = true;
          this.$root.errorMsg = response.data.msg
        }
      })
    },
		newFile () {
      if(this.editId===1){
        return false
      }
			this.newName = '';
			let file = {
          id: 1,
          newFile:true,
          name:'',
          size: 0
			}
      this.editId = 1;
			this.tableList.unshift(file)
    },
    goback (curPath,tabIndex) {
      if(this.editId===1) return false
      let index = curPath.lastIndexOf('/');
      this.tableS.splice(tabIndex+1)
      this.curPath = curPath 
      this.loadGlobal = true
      if(this.TabForm){
        this.tableFilter.path = {id: curPath, name: curPath}
        this.tableRe()
      }else{
        this.getData(curPath)
      }  
    },
    backData_mgt (){
      this.preview = true
      this.loadGlobal = false
    },
    gotoPreview (item) {
      if(item.type=="file"){
        this.preview = false;
        this.loadTable = true
        this.newestTime = item.change_time
        this.PretableFilter= {
          "path": {id: item.path, name: item.path}
        }
      this.getDataPreview (item.path) 
      }
    },
    setScroll(){
      $(".tableFile ul").slimScroll({
        height: window.screen.height -380,
        alwaysVisible: true,
      });
    },
    tabFromWidth () {
      let tabWidth = $(".tableFile ul").width();
      let liWidth = $(".tableFile li").outerWidth(true);
      this.difference = parseInt(tabWidth/liWidth);
      this.setScroll()  
    },
    move (item) {
      this.moveId = item.id
    },
    moveRome (list) {
      if(list.id===this.moveId){
        return true
      }else if(list.selected&&list.type=="file"){
        return true
      }else{
        return false
      }
    },
    sort (str) {  
      if(str=="name"){
        this.className.flipy == true?this.className.flipy=false:this.className.flipy=true
      }else if(str=="change_time"){
        this.classTime.flipy == true?this.classTime.flipy=false:this.classTime.flipy=true
      }
      this.order_type=='asc'?this.order_type='desc':this.order_type='asc';
      if(this.TabForm){
        this.tableList = []
        this.tableFilter = {
          "path": {id: this.curPath, name: this.curPath},
          "order": {id: str, name: str},
          "order_type": {id: this.order_type, name: this.order_type},
        }
        this.$refs.table.Re()
        this.loadGlobal = false
      }else{
        this.$http.get('/api/ssa/file_manage/dts', {
        "path": this.curPath,
        "order": str,
        "search": '' ,
        "order_type": this.order_type
        }).then(function (response) {
          let res = response.data;
          this.tableList = res.data;
          this.count = res.recordsTotal -res.dir_count;
          this.recordsTotal = res.recordsTotal;
        })
      }
    },
    tabFrom (bl) {
      if(bl){
        this.TabForm = true
        this.tableFilter.path = {id: this.curPath, name: this.curPath}
      }else{
        this.TabForm = false 
        this.loadGlobal = true
        this.getData(this.curPath,'desc','change_time')
      }
      this.editId = 0;
    },
    tableClass(item){
      let index = item.path.lastIndexOf('/');
      let className = item.path.substring(index+1);
      let objectItem = {
        name: className,
        path: item.path
      };
      this.tableS.push(objectItem)    
    },
		tableGoto (item) {
      if(this.editId===1) return false
      this.gotoPreview(item)
      if(item.type!="file") {
        this.tableClass(item)
        this.curPath = item.path
        this.tableFilter.path = {id: this.curPath, name: this.curPath}
        this.tableRe()
      }
    },
    fileGoto (item) {
      if(this.editId===1) return false
        this.loadGlobal = true
        this.gotoPreview(item)
      if(item.type!="file") {
        this.tableClass(item)
        this.curPath = item.path
        this.getData(this.curPath)
      }
    },
		tableRe(){
      if(this.TabForm){
        this.tableList = []
        this.$refs.table.Re()
        this.loadGlobal = false
      }else{
        this.getData(this.curPath)
      }   
		},
		EditName (item) {
      if(this.editId===1) return false
      this.editId = item.id
      this.editName = item.name
      this.newName = item.name;		
		},
		download (item) {
      if(this.editId===1) return false
      window.open('/api/ssa/file_manage/download?path='+item.path)
		},
		deleteFile(item,i){
      if(this.editId===1) return false
      this.loadGlobal = true
      this.$http.delete('/api/ssa/file_manage',{
        path: item.path
      }).then((response) => {
        let res = response.data;
        if (res.status == 200) {
          if(this.TabForm){
            this.tableRe()
          }
          this.tableList.splice(i,1)
          this.loadGlobal = false
        } else {
          this.$root.alertError = true;
          this.$root.errorMsg = response.data.msg
          this.loadGlobal = false
        }  
      }, function (response) {
        Api.user.requestFalse(response, this);
      })
    },
    deleteFileAll () {
      let paths = [];
      this.tableList.forEach((item,index)=>{
        if(item.type=="file"&&item.selected){
          paths.push(item.path)
        }
      })
      if(paths.length===0) {
        this.$root.errorMsg = '无可删除内容'
        this.$root.alertError = true;
        return false;
      }
      this.loadGlobal = true
      this.$http.delete('/api/ssa/file_manage',{
        paths: paths
      }).then((response) => {
        let res = response.data;
        if (res.status == 200) {
          if(this.TabForm){
            this.tableRe()
          }
            this.getData(this.curPath)
        } else {
          this.$root.alertError = true;
          this.$root.errorMsg = response.data.msg
        }
      }, function (response) {
        Api.user.requestFalse(response, this);
      })
    },
		removeFile (item,bl) {
      let oldName = item.name;
			if(bl){
				if(item.name!=''){
          if(item.newFile==true){
            this.tableList.shift()
          }
          item.name = oldName
        }else{
          this.tableList.shift()
        }   
        this.editId = 0
			}else{
        item.name = this.newName
        if(this.newName==""){
          this.$root.errorMsg = '文件夹名称不能为空'
          this.$root.alertError = true;
          return false;
        }
        if(this.newName == oldName){
          this.editId = 0
          return false;
        }
        if(this.editName!=item.name&&this.editName!=""){//修改   
          this.loadGlobal = true  
          this.$http.put('/api/ssa/file_manage',{
            old_name: this.curPath+'/'+this.editName,
            new_name: this.curPath+'/'+item.name
          }).then((response) => {
            let res = response.data;
            if (res.status == 200) {
              if(this.TabForm){
                this.tableRe()
              }else{
                this.getData(this.curPath)
              }  
              this.editId = 0
            } else {
              this.$root.alertError = true;
              this.$root.errorMsg = response.data.msg
              this.loadGlobal = false
              item.name = oldName
            }
            
          }, function (response) {
            Api.user.requestFalse(response, this);
          })
        }else{//新建
          this.loadGlobal = true
          this.$http.post('/api/ssa/file_manage',{
            path: this.curPath +'/'+ item.name
          }).then((response) => {
            let res = response.data;
            if (res.status == 200) {
              if(this.TabForm){
                this.tableRe()
              }
                this.getData(this.curPath)
                item.id = item.name
                this.editId = 0
            } else {
              this.$root.alertError = true;
              this.$root.errorMsg = response.data.msg
              this.loadGlobal = false;
              this.editId = 1
            }
            
          }, function (response) {
            Api.user.requestFalse(response, this);
          })
        }
			}
		}
	}
}
</script>