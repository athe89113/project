<template>
  <div class="ys-box" >
    <div v-bind:class="[showInfo ? 'ys-blur' : '']">
      <guides :step="stepData" :cur="curStep">
        <div slot="content">
          <div v-if="curStep==1">
            <radio :list="upgradeTypeData" :value.sync="upgradeType"></radio>
            <div class="ys-box-con bor-blue-bg-solid m-t-20 ys-info-color">
              <p v-if="upgradeType=='system'" class="fadeIn animated">选择此项可以升级中心系统控制台，新的中心系统可以提供更多的功能，修复BUG，及时更新带来更好的体验。</p>
              <p v-if="upgradeType=='event'" class="fadeIn animated">选择此项可以升级安全组件的事件库，新的事件库将包含更多的安全特征和安全信息，用于发现新的安全威胁或做出安全防御，及时更新保证安全能力处于最新状态。</p>
              <p v-if="upgradeType=='engine'" class="fadeIn animated">选择此项可以升级安全组件引擎，新的处理引擎将提供更先进，更准确，更高效的处理方法，及时更新保持最优效果。</p>
            </div>
            <p class="m-t-20"><button class="ys-btn" @click="curStep=2">下一步</button></p>
          </div>
          <div v-if="curStep==2">
            <table class="ys-form-table">
              <tr>
                <td class="ys-info-color">添加升级文件</td>
                <td>
                  <span class="ys-file-input">
                    <input class="ys-input"
                           style="width:260px;"
                           placeholder="选择文件"
                           v-model="fileName"/>
                    <i class="ys-icon icon-file ys-primary-color text-cursor"  @click="clickFileBtn()"></i>
                    <div class="form-group d-none">
                      <form enctype="multipart/form-data" method="post">
                        <input id="select_upgrade_file" class="ys-input" type="file" @change="selectFile" class="form-control">
                      </form>
                    </div>
                  </span>
                  <span v-bind:class="[fileBtnStatus ? '' : 'disabled']">
                    <button class="ys-btn ys-btn-blue ys-btn-s m-l-5" @click="uploadFile">上传</button>
                  </span>
                </td>
              </tr>
            </table>
            <div style="height:60px;">
              <div v-show="fileProgress>=0">
                <p class="m-t-20 textC" style="width:500px">
                  <span v-if="fileUploadStatus==0">
                    <loading-mini :show="true"></loading-mini>
                    <span v-if="fileUpgradeStep==0" class="verticalM m-l-5">等待上传</span>
                    <span v-if="fileUpgradeStep==1" class="verticalM m-l-5">正在上传</span>
                    <span v-if="fileUpgradeStep==2" class="verticalM m-l-5">暂存文件</span>
                    <span v-if="fileUpgradeStep==3" class="verticalM m-l-5">校验文件</span>
                    <span v-if="fileUpgradeStep==4" class="verticalM m-l-5">检查版本</span>
                  </span>
                  <span v-if="fileUploadStatus==2">{{fileErrorMsg}}</span>
                  <span v-if="fileUploadStatus==1">升级文件正常，升级包为{{upgradeType | upgradeTypeFil}}升级包，版本为{{fileVersion}}，构建时间{{fileBuildDate}}</span>
                </p>
                <div class="ys-load-step-con m-t-10" style="width:500px">
                  <p class="progress-box progress-box-active"
                     v-bind:style="{width: fileProgress + '%'}"></p>
                </div>
                <p class="m-t-5 textC" style="width:500px">{{fileProgress}}%</p>
              </div>
            </div>
            <p class="m-t-20" v-bind:class="[fileUploadStatus==1 ? '' : 'disabled']"><button class="ys-btn" @click="curStep=3">下一步</button></p>
          </div>
          <div v-if="curStep==3">
            <p><i class="ys-icon icon-info-circle m-r-5 ys-primary-color"></i><span class="ys-info-color">本级中心升级后才能升级下级中心</span></p>
            <div class="tree pos-r">
              <div class="iconDes ys-box-con bor-blue-bg-solid">
                <p>
                  <span class="bg"><i class="ys-icon icon-core"></i></span>
                  <span class="ys-info-color m-l-5">中心服务器</span>
                </p>
                <p class="m-t-10">
                  <span class="bg"><i class="ys-icon icon-defense"></i></span>
                  <span class="ys-info-color m-l-5">高防服务器</span>
                </p>
                <p class="m-t-10">
                  <span class="bg"><i class="ys-icon icon-internet"></i></span>
                  <span class="ys-info-color m-l-5">网络安全服务器</span>
                </p>
                <p class="m-t-10">
                  <span class="bg"><i class="ys-icon icon-monitor"></i></span>
                  <span class="ys-info-color m-l-5">监控服务器</span>
                </p>
                <p class="m-t-10">
                  <span class="bg"><i class="ys-icon icon-scan"></i></span>
                  <span class="ys-info-color m-l-5">漏扫服务器</span>
                </p>
                <p class="m-t-10">
                  <span class="bg"><i class="ys-icon icon-cloud"></i></span>
                  <span class="ys-info-color m-l-5">云防服务器</span>
                </p>
                <p class="m-t-10">
                  <span class="bg"><i class="ys-icon icon-computer"></i></span>
                  <span class="ys-info-color m-l-5">终端安全服务器</span>
                </p>
              </div>
              <topo :options="nodeTopo" :target="upgradeTarget"></topo>
            </div>
            <p class="m-t-10"><button class="ys-btn" @click="addUpgrade()">下一步</button></p>
          </div>
          <div v-if="curStep==4">
            <table class="ys-table" style="width:600px;">
              <thead>
              <tr>
                <th class="textL">名称</th>
                <th>当前版本</th>
                <th>升级版本</th>
                <th>进度</th>
              </tr>
              </thead>
              <tbody>
              <tr class="odd" v-for="list in upgradeList">
                <td class="textL">{{list.name}}</td>
                <td>{{list.current_version}}</td>
                <td>{{list.upgrade_version}}</td>
                <td>
                  <percent :data="list.percent"></percent>
                  <span style="width:60px;" class="d-i-b textL">
                    <span class="ys-success-color m-l-5" v-if="list.status==1"><i class="ys-icon icon-check-circle"></i></span>
                    <span class="ys-error-color m-l-5" v-if="list.status==2"><i class="ys-icon icon-clear-circle"></i></span>
                    <a class="m-l-5" v-if="list.status==2" @click="retryUpgrade(list)">重试</a>
                  </span>

                </td>
              </tr>
              </tbody>
            </table>
            <p class="m-t-15"><i class="ys-icon icon-info-circle m-r-5 ys-primary-color"></i><span class="ys-info-color">如果升级失败请联系厂商进行处理</span></p>
            <p class="m-t-20"><button class="ys-btn" @click="curStep=4">完成,并查看级联状态</button></p>
          </div>
        </div>
      </guides>
    </div>
    <ys-info :show.sync="showInfo"
             :title="infoTitle">
      <div slot="content">
        <p class="d-none">{{infoTitle}}</p>
        <p class="textC m-t-15"><i class="ys-icon icon-help-circle m-r-5 ys-primary-color"></i><span class="ys-info-color">我需要做什么？</span></p>
        <p class="textC m-t-10">中心系统更新后如果出现访问问题，请 清除浏览器缓存 后重新打开</p>
      </div>
      <div slot="footer">
        <button class="ys-btn" @click="reloadPage()">重新加载页面</button>
      </div>
    </ys-info>
  </div>
