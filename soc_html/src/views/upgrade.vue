<template>
  <div>
    <span class="ys-file-box d-i-b">
      <span class="file-name d-i-b">{{filename}}</span>
      <span class="ys-file-btn d-i-b" @click="selFile()">
        <i class="glyphicon glyphicon-folder-close"></i>选择文件
        <div class="form-group d-none">
          <form enctype="multipart/form-data" method="post">
            <input id="input_file" type="file"
                   @change="bindFile" class="form-control">
          </form>
        </div>
      </span>
    </span>
    <button class="ys-btn m-r-10" @click="saveUpdate">更新</button>
  </div>
</template>

<script>
  import Api from 'src/lib/api'
  export default {
    data () {
      return {
        filename: '',
        file: new FormData()
      }
    },
    ready: function () {

    },

    methods: {
      selFile() {
        $("#input_file").click()
      },
      bindFile(e){
        e.preventDefault();
        this.file.append('binfile', e.target.files[0]);
        this.filename=e.target.files[0].name;
      },
      saveUpdate(){
        this.$http.post('/api/upgrade', this.file).then(function (response) {
          this.$root.loadStatus = false;
          if (response.data.status == 200) {
            this.$root.alertSuccess = true;
            this.$root.errorMsg = "添加成功!";
          } else {
            this.$root.alertError = true;
            this.$root.errorMsg = response.data.msg;
          }
        }, function (response) {
          Api.user.requestFalse(response,this);
        });
      }
    },
    components: {}

  }
</script>