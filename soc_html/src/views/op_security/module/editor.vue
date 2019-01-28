<template>
  <div style="width:600px;" id="ys-editor-{{id}}">
    <p>
      <button class="ys-btn ys-btn-op m-r-20" @click="selImg()">插入图片</button>
      <button class="ys-btn ys-btn-op" @click="insertText()">插入文字</button>
    </p>
    <div class="form-group d-none">
      <form enctype="multipart/form-data" method="post">
        <input id="fileUploadFile" type="file" @change="bindFile" class="form-control">
      </form>
    </div>
    <div class="editor-box m-t-10">
      <div class="editor-box-con">
        <div class="editor-show">
        </div>
        <div class="editor-edit">
          <p class='editor-text' v-if="textStatus">
            <textarea class='ys-textarea m-t-5' v-model="curText"></textarea>
            <button class='ys-btn ys-btn-s ys-btn-blue sure' @click="sureText()">确定</button>
            <button class='ys-btn ys-btn-s ys-btn-white quit' @click="quitText()">取消</button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .editor-box{
    width:100%;
    border-radius: 3px;
    border: 1px solid rgba(74,146,255,0.2);
    box-shadow: inset 1px 1px 3px 0px rgba(0,0,0,0.2);
    background: rgba(0,0,0,0.2);
    min-height: 200px;
    padding: 0px 5px;
    display: inline-block;
    white-space: normal !important;
    word-break: break-all;
    word-wrap: break-word;
    cursor: text;
  }
  .editor-text{
    position: relative;
  }
  .editor-text button{
    position:absolute;
    right:2px;
    bottom:8px;
  }
  .editor-text button.sure{
    right:50px;
  }
</style>
<script>
  export default {
    props: {
      id: {
        default: ""
      },
      data:{
        default: ""
      }
    },
    data () {
      return {
        textStatus:false,
        curText:""
      }
    },
    ready(){
      let self=this;
      $("#ys-editor-"+self.id+" .editor-box-con").slimScroll({
        height: '500',
        position: 'right',
        size: "5px",
        color: '#4a92ff',
        opacity: 1,
        railColor: '#232027',
        railOpacity: 1,
        wheelStep: 5,
        start:"bottom",
      })
    },
    methods:{
      selImg(){
        let self=this;
        $("#ys-editor-"+self.id+" #fileUploadFile").click()
      },
      bindFile(e){
        e.preventDefault();
        let self=this;
        var reader = new FileReader();
        reader.readAsDataURL(e.target.files[0]); // 读取文件
        reader.onload = function (arg) {
          $("#ys-editor-"+self.id+" .editor-show").append("<p class='m-t-10'><img src='"+arg.target.result+"' style='max-width:600px;'/></p>");
          self.data=$("#ys-editor-"+self.id+" .editor-show").html()
        }// 渲染文件
        setTimeout(function(){
          $("#ys-editor-"+self.id+" .editor-box-con").slimScroll({
            height: '500',
            position: 'right',
            size: "5px",
            color: '#4a92ff',
            opacity: 1,
            railColor: '#232027',
            railOpacity: 1,
            wheelStep: 5,
            start:"bottom",
            scrollTo:'99999px'
          })
          $("#ys-editor-"+self.id).find(".slimScrollBar").css({"top":"99999px"});
        },500)
      },
      insertText(){
        this.curText="";
        this.textStatus=true;
        setTimeout(function(){
          $("#ys-editor-"+self.id+" .editor-box-con").scrollTop(99999,0)
          $("#ys-editor-"+self.id).find(".slimScrollBar").css({"top":"99999px"});
        },500)
      },
      sureText(){
        this.textStatus=false;
        let self=this;
        $("#ys-editor-"+self.id+" .editor-show").append("<p class='m-t-10'>"+this.curText+"</p>");
        this.data=$("#ys-editor-"+self.id+" .editor-show").html();
      },
      quitText(){
        this.textStatus=false;
      },
      close(){
        this.show = false
      }
    },
    watch: {
      'data'(){
        $("#ys-editor-"+this.id+" .editor-show").html(this.data)
      }
    }
  }
</script>