</template>
<style scoped>
  .iconDes{
    position:absolute;
    right:15px;
    top:0px;
  }
  .iconDes p .bg{
    width:18px;
    height:18px;
    background:#4a92ff;
    line-height:18px;
    display: inline-block;
    border-radius: 2px;
    text-align: center;
    line-height:18px;
  }
  .iconDes p .bg i{
   color:#4f4552;
  }
  .ys-load-step-con {
    height: 4px;
    background: #45536e;
    width: 100%;
    position: relative;
    border-radius: 3px;
  }

  .progress-box {
    width: 50%;
    height: 4px;
    position: absolute;
    top: 0px;
    left: 0px;
    border-radius: 3px;
    background: #00bd85;
    transition: 1.5s width ease-in;
  }

  .progress-box-active:before {
    content: "";
    opacity: 0;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: #fff;
    border-radius: 3px;
    animation: ys-progress-active 2s ease-in-out infinite;
  }

  @keyframes ys-progress-active {
    0% {
      opacity: .5;
      width: 0;
    }
    100% {
      opacity: .2;
      width: 100%;
    }
  }
  .upAndDown{
    position:absolute;
    width:100%;
    height:100%;
    left:0px;
    top:0px;

  }
</style>
<script>
  import Api from 'src/lib/api'
  import topo from './topo.vue'
  export default {
    name: "upgrade-mgt",
    data() {
      return {
        hasUpgradeStatus:false,
        upgradeList:[],
        curStep:1,
        stepData:[
          {step:1,before:"选择升级组件",after:"选择升级组件"},
          {step:2,before:"上传升级文件",after:"上传升级文件"},
          {step:3,before:"选择升级范围",after:"选择升级范围"},
          {step:4,before:"更新升级",after:"更新升级"}
        ],
        upgradeTypeData:[
          {id:"system",text:"升级系统"},
          {id:"event",text:"升级事件库"},
          {id:"engine",text:"升级引擎"}
        ],
        upgradeType:"system",
        fileBtnStatus:false,
        fileName:"",
        fileProgress:-1,
        fileUpgradeStep:0,//0 - 等待上传 1 - 正在上传 2 - 暂存文件 3 - 校验文件 4 - 检查版本 5 - 完成
        progressId:0,//进程ID，可以用来获取上传进度
        fileData:{},
        fileId:"",//升级文件ID
        fileVersion:"",//版本
        fileBuildDate:"",//构建时间
        fileUpgradeType:"",//检测出的文件升级类型
        fileUploadStatus:"",
        fileErrorMsg:"",
        uploadSuccess:false,
        nodeTopo:[],
        addList:[],
        showInfo:false,
        infoTitle:"",
        statusRepeat:{},
        upgradeTarget:[],
        centerData:{},
        centerStatus:false
      }
    },
    ready: function() {
      this.getUpgradeList()
    },
    filters: {
      upgradeTypeFil: function (type) {
        switch(type) {
          case "system":
            return "系统"
            break;
          case "event":
            return "事件库"
            break;
          case "engine":
            return "引擎"
            break;
          default:
            return "系统"
        }
      },
    },
    methods:{
      clickFileBtn(){
        $("#select_upgrade_file").click();
      },
      selectFile(e){
        e.preventDefault();
        this.fileData=new FormData();
        this.fileData.append('upgrade_file', e.target.files[0]);
        this.fileName=e.target.files[0].name;
        this.progressId=Math.random().toString().slice(-6);
        this.fileBtnStatus=true;
      },
      uploadFile(){
        this.fileProgress=0;
        this.fileData.delete('upgrade_type');
        this.fileData.append('upgrade_type',this.upgradeType);
        let self=this;
        var xhr = new XMLHttpRequest();
        // 获取上传进度
        xhr.open('POST', '/api/system/upgrade/file/upload?progress_id='+this.progressId);
        xhr.upload.onprogress = function (event) {
          if (event.lengthComputable) {
            var percent = Math.floor(event.loaded / event.total * 100) ;
            // 设置进度显示
            if(percent%2==0){
              self.fileProgress=percent*0.5
            }
            if(percent==100){
              self.statusRepeat=setInterval(function(){
                self.getProgress()
              },3000)
            }
          }
        };
        xhr.onreadystatechange = function(){
          if ( xhr.readyState == 4 && xhr.status == 200 ) {
            let response=JSON.parse(xhr.responseText);
            let data=response.data;
            if(response.status==200){
              self.fileBuildDate=data.build_date;
              self.fileId=data.file_id;
              self.fileVersion=data.version;
              self.fileUpgradeType=data.u_type;
              self.upgradeType=data.upgrade_type

            }else{
              self.fileErrorMsg=data.error;
            }
          }
        };
        xhr.send(this.fileData);
      },
      getProgress(){
        let postData={progress_id:this.progressId}
        this.$http.get('/api/system/upgrade/file/upload', postData).then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data;
            this.fileProgress=data.percent;
            this.fileUploadStatus=data.status;
            this.fileUpgradeStep=data.step;
            this.fileErrorMsg=data.error_msg;
            if(data.status==1){
              clearInterval(this.statusRepeat)
              this.getTopoList()
            }
          } else {
            this.$root.errorMsg = response.data.msg
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getTopoList(){
        let data={
          u_type:this.fileUpgradeType,
          file_id:this.fileId
        }
        this.$http.get('/api/system/upgrade/nodes', data).then(function (response) {
          if (response.data.status == 200) {
            let data=[];
            data.push(response.data.data)
            function getArray(arr) {
              for(var i=0;i<arr.length;i++){
                if(arr[i].status == 1) {
                  arr[i].select=false;
                }
                if(i==arr.length-1 && arr[i].children) {
                  getArray(arr[i].children);
                }
              }
              return arr;
            }
            this.nodeTopo=getArray(data);
          } else {
            this.$root.errorMsg = response.data.msg
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      showReload(){
        this.showInfo=true;
        let self=this;
        self.infoTitle="升级成功, 10秒后将自动刷新页面"
        if(self.showInfo){
          let num=10;
          let repeat=setInterval(function(){
            num--;
            if(num==0){
              clearInterval(repeat)
              self.reloadPage();
            }else{
              self.infoTitle= "升级成功, "+num+"秒后将自动刷新页面"
            }
          },1000)
        }else{
          return ""
        }
      },
      reloadPage(){
        window.location.reload()
      },
      addUpgrade(){
        let self=this;
        function getArray(arr) {
          for(var i=0;i<arr.length;i++){
            if(arr[i].select) {
              self.upgradeTarget.push({"uuid":arr[i].uuid,id:arr[i].id})
              if(arr[i].is_self==1){
                self.centerStatus=true;
                self.centerData=arr[i];
              }
            }
            if(i==arr.length-1 && arr[i].children) {
              getArray(arr[i].children);
            }
          }
          return arr;
        }
        getArray(this.nodeTopo);
        let data={
          file_id: this.fileId,
          u_type: this.fileUpgradeType,
          targets:this.upgradeTarget
        }
        this.$root.loadStatus=true;
        this.$http.post('/api/system/upgrade', data).then(function (response) {
          if (response.data.status == 200) {
            this.$root.loadStatus=false;
            this.curStep=4;
            if(this.centerStatus){
              this.upgradeSelfCenter()
            }else{
              this.getUpgradeList()
            }
          } else {
            this.$root.errorMsg = response.data.msg
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      upgradeSelfCenter(){
        this.upgradeList.push({
          name:this.centerData.name,
          current_version:this.centerData.version,
          upgrade_version:this.fileVersion,
          percent:0
        })
        let self=this;
        let repeat=setInterval(function(){
          self.upgradeList[0].percent++
          if(self.upgradeList[0].percent==100){
            self.showReload();
            clearInterval(repeat)
          }
        },1000)
      },
      getUpgradeList(){
        this.$http.get('/api/system/upgrade/list').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data;
            if(data.status==1){
              this.curStep=4;
              this.upgradeList=data.list;
            }else{

            }
          } else {
            this.$root.errorMsg = response.data.msg
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      retryUpgrade(list){
        let data={task_id:list.task_id}
        this.$http.post('/api/system/upgrade/retry',data).then(function (response) {
          if (response.data.status == 200) {
            this.getUpgradeList();
          } else {
            this.$root.errorMsg = response.data.msg
            this.$root.alertError = true;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      }
    },
    components: {
      topo
    }
  }
</script>
